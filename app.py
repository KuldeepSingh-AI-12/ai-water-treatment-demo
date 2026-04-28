import streamlit as st
import pandas as pd

# Optional AI feature
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


st.set_page_config(
    page_title="Cr(VI) Treatment Selector",
    layout="wide"
)

st.title("Cr(VI) Treatment Selection Demo")
st.write(
    "A simple rule-based and optional AI-assisted screening tool for hypothetical "
    "hexavalent chromium removal from water."
)

st.info(
    "This is a screening-level educational demo only. Final design requires full water chemistry, "
    "supplier confirmation, and lab/pilot testing."
)


# -----------------------------
# Sidebar inputs
# -----------------------------

st.sidebar.header("Input water data")

flowrate = st.sidebar.number_input(
    "Flowrate (m³/h)",
    min_value=0.1,
    value=5.0
)

cr_in = st.sidebar.number_input(
    "Inlet Cr(VI) concentration (mg/L)",
    min_value=0.0,
    value=1.0
)

cr_out = st.sidebar.number_input(
    "Target outlet Cr(VI) concentration (mg/L)",
    min_value=0.0,
    value=0.05
)

ph = st.sidebar.number_input(
    "pH",
    min_value=0.0,
    max_value=14.0,
    value=7.0
)

sulfate = st.sidebar.number_input(
    "Sulfate concentration (mg/L)",
    min_value=0.0,
    value=100.0
)

cod = st.sidebar.number_input(
    "COD (mg/L)",
    min_value=0.0,
    value=20.0
)

bed_volume = st.sidebar.number_input(
    "Resin bed volume (m³)",
    min_value=0.1,
    value=1.0
)

bed_depth = st.sidebar.number_input(
    "Bed depth (mm)",
    min_value=100.0,
    value=800.0
)

use_ai = st.sidebar.checkbox(
    "Use AI-based recommendation",
    value=False
)


# -----------------------------
# Rule-based logic
# -----------------------------

def select_treatment(cr_in, cr_out, ph, sulfate, cod):
    if cr_in <= 0:
        return (
            "No Cr(VI) treatment required",
            "The inlet Cr(VI) concentration is zero.",
            0
        )

    removal_percent = max(0, (cr_in - cr_out) / cr_in * 100)

    if cr_in > 50:
        treatment = "Chemical reduction + Cr(III) hydroxide precipitation"
        reason = (
            "The Cr(VI) concentration is high. Bulk chemical reduction of Cr(VI) to Cr(III), "
            "followed by hydroxide precipitation, is usually more suitable than direct resin polishing."
        )

    elif cod > 200:
        treatment = "Organic pre-treatment + ion exchange polishing"
        reason = (
            "COD is high, which can increase fouling risk for ion exchange resin. "
            "A pre-treatment step should be considered before resin polishing."
        )

    elif sulfate > 1000:
        treatment = "Competing anion control + ion exchange polishing"
        reason = (
            "Sulfate is high and may compete with chromate/dichromate on anion exchange resin. "
            "The resin system may still work, but capacity and breakthrough behavior must be tested."
        )

    elif ph < 2 or ph > 10:
        treatment = "pH adjustment + chemical treatment or ion exchange polishing"
        reason = (
            "The pH is outside a comfortable preliminary screening range. "
            "pH adjustment may be required before selecting the final Cr(VI) removal method."
        )

    elif removal_percent > 90 and cr_in <= 50:
        treatment = "Strong-base anion exchange resin for Cr(VI) polishing"
        reason = (
            "The Cr(VI) concentration is relatively low and the removal target is high. "
            "Cr(VI) commonly exists as oxyanions such as chromate/dichromate, making strong-base "
            "anion exchange resin a suitable polishing option."
        )

    elif cr_in < 1:
        treatment = "Adsorption or ion exchange polishing"
        reason = (
            "The inlet Cr(VI) concentration is low. A polishing technology such as adsorption "
            "or ion exchange may be suitable."
        )

    else:
        treatment = "Chemical reduction + precipitation followed by polishing"
        reason = (
            "A combined treatment route may be appropriate, especially if the outlet target is strict "
            "or the water contains competing ions."
        )

    return treatment, reason, removal_percent


treatment, reason, removal_percent = select_treatment(
    cr_in,
    cr_out,
    ph,
    sulfate,
    cod
)


# -----------------------------
# Calculations
# -----------------------------

cr_removed_kg_h = flowrate * max(0, cr_in - cr_out) / 1000

bv_per_h = flowrate / bed_volume if bed_volume > 0 else 0
ebct_min = 60 / bv_per_h if bv_per_h > 0 else 0

# Simplified ion exchange capacity estimate
# Approximation: Cr(VI) as chromate, using Cr mass equivalent.
# Cr atomic mass about 52 g/mol, chromate charge 2-, equivalent weight approx. 26 g/eq.
resin_capacity_eq_L = 2.4
theoretical_cr_capacity_g_L = resin_capacity_eq_L * 26
working_capacity_factor = 0.25
working_cr_capacity_g_L = theoretical_cr_capacity_g_L * working_capacity_factor

resin_volume_L = bed_volume * 1000
estimated_cr_capacity_kg = working_cr_capacity_g_L * resin_volume_L / 1000

runtime_h = estimated_cr_capacity_kg / cr_removed_kg_h if cr_removed_kg_h > 0 else 0


