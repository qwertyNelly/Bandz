#!/usr/bin/env python3
from hyperliquid.info import Info
from hyperliquid.utils.constants import MAINNET_API_URL as mainnet
from hyperliquid.utils.error import ClientError, ServerError
from HL.logging import LOGGING_CONFIG
import os
from dotenv import load_dotenv
import logging as lg
import logging.config as lgc
from HL.errors.PositionExceptions import WalletNotFoundError
from logging import getLogger as gl, StreamHandler as sh
import logging.config as lgc
import json

from HL.utils import val_wallet_is_in_env


lgc.dictConfig(LOGGING_CONFIG)

log = lg.getLogger(__name__)
log.debug(f"Initialized Logger for {__name__}")
log.debug(f"Initializing Hyperliquid Connection to {mainnet}")
hl = Info(mainnet)
log.debug(f"Connected to Hyperliquid @ {mainnet} with URL {hl.base_url}")

val_wallet_is_in_env()

_wallet = os.environ.get("WALLET")


class position:
    """_summary_

    Raises:
        WalletNotFoundError: _description_

    Returns:
        _type_: _description_
    """

    # Account
    _wallet: str = _wallet

    # Funding
    funding_all_time: float = 0.0
    funding_since_change: float = 0.0
    funding_since_open: float = 0.0

    #  Price
    entry_price: float = 0.0
    position_value: float = 0.0
    return_on_equity: float = 0.0
    unrealized_pnl: float = 0.0
    liquidation_price: float = 0.0
    position_size: float = 0.0

    # Position Type
    coin: str = ""

    leverage: int = 0
    leverage_type: str = "cross"  # Default to ISO

    margin_used: float = 0.0
    max_leverage: int = 0
    maintenance_margin: float = 0.0
    total_cross_margin_used: float = 0.0
    total_margin_used: float = 0.0
    notional_value: float = 0.0

    account_margin_used: float = 0.0
    account_notional_position: float = 0.0
    account_raw_usd: float = 0.0
    funds_withdrawable: float = 0.0
    time: int = 0

    position_dict: dict = {}
    position_strength: float
    # Only Iso
    raw_usd: str = ""
    total_raw_usd: float = 0.0

    def __init__(self, account_data: dict, position_strength: float = 0.0):
        self.position_strength = position_strength
        self.account_data = account_data
        self.init_position()

    def init_position(self) -> None:
        """_summary_

        Args:
            position (dict): _description_

        Raises:
            KeyError: _description_

        Returns:
            self: _description_
        """
        try:
            position = self.account_data
            log.debug(f"Keys : {position.keys()}")
            log.debug(position)
            self.coin = position["position"]["coin"]
            print(self.coin)
            self.size = float(position["position"]["szi"])
            print(self.size)
            # Funding
            self.funding_all_time = float(position["position"]["cumFunding"]["allTime"])
            self.funding_since_change = position["position"]["cumFunding"][
                "sinceChange"
            ]
            self.funding_since_open = position["position"]["cumFunding"]["sinceOpen"]
            # Leverage
            self.leverage = position["position"]["leverage"]["value"]
            self.leverage_type = position["position"]["leverage"]["type"]
            self.max_leverage = position["position"]["maxLeverage"]
            # Coin Value
            self.entry_price = position["position"]["entryPx"]
            self.liquidation_price = position["position"]["liquidationPx"]
            self.position_value = position["position"]["positionValue"]
            self.margin_used = position["position"]["marginUsed"]
            self.return_on_equity = position["position"]["returnOnEquity"]
            self.leverage_type = position["type"]
        except KeyError as e:
            raise KeyError(f"KEYERROR: Could not find {e.args}")

    def parse_positions(self):
        for index, val in enumerate(self.positions):
            log.info(f"Parsing Position {index} for {val}")

    def get_positions(self) -> dict:
        """{'assetPositions':
            [
            {'position':
                    {'coin': 'ETH', 'cumFunding': {'allTime': '27.984481', 'sinceChange': '0.030138', 'sinceOpen': '0.030138'}, 'entryPx': '3141.3',
                    'leverage': {'type': 'cross', 'value': 8},
                    'liquidationPx': '2668.7911259', 'marginUsed': '150.205673', 'maxLeverage': 50,
                    'positionValue': '1201.64539', 'returnOnEquity': '-0.02852322', 'szi': '0.3839',
                    'unrealizedPnl': '-4.29968'}, 'type': 'oneWay'},
            {'position':
                    {'coin': 'TIA', 'cumFunding': {'allTime': '-0.166859', 'sinceChange': '0.076194', 'sinceOpen': '0.076194'}, 'entryPx': '10.217', 'leverage': {'type': 'cross', 'value': 20}, 'liquidationPx': '9.51093214', 'marginUsed': '156.4105', 'maxLeverage': 20, 'positionValue': '3128.21', 'returnOnEquity': '-0.24664774', 'szi': '310.0', 'unrealizedPnl': '-39.06'}, 'type': 'oneWay'},
            {'position':
                {'coin': 'ONDO', 'cumFunding': {'allTime': '0.149334', 'sinceChange': '0.114875', 'sinceOpen': '0.114875'}, 'entryPx': '0.82524',

        'leverage': {'rawUsd': '-1344.853853', 'type': 'isolated', 'value': 5}, 'liquidationPx': '0.69530237', 'marginUsed': '330.448387', 'maxLeverage': 10, 'positionValue': '1675.30224', 'returnOnEquity': '-0.01454122', 'szi': '2036.0', 'unrealizedPnl': '-4.8864'}, 'type': 'oneWay'}


            'crossMaintenanceMarginUsed': '90.221703', 'crossMarginSummary': {'accountValue': '265.547215', 'totalMarginUsed': '306.616173', 'totalNtlPos': '4329.85539', 'totalRawUsd': '-4064.308175'},
            'marginSummary': {'accountValue': '595.995602', 'totalMarginUsed': '637.06456', 'totalNtlPos': '6005.15763', 'totalRawUsd': '-5409.162028'}, 'time': 1714834365581, 'withdrawable': '0.0'}

        Returns:
            dict: _description_
        """
        # Only Feed under AssetPositions
        self.position_dict = hl.user_state(self.wallet)["assetPositions"]
        return hl.user_state(self.wallet)["assetPositions"]

    def get_account_info(self):
        """
        crossMarginSummary: MarginSummary,
        marginSummary: MarginSummary,
        withdrawable: float string,

        Returns:
            _type_: _description_
        """
        return hl.user_state(self.wallet)
