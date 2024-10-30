import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date
import json
import os

# Helper function to load user data from a JSON file
def load_user_data(username):
    filename = f"{username}.json"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return []

# Helper function to save user data to a JSON file
def save_user_data(username, data):
    filename = f"{username}.json"
    with open(filename, "w") as file:
        json.dump(data, file)

# Application title
st.title("Mental Health Tracker")

# Username Input
st.sidebar.header("Login")
username = st.sidebar.text_input("Enter your username:")

if username:
    # Load user data from JSON file on startup
    if 'user_data' not in st.session_state:
        st.session_state['user_data'] = {}

    if username not in st.session_state['user_data']:
        st.session_state['user_data'][username] = load_user_data(username)

    today = date.today()
    st.write(f"Hello, {username}! Today's Date: {today}")

    # Daily Mood Tracker
    st.subheader("Daily Mood Tracker")
    mood_options = ["😊 Happy", "😟 Anxious", "😞 Sad", "😠 Angry", "😌 Calm"]
    mood = st.selectbox("How are you feeling today?", mood_options)

    # Daily Journal Entry
    st.subheader("Daily Journal")
    journal_entry = st.text_area("Write down your thoughts or anything on your mind", "")
    
    # Save Entry Button
    if st.button("Save Entry"):
        new_entry = {
            "date": str(today),
            "mood": mood,
            "entry": journal_entry
        }
        
        # Update session state and save data to JSON file
        st.session_state['user_data'][username].append(new_entry)
        save_user_data(username, st.session_state['user_data'][username])
        st.success("Entry saved successfully!")

    # Mood Trend Analysis with Seaborn
    st.subheader("Mood Trend Analysis")
    user_entries = st.session_state['user_data'][username]
    
    if user_entries:
        df = pd.DataFrame(user_entries)
        
        # Set up the Seaborn plot
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(10, 6))
        ax = sns.countplot(data=df, x="mood", palette="viridis", order=df["mood"].value_counts().index)
        ax.set_title("Mood Distribution")
        ax.set_xlabel("Mood")
        ax.set_ylabel("Frequency")
        
        # Display the plot in Streamlit
        st.pyplot(plt)
    else:
        st.write("No data to display. Start tracking your mood to see insights.")

    # Mindfulness and Cognitive Exercises
    st.subheader("Mindfulness and Cognitive Exercises")
    def get_exercise(mood):
        exercises = {
            "😊 Happy": ["Keep a gratitude journal", "https://www.youtube.com/watch?v=ZToicYcHIOU"],
            "😟 Anxious": ["Deep breathing exercises", "https://www.youtube.com/watch?v=aNXKjGFUlMs"],
            "😞 Sad": ["Take a walk in nature", "https://www.youtube.com/watch?v=inpok4MKVLM"],
            "😠 Angry": ["Try progressive muscle relaxation", "https://www.youtube.com/watch?v=ihO02wUzgkc"],
            "😌 Calm": ["Continue with a mindfulness meditation", "https://www.youtube.com/watch?v=6p_yaNFSYao"]
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
