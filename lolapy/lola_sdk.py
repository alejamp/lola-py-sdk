
import asyncio
import threading
import requests
from flask import Flask, request
import json
import os
from lolapy.lola_context import LolaContext
from lolapy.lola_logtail import connectLogTail, syncConnectLogTail
from lolapy.lola_timeout import LolaTimeout
from lolapy.lola_utils import get_invariant_hash



class LolaSDK:
    def __init__(self, lola_token=None, webhook_url=None, prompter_url=None, host='localhost', port=5000, path='/event'):
        self.lola_token = lola_token or os.environ.get('LOLA_TOKEN')
        self.webhook_url = webhook_url
        self.prompter_url = prompter_url or os.environ.get('PROMPTER_URL', 'http://localhost:4000')
        self.host = host
        self.port = port
        self.path = path
        self.cmd_handlers = {}
        self.event_handlers = {}
        self.timeout_handler = None
        self.callback_handlers = {}
        self.events = []
        self.timeout = None

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
        print('Webhook registered')
        # Show list of events to listen:
        print(f'Listening to events: {self.events}')

        # Start timeout thread
        if self.timeout:
            self.timeout.start()

        # Start Flask server
        app = Flask(__name__)

        @app.route('/event', methods=['POST'])
        def handle_event():
            # Example event:
            # '{
            # "lead": {"botName": "lola_chatwoot_test_bot", "tenantId": "0Leo0rEyx6t6U3pP6p7j", "assistantId": "1ZtZEM8bZGsMUBUf9YuXEf", "channelSource": "telegram", "metadata": {}, "signature": "3cb6e52fbf72dbe649f9fac7d184dc75ca327b90f9ef3204d4b5921b90db3e1f", "chatId": 1320141990}, 
            # "event": "onCommand", 
            # "data": {"name": "get_cryptocurrency_price", "args": {"cryptocurrency": "ETH", "currency": "USD"}}
            # }'
            print('Received event')
            print(request)
            event = request.json
            if event is None:
                return self.on_error('Invalid event')   
            
            session = self.__getSession(event['lead'])
            ctx = self.context(session)
            result = self.__process_event(session, ctx, event)
            return json.dumps(result), 200, {'Content-Type': 'application/json'}


        if (debug):
            print('Starting logtail thread!!!!!!')
            download_thread = threading.Thread(target=syncConnectLogTail, name="Logtail", args=(self.prompter_url, self.lola_token,))
            download_thread.start()

        app.run(host=self.host, port=self.port)

    def context(self, session):
        return LolaContext(session, self.lola_token, self.prompter_url, self.timeout)
    
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
    
    def on_timeout(self):
        def decorator(handler):
            print ('LolaSDK -> Setting timeout handler')
            self.timeout = LolaTimeout(handler)
            return handler
        return decorator

    def __getSession(self, lead):
        # generate hash as a unique identifier for this lead
        hlead = get_invariant_hash(lead)
        session = {
            'id': hlead,
            'lead': lead,
        }
        return session

    def __process_event(self, session, ctx, event):

        event_type = event.get('event')
        if event_type == 'onCommand':
            command_name = event['data'].get('name')
            if command_name in self.cmd_handlers:
                return self.cmd_handlers[command_name](session, ctx, event)
            
        if event_type in self.event_handlers:
            return self.event_handlers[event_type](session, ctx, event['data']['message'])
        
        return self.on_error(f'Unknown event type: {event_type}')
    
    def on_error(self, error):
        raise NotImplementedError




