# PitchIQ 🏏

**Data-driven IPL player performance insights and a What-If prediction tool — built with Streamlit and scikit-learn.**

PitchIQ lets you explore historical IPL player performance and generate directional predictions for batting and bowling outcomes based on match context (venue, opponent, toss, and historical form).

---

## Features

- **Batting Predictor** — Predicts expected runs for a player in a given matchup (venue, opponent, toss decision, innings context).
- **Bowling Predictor** — Predicts expected wickets under the same kind of match context.
- **Player Insights** — Career summary (matches, average, strike rate / economy, best performance) plus season-wise, venue-wise, and opponent-wise breakdowns with visualizations.
- Dark, cricket-themed UI with a horizontal top navigation bar.

---

## How It Works

Both models are trained on ball-by-ball IPL data (2008–2026), aggregated to player-match level. Features used:

- Player identity, venue, team, opponent, toss decision, season, innings context
- Historical form indicators: career average, average vs. this opponent, average at this venue, recent form (last 5 matches)

Models are built with **Linear Regression** (scikit-learn), chosen after comparing against a tuned Random Forest that showed no meaningful improvement on this feature set.

### A note on accuracy

| Model | R² (Test) |
|---|---|
| Batting (Runs) | ~0.11 |
| Bowling (Wickets) | ~0.02 |

These scores are intentionally low, and that's the point: after iterating through multiple rounds of feature engineering (static context → historical averages → recent form), it became clear that **individual match performance in cricket is dominated by in-match variance** (day's form, catches, umpiring, pitch behavior) rather than static pre-match context. Predictions in this app should be read as **directional tendencies, not precise forecasts** — this is explicitly disclaimed in the app itself, especially on the Bowling Predictor page.

---

## Tech Stack

- **Frontend/App:** Streamlit
- **ML:** scikit-learn (Linear Regression)
- **Data processing:** pandas
- **Visualization:** Matplotlib
- **Model persistence:** joblib

---

## Project Structure

```
pitchiq/
├── app.py                      # Navigation entry point
├── requirements.txt
├── .streamlit/
│   └── config.toml             # Theme config
├── views/
│   ├── home.py
│   ├── batting_predictor.py
│   ├── bowling_predictor.py
│   └── player_insights.py
├── models/
│   ├── batter_model.pkl
│   └── bowler_model.pkl
├── encoders/
│   ├── batter_encoders.pkl
│   └── bowler_encoders.pkl
└── data/
    ├── ml_batter.csv
    └── ml_bowler.csv
```

---

## Running Locally

```bash
git clone https://github.com/<your-username>/pitchiq.git
cd pitchiq
pip install -r requirements.txt
streamlit run app.py
```

---

## Data Source

IPL ball-by-ball delivery data (2008–2026), sourced from Kaggle, aggregated to player-match level for training.

---

## Author

Built by [Your Name] as a portfolio project exploring the boundary of what pre-match context can (and can't) predict in cricket.
