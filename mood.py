import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import random

st.title("Mental Health Tracker")
today = date.today()
st.write(f"Date: {today}")

st.subheader("Daily Mood Tracker")
mood_options = ["😊 Happy", "😟 Anxious", "😞 Sad", "😠 Angry", "😌 Calm"]
mood = st.selectbox("How are you feeling today?", mood_options)

st.subheader("Daily Journal")
journal_entry = st.text_area("Write down your thoughts or anything on your mind", "")
if st.button("Save Entry"):
    if 'data' not in st.session_state:
        st.session_state['data'] = []
    st.session_state['data'].append({"date": today, "mood": mood, "entry": journal_entry})
    st.success("Entry saved successfully!")

st.subheader("Mood Trend Analysis")
if 'data' in st.session_state and st.session_state['data']:
    df = pd.DataFrame(st.session_state['data'])
    mood_counts = df['mood'].value_counts()
    fig, ax = plt.subplots()
    mood_counts.plot(kind='bar', ax=ax, color=['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#FFD700'])
    ax.set_title("Mood Distribution")
    ax.set_xlabel("Mood")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)
else:
    st.write("No data to display. Start tracking your mood to see insights.")

st.subheader("Mindfulness and Cognitive Exercises")
def get_exercise(mood):
    exercises = {
        "😊 Happy": ["Keep a gratitude journal", "https://www.youtube.com/watch?v=ZToicYcHIOU"],
        "😟 Anxious": ["Deep breathing exercises", "https://www.youtube.com/watch?v=5zhnLG3GW-8"],
        "😞 Sad": ["Take a walk in nature", "https://www.youtube.com/watch?v=nZ4gK_AbCoY"],
        "😠 Angry": ["Try progressive muscle relaxation", "https://www.youtube.com/watch?v=bPu87cLEHac"],
        "😌 Calm": ["Continue with a mindfulness meditation", "https://www.youtube.com/watch?v=syx3a1_LeFo"]
    }
    return exercises.get(mood, ["Take a few deep breaths and relax", "https://www.youtube.com/watch?v=inpok4MKVLM"])

if 'data' in st.session_state and st.session_state['data']:
    last_mood = st.session_state['data'][-1]['mood']
    exercise, video_url = get_exercise(last_mood)
    st.write(f"Suggested Exercise for '{last_mood}': {exercise}")
    st.video(video_url)
else:
    st.write("Track your mood to receive personalized exercises.")