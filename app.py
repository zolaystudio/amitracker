import streamlit as st
from googleapiclient.discovery import build

# 1. Page Setup
st.set_page_config(page_title="Arthur Murray Exec Tracker", layout="wide")

# Custom CSS to make the Channel Name look like a "Title Card" over the video
st.markdown("""
    <style>
    .channel-card {
        background-color: #1e1e1e;
        color: #f1c40f; /* Gold color */
        padding: 10px;
        border-radius: 10px 10px 0 0;
        text-align: center;
        font-weight: bold;
        font-size: 20px;
        border: 2px solid #333;
    }
    .video-container {
        border: 2px solid #333;
        border-top: none;
        border-radius: 0 0 10px 10px;
        padding: 10px;
        background-color: #000;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🕺 Arthur Murray Executive Tracker")
my_key = st.sidebar.text_input("YouTube API Key:", type="password")

if my_key:
    youtube = build('youtube', 'v3', developerKey=my_key)
    
    # 2. Advanced Search (Looking for the latest 30 videos)
    search_response = youtube.search().list(
        q="Arthur Murray",
        part="snippet",
        type="video",
        maxResults=30,
        order="date" # Newest videos first
    ).execute()

    video_ids = [item['id']['videoId'] for item in search_response['items']]
    
    # 3. Get Stats (Views) and Full Snippets
    video_details = youtube.videos().list(
        id=','.join(video_ids),
        part="snippet,statistics"
    ).execute()

    # 4. The Grid Display
