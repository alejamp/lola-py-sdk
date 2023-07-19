
import requests

class LolaMessageSender:

    def __init__(self, lead, lola_token, prompter_url):
        self.lola_token = lola_token
        self.prompter_url = prompter_url 
        self.lead = lead

    def send_text_message(self, text, appendToHistory=False):
        url = f'{self.prompter_url}/api/messanger/send/text'
        headers = {'x-lola-auth': self.lola_token, 'Content-Type': 'application/json'}
        data = {'lead': self.lead, 'text': text, 'appendToHistory': appendToHistory}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return
    
    def send_typing_action(self):
        url = f'{self.prompter_url}/api/messanger/send/action'
        headers = {'x-lola-auth': self.lola_token, 'Content-Type': 'application/json'}
        data = {'lead': self.lead, 'action': 'typing_on'}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return