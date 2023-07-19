import requests

class LolaStateManager:

    def __init__(self, lead, lola_token, prompter_url):
        self.lola_token = lola_token
        self.prompter_url = prompter_url 
        self.lead = lead

    def get(self):    
        url = f'{self.prompter_url}/api/state/retrieve'
        headers = {'x-lola-auth': self.lola_token, 'Content-Type': 'application/json'}
        data = {'lead': self.lead}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['state']
    
    def set(self, state):
        url = f'{self.prompter_url}/api/state/update'
        headers = {'x-lola-auth': self.lola_token, 'Content-Type': 'application/json'}
        data = {'lead': self.lead, 'state': state}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return