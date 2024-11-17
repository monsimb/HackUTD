import pandas as pd
import numpy as np
from ai_connection import chat_conn as cc
import streamlit as st

st.title('Home')

# init chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Type here...")

cc.st_chat(prompt)