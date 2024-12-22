from dataclasses import dataclass
from typing import Dict, List
import streamlit as st
from config.agent_config import AgentConfig

@dataclass
class UserAgent(AgentConfig):
    pass

def save_user_agent(agent: UserAgent):
    if "user_agents" not in st.session_state:
        st.session_state.user_agents = {}
    st.session_state.user_agents[agent.name] = agent

def get_user_agents() -> Dict[str, UserAgent]:
    if "user_agents" not in st.session_state:
        st.session_state.user_agents = {}
    return st.session_state.user_agents 