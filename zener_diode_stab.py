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

# --- MODERN HIGH-CONTRAST LAB THEME (CSS) ---
st.markdown("""
    <style>
        /* Base application background (Warm Light Cream) */
        .stApp {
            background-color: #FDFBF7;
            color: #2B2625;
        }
        /* Main background content container card (Clean Canvas Soft Gray-Beige) */
        .main .block-container {
            background-color: #F4F0E6;
            padding: 3rem;
            border-radius: 12px;
            margin-top: 2rem;
            border: 1px solid #D1C7BD;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        }
        /* Sidebar layout styling (Professional Charcoal) */
        section[data-testid="stSidebar"] {
            background-color: #2B2625 !important;
            border-right: 1px solid #1E1A19;
        }
        /* Sidebar texts forced to crisp white/light gray for readability */
        section[data-testid="stSidebar"] .stMarkdown, 
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3, 
        section[data-testid="stSidebar"] label {
            color: #F4F0E6 !important;
        }
        /* Enforce elegant dark charcoal on main headings and texts */
        h1, h2, h3, h4, p, span, label, li, .stMarkdown {
            color: #2B2625 !important;
            font-weight: 500;
        }
        /* Input blocks, Forms and Alerts stylized clearly */
        div[data-testid="stForm"], .stAlert, div[data-testid="stNumberInput"] {
            background-color: #FFFFFF !important;
            border: 1px solid #C4B9AF !important;
            border-radius: 8px;
        }
        /* Interactive Primary Accent Buttons */
        div.stButton > button {
            background-color: #D96B43 !important;
            color: #FFFFFF !important;
            border: none !important;
            font-weight: bold !important;
            border-radius: 6px !important;
            padding: 0.5rem 1.5rem !important;
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: #B8532D !important;
            color: #FFFFFF !important;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
        }
        /* Clean Tab Navigation */
        button[data-baseweb="tab"] {
            color: #8C8075 !important;
            font-weight: bold !important;
        }
        button[aria-selected="true"] {
            color: #D96B43 !important;
            border-bottom-color: #D96B43 !important;
            font-size: 1.05em !important;
        }
        hr {
            border-color: #C4B9AF !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- LEARNING ANALYTICS LOGGER (FIXED CSV EXPORT BUG) ---
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
        log_data.to_csv(LOG_FILE, index=False)  # FIXED: Writing to file target instead of data variable
    else:
        log_data.to_csv(LOG_FILE, mode='a', header=False, index=False)

# --- SESSION STATE INITIALIZATION ---
if 'student_id' not in st.session_state:
    st.session_state['student_id'] = "Guest_Student"
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'quiz_submitted' not in st.session_state:
    st.session_state['quiz_submitted'] = False
if 'saved_score' not in st.session_state:
    st.session_state['saved_score'] = 0

if 'zener_data' not in st.session_state:
    st.session_state['zener_data'] = pd.DataFrame(columns=[
        "PSU Voltage V_s (V)", 
        "Calculated Output V_o (V)", 
        "Series Resistor (Ω)", 
        "Load Resistor (Ω)"
    ])

# --- HEADER ---
st.title("⚡ Interactive Zener Diode Shunt Voltage Stabilizer Simulation")
st.subheader("Solid State Electronics Virtual Laboratory Bench")
st.markdown("---")

# --- LOGIN GATEWAY ---
if not st.session_state['authenticated']:
    st.info("👋 Welcome! Please enter your Matriculation or Student Identification Number to launch the bench.")
    matric_no = st.text_input("Student Identification Number:")
    if st.button("Initialize Lab Bench"):
        if matric_no.strip() != "":
            st.session_state['zener_data'] = pd.DataFrame(columns=[
                "PSU Voltage V_s (V)", 
                "Calculated Output V_o (V)", 
                "Series Resistor (Ω)", 
                "Load Resistor (Ω)"
            ])
            st.session_state['student_id'] = matric_no.strip()
            st.session_state['authenticated'] = True
            st.session_state['quiz_submitted'] = False 
            st.session_state['saved_score'] = 0
            
            log_user_action(st.session_state['student_id'], "Session_Start", "Initialized Fresh Isolated Lab Bench.")
            st.rerun()
        else:
            st.warning("An identification number is required to save experimental records.")
    st.stop()

# --- SIDEBAR INTERFACE ---
st.sidebar.header("🎛️ Virtual Instruments")
st.sidebar.markdown(f"**Active Researcher:** `{st.session_state['student_id']}`")
st.sidebar.markdown("---")

# --- MULTI-TAB WORKSPACE NAVIGATION ---
tab_theory, tab_sim, tab_quiz = st.tabs([
    "📖 1. Theory & Component Description", 
    "💻 2. Interactive Simulation Engine", 
    "📝 3. Conceptual Exercise"
])

# ==========================================
# TAB 1: THEORY & COMPONENT DESCRIPTION
# ==========================================
with tab_theory:
    st.header("Theory of Shunt Voltage Regulation")
    st.markdown("""
    A **Zener Diode Shunt Regulator** is an elemental solid-state configuration used to maintain a constant DC output voltage across a fluctuating load or from an unregulated input source. Unlike standard rectifying diodes, a Zener diode is explicitly designed to operate safely in its **reverse breakdown region**.
    
    ### Circuit Dynamics and Physics
    When the unregulated input voltage ($V_s$) rises above the characteristic Zener breakdown voltage ($V_Z$), the Zener diode drops its dynamic resistance drastically. It shunts varying magnitudes of current to ground to keep the terminal voltage stabilized across the load ($R_L$).
    
    1. **Unregulated Region ($V_{open} < V_Z$):** If the open-circuit voltage across the nodes is insufficient to cause reverse breakdown, the Zener diode behaves like an open switch (infinite resistance). The output voltage is simply given by the standard resistive divider equation:
       $$V_o = V_s \\cdot \\left(\\frac{R_L}{R_s + R_L}\\right)$$
       
    2. **Regulated Region ($V_{open} \\ge V_Z$):**
       Once breakdown conditions are met, the voltage across the Zener remains clamped near $V_Z$. In this state, any input voltage surges are absorbed as an increased voltage drop across the series limiting resistor ($R_s$).
    """)
    
    st.markdown("---")
    st.subheader("🛠️ Component Directory")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("""
        * **Power Supply Unit (PSU - $V_s$):** The primary unregulated DC power source supplying variable current to the system loop.
        * **Series Limiting Resistor ($R_s$):** A fundamental protective component. It drops excess raw line voltage and limits structural current loops to defend the Zener diode from lethal thermal runaway.
        """)
    with col_c2:
        st.markdown("""
        * **Zener Diode ($D_Z$):** Connected in *reverse-bias* shunt configurations across the load network. Operates as a variable dynamic impedance reference grid.
        * **Load Resistor ($R_L$):** The terminal system element consuming power, connected in parallel with the regulating Zener.
        """)

# ==========================================
# TAB 2: INTERACTIVE SIMULATION ENGINE
# ==========================================
with tab_sim:
    st.header("Live Circuit Bench & Plotting Module")
    
    st.sidebar.markdown("### Component Tuning")
    r_series = st.sidebar.number_input("Series Limiting Resistor, Rs (Ω):", min_value=10.0, max_value=1000.0, value=220.0, step=10.0, format="%.2f")
    r_load = st.sidebar.number_input("Load Resistor, R_L (Ω):", min_value=100.0, max_value=5000.0, value=1000.0, step=50.0, format="%.2f")
    v_zener = st.sidebar.number_input("Nominal Zener Breakdown Voltage, V_Z (V):", min_value=2.0, max_value=15.0, value=5.1, step=0.1, format="%.2f")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📥 Data Logger Controls")
    v_psu = st.sidebar.number_input("PSU Input Voltage, V_s (Volts):", min_value=0.00, max_value=30.00, value=0.00, step=0.50, format="%.2f")

    # Math Calculation Engine
    v_open = v_psu * (r_load / (r_series + r_load))
    if v_open < v_zener:
        v_output_calc = v_open
    else:
        r_z = 5.0 
        v_output_calc = (((v_psu / r_series) + (v_zener / r_z)) / ((1.0 / r_series) + (1.0 / r_load) + (1.0 / r_z)))

    v_output_calc = min(round(v_output_calc, 2), round(v_psu, 2))

    st.sidebar.info(f"**⚡ Measured Output $V_o$ = {v_output_calc:.2f} Volts**")

    if st.sidebar.button("Log Calculated Metrics to Table"):
        new_row = pd.DataFrame([{
            "PSU Voltage V_s (V)": round(v_psu, 2), 
            "Calculated Output V_o (V)": v_output_calc,
            "Series Resistor (Ω)": round(r_series, 2),
            "Load Resistor (Ω)": round(r_load, 2)
        }])
        st.session_state['zener_data'] = pd.concat([st.session_state['zener_data'], new_row], ignore_index=True).drop_duplicates(subset=["PSU Voltage V_s (V)"]).sort_values(by="PSU Voltage V_s (V)")
        log_user_action(st.session_state['student_id'], "Zener_Auto_Row_Added", f"Vs={v_psu}, Vo={v_output_calc}")
        st.toast("Calculated values recorded!", icon="⚙️")

    if st.sidebar.button("🚨 Clear Active Session Data"):
        st.session_state['zener_data'] = pd.DataFrame(columns=["PSU Voltage V_s (V)", "Calculated Output V_o (V)", "Series Resistor (Ω)", "Load Resistor (Ω)"])
        st.sidebar.warning("All data records purged.")
        st.rerun()

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("🖼️ Circuit Schematic Reference")
        
        # High-Fidelity Professional Image Call
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/e/ee/Zener_diode_stabilizer.svg", 
            caption="Standard Zener Diode Shunt Regulator Topology",
            use_container_width=True
        )
        
        st.caption(f"Active Live Parameters: Rs = {r_series} Ω, RL = {r_load} Ω, VZ Target = {v_zener} V")

    with col_right:
        st.subheader("📋 Experimental Spreadsheet Log")
        active_df = st.session_state['zener_data']
        st.dataframe(active_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("📊 Regulation Characteristics Plot: Output Voltage vs Supply Input")
    
    fig = go.Figure()
    if not active_df.empty:
        fig.add_trace(go.Scatter(
            x=active_df["PSU Voltage V_s (V)"], 
            y=active_df["Calculated Output V_o (V)"],
            mode='markers+lines', 
            name="Logged Lab Data",
            marker=dict(color='#D96B43', size=10, symbol='diamond'),
            line=dict(color='#D96B43', width=2.5)
        ))
        x_max = max(active_df["PSU Voltage V_s (V)"].max() + 2, 15.0)
        y_max = max(active_df["Calculated Output V_o (V)"].max() + 2, v_zener + 2)
    else:
        x_max, y_max = 15.0, 10.0
        st.info("💡 The coordinate grid is waiting for logs. Adjust 'PSU Input Voltage' in the sidebar and click 'Log Calculated Metrics to Table'.")

    fig.layout = go.Layout(
        xaxis=dict(title="Input Supply Voltage, V_s (Volts)", range=[0, x_max], zeroline=True, gridcolor="#EBE5DC", titlefont=dict(color="#2B2625"), tickfont=dict(color="#2B2625")),
        yaxis=dict(title="Stabilized Output Voltage, V_o (Volts)", range=[0, y_max], zeroline=True, gridcolor="#EBE5DC", titlefont=dict(color="#2B2625"), tickfont=dict(color)
