

from lolapy.lola_message_sender import LolaMessageSender
from lolapy.lola_state_manager import LolaStateManager

class LolaContext:

    def __init__(self, session, lola_token, prompter_url, timeout):
        self.lola_token = lola_token
        self.prompter_url = prompter_url 
        self.session = session
        self.timeout = timeout
        
        self.state = LolaStateManager(self.session['lead'], self.lola_token, self.prompter_url)
        self.messanger = LolaMessageSender(self.session['lead'], self.lola_token, self.prompter_url)
        # TODO
        # history
        # services

    def set_timeout(self, timeout_in_seconds, label=None):
        # ctx.timeout.set(session, ctx, 5, '5_seconds_without_message')
        self.timeout.set(self.session, self, timeout_in_seconds, label)
