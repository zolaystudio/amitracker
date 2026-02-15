import streamlit as st
from googleapiclient.discovery import build

st.set_page_config(page_title="Arthur Murray Global Network", layout="wide")
st.title("💃 Arthur Murray Global Network Tracker")

# Use Sidebar for the key
my_key = st.sidebar.text_input("YouTube API Key:", type="password")

if my_key:
    youtube = build('youtube', 'v3', developerKey=my_key)
    
    # STEP 1: Find all CHANNELS that match "Arthur Murray"
    channel_search = youtube.search().list(
        q="Arthur Murray",
        type="channel",
        part="snippet",
        maxResults=50 # Find as many studios as possible
    ).execute()

    # STEP 2: Filter for ONLY those starting with "Arthur Murray"
    studio_ids = []
    for item in channel_search.get('items', []):
        name = item['snippet']['title']
        if name.lower().startswith("arthur murray"):
            studio_ids.append({'id': item['id']['channelId'], 'name': name})

    # STEP 3: Grab the newest video from each studio
    if studio_ids:
        cols = st.columns(3)
        for index, studio in enumerate(studio_ids):
            video_request = youtube.search().list(
                channelId=studio['id'],
                part="snippet",
                order="date", # Newest first
                maxResults=1,
                type="video"
            ).execute()
            
            # STEP 4: Display with the big Studio Name header
            for vid in video_request.get('items', []):
                with cols[index % 3]:
                    st.markdown(f"### 📍 {studio['name']}") # Big Studio Name
                    st.video(f"https://www.youtube.com/watch?v={vid['id']['videoId']}")
                    st.caption(vid['snippet']['title'])
                    st.divider()
    else:
        st.warning("No channels found starting exactly with 'Arthur Murray'.")
else:
    st.info("👈 Please enter your API key in the sidebar.")
