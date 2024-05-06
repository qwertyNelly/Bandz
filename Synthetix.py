from synthetix import Synthetix
from synthetix.core import Core
from os import environ
from kwenta import kwenta
from web3 import providers
import json

perp_account_id = environ.get('PERP_ACCOUNT_ID']
snx_account_id = environ.get('SNX_ACCOUNT_ID')

wallet = environ.get("WALLET")
pk = environ.get(
    "PK"
)

snx = Synthetix(
    provider_rpc="https://base-mainnet.g.alchemy.com/v2/5we2Js--5Ad5bVil4IVadRv0KDdcVpTP",
    network_id=8453,
    address=wallet,
    private_key=pk,
)
snxc = Core(snx=snx)
print(f"SNX Address: {snx.address}")


paddress = snx.perps.market_proxy.address
print(f"Proxy Address : {paddress}")


print(snx.perps.get_market_summaries())
# print(snx.perps.get_market_summary(84532))


# def create_account():
#     ret = snx.perps.create_account(0, submit=True)
#     print(ret)


# create_account()
approve_tx = snx.spot.approve(wallet, market_name="sUSD")

print(approve_tx)
print(f"Accounts:{snx.perps.get_account_ids()}")
print(snx.get_susd_balance(paddress))


def get_susd_balance() -> dict:
    return snx.get_susd_balance()


def get_collateral():
    return snx.perps.get_collateral_balances()


positions = snx.perps.get_open_positions()
print(f"Open Positions : {positions}")
print(f"SUSD Balance : {snx.get_susd_balance()}")
print(f"Proxy Address : {snx.perps.market_proxy.address}")
print(f"Collateral : {get_collateral()}")
print(f"sUSD Balance : {snx.get_susd_balance()}")
print(f"ETH Balance : {snx.get_eth_balance()}")

print(get_collateral())


class DumboBot:
    snx = Synthetix(
        provider_rpc="https://base-mainnet.g.alchemy.com/v2/5we2Js--5Ad5bVil4IVadRv0KDdcVpTP",
        network_id=8453,
        address=wallet,
        private_key=pk,
    )

    def __init__(self, snx: Synthetix):
        self.snx = snx
        self.eth_balance = json.loads(snx.get_eth_balance())["ETH"]
        self.susd_balance = json.loads(snx.get_susd_balance())["sUSD"]
        self.account = snx.perps.create_account()
        self.network_id = snx.network_id
        print(self.eth_balance)
        print(self.susd_balance)
        print(self.network)

    @property
    def eth_balance():
        return snx.get_eth_balance()

    @eth_balance.setter
    def eth_balance(self):
        self.eth_balance = snx.get_eth_balance()
        pass

    @property
    def account():
        pass

    print(f"Collateral : {snx.perps.get_collateral_balances()}")
    print(f"sUSD Balance : {snx.get_susd_balance()}")
    print(f"ETH Balance : {snx.get_eth_balance()}")
    perps_address = snx.perps.market_proxy.address
    approve_tx = snx.spot.approve(perps_address, market_name="sUSD", submit=True)

    def modify_collateral(self, amount, market, account):
        deposit_tx = snx.perps.modify_collateral(
            amount, market_name=market, account_id=self.account, submit=True
        )
        snx.logger.info(deposit_tx)

    def submit_order(size, market):
        snx.perps.commit_order(0.1, market_name="ETH", submit=True)


def get_sm_account():
    global accounts
    account = snx.perps.get_account_ids(default_account_id=perp_account_id)
    for a in account:
        snx.logger.info("Entering Loop")
        accounts.append(a)
        snx.logger.info(f"Appended Account {a}")
    return accounts


def get_susd_wallet_balance():
    return snx.get_susd_balance("0x589197b4AFC9E50A2cc872540a3760C624BBF97c")


def check_collateral():
    if (
        json.loads(snx.perps.get_collateral_balances())["sUSD"]
        > json.loads(snx.get_susd_balance())["sUSD"]
    ):
        print("Hello")


def get_historical_data():
    queries.Queries(kwenta="")


perps_address = snx.perps.market_proxy.address


def create_account():
    return snx.perps.create_account()  # submit=True)


def submit_order(size: int, market: str, limit):
    order = snx.perps.commit_order(
        size, market_name=market, desired_fill_price=3006, submit=True
    )
    return order


perps_address = snx.perps.market_proxy.address
snx.perps.commit_order(10, market_name="ETH", desired_fill_price=3006, submit=True)

# approve_tx = snx.spot.approve(perps_address, market_name='sUSD', submit=True)
# deposit_tx = snx.perps.modify_collateral(2, market_name='sUSD', submit=True)


print(snx.perps.get_open_positions())

providers.rpc.HTTPProvider()
wallet = environ.get("WALLET", "0x589197b4AFC9E50A2cc872540a3760C624BBF97c")
pk = environ.get(
    "PK", 
)
account = None


def get_accounts() -> dict:
    try:
        return kwn.get_sm_accounts()[0]
    except IndexError() as e:
        return kwn.new_sm_account()


print(get_accounts())
