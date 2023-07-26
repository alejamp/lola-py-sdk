

from lolapy.lola_message_sender import LolaMessageSender
from lolapy.lola_state_manager import LolaStateManager

class LolaContext:

    def __init__(self, lead, lola_token, prompter_url, timeout):
        self.lola_token = lola_token
        self.prompter_url = prompter_url 
        self.lead = lead
        self.timeout = timeout
        
        self.state = LolaStateManager(self.lead, self.lola_token, self.prompter_url)
        self.messanger = LolaMessageSender(self.lead, self.lola_token, self.prompter_url)
        # TODO
        # history
        # services
