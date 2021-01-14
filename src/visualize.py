import pandas as pd
import plotly.express as px


WIDTH = 1_000
HEIGHT = 1_000


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
