import streamlit as st

def login_page():
    st.title("🔐 Login")
    
    # Hardcoded credentials
    USER = "admin"
    PASS = "biomed2024"
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if username == USER and password == PASS:
                st.session_state.logged_in = True
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid username or password")

def logout():
    st.session_state.logged_in = False
    st.rerun()
