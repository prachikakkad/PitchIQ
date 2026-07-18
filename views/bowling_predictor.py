import streamlit as st
import pandas as pd
import joblib

with st.spinner("Loading model..."):
    @st.cache_data
    def load_data():
        return pd.read_csv("data/ml_bowler.csv")
    df = load_data()

    @st.cache_resource
    def load_encoder():
        return joblib.load("encoders/bowler_encoders.pkl")
    encoder = load_encoder()

    @st.cache_resource
    def load_model():
        return joblib.load("models/bowler_model.pkl")
    model = load_model()

st.title("🎯 Bowling Predictor")
st.markdown("##### Predict expected wickets based on bowler, venue & match context")
st.markdown("---")

st.info(
    "📊 **Note:** Bowling predictions have lower accuracy (R² ~0.02) compared to batting — "
    "wicket-taking is highly influenced by match-day factors (catches, umpiring, pitch behavior) "
    "not captured in this model. Treat results as directional, not precise."
)

with st.form("bowling_prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        bowler = st.selectbox("Bowler", encoder['bowler'].classes_)
        venue = st.selectbox("Venue", encoder['venue'].classes_)
        bowling_team = st.selectbox("Bowling Team", encoder['bowling_team'].classes_)
        opponent = st.selectbox(
            "Opponent Team",
            [team for team in encoder['opponent_team'].classes_ if team != bowling_team]
        )

    with col2:
        toss_decision = st.selectbox("Toss Decision", ["bat", "field"])
        season = st.selectbox("Season", sorted(df['season'].unique()))
        is_chasing = st.radio("Match Innings", ["1st Innings", "2nd Innings (Chasing)"])
        is_chasing = True if is_chasing == "2nd Innings (Chasing)" else False

    st.markdown("")
    submitted = st.form_submit_button("🔮 Predict Wickets", use_container_width=True)

if submitted:
    player_data = df[df['bowler'] == bowler]
    
    career_avg = player_data['wickets'].mean()
    
    vs_opp_data = player_data[player_data['opponent_team'] == opponent]
    vs_opponent_avg = vs_opp_data['wickets'].mean() if len(vs_opp_data) > 0 else career_avg
    
    at_venue_data = player_data[player_data['venue'] == venue]
    at_venue_avg = at_venue_data['wickets'].mean() if len(at_venue_data) > 0 else career_avg

    recent_matches = player_data.sort_values('match_id').tail(5)
    recent_form = recent_matches['wickets'].mean()

    # encode inputs and predict

    player_enc = encoder['bowler'].transform([bowler])[0]
    venue_enc = encoder['venue'].transform([venue])[0]
    bowling_team_enc = encoder['bowling_team'].transform([bowling_team])[0]
    opponent_enc = encoder['opponent_team'].transform([opponent])[0]
    toss_enc = encoder['toss_decision'].transform([[toss_decision]])[0][0]

    input_df = pd.DataFrame([[
        player_enc, venue_enc, bowling_team_enc, opponent_enc,
        toss_enc, season, is_chasing, career_avg, vs_opponent_avg, at_venue_avg, recent_form
    ]], columns=[
        'bowler', 'venue', 'bowling_team', 'opponent_team',
        'toss_decision', 'season', 'is_chasing', 
        'career_avg_wkts', 'avg_vs_opponent', 'avg_at_venue', 'recent_form_5'
    ])

    prediction = model.predict(input_df)[0]

    st.metric(label="Predicted wickets", value=f"{round(prediction)}")