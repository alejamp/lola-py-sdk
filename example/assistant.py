#---------------------------------------------------------------------------------------------------
# COIN GURU
# Virtual Assistant based on Lola Platform
#---------------------------------------------------------------------------------------------------
# This is a simple example of how to use 
# Lola SDK to build an AI Virtual Assistant that can answer questions related 
# to the cryptocurrency market.
# Features:
# - Get the price of a cryptocurrency in a specific currency
# - Restrict the assests to the "BTC", "ETH", "ADA", "DOT", "XRP", "LTC", checkout prompt.state.json
# - Implement limits on the number of requests per user based on credits (tokens are used as credits)
#---------------------------------------------------------------------------------------------------

import sys
import os
from crypto import get_crypto_prices_from_list

# Get the parent directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the Python module search path
sys.path.append(parent_dir)
sys.path.append(parent_dir + '/lolapy')

import os
from time import sleep, time
from auth_middleware import AuthMiddleware
from lolapy import LolaSDK
from lolapy import LolaContext
from lolapy import ResponseText, ResponseImage
import requests
import json
from dotenv import dotenv_values


config = {
    **dotenv_values("example/.env"),    # load development variables
    **os.environ,                       # override loaded values with environment variables
}

# Create a new instance of Lola SDK
# Lola SDK will listen for events and commands from the selected Assistant
lola = LolaSDK(
    lola_token=config['ASSISTANT_TOKEN'],
    prompter_url=config['PROMPTER_URL'],
    # Set to HOST env var to 0.0.0.0 on Railways or Heroku or any other cloud provider
    host=config['HOST'],  
    port=int(config['PORT']),
    # this must be a public url, you can use ngrok to expose your localhost, check README.md
    webhook_url=config['WEBHOOK_URL'],
    # Optional for Session Store into Redis instead of local memory
    # redis_url=config['REDIS_URL']
)

# Register middlewares
# --------------------------------------------------------
auth_middleware = AuthMiddleware()
lola.register_middleware(auth_middleware)



@lola.on_event('onAgentResponse')
def handle_new_conversation(session, ctx: LolaContext, msg, event):
    print(f'Got Agent Response message!!!!!')
    print(msg)

    metadata = event.get('data', {}).get('options', {}).get('metadata', {})
    ctx.messanger.send_text_message('>> Agent: ' + msg, blend=False, appendToHistory=False)


@lola.on_event('onTextMessage')
def handle_text_message(session, ctx: LolaContext, msg, req):
    print(f'Got text message: {msg["text"]}')
    lola.request_chat_completion("123", msg['text'])


@lola.on_command('get_cryptocurrency_price')
def handle_get_cryptocurrency_price(session, ctx: LolaContext, cmd):


    print(f'Got command!')
    assets_list = cmd['data']['args']['assets_list']
    currency = cmd['data']['args']['currency']
    print(f'User wants to know the price of {assets_list} in {currency}')

    # This line will send a message to the user without passing trough the AI
    # but the AI is going to response to the user after this message    
    #------------------------------------------------------------------------
    # ctx.messanger.send_text_message("Hold on... let me check the price", blend=True)
    
    # ctx.messanger.send_text_message(
    #     f'Did you know that you can get a discount at CoinGuru if you use the code 1234?', 
    #     blend=True
    # )
    ctx.messanger.send_typing_action()

    # split the assets list
    assets = assets_list.split(',')

    # get the prices
    prices = get_crypto_prices_from_list(assets, currency)

    return ResponseText(json.dumps(prices)).Send()

    # When you want to response to a command:
    # you can take the json and build a natural lang response or 
    # you can send the json as a response to the command
    #------------------------------------------------------------------------
    # return ResponseText(json.dumps(prices)).HookResponse({
    #     "meta1": "value1",
    # }).Send()

# Hook on every new conversation started by a new user
@lola.on_event('onNewConversation')
def handle_new_conversation(session, ctx: LolaContext, msg):
    # print(f'Got new conversation message: {msg["text"]}')
    img_url = "https://firebasestorage.googleapis.com/v0/b/numichat.appspot.com/o/bitcoin-btc-banner-bitcoin-cryptocurrency-concept-banner-background-vector.jpeg?alt=media&token=d9a4e055-e61c-40ac-9584-51d7a3709901"

    ctx.messanger.send_typing_action()
    
    # This line will send a message to the user without passing trough the AI
    # but the AI is going to response to the user after this message    
    #------------------------------------------------------------------------
    # return ResponseImage(img_url, "Welcome to CoinGuru!").Send()

    # If you want to response to the user and then disable the AI response
    # only for this message, you can use the following line
    # note the DisableAI() method, this will disable the AI response
    #------------------------------------------------------------------------
    return ResponseImage(img_url, "Welcome to the game!").DisableAI().Send()


@lola.on_client_command('/ping')
def handle_client_command(session, ctx: LolaContext, cmd):
    print(f'Got client command: {cmd}')
    ctx.messanger.send_text_message('pong', blend=False, appendToHistory=False)


# Hook on every image received by Lola from the user
@lola.on_event('onImage')
def handle_text_message(session, ctx: LolaContext, msg):
    attach = msg['attachments'][0]
    print(f'Got image message: {attach["url"]}')
    return ResponseText('You\'ve sent me an image? you made it? Awesome painting').DisableAI().Blend().Send()




# Hook on every timeout triggered
@lola.on_timeout()
def handle_timeout(session, ctx: LolaContext, label):
    print(f'Timeout reached for label: {label}')



if __name__ == '__main__':
    # -----------------------------------------------------
    lola.listen(debug=False)
    # -----------------------------------------------------
 
