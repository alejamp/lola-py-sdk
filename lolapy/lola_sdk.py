import threading
import requests
from flask import Flask, request
import json
from colorama import Fore, Style
from lolapy.lola_context import LolaContext
from lolapy.lola_logtail import connectLogTail, syncConnectLogTail
from lolapy.lola_timeout import LolaTimeout
from lolapy.lola_utils import get_invariant_hash
from lolapy.lola_prompt_manager import LolaPromptManager



class LolaSDK:
    def __init__(self, 
                 lola_token=None, 
                 webhook_url=None, 
                 prompter_url=None, 
                 host='localhost', 
                 port=5000, 
                 path='/event',
                 redis_url=None,
                 ):
        self.lola_token = lola_token 
        self.webhook_url = webhook_url
        self.prompter_url = prompter_url
        self.host = host
        self.port = port
        self.path = path
        self.cmd_handlers = {}
        self.event_handlers = {}
        self.notification_handlers = {}
        self.timeout_handler = None
        self.callback_handlers = {}
        self.events = []
        self.timeout = None
        self.redis_url = redis_url
        self.promptstr = ""
        self.promptstate = {}
        # print init info
        print(f'LOLA_TOKEN: {self.lola_token}')
        print(f'WEBHOOK_URL: {self.webhook_url}')
        print(f'PROMPTER_URL: {self.prompter_url}')
        print(f'HOST: {self.host}:{self.port}')
        print(f'REDIS_URL: {self.redis_url}')   
    def onInitilize(self, promptId, prompt):
        ## extract the file promp.hbr and the file state.js from the root path
        with open(f"{prompt}.hbr") as prompt:
            self.promptstr = str(prompt.read())
        print (f"promptstr: {self.promptstr}")
        with open(f"{prompt}.state.json") as state:
            self.promptstate = json.load(state)
        print (f"promptstate: {self.promptstate}")
        promptManager = LolaPromptManager(lola_token=self.lola_token, prompter_url=self.prompter_url)
        try:
            promptManager.publishPrompt(promptid=promptId,promptName=promptId,promptFileContent=self.promptstr,state=self.promptstate)
        except Exception as e:
            print(f'Error publishing prompt: {e}')
        pass     

    def listen(self, debug=False):

        if not self.lola_token:
            raise Exception('LOLA_TOKEN not set')
        
        if not self.webhook_url:
            raise Exception('WEBHOOK_URL not set')

        # check if self.events is empty
        # if not self.events:
        #     raise Exception('Events not set')
        
        # Register webhook
        url = f'{self.prompter_url}/api/webhook/register'
        headers = {'x-lola-auth': self.lola_token, 'Content-Type': 'application/json'}
        data = {'url': (self.webhook_url or '') + self.path, 'events': self.events}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f'{Fore.GREEN}Webhook registered: {self.webhook_url}{self.path}{Style.RESET_ALL}')
        # Show list of events to listen:
        print(f'Listening to events: {self.events}')

        # Start timeout thread
        if self.timeout:
            self.timeout.start()

        # Start Flask server
        app = Flask(__name__)

        @app.route('/health', methods=['GET'])
        def health_check():
            return 'OK'

        @app.route('/event', methods=['POST'])
        def handle_event():
            # Example event:
            # '{
            # "lead": {"botName": "lola_chatwoot_test_bot", "tenantId": "0Leo0rEyx6t6U3pP6p7j", "assistantId": "1ZtZEM8bZGsMUBUf9YuXEf", "channelSource": "telegram", "metadata": {}, "signature": "3cb6e52fbf72dbe649f9fac7d184dc75ca327b90f9ef3204d4b5921b90db3e1f", "chatId": 1320141990}, 
            # "event": "onCommand", 
            # "data": {"name": "get_cryptocurrency_price", "args": {"cryptocurrency": "ETH", "currency": "USD"}}
            # }'

            print(request)
            event = request.json
            if event is None:
                return self.on_error('Invalid event') 
            
            print(f'Received event: {event}')  
            
            session = self.__buildSession(event['lead'])
            ctx = self.context(session)
            result = self.__process_event(session, ctx, event)
            return json.dumps(result), 200, {'Content-Type': 'application/json'}


        if (debug):
            print(f'{Fore.RED}Debug mode enabled: starting logtail thread!{Style.RESET_ALL}')
            print(f'{Fore.RED}This mode is not recommended in prodcution{Style.RESET_ALL}')
            download_thread = threading.Thread(target=syncConnectLogTail, name="Logtail", args=(self.prompter_url, self.lola_token,))
            download_thread.start()

        app.run(host=self.host, port=self.port)

    def context(self, session):
        return LolaContext(session, self.lola_token, self.prompter_url, self.timeout, self.redis_url)
    
    def add_event(self, event):
        # check if event is already in self.events
        # if not, add it
        if event not in self.events:
            self.events.append(event)


    def on_command(self, name):
        def decorator(handler):
            self.add_event('onCommand')
            self.cmd_handlers[name] = handler
            return handler
        return decorator
    
    def on_event(self, name):
        def decorator(handler):
            self.add_event(name)
            self.event_handlers[name] = handler
            return handler
        return decorator
    
    def on_notification(self, name):
        def decorator(handler):
            self.add_event('onNotification')
            self.notification_handlers[name] = handler
            return handler
        return decorator
    
    def on_timeout(self):
        def decorator(handler):
            print ('LolaSDK -> Setting timeout handler')
            self.timeout = LolaTimeout(handler)
            return handler
        return decorator

    def __buildSession(self, lead):
        # generate hash as a unique identifier for this lead
        hlead = get_invariant_hash(lead)
        session = {
            'id': hlead,
            'lead': lead,
        }
        return session

    def __process_event(self, session, ctx, event):
        
        event_type = event.get('event')

        print(f'Processing event: {event_type}')

        print(f'Event data: {event["data"]}')

        if event_type == 'onCommand':
            command_name = event['data'].get('name')
            if command_name in self.cmd_handlers:
                return self.cmd_handlers[command_name](session, ctx, event)
            
        if event_type == 'onNotification':
            notification_name = event['data'].get('name')
            if notification_name in self.notification_handlers:
                return self.notification_handlers[notification_name](session, ctx, event)
        
            
        if event_type in self.event_handlers:
            return self.event_handlers[event_type](session, ctx, event['data']['message'])
        
        return self.on_error(f'Unknown event type: {event_type}')
    
    def on_error(self, error):
        raise NotImplementedError




