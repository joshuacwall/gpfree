import streamlit as st
from typing import Dict, Optional

# Simulated user database (in memory)
USERS = {
    "theo": "comeonson",
    "jon": "hesignseverycan",
    "josh": "josh",
    "scott": "grandman",
    "meg": "canigetthisdog",
    "aimee": "ipromisehegrowsonyou",
    "cami": "*eyerollatjon*",
    "chloe": "iliketurtles"
}

def init_auth():
    """Initialize authentication states"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}

def login(username: str, password: str) -> bool:
    """Simple login function"""
    if username in USERS and USERS[username] == password:
        st.session_state.authenticated = True
        st.session_state.username = username
        # Initialize user data if first login
        if username not in st.session_state.user_data:
            st.session_state.user_data[username] = {
                "sessions": {},
                "current_session": None,
                "user_agents": {}
            }
        return True
    return False

def logout():
    """Logout function"""
    st.session_state.authenticated = False
    st.session_state.username = None

def get_current_user() -> Optional[str]:
    """Get current authenticated user"""
    return st.session_state.username if st.session_state.authenticated else None

def get_user_data() -> Dict:
    """Get current user's data"""
    username = get_current_user()
    if username:
        return st.session_state.user_data[username]
    return {} 