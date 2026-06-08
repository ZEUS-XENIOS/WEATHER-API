import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import requests
import plotly.express as px
from datetime import datetime
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="SkyCast AI | Premium Weather Intelligence",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- PREMIUM CSS INJECTION ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    /* Global Styles */
    .main {
        background-color: #0f172a;
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Glassmorph Card */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        padding: 25px;
        margin-bottom: 20px;
        transition: transform 0.3s ease, border 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(56, 189, 248, 0.5);
    }

    /* Metric Styles */
    .metric-label {
        color: #94a3b8;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .prediction-value {
        background: linear-gradient(135deg, #f472b6 0%, #fb923c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Search Bar Customization */
    .stTextInput input {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }

    /* Titles */
    h1, h2, h3 {
        font-weight: 800 !important;
        letter-spacing: -1px;
    }
    .hero-title {
        font-size: 3.5rem;
        margin-bottom: 0;
        background: linear-gradient(to right, #f8fafc, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)

# --- APP LOGIC ---

# 1. API Config (Use st.secrets on Cloud)
# Get your key from https://home.openweathermap.org/api_keys
API_KEY = st.secrets.get("OPENWEATHER_API_KEY", "PASTE_YOUR_KEY_HERE")

# Header
st.markdown('<h1 class="hero-title">SkyCast AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8; font-size:1.2rem;'>Advanced Weather Analytics & Machine Learning Predictions</p>", unsafe_allow_html=True)

# 2. Sidebar/Top Search
with st.container():
    col_search, _ = st.columns([1, 2])
    with col_search:
        city = st.text_input("📍 Enter City Name", value="Bangalore", placeholder="e.g. London, New York, Tokyo")

# 3. Data Fetching
@st.cache_data(ttl=600)  # Cache for 10 mins
def fetch_weather(city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    try:
        res = requests.get(url)
        return res.json()
    except:
        return None

data = fetch_weather(city)

# 4. History Management
file_name = "weather_history.csv"
if not os.path.exists(file_name):
    pd.DataFrame(columns=["timestamp", "city", "temp", "humidity", "condition"]).to_csv(file_name, index=False)

# 5. Process Current Data
if data and "main" in data:
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    condition = data["weather"][0]["main"]
    
    # Save to history
    new_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "city": city,
        "temp": temp,
        "humidity": humidity,
        "condition": condition
    }
    pd.DataFrame([new_entry]).to_csv(file_name, mode="a", header=False, index=False)
else:
    st.error("⚠️ City not found or API issue. Please check the spelling.")
    temp, humidity, condition = 0, 0, "N/A"

# 6. Load & Analyze History
df = pd.read_csv(file_name)
df["timestamp"] = pd.to_datetime(df["timestamp"])
city_df = df[df["city"].str.lower() == city.lower()].sort_values("timestamp")

# 7. AI ML Prediction
prediction = 0
if len(city_df) > 5:
    city_df["hour_index"] = range(len(city_df))
    X = city_df[["hour_index"]]
    y = city_df["temp"]
    model = LinearRegression()
    model.fit(X, y)
    prediction = model.predict([[len(city_df)]])[0]
else:
    # Fallback if not enough data
    prediction = temp + (np.random.uniform(-2, 2) if temp != 0 else 0)

# --- UI LAYOUT ---

# Metrics Row
m1, m2, m3, m4 = st.columns(4)

def glass_metric(col, label, value, is_prediction=False):
    css_class = "prediction-value" if is_prediction else "metric-value"
    col.markdown(f"""
        <div class="glass-card">
            <div class="metric-label">{label}</div>
            <div class=" {css_class}">{value}</div>
        </div>
    """, unsafe_allow_html=True)

glass_metric(m1, "Current Temperature", f"{temp:.1f}°C")
glass_metric(m2, "Relative Humidity", f"{humidity}%")
glass_metric(m3, "Sky Condition", condition)
glass_metric(m4, "AI Projected Temp", f"{prediction:.1f}°C", is_prediction=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Dashboard Content
c_left, c_right = st.columns([2, 1])

with c_left:
    st.markdown("### 📈 Temperature Trajectory")
    if len(city_df) > 1:
        fig = px.line(city_df, x="timestamp", y="temp", 
                      template="plotly_dark",
                      markers=True, line_shape="spline",
                      color_discrete_sequence=['#38bdf8'])
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis_title="",
            yaxis_title="Temp (°C)",
            margin=dict(l=0, r=0, t=20, b=0),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Gathering historical data for this city... More insights will appear as you check back!")

with c_right:
    st.markdown("### 📜 Activity Log")
    if not city_df.empty:
        st.dataframe(
            city_df[["timestamp", "temp", "condition"]].tail(8).sort_values("timestamp", ascending=False),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.write("No local records found.")

# Information Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; font-size: 0.9rem;'>
    Powered by Linear Regression ML • Data from OpenWeather • Built with Streamlit Premium
</div>
""", unsafe_allow_html=True)