# -----------------------------
# Output: key metrics
# -----------------------------

st.subheader("Key results")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Removal required", f"{removal_percent:.1f} %")
col2.metric("Cr(VI) removed", f"{cr_removed_kg_h:.3f} kg/h")
col3.metric("Hydraulic loading", f"{bv_per_h:.1f} BV/h")
col4.metric("EBCT", f"{ebct_min:.1f} min")


# -----------------------------
# Output: treatment selection
# -----------------------------

st.subheader("Rule-based treatment recommendation")
st.success(treatment)

st.subheader("Why this treatment?")
st.write(reason)


# -----------------------------
# Design checks
# -----------------------------

st.subheader("Ion exchange design checks")

if 5 <= bv_per_h <= 30:
    st.success("Hydraulic loading is within the typical 5–30 BV/h screening range.")
else:
    st.warning("Hydraulic loading is outside the typical 5–30 BV/h screening range.")

if bed_depth >= 800:
    st.success("Bed depth meets the 800 mm minimum screening criterion.")
else:
    st.warning("Bed depth is below 800 mm. Consider increasing column height or resin volume.")

if ph < 2:
    st.warning("Very low pH: check Cr(VI) speciation, resin compatibility, and material selection.")
elif ph > 10:
    st.warning("High pH: check competing anions, regeneration strategy, and resin performance.")
else:
    st.success("pH is within a reasonable preliminary screening range.")


# -----------------------------
# Resin estimate
# -----------------------------

st.subheader("Simplified resin loading estimate")

col5, col6 = st.columns(2)

col5.metric(
    "Assumed working capacity",
    f"{working_cr_capacity_g_L:.1f} g Cr(VI)/L resin"
)

col6.metric(
    "Estimated runtime before regeneration",
    f"{runtime_h:.0f} h"
)

st.caption(
    "The resin capacity calculation is simplified. Actual working capacity depends on water chemistry, "
    "competing ions, resin type, regeneration strategy, and breakthrough criteria."
)


# -----------------------------
# Optional AI recommendation
# -----------------------------

def get_ai_recommendation(
    flowrate,
    cr_in,
    cr_out,
    ph,
    sulfate,
    cod,
    treatment,
    reason
):
    if OpenAI is None:
        return "OpenAI package is not installed. Run: pip install openai"

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    prompt = f"""
You are a water treatment process engineer.

Evaluate this hypothetical Cr(VI) removal case.

Input data:
- Flowrate: {flowrate} m3/h
- Inlet Cr(VI): {cr_in} mg/L
- Target outlet Cr(VI): {cr_out} mg/L
- pH: {ph}
- Sulfate: {sulfate} mg/L
- COD: {cod} mg/L

Rule-based recommendation:
{treatment}

Rule-based reason:
{reason}

Compare these options:
1. Strong-base anion exchange resin
2. Chemical reduction of Cr(VI) to Cr(III) followed by precipitation
3. Adsorption polishing
4. Combined treatment

Give a concise engineering recommendation with:
- Recommended treatment route
- Why this route was selected
- Main risks
- Additional data needed before final design

Do not overclaim. State that this is only preliminary screening.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text


if use_ai:
    st.subheader("AI-based treatment recommendation")

    try:
        ai_result = get_ai_recommendation(
            flowrate,
            cr_in,
            cr_out,
            ph,
            sulfate,
            cod,
            treatment,
            reason
        )
        st.write(ai_result)

    except Exception as e:
        st.error("AI recommendation could not be generated.")
        st.write("Most likely reason: missing OpenAI API key in Streamlit secrets.")
        st.code(str(e))


# -----------------------------
# Input summary table
# -----------------------------

st.subheader("Input summary")

df = pd.DataFrame({
    "Parameter": [
        "Flowrate",
        "Inlet Cr(VI)",
        "Target outlet Cr(VI)",
        "pH",
        "Sulfate",
        "COD",
        "Resin bed volume",
        "Bed depth",
        "Hydraulic loading",
        "EBCT"
    ],
    "Value": [
        flowrate,
        cr_in,
        cr_out,
        ph,
        sulfate,
        cod,
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
        "mg/L",
        "mg/L",
        "m³",
        "mm",
        "BV/h",
        "min"
    ]
})

st.dataframe(df, use_container_width=True)


# -----------------------------
# Simple written summary
# -----------------------------

st.subheader("Simple interpretation")

summary = f"""
For this hypothetical Cr(VI) case, the inlet concentration is {cr_in} mg/L and the target outlet concentration is {cr_out} mg/L.

The required removal is approximately {removal_percent:.1f} %, corresponding to {cr_removed_kg_h:.3f} kg/h of Cr(VI) removed.

The rule-based treatment recommendation is:

{treatment}

Reason:
{reason}

For ion exchange screening, the hydraulic loading is {bv_per_h:.1f} BV/h and the EBCT is {ebct_min:.1f} minutes.

Using a simplified working capacity assumption of {working_cr_capacity_g_L:.1f} g Cr(VI)/L resin, the estimated operating time before regeneration is approximately {runtime_h:.0f} hours.

This is only a screening-level estimate. Final design requires full water chemistry, competing ion analysis, supplier confirmation, safety review, and breakthrough testing.
"""

st.text_area("Result summary", summary, height=320)
