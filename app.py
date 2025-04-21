import streamlit as st
from stream import SportPredictor
import datetime

st.header("This is a Sport Prediction Model. Beta Version")

with open("all_teams.txt", "r") as file:
    teams = [team.strip() for team in file.readlines()]

home_team = st.selectbox("Select Home Team", teams)
away_team = st.selectbox("Select Away Team", teams)
match_date = st.date_input(
    "Match Date",
    value=datetime.date.today(),
    min_value=datetime.date(2000, 1, 1),
    max_value=datetime.date(2030, 12, 31)
)

predictor = SportPredictor(HomeTeam=home_team, AwayTeam=away_team, MatchDate=match_date)

if st.button("Predict Match Result"):
    if home_team != away_team:
        result = predictor.predict
        st.success(f"🏁 Predicted Result: {result}")
    else:
        st.error("Please choose different teams.")

if st.button("Check HomeTeam Data"):
    st.subheader(f"Match History for {home_team}")
    dataframeHome, scoreHome = predictor.get_homeTeam_past_data
    st.write(scoreHome)
    st.dataframe(dataframeHome)
    
if st.button("Check AwayTeam Data"):
    st.subheader(f"Match History for {away_team}")
    dataframeAway, scoreAway = predictor.get_awayTeam_past_data
    st.write(scoreAway)
    st.dataframe(dataframeAway)
