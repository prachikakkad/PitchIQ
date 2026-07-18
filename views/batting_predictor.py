import streamlit as st
import pandas as pd
import joblib

st.title("🏏 Batting Predictor")
st.markdown("##### Predict expected runs based on player, venue & match context")
st.markdown("---")

@st.cache_data
def load_data():
    return pd.read_csv("data/ml_batter.csv")
df = load_data()

@st.cache_resource
def load_encoder():
    return joblib.load("encoders/batter_encoders.pkl")
encoder = load_encoder()

@st.cache_resource
def load_model():
    return joblib.load("models/batter_model.pkl")
model = load_model()

# form

with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        player = st.selectbox("Batsman", encoder['batter'].classes_)
        venue = st.selectbox("Venue", encoder['venue'].classes_)
        batting_team = st.selectbox("Batting Team", encoder['batting_team'].classes_)
        opponent = st.selectbox(
            "Opponent Team", 
            [team for team in encoder['opponent_team'].classes_ if team != batting_team]
        )
    
    with col2:
        toss_decision = st.selectbox("Toss Decision", ["bat", "field"])
        season = st.selectbox("Season", sorted(df['season'].unique()))
        is_chasing = st.radio("Batting Situation", ["Chasing (2nd innings)", "Defending (1st innings)"])
        is_chasing = True if is_chasing == "Chasing (2nd innings)" else False

    st.markdown("") 
    submitted = st.form_submit_button("🔮 Predict Runs", use_container_width=True)

if submitted:
    player_data = df[df['batter'] == player]
    
    career_avg = player_data['runs'].mean()
    
    vs_opp_data = player_data[player_data['opponent_team'] == opponent]
    vs_opponent_avg = vs_opp_data['runs'].mean() if len(vs_opp_data) > 0 else career_avg
    
    at_venue_data = player_data[player_data['venue'] == venue]
    at_venue_avg = at_venue_data['runs'].mean() if len(at_venue_data) > 0 else career_avg

    recent_matches = player_data.sort_values('match_id').tail(5)
    recent_form = recent_matches['runs'].mean()

    # encode inputs and predict

    player_enc = encoder['batter'].transform([player])[0]
    venue_enc = encoder['venue'].transform([venue])[0]
    batting_team_enc = encoder['batting_team'].transform([batting_team])[0]
    opponent_enc = encoder['opponent_team'].transform([opponent])[0]
    toss_enc = encoder['toss_decision'].transform([[toss_decision]])[0][0]

    input_df = pd.DataFrame([[
        player_enc, venue_enc, batting_team_enc, opponent_enc,
        toss_enc, season, is_chasing, career_avg, vs_opponent_avg, at_venue_avg, recent_form
    ]], columns=[
        'batter', 'venue', 'batting_team', 'opponent_team',
        'toss_decision', 'season', 'is_chasing', 
        'career_avg_runs', 'avg_vs_opponent', 'avg_at_venue', 'recent_form_5'
    ])

    prediction = model.predict(input_df)[0]

    st.markdown("---")
    st.metric(label="Predicted Runs", value=f"{prediction:.1f}")