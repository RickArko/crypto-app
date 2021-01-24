import pandas as pd
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

 
def get_full_token_df():
    """
    returns: DataFrame
    """
    TOKEN_LIST = cg.get_coins_list()
    DF_TOKENS = pd.DataFrame(TOKEN_LIST)
    return DF_TOKENS


def get_trending_token_df():
    """
    returns: DataFrame
    """
    TREND_DICT = cg.get_search_trending()
    DF_TREND = pd.concat([pd.json_normalize(dic) for dic in TREND_DICT.get('coins')])
    return DF_TREND 


def get_cg_price(coingeckoid):
    """Fetches and returns DataFrame of Historic price data from CoingeckoAPI.

    inputs:
        coingeckoid - str: required see DF_TOKENS
    returns:
        DataFrame (daily historic prices indexed by date.)
    """
    resp = cg.get_coin_market_chart_by_id(
            id=coingeckoid, vs_currency="usd", days='max'
        )

    prices = pd.Series([l[1] for l in resp['prices']], index=[l[0] for l in resp['prices']])
    market_caps = pd.Series([l[1] for l in resp['market_caps']], index=[l[0] for l in resp['market_caps']])
    total_volumes = pd.Series([l[1] for l in resp['total_volumes']], index=[l[0] for l in resp['total_volumes']])

    data = {"price": prices, "market_caps": market_caps, "total_volumes": total_volumes}
    df = pd.DataFrame(data)
    df.index = pd.to_datetime(df.index, unit="ms")
    df.index.name = "Date"
    df['daily_return'] = df['price'].shift(1) / df['price'] - 1
    return df


def get_coin_info_dict_by_id(coingeckoid):
    """
    returns: dict
    """
    resp = cg.get_coin_by_id(coingeckoid)
    return resp


def get_cg_daily_ohlc(coingeckoid):
    """
    returns: DataFrame (index: datetime, open, high, low, close)
    """
    resp = cg.get_coin_ohlc_by_id(id=coingeckoid, vs_currency='usd', days='max')

    df = pd.DataFrame(resp, columns=['time', 'open', 'high', 'low', 'close'])
    df['datetime'] = pd.to_datetime(df['time'], unit='ms')
    df = df.set_index('datetime')
    return df
