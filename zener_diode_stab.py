import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Zener Diode Voltage Stabilizer Module",
    page_icon=" ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS — Deep Space Teal & Violet Theme ────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Nunito:wght@400;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }

/* ── Background ── */
.stApp {
    background: linear-gradient(145deg, #020818 0%, #060d1f 40%, #030b18 100%);
    color: #cde8f5;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #0a1f4e 0%, #0d2860 40%, #1a1060 100%);
    border: 1px solid #2563eb;
    border-radius: 14px; padding: 30px 40px; margin-bottom: 26px;
    position: relative; overflow: hidden;
    box-shadow: 0 8px 32px rgba(14,165,233,0.25);
}
.hero::before {
    content:''; position:absolute; top:0; left:0; right:0; height:3px;
    background: linear-gradient(90deg, transparent, #06b6d4, #7c3aed, transparent);
}
.hero::after {
    content:''; position:absolute; right:-60px; top:-60px;
    width:200px; height:200px; border-radius:50%;
    background: rgba(6,182,212,0.07);
}
.hero-title { font-family:'Share Tech Mono',monospace; font-size:1.85rem; color:#06b6d4; margin:0; letter-spacing:.04em; }
.hero-sub   { font-size:.82rem; color:#7dd3fc; margin-top:7px; letter-spacing:.1em; text-transform:uppercase; font-weight:700; }

/* ── Section Header ── */
.sec {
    font-family:'Share Tech Mono',monospace; font-size:.74rem; color:#06b6d4;
    letter-spacing:.18em; text-transform:uppercase;
    border-bottom:1px solid #1e3a5f; padding-bottom:5px; margin:22px 0 14px;
}

/* ── Definition Cards ── */
.def-card {
    background: #060f24; border:1px solid #1e3a5f; border-left:4px solid #06b6d4;
    border-radius:10px; padding:15px 18px; margin-bottom:12px;
    box-shadow: 0 2px 10px rgba(6,182,212,0.08);
    transition: transform 0.2s;
}
.def-card:hover { transform: translateX(4px); }
.def-title { font-weight:800; color:#38bdf8; font-size:.9rem; margin-bottom:5px; }
.def-body  { font-size:.83rem; color:#94c4d8; line-height:1.68; }

/* ── Info Box ── */
.info-box {
    background:#060f24; border:1px solid #1e4a7f; border-radius:10px;
    padding:16px 20px; font-size:.86rem; color:#a5d8ef; line-height:1.7;
}
.info-box strong { color:#38bdf8; }

/* ── Callout box ── */
.amber-box {
    background:#0a0f2a; border:1px solid #7c3aed; border-radius:10px;
    padding:14px 18px; font-size:.84rem; color:#c4b5fd; line-height:1.65; margin:10px 0;
}
.amber-box strong { color:#a78bfa; }

/* ── Metric Cards ── */
.mc {
    background:#060f24; border:1px solid #1e3a5f; border-radius:10px;
    padding:14px 10px; text-align:center;
    box-shadow:0 2px 8px rgba(6,182,212,0.1);
}
.mc .ml { font-size:.65rem; color:#4a7a9b; text-transform:uppercase; letter-spacing:.09em; font-weight:700; }
.mc .mv { font-family:'Share Tech Mono',monospace; font-size:1.35rem; color:#06b6d4; margin-top:4px; }
.mc .mu { font-size:.65rem; color:#2a5a7a; }

/* ── Status indicators ── */
.status-reg   { background:#021a10; border:2px solid #4ade80; border-radius:8px; padding:12px 18px; color:#4ade80; font-family:'Share Tech Mono',monospace; font-size:.9rem; }
.status-unreg { background:#0a0a20; border:2px solid #a78bfa; border-radius:8px; padding:12px 18px; color:#a78bfa; font-family:'Share Tech Mono',monospace; font-size:.9rem; }

/* ── Score cards ── */
.score-pass { background:#021a10; border:2px solid #4ade80; border-radius:12px; padding:20px; color:#4ade80; }
.score-mid  { background:#0d1030; border:2px solid #818cf8; border-radius:12px; padding:20px; color:#818cf8; }
.score-fail { background:#1a0520; border:2px solid #f472b6; border-radius:12px; padding:20px; color:#f472b6; }

/* ── Param display ── */
.pd { background:#060f24; border:2px solid #1e4a7f; border-radius:8px; padding:9px 0;
      text-align:center; font-family:'Share Tech Mono',monospace; font-size:1.2rem; color:#06b6d4; font-weight:700; }
.pl { font-size:.68rem; color:#4a7a9b; text-transform:uppercase; letter-spacing:.09em; text-align:center; margin-bottom:3px; font-weight:700; }

/* ── Comparison table ── */
.cmp-table { width:100%; border-collapse:collapse; font-size:.84rem; border-radius:10px; overflow:hidden; }
.cmp-table th { background:#0d2860; color:#38bdf8; padding:10px 14px; text-align:left; font-weight:800; }
.cmp-table td { padding:9px 14px; border-bottom:1px solid #0f1f3a; color:#94c4d8; }
.cmp-table tr:nth-child(even) td { background:#060f24; }
.cmp-table td:first-child { font-weight:700; color:#06b6d4; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060d1f 0%, #020818 100%);
    border-right:1px solid #1e3a5f;
}
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color:#38bdf8; }
[data-testid="stSidebar"] label { color:#7dd3fc !important; font-weight:600 !important; }
[data-testid="stSidebar"] .stMarkdown p { color:#4a7a9b; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background:#060d1f; border-bottom:2px solid #1e3a5f;
    border-radius:10px 10px 0 0; gap:4px; padding:0 8px;
}
.stTabs [data-baseweb="tab"] {
    background:transparent; color:#4a7a9b; border:none;
    font-family:'Nunito',sans-serif; font-size:.88rem; font-weight:700; padding:12px 20px;
}
.stTabs [aria-selected="true"] {
    background:#060f24 !important; color:#06b6d4 !important;
    border-bottom:3px solid #06b6d4 !important; border-radius:8px 8px 0 0;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #0d2860, #1a1060);
    color:#38bdf8; border:1px solid #2563eb; border-radius:8px;
    font-family:'Nunito',sans-serif; font-size:.85rem; font-weight:700;
    padding:8px 20px; transition:all .2s; width:100%;
    box-shadow:0 2px 8px rgba(6,182,212,0.2);
}
.stButton > button:hover { background:linear-gradient(135deg,#1e4a9f,#2d1a90); transform:translateY(-1px); }

/* ── Inputs ── */
.stNumberInput label, .stSelectbox label, .stRadio label { color:#7dd3fc !important; font-weight:600 !important; font-size:.85rem !important; }
div[data-baseweb="radio"] > div {
    background:#060f24; border:1px solid #1e3a5f; border-radius:8px;
    padding:8px 12px; margin:4px 0; transition:all .15s;
}
div[data-baseweb="radio"] > div:hover { background:#0d1a3a; border-color:#2563eb; }
</style>
""", unsafe_allow_html=True)

# ─── LOGGER (FIXED — was passing df instead of LOG_FILE) ─────────────────────
LOG_FILE = "zener_lab_log.csv"

def log_action(sid, action, detail=""):
    row = pd.DataFrame([{
        "Timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Student_ID": sid, "Action": action, "Detail": str(detail)
    }])
    if not os.path.isfile(LOG_FILE):
        row.to_csv(LOG_FILE, index=False)          # ← FIXED: was log_data.to_csv(log_data,...)
    else:
        row.to_csv(LOG_FILE, mode='a', header=False, index=False)

# ─── SESSION STATE ────────────────────────────────────────────────────────────
DEFS = {
    "auth": False, "student_id": "",
    "zener_data": pd.DataFrame(columns=["V_s (V)", "V_o (V)", "Rs (Ω)", "RL (Ω)"]),
    "quiz_submitted": False, "quiz_score": 0,
}
for k, v in DEFS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── HERO ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <p class="hero-title"> Zener Diode Shunt Voltage Stabilizer Virtual Lab</p>
  <p class="hero-sub">DC Voltage Regulation · Breakdown Characteristics · Solid State Electronics</p>
</div>""", unsafe_allow_html=True)

# ─── LOGIN ────────────────────────────────────────────────────────────────────
if not st.session_state["auth"]:
    c1, c2, c3 = st.columns([1, 1.6, 1])
    with c2:
        st.markdown("""
        <div class="info-box" style="text-align:center;margin-bottom:20px;">
             <strong>Welcome to the Zener Stabilizer Lab!</strong><br>
            Enter your Matriculation Number to initialise the laboratory bench.
        </div>""", unsafe_allow_html=True)
        mat = st.text_input("Matriculation Number", placeholder="e.g. ENG/HND/2024/021")
        if st.button("▶  INITIALISE THE LAB"):
            if mat.strip():
                st.session_state["student_id"]  = mat.strip()
                st.session_state["auth"]        = True
                st.session_state["zener_data"]  = pd.DataFrame(columns=["V_s (V)","V_o (V)","Rs (Ω)","RL (Ω)"])
                st.session_state["quiz_submitted"] = False
                st.session_state["quiz_score"]  = 0
                log_action(mat.strip(), "Session_Start")
                st.rerun()
            else:
                st.error("⚠️  Matriculation number is required.")
    st.stop()

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"###  Lab Bench")
    st.markdown(f"**`{st.session_state['student_id']}`**")
    st.markdown("---")
    st.markdown("###  Component Values")

    rs     = st.number_input("Series Resistor Rs (Ω):", 10.0, 1000.0, 220.0, 10.0, format="%.1f")
    rl     = st.number_input("Load Resistor RL (Ω):",  100.0,5000.0,1000.0, 50.0, format="%.1f")
    vz     = st.number_input("Zener Voltage Vz (V):",   2.0,  15.0,   5.1,   0.1, format="%.1f")

    st.markdown("---")
    st.markdown("###  PSU Input")
    vs     = st.number_input("Supply Voltage Vs (V):", 0.0, 30.0, 0.0, 0.5, format="%.2f")

    # ── Physics engine ──
    rz      = 5.0   # Zener dynamic resistance
    v_div   = vs * (rl / (rs + rl))
    if v_div < vz:
        vo = round(v_div, 3)
    else:
        vo = round(((vs / rs) + (vz / rz)) / ((1/rs) + (1/rl) + (1/rz)), 3)
    vo = min(vo, vs)

    is_reg = vo >= vz * 0.95
    clr    = "#4ade80" if is_reg else "#f0a060"
    lbl    = "REGULATING ✓" if is_reg else "UNREGULATED"

    st.markdown(f"""
    <div style="background:#0d0600;border:2px solid {clr};border-radius:10px;
                padding:14px;text-align:center;margin:12px 0;
                box-shadow:0 2px 12px rgba(0,0,0,0.5);">
      <div style="font-size:.65rem;color:#8b6040;text-transform:uppercase;
                  letter-spacing:.1em;font-weight:700;">Computed Output Vo</div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:1.6rem;
                  color:{clr};font-weight:700;margin:4px 0;">{vo:.3f} V</div>
      <div style="font-size:.72rem;color:{clr};font-weight:700;">{lbl}</div>
    </div>""", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button(" Log Data"):
            nr = pd.DataFrame([{"V_s (V)":round(vs,2),"V_o (V)":vo,"Rs (Ω)":round(rs,1),"RL (Ω)":round(rl,1)}])
            st.session_state["zener_data"] = (
                pd.concat([st.session_state["zener_data"], nr], ignore_index=True)
                .drop_duplicates(subset=["V_s (V)"]).sort_values("V_s (V)"))
            log_action(st.session_state["student_id"], "DataPoint", f"Vs={vs},Vo={vo}")
            st.toast("Logged!", icon="⚙️")
    with col_b:
        if st.button(" Clear"):
            st.session_state["zener_data"] = pd.DataFrame(columns=["V_s (V)","V_o (V)","Rs (Ω)","RL (Ω)"])
            st.rerun()

    st.markdown("---")
    st.markdown(f"**Points logged:** `{len(st.session_state['zener_data'])}`")
    if st.session_state["quiz_submitted"]:
        sc = st.session_state["quiz_score"]
        clr2 = "#4ade80" if sc >= 60 else "#f87171"
        st.markdown(f'<span style="color:{clr2};font-weight:700;font-family:monospace;">Quiz: {sc}/100</span>',
                    unsafe_allow_html=True)
    st.markdown("---")
    if st.button(" Log Out"):
        st.session_state["auth"] = False
        st.rerun()

# ─── TABS ────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📖  THEORY & COMPONENTS",
    "🔬  SIMULATION",
    "📝  EXERCISE & SCORING",
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — THEORY & COMPONENTS
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<p class="sec">Practical Overview</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
    <strong>Objective:</strong> To investigate the voltage regulation characteristics of a Zener Diode
    Shunt Stabilizer circuit and to understand how a reverse-biased Zener diode maintains a constant
    output voltage despite variations in input supply voltage (Vs) and load conditions.<br><br>
    <strong>Principle:</strong> When reverse-biased beyond its breakdown voltage (Vz), a Zener diode
    enters the <em>avalanche/Zener breakdown region</em> and clamps the voltage across its terminals
    to a near-constant value. A series resistor (Rs) absorbs the excess voltage and limits current,
    protecting the diode. This behaviour forms the basis of simple DC voltage regulation.
    </div>""", unsafe_allow_html=True)

    # ── Component Definitions ─────────────────────────────────────────────────
    st.markdown('<p class="sec">Definitions of Key Components & Terms</p>', unsafe_allow_html=True)

    defs = [
        ("🛡️ Zener Diode (Dz)",
         "A specially manufactured PN junction diode designed to operate reliably in the reverse "
         "breakdown region. Unlike ordinary diodes, it is not destroyed by controlled reverse breakdown. "
         "It maintains a nearly constant voltage (Vz) across its terminals over a wide range of currents. "
         "Common Vz values: 2.4 V, 3.3 V, 5.1 V, 6.2 V, 9.1 V, 12 V."),
        ("⚡ Zener Breakdown Voltage (Vz)",
         "The specific reverse voltage at which the Zener diode enters conduction. Below Vz, the diode "
         "blocks (acts as open circuit). At and above Vz, it conducts and clamps the voltage. Two physical "
         "mechanisms: Zener effect (quantum tunnelling, dominant below 5.5 V) and avalanche multiplication "
         "(impact ionisation, dominant above 5.5 V)."),
        ("🔗 Series Limiting Resistor (Rs)",
         "Connected between the unregulated input supply and the Zener-load junction. It serves two "
         "critical roles: (1) drops the excess voltage (Vs − Vz) across itself, and (2) limits the "
         "current through the Zener diode to a safe level. Rs must be sized so that Iz stays between "
         "Iz(min) and Iz(max) across all load conditions."),
        ("🏋️ Load Resistor (RL)",
         "The component drawing current from the regulated output. In a real system this represents "
         "any electronic device being powered. The stabilizer must maintain Vo ≈ Vz regardless of "
         "changes in RL. If RL → ∞ (open circuit), all Is flows through the Zener. If RL → 0 "
         "(short circuit), the circuit may fail — hence the importance of Rs."),
        ("📐 Resistive Voltage Divider (Pre-regulation)",
         "When Vs < Vz, the Zener diode is reverse biased but not in breakdown — it acts as an open "
         "circuit. The output voltage is then determined purely by the Rs–RL voltage divider: "
         "Vo = Vs × RL / (Rs + RL). This is the unregulated region of the Vo vs Vs characteristic."),
        ("📈 Regulation Characteristic Curve",
         "A plot of output voltage Vo (y-axis) versus input supply voltage Vs (x-axis). It shows two "
         "distinct regions: (1) a rising linear section (Vs < Vz) where Vo follows the divider ratio, "
         "and (2) a flat plateau (Vs ≥ Vz) where Vo ≈ Vz. The sharpness of the knee indicates "
         "regulation quality."),
        ("⚡ Zener Current (Iz)",
         "The current flowing through the Zener diode. Iz = Is − IL, where Is = (Vs − Vz)/Rs is the "
         "series current and IL = Vz/RL is the load current. Iz must remain above Iz(min) to keep the "
         "diode in regulation, and below Iz(max) to prevent thermal damage. Power dissipated: Pz = Vz × Iz."),
        ("🔥 Power Dissipation (Pz)",
         "The heat generated by the Zener diode: Pz = Vz × Iz. Every Zener has a maximum rated power "
         "(e.g. 400 mW, 1 W, 5 W). If Pz exceeds this rating, the junction overheats and fails. "
         "Proper Rs selection ensures Iz stays within safe limits under all load conditions, including "
         "open-circuit (no load) — the worst case for Zener current."),
        ("📏 Line Regulation",
         "A measure of how well the circuit maintains Vo when Vs changes: "
         "Line Regulation = ΔVo / ΔVs (expressed as % or mV/V). An ideal stabilizer has zero line "
         "regulation. In practice, the finite Zener dynamic resistance (rz = ΔVz/ΔIz) causes a "
         "small rise in Vz with increasing Iz, giving a slight upward slope in the regulated region."),
        ("📐 Dynamic Resistance (rz)",
         "The slope of the Vz vs Iz curve in the breakdown region: rz = ΔVz / ΔIz. A small rz "
         "(typically 1–50 Ω) means the Zener voltage is nearly independent of current — good regulation. "
         "It appears in the equivalent circuit model as a small resistor in series with the ideal "
         "Zener voltage source. In this simulation rz = 5 Ω."),
    ]

    col1, col2 = st.columns(2)
    for i, (title, body) in enumerate(defs):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="def-card">
              <div class="def-title">{title}</div>
              <div class="def-body">{body}</div>
            </div>""", unsafe_allow_html=True)

    # ── Equations ─────────────────────────────────────────────────────────────
    st.markdown('<p class="sec">Key Circuit Equations</p>', unsafe_allow_html=True)
    st.markdown("""
    <table class="cmp-table">
      <thead><tr><th>Quantity</th><th>Formula</th><th>Notes</th></tr></thead>
      <tbody>
        <tr><td>Series Current Is</td><td>Is = (Vs − Vz) / Rs</td><td>Valid when Vs ≥ Vz</td></tr>
        <tr><td>Load Current IL</td><td>IL = Vz / RL</td><td>In regulation region</td></tr>
        <tr><td>Zener Current Iz</td><td>Iz = Is − IL</td><td>Must stay above Iz(min)</td></tr>
        <tr><td>Output Voltage (unreg)</td><td>Vo = Vs × RL / (Rs + RL)</td><td>When Vs &lt; Vz</td></tr>
        <tr><td>Output Voltage (reg)</td><td>Vo ≈ Vz</td><td>When Vs ≥ Vz + Is·Rs</td></tr>
        <tr><td>Zener Power</td><td>Pz = Vz × Iz</td><td>Must not exceed Pz(max)</td></tr>
        <tr><td>Min Rs (no load)</td><td>Rs(min) = (Vs(max) − Vz) / Iz(max)</td><td>Worst case: RL = ∞</td></tr>
      </tbody>
    </table>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="amber-box">
    <strong>⚠️ Lab Safety:</strong> Never connect a Zener diode in forward bias as a regulator — it will
    simply conduct at ~0.7 V like a normal diode. Always include Rs to limit current.
    Exceeding Iz(max) causes permanent thermal damage. In this simulation: Rs = {rs:.0f} Ω,
    RL = {rl:.0f} Ω, Vz = {vz:.1f} V, rz = 5 Ω.
    </div>""", unsafe_allow_html=True)

    # ── Circuit Diagram ───────────────────────────────────────────────────────
    st.markdown('<p class="sec">Circuit Diagram</p>', unsafe_allow_html=True)
    components.html(f"""
    <style>
      body {{ margin:0; padding:14px 10px 20px; background:#020818; }}
      .w   {{ stroke:#06b6d4; stroke-width:2; fill:none; }}
      .t   {{ fill:#cde8f5; font-family:monospace; font-size:11px; }}
      .lbl {{ fill:#38bdf8; font-family:monospace; font-size:10px; font-weight:bold; }}
      .sub {{ fill:#4a7a9b; font-family:monospace; font-size:9px; }}
    </style>
    <svg viewBox="0 0 760 170" xmlns="http://www.w3.org/2000/svg" width="100%">
      <rect width="760" height="170" fill="#020818"/>

      <!-- PSU -->
      <rect x="20" y="55" width="65" height="60" rx="5"
            style="fill:#060d1f;stroke:#06b6d4;stroke-width:1.8"/>
      <text x="52" y="82" text-anchor="middle" class="t" font-size="13">DC</text>
      <text x="52" y="97" text-anchor="middle" class="lbl">PSU</text>
      <text x="52" y="130" text-anchor="middle" class="sub">Vs={vs:.1f}V</text>

      <!-- Top wire PSU → Rs -->
      <line x1="85" y1="70" x2="150" y2="70" class="w"/>

      <!-- Series Resistor Rs -->
      <rect x="150" y="55" width="100" height="30" rx="4"
            style="fill:#060d1f;stroke:#06b6d4;stroke-width:1.8"/>
      <text x="200" y="74" text-anchor="middle" class="lbl">Rs  {rs:.0f} Ω</text>
      <text x="200" y="100" text-anchor="middle" class="sub">Series Resistor</text>

      <!-- Wire Rs → node A -->
      <line x1="250" y1="70" x2="370" y2="70" class="w"/>
      <!-- node A dot -->
      <circle cx="370" cy="70" r="5" fill="#06b6d4"/>
      <text x="370" y="50" text-anchor="middle" class="sub">Node A</text>

      <!-- Zener Diode (pointing down = reverse bias operation) -->
      <line x1="370" y1="70" x2="370" y2="88" class="w"/>
      <!-- Triangle (anode at bottom in reverse) -->
      <polygon points="356,105 384,105 370,87"
               style="fill:#7c3aed;stroke:#a78bfa;stroke-width:1"/>
      <!-- Cathode bar (Zener has bent ends) -->
      <line x1="352" y1="105" x2="388" y2="105" style="stroke:#a78bfa;stroke-width:3"/>
      <line x1="352" y1="101" x2="352" y2="109" style="stroke:#a78bfa;stroke-width:2"/>
      <line x1="388" y1="101" x2="388" y2="109" style="stroke:#a78bfa;stroke-width:2"/>
      <!-- Zener bent ends on cathode bar -->
      <line x1="352" y1="101" x2="346" y2="96"  style="stroke:#a78bfa;stroke-width:2"/>
      <line x1="388" y1="109" x2="394" y2="114" style="stroke:#a78bfa;stroke-width:2"/>
      <line x1="370" y1="105" x2="370" y2="130" class="w"/>
      <text x="402" y="98"  class="lbl">Dz</text>
      <text x="402" y="110" class="sub">Vz={vz:.1f}V</text>

      <!-- Load Resistor RL (vertical, parallel with Zener) -->
      <rect x="490" y="55" width="100" height="30" rx="4"
            style="fill:#060d1f;stroke:#38bdf8;stroke-width:1.8"/>
      <text x="540" y="74" text-anchor="middle" class="lbl">RL  {rl:.0f} Ω</text>
      <text x="540" y="100" text-anchor="middle" class="sub">Load Resistor</text>

      <!-- Wire Node A → RL top -->
      <line x1="370" y1="70"  x2="490" y2="70"  class="w"/>
      <!-- RL bottom → ground bus -->
      <line x1="590" y1="70"  x2="650" y2="70"  class="w"/>
      <line x1="650" y1="70"  x2="650" y2="130" class="w"/>

      <!-- Ground bus -->
      <line x1="85"  y1="130" x2="650" y2="130" class="w"/>
      <line x1="370" y1="130" x2="370" y2="130" class="w"/>

      <!-- Voltmeter Vo -->
      <circle cx="610" cy="100" r="20" style="fill:#150900;stroke:#facc15;stroke-width:1.8"/>
      <text x="610" y="105" text-anchor="middle"
            style="fill:#facc15;font-family:monospace;font-size:11px;font-weight:bold">V</text>
      <line x1="610" y1="80"  x2="610" y2="70"  style="stroke:#facc15;stroke-width:1.5"/>
      <line x1="610" y1="120" x2="610" y2="130" style="stroke:#facc15;stroke-width:1.5"/>
      <text x="670" y="104" style="fill:#facc15;font-family:monospace;font-size:10px">Vo={vo:.2f}V</text>

      <!-- Is arrow annotation -->
      <text x="290" y="62" class="sub">→ Is</text>

      <!-- Iz annotation -->
      <text x="378" y="90" class="sub">↓ Iz</text>

      <!-- IL annotation -->
      <text x="440" y="62" class="sub">→ IL</text>
    </svg>""", height=195, scrolling=False)

    svg_bytes = f"""<svg viewBox="0 0 760 170" xmlns="http://www.w3.org/2000/svg">
<rect width="760" height="170" fill="#0d0600"/>
<text x="380" y="85" text-anchor="middle" fill="#f0a060" font-family="monospace" font-size="13">
Zener Stabilizer: Rs={rs:.0f}ohm RL={rl:.0f}ohm Vz={vz:.1f}V
</text></svg>""".encode()
    st.download_button("⬇️ Download Circuit Diagram (SVG)", svg_bytes,
                       "zener_circuit.svg", "image/svg+xml")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — SIMULATION
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<p class="sec">Voltage Regulation Characteristic</p>', unsafe_allow_html=True)

    # ── Live metric row ───────────────────────────────────────────────────────
    is_val  = (vs - vo) / rs if rs > 0 else 0
    il_val  = vo / rl if rl > 0 else 0
    iz_val  = max(is_val - il_val, 0)
    pz_val  = vz * iz_val

    def mc(col, lbl, val, unit):
        col.markdown(f'<div class="mc"><div class="ml">{lbl}</div>'
                     f'<div class="mv">{val}</div><div class="mu">{unit}</div></div>',
                     unsafe_allow_html=True)

    m1,m2,m3,m4,m5,m6 = st.columns(6)
    mc(m1, "Vs (input)",  f"{vs:.2f}",        "V")
    mc(m2, "Vo (output)", f"{vo:.3f}",        "V")
    mc(m3, "Is",          f"{is_val*1000:.2f}","mA")
    mc(m4, "IL",          f"{il_val*1000:.2f}","mA")
    mc(m5, "Iz",          f"{iz_val*1000:.2f}","mA")
    mc(m6, "Pz",          f"{pz_val*1000:.2f}","mW")

    st.markdown("")
    reg_cls = "status-reg" if is_reg else "status-unreg"
    reg_msg = (f"✅  REGULATING — Vo ≈ Vz = {vz:.1f} V  |  Zener in breakdown"
               if is_reg else
               f"⚠️  UNREGULATED — Vs ({vs:.2f} V) below Vz ({vz:.1f} V)  |  Output = voltage divider")
    st.markdown(f'<div class="{reg_cls}">{reg_msg}</div>', unsafe_allow_html=True)
    st.markdown("")

    # ── Theoretical sweep + logged data ──────────────────────────────────────
    vs_th   = np.linspace(0, 30, 500)
    vo_th   = []
    for v in vs_th:
        vd = v * (rl / (rs + rl))
        if vd < vz:
            vo_th.append(vd)
        else:
            vr = ((v / rs) + (vz / rz)) / ((1/rs) + (1/rl) + (1/rz))
            vo_th.append(min(vr, v))
    vo_th = np.array(vo_th)

    fig = go.Figure()

    # Shaded regulation region
    reg_start = next((i for i, v in enumerate(vo_th) if v >= vz * 0.95), None)
    if reg_start:
        fig.add_trace(go.Scatter(
            x=np.concatenate([vs_th[reg_start:], vs_th[reg_start:][::-1]]),
            y=np.concatenate([vo_th[reg_start:], np.full(len(vs_th)-reg_start, 0)]),
            fill="toself", fillcolor="rgba(74,222,128,0.05)",
            line=dict(color="rgba(0,0,0,0)"), name="Regulation Zone",
            showlegend=True
        ))

    # Theoretical curve
    fig.add_trace(go.Scatter(
        x=vs_th, y=vo_th,
        mode="lines", name="Theoretical Vo vs Vs",
        line=dict(color="#06b6d4", width=2.5)
    ))

    # Vz reference line
    fig.add_trace(go.Scatter(
        x=[0, 30], y=[vz, vz], mode="lines",
        name=f"Vz = {vz:.1f} V",
        line=dict(color="#facc15", width=1.5, dash="dash")
    ))

    # Logged data
    zdf = st.session_state["zener_data"]
    if not zdf.empty:
        fig.add_trace(go.Scatter(
            x=zdf["V_s (V)"], y=zdf["V_o (V)"],
            mode="markers", name="Logged Data Points",
            marker=dict(color="#4ade80", size=11, symbol="diamond",
                        line=dict(color="#ffffff", width=1.5))
        ))

    # Current operating point
    fig.add_trace(go.Scatter(
        x=[vs], y=[vo], mode="markers",
        name=f"Current Q-point ({vs:.1f}V → {vo:.3f}V)",
        marker=dict(color="#f0a060", size=14, symbol="star",
                    line=dict(color="#ffffff", width=1.5))
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#020818",
        plot_bgcolor="#060d1f",
        height=450, margin=dict(l=10,r=10,t=30,b=10),
        xaxis=dict(title="Input Supply Voltage Vs (V)",
                   gridcolor="#0f1f3a", zeroline=True, zerolinecolor="#1e3a5f",
                   title_font=dict(color="#06b6d4")),
        yaxis=dict(title="Output Voltage Vo (V)",
                   gridcolor="#0f1f3a", zeroline=True, zerolinecolor="#1e3a5f",
                   title_font=dict(color="#06b6d4")),
        font=dict(family="Nunito", color="#7dd3fc", size=11),
        legend=dict(orientation="h", y=-0.22, bgcolor="rgba(0,0,0,0)",
                    bordercolor="#5c2800", borderwidth=1)
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Data Table & Export ───────────────────────────────────────────────────
    st.markdown('<p class="sec">Logged Data Table</p>', unsafe_allow_html=True)
    col_t, col_e = st.columns([2, 1])
    with col_t:
        if not zdf.empty:
            st.dataframe(zdf, use_container_width=True, hide_index=True)
        else:
            st.markdown('<div class="amber-box">No data logged yet. Set Vs in the sidebar and click Log Data.</div>',
                        unsafe_allow_html=True)
    with col_e:
        if not zdf.empty:
            st.download_button("⬇️ Export Data CSV", zdf.to_csv(index=False),
                               "zener_regulation_data.csv", "text/csv")
            # computed metrics table
            st.markdown(f"""
            <div class="info-box" style="margin-top:10px;">
            <strong>Current Operating Point</strong><br>
            Vs = {vs:.2f} V<br>
            Vo = {vo:.3f} V<br>
            Is = {is_val*1000:.3f} mA<br>
            IL = {il_val*1000:.3f} mA<br>
            Iz = {iz_val*1000:.3f} mA<br>
            Pz = {pz_val*1000:.3f} mW<br>
            Status = <strong style="color:{'#4ade80' if is_reg else '#f0a060'}">
            {'REGULATING' if is_reg else 'UNREGULATED'}</strong>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — EXERCISE & SCORING
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<p class="sec">Practical Exercises — 5 Questions</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
    Answer all <strong>5 questions</strong> below. Each question carries <strong>20 marks</strong>.
    Select your answers and click <strong>Submit</strong> — your score, grade, and full answer
    review will appear immediately.
    </div>""", unsafe_allow_html=True)
    st.markdown("")

    QUESTIONS = [
        {
            "q": "1. In what bias condition must a Zener diode be connected to function as a voltage regulator?",
            "opts": [
                "A — Forward bias, using the knee voltage (~0.7 V) as the reference",
                "B — Reverse bias, operating in the controlled Zener/avalanche breakdown region",
                "C — Alternating bias, switching between forward and reverse each half-cycle",
                "D — Zero bias, relying on the built-in junction potential only"
            ],
            "ans": "B — Reverse bias, operating in the controlled Zener/avalanche breakdown region",
            "exp": "A Zener diode regulates voltage only in reverse breakdown. Forward biased, it behaves like any ordinary diode (~0.7 V drop) and provides no useful regulation."
        },
        {
            "q": "2. What is the primary purpose of the series resistor Rs in the Zener shunt stabilizer circuit?",
            "opts": [
                "A — To increase the output voltage above Vz",
                "B — To block AC components from reaching the load",
                "C — To drop the excess voltage (Vs − Vz) and limit current through the Zener to a safe level",
                "D — To filter ripple by forming an RC low-pass network with the Zener"
            ],
            "ans": "C — To drop the excess voltage (Vs − Vz) and limit current through the Zener to a safe level",
            "exp": "Rs absorbs the voltage difference between the supply and the regulated output (Vs − Vz) and limits current to prevent the Zener from exceeding its maximum power rating Pz(max)."
        },
        {
            "q": "3. When the input supply voltage Vs is below the Zener breakdown voltage Vz, what is the output voltage Vo?",
            "opts": [
                "A — Vo = Vz (the Zener clamps immediately at any input voltage)",
                "B — Vo = 0 V (the Zener acts as a perfect short to ground)",
                "C — Vo = Vs × RL / (Rs + RL) — a simple resistive voltage divider output",
                "D — Vo = Vs − 0.7 V (forward diode drop subtracted)"
            ],
            "ans": "C — Vo = Vs × RL / (Rs + RL) — a simple resistive voltage divider output",
            "exp": "When Vs < Vz, the Zener is reverse biased but not yet in breakdown — it acts as an open circuit. The Rs–RL network forms a voltage divider and Vo = Vs × RL/(Rs + RL), which is less than Vz."
        },
        {
            "q": "4. If the load resistor RL is disconnected (open circuit) while the circuit is regulating, what happens to the Zener current Iz?",
            "opts": [
                "A — Iz drops to zero because there is no complete circuit",
                "B — Iz increases — it must now carry the full series current Is that was previously shared with RL",
                "C — Iz stays exactly the same regardless of load changes",
                "D — Iz becomes negative, reversing current direction through the Zener"
            ],
            "ans": "B — Iz increases — it must now carry the full series current Is that was previously shared with RL",
            "exp": "With RL open, IL = 0. All the series current Is = (Vs − Vz)/Rs flows through the Zener. This is the worst-case condition for Zener power dissipation: Pz = Vz × Is. Rs must be chosen to keep Is below Iz(max)."
        },
        {
            "q": "5. What does the 'flat plateau' region on a Vo vs Vs regulation characteristic curve indicate?",
            "opts": [
                "A — The circuit has failed and Vo is stuck at a fixed value regardless of physics",
                "B — The Zener diode is in forward conduction and the voltage equals Vf",
                "C — Effective voltage regulation — the Zener is in breakdown and clamping Vo ≈ Vz despite rising Vs",
                "D — The load resistor has burned out and is no longer drawing current"
            ],
            "ans": "C — Effective voltage regulation — the Zener is in breakdown and clamping Vo ≈ Vz despite rising Vs",
            "exp": "The flat plateau is the regulated region. As Vs increases above Vz, the extra voltage is dropped across Rs while the Zener keeps Vo ≈ Vz. The slight positive slope in practice is due to the finite Zener dynamic resistance rz."
        },
    ]

    if st.session_state["quiz_submitted"]:
        sc   = st.session_state["quiz_score"]
        grade = "A" if sc >= 80 else "B" if sc >= 65 else "C" if sc >= 50 else "F"
        cls  = "score-pass" if sc >= 60 else "score-mid" if sc >= 40 else "score-fail"
        msg  = ("🏆 Excellent! You have a strong command of Zener stabilizer theory." if sc == 100
                else "✅ Good work! Solid understanding demonstrated." if sc >= 60
                else "📘 Fair attempt. Review the Theory tab and the regulation curve carefully." if sc >= 40
                else "⚠️  Below pass mark. Re-read the Theory tab and repeat the simulation.")

        st.markdown(f"""
        <div class="{cls}">
          <div style="font-size:1.6rem;font-weight:800;">
            Score: {sc} / 100 &nbsp;&nbsp; Grade: {grade}
          </div>
          <div style="margin-top:8px;font-size:.95rem;">{msg}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("")

        # Score bar
        fig_sc = go.Figure(go.Bar(
            x=[sc], y=["Score"], orientation="h",
            marker_color="#4ade80" if sc >= 60 else "#f0a060" if sc >= 40 else "#f87171",
            text=[f"{sc} / 100"], textposition="outside"
        ))
        fig_sc.add_shape(type="line", x0=60, x1=60, y0=-0.5, y1=0.5,
                         line=dict(color="#facc15", dash="dash", width=2))
        fig_sc.update_layout(
            template="plotly_dark", paper_bgcolor="#020818", plot_bgcolor="#060d1f",
            height=110, margin=dict(l=10,r=50,t=10,b=10),
            xaxis=dict(range=[0,115], gridcolor="#0f1f3a",
                       title_font=dict(color="#06b6d4")),
            yaxis=dict(showticklabels=False),
            font=dict(family="Nunito", color="#c4956a", size=12),
            showlegend=False,
            annotations=[dict(x=60, y=0.6, text="Pass (60%)", showarrow=False,
                              font=dict(color="#facc15", size=10))]
        )
        st.plotly_chart(fig_sc, use_container_width=True)

        # Answer review
        st.markdown('<p class="sec">Answer Review</p>', unsafe_allow_html=True)
        for i, q in enumerate(QUESTIONS, 1):
            ua  = st.session_state.get(f"zq{i}_ans", "—")
            ok  = ua == q["ans"]
            icon= "✅" if ok else "❌"
            bg  = "#081a05" if ok else "#1a0800"
            bdr = "#4ade80" if ok else "#f0a060"
            st.markdown(f"""
            <div style="background:{bg};border:1px solid {bdr};border-radius:10px;
                        padding:15px 18px;margin-bottom:12px;">
              <div style="font-weight:800;color:#f0dcc0;margin-bottom:8px;">
                {icon} Q{i}. {q['q']}
              </div>
              <div style="font-size:.83rem;color:#c4956a;line-height:1.65;">
                <strong style="color:#f0dcc0;">Your answer:</strong> {ua}<br>
                <strong style="color:#4ade80;">Correct answer:</strong> {q['ans']}<br>
                <em style="color:#8b6040;">{q['exp']}</em>
              </div>
            </div>""", unsafe_allow_html=True)

        if st.button("🔄 Retake Exercise"):
            st.session_state["quiz_submitted"] = False
            st.session_state["quiz_score"]     = 0
            for i in range(1, 6):
                st.session_state.pop(f"zq{i}_ans", None)
            st.rerun()

    else:
        with st.form("zener_exercise"):
            responses = {}
            for i, q in enumerate(QUESTIONS, 1):
                st.markdown(f"""
                <div style="background:#1e0e04;border:1px solid #5c2800;border-radius:12px;
                            padding:18px 22px;margin-bottom:16px;
                            box-shadow:0 2px 10px rgba(0,0,0,0.5);">
                  <div style="font-weight:800;color:#f0a060;font-size:.92rem;margin-bottom:12px;">
                    {q['q']}
                  </div>
                </div>""", unsafe_allow_html=True)
                responses[i] = st.radio(
                    label=f"zq{i}",
                    options=q["opts"],
                    key=f"zform_q{i}",
                    label_visibility="collapsed"
                )
                st.markdown("")

            if st.form_submit_button("SUBMIT AND WAIT FOR YOUR SCORE",
                                     use_container_width=True):
                score = 0
                for i, q in enumerate(QUESTIONS, 1):
                    ans = responses[i]
                    st.session_state[f"zq{i}_ans"] = ans
                    if ans == q["ans"]:
                        score += 20
                st.session_state["quiz_score"]     = score
                st.session_state["quiz_submitted"] = True
                log_action(st.session_state["student_id"], "Quiz_Submitted", f"Score={score}/100")
                st.rerun()

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("---")
col_f1, col_f2 = st.columns([2, 1])
with col_f1:
    st.caption(f"🛡️ Zener Diode Stabilizer Lab · Student: `{st.session_state['student_id']}` · "
               f"Points: {len(st.session_state['zener_data'])} · "
               f"Rs={rs:.0f}Ω · RL={rl:.0f}Ω · Vz={vz:.1f}V")
with col_f2:
    if os.path.isfile(LOG_FILE):
        with open(LOG_FILE, "rb") as f:
            st.download_button("⬇️ Download Session Log", f,
                               "zener_lab_log.csv", "text/csv")
