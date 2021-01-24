import pandas as pd

from ta import add_all_ta_features
from ta.volatility import BollingerBands

from coingecko import get_cg_daily_ohlc, get_cg_price
from coingecko import get_coin_info_dict_by_id



# dff = add_all_ta_features(DF, 'open', 'high', 'low', 'close','volume')
# df_ohlc = get_cg_daily_ohlc(ID)
# dft = DF.join(df_ohlc, how='left')



class CoingeckoCoin:
    def __init__(self, id):
        """Initialize Class with coingecko id.
        """
        self.info_dict = get_coin_info_dict_by_id(id)
        self.df_ohlc = get_cg_daily_ohlc(id)
        self.df = get_cg_price(id)
        
    

coin = CoingeckoCoin(ID)
# coin.info_dict
# coin.df
# coin.df_ohlc