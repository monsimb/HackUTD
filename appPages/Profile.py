import streamlit as st
import pandas as pd
import numpy as np

st.title('Profile')
# temp user data. pull from db here
current_username = "JohnDoe123"
current_pwd = "password123"

# Display current username
st.subheader("Current Username")
st.write(f"Username: **{current_username}**")

# change username
st.subheader("Change Username")
new_username = st.text_input("Enter new username")

if st.button("Update Username"):
    if new_username.strip() == "":
        st.error("Username cannot be empty.")
    elif new_username == current_username:
        st.warning("New username cannot be the same as the current username.")
    else:
        # save new username to db
        st.success(f"Username successfully updated to **{new_username}**!")

# change password
st.subheader("Change Password")
new_password = st.text_input("Enter new password", type="password")
confirm_password = st.text_input("Confirm new password", type="password")

if st.button("Update Password"):
    if new_password.strip() == "":
        st.error("Password cannot be empty.")
    elif new_password == current_pwd:
        st.warning("New password cannot be the same as the current password.")
    elif new_password != confirm_password:
        st.error("Passwords do not match.")
    else:
        # update the password in the database
        st.success("Password successfully updated!")