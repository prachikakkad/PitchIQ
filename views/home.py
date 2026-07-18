import streamlit as st

# Hero section
st.title("PitchIQ 🏏")
st.markdown("##### Data-driven cricket insights, powered by IPL history (2008–2026)")

st.markdown("---")

# Overview
st.markdown("""
**PitchIQ** predicts IPL player performance using historical match context — 
player identity, venue, opponent, and past form. Built as an exploratory 
What-If tool for batting and bowling outcomes.
""")

# Honest R² summary — use columns for a clean card layout
st.markdown("### Model Performance")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Batting Model (R²)", value="0.11")
    st.caption("Predicts runs using player history, venue & opponent context")

with col2:
    st.metric(label="Bowling Model (R²)", value="0.02")
    st.caption("Wickets are highly match-dependent — treat as directional only")

st.info(
    "📊 **Note on accuracy:** These models use only pre-match context (no live "
    "match data). Real cricket outcomes involve high in-match variance — "
    "predictions should be read as *tendencies*, not precise forecasts."
)

st.markdown("---")

# Navigation guide
st.markdown("### Explore")
nav1, nav2, nav3 = st.columns(3)

with nav1:
    st.markdown("**🏏 Batting Predictor**")
    st.caption("Predict expected runs for a player in a given matchup")

with nav2:
    st.markdown("**🎯 Bowling Predictor**")
    st.caption("Predict expected wickets (exploratory, low confidence)")

with nav3:
    st.markdown("**📈 Player Insights**")
    st.caption("Explore historical trends, venue & opponent-wise stats")

st.caption("Use the sidebar to navigate between pages →")