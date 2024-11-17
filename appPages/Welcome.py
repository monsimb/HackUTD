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
        # Display retrieved information
        st.write(user_info)
        sleep(0.5)
        st.switch_page("appPages/Home.py")
        # st.session_state.messages.append({"role": "system", "content": f"User {username} found in database."})
    else:
        st.warning("Username not found. Let's create a new profile.")
        credit = st.number_input("Enter your credit score", min_value=0, max_value=850)
        had_bankrupcies = st.checkbox("Have you had bankrupcies?")
        is_working = st.checkbox("Are you currently working?")
        income = st.number_input("Enter your annual income", min_value=0)
        is_veteran = st.checkbox("Are you a veteran?")
        first_time_home_buyer = st.checkbox("Are you a first time home buyer?")
        property_type = st.selectbox("What type of property are you looking for?", ["residential", "commercial"])
        budget = st.number_input("Enter your budget", min_value=0)
        had_loans_before = st.checkbox("Have you had loans before?")
        home_value = st.number_input("Enter the estimated value of the home you are looking to buy", min_value=0)

        if st.button("Submit"):
            new_user_data = {
                "_id": username,
                "credit": credit,
                "had_bankrupcies": had_bankrupcies,
                "is_working": is_working,
                "income": income,
                "is_veteran": is_veteran,
                "first_time_home_buyer": first_time_home_buyer,
                "property_type": property_type,
                "budget": budget,
                "had_loans_before": had_loans_before,
                "home_value": home_value,
            }
            db.add_user_data(new_user_data)
            st.success("Profile created successfully!")
            sleep(0.5)
            st.switch_page("appPages/Home.py")
            # st.session_state.messages.append({"role": "system", "content": f"User {username} added to database."})
