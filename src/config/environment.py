import os
from dotenv import load_dotenv
import streamlit as st

def get_env_variable(key: str) -> str:
    """Get environment variable from either secrets or .env"""
    # Try getting from Streamlit secrets first
    try:
        value = st.secrets[key]
        if value:
            return value
    except (KeyError, FileNotFoundError):
        pass
    
    # Fall back to environment variable
    value = os.getenv(key)
    if value:
        return value
    
    # Debug output
    st.write(f"Failed to get {key} from both secrets and env vars")
    st.write(f"Available secrets: {list(st.secrets.keys()) if hasattr(st, 'secrets') else 'No secrets'}")
    st.write(f"Available env vars: {[k for k in os.environ.keys() if k in required_vars]}")
    
    return None

def check_environment():
    """Check and validate environment variables"""
    # Load .env file for local development
    load_dotenv()
    
    required_vars = [
        "LANGCHAIN_API_KEY",
        "LANGCHAIN_TRACING_V2",
        "TAVILY_API_KEY",
        "QDRANT_URL",
        "QDRANT_API_KEY",
        "HUGGINGFACE_API_KEY"
    ]
    
    missing_vars = [var for var in required_vars if not get_env_variable(var)]
    
    if missing_vars:
        st.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        st.error("Please check your .env file or Streamlit secrets")
        st.stop()
