from lolapy.lola_in_memory_session_store import InMemorySessionStore
from lolapy.lola_redis_session_store import RedisSessionStore
from colorama import Fore, Style

class LolaSessionStore:

    def __init__(self, session_id, redis_url):
        self.sesion_id = session_id
        self.redis_url = redis_url

        if self.redis_url:
            print( f'{Fore.WHITE}LolaSessionStore -> {Fore.GREEN}Using RedisSessionStore{Style.RESET_ALL}')
            self.store = RedisSessionStore(self.redis_url)
        else:
            print( f'{Fore.WHITE}LolaSessionStore -> {Fore.RED}Using InMemorySessionStore{Style.RESET_ALL}')
            self.store = InMemorySessionStore()

    def __key(self, key):
        return self.sesion_id +':'+ key

    def set(self, key, value):
        self.store.set(self.__key(key), value)
        return value

    def get(self, key):
        return self.store.get(self.__key(key))



