import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Zener Shunt Stabilizer Lab Bench",
    page_icon="⚡",
    layout="wide"
)

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
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Unified Data Table holding all custom stabilization entries
if 'zener_data' not in st.session_state:
    st.session_state['zener_data'] = pd.DataFrame(columns=[
        "PSU Voltage V_s (V)", 
        "Measured Output V_o (V)", 
        "Series Resistor (Ω)", 
        "Load Resistor (Ω)"
    ])

# --- HEADER ---
st.title("⚡ Practical: Zener Diode Shunt Voltage Stabilizer")
st.subheader("Department of Physics/Electronics — Solid State Electronics Laboratory")
st.markdown("---")

# --- LOGIN GATEWAY ---
if not st.session_state['authenticated']:
    st.info("👋 Welcome! Please initialize the laboratory bench by entering your Matriculation Number.")
    matric_no = st.text_input("Student Matriculation Number:")
    if st.button("Initialize Lab Bench"):
        if matric_no.strip() != "":
            st.session_state['student_id'] = matric_no.strip()
            st.session_state['authenticated'] = True
            log_user_action(st.session_state['student_id'], "Session_Start", "Initialized Zener Stabilizer Bench.")
            st.rerun()
        else:
            st.warning("Identification required to track experimental logs.")
    st.stop()

# --- SIDEBAR: BENCH CONFIGURATION & VARIABLE ENTRY PANEL ---
st.sidebar.header("🎛️ Virtual Instrument Controls")

st.sidebar.markdown("### 1. Component Tuning (Variable Inputs)")
# Enable students to change and configure nominal component values dynamically
r_series = st.sidebar.number_input("Series Limiting Resistor, Rs (Ω):", min_value=10.0, max_value=1000.0, value=220.0, step=10.0, format="%.2f")
r_load = st.sidebar.number_input("Load Resistor, R_L (Ω):", min_value=100.0, max_value=5000.0, value=1000.0, step=50.0, format="%.2f")
v_zener = st.sidebar.number_input("Nominal Zener Voltage, V_Z (Volts):", min_value=2.0, max_value=15.0, value=5.1, step=0.1, format="%.2f")

st.sidebar.markdown("---")
st.sidebar.subheader("📥 Active Measurement Data Logger")
st.sidebar.markdown("*Vary your unregulated DC Input Power Supply Unit (PSU) voltage and log the resulting stabilized output voltage.*")

# Measurement input fields supporting 2 decimal places
v_psu = st.sidebar.number_input("PSU Input Voltage, V_s (Volts):", min_value=0.00, max_value=30.00, value=0.00, step=0.50, format="%.2f")
v_output = st.sidebar.number_input("Measured Output Voltage, V_o (Volts):", min_value=0.00, max_value=20.00, value=0.00, step=0.01, format="%.2f")

if st.sidebar.button("Log Stabilizer Metrics Row"):
    new_row = pd.DataFrame([{
        "PSU Voltage V_s (V)": round(v_psu, 2), 
        "Measured Output V_o (V)": round(v_output, 2),
        "Series Resistor (Ω)": round(r_series, 2),
        "Load Resistor (Ω)": round(r_load, 2)
    }])
    st.session_state['zener_data'] = pd.concat([st.session_state['zener_data'], new_row], ignore_index=True).drop_duplicates(subset=["PSU Voltage V_s (V)"]).sort_values(by="PSU Voltage V_s (V)")
    log_user_action(st.session_state['student_id'], "Zener_Row_Added", f"Vs={v_psu}, Vo={v_output}, Rs={r_series}, Rl={r_load}")
    st.toast("Data point successfully logged!", icon="📝")

if st.sidebar.button("🚨 Clear Active Session Data"):
    st.session_state['zener_data'] = pd.DataFrame(columns=["PSU Voltage V_s (V)", "Measured Output V_o (V)", "Series Resistor (Ω)", "Load Resistor (Ω)"])
    st.sidebar.warning("All data records purged.")
    st.rerun()

# --- MAIN BENCH INTERFACE ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🎛️ Software-Defined Schematic Circuit Diagram")
    
    # Text-Based ASCII Schematic Mapping representing the precise physical connection setup
    st.code(f"""
    Unregulated DC PSU                   Series Resistor Rs ({r_series} Ω)
         (V_s) ───────────────────────────[ 220 Ω Nominal ]───────────┬──────────────┐
                                                                       │              │
                                                                     ┌─┴─┐          ┌─┴─┐
                                                                     └───┘          │   │
                                                                   Zener Diode      │1K │ Load Resistor
                                                                     (D_Z)          │   │  R_L ({r_load} Ω)
                                                                     ▲ V_Z          │   │
                                                                     └───┘          └─┬─┘
                                                                       │              │
         GND (0V) ─────────────────────────────────────────────────────┴──────────────┴────── (V_o)
                                                                                      Digital Voltmeter
    """, language="text")
    
    st.markdown("""
    ### 🔬 Experimental Bill of Materials Used:
    * **Power Supply Unit (PSU):** Variable un-regulated DC voltage source ($V_s$)
    * **Series Limiting Resistor ($R_s$):** $220\ \Omega$ nominal value (used to drop excess voltage)
    * **Zener Diode ($D_Z$):** Shunt regulator acting as the fixed voltage reference
    * **Load Resistor ($R_L$):** $1\text{ k}\Omega$ ($1000\ \Omega$) terminal element
    * **Digital Voltmeter:** High-impedance monitoring device connected in shunt to measure output ($V_o$)
    """)

