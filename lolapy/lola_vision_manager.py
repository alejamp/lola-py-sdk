import requests

class LolaVisionManager:

    def __init__(self, lead, lola_token, prompter_url):
        self.lola_token = lola_token
        self.prompter_url = prompter_url 
        self.lead = lead

    def scanGenericId(self, url=None, image=None):
        if url is None and image is None:
            raise ValueError('Either url or image must be provided')

        endpoint = f'{self.prompter_url}/api/vision/generic_id'
        headers = {'x-lola-auth': self.lola_token, 'Content-Type': 'application/json'}

        data = {
            'url': url,
            'image': image
        }

        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        return response.json()


