import pandas as pd
import numpy as np
from ai_connection import chat_conn as cc  # Import the chat module
from ai_connection import nlp_intent_detection as id    # import intent detection module
import streamlit as st
from ai_connection import db_connection as db
from time import sleep

st.title('Welcome to Chrys!')

# Get the username from the user
st.subheader("Please enter your username")
username = st.text_input("Username")

# Check if the username exists in the database
if username:
    user_info = db.get_user_data(username)
    if user_info:
        st.success(f"Welcome back, {username}!")
        st.write("Fetching your profile data...")

        # Set session state to True
        st.session_state["has_profile"] = True
        st.session_state["username"] = username

        # Display retrieved information
        st.write(user_info)
        sleep(1.5)    
    else:
        sleep(3)
        st.warning("Username not found. Let's create a new profile.")
        st.session_state["has_profile"] = False
        st.session_state["username"] = username
    st.switch_page("appPages/Home.py")
            # st.session_state.messages.append({"role": "system", "content": f"User {username} added to database."})
