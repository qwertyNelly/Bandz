#/Users/I516172/Desktop/Bandz/.venv/bin python3

from hyperliquid.utils.types import L2Level, L2BookSubscription, L2BookData, L2BookMsg
import logging as lg
import logging.config as lgc

log = lg.getLogger(__name__)
class DaBook:
    lslevel: L2Level
    lsbook : L2BookData # list[L2Level]
    l2book_msg : L2BookMsg # for WS

    def __init__(self, price : float, coin : str, size : float) -> None:
        """_summary_

        Args:
            price (float): _description_
            coin (str): _description_
            size (float): _description_
        """
        self.lslevel = [L2Level(px=price, size=size)]
        self.levelsi : int = len(self.level)
        self.l2book_msg = []
        self.lsbook = L2BookData(levels=self.level, coin = self.coin, n)
        self.coin = coin
        pass

    @classmethod
    def run_it(cls):


    def add_level(self, lvl : L2Level):
        if len(self.lsbook) == 0:
            log.
            self.l2book = L2BookData(levels=self.level, coin = self.coin, n)