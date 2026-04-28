import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Water Treatment Concept Selector", layout="wide")

st.title("AI Water Treatment Concept Selector")
st.write("A simple demo for industrial wastewater concept screening.")

st.sidebar.header("Input stream data")

flowrate = st.sidebar.number_input("Flowrate (m³/h)", min_value=1.0, value=18.0)
sulfate = st.sidebar.number_input("Sulfate (g/L)", min_value=0.0, value=90.0)
lithium = st.sidebar.number_input("Lithium (g/L)", min_value=0.0, value=10.0)
cod = st.sidebar.number_input("COD (mg/L)", min_value=0.0, value=30.0)
ph = st.sidebar.number_input("pH", min_value=0.0, max_value=14.0, value=7.0)

def recommend_process(sulfate, lithium, cod, ph):
    route = []
    risks = []

    if sulfate > 50:
        route.append("MVR crystallization for sodium sulfate recovery")
    if lithium > 2:
        route.append("Lithium concentration and recovery from mother liquor")
    if sulfate > 20:
        route.append("BPED for acid/base generation from sulfate-rich stream")
    if cod > 100:
        route.insert(0, "Pre-treatment for organics removal")
        risks.append("High COD may affect membranes and crystallization")
    if ph < 3 or ph > 11:
        risks.append("Extreme pH requires material compatibility check")

    if not route:
        route.append("Conventional polishing / ion exchange / RO screening")

    return route, risks

route, risks = recommend_process(sulfate, lithium, cod, ph)

energy_kwh_h = flowrate * sulfate * 0.08
opex_score = energy_kwh_h * 0.08
capex_index = flowrate * (1 + sulfate / 100 + lithium / 20)

col1, col2, col3 = st.columns(3)

col1.metric("Estimated energy", f"{energy_kwh_h:,.0f} kWh/h")
col2.metric("OPEX index", f"{opex_score:,.0f} €/h")
col3.metric("CAPEX complexity index", f"{capex_index:,.1f}")

st.subheader("Recommended treatment concept")

for step in route:
    st.write(f"✅ {step}")

st.subheader("Key risks")

if risks:
    for risk in risks:
        st.warning(risk)
else:
    st.success("No major early-stage risks detected.")

st.subheader("Input summary")

df = pd.DataFrame({
    "Parameter": ["Flowrate", "Sulfate", "Lithium", "COD", "pH"],
    "Value": [flowrate, sulfate, lithium, cod, ph],
    "Unit": ["m³/h", "g/L", "g/L", "mg/L", "-"]
})

st.dataframe(df, use_container_width=True)

st.subheader("LinkedIn summary")

summary = f"""
I built a small AI-style process screening demo for industrial wastewater treatment.

Example case:
- Flowrate: {flowrate} m³/h
- Sulfate: {sulfate} g/L
- Lithium: {lithium} g/L
- COD: {cod} mg/L
- pH: {ph}

The tool suggests:
{chr(10).join(["- " + step for step in route])}

This is an early prototype to explore how AI and data-driven tools can support faster concept development, CAPEX/OPEX screening, and circular water treatment solutions.
"""

st.text_area("Copy this for LinkedIn", summary, height=260)
