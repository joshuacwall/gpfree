import streamlit as st
from auth.auth import init_auth
from config.environment import check_environment
from utils.session import init_session_state
from components.login import render_login_page
from components.sidebar import render_sidebar
from components.chat import render_chat_interface

# Set page config
st.set_page_config(
    page_title="GPFree",
    page_icon="🤖",
    layout="wide"
)

# Initialize authentication
init_auth()

# Check environment variables
check_environment()

# Initialize session state
init_session_state()

# Main app flow
if not st.session_state.authenticated:
    render_login_page()
    st.stop()

# Main app (only shown to authenticated users)
render_sidebar()
render_chat_interface()

# Add styling
st.markdown("""
<style>
    .stButton button {
        width: 100%;
        text-align: left;
        background-color: #262730;
        color: #FAFAFA;
    }
    .stButton button:hover {
        border-color: #ff4b4b;
        background-color: #363840;
    }
</style>
""", unsafe_allow_html=True)
