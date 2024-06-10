
import threading
import hyperliquid.utils.types as hlt
import hyperliquid.utils.constants as hlc

class Feed(threading.Thread):


    coin : str 

    def __init__(self, coin : str, is_buy : bool, ):
        self.name = coin.upper()
        if self.name in threading.enumerate():
            raise threading.ThreadError(f"Duplicate? Thread for {self.coin}")
        self.lvl : hlt.List[hlt.L2Level] = None
        self.l2book : hlt.L2BookData = None
        self.position_side = None
        self.side = is_buy


    @classmethod
    def init_l2book(cls, price : str, size : str):
        if cls.lvl is None:

            cls.lvl[hlt.L2Level(str=cls.coin, sz=size, px=price, n=1)]
        if cls.l2book is None:
            # TODO: Init Book

    @classmethod
    def get_data(cls):
        cls


        
        

