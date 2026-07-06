import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Zener Shunt Stabilizer Lab",
    page_icon="⚡",
    layout="wide"
)

# --- STRICT BLACK-ON-BROWN LAB THEME (CSS) ---
st.markdown("""
    <style>
        /* Base application background (Warm Laboratory Brown) */
        .stApp {
            background-color: #d4a373;
            color: #000000;
        }
        /* Main background content container card (Slightly Lighter Warm Brown for visibility) */
        .main .block-container {
            background-color: #e9c46a;
            padding: 3rem;
            border-radius: 10px;
            margin-top: 2rem;
            border: 2px solid #000000;
        }
        /* Sidebar layout styling */
        section[data-testid="stSidebar"] {
            background-color: #c69363 !important;
            border-right: 2px solid #000000;
        }
        /* Enforce absolute black on text, labels, headers, and descriptions */
        h1, h2, h3, h4, p, span, label, .stMarkdown, section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] h3 {
            color: #000000 !important;
            font-weight: 500;
        }
        /* Form containers, alerts, and input blocks */
        div[data-testid="stForm"], .stAlert, div[data-testid="stWidgetLabel"] {
            background-color: #f4a261 !important;
            border: 2px solid #000000 !important;
            color: #000000 !important;
        }
        /* Interactive Buttons */
        div.stButton > button {
            background-color: #000000 !important;
            color: #e9c46a !important;
            border: 2px solid #000000 !important;
            font-weight: bold;
        }
        div.stButton > button:hover {
            background-color: #e9c46a !important;
            color: #000000 !important;
            border-color: #000000 !important;
        }
        /* Tab navigation formatting */
        button[data-baseweb="tab"] {
            color: #4a3525 !important;
            font-weight: bold !important;
        }
        button[aria-selected="true"] {
            color: #000000 !important;
            border-bottom-color: #000000 !important;
        }
        hr {
            border-color: #000000 !important;
        }
        /* Structural Dataframe tables forced visibility styling */
        div[data-testid="stDataFrame"] {
            background-color: #f4a261 !important;
            border: 1px solid #000000;
        }
    </style>
""", unsafe_allow_html=True)

# --- LEARNING ANALYTICS LOGGER ---
LOG_FILE = "student_analytics_log.csv"

def log_user_action(student_id, action_type, details):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_data = pd.DataFrame([{
        "Timestamp": timestamp,
        "Student_ID": student_id,
        "Action_Type": action_type,
        "Details": str(details)
    }])
    if not os.path.isfile(LOG_FILE):
        log_data.to_csv(LOG_FILE, index=False)
    else:
        log_data.to_csv(LOG_FILE, mode='a', header=False, index=False)

# --- SESSION STATE INITIALIZATION ---
if 'student_id' not in st.session_state:
    st.session_state['student_id'] = "Guest_Student"
if 'authenticated
