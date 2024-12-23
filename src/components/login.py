import streamlit as st
from auth.auth import login

def render_login_page():
    """Render a clean, simple login page"""
    # Hide streamlit default elements
    hide_streamlit_elements = """
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_elements, unsafe_allow_html=True)
    
    # Center login form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            """
            <div style='text-align: center; margin-bottom: 40px; margin-top: 40px;'>
                <h1 style='color: #FAFAFA;'>🤖 GPFree</h1>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Login form with custom styling
        with st.form("login_form", clear_on_submit=True):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            # Add disclaimer and checkbox
            st.markdown("""
                <div style='margin: 20px 0; padding: 15px; background-color: #1E1E1E; border-radius: 5px;'>
                    <p style='font-size: 0.9em; color: #FAFAFA;'>
                        <strong>⚠️ Disclaimer:</strong> Messages are logged for maintenance purposes. 
                        Additionally, LLM service providers may separately log and store conversations. 
                        By checking the box below, you acknowledge and accept these data handling practices.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            accept_terms = st.checkbox("I understand and accept the data handling practices")
            
            submit = st.form_submit_button("Login")
            if submit:
                if not accept_terms:
                    st.error("Please accept the data handling practices to continue")
                elif login(username, password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        # Add custom CSS
        st.markdown(
            """
            <style>
                /* Form styling */
                [data-testid="stForm"] {
                    background-color: #262730;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }
                
                /* Input fields */
                .stTextInput input {
                    background-color: #1E1E1E;
                    border: 1px solid #363636;
                    color: #FAFAFA;
                }
                
                /* Submit button */
                .stButton button {
                    width: 100%;
                    background-color: #262730;
                    color: #FAFAFA;
                    border: 1px solid #363636;
                    padding: 10px;
                    margin-top: 20px;
                }
                
                .stButton button:hover {
                    border-color: #ff4b4b;
                    background-color: #363840;
                }
                
                /* Success/Error messages */
                .stAlert {
                    margin-top: 20px;
                }
                
                /* Checkbox styling */
                .stCheckbox {
                    margin: 15px 0;
                }
                
                .stCheckbox label {
                    color: #FAFAFA !important;
                }
            </style>
            """,
            unsafe_allow_html=True
        )