import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Cr(VI) Treatment Selector",
    layout="wide"
)

st.title("Cr(VI) Treatment Selection Demo")

st.write(
    "A simple rule-based screening tool for hypothetical hexavalent chromium "
    "Cr(VI) removal from industrial water."
)

st.info(
    "This is a preliminary educational demo only. Final design requires full water "
    "chemistry, supplier confirmation, safety review, and lab or pilot testing."
)

# -----------------------------
# Sidebar inputs
# -----------------------------

st.sidebar.header("Input water data")

flowrate = st.sidebar.number_input("Flowrate (m³/h)", min_value=0.1, value=5.0)

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

ph = st.sidebar.number_input("pH", min_value=0.0, max_value=14.0, value=7.0)

sulfate = st.sidebar.number_input(
    "Sulfate concentration (mg/L)",
    min_value=0.0,
    value=100.0
)

cod = st.sidebar.number_input("COD (mg/L)", min_value=0.0, value=20.0)

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

# -----------------------------
# Rule-based treatment logic
# -----------------------------

def select_treatment(cr_in, cr_out, ph, sulfate, cod):
    if cr_in <= 0:
        return (
            "No Cr(VI) treatment required",
            "No Cr(VI) is present in the inlet water.",
            0
        )

    removal_percent = max(0, (cr_in - cr_out) / cr_in * 100)

    if cr_in > 50 or ph < 2:
        treatment = "Chemical reduction + Cr(III) hydroxide precipitation"
        reason = (
            "The Cr(VI) concentration is very high or the water is very acidic. "
            "In this case, chemical reduction of Cr(VI) to Cr(III), followed by "
            "hydroxide precipitation, is usually preferred for bulk removal."
        )

    elif cod > 200:
        treatment = "Organic pre-treatment + ion exchange polishing"
        reason = (
            "COD is high. Organic compounds may foul ion exchange resin, so an "
            "organic removal or pre-treatment step should be considered before polishing."
        )

    elif sulfate > 2000:
        treatment = "Competing anion control + ion exchange polishing"
        reason = (
            "Sulfate concentration is high. Sulfate may compete with chromate/dichromate "
            "on anion exchange resin and reduce effective resin capacity."
        )

    elif ph < 4:
        treatment = "Chemical reduction followed by polishing"
        reason = (
            "The water is acidic. At lower pH, Cr(VI) speciation and resin performance "
            "should be carefully evaluated. Chemical reduction followed by polishing may "
            "be more robust."
        )

    elif ph > 9:
        treatment = "Ion exchange polishing with pH and competing-ion checks"
        reason = (
            "At higher pH, chromate species are generally suitable for anion exchange, "
            "but competing ions and regeneration strategy should be carefully checked."
        )

    elif removal_percent > 90 and cr_in <= 50:
        treatment = "Strong-base anion exchange resin for Cr(VI) polishing"
        reason = (
            "The Cr(VI) concentration is relatively low and the required removal is high. "
            "Cr(VI) commonly exists as oxyanions such as chromate/dichromate, so "
            "strong-base anion exchange is a suitable polishing option."
        )

    elif cr_in < 1:
        treatment = "Adsorption or ion exchange polishing"
        reason = (
            "The inlet Cr(VI) concentration is low. A polishing technology such as "
            "adsorption or ion exchange may be suitable."
        )

    else:
        treatment = "Combined treatment approach"
        reason = (
            "The stream does not clearly fall into one single category. A combined "
            "approach using chemical treatment and polishing may be appropriate."
        )

    return treatment, reason, removal_percent


def alternative_treatment(treatment):
    treatment_lower = treatment.lower()

    if "chemical reduction" in treatment_lower:
        return "Alternative: Ion exchange polishing after chemical reduction and precipitation."

    elif "ion exchange" in treatment_lower:
        return "Alternative: Chemical reduction + precipitation for bulk Cr(VI) removal."

    elif "adsorption" in treatment_lower:
        return "Alternative: Strong-base anion exchange resin for more selective polishing."

    elif "no cr" in treatment_lower:
        return "Alternative: No treatment required unless other contaminants are present."

    else:
        return "Alternative: Combined treatment using chemical reduction followed by polishing."


