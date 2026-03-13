import streamlit as st
import pandas as pd
from decimal import Decimal, InvalidOperation

# Configure Streamlit page settings
st.set_page_config(
    page_title="Shopping Expense Splitter",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize temporary members in session state
if "temp_members" not in st.session_state:
    st.session_state.temp_members = []

# Get the appropriate names based on the state
def get_names():
    base_names = ["MS", "AD", "RS"]
    return base_names + st.session_state.temp_members

# Custom CSS for better alignment and to hide default menu items
st.markdown("""
    <style>
    .stTextInput > label { display: none; }
    .stCheckbox { margin-top: 0px !important; }
    .stCheckbox > label { font-size: 0.9rem; }
    div[data-testid="column"] { gap: 0rem; }
    /* Reduce spacing between rows */
    .row-widget { margin-bottom: -1rem; }

    /* Reduce main container padding for wider layout */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }

    /* Ensure columns have proper spacing */
    .stColumns > div {
        padding: 0 0.5rem;
    }

    /* Hide all default menu items */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}

    /* Retro-style GitHub button */
    .custom-github-btn {
        position: fixed;
        right: 1rem;
        top: 1rem;
        padding: 0.7rem 1.2rem;
        background: #ffd700;
        color: #000000;
        border-radius: 0;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 0.7rem;
        font-size: 0.8rem;
        font-family: 'Press Start 2P', monospace;
        text-transform: uppercase;
        border: 3px solid #000000;
        box-shadow: 4px 4px 0px #000000;
        transition: all 0.1s ease;
        z-index: 1000;
    }

    .custom-github-btn:hover {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px #000000;
        background: #ffed4a;
    }

    .custom-github-btn:active {
        transform: translate(4px, 4px);
        box-shadow: 0px 0px 0px #000000;
    }

    .github-logo {
        width: 20px;
        height: 20px;
        display: inline-block;
    }

    /* Align checkboxes horizontally for mobile view */
    @media (max-width: 768px) {
        .stCheckbox {
            display: flex;
            flex-direction: row;
            align-items: center;
        }
    }

    </style>

    <!-- Import Google Font -->
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">

    <!-- Custom GitHub button -->
    <a href="https://www.linkedin.com/posts/saifeemustafa_shopping-expense-splitter-activity-7284066826970435584-A-Kj" 
       target="_blank" 
       class="custom-github-btn">
        Fork this app
        <svg class="github-logo" viewBox="0 0 24 24" fill="#000000">
            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
        </svg>
    </a>
"""
