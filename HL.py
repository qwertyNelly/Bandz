from hyperliquid.info import Info
from hyperliquid.api import API
from hyperliquid.utils import constants
import json

wallet = "0x589197b4AFC9E50A2cc872540a3760C624BBF97c"

account_info = Info(constants.MAINNET_API_URL)


def get_positions() -> dict:
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
    return account_info.user_state("0x589197b4AFC9E50A2cc872540a3760C624BBF97c")


positions = get_positions()["assetPositions"]
for p in positions:
    print(p)
    print("\n")


print(account_info.all_mids())
