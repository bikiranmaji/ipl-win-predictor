import streamlit as st
import pickle
import pandas as pd
import time
import math

teams = ['Chennai Super Kings',
 'Mumbai Indians',
 'Kolkata Knight Riders',
 'Gujarat Titans',
 'Delhi Capitals',
 'Lucknow Super Giants',
 'Punjab Kings',
 'Royal Challengers Bangalore',
 'Sunrisers Hyderabad',
 'Rajasthan Royals']

cities = ['Ahmedabad', 'Chennai', 'Mumbai', 'Kolkata', 'Delhi',
       'Dharamsala', 'Hyderabad', 'Lucknow', 'Jaipur', 'Chandigarh',
       'Guwahati', 'Navi Mumbai', 'Pune', 'Dubai', 'Sharjah', 'Abu Dhabi', 'Visakhapatnam', 'Bangalore', 'Ranchi', 'Cuttack',
       'Johannesburg', 'Durban', 'Centurion', 'Port Elizabeth',
       'Kimberley', 'East London', 'Cape Town']

pipe = pickle.load(open('pipe.pkl', 'rb'))

st.title('IPL Win Predictor')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(teams))

col3, col4 = st.columns(2)

with col3:
    selected_city = st.selectbox('Select Host City', sorted(cities))
with col4:
    target = st.number_input('Target', min_value = 1, step = 1, format = '%i')

col5, col6, col7 = st.columns(3)

with col5:
    score = st.number_input('Current Score', min_value = 0, max_value = target - 1, step = 1, format = '%i')
with col6:
    overs = st.number_input('Overs Completed', min_value = 0.1, max_value = 19.5, step = 0.1, format = '%1f')
with col7:
    wickets = st.number_input('Wickets Down', min_value = 0, max_value = 9, step = 1, format = '%i')

if st.button('Predict Win Probablity'):
    runs_left = target - score
    balls_left = 120 - (math.floor(overs) * 6 + (overs % 1) * 10)
    wickets =  10 - wickets
    curr_run_rate = score / overs
    req_run_rate = (runs_left * 6) / balls_left

    input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],'wickets_left':[wickets],'runs_off_bat_x':[target],'curr_run_rate':[curr_run_rate],'req_run_rate':[req_run_rate]})

    result = pipe.predict_proba(input_df)
    batting_team_win_percentage = result[0][1] * 100
    bowling_team_win_percentage = result[0][0] * 100
    col8, col9 = st.columns(2)
    with col8:
        batting_team_win_bar = st.progress(0)
        st.text(batting_team + " : " + str(round(batting_team_win_percentage)) + "%")
    with col9:
        bowling_team_win_bar = st.progress(0)
        st.text(bowling_team + " : " + str(round(bowling_team_win_percentage)) + "%")

    for percent_complete in range(batting_team_win_percentage.astype(int)):
        time.sleep(0.01)
        batting_team_win_bar.progress(percent_complete + 1)
    
    for percent_complete in range(bowling_team_win_percentage.astype(int)):
        time.sleep(0.01)
        bowling_team_win_bar.progress(percent_complete + 1)

