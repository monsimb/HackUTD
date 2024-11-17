import pandas as pd
import numpy as np
from ai_connection import chat_conn as cc  # Import the chat module
from ai_connection import nlp_intent_detection as id    # import intent detection module
import streamlit as st

st.title('Chrys')

model = id.intentDetection()

# First, check if user has a profile
cc.setup_profile()

# Initialize chat history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat functionality
prompt = st.chat_input("Type here...")

# Display chat messages from history on rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Ensure that there's a prompt
if prompt:

    # Predict intent using the trained model
    predicted_intent = cc.predict_intent(model, prompt)  # Use the predict_intent function from chat_conn

    if predicted_intent == "buy":
        # Chatbot asks user for details about buying a home
        cc.st_chat(prompt, "the information required to calculate house payments. Ask me if I want help calculating any of those factors")
    elif predicted_intent == "refinance":
        # Chatbot asks user for details about refinancing
        cc.st_chat(prompt, "the information required to refinance a home. Ask me if I want help calculating any of them")