with col_right:
    st.subheader("📋 Experimental Spreadsheet Log")
    active_df = st.session_state['zener_data']
    st.dataframe(active_df, use_container_width=True, hide_index=True)

st.markdown("---")

# --- UNIFIED ANALYSIS GRAPHING ENGINE ---
col_chart, col_viva = st.columns([4, 3])

with col_chart:
    st.subheader("📊 Regulation Characteristics Plot: $V_o$ versus $V_s$")
    st.markdown("*Observing the structural transition from the unregulated linear tracking state to the flat voltage stabilization plateau.*")
    
    fig = go.Figure()
    
    if not active_df.empty:
        # Plotting actual student entries
        fig.add_trace(go.Scatter(
            x=active_df["PSU Voltage V_s (V)"], 
            y=active_df["Measured Output V_o (V)"],
            mode='markers+lines', 
            name="Your Custom Logged Data",
            marker=dict(color='#00CC96', size=10, symbol='diamond'),
            line=dict(color='#00CC96', width=2.5)
        ))
        x_max = max(active_df["PSU Voltage V_s (V)"].max() + 2, 15.0)
        y_max = max(active_df["Measured Output V_o (V)"].max() + 2, v_zener + 2)
    else:
        x_max, y_max = 15.0, 10.0
        st.info("💡 The coordinate grid is waiting for entry matrices. Input values from your bench observations into the sidebar panel.")

    fig.layout = go.Layout(
        xaxis=dict(title="Input Supply Voltage, V_s (Volts)", range=[0, x_max], zeroline=True, gridcolor="rgba(255,255,255,0.1)"),
        yaxis=dict(title="Stabilized Output Voltage, V_o (Volts)", range=[0, y_max], zeroline=True, gridcolor="rgba(255,255,255,0.1)"),
        template="plotly_dark",
        height=400,
        margin=dict(l=20, r=20, t=10, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

with col_viva:
    st.subheader("📝 Post-Lab Regulation Assessment")
    
    with st.form("zener_viva_voce"):
        q1 = st.radio(
            "1. What happens to the output voltage (Vo) once the input supply voltage (Vs) exceeds the Zener breakdown threshold?",
            ["Vo continues to rise linearly matching the input ramp profile.",
             "Vo enters a flat stabilization plateau, clamping around the Zener breakdown voltage layer.",
             "Vo immediately drops to absolute zero due to internal shunt thermal failure."]
        )
        
        q2 = st.radio(
            "2. What is the explicit physical purpose of the 220 ohm resistor connected in series with the input line?",
            ["To boost the current flow passing downstream toward the load infrastructure.",
             "To absorb excess voltage variations and limit current to protect the Zener diode from thermal runaway.",
             "To bypass the breakdown region completely and force the circuit into forward conduction."]
        )
        
        q3 = st.radio(
            "3. If the load resistance (1k resistor) is decoupled entirely from the output nodes, what happens to the current passing through the Zener diode?",
            ["Zener current increases substantially because it must shunt all current previously drawn by the load.",
             "Zener current drops to absolute zero because open loops isolate the semiconductor matrix.",
             "The Zener diode transforms into an active current generator."]
        )
        
        q4 = st.radio(
            "4. In which operational bias condition must a Zener diode be connected to function reliably as a shunt voltage stabilizer?",
            ["Strict Forward Bias, utilizing its native knee potential threshold.",
             "Strict Reverse Bias, operating in its avalanche/Zener breakdown region.",
             "Alternating Bias conditions to periodically balance majority charge carrier fields."]
        )
        
        q5 = st.radio(
            "5. If your input PSU voltage is lower than the configured breakdown threshold, what is the operational state of the stabilizer circuit?",
            ["The Zener diode acts as an open circuit, and output voltage is determined strictly by a resistive voltage divider.",
             "The Zener diode behaves as a perfect short circuit, routing all available input energy straight to ground.",
             "The system operates with maximum efficiency because leakage lines are minimized."]
        )
        
        submitted = st.form_submit_button("Submit Grade Matrix")
        
        if submitted:
            score = 0
            if q1 == "Vo enters a flat stabilization plateau, clamping around the Zener breakdown voltage layer.": score += 20
            if q2 == "To absorb excess voltage variations and limit current to protect the Zener diode from thermal runaway.": score += 20
            if q3 == "Zener current increases substantially because it must shunt all current previously drawn by the load.": score += 20
            if q4 == "Strict Reverse Bias, operating in its avalanche/Zener breakdown region.": score += 20
            if q5 == "The Zener diode acts as an open circuit, and output voltage is determined strictly by a resistive voltage divider.": score += 20
            
            st.metric("Final Assessment Score", f"{score}/100")
            if score == 100:
                st.success("Perfect alignment! You have fully verified the dynamics of shunt voltage regulation networks.")
            else:
                st.warning("Discrepancies identified. Review your logged data tracking matrices and retry.")
            log_user_action(st.session_state['student_id'], "Zener_Quiz_Submitted", f"Score: {score}/100")

st.markdown("---")
if st.button("Log Out / Reset Lab Bench"):
    st.session_state['authenticated'] = False
    st.rerun()