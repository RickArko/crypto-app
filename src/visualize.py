import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

from plotly.subplots import make_subplots
from statsmodels.tsa.seasonal import seasonal_decompose

from io import BytesIO
from PIL import Image

WIDTH = 1_000
HEIGHT = 1_000


def get_gecko_logo():
    """Display coingecko image from static dir.
    """
    with open('static/gecko-mask.jpg', 'rb') as image:
        f = image.read()
        img = Image.open((BytesIO(f)))
        img.convert('RGB')
    
    return img


def plotly_ma_daily_price(df, ma_slow, ma_fast):
    """
    df : DataFrame (index: Date datetime, Price float)
    """
    df[f"{ma_slow}dayMA"] = df['price'].rolling(ma_slow).mean()
    df[f"{ma_fast}dayMA"] = df['price'].rolling(ma_fast).mean()
    dfl = df.reset_index().melt(id_vars="Date", value_vars=["price", f"{ma_fast}dayMA", f"{ma_slow}dayMA"], value_name="Value", var_name="Description")
    fig = px.line(dfl, x="Date", y='Value', title='Daily Price', color="Description")

    x_axis_dict = dict(
        rangeselector=dict(buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
    fig.update_layout(xaxis=x_axis_dict, width=WIDTH, height=HEIGHT)
    # fig.update_layout(title='Fast and Slow Moving Average', width=WIDTH, height=HEIGHT)
    return fig


def plotly_seasonal_decomposition(ts):
    """
     inputs: ts array-like, timeseries
     returns: plotly.Figure
    """
    freq = 365

    if len(ts) <= 750:
        freq = 1

    decomp = seasonal_decompose(ts, model='additive', period=freq)

    trend = decomp.trend
    seasonal = decomp.seasonal
    residual = decomp.resid

    fig = make_subplots(rows=2, cols=2, subplot_titles=['TimeSeries', 'Trend', 'Seasonal', 'Residual'], vertical_spacing=.05)

    fig_ts = go.Scatter(name="TimeSeries", x=ts.index, y=ts, hovertemplate="%{y:$,.0f}")
    fig_trend = go.Scatter(name="Trend", x=trend.index, y=trend, hovertemplate="%{y:$,.0f}")
    fig_seasonal = go.Scatter(name="Seasonal", x=seasonal.index, y=seasonal, hovertemplate="%{y:$,.0f}")
    fig_resid = go.Scatter(name="Residuals", x=residual.index, y=residual, hovertemplate="%{y:$,.0f}")

    fig.add_trace(fig_ts, row=1, col=1)
    fig.add_trace(fig_trend, row=1, col=2)
    fig.add_trace(fig_seasonal, row=2, col=1)
    fig.add_trace(fig_resid, row=2, col=2)
    fig.update_layout(title=f"Seasonal Decomposition ({freq} periods)", height=HEIGHT, width=WIDTH)

    return fig


def plotly_plot_forecast(df_forecast):
    """
        inputs: ts array-like, timeseries
        returns: plotly.Figure
    """
    fig = go.Figure()
    # trend = go.Scatter(name='trend', mode='lines', x=df_forecast['ds'].tolist(), y=df_forecast['yhat'].tolist(), marker=dict(color='red', line=dict(width=3)))
    lower_band = go.Scatter(name="lower_band", mode="lines", x=df_forecast["ds"].tolist(), y=df_forecast["yhat_lower"].tolist(), line= dict(color='#FF8787'), hovertemplate="%{y:$,.02f}")
    upper_band = go.Scatter(name="upper_band", mode="lines", x=df_forecast["ds"].tolist(), y=df_forecast["yhat_upper"].tolist(), line=dict(color="#229442"), hovertemplate="%{y:$,.02f}", fill="tonexty")
    actual_price = go.Scatter(name="Actual", mode="markers", x=df_forecast["ds"].tolist(), y=df_forecast["y"].tolist(), marker=dict(symbol='x', color="#475A61"), hovertemplate="%{y:$,.02f}")
    price_forecast = go.Scatter(name="Forecast", mode="markers", x=df_forecast["ds"].tolist(), y=df_forecast["yhat"].tolist(), marker=dict(symbol='x', color="#5948E0"), hovertemplate="%{y:$,.02f}")
    # fig.add_trace(trend)
    fig.add_trace(actual_price)
    fig.add_trace(lower_band)
    fig.add_trace(upper_band)
    fig.add_trace(price_forecast)

    x_axis_dict = dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="ytd", step="year", stepmode="todate"),
                dict(step="all")
                ])
            ),
        rangeslider=dict(visible=True),
        type="date",
        zeroline=True)

    fig.update_layout(xaxis=x_axis_dict, width=WIDTH, height=HEIGHT)
    # fig.show()
    return fig
    

