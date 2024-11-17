import pandas as pd
import numpy as np
from ai_connection import chat_conn as cc  # Import the chat module
from ai_connection import nlp_intent_detection as id    # import intent detection module
import streamlit as st

st.title('Home')

model = id.intentDetection()

# Initialize chat history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
prompt = st.chat_input("Type here...")

# Ensure that there's a prompt
if prompt:
    # Predict intent using the trained model
    predicted_intent = cc.predict_intent(model, prompt)  # Use the predict_intent function from chat_conn

    # cc.st_chat(prompt)  # This should work now without issues

    st.write(prompt)

    if predicted_intent == "buy":
            # Chatbot asks user for details about buying a home
            cc.st_chat(prompt, "the information required to calculate house payments. Ask me if I want help calculating any of them")
    elif predicted_intent == "refinance":
        # Chatbot asks user for details about refinancing
            st.write("It looks like you're asking about refinancing. Let's talk about Refinancing.")
            st.session_state.messages.append({"role": "assistant", "content": "What is your current loan balance?"})
            cc.st_chat("What is your current loan balance?")
    
    # Handle the conversation flow by calling st_chat
