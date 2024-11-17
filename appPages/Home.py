import pandas as pd
from ai_connection.api_calls import mortgage_rate
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
        mortgage_rates = mortgage_rate()
        fmr15 = mortgage_rates[0]
        fmr30 = mortgage_rates[1]
        # cc.st_chat(prompt, f"The current mortgage rates are:\n- 15-Year Fixed: {fmr15}%\n- 30-Year Fixed: {fmr30}%\n")
        cc.st_chat(prompt, "help me calculate the best refinancing options.")

    else:
        # Fallback response for undefined intents
        st.write("I'm not sure about that. Can you clarify?")