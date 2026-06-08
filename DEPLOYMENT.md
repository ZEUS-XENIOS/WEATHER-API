# 🚀 How to Launch Your Website (Shareable Link)

To get a link like `https://skycast-ai.streamlit.app` that you can share with anyone, follow these 3 simple steps:

### 1. Upload to GitHub
Streamlit Cloud links directly to a GitHub repository.
1. Go to [github.com](https://github.com) and create a new public repository (e.g., `weather-ai-site`).
2. Upload all the files in this folder to that repository.
3. **Important**: Make sure `requirements.txt` and `weather_dashboard.py` are in the main folder.

### 2. Connect to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io).
2. Sign in with your GitHub account.
3. Click **"New app"**.
4. Select your repository, branch (`main`), and main file path (`weather_dashboard.py`).
5. Click **"Deploy"**.

3. ### Add Your API Key (Secret)
Since we want to keep your OpenWeather API key safe:
1. In the Streamlit Cloud dashboard, go to your app's **Settings**.
2. Go to the **Secrets** tab.
3. Paste the following (replace the text in quotes with your ACTUAL key):
   ```toml
   OPENWEATHER_API_KEY = "PASTE_YOUR_KEY_HERE"
   ```
4. Save and your app will be live with a shareable URL!

---

### Tips for Success
- **Link Title**: You can change the URL in the Streamlit Cloud settings to make it shorter (e.g., `kapil-weather.streamlit.app`).
- **Mobile Check**: Open the link on your phone; it will look like a premium mobile app.
