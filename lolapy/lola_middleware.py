from abc import ABC, abstractmethod
import json

from lolapy.lola_context import LolaContext

class Middleware(ABC):
    @abstractmethod
    def process_request(self, session, ctx: LolaContext, req):
        """Called when a request is received from Lola backend:
        - onTextMessage
        - onImage
        - onNewConversation
        - onCommand
        - onClientCommand
        """
        pass




if __name__ == '__main__':
    

    class MyMiddleware(Middleware):
        def process_request(self, session, ctx: LolaContext, req):
            req['__text'] = 'Hello from middleware'
            # return req
        

    class MyMiddleware2(Middleware):
        def process_request(self, session, ctx: LolaContext, req):
            req['__text2'] = 'Hello from middleware2'
            # return req
        
    middlewares = [MyMiddleware(), MyMiddleware2()]


    req = {
        'text': 'Hello world'
    }
    for middleware in middlewares:
        middleware.process_request(None, None, req)
        print(req)


    # show results in json
    print('---------------------')
    print(json.dumps(req, indent=4))        