import streamlit as st
import pandas as pd
from datetime import date
import json
import os
#import matplotlib.pyplot as plt

def load_user_data(username):
    filename = f"{username}.json"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return []

def save_user_data(username, data):
    filename = f"{username}.json"
    with open(filename, "w") as file:
        json.dump(data, file)

st.title("Mental Health Tracker")
st.sidebar.header("Login")
username = st.sidebar.text_input("Enter your username:")

if username:
    if 'user_data' not in st.session_state:
        st.session_state['user_data'] = {}

    if username not in st.session_state['user_data']:
        st.session_state['user_data'][username] = load_user_data(username)

    today = date.today()
    st.write(f"Hello, {username}! Today's Date: {today}")

    st.subheader("Daily Mood Tracker")
    mood_options = ["😊 Happy", "😟 Anxious", "😞 Sad", "😠 Angry", "😌 Calm"]
    mood = st.selectbox("How are you feeling today?", mood_options)
    st.subheader("Daily Journal")
    journal_entry = st.text_area("Write down your thoughts or anything on your mind", "")

    if st.button("Save Entry"):
        new_entry = {
            "date": str(today),
            "mood": mood,
            "entry": journal_entry}
        
        st.session_state['user_data'][username].append(new_entry)
        save_user_data(username, st.session_state['user_data'][username])
        st.success("Entry saved successfully!")

    st.subheader("Mood Trend Analysis")
    user_entries = st.session_state['user_data'][username]
    
    if user_entries:
        df = pd.DataFrame(user_entries)
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

    if user_entries:
        last_mood = user_entries[-1]['mood']
        exercise, video_url = get_exercise(last_mood)
        st.write(f"Suggested Exercise for '{last_mood}': {exercise}")
        st.video(video_url)
    else:
        st.write("Track your mood to receive personalized exercises.")

else:
    st.write("Please enter a username to begin tracking.")
