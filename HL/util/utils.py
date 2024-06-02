#/Users/I516172/Desktop/Bandz/.venv/bin python3
# -*- coding: utf-8 -*-

from HL.errors.PositionExceptions import WalletNotFoundError
from HL.util.logging import LOGGING_CONFIG
import logging as lg
import logging.config as lgc
import eth_account
from eth_account.signers.local import LocalAccount
import json
import os

from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils.constants import MAINNET_API_URL as mainnet

lgc.dictConfig(LOGGING_CONFIG)

log = lg.getLogger(__name__)
log.debug(f"Initialized Logger for {__name__}")
log.debug(f"Initializing Hyperliquid Connection to {mainnet}")


def val_wallet_is_in_env() -> bool | WalletNotFoundError:
    if len(os.environ.get("WALLET")) == 0 or os.environ.get("WALLET") is None:
        return WalletNotFoundError()
    else:
        return True


def setup(base_url=None, skip_ws=False):
    """_summary_

    Args:
        base_url (_type_, optional): _description_. Defaults to None.
        skip_ws (bool, optional): _description_. Defaults to False.

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    log.info(f"HL Configuration path: {config_path}")
    with open(config_path) as f:
        config = json.load(f)
    account: LocalAccount = eth_account.Account.from_key(config["secret_key"])
    address = config["account_address"]
    if address == "":
        address = account.address
    print("Running with account address:", address)
    if address != account.address:
        print("Running with agent address:", account.address)
    info = Info(base_url, skip_ws)
    user_state = info.user_state(address)
    margin_summary = user_state["marginSummary"]
    if float(margin_summary["accountValue"]) == 0:
        print("Not running the example because the provided account has no equity.")
        url = info.base_url.split(".", 1)[1]
        error_string = f"No accountValue:\nIf you think this is a mistake, make sure that {address} has a balance on {url}.\nIf address shown is your API wallet address, update the config to specify the address of your account, not the address of the API wallet."
        raise Exception(error_string)
    exchange = Exchange(account, base_url, account_address=address)
    return address, info, exchange
