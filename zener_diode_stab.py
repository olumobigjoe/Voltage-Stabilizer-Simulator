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
            background-color: #8B5A2B;
            color: #000000;
        }
        /* Main background content container card (Slightly Lighter Warm Brown for visibility) */
        .main .block-container {
            background-color: #A06D3B;
            padding: 3rem;
            border-radius: 10px;
            margin-top: 2rem;
            border: 3px solid #000000;
        }
        /* Sidebar layout styling */
        section[data-testid="stSidebar"] {
            background-color: #734A22 !important;
            border-right: 3px solid #000000;
        }
        /* Enforce absolute black on text, labels, headers, and descriptions */
        h1, h2, h3, h4, p, span, label, li, .stMarkdown, section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] h3 {
            color: #000000 !important;
            font-weight: 600 !important;
        }
        /* Form containers, alerts, and input blocks */
        div[data-testid="stForm"], .stAlert, div[data-testid="stWidgetLabel"], div[data-testid="stNumberInput"] {
            background-color: #B3804E !important;
            border: 2px solid #000000 !important;
            color: #000000 !important;
        }
        /* Input elements internal text color override */
        input {
            color: #000000 !important;
            font-weight: bold !important;
        }
        /* Interactive Buttons */
        div.stButton > button {
            background-color: #000000 !important;
            color: #A06D3B !important;
            border: 2px solid #000000 !important;
            font-weight: bold;
        }
        div.stButton > button:hover {
            background-color: #A06D3B !important;
            color: #000000 !important;
            border-color: #000000 !important;
        }
        /* Tab navigation formatting */
        button[data-baseweb="tab"] {
            color: #3D2510 !important;
            font-weight: bold !important;
        }
        button[aria-selected="true"] {
            color: #000000 !important;
            border-bottom-color: #000000 !important;
            font-size: 1.1em !important;
        }
        hr {
            border-color: #000000 !important;
            border-width: 2px;
        }
        /* Structural Dataframe tables forced visibility styling */
        div[data-testid="stDataFrame"] {
            background-color: #B3804E !important;
            border: 2px solid #000000;
        }
    </style>
