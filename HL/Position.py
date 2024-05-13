from hyperliquid.info import Info
from hyperliquid.utils.constants import MAINNET_API_URL as mainnet
from hyperliquid.utils.error import ClientError, ServerError
from hyperliquid.utils.types import (
    L2BookDataType,
    L2BookMsgType,
    L2Book,
    Trade,
    L2Book,
    TradesMsgType,
    L2Book,
    TradesSubscription,
)
from HL.logging import LOGGING_CONFIG
import os
import logging as lg
import logging.config as lgc

from HL.errors.PositionExceptions import WalletNotFoundError


from logging import getLogger as gl, StreamHandler as sh
import logging.config as lgc


lgc.dictConfig(LOGGING_CONFIG)

log = lg.getLogger(__name__)
log.debug(f"Initialized Logger for {__name__}")
log.debug(f"Initializing Hyperliquid Connection to {mainnet}")
hl = Info(mainnet)
log.debug(f"Connected to Hyperliquid @ {mainnet} with URL {hl.base_url}")


class position:
    """_summary_

    Raises:
        WalletNotFoundError: _description_

    Returns:
        _type_: _description_
    """

    # Account
    wallet: str

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
    account_notional_position : float = 0.0
    account_raw_usd : float = 0.0
    funds_withdrawlable : float = 0.0
    time : int = 0

    position_dict: dict = {}

    # Only Iso
    raw_usd: str = ""
    total_raw_usd: float = 0.0

    def __init__(self, position_data: dict, wallet: str = None):
        self.wallet = wallet
        self.position_dict = position_data

    @property
    def leverage_type(self):
        """
        Probably not needed
        """
        self.leverage_type = ""

    @property
    def wallet(self):
        """
        String of the wallet

        Raises:
            WalletNotFoundError: _description_
        """
        if self.wallet is None:
            self.wallet = os.environ.get("WALLET")
            return os.environ.get("WALLET")
        # TODO: Add better exception handling
        else:
            raise WalletNotFoundError("Wallet not configured")

    @wallet.setter
    def wallet(self, wallet: str):
        self.wallet = wallet

    @wallet.getter
    def wallet(self):
        if self.wallet is None:
            self.wallet = os.environ.get("WALLET")
            return os.environ.get("WALLET")
        # TODO: Add better exception handling
        else:
            raise WalletNotFoundError("Wallet not configured")

    @classmethod
    def init_position(cls, position: dict):
        """
        Run this First
        Args:
            position (dict): the shit coming from the api
        """
        # Time spent (Wasted) : 34 minutes
        # hate = ['szi', 'entryPx', 'liquidationPx', 'positionValue', 'marginUsed']
        # for why in hate:
        #     #TODO: Iterate and get the class variable - good look
        # TODO: Think about this if statement, its not gonna work long term
        if "position" in position.keys:
            print(f"Keys : {position.keys()}")
            cls.coin = position["position"]["coin"]
            cls.size = position["position"]["coin"]["szi"]
            # Funding
            cls.funding_all_time = position["position"]["coin"]["cumFunding"]["allTime"]
            cls.funding_since_change = position["position"]["coin"]["cumFunding"][
                "sinceChange"
            ]
            cls.funding_since_open = position["position"]["coin"]["cumFunding"][
                "sinceOpen"
            ]
            # Leverage
            cls.leverage = position["position"]["coin"]["leverage"]["value"]
            cls.leverage_type = position["position"]["coin"]["leverage"]["type"]
            cls.max_leverage = position["position"]["coin"]["maxLeverage"]
            # Coin Value
            cls.entry_price = position["position"]["coin"]["entryPx"]
            cls.liquidation_price = position["position"]["coin"]["liquidationPx"]
            cls.position_value = position["position"]["coin"]["positionValue"]
            cls.margin_used = position["position"]["coin"]["marginUsed"]
            cls.return_on_equity = position["position"]["coin"]["returnOnEquity"]
            cls.leverage_type = position["position"]["coin"]["type"]
            # ISO Margin
            if cls.leverage_type.__eq__("isolated"):
                cls.raw_usd = position["position"]["coin"]["leverage"]["rawUsd"]
                cls.max_leverage = position["position"]["coin"]["leverage"]["rawUsd"]
            # Cross Margin
            cls.maintenance_margin = float(
                position["position"]["coin"]["crossMaintenanceMarginUsed"]
            )
            cls.maintenance_margin = float(
                position["position"]["coin"]["crossMarginSummary"]["accountValue"]
            )
            cls.total_cross_margin_used = float(
                position["position"]["crossMarginSummary"]["totalMarginUsed"]
            )
            cls.notional_value = float(
                position["position"]["marginSummary"]["totalNtlPos"]
            )
            # Margin Summary (Both Iso and Cross)
            cls.total_margin_account_value = float(
                position["marginSummary"]["accountValue"]
            )
            cls.account_margin_used = float(
                position["marginSummary"]["totalMarginUsed"]
            )
            cls.

            return cls

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
        return hl.user_state(self.wallet)["assetPositions"]
