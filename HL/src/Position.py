# /Users/I516172/Desktop/Bandz/.venv/bin python3
from hyperliquid.info import Info
from HL.globals import EXCHANGE, INFO, ADDRESS, DEFAULT_SLIPPAGE
from hyperliquid.utils.constants import MAINNET_API_URL as mainnet
from hyperliquid.utils.error import ClientError, ServerError

from HL.util.logging import LOGGING_CONFIG
from hyperliquid.utils.types import Any, List, Meta, SpotMeta, Optional, Tuple, Cloid
import os
import logging as lg
import logging.config as lgc
from HL.errors.PositionExceptions import WalletNotFoundError, PositionAlreadyExists
from logging import getLogger as gl, StreamHandler as sh
import logging.config as lgc
import time

from HL.util.utils import val_wallet_is_in_env


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
    is_buy: bool

    # Position Active?

    active: bool = False

    leverage: float = 0.0
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

    def __init__(self, size: float, leverage: float, strategy):
        self.size = size
        self.leverage = leverage
        self.position_strat = strategy

    @property
    def active(self):
        log.debug(f"Checking if Position Exists or is Active")
        if self.entry_price == 0 or self.entry_price is None:
            raise PositionAlreadyExists()
        else:
            if isinstance(self.coin, str):
                # must be Coin assigned to position
                if len(self.coin) > 0:
                    log.debug(f"Found Active Position for {self.coin}")
                    self.active = True
                else:
                    raise PositionAlreadyExists()
            else:
                raise PositionAlreadyExists()

    @classmethod
    def attach_strategy(cls, strategy):
        pass

    @classmethod
    def init_position(cls, position: dict):
        """_summary_

        Args:
            position (dict): _description_

        Raises:
            KeyError: _description_

        Returns:
            self: _description_
        """
        try:
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
            cls.leverage = float(position["position"]["coin"]["leverage"]["value"])
            cls.leverage_type = float(position["position"]["coin"]["leverage"]["type"])
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
            return cls
        except KeyError as e:
            raise KeyError(f"KEYERROR: Could not find {e.args}")

    def _slippage_price(
        self,
        is_buy: bool,
        px: Optional[float] = None,
    ) -> float:
        """_summary_

        Args:
            is_buy (bool): _description_
            px (Optional[float], optional): _description_. Defaults to None.

        Returns:
            float: _description_
        """
        slippage = self._slippage_price(is_buy, px)

        if not px:
            # Get midprice
            px = float(self.info.all_mids()[self.coin])
        # Calculate Slippage
        px *= (1 + slippage) if is_buy else (1 - slippage)
        # We round px to 5 significant figures and 6 decimals
        return round(float(f"{px:.5g}"), 6)

    def get_market_price(self, is_buy: bool, px, slippage: float = DEFAULT_SLIPPAGE):
        # Get aggressive Market Price
        return self._slippage_price(self.coin, is_buy, slippage, px)

    @classmethod
    def market_order(cls, coin: str, sz: float, is_buy: bool, leverage: float):
        print(f"We try to Market {'Buy' if is_buy else 'Sell'} {sz} {coin}.")

        order_result = EXCHANGE.market_open(coin, is_buy, sz, None, 0.01)
        if order_result["status"] == "ok":
            for status in order_result["response"]["data"]["statuses"]:
                try:
                    filled = status["filled"]
                    print(
                        f'Order #{filled["oid"]} filled {filled["totalSz"]} @{filled["avgPx"]}'
                    )
                except KeyError:
                    print(f'Error: {status["error"]}')

            print("We wait for 2s before closing")
            time.sleep(2)

            print(f"We try to Market Close all {coin}.")
            order_result = EXCHANGE.market_close(coin)
            if order_result["status"] == "ok":
                for status in order_result["response"]["data"]["statuses"]:
                    try:
                        filled = status["filled"]
                        print(
                            f'Order #{filled["oid"]} filled {filled["totalSz"]} @{filled["avgPx"]}'
                        )
                    except KeyError:
                        print(f'Error: {status["error"]}')

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

    def get_cross_margin_info(self):
        pass
