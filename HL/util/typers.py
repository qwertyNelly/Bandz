#/Users/I516172/Desktop/Bandz/.venv/bin python3
from hyperliquid.utils.types import Any, Callable, Dict, List, NamedTuple, Optional, Subscription, Tuple, WsMsg, L2BookSubscription, L2BookData, L2Level

def make_trade_subcsription(coin):
    return L2BookSubscription(coin=coin)

def make_book(coin):
    return L2BookData()