def decision_drivers(cr_in, cr_out, ph, sulfate, cod):
    drivers = []

    if cr_in > 50:
        drivers.append("High Cr(VI) concentration")
    elif cr_in < 1 and cr_in > 0:
        drivers.append("Low Cr(VI) concentration / polishing case")

    if cr_in > 0:
        removal_percent = max(0, (cr_in - cr_out) / cr_in * 100)
        if removal_percent > 90:
            drivers.append("High removal requirement")

    if cod > 200:
        drivers.append("High COD / organic fouling risk")

    if sulfate > 2000:
        drivers.append("High sulfate / competing anion risk")

    if ph < 2:
        drivers.append("Very acidic pH")
    elif ph < 4:
        drivers.append("Low pH condition")
    elif ph > 10:
        drivers.append("Very high pH")
    elif ph > 9:
        drivers.append("Moderately high pH")

    if not drivers:
        drivers.append("No dominant limiting factor identified")

    return drivers


treatment, reason, removal_percent = select_treatment(
    cr_in,
    cr_out,
    ph,
    sulfate,
    cod
)

alternative = alternative_treatment(treatment)
drivers = decision_drivers(cr_in, cr_out, ph, sulfate, cod)

# -----------------------------
# Calculations
# -----------------------------

cr_removed_kg_h = flowrate * max(0, cr_in - cr_out) / 1000

bv_per_h = flowrate / bed_volume if bed_volume > 0 else 0
ebct_min = 60 / bv_per_h if bv_per_h > 0 else 0

resin_capacity_eq_L = 2.4
theoretical_cr_capacity_g_L = resin_capacity_eq_L * 26
working_capacity_factor = 0.25
working_cr_capacity_g_L = theoretical_cr_capacity_g_L * working_capacity_factor

resin_volume_L = bed_volume * 1000
estimated_cr_capacity_kg = working_cr_capacity_g_L * resin_volume_L / 1000

runtime_h = estimated_cr_capacity_kg / cr_removed_kg_h if cr_removed_kg_h > 0 else 0

# -----------------------------
# Key results
# -----------------------------

st.subheader("Key results")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Removal required", f"{removal_percent:.1f} %")
col2.metric("Cr(VI) removed", f"{cr_removed_kg_h:.3f} kg/h")
col3.metric("Hydraulic loading", f"{bv_per_h:.1f} BV/h")
col4.metric("EBCT", f"{ebct_min:.1f} min")

# -----------------------------
# Treatment recommendation
# -----------------------------

st.subheader("Treatment recommendation")
st.success(treatment)

st.subheader("Why this treatment?")
st.write(reason)

st.subheader("Alternative treatment option")
st.info(alternative)

st.subheader("Key decision drivers")

for driver in drivers:
    st.write(f"- {driver}")

st.subheader("Engineering interpretation")

st.info(
    f"""
Based on the input conditions, the tool selected:

**{treatment}**

This decision is influenced by:
- Cr(VI) concentration
- Required removal efficiency
- pH
- COD / organic fouling risk
- Sulfate / competing anion risk

The tool also suggests:

**{alternative}**
"""
)

# -----------------------------
# Ion exchange design checks
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
    st.warning("Very low pH: chemical reduction is likely preferred before polishing.")
elif ph < 4:
    st.warning("Low pH: Cr(VI) speciation and resin performance should be checked.")
elif ph > 10:
    st.warning("High pH: check competing anions, regeneration strategy, and resin performance.")
elif ph > 9:
    st.warning("Moderately high pH: ion exchange may work, but design checks are important.")
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
    "This capacity calculation is simplified. Actual working capacity depends on water chemistry, "
    "competing ions, resin type, regeneration strategy, and breakthrough criteria."
)

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

Alternative option:
{alternative}

Key decision drivers:
{chr(10).join(["- " + driver for driver in drivers])}

For ion exchange screening, the hydraulic loading is {bv_per_h:.1f} BV/h and the EBCT is {ebct_min:.1f} minutes.

Using a simplified working capacity assumption of {working_cr_capacity_g_L:.1f} g Cr(VI)/L resin, the estimated operating time before regeneration is approximately {runtime_h:.0f} hours.

This is only a screening-level estimate. Final design requires full water chemistry, competing ion analysis, supplier confirmation, safety review, and breakthrough testing.
"""

st.text_area("Result summary", summary, height=360)