""", unsafe_allow_html=True)

# --- LEARNING ANALYTICS LOGGER (FIXED BUG) ---
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
        log_data.to_csv(LOG_FILE, index=False) # FIXED: Changed from log_data to LOG_FILE
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
st.subheader("Department of Physics/Electronics — Solid State Electronics Laboratory Workspace")
st.markdown("---")

# --- LOGIN GATEWAY ---
if not st.session_state['authenticated']:
    st.info("👋 Welcome! Please initialize the laboratory bench by entering your Matriculation/Student Number.")
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
            st.warning("Identification required to track experimental logs.")
    st.stop()

# --- SIDEBAR INTERFACE ---
st.sidebar.header("🎛️ Virtual Instrument Controls")
st.sidebar.markdown(f"**Active User:** `{st.session_state['student_id']}`")
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
        st.subheader("🎛️ Schematic Circuit Diagram Reference")
        
        # High-Fidelity Diagram Injection Tag replacing the old code text block
        st.markdown("")
        
        st.caption(f"Active Parameter States: Series Resistor ($R_s$) = {r_series} Ω, Load Resistor ($R_L$) = {r_load} Ω, Target Reference ($V_Z$) = {v_zener} V")

    with col_right:
        st.subheader("📋 Experimental Spreadsheet Log")
        active_df = st.session_state['zener_data']
        st.dataframe(active_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("📊 Regulation Characteristics Plot: $V_o$ versus $V_s$")
    
    fig = go.Figure()
    if not active_df.empty:
        fig.add_trace(go.Scatter(
            x=active_df["PSU Voltage V_s (V)"], 
            y=active_df["Calculated Output V_o (V)"],
            mode='markers+lines', 
            name="Logged Automated Data",
            marker=dict(color='#000000', size=10, symbol='diamond'),
            line=dict(color='#000000', width=2.5)
        ))
        x_max = max(active_df["PSU Voltage V_s (V)"].max() + 2, 15.0)
        y_max = max(active_df["Calculated Output V_o (V)"].max() + 2, v_zener + 2)
    else:
        x_max, y_max = 15.0, 10.0
        st.info("💡 The coordinate grid is waiting for logs. Adjust 'PSU Input Voltage' in the sidebar and click 'Log Calculated Metrics to Table'.")

    fig.layout = go.Layout(
        xaxis=dict(title="Input Supply Voltage, V_s (Volts)", range=[0, x_max], zeroline=True, gridcolor="rgba(0,0,0,0.25)", titlefont=dict(color="#000000"), tickfont=dict(color="#000000")),
        yaxis=dict(title="Stabilized Output Voltage, V_o (Volts)", range=[0, y_max], zeroline=True, gridcolor="rgba(0,0,0,0.25)", titlefont=dict(color="#000000"), tickfont=dict(color="#000000")),
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#B3804E",
        height=400,
        margin=dict(l=20, r=20, t=10, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# TAB 3: CONCEPTUAL EXERCISE
# ==========================================
with tab_quiz:
    st.header("Post-Lab Core Component Assessment")
    
    if st.session_state['quiz_submitted']:
        st.error(f"🔒 Submission Closed. You have already completed this laboratory evaluation test.")
        st.metric("Your Locked Grade Score", f"{st.session_state['saved_score']}/100")
    else:
        with st.form("zener_viva_voce"):
            q1 = st.radio(
                "1. What structural behavior defines a Zener diode compared to standard rectifying diodes?",
                ["It possesses a heavily doped p-n junction engineered for reliable breakdown in reverse bias.",
                 "It acts exclusively as an open circuit when forward-biased.",
                 "It completely blocks current flow in both operational directions permanently."]
            )
            
            q2 = st.radio(
                "2. What is the role of the series limiting resistor ($R_s$) in this shunt circuit?",
                ["To boost the overall current profile exiting the unregulated supply network.",
                 "To handle excess input voltage variance and protect the Zener from thermal destruction.",
                 "To eliminate voltage limits and facilitate unregulated high power transfer."]
            )
            
            q3 = st.radio(
                "3. If the load resistor ($R_L$) is completely disconnected (open-circuit condition), how does the Zener diode react?",
                ["Its current increases substantially because it must shunt all loop current previously routed to the load.",
                 "The diode instantly reverses into an active power source generation matrix.",
                 "Zener tracking current falls directly to zero as power paths decouple."]
            )
            
            q4 = st.radio(
                "4. What operational state occurs if the unregulated input voltage supply is less than the Zener breakdown threshold?",
                ["The Zener operates as an open circuit, making output voltage dependent on the resistive voltage divider.",
                 "The Zener turns into an ideal short circuit to loop structural configurations to ground.",
                 "The load drops to a negative voltage range relative to standard system ground references."]
            )
            
            q5 = st.radio(
                "5. In which bias condition must a Zener diode run to achieve voltage regulation outputs?",
                ["Forward-bias condition near standard native knee values.",
                 "Reverse breakdown avalanche/Zener region thresholds.",
                 "Unbiased floating state loops entirely decoupled from active ground paths."]
            )
            
            submitted = st.form_submit_button("Submit Assessment (Single Attempt Only)")
            
            if submitted:
                score = 0
                if q1 == "It possesses a heavily doped p-n junction engineered for reliable breakdown in reverse bias.": score += 20
                if q2 == "To handle excess input voltage variance and protect the Zener from thermal destruction.": score += 20
                if q3 == "Its current increases substantially because it must shunt all loop current previously routed to the load.": score += 20
                if q4 == "The Zener operates as an open circuit, making output voltage dependent on the resistive voltage divider.": score += 20
                if q5 == "Reverse breakdown avalanche/Zener region thresholds.": score += 20
                
                st.session_state['quiz_submitted'] = True
                st.session_state['saved_score'] = score
                
                log_user_action(st.session_state['student_id'], "Zener_Quiz_Locked_Submission", f"Score: {score}/100")
                st.rerun()

# --- FOOTER RESET TRIGGER ---
st.markdown("---")
if st.button("🚪 Log Out / Reset Lab Bench Session"):
    st.session_state['authenticated'] = False
    st.session_state['quiz_submitted'] = False
    st.session_state['saved_score'] = 0
    st.session_state['zener_data'] = pd.DataFrame(columns=["PSU Voltage V_s (V)", "Calculated Output V_o (V)", "Series Resistor (Ω)", "Load Resistor (Ω)"])
    st.rerun()
