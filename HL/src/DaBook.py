#/Users/I516172/Desktop/Bandz/.venv/bin python3

from hyperliquid.utils.types import L2Level, Subscription, TradesSubscription, AllMidsSubscription, L2BookSubscription, L2BookData, L2BookMsg
from hyperliquid.websocket_manager import WebsocketManager, WsMsg, ActiveSubscription
import logging as lg
import logging.config as lgc
from HL.errors.BookExceptions import BookNotInitiatedError, IncorrectLevelDataType
import sys
<<<<<<< HEAD
import websocket
import threading as thread
from types import NamedTuple

log = lg.getLogger(__name__)





class DaBook:
=======
import threading as th

log = lg.getLogger(__name__)

class DaBook():
    lsleveli : int = 0
>>>>>>> 4d2fbaa2a82cb35d64e843fd0f91b1b78367681a
    lslevel: L2Level
    lsbook : L2BookData # list[L2Level]
    l2book_msg : L2BookMsg # for WS
    ws : WebsocketManager
    ws_active : bool
<<<<<<< HEAD
    ws_daemon : websocket.WebSocket
    coin : str
    
=======
    lsthread : th.Thread
>>>>>>> 4d2fbaa2a82cb35d64e843fd0f91b1b78367681a

    def __init__(self, price : float, coin : str, size : float ) -> None:
        """_summary_

        Args:
            price (float): price
            coin (str): name of coin
            size (float): positions size
        """
<<<<<<< HEAD
        self.active_subscription = ActiveSubscription(self.on_message, coin, size)
        self.coin = coin
        self.lslevel = L2Level(px=price, size=size)
=======
        super().__init__()
        self.lslevel = [L2Level(px=price, size=size)]  # type: list[L2Level]
>>>>>>> 4d2fbaa2a82cb35d64e843fd0f91b1b78367681a
        self.levelsi : int = len(self.lslevel)
        self.l2book_msg = [L2Level]
        self.lsbook = L2BookData(levels=self.level, coin = self.coin, n = self.levelsi)
<<<<<<< HEAD

        
        self.is_daemon = False
        self.ws = None
=======
        self.ws = None  # type: WebsocketManager
>>>>>>> 4d2fbaa2a82cb35d64e843fd0f91b1b78367681a
        self.ws_active = False
        pass
    
    
    
    @property
    def is_daemon(self):
        if isinstance(self.ws, WebsocketManager):
            return self.ws.is_daemon()
        pass
    
    @classmethod
    def add_level(cls, lslevel : L2Level, time : int):
        cls.lsbook.update(levels=lslevel, coin=cls.coin)
        
    
    def on_message(self):
        
        pass
        
        
    @classmethod
    def init_ws(cls):
        try:
            cls.ws = WebsocketManager()
        except BaseException as e:
            raise e
        
    
    @property
    def ws(self):
        if self.ws_active:
            log.debug(f"Found Already Active WS for {self.coin}")
        if self.ws is None:
            log.debug(f"ws is None at {__spec__}")
            log.debug(f"Creating new WebSocket")
            try:
                self.ws = WebsocketManager()
            except ConnectionError as e:
                raise e
        elif isinstance(self.ws, WebsocketManager):
            log.debug(f'Found an instance of WS in class. Checking if its active')
            self.ws
        # If Daemon, assign to damon attribute
        if self.ws.isDaemon():
            log.debug("ws is daemon")
            
            
            
            
            
    
    @property
    def ws_active(self):
        self.ws_active = True
        pass

    @property.setter
    def ws_active(self, active : bool):
        log.debug(f"Setting Websocket to Active")
        self.ws_active = active
    
    @property.getter
    def ws_active(self) -> bool:
        return self.ws_active
        
    @ws_active.setter
    def ws_active(self, active : bool):
        log.debug(f'Setting Websocket to Active')
        self.ws_active = active
    
    @ws_active.getter
    def ws_active(self):
        if self.ws_active:
            log.debug("ws is active")
            if self.ws.is_alive():
                log.debug("ws is alive")
            else:
                log.debug(f'Trying to Create new Websocket for {self.coin}')
                self.ws.run()
            
            return self.ws   


    @classmethod
    def run_ws(cls):
        # TODO: Threading or Instantiate many books
        try:
            cls.ws.run()
            cls.ws_active = True
        except BaseException as e:
            raise e
        pass
    
    
    def subscribe(cls):
        if cls.ws_active is True:
            cls.ws.subscribe()
        

    @classmethod
    def run(cls, baseurl : str = None):
        """_summary_

        Raises:
            BookNotInitiatedError: _description_
        """
        if len(cls.l2book_msg) == 0:
            # Flush l2book_msg into book
            raise BookNotInitiatedError(__name__)
        else:
            try:
                cls.ws = WebsocketManager(base_url=baseurl)
                cls.run()
            except Exception as e:
                log.error(f'Error establishing WS connection : {e.args}')
            
    
    @classmethod
    def new(cls, price : float, coin : str, size : float):
        return cls.__init__( price : float, coin : str, size : float)
            


    def add_level(self, lvl : L2Level):
        if len(self.lsbook) == 0:
            log.debug(f'Adding level {lvl.items}')
            self.l2book = L2Level(levels=self.level, coin = self.coin)
            log.debug(f'Adding level {lvl.items}')
            log.debug(f'Adding level {len(self.l2book)}')
        else:
            if isinstance(lvl, L2Level):
                self.l2book.add(lvl)
            else:
                log.error('Error adding level')
                raise IncorrectLevelDataType
            sys.exit(59)
    
class DaBookManager(WebsocketManager):
    # L2BookSubscription = TypedDict("L2BookSubscription", {"type": Literal["l2Book"], "coin": str})
    l2booksubs : L2BookSubscription
    # AllMidsSubscription = TypedDict("AllMidsSubscription", {"type": Literal["allMids"]})
    mid_subscription : AllMidsSubscription
    # TradesSubscription = TypedDict("TradesSubscription", {"type": Literal["trades"], "coin": str})
    trade_subscription : TradesSubscription
    # Subscription = Union[AllMidsSubscription, L2BookSubscription, TradesSubscription, UserEventsSubscription]
    all_subscriptions : Subscription
    
    
    allBooks : NamedTuple['coin': str, 'l2book' : L2BookSubscription]
    
    
    all_books : NamedTuple["Books", {'coin': str, 'book' : DaBook}]
    
    def __init__(self, coin : str, base_url = None, all_books = all_books):
        super().__init__(base_url)
        log.debug(f"Initializing the Book Manager for : {coin}")
        self.coin = []
        self.books = all_books
        pass
    
    
    def 
        
        
        
    
    
    def init_mid_subscription(self)
     