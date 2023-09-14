
from lolapy.lola_message_sender import LolaMessageSender
from lolapy.lola_session_store import LolaSessionStore
from lolapy.lola_state_manager import LolaStateManager
from lolapy.lola_stats_manager import LolaStatsManager
from lolapy.lola_vision_manager import LolaVisionManager
from lolapy.lola_history_manager import LolaHistoryManager

class LolaContext:

    def __init__(self, session, lola_token, prompter_url, timeout, redis_url=None):
        self.lola_token = lola_token
        self.prompter_url = prompter_url 
        self.session = session
        self.timeout = timeout
        self.redis_url = redis_url
        
        self.state = LolaStateManager(self.session['lead'], self.lola_token, self.prompter_url)
        self.messanger = LolaMessageSender(self.session['lead'], self.lola_token, self.prompter_url)
        self.stats = LolaStatsManager(self.session['lead'], self.lola_token, self.prompter_url)
        self.session_store = LolaSessionStore(self.session['id'], self.redis_url)
        self.vision = LolaVisionManager(self.session['lead'], self.lola_token, self.prompter_url)
        self.history = LolaHistoryManager(self.session['lead'], self.lola_token, self.prompter_url)

        # TODO
        # history
        # services

    def set_timeout(self, timeout_in_seconds, label=None):
        # ctx.timeout.set(session, ctx, 5, '5_seconds_without_message')
        self.timeout.set(self.session, self, timeout_in_seconds, label)
