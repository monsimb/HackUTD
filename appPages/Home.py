import pandas as pd
import numpy as np
from ai_connection import chat_conn as cc  # Import the chat module
import streamlit as st

st.title('Home')

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
    predicted_intent = cc.predict_intent(prompt)  # Use the predict_intent function from chat_conn

    if predicted_intent == "buy":
        st.write("It looks like you're asking about buying a home. Let's talk about Home Purchase.")
        loan_amount = st.number_input("Enter loan amount:", min_value=0.0, value=200000.0)
        interest_rate = st.number_input("Enter interest rate (%):", min_value=0.0, value=3.5)
        loan_term = st.number_input("Enter loan term (years):", min_value=1, value=30)
        
        if loan_amount and interest_rate and loan_term:
            monthly_payment = cc.calculate_home_loan.invoke(input={"loan_amount": loan_amount, "interest_rate": interest_rate, "loan_term": loan_term})
            st.write(f"Your estimated monthly payment is: ${monthly_payment:.2f}")

    elif predicted_intent == "refinance":
        st.write("It looks like you're asking about refinancing. Let's talk about Refinancing.")
        current_loan_balance = st.number_input("Enter current loan balance:", min_value=0.0, value=150000.0)
        current_interest_rate = st.number_input("Enter current interest rate (%):", min_value=0.0, value=4.0)
        new_interest_rate = st.number_input("Enter new interest rate (%):", min_value=0.0, value=3.0)
        
        if current_loan_balance and current_interest_rate and new_interest_rate:
            monthly_savings = cc.refinancing_calculator(current_loan_balance, current_interest_rate, new_interest_rate)
            st.write(f"Your estimated monthly savings from refinancing would be: ${monthly_savings:.2f}")
    
    # Handle the conversation flow by calling st_chat
    cc.st_chat(prompt)  # This should work now without issues
