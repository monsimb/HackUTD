import streamlit as st

pages = {
    "": [
        st.Page("appPages/Home.py", title="Home"),
    ],
    "Log Files":[],
    "Profile & Settings": [
        st.Page("appPages/Profile.py", title="Profile"),
        st.Page("appPages/Graph.py", title="Graph"),
        st.Page("appPages/Data.py", title="Data")
    ]
}

pg = st.navigation(pages)

# Logout button
with st.sidebar:
    if st.button("Logout", key="logout"):
        # add logout logic
        st.sidebar.success("You have been logged out!")
        
pg.run()