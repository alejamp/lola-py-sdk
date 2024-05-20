
class ResponseImage:
    
    def __init__(self, url, text=None):
        self.response = {
            "type": "image",
            "url": url,
            "text": text,
            "options": {
                "disableAI": False,
                "isPrivate": False,
                "appendHistory": False,
                "blend": False
            },
        }

    def DisableAI(self):
        self.response["options"]["disableAI"] = True
        return self
    
    def IsPrivate(self):
        self.response["options"]["isPrivate"] = True
        return self
    
    def Send(self):
        return self.response

class ResponseText:
    
    def __init__(self, text):
        self.response = {
            "type": "text",
            "text": text,
            "options": {
                "disableAI": False,
                "isPrivate": False,
                "appendHistory": False,
                "blend": False
            },
        }
        
    def HookResponse(self, metadata: dict = None):
        self.response["options"]["hookResponse"] = True
        if metadata:
            self.response["options"]["metadata"] = metadata
        return self

    def DisableAI(self):
        self.response["options"]["disableAI"] = True
        return self
    
    def IsPrivate(self):
        self.response["options"]["isPrivate"] = True
        return self
    
    def AppendHistory(self):
        self.response["options"]["appendHistory"] = True
        return self
    
    def Blend(self):
        self.response["options"]["blend"] = True
        return self
    
    def Send(self):
        return self.response
