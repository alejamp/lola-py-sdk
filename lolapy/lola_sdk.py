import threading
import requests
from flask import Flask, request
import json
from colorama import Fore, Style
from lolapy.lola_agent_manager import LolaAgentManager
from lolapy.lola_context import LolaContext
from lolapy.lola_logtail import connectLogTail, syncConnectLogTail
from lolapy.lola_middleware import Middleware
from lolapy.lola_response import ResponseText
from lolapy.lola_timeout import LolaTimeout
from lolapy.lola_token import decode_lola_token
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
        # CLIENT_COMMAND by Ale
        self.client_cmd_handlers = {}
        self.event_handlers = {}
        self.notification_handlers = {}
        self.timeout_handler = None
        self.callback_handlers = {}
        self.events = []
        self.middlewares = []
        self.timeout = None
        self.redis_url = redis_url
        self.promptstr = ""
        self.promptstate = {}
        self.agent_manager = LolaAgentManager(lola_token, prompter_url)
        # print init info
        print(f'LOLA_TOKEN: {self.lola_token}')
        print(f'WEBHOOK_URL: {self.webhook_url}')
        print(f'PROMPTER_URL: {self.prompter_url}')
        print(f'HOST: {self.host}:{self.port}')
        print(f'REDIS_URL: {self.redis_url}')

    def request_chat_completion(self, userId, text):
        self.agent_manager.completion(userId, text)


    def onInitilize(self, promptId, prompt):
        ## extract the file promp.hbr and the file state.js from the root path
        with open(f"{prompt}.hbr") as promptFile:
            self.promptstr = str(promptFile.read())
        
        print (f"promptstr: ok")
        with open(f"{prompt}.state.json") as state:
            self.promptstate = json.load(state)
        print (f"promptstate: ok")
        promptManager = LolaPromptManager(lola_token=self.lola_token, prompter_url=self.prompter_url)
        try:
            promptManager.publishPrompt(promptid=promptId,promptName=promptId,promptFileContent=self.promptstr,state=self.promptstate)
        except Exception as e:
            print(f'Error publishing prompt: {e}')
        pass          

    def listen(self, debug=False, disableWebServer=False):

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

        # Skip web server if Flask disableWebServer is True
        if disableWebServer == True:
            print(f'{Fore.YELLOW}WRN: Lola\'s Flask Web server disabled{Style.RESET_ALL}')
            return
        
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

            result = self.process_event(event)
            return json.dumps(result), 200, {'Content-Type': 'application/json'}


        if (debug):
            print(f'{Fore.RED}Debug mode enabled: starting logtail thread!{Style.RESET_ALL}')
            print(f'{Fore.RED}This mode is not recommended in prodcution{Style.RESET_ALL}')
            download_thread = threading.Thread(target=syncConnectLogTail, name="Logtail", args=(self.prompter_url, self.lola_token,))
            download_thread.start()

        app.run(host=self.host, port=self.port)


    def process_event(self, event):
        if event is None:
            return self.on_error('Invalid event') 

        print(f'Processing event: {event}')  
        session = self.__buildSession(event['lead'])
        ctx = self.context(session)
        return self.__process_event(session, ctx, event)


    def register_middleware(self, middleware: Middleware):
        """Register a middleware to process events and commands or client commands.
        It supports multiple middlewares."""
        if not isinstance(middleware, Middleware):
            raise TypeError('Middleware must be an instance of Middleware class')
        
        if middleware not in self.middlewares:
            self.middlewares.append(middleware)
        else:
            raise Exception('Middleware already registered')

    
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
    
    # CLIENT_COMMAND by Ale
    def on_client_command(self, name):
        def decorator(handler):
            self.add_event('onClientCommand')
            self.client_cmd_handlers[name] = handler
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

        # process middlewares
        skip = False
        for middleware in self.middlewares:
            res = middleware.process_request(session, ctx, event)
            # if middleware returns False, skip event processing
            # keep processing if middleware returns None or True
            if res == False:
                skip = True

        # skip event processing if a middleware returns False
        if skip:
            return ResponseText('').DisableAI().Send()

        if event_type == 'onCommand':
            command_name = event['data'].get('name')
            if command_name in self.cmd_handlers:
                return self.cmd_handlers[command_name](session, ctx, event)
            
        if event_type == 'onNotification':
            notification_name = event['data'].get('name')
            if notification_name in self.notification_handlers:
                return self.notification_handlers[notification_name](session, ctx, event)
        
        # CLIENT_COMMAND by Ale
        if event_type == 'onClientCommand':
            command_name = event['data'].get('name')
            if command_name in self.client_cmd_handlers:
                return self.client_cmd_handlers[command_name](session, ctx, event)
            
            # no handler found
            # print(f'No handler found for command: {command_name}')
            print(f'{Fore.YELLOW}WRN: No handler found for command: {command_name}{Style.RESET_ALL}')
            # raise error no handler for client command
            raise NotImplementedError(f'No handler found for command: {command_name}')
            

            
        if event_type in self.event_handlers:
            if self.handler_has_4_args(self.event_handlers[event_type]):
                return self.event_handlers[event_type](session, ctx, event['data']['message'], event)
            else:
                return self.event_handlers[event_type](session, ctx, event['data']['message'])
        
        return self.on_error(f'Unknown event type: {event_type}')
    
    def on_error(self, error):
        print(f'{Fore.YELLOW}WRN: {error}{Style.RESET_ALL}')
        raise NotImplementedError


    def handler_has_4_args(self, handler):
        return handler.__code__.co_argcount == 4


