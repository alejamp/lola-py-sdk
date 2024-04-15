from dataclasses import dataclass
import requests
from lolapy.lola_token import decode_lola_token

# "tenantId": "Ale2fMqvZCW7ZOWLom9S",
# "assistantId": "ftUS4ARKHVHyzrguUpvhzP",
# "channelSource": "custom",
# "userId": "123"
@dataclass
class CustomLead:
    tenantId: str
    assistantId: str
    channelSource: str
    userId: str

    def __init__(self, tenantId: str, assistantId: str, userId: str):
        self.tenantId = tenantId
        self.assistantId = assistantId
        self.channelSource = 'custom'
        self.userId = userId
    
    def serialize(self):
        return {
            'tenantId': self.tenantId,
            'assistantId': self.assistantId,
            'channelSource': self.channelSource,
            'userId': self.userId
        }



class LolaAgentManager:

    def __init__(self, lola_token, prompter_url):
        self.lola_token = lola_token
        self.prompter_url = prompter_url 

    def __build_lead(self, userId: str):
        return CustomLead(self.tenantId, self.assistantId, userId)


    def completion(self, userId: str, text: str):    
        url = f'{self.prompter_url}/api/agent/completion'
        headers = {'x-lola-auth': self.lola_token, 'Content-Type': 'application/json'}
        data = {'userId': userId, 'text': text}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
    

