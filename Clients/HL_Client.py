from hyperliquid.exchange import exchange as ex
from hyperliquid.info import Info
from eth_account.account import Account
from HL.utils.utils import setup
import os


class HL_Client:

    _address: Account
    info: Info
    exchange: ex

    def __init__(self) -> None:
        _address, info, exchange = setup()
        self._address = _address
        self.info = info
        self.exchange = exchange
