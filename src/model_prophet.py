import pandas as pd
import numpy as np

from fbprophet import Prophet
import matplotlib.pyplot as plt


def add_lags(df, N, lag_cols):
    """Adds lags up to N number of days to use as features
    The lag columns are labelled as 'adj_close_lag_1', 'adj_close_lag_2', ... etc.
    """
    # Use lags up to N number of days to use as features
    df_w_lags = df.copy()
    df_w_lags.loc[:, 'order_day'] = [x for x in list(range(len(df)))] # Add a column 'order_day' to indicate the order of the rows by date
    merging_keys = ['order_day'] # merging_keys
    shift_range = [x+1 for x in range(N)]

    for shift in shift_range:
        train_shift = df_w_lags[merging_keys + lag_cols].copy()

        # E.g. order_day of 0 becomes 1, for shift = 1.
        # So when this is merged with order_day of 1 in df_w_lags, this will represent lag of 1.
        train_shift['order_day'] = train_shift['order_day'] + shift

        foo = lambda x: '{}_lag_{}'.format(x, shift) if x in lag_cols else x
        train_shift = train_shift.rename(columns=foo)

        df_w_lags = pd.merge(df_w_lags, train_shift, on=merging_keys, how='left') #.fillna(0)
    del train_shift
    
    return df_w_lags


def make_forecast_df(data, periods=30):
    """
    inputs:
        data: DataFrame
        periods: 30
    returns: DataFrame prophet forecast dataframe.
    """
    df_ts = data[['price']]
    df_ts['ds'] = df_ts.index
    df_ts = df_ts.rename(columns={'price': 'y'})
    model = Prophet()
    model.fit(df_ts)
    df_forecast = model.make_future_dataframe(periods=periods, freq="D")
    df_forecast = model.predict(df_forecast)
    df_forecast = df_forecast.merge(df_ts, on='ds', how='left')
    return df_forecast


