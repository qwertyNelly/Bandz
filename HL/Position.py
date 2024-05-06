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
import os
import logging as lg
import logging.config as lgc

from bndni.HL.errors.PositionExceptions import WalletNotFoundError

hl = Info(mainnet)


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
    coin: str = None

    leverage: int = 0
    leverage_type: str = None  # Cross or Iso

    margin_used: float = 0.0

    # Only Iso
    raw_usd: str

    def __init__(self, wallet: str = None) -> None:
        self.wallet = wallet

    @property
    def wallet(self):
        """_summary_

        Raises:
            WalletNotFoundError: _description_
        """
        if self.wallet is None:
            self.wallet = os.environ.get("WALLET")
        # TODO: Add better exception handling
        else:
            raise WalletNotFoundError("Wallet not configured")

    @classmethod
    def init_position(cls, position: dict):
        """_summary_

        Args:
            position (dict): _description_
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
            # Value
            cls.entry_price = position["position"]["coin"]["entryPx"]
            cls.liquidation_price = position["position"]["coin"]["liquidationPx"]
            cls.position_value = position["position"]["coin"]["positionValue"]
            cls.margin_used = position["position"]["coin"]["marginUsed"]

    def get_positions(self) -> dict:
        """{'assetPositions':
            [
            {'position':
                    {'coin': 'ETH', 'cumFunding': {'allTime': '27.984481', 'sinceChange': '0.030138', 'sinceOpen': '0.030138'}, 'entryPx': '3141.3', 'leverage': {'type': 'cross', 'value': 8}, 'liquidationPx': '2668.7911259', 'marginUsed': '150.205673', 'maxLeverage': 50, 'positionValue': '1201.64539', 'returnOnEquity': '-0.02852322', 'szi': '0.3839', 'unrealizedPnl': '-4.29968'}, 'type': 'oneWay'},
            {'position':
                    {'coin': 'TIA', 'cumFunding': {'allTime': '-0.166859', 'sinceChange': '0.076194', 'sinceOpen': '0.076194'}, 'entryPx': '10.217', 'leverage': {'type': 'cross', 'value': 20}, 'liquidationPx': '9.51093214', 'marginUsed': '156.4105', 'maxLeverage': 20, 'positionValue': '3128.21', 'returnOnEquity': '-0.24664774', 'szi': '310.0', 'unrealizedPnl': '-39.06'}, 'type': 'oneWay'},
            {'position':
                {'coin': 'ONDO', 'cumFunding': {'allTime': '0.149334', 'sinceChange': '0.114875', 'sinceOpen': '0.114875'}, 'entryPx': '0.82524', 'leverage': {'rawUsd': '-1344.853853', 'type': 'isolated', 'value': 5}, 'liquidationPx': '0.69530237', 'marginUsed': '330.448387', 'maxLeverage': 10, 'positionValue': '1675.30224', 'returnOnEquity': '-0.01454122', 'szi': '2036.0', 'unrealizedPnl': '-4.8864'}, 'type': 'oneWay'}
                ],
            'crossMaintenanceMarginUsed': '90.221703', 'crossMarginSummary': {'accountValue': '265.547215', 'totalMarginUsed': '306.616173', 'totalNtlPos': '4329.85539', 'totalRawUsd': '-4064.308175'},
            'marginSummary': {'accountValue': '595.995602', 'totalMarginUsed': '637.06456', 'totalNtlPos': '6005.15763', 'totalRawUsd': '-5409.162028'}, 'time': 1714834365581, 'withdrawable': '0.0'}

        Returns:
            dict: _description_
        """
        return hl.user_state(self.wallet)["assetPositions"]
