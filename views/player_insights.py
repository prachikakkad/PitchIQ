import streamlit as st
import pandas as pd
import joblib

st.title("📈 Player Insights")
st.markdown("##### Explore historical performance trends")
st.markdown("---")

stat_type = st.radio("View Stats For", ["Batting", "Bowling"], horizontal=True)

@st.cache_data
def load_data():
    return pd.read_csv("data/ml_batter.csv")
batter_df = load_data()

@st.cache_data
def load_data():
    return pd.read_csv("data/ml_bowler.csv")
bowler_df = load_data()

if stat_type == "Batting":
    data = batter_df
    player_col = 'batter'
    metric_col = 'runs'
else:
    data = bowler_df
    player_col = 'bowler'
    metric_col = 'wickets'

player = st.selectbox("Select Player", sorted(data[player_col].unique()))
player_data = data[data[player_col] == player]

# graphs and stats

st.markdown(f"### Career Summary : {player}")

if stat_type == "Batting":
    total_runs = player_data['runs'].sum()
    total_balls = player_data['balls_faced'].sum()
    strike_rate = (total_runs / total_balls * 100) if total_balls > 0 else 0
    matches_played = player_data.shape[0]
    avg_runs = player_data['runs'].mean()
    highest_score = player_data['runs'].max()

    summary = pd.DataFrame({
        "Metric": ["Matches", "Total Runs", "Average", "Strike Rate", "Highest Score"],
        "Value": [matches_played, total_runs, f"{avg_runs:.1f}", f"{strike_rate:.1f}", highest_score]
    })

else:
    total_wickets = player_data['wickets'].sum()
    total_balls = player_data['balls_bowled'].sum()
    total_runs_conceded = player_data['runs_conceded'].sum()
    economy = (total_runs_conceded / (total_balls / 6)) if total_balls > 0 else 0
    matches_played = player_data.shape[0]
    avg_wickets = player_data['wickets'].mean()
    best_match = player_data.loc[player_data['wickets'].idxmax()]
    best_figures = f"{int(best_match['wickets'])}/{int(best_match['runs_conceded'])}"

    summary = pd.DataFrame({
        "Metric": ["Matches", "Total Wickets", "Average", "Economy Rate", "Best Figures"],
        "Value": [matches_played, total_wickets, f"{avg_wickets:.2f}", f"{economy:.2f}", best_figures]
    })

st.table(summary)

import matplotlib.pyplot as plt

st.markdown("### Venue-wise Performance")

venue_stats = player_data.groupby('venue')[metric_col].mean().sort_values(ascending=False).head(8)

fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('#0E1117')
ax.set_facecolor('#0E1117')

bars = ax.bar(venue_stats.index, venue_stats.values, color='#00A86B')

ax.set_xlabel("Venue")
ax.set_ylabel(f"Avg {metric_col.capitalize()}")
ax.set_title(f"{player}'s Average {metric_col.capitalize()} by Venue")
ax.tick_params(colors='white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.title.set_color('white')
plt.xticks(rotation=45, ha='right')

for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.1f}', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', fontsize=8, color='white')

st.pyplot(fig)

# #############

st.markdown("### Season-wise Trend")

season_stats = player_data.groupby('season')[metric_col].mean().sort_index()

fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('#0E1117')
ax.set_facecolor('#0E1117')

bars = ax.bar(season_stats.index.astype(str), season_stats.values, color='#00A86B')

ax.set_xlabel("Season")
ax.set_ylabel(f"Avg {metric_col.capitalize()}")
ax.set_title(f"{player}'s Average {metric_col.capitalize()} by Season")
ax.tick_params(colors='white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.title.set_color('white')
plt.xticks(rotation=45, ha='right')

for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.1f}', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', fontsize=8, color='white')

st.pyplot(fig)

# #############

st.markdown("### Opponent-wise Performance")

opponent_stats = player_data.groupby('opponent_team')[metric_col].mean().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('#0E1117')
ax.set_facecolor('#0E1117')

bars = ax.bar(opponent_stats.index, opponent_stats.values, color='#00A86B')

ax.set_xlabel("Opponent Team")
ax.set_ylabel(f"Avg {metric_col.capitalize()}")
ax.set_title(f"{player}'s Average {metric_col.capitalize()} vs Opponents")
ax.tick_params(colors='white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.title.set_color('white')
plt.xticks(rotation=45, ha='right')

for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.1f}', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', fontsize=8, color='white')

st.pyplot(fig)