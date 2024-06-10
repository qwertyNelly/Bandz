#/Users/I516172/Desktop/Bandz/.venv/bin python3
from hyperliquid.utils.types import L2Level, L2BookSubscription, L2BookData, L2BookMsg
from hyperliquid.websocket_manager import WebsocketManager, WsMsg
import logging as lg
import logging.config as lgc
from HL.errors.BookExceptions import BookNotInitiatedError, IncorrectLevelDataType
import sys
import threading as th

log = lg.getLogger(__name__)

class DaBook():
    lsleveli : int = 0
    lslevel: L2Level
    lsbook : L2BookData # list[L2Level]
    l2book_msg : L2BookMsg # for WS
    ws : WebsocketManager
    ws_active : bool
    lsthread : th.Thread

    def __init__(self, price : float, coin : str, size : float) -> None:
        """_summary_

        Args:
            price (float): _description_
            coin (str): _description_
            size (float): _description_
        """
        super().__init__()
        self.lslevel = [L2Level(px=price, size=size)]  # type: list[L2Level]
        self.levelsi : int = len(self.lslevel)
        self.l2book_msg = [L2Level]
        self.coin = coin
        self.lsbook = L2BookData(levels=self.level, coin = self.coin, n = self.levelsi)
        self.ws = None  # type: WebsocketManager
        self.ws_active = False
        pass
    
    @property
    def ws(self):
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
        if self.ws.isDaemon():
            log.debug("ws is daemon")
            
    
    @property
    def ws_active(self):
        self.ws_active = True
        pass
        
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
        """_summary_

        Args:
            lvl (L2Level): _description_
        """
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
    
    