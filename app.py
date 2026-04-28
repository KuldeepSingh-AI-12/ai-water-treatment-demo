import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cr(VI) Ion Exchange Demo", layout="wide")

st.title("Cr(VI) Removal by Ion Exchange Resin")
st.write("A simple screening demo for hexavalent chromium removal using strong-base anion exchange resin.")

st.sidebar.header("Input data")

flowrate = st.sidebar.number_input("Flowrate (m³/h)", min_value=0.1, value=5.0)
cr_in = st.sidebar.number_input("Inlet Cr(VI) concentration (mg/L)", min_value=0.0, value=1.0)
cr_out = st.sidebar.number_input("Target outlet Cr(VI) concentration (mg/L)", min_value=0.0, value=0.05)
ph = st.sidebar.number_input("pH", min_value=0.0, max_value=14.0, value=7.0)
bed_volume = st.sidebar.number_input("Resin bed volume (m³)", min_value=0.1, value=1.0)
bed_depth = st.sidebar.number_input("Bed depth (mm)", min_value=100.0, value=800.0)

removal_percent = ((cr_in - cr_out) / cr_in * 100) if cr_in > 0 else 0
cr_removed_kg_h = flowrate * (cr_in - cr_out) / 1000
bv_per_h = flowrate / bed_volume
ebct_min = 60 / bv_per_h if bv_per_h > 0 else 0

# Simplified capacity estimate
# Cr(VI) as chromate: CrO4 2-
# Equivalent weight based on Cr mass approximation: 52 g Cr / 2 eq = 26 g/eq
resin_capacity_eq_L = 2.4
theoretical_cr_capacity_g_L = resin_capacity_eq_L * 26
working_capacity_factor = 0.25
working_cr_capacity_g_L = theoretical_cr_capacity_g_L * working_capacity_factor

resin_volume_L = bed_volume * 1000
estimated_cr_capacity_kg = working_cr_capacity_g_L * resin_volume_L / 1000

runtime_h = estimated_cr_capacity_kg / cr_removed_kg_h if cr_removed_kg_h > 0 else 0

st.subheader("Key results")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Removal required", f"{removal_percent:.1f} %")
col2.metric("Cr(VI) removed", f"{cr_removed_kg_h:.3f} kg/h")
col3.metric("Flow rate", f"{bv_per_h:.1f} BV/h")
col4.metric("EBCT", f"{ebct_min:.1f} min")

st.subheader("Suggested treatment concept")

st.success("Strong-base macroporous anion exchange resin for chromate / Cr(VI) removal")

st.write("""
A suitable first screening concept is a fixed-bed ion exchange column using a strong-base anion exchange resin.
Cr(VI) is typically present as oxyanions such as chromate/dichromate depending on pH, so an anion exchange resin is suitable for removal.
""")

st.subheader("Estimated resin loading")

col5, col6 = st.columns(2)

col5.metric("Assumed working capacity", f"{working_cr_capacity_g_L:.1f} g Cr(VI)/L resin")
col6.metric("Estimated runtime before regeneration", f"{runtime_h:.0f} h")

st.caption("Note: Capacity and runtime are simplified screening values only. Real design needs lab/pilot breakthrough testing.")

st.subheader("Design checks")

if 5 <= bv_per_h <= 30:
    st.success("Flow rate is within the typical 5–30 BV/h operating range.")
else:
    st.warning("Flow rate is outside the typical 5–30 BV/h operating range.")

if bed_depth >= 800:
    st.success("Bed depth meets the minimum 800 mm screening criterion.")
else:
    st.warning("Bed depth is below 800 mm. Increase column height or resin volume.")

if ph < 2:
    st.warning("Very low pH: check Cr(VI) speciation, resin compatibility, and material selection.")
elif ph > 10:
    st.warning("High pH: check competing anions and regeneration strategy.")
else:
    st.success("pH is within a reasonable preliminary screening range.")

st.subheader("Input summary")

df = pd.DataFrame({
    "Parameter": [
        "Flowrate",
        "Inlet Cr(VI)",
        "Target outlet Cr(VI)",
        "pH",
        "Resin bed volume",
        "Bed depth",
        "BV/h",
        "EBCT"
    ],
    "Value": [
        flowrate,
        cr_in,
        cr_out,
        ph,
        bed_volume,
        bed_depth,
        bv_per_h,
        ebct_min
    ],
    "Unit": [
        "m³/h",
        "mg/L",
        "mg/L",
        "-",
        "m³",
        "mm",
        "BV/h",
        "min"
    ]
})

st.dataframe(df, use_container_width=True)

st.subheader("Simple interpretation")

summary = f"""
For this hypothetical Cr(VI) case, the inlet concentration is {cr_in} mg/L and the target outlet concentration is {cr_out} mg/L.

The required removal is approximately {removal_percent:.1f} %, corresponding to {cr_removed_kg_h:.3f} kg/h of Cr(VI) removed.

The selected concept is a fixed-bed strong-base anion exchange resin system for chromate / Cr(VI) removal.

The hydraulic loading is {bv_per_h:.1f} BV/h and the EBCT is {ebct_min:.1f} minutes.

Using a simplified working capacity assumption of {working_cr_capacity_g_L:.1f} g Cr(VI)/L resin, the estimated operating time before regeneration is approximately {runtime_h:.0f} hours.

This is only a screening-level estimate. Final design requires water chemistry review, competing ion analysis, resin supplier confirmation, and breakthrough testing.
"""

st.text_area("Result summary", summary, height=300)
