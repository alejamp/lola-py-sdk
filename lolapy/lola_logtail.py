# import asyncio
import asyncio
import json
from colorama import Fore, Style
import socketio
import datetime

# Crea un objeto SocketIO
sio = socketio.AsyncClient()

# Define una función para manejar el evento "connect"
@sio.on('connect', namespace='/logtail')
def connect():
    print('Conectado al servidor Prompter de Socket.IO')
    


@sio.on('onLogEntry', namespace='/logtail')
async def onLogEntry(log):
    # log is a stringified JSON object
    log = json.loads(log)
    # ask if has a category property
    
    if ('category' in log and log['category'] == "heartbeat"):
        # print a dot in console without new line
        # print('.')
        # print(f'{Fore.BLACK}{Back.GREEN}.{Style.RESET_ALL}')
        print(f'{Fore.LIGHTBLACK_EX}.{Style.RESET_ALL}')
    else:
        category = log['categoryName']
        level = log['level']['levelStr']
        if (level == "INFO"):
            print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}][{category}]{Fore.LIGHTBLACK_EX}[{level}] > {log["data"]}{Style.RESET_ALL}')
        elif (level == "WARN"):
            print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}][{category}]{Fore.YELLOW}[{level}] > {log["data"]}{Style.RESET_ALL}')
        elif (level == "ERROR"):
            print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}][{category}]{Fore.RED}[{level}] > {log["data"]}{Style.RESET_ALL}')
        elif (level == "DEBUG"):
            print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}][{category}]{Fore.LIGHTBLACK_EX}[{level}] > {log["data"]}{Style.RESET_ALL}')
        else:
            print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}][{category}]{Fore.LIGHTBLACK_EX}[{level}] > {log["data"]}{Style.RESET_ALL}')
    

# Define una función para manejar el evento "disconnect"
@sio.event
def disconnect():
    print('Desconectado del servidor de Socket.IO')


async def connectLogTail(url: str, token: str):
    print(f'Connecting to {url} for logtail...')
    await sio.connect(f'{url}/?token={token}', socketio_path="/socket.io/logtail", namespaces=["/logtail"])
    await sio.wait()


def syncConnectLogTail(url: str, token: str):
    asyncio.run(connectLogTail(url, token))

if __name__ == '__main__':
    token = "..."
    syncConnectLogTail("http://127.0.0.1:4000", token)

