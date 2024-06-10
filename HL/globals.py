#/Users/I516172/Desktop/Bandz/.venv/bin python3
from HL.util.utils import setup
from hyperliquid.utils.constants import MAINNET_API_URL as mainnet, TESTNET_API_URL as testnet
from dotenv import load_dotenv
import os

load_dotenv
env = os.environ.get('ENVIORNMENT', 'test')


# ++++ Order Globals +++
DEFAULT_SLIPPAGE = 0.05




env_loaded = load_dotenv()

if not env_loaded:
    raise EnvironmentError()

if env[:4].__eq__('prod'):
    try:
        ADDRESS, INFO, EXCHANGE = setup(testnet)
    except Exception as e:
        raise e
else:
    try:
        ADDRESS, INFO, EXCHANGE = setup(mainnet)
    except Exception as e:
        raise e