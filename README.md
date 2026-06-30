# Zener Diode Shunt Voltage Stabilizer Simulation Engine & Learning Analytics

An interactive, data-driven virtual laboratory application engineered for Higher National Diploma (HND) Physics with Electronics modules. This platform serves as a software-defined virtual laboratory test bench, enabling students to manually log experimental readings to observe and analyze the structural effects of supply voltage variations on the output voltage stabilization of a Zener diode network.

---

## 📌 Project Overview & Experimental Objective

The primary objective of this experiment is to evaluate how a Zener diode behaves when placed in a parallel (shunt) configuration with a load, specifically under a changing, unregulated DC input source. 

The software-defined interface allows students to modify the operational properties of essential circuit components and record observations down to two decimal places:
1. **Power Supply Unit (PSU):** Variable un-regulated DC input source ($V_s$).
2. **Series Limiting Resistor ($R_s$):** $220\ \Omega$ nominal value used to absorb excess voltage ripples.
3. **Zener Diode ($D_Z$):** The core shunt semiconductor component providing reference clamping.
4. **Load Resistor ($R_L$):** $1\text{ k}\Omega$ ($1000\ \Omega$) terminal execution element.
5. **Digital Voltmeter:** High-impedance monitor recording output stabilization voltage ($V_o$).

---

## 🛠️ Key System Features

* **Interactive Component Tuning:** Allows students to dynamically modify the nominal resistance parameters ($R_s$ and $R_L$) and Zener breakdown limits directly via the sidebar controls.
* **Precise Multi-Decimal Spreadsheet Logger:** Supports custom input logs for PSU Volts ($V_s$) and Output Volts ($V_o$) with rigid 2-decimal point precision tracking.
* **Continuous Regulation Characteristics Plot:** Maps the transition from the linear unregulated tracking zone to the stabilized breakdown plateau on a unified, dark-themed Plotly canvas.
* **Post-Lab Regulation Assessment Form:** Integrates a 5-question automated viva-voce grading system testing structural circuit deductions.
* **Decoupled Telemetry Pipeline:** Records all workspace activities, parameters, and assessment metrics chronologically to a local `student_analytics_log.csv` file for instructor auditing.

---

## 📐 Circuit Design Layout

The interactive workbench displays and implements the following shunt regulator configuration layout:

```text
    Unregulated DC PSU                   Series Resistor Rs
         (V_s) ───────────────────────────[ 220 Ω Nominal ]───────────┬──────────────┐
                                                                       │              │
                                                                     ┌─┴─┐          ┌─┴─┐
                                                                     └───┘          │   │
                                                                   Zener Diode      │1K │ Load Resistor
                                                                     (D_Z)          │   │  R_L
                                                                     ▲ V_Z          │   │
                                                                     └───┘          └─┬─┘
                                                                       │              │
         GND (0V) ─────────────────────────────────────────────────────┴──────────────┴────── (V_o)
                                                                                      Digital Voltmeter
