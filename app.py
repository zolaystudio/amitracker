import streamlit as st
from googleapiclient.discovery import build
from datetime import datetime

st.set_page_config(page_title="Arthur Murray Analytics", layout="wide")
st.title("🕺 Arthur Murray: The Global Dashboard")

my_key = st.sidebar.text_input("YouTube API Key:", type="password")

if my_key:
    try:
        youtube = build('youtube', 'v3', developerKey=my_key)
        
        # 1. ONE SEARCH to find videos from accounts named Arthur Murray
        # This is much "cheaper" on your quota than searching for channels first.
        search_request = youtube.search().list(
            q="Arthur Murray",
            part="snippet",
            type="video",
            maxResults=30,
            order="date" # Gets the newest videos globally
        ).execute()

        video_ids = [item['id']['videoId'] for item in search_request.get('items', [])]
        
        if video_ids:
            # 2. GET STATS (Views, Comments, Dates) in one batch
            v_details = youtube.videos().list(
                id=','.join(video_ids),
                part="snippet,statistics"
            ).execute()
            
            cols = st.columns(3)
            display_count = 0

            for video in v_details.get('items', []):
                channel_name = video['snippet']['channelTitle']
                
                # 3. FILTER: Only show if it starts with Arthur Murray
                if channel_name.lower().startswith("arthur murray"):
                    title = video['snippet']['title']
                    stats = video['statistics']
                    
                    # Clean the Date
                    raw_date = video['snippet']['publishedAt']
                    clean_date = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d, %Y")
                    
                    with cols[display_count % 3]:
                        st.markdown(f"### 📍 {channel_name}")
                        st.video(f"https://www.youtube.com/watch?v={video['id']}")
                        st.write(f"**{title}**")
                        st.caption(f"📅 Uploaded: {clean_date}")
                        
                        # Metrics
                        m1, m2 = st.columns(2)
                        m1.metric("Views", f"{int(stats.get('viewCount', 0)):,}")
                        m2.metric("Comments", f"{int(stats.get('commentCount', 0)):,}")
                        st.divider()
                        display_count += 1
            
            if display_count == 0:
                st.warning("Found videos mentioning 'Arthur Murray', but none were from channels starting with that name.")
        else:
            st.warning("YouTube didn't return any videos for this search.")

    except Exception as e:
        # This will tell us if your "Magic Key" is actually out of credits
        if "quotaExceeded" in str(e):
            st.error("🛑 You've hit your daily free limit! Wait until tomorrow or use a different API key.")
        else:
            st.error(f"Something went wrong: {e}")
else:
    st.info("👈 Enter your API key in the sidebar.")
