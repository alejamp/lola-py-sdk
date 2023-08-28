import requests

class LolaVisionManager:

    def __init__(self, lead, lola_token, prompter_url):
        """
        Initializes the LolaVisionManager class with the given parameters.

        Args:
            lead (str): The lead name.
            lola_token (str): The Lola API token.
            prompter_url (str): The URL of the prompter.
        """
        self.lola_token = lola_token
        self.prompter_url = prompter_url 
        self.lead = lead


    def scanGenericId(self, url=None, image=None):
        """
        Scans a generic ID from an image or URL.

        Args:
            url (str): The URL of the image.
            image (bytes): The image data.

        Raises:
            ValueError: If neither url nor image is provided.

        Returns:
            dict: The response JSON.
        """
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


    def extractFace(self, url=None, image=None):
        """
        Extracts a face from an image or URL.

        Args:
            url (str): The URL of the image.
            image (bytes): The image data.

        Raises:
            ValueError: If neither url nor image is provided.

        Returns:
            dict: The response JSON.
        """
        if url is None and image is None:
            raise ValueError('Either url or image must be provided')

        endpoint = f'{self.prompter_url}/api/vision/facecrop'
        headers = {'x-lola-auth': self.lola_token, 'Content-Type': 'application/json'}

        data = {
            'url': url,
            'image': image
        }

        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def facematch(self, url1=None, image1=None, url2=None, image2=None):
        """
        Matches two faces from two images or URLs.

        Args:
            url1 (str): The URL of the first image.
            image1 (bytes): The first image data.
            url2 (str): The URL of the second image.
            image2 (bytes): The second image data.

        Raises:
            ValueError: If url1 and image1 are not provided, or if url2 and image2 are not provided.

        Returns:
            dict: The response JSON.
        """
        if url1 is None and image1 is None:
            raise ValueError('Either url1 or image1 must be provided')
        if url2 is None and image2 is None:
            raise ValueError('Either url2 or image2 must be provided')

        endpoint = f'{self.prompter_url}/api/vision/facematch'
        headers = {'x-lola-auth': self.lola_token, 'Content-Type': 'application/json'}

        data = {
            'referenceImage': {
                'url': url1,
                'content': image1,
            },
            'targetImage': {
                'url': url2,
                'content': image2
            }
        }

        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        return response.json()