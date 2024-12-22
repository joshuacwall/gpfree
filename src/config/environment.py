import os
from dotenv import load_dotenv
import streamlit as st

def check_environment():
    """Check and validate environment variables"""
    load_dotenv()
    
    required_vars = ["LANGCHAIN_API_KEY", "LANGCHAIN_TRACING_V2"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        st.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        st.error("Please check your .env file")
        st.stop()
