#/Users/I516172/Desktop/Bandz/.venv/bin python3


from hyperliquid.websocket_manager import WebsocketManager
from HL.errors.Connection.ConnectionErrors import PingAtWebsocketError
from hyperliquid.utils.types import Any, Callable, Dict, List, NamedTuple, Optional, Subscription, Tuple, WsMsg, L2BookSubscription, L2BookData, L2Level

import asyncio as aio


ws = WebsocketManager()
# Create a level in book
lvl = L2Level()
#Add to book
dabook = L2BookData(coin='ETH')
# Create Book
book = L2BookSubscription(coin='eth',)



def make_order_book_data(coin : str) -> L2BookData:
    """_summary_

    Args:
        coin (str): the coin of the book

    Returns:
        _type_: _description_
    """
    return L2BookData(coin=coin)





def pang():
    try:
        ws.send_ping()
    except Exception as e:
        raise PingAtWebsocketError(e)

if __name__=="__main__":
    eloop = aio.get_event_loop()

