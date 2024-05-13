#!
from HL.Position import position
from HL.logging import LOGGING_CONFIG

from hyperliquid.info import Info
from hyperliquid.utils.constants import MAINNET_API_URL as mainnet


import logging as lg
import logging.config as lgc
import os
import sys

lgc.dictConfig(LOGGING_CONFIG)
log = lg.getLogger(__name__)
log.debug(f"Initialized Logger for {__name__}")
log.debug(f"Initializing Hyperliquid Connection to {mainnet}")
# Static Condition Class
wallet = os.environ.get("WALLET")
# Check if wallet is loaded in the env. If not exit
if wallet is None or len(wallet) == 0:
    log.error("No wallet")
    sys.exit(404)




hl = Info(mainnet)
log.debug(f"Connected to Hyperliquid @ {mainnet} with URL {hl.base_url}")


class account:
    
    
    position_holder : position = position(wallet=wallet)
    account_name: str
    positions: position
    cross_margin_summary : float | str
    total_margin_used : float | str
    account_value : float | str 
    total_notional_value : float | str
    total_raw_usd : float | str
    account_data : dict
    hl_user_state : dict
    
    def __init__(self, wallet : str):
        self.hl_info = Info(mainnet)
        self.hl_user_state = self.hl_info.user_state(wallet)
        self.account_data = self.hl_info.get_positions()
        self.account_positions = self.account_data['assetPositions']
        self.account_value = self.account_data['marginSummary']['accountValue']
        self.total_margin_used = self.account_data['marginSummary']['totalMarginUsed']
        self.total_notional_value = self.account_data['marginSummary']['totalNtlPos']
        self.total_raw_usd = self.account_data['marginSummary']['totalNtlPos']
    
    @property
    def positions(self):
        account_data = 
