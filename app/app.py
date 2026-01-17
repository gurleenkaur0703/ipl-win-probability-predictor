import streamlit as st
import pickle
import pandas as pd
import base64
import os

# -------------------- Background setup --------------------
def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

background_image = get_base64(os.path.join(os.path.dirname(__file__), "BG.jpg"))

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{background_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    .overlay {{
        background-color: rgba(0, 0, 0, 0.45);
        padding: 1rem 1.2rem;
        border-radius: 12px;
        margin-bottom: 10px;
    }}

    h1, h2, h3, .stSelectbox label, .stNumberInput label {{
        color: white !important;
        text-shadow: 1px 1px 2px black;
        font-weight: 600;
    }}

    .prob-title {{
        color: white;
        font-size: 20px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 8px;
        text-shadow: 1px 1px 2px black;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------- Load trained pipeline --------------------
pipe = pickle.load(open("pipe.pkl", "rb"))

# -------------------- Team and city options --------------------
teams = [
    "Chennai Super Kings",
    "Delhi Capitals",
    "Gujarat Titans",
    "Kolkata Knight Riders",
    "Lucknow Super Giants",
    "Mumbai Indians",
    "Punjab Kings",
    "Rajasthan Royals",
    "Royal Challengers Bangalore",
    "Sunrisers Hyderabad"
]

cities = [
    "Ahmedabad",       # Narendra Modi Stadium
    "Lucknow",         # Ekana Cricket Stadium
    "Mumbai",          # Wankhede Stadium
    "Chennai",         # M.A. Chidambaram Stadium
    "Kolkata",         # Eden Gardens
    "Delhi",           # Arun Jaitley Stadium
    "Bengaluru",       # M. Chinnaswamy Stadium
    "Hyderabad",       # Rajiv Gandhi International Stadium
    "Jaipur",          # Sawai Mansingh Stadium
    "Visakhapatnam",   # ACA-VDCA Cricket Stadium
    "Guwahati",        # Barsapara Cricket Stadium
    "Dharamsala",      # HPCA Stadium
    "Mullanpur"        # Maharaja Yadavindra Singh International Cricket Stadium (New Chandigarh)
]

# -------------------- App title --------------------
st.markdown("<h1 class='overlay'>🏏 IPL Win Probability Predictor</h1>", unsafe_allow_html=True)

# -------------------- Inputs --------------------
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox("Select the batting team", sorted(teams))

with col2:
    bowling_team = st.selectbox(
        "Select the bowling team",
        [t for t in sorted(teams) if t != batting_team]
    )

selected_city = st.selectbox("Select host city", sorted(cities))

target = st.number_input("Target", min_value=0, value=150)

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input("Score", min_value=0, value=0)

with col4:
    overs = st.number_input("Overs completed", min_value=0.0, max_value=20.0, step=0.1, value=0.0)

with col5:
    wickets_out = st.number_input("Wickets out", min_value=0, max_value=10, value=0)

# -------------------- Prediction --------------------
if st.button("Predict Probability"):

    # 1) Prevent invalid cases (score > target)
    if score > target:
        st.error("⚠️ Score cannot be greater than Target!")
        st.stop()

    # 2) Overs should not be 20.0 (balls_left becomes 0)
    if overs >= 20:
        st.error("⚠️ Overs completed should be less than 20 for live prediction.")
        st.stop()

    # Feature calculations
    runs_left = target - score
    balls_bowled = int(overs * 6)
    balls_left = 120 - balls_bowled
    wickets_left = 10 - wickets_out

    crr = (score / overs) if overs > 0 else 0
    rrr = (runs_left * 6 / balls_left) if balls_left > 0 else 0

    # Build input dataframe (keep same columns as your trained pipeline)
    input_df = pd.DataFrame({
        "batting_team": [batting_team],
        "bowling_team": [bowling_team],
        "city": [selected_city],
        "runs_left": [runs_left],
        "balls_left": [balls_left],
        "wickets": [wickets_left],
        "total_runs_x": [target],
        "crr": [crr],
        "rrr": [rrr]
    })

    # Predict probabilities
    proba = pipe.predict_proba(input_df)[0]
    loss = proba[0]
    win = proba[1]

    batting_perc = round(win * 100)
    bowling_perc = round(loss * 100)

    # -------------------- Output --------------------
    st.markdown("<h2 class='overlay'>📊 Prediction Results</h2>", unsafe_allow_html=True)

    colA, colB = st.columns(2)
    colA.metric(label=f"{batting_team} Win %", value=f"{batting_perc}%")
    colB.metric(label=f"{bowling_team} Win %", value=f"{bowling_perc}%")

    # -------------------- IPL Style Win Probability Bar --------------------
    st.markdown("<div class='prob-title'>WIN PROBABILITY</div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="display:flex; justify-content:space-between; font-size:16px; font-weight:700; color:white; text-shadow:1px 1px 2px black;">
            <span>{batting_team} <span style="color:#00ff99;">{batting_perc}%</span></span>
            <span>{bowling_team} <span style="color:#ff4d4d;">{bowling_perc}%</span></span>
        </div>

        <div style="display:flex; width:100%; height:16px; border-radius:10px; overflow:hidden; margin-top:8px; background:#e0e0e0;">
            <div style="background:#00c853; width:{batting_perc}%;"></div>
            <div style="background:#d50000; width:{bowling_perc}%;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Extra match summary
    st.markdown(
        f"""
        <div style="
            background-color: rgba(0, 0, 0, 0.65);
            padding: 1rem 1.2rem;
            border-radius: 12px;
            margin-top: 12px;
            color: white;
            font-weight: 600;
            font-size: 16px;
            text-shadow: 1px 1px 2px black;
            line-height: 1.6;
        ">
            <b>Match Situation:</b><br>
            Target: {target}<br>
            Score: {score}/{wickets_out}<br>
            Overs: {overs} | Balls Left: {balls_left}<br>
            Runs Left: {runs_left} | Wickets Left: {wickets_left}<br>
            CRR: {round(crr,2)} | RRR: {round(rrr,2)}
        </div>
        """,
        unsafe_allow_html=True
    )
