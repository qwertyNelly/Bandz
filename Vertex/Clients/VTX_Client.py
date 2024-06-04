#!/Users/ben/Desktop/bndni/.venv/bin python3.11
# -*- coding: utf-8 -*-
from vertex_protocol import VertexProtocol
import os
import time
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


class vtx_client:

    _pk = os.environ.get("PK")
    _wallet = os.environ.get("WALLET")

    def __init__(self, _wallet=_wallet, _private_key=_pk):
        self._wallet = _wallet
        self._pk = _private_key
