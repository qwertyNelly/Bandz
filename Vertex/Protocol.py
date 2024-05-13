#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import os
import web3
from vertex_protocol.client import create_vertex_client
from vertex_protocol.engine_client.types.execute import (
    OrderParams,
    PlaceOrderParams,
    WithdrawCollateralParams,
    CancelOrdersParams,
)
from vertex_protocol.contracts.types import DepositCollateralParams
from vertex_protocol.utils.bytes32 import subaccount_to_bytes32, subaccount_to_hex
from vertex_protocol.utils.expiration import OrderType, get_expiration_timestamp
from vertex_protocol.utils.math import to_pow_10, to_x18
from vertex_protocol.utils.nonce import gen_order_nonce
from vertex_protocol.utils.subaccount import SubaccountParams
from dotenv import load_dotenv
from eth_account.signers.local import LocalAccount
from eth_account import Account

load_dotenv()
_pk = os.environ.get("PK")
_wallet = os.environ.get("WALLET")

l_account = Account.from_key(_pk)
blast3 = web3.Web3(
    web3.WebsocketProviderV2("wss://gateway.blast-prod.vertexprotocol.com/v1/ws")
)
print(blast3)
vtrx_client = create_vertex_client("blast-mainnet", signer=l_account)

btc_usd_perp = vtrx_client.subaccount.get_subaccounts()
for s in btc_usd_perp.subaccounts:
    print(s)
