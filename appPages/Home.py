import streamlit as st
# from ai_connection.db_connection from ai_connection.api_calls import mortgage_rate
import get_user_data, add_user_data
from ai_connection import chat_conn as cc  # Import the chat module
from ai_connection import nlp_intent_detection as id    # import intent detection module

st.title('Home')

model = id.intentDetection()

# Initialize chat history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Get the username from the user
st.subheader("Welcome! Please enter your username")
username = st.text_input("Username")

# Check if the username exists in the database
if username:
    user_info = get_user_data(username)
    if user_info:
        st.success(f"Welcome back, {username}!")
        st.write("Fetching your profile data...")
        # Display retrieved information
        st.write(user_info)
        st.session_state.messages.append({"role": "system", "content": f"User {username} found in database."})
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
            add_user_data(new_user_data)
            st.success("Profile created successfully!")
            st.session_state.messages.append({"role": "system", "content": f"User {username} added to database."})

# Chat functionality
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
        # mortgage_rates = mortgage_rate()
        # fmr15 = mortgage_rates[0]
        # fmr30 = mortgage_rates[1]
        # cc.st_chat(prompt, f"The current mortgage rates are:\n- 15-Year Fixed: {fmr15}%\n- 30-Year Fixed: {fmr30}%\n")
        cc.st_chat(prompt, "help me calculate the best refinancing options.")

    else:
        # Fallback response for undefined intents
        st.write("I'm not sure about that. Can you clarify?")