#/Users/I516172/Desktop/Bandz/.venv/bin python3
from HL.util.utils import setup
from hyperliquid.utils.constants import MAINNET_API_URL as mainnet

# ++++ Order Globals +++
DEFAULT_SLIPPAGE = 0.05


try:
    ADDRESS, INFO, EXCHANGE = setup(mainnet)
except Exception as e:
    raise e