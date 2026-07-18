import streamlit as st

st.markdown("""
<style>
    /* Widget labels (titles) */
    div[data-testid="stRadio"] label p,
    div[data-testid="stSelectbox"] label p {
        font-size: 18px !important;
        font-weight: 600 !important;
    }
    
    /* Selectbox ke andar selected value ka text (e.g. "A Ashish Reddy") */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        font-size: 21px !important;
    }
    
    /* Radio options ka text */
    div[data-testid="stRadio"] label span {
        font-size: 16px !important;
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="PitchIQ", page_icon="🏏", layout="wide")

home_page = st.Page("views/home.py", title="Home", icon="🏠")
batting_page = st.Page("views/batting_predictor.py", title="Batting Predictor", icon="🏏")
bowling_page = st.Page("views/bowling_predictor.py", title="Bowling Predictor", icon="🎯")
insights_page = st.Page("views/player_insights.py", title="Player Insights", icon="📈")

pg = st.navigation([home_page, batting_page, bowling_page, insights_page], position="top")
pg.run()
