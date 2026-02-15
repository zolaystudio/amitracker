import streamlit as st
from googleapiclient.discovery import build
from datetime import datetime

st.set_page_config(page_title="Arthur Murray Analytics", layout="wide")
st.title("💃 Arthur Murray: YouTube Dashboard")

my_key = st.sidebar.text_input("YouTube API Key:", type="password")

if my_key:
    youtube = build('youtube', 'v3', developerKey=my_key)
    
    # 1. FIND CHANNELS starting with "Arthur Murray"
    channel_search = youtube.search().list(
        q="Arthur Murray",
        type="channel",
        part="snippet",
        maxResults=15 # Focus on top 15 studios
    ).execute()

    studio_ids = []
    for item in channel_search.get('items', []):
        name = item['snippet']['title']
        if name.lower().startswith("arthur murray"):
            studio_ids.append({'id': item['id']['channelId'], 'name': name})

    # 2. FETCH LATEST VIDEO DATA
    if studio_ids:
        cols = st.columns(3)
        for index, studio in enumerate(studio_ids):
            # Get the single newest video ID for this studio
            v_request = youtube.search().list(
                channelId=studio['id'],
                part="snippet",
                order="date",
                maxResults=1,
                type="video"
            ).execute()
            
            for vid in v_request.get('items', []):
                v_id = vid['id']['videoId']
                
                # 3. ASK FOR STATS (Views, Comments, Date)
                v_details = youtube.videos().list(
                    id=v_id,
                    part="snippet,statistics"
                ).execute()
                
                for detail in v_details.get('items', []):
                    stats = detail['statistics']
                    # Format Date
                    raw_date = detail['snippet']['publishedAt']
                    clean_date = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d, %Y")
                    
                    with cols[index % 3]:
                        st.markdown(f"### 📍 {studio['name']}")
