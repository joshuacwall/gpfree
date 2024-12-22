def get_login_styles():
    return """
    <style>
        /* Center content */
        .block-container {
            max-width: 100%;
            padding-top: 2rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        /* Form container */
        div[data-testid="stForm"] {
            background-color: #262730;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Form inputs */
        div[data-testid="stForm"] input {
            background-color: #1E1E1E;
            border: 1px solid #363636;
            border-radius: 5px;
            padding: 0.5rem;
            margin-bottom: 1rem;
            width: 100%;
        }
        
        /* Submit button */
        div[data-testid="stForm"] button {
            width: 100%;
            background-color: #262730;
            color: #FAFAFA;
            border: 1px solid #363636;
            padding: 0.5rem;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        div[data-testid="stForm"] button:hover {
            border-color: #ff4b4b;
            background-color: #363840;
        }

        /* Media query for smaller screens */
        @media (max-width: 600px) {
            .block-container {
                padding-top: 1rem;
                padding-left: 0.5rem;
                padding-right: 0.5rem;
            }
            
            div[data-testid="stForm"] {
                padding: 1rem;
            }
        }
    </style>
    """ 