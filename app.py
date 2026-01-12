import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def effectiveness_gauge(effectiveness, ntu, c_ratio):
    """
    Streamlit Effectiveness Gauge (ε–NTU)
    effectiveness: percentage (0–100)
    ntu: float
    c_ratio: float
    """

    # Performance classification
    if effectiveness >= 80:
        label = "Excellent"
        color = "green"
    elif effectiveness >= 60:
        label = "Good"
        color = "limegreen"
    elif effectiveness >= 40:
        label = "Fair"
        color = "orange"
    else:
        label = "Poor"
        color = "red"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=effectiveness,
            number={"suffix": "%"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": color},
                "steps": [
                    {"range": [0, 40], "color": "#fee2e2"},
                    {"range": [40, 60], "color": "#fde68a"},
                    {"range": [60, 80], "color": "#bbf7d0"},
                    {"range": [80, 100], "color": "#86efac"},
                ],
                "threshold": {
                    "line": {"color": "black", "width": 3},
                    "thickness": 0.75,
                    "value": effectiveness,
                },
            },
            title={"text": "Heat Exchanger Effectiveness (ε)"},
        )
    )

    fig.update_layout(
        height=320,
        margin=dict(t=50, b=10, l=10, r=10),
    )

    # Display
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    col1.metric("NTU", f"{ntu:.2f}")
    col2.metric("Cmin / Cmax", f"{c_ratio:.3f}")

    st.success(f"Performance Rating: **{label}**")

    st.info(
        """
        **Effectiveness (ε)**  
        Ratio of actual heat transfer to the maximum possible heat transfer.

        ε = Q / Qₘₐₓ

        Higher values indicate better thermal performance of the heat exchanger.
        """
    )

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Heat Exchanger Design Tool",
    layout="wide"
)

st.title("🔥 Heat Exchanger Design Tool")
st.caption("LMTD & ε–NTU based steady-state design calculator")

# -------------------------------------------------
# Sidebar: Flow configuration
# -------------------------------------------------
st.sidebar.header("Flow Configuration")
configuration = st.sidebar.radio(
    "Select Flow Type",
    ["Counterflow", "Parallel Flow"],
    key="flow_type"
)

# -------------------------------------------------
# Input parameters
# -------------------------------------------------
st.subheader("Input Parameters")

col1, col2 = st.columns(2)

# 🔥 Hot fluid
with col1:
    st.markdown("### 🔥 Hot Fluid")
    Th_in = st.number_input(
        "Inlet Temperature (°C)",
        value=150.0,
        key="Th_in"
    )
    Th_out = st.number_input(
        "Outlet Temperature (°C)",
        value=90.0,
        key="Th_out"
    )
    m_hot = st.number_input(
        "Mass Flow Rate (kg/s)",
        value=2.5,
        key="m_hot"
    )
    Cp_hot = st.number_input(
        "Cp (kJ/kg·K)",
        value=4.18,
        key="Cp_hot"
    )

# 💧 Cold fluid
with col2:
    st.markdown("### 💧 Cold Fluid")
    Tc_in = st.number_input(
        "Inlet Temperature (°C)",
        value=25.0,
        key="Tc_in"
    )
    Tc_out = st.number_input(
        "Outlet Temperature (°C)",
        value=70.0,
        key="Tc_out"
    )
    m_cold = st.number_input(
        "Mass Flow Rate (kg/s)",
        value=3.0,
        key="m_cold"
    )
    Cp_cold = st.number_input(
        "Cp (kJ/kg·K)",
        value=4.18,
        key="Cp_cold"
    )

U = st.number_input(
    "Overall Heat Transfer Coefficient U (W/m²·K)",
    value=500.0,
    key="overall_U"
)

# -------------------------------------------------
# Calculations
# -------------------------------------------------
st.subheader("Calculated Results")

# Heat duty (kW)
Q_hot = m_hot * Cp_hot * (Th_in - Th_out)
Q_cold = m_cold * Cp_cold * (Tc_out - Tc_in)
Q_avg = (Q_hot + Q_cold) / 2
Q = Q_avg * 1000  # W

# LMTD
if configuration == "Counterflow":
    dT1 = Th_in - Tc_out
    dT2 = Th_out - Tc_in
else:
    dT1 = Th_in - Tc_in
    dT2 = Th_out - Tc_out

if abs(dT1 - dT2) < 1e-6:
    LMTD = dT1
else:
    LMTD = (dT1 - dT2) / np.log(dT1 / dT2)

# Heat transfer area
A = Q / (U * LMTD)

# Capacity rates
C_hot = m_hot * Cp_hot * 1000
C_cold = m_cold * Cp_cold * 1000
C_min = min(C_hot, C_cold)
C_max = max(C_hot, C_cold)
C_ratio = C_min / C_max

# Effectiveness
Q_max = C_min * (Th_in - Tc_in)
effectiveness = Q / Q_max

# NTU
NTU = (U * A) / C_min

# Heat balance error
heat_balance_error = abs(Q_hot - Q_cold) / Q_avg * 100

st.subheader("Performance Analysis")

effectiveness_gauge(
    effectiveness=effectiveness * 100,
    ntu=NTU,
    c_ratio=C_ratio
)


# -------------------------------------------------
# Display metrics
# -------------------------------------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Heat Duty (kW)", f"{Q/1000:.2f}")
    st.metric("LMTD (°C)", f"{LMTD:.2f}")
    st.metric("Area (m²)", f"{A:.2f}")

with c2:
    st.metric("Effectiveness (%)", f"{effectiveness*100:.1f}")
    st.metric("NTU", f"{NTU:.2f}")
    st.metric("Cmin / Cmax", f"{C_ratio:.3f}")

with c3:
    st.metric("Q_hot (kW)", f"{Q_hot:.2f}")
    st.metric("Q_cold (kW)", f"{Q_cold:.2f}")
    st.metric("Heat Balance Error (%)", f"{heat_balance_error:.1f}")

# -------------------------------------------------
# Temperature profile plot
# -------------------------------------------------
st.subheader("Temperature Profile")

x = np.linspace(0, 1, 50)

if configuration == "Counterflow":
    Th = Th_in - (Th_in - Th_out) * x
    Tc = Tc_out - (Tc_out - Tc_in) * x
else:
    Th = Th_in - (Th_in - Th_out) * x
    Tc = Tc_in + (Tc_out - Tc_in) * x

fig, ax = plt.subplots()
ax.plot(x, Th, label="Hot Fluid", color="red")
ax.plot(x, Tc, label="Cold Fluid", color="blue")
ax.set_xlabel("Exchanger Length (Normalized)")
ax.set_ylabel("Temperature (°C)")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# -------------------------------------------------
# Engineering notes
# -------------------------------------------------
st.info(
    """
    **Assumptions**
    - Steady-state operation  
    - Constant specific heat (Cp)  
    - No phase change  
    - Single-pass heat exchanger  
    - No fouling resistance  

    **Methods Used**
    - LMTD Method  
    - ε–NTU Method
    """
)
