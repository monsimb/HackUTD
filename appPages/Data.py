import streamlit as st

st.title("Data Maintenance")

if st.button("Clear Logs"):
    # Logic for clearing logs go here
    st.success("Logs cleared successfully!")

if st.button("Clear Cache"):
    # Logic for clearing cache go here
    st.success("Cache cleared successfully!")

if st.button("Delete Account"):
    # Confirmation for account deletion
    delete_confirmation = st.radio(
        "Are you sure you want to delete your account? This action cannot be undone.",
        ("No", "Yes"),
        index=0,
    )
    if delete_confirmation == "Yes":
        # Logic for deleting account go here
        st.error("Your account has been deleted.")
    elif delete_confirmation == "No":
        st.info("Account deletion canceled.")

# warning
st.write("---")
st.caption("Deleted data may not be recoverable.")