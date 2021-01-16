import streamlit as st

from coingecko import get_full_token_df, get_trending_token_df, get_cg_price, get_coin_info_dict_by_id
from visualize import plotly_ma_daily_price, plotly_seasonal_decomposition, plotly_plot_forecast
from visualize import get_gecko_logo
from model import make_forecast_df


DF_TOKENS = get_full_token_df()
DF_TREND = get_trending_token_df()


def set_app_layout_and_return_text_input():
    """Create Side Pane
    """
    st.title('Crypto Asset Price Explorer')
    
    st.sidebar.title("Powered By CoinGecko!")
    st.sidebar.image(get_gecko_logo(), use_column_width=True)
    st.sidebar.header('**How to use:**')
    desc_markdown = """Search for any CoinGecko listed crpto asset using its **NAME** or ticker **SYMBOL**
    
    
    Examples:
    - name: bitcoin, ethereum, chainlink, etc.
    - symbol: sym:btc, sym:eth, sym:link, etc.

    """
    # st.sidebar.markdown(desc_markdown)

    # Adjust the left margin
    max_width_str = f"max-width: 1200px;"
    st.markdown(f"""
        <style>
        .reportview-container .main .block-container{{
            {max_width_str}
        }}
        </style>    
        """,
        unsafe_allow_html=True,
    )
    
    st.header('Search for Crypto Currency by (name/ticker symbol)')
    text_input = st.text_input('Enter a token name (bitcoin, ethereum, chainlink, etc) or a token symbol with preface sym: (sym:btc, sym:eth, etc.)', 'sym:btc')
    return text_input


def get_token_df_from_user_search(text_input):
    """Get token price df from user search.
    returns: DataFrame
    """
    input = text_input.lower()

    if input.startswith('sym:'):
        sym = input.split('sym:')[1]
        df_token = DF_TOKENS[DF_TOKENS['symbol'] == sym]
        return df_token
    df_token = DF_TOKENS[DF_TOKENS['name'].str.lower() == input]
    return df_token


def summarise_coin_info(resp):
    """Format streamlit high level coin summary from result dict.
    """
    repo = resp.get('links').get('repos_url').get("github")
    price_delta24hour = resp.get("market_data").get("price_change_24h_in_currency").get("usd")
    sentiment = resp.get("sentiment_votes_up_percentage")

    if price_delta24hour:
        if price_delta24hour > 0:
            msg = f'up ${price_delta24hour:,.2f}'
        elif price_delta24hour < 0:
            msg = f'down ${price_delta24hour:,.2f}'
        st.write('In the last 24 hours price is ' + msg)

    if sentiment:
        st.write(f'Sentiment: {sentiment}')

    if repo:
        st.write(f'See GitHub: {repo[0]}')
    return



if __name__ == '__main__':

    TEXT_INPUT = set_app_layout_and_return_text_input()
    DF_TOKEN = get_token_df_from_user_search(TEXT_INPUT)

    TITLE = f'Retrieving CoinGecko Price Data for {DF_TOKEN["name"].iloc[0]}'
    ID = DF_TOKEN['id'].iloc[0]

    COIN_INFO_DICT = get_coin_info_dict_by_id(ID)

    if st.checkbox('Show Everything from Coingecko:'):
        st.write(COIN_INFO_DICT)

    st.header(TITLE)

    summarise_coin_info(COIN_INFO_DICT)
    st.dataframe(DF_TOKEN)

    DF = get_cg_price(ID)

    MA_DAYS_FAST = st.select_slider('MA Days', range(5, 51), 20)
    MA_DAYS_SLOW = st.select_slider('MA Days', range(MA_DAYS_FAST, 200), 100)

    fig_ma = plotly_ma_daily_price(DF, ma_slow=MA_DAYS_SLOW, ma_fast=MA_DAYS_FAST)
    st.plotly_chart(fig_ma)

    if st.checkbox('Show Seasonal Decomposition'):
        fig_decomp = plotly_seasonal_decomposition(DF['price'])
        st.plotly_chart(fig_decomp)


    if st.checkbox('Prophet Forecast'):
        df_forecast = make_forecast_df(DF)
        fig_fc = plotly_plot_forecast(df_forecast)
        st.plotly_chart(fig_fc)