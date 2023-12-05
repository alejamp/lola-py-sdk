

import requests


class LolaPromptManager:

    def __init__(self,lola_token, prompter_url):
        self.lola_token = lola_token
        self.prompter_url = prompter_url
    
    def publishPrompt(self,promptid:str,promptName:str,promptFileContent:str,state):
        print(f'Publishing prompt with id {promptid}')
        url = f'{self.prompter_url}/api/prompt'
        body={
            "id": promptid,
            "name": promptName,
            "content": promptFileContent,
            "owner": "lolaSDK",
            "state": state,
            "enabled": True
        }
        
        headers = {'Authorization': f'Bearer {self.lola_token}', 'Content-Type': 'application/json'}
        print(str(headers))
        responsePublishPrompt = requests.post(url, headers=headers, json=body)
        responsePublishPrompt.raise_for_status()
        return responsePublishPrompt.json()