import streamlit as st
import uuid

def init_session_state():
    """Initialize session state variables"""
    if "sessions" not in st.session_state:
        st.session_state.sessions = {}
    if "current_session" not in st.session_state:
        st.session_state.current_session = None

def get_current_session():
    """Get current session details"""
    current_session_id = next(
        (sid for sid, s in st.session_state.sessions.items() 
         if s["agent"] == st.session_state.current_session),
        None
    )
    return current_session_id, st.session_state.sessions.get(current_session_id) if current_session_id else (None, None)

def create_new_session(agent_name, agent_config, agent_instance):
    """Create a new agent session"""
    session_id = str(uuid.uuid4())
    st.session_state.sessions[session_id] = {
        "agent": agent_name,
        "agent_config": agent_config,
        "messages": [],
        "thread_id": str(uuid.uuid4()),
        "memory": agent_instance.get_memory()
    }
    st.session_state.current_session = agent_name
