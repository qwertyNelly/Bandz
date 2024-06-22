
import threading
import hyperliquid.utils.types as hlt
import hyperliquid.utils.constants as hlc
from HL.src.Strategies.TDSequential import tds

class BookFeed(threading.Thread):


    coin : str
    book : hlt.L2BookData

    def __init__(self, coin : str, is_buy : bool, size : int, strategy : B, n : int = 0):
        self.n = n
        self.size = size
        self.name = coin.upper() # Thread Name 
        self.side = is_buy
        self.position = position
        self.strategy = strategy
        
        if self.name in threading.enumerate():
        
            raise threading.ThreadError(f"Duplicate? Thread for {self.coin}")
        self.lvl : hlt.List[hlt.L2Level] = None  # type: hlt.List[hlt.L2Level]
        self.l2book : hlt.L2BookData = None
        


    @classmethod
    def init_l2book(cls, price : str, size : str, lvl : hlt.L2Level | None):
        if cls.lvl is None:
            cls.lvl[hlt.L2Level(str=cls.coin, sz=size, px=price, n=1)]
        if cls.l2book is None:
            # TODO: Init Book


    @classmethod
    def get_data(cls):
        cls


        
        

