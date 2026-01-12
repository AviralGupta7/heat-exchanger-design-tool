#  Heat Exchanger Design Tool (Python + Streamlit)

An interactive **heat exchanger design calculator** built using Python and Streamlit, based on **LMTD and ε–NTU methods** commonly used in undergraduate Chemical Engineering.

##  Features
- Heat duty calculation
- LMTD for parallel and counterflow configurations
- Required heat transfer area estimation
- Effectiveness (ε), NTU, and capacity ratio
- Temperature profile visualization
- Interactive Streamlit interface

##  Engineering Methods Used
- Steady-state energy balance
- Log Mean Temperature Difference (LMTD)
- Effectiveness–NTU (ε–NTU) method

##  Inputs
- Mass flow rates
- Inlet and outlet temperatures
- Specific heat capacities
- Overall heat transfer coefficient
- Flow configuration (parallel / counterflow)

##  Outputs
- Heat duty (kW)
- LMTD (°C)
- Heat transfer area (m²)
- Effectiveness (%)
- NTU and capacity ratio
- Temperature profiles

##  Assumptions
- Steady-state operation
- Constant Cp
- No phase change
- Single-pass heat exchanger
- No fouling resistance

##  How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
You can see the working version of this app on https://heat-exchanger-design.streamlit.app/
