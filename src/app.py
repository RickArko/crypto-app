import streamlit as st

from coingecko import get_full_token_df, get_trending_token_df, get_cg_price, get_coin_info_dict_by_id
from visualize import plotly_ma_daily_price

DF_TOKENS, DF_TREND = get_full_token_df(), get_trending_token_df()

max_width_str = f"max-width: 1200px;"
st.markdown(
    f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
    unsafe_allow_html=True,
)


def get_token_df_from_user_search(text_input):
    """
    returns: DataFrame
    """
    input = text_input.lower()
    if input.startswith('sym:'):
        sym = input.split('sym:')[1]
        df_token = DF_TOKENS[DF_TOKENS['symbol'] == sym]
        return df_token

    # elif len(input) ==3:
    
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

if __name__ == '__main__':

    st.title('Crypto Price Explorer')

    st.header('Search for Crypto Currency by (symbol/name/id)')
    TEXT_INPUT = st.text_input('Enter a token name (bitcoin, ethereum, chainlink, etc) or a token symbol with preface sym: (sym:btc, sym:eth, etc.)', 'sym:btc')
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