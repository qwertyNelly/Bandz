#!/Users/ben/Desktop/bndni/.venv/bin python3.11
from HL.Position import position
from HL.logging import LOGGING_CONFIG
from HL.utils import setup, val_wallet_is_in_env
from hyperliquid.info import Info
from hyperliquid.utils.types import AssetInfo, MetaInfo, L2Level
from hyperliquid.utils.constants import MAINNET_API_URL as mainnet
import logging as lg
import logging.config as lgc
import os
import sys
import json

lgc.dictConfig(LOGGING_CONFIG)
log = lg.getLogger(__name__)
log.debug(f"Initialized Logger for {__name__}")
log.debug(f"Initializing Hyperliquid Connection to {mainnet}")
# Static Condition Class


address, info, exchange = setup(mainnet)
print(address, info, exchange)
val_wallet_is_in_env()
_wallet = os.environ.get("WALLET")
# Check if wallet is loaded in the env. If not exit
if _wallet is None or len(_wallet) == 0:
    log.error("No wallet")
    # TODO: Add exit codes
    sys.exit(404)


hl_info = Info(mainnet)
log.debug(f"Connected to Hyperliquid @ {mainnet} with URL {hl_info.base_url}")


class account:

    positions: list[position]
    account_name: str
    _wallet: str = _wallet
    positions: position
    cross_margin_summary: float | str
    total_margin_used: float | str
    account_value: float | str
    total_notional_value: float | str
    total_raw_usd: float | str
    account_data: dict
    hl_user_state: dict
    hl_info: Info
    withdrawable: float | str

    def __init__(self):
        self.hl_info = Info(mainnet)
        self._wallet = _wallet
        self.positions: list[position] = []
        log.info(f"Initializing Property of the user state for {_wallet}")
        log.debug(f"Getting the Positions for {_wallet}")
        self.account_data = self.hl_info.user_state(_wallet)
        for idx, pos in enumerate(self.account_data["assetPositions"]):
            new_pos = position(pos)
            log.debug(f"Adding asset  {new_pos.coin} to the Account {_wallet}")
            self.positions.append(new_pos)
            log.debug(
                f"Adding asset {new_pos.coin} to the list of positions for {_wallet}"
            )
            print(new_pos.position_value)
        print(self.positions)
        log.debug(f"Positions: {self.account_data}")
        # Fill Account
        self.get_cross_margin_summary()
        self.get_margin_summary()
        self.fill_account_data()
        for idx, p in enumerate(self.positions):
            print(f"Position : {p.coin}, ROE : {p.return_on_equity}")

    def get_margin_summary(self):
        log.info(f"Parsing Margin Summary for {_wallet}")
        try:
            log.info(f"Filling Margin Summary Information for {self._wallet}")
            self.account_value = float(
                self.account_data["marginSummary"]["accountValue"]
            )
            self.total_margin_used = float(
                self.account_data["marginSummary"]["totalMarginUsed"]
            )
            self.total_notional_value = float(
                self.account_data["marginSummary"]["totalNtlPos"]
            )
            self.total_raw_usd = float(
                self.account_data["marginSummary"]["totalNtlPos"]
            )
        except (ValueError, KeyError) as e:
            print(e)

    def get_cross_margin_summary(self):
        try:
            log.info(f"Filling Margin Summary Information for {self._wallet}")
            self.account_value = float(
                self.account_data["crossMarginSummary"]["accountValue"]
            )
            self.total_margin_used = float(
                self.account_data["crossMarginSummary"]["totalMarginUsed"]
            )
            self.total_notional_value = float(
                self.account_data["crossMarginSummary"]["totalNtlPos"]
            )
            self.total_raw_usd = float(
                self.account_data["crossMarginSummary"]["totalNtlPos"]
            )
        except (KeyError, ValueError) as e:
            print(e)

    def fill_account_data(self):
        self.withdrawable = self.account_data["withdrawable"]
        self.time = self.account_data["time"]

    def market_buy(self, coin):
        exchange.market_open()


if __name__ == "__main__":
    a = account()
