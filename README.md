 AI Weather Dashboard & Predictor
A personal project where I built a real-time weather tracker and simple AI temperature predictor using Python, Streamlit, and Machine Learning. 
It fetches live weather data from OpenWeatherMap, saves historical trends, displays everything on a clean dark-mode dashboard, and uses a scikit-learn Linear Regression model to forecast what tomorrow's temperature might look like.

 What it does
- Live Weather Updates: Pulls live temperature, humidity, and condition for any city (currently set to Bangalore).
- Temperature Prediction: Uses linear regression on past readings to predict the next temperature trend.
- Interactive UI: Built with Streamlit and Plotly for smooth, responsive charts.
- Flask API Route: Also includes a standalone Flask backend with a /predict endpoint if you want to query predictions via JSON.
- History Tracking: Automatically logs fetches into weather_history.csv so the model gets better with more data.
---
 Files in this Repo
- weather_dashboard.py — The main Streamlit web dashboard.
- weather_api.py — Flask API endpoint for model predictions.
- fetch_weather.py — Quick script to grab live data and append it to CSV.
- weather_analysis.py — Simple script to plot historical data using Matplotlib.
- weatherprediction_.py — Command-line ML script for quick testing.
- generate_dataset.py — Script to generate sample weather data if you're starting fresh.
- requirements.txt — All Python packages needed to run the project.
---
   Built With
- Python 3.10+
- Streamlit & Plotly (Dashboard & Charts)
- Flask (REST API)
- Scikit-Learn, Pandas, NumPy (Data & ML)
- OpenWeatherMap API (Live Weather Data)
---
# How to Run It Locally
1. Clone & Set Up
git clone https://github.com/ZEUS-XENIOS/Weather-API-AI.git
cd Weather-API-AI
 2. Create a virtual environment (recommended)
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate
3. Install packages
pip install -r requirements.txt
 4. Add your API Key
Grab a free API key from https://openweathermap.org/ and replace the API_KEY in weather_dashboard.py:
API_KEY = "your_api_key_here"
CITY = "Bangalore"  # or your preferred city
 5. Launch the Dashboard
streamlit run weather_dashboard.py
Open your browser at http://localhost:8501 and you're good to go!
