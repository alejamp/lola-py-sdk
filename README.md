# Lola v2 Python SDK

This project is a Python SDK for the Prompter API. It is intended to be used by developers who want to integrate Lola into their own applications.

## Installation

``` pip install lola-py-sdk ```

## Usage

```python

from lola import LolaSDK
from lola import LolaContext


token = "YOUR_ASSISTANT_TOKEN_HERE"
lola = LolaSDK(lola_token=token, webhook_url='http://localhost:5000', promter_url="PROMPTER_API_URL_HERE")
```

Where `webhook_url` is the URL of your webhook endpoint. This is where Lola will send the response to your request.
By default, the webhook URL is set to `http://localhost:5000`. If you are running the SDK locally, you can use this URL.

If you are running Promtper API externally, you will need to set up a public URL for your webhook endpoint. You can use a service like [ngrok](https://ngrok.com/) to do this. Then you can set the webhook URL to the URL provided by ngrok.

Set prompter_url to the URL of your Prompter API instance. If you are running Prompter API locally, you can use `http://localhost:8080`. Remote instances of Prompter API will require a public URL. **This service will be provided by Lola.**


### Register for commands

Lola Python SDK provides a decorator to register your functions as commands. The decorator takes a command name as an argument. This is the name of the command that you will use to call your function from Lola.

```python
@lola.on_command('get_cryptocurrency_price')
def hanfler(lead, ctx: LolaContext, request):
```


For example if you register a function with the command name `get_cryptocurrency_price`, you can call it from Lola like this:

```python
@lola.on_command('get_cryptocurrency_price')
def handle_get_cryptocurrency_price(lead, ctx: LolaContext, request):
    cryptocurrency = request['data']['args']['cryptocurrency']
    currency = request['data']['args']['currency']

    # dict with data to return to Lola
    prices = {
        'ETH': 600,
        'BTC': 20000,
        'LTC': 100,
        'ADA': 1.5        
    }

    # if cryptocurrency is not in prices, return error
    if cryptocurrency not in prices:
        return {'data': f'Cryptocurrency {cryptocurrency} not supported'}
    
    return {'data': f'{cryptocurrency} price in {currency} is {prices[cryptocurrency]}'}

```

The arguments to the function are:
 - lead: The lead object from Prompter API that allows you to access the message routung information. 
 - ctx: The LolaContext object that allows you to access the user's context such as state, history and messanger
 - request: The request object from Prompter API that contains the data sent by Lola in this case the command and arguments


### Register to events

Lola Python SDK provides decorators to register your functions to events. The decorator takes an event name as an argument. This is the name of the event that you will use to call your function from Lola.

```python
@lola.on_event('onTextMessage')
```

```python 
@lola.on_event('onTextMessage')
def handle_text_message(lead, ctx: LolaContext, msg):
    
    print(f'Got text message: {msg["text"]}')
    s = ctx.state.get()
    print(f'Current state: {s}')
    ctx.state.set({'counter': s.get('counter', 0) + 1})

    # Testing send message to client
    # This message will be sent to the client
    # But it will not interrupt the flow to the AI
    # Use this to send messages to the client without interrupting the flow
    ctx.messanger.send_text_message(f'You said1: {msg["text"]}') 

    # Testing send message to client
    # This message will be sent to the client
    # And it will interrupt the flow to the AI
    # return f'You said2: {msg["text"]}'
```


## Contributing

Guidelines for contributing to the project, including how to report bugs, suggest enhancements, and submit pull requests.

## License

A statement about the license under which the project is released.

## Credits

Lola Team
