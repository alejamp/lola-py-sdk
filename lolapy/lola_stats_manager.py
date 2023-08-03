import requests

class LolaStatsManager:

    def __init__(self, lead, lola_token, prompter_url):
        self.lola_token = lola_token
        self.prompter_url = prompter_url 
        self.lead = lead

    def getTokens(self):    
        url = f'{self.prompter_url}/api/state/stats/tokens_used'
        headers = {'x-lola-auth': self.lola_token, 'Content-Type': 'application/json'}
        data = {'lead': self.lead}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['data']
    
    def getMessagesSent(self):
        url = f'{self.prompter_url}/api/state/stats/messages_sent'
        headers = {'x-lola-auth': self.lola_token, 'Content-Type': 'application/json'}
        data = {'lead': self.lead}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['data']
    
    def setMessagesSent(self, value):
        url = f'{self.prompter_url}/api/state/stats/messages_sent'
        headers = {'x-lola-auth': self.lola_token, 'Content-Type': 'application/json'}
        data = {'lead': self.lead, 'value': value}
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        return
    
    def setTokens(self, value):
        url = f'{self.prompter_url}/api/state/stats/tokens_used'
        headers = {'x-lola-auth': self.lola_token, 'Content-Type': 'application/json'}
        data = {'lead': self.lead, 'value': value}
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        return