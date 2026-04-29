import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Heavy Metal Precipitation Demo",
    layout="wide"
)

st.title("Black Mass Refinery Heavy Metal Precipitation Demo")

st.write(
    "A simple rule-based screening tool for hypothetical heavy metal removal "
    "from sodium sulfate-rich black mass refinery wastewater."
)

st.warning(
    "Disclaimer: This is a purely hypothetical educational example. "
    "It is not based on any real industrial stream, project, or company data. "
    "Final design requires full water chemistry, laboratory testing, safety review, "
    "and process validation."
)

# -----------------------------
# Sidebar inputs
# -----------------------------

st.sidebar.header("Input stream data")

flowrate = st.sidebar.number_input("Flowrate (m³/h)", min_value=0.1, value=10.0)

initial_ph = st.sidebar.number_input("Initial pH", min_value=0.0, max_value=14.0, value=3.0)

target_ph = st.sidebar.number_input(
    "Target precipitation pH",
    min_value=0.0,
    max_value=14.0,
    value=10.0
)

alkali = st.sidebar.selectbox(
    "Alkali for pH adjustment",
    ["NaOH", "Lime / Ca(OH)₂"]
)

st.sidebar.subheader("Dissolved metals (mg/L)")

ni = st.sidebar.number_input("Nickel, Ni (mg/L)", min_value=0.0, value=100.0)
co = st.sidebar.number_input("Cobalt, Co (mg/L)", min_value=0.0, value=50.0)
mn = st.sidebar.number_input("Manganese, Mn (mg/L)", min_value=0.0, value=200.0)
fe = st.sidebar.number_input("Iron, Fe (mg/L)", min_value=0.0, value=20.0)
al = st.sidebar.number_input("Aluminium, Al (mg/L)", min_value=0.0, value=10.0)
ca = st.sidebar.number_input("Calcium, Ca (mg/L)", min_value=0.0, value=300.0)
mg = st.sidebar.number_input("Magnesium, Mg (mg/L)", min_value=0.0, value=100.0)

sulfate = st.sidebar.number_input(
    "Sodium sulfate / sulfate level (mg/L as SO₄)",
    min_value=0.0,
    value=50000.0
)

# -----------------------------
# Helper calculations
# -----------------------------

metals = {
    "Ni": ni,
    "Co": co,
    "Mn": mn,
    "Fe": fe,
    "Al": al,
    "Ca": ca,
    "Mg": mg
}

def precipitation_status(target_ph):
    status = {}

    if target_ph >= 4:
        status["Fe"] = "Likely precipitates as Fe(OH)₃ / Fe hydroxides"
    else:
        status["Fe"] = "Mostly soluble"

    if target_ph >= 5:
        status["Al"] = "Likely precipitates as Al(OH)₃"
    else:
        status["Al"] = "Mostly soluble"

    if target_ph >= 8.5:
        status["Ni"] = "Likely starts precipitating as Ni(OH)₂"
        status["Co"] = "Likely starts precipitating as Co(OH)₂"
    else:
        status["Ni"] = "May remain partly soluble"
        status["Co"] = "May remain partly soluble"

    if target_ph >= 9.5:
        status["Mn"] = "Likely precipitates more strongly as Mn hydroxide/oxide"
    else:
        status["Mn"] = "May require higher pH or oxidation support"

    if target_ph >= 10:
        status["Mg"] = "May precipitate as Mg(OH)₂ and increase sludge"
    else:
        status["Mg"] = "Mostly remains in solution"

    if target_ph >= 10.5:
        status["Ca"] = "Scaling/sludge risk may increase"
    else:
        status["Ca"] = "Mostly remains in solution, but scaling risk depends on carbonate/sulfate chemistry"

    return status


def estimate_removed_fraction(metal, target_ph):
    if metal == "Fe":
        return 0.95 if target_ph >= 4 else 0.2
    if metal == "Al":
        return 0.95 if target_ph >= 5 else 0.2
    if metal in ["Ni", "Co"]:
        if target_ph >= 10:
            return 0.95
        elif target_ph >= 8.5:
            return 0.75
        else:
            return 0.2
    if metal == "Mn":
        if target_ph >= 10.5:
            return 0.85
        elif target_ph >= 9.5:
            return 0.6
        else:
            return 0.15
    if metal == "Mg":
        return 0.5 if target_ph >= 10 else 0.05
    if metal == "Ca":
        return 0.2 if target_ph >= 10.5 else 0.05
    return 0


def select_treatment(initial_ph, target_ph, sulfate, metals, alkali):
    total_transition_metals = metals["Ni"] + metals["Co"] + metals["Mn"]
    total_impurities = metals["Fe"] + metals["Al"] + metals["Ca"] + metals["Mg"]

    if target_ph < 7:
        treatment = "Partial neutralization / Fe-Al removal step"
        reason = (
            "The target pH is relatively low. This condition is more suitable for removing "
            "Fe and Al hydroxides, while Ni, Co, and Mn may remain largely soluble."
        )

    elif 7 <= target_ph < 9:
        treatment = "Two-stage precipitation recommended"
        reason = (
            "This pH range may remove Fe and Al effectively, but Ni, Co, and Mn may need "
            "a second higher-pH precipitation step."
        )

    elif 9 <= target_ph <= 10.5:
        treatment = "Hydroxide precipitation of Ni/Co/Mn + solid-liquid separation"
        reason = (
            "The selected pH is suitable for bulk hydroxide precipitation of transition metals "
            "such as Ni, Co, and partly Mn."
        )

    else:
        treatment = "High-pH precipitation with scaling/sludge risk"
        reason = (
            "Very high pH may improve some metal removal, but it can increase Mg/Ca precipitation, "
            "scaling, chemical consumption, and sludge production."
        )

    if sulfate > 50000:
        reason += " The sulfate level is high, so the treated water may remain sodium sulfate-rich."

    if alkali == "Lime / Ca(OH)₂":
        reason += " Lime may reduce chemical cost but can increase calcium load and sludge volume."
    else:
        reason += " NaOH gives cleaner sodium-based chemistry but can be more expensive."

    return treatment, reason


status = precipitation_status(target_ph)
treatment, reason = select_treatment(initial_ph, target_ph, sulfate, metals, alkali)

# -----------------------------
# Mass estimates
# -----------------------------

results = []

total_removed_kg_h = 0

for metal, conc in metals.items():
    removed_fraction = estimate_removed_fraction(metal, target_ph)
    removed_mg_l = conc * removed_fraction
    remaining_mg_l = conc - removed_mg_l
    removed_kg_h = flowrate * removed_mg_l / 1000

    total_removed_kg_h += removed_kg_h

    results.append({
        "Metal": metal,
        "Inlet (mg/L)": conc,
        "Estimated removal (%)": removed_fraction * 100,
        "Remaining (mg/L)": remaining_mg_l,
        "Removed (kg/h)": removed_kg_h,
        "Comment": status.get(metal, "")
    })

df_results = pd.DataFrame(results)

# Simple neutralization index
ph_increase = max(0, target_ph - initial_ph)
alkali_index = flowrate * ph_increase

if alkali == "NaOH":
    chemical_comment = "NaOH selected: cleaner sodium chemistry, suitable for sodium sulfate-rich systems."
else:
    chemical_comment = "Lime selected: lower-cost alkali, but may increase Ca-related scaling and sludge."

# -----------------------------
# Key outputs
# -----------------------------

st.subheader("Key screening results")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Target pH", f"{target_ph:.1f}")
col2.metric("pH increase", f"{ph_increase:.1f}")
col3.metric("Estimated metal sludge load", f"{total_removed_kg_h:.2f} kg/h")
col4.metric("Alkali demand index", f"{alkali_index:.1f}")

st.subheader("Recommended treatment route")
st.success(treatment)

st.subheader("Why this route?")
st.write(reason)

st.subheader("Suggested process train")

if target_ph < 7:
    process_train = [
        "Feed equalization",
        "Controlled alkali dosing",
        "Fe/Al hydroxide precipitation",
        "Clarification or filtration",
        "Second-stage pH adjustment if Ni/Co/Mn removal is required",
        "Polishing if needed"
    ]
elif target_ph <= 10.5:
    process_train = [
        "Feed equalization",
        "pH adjustment with selected alkali",
        "Hydroxide precipitation of heavy metals",
        "Coagulation/flocculation if needed",
        "Clarification or filtration",
        "Chelating ion exchange polishing if strict limits are required",
        "Sodium sulfate-rich treated water management"
    ]
else:
    process_train = [
        "Feed equalization",
        "High-pH alkali dosing",
        "Heavy metal + Mg/Ca precipitation",
        "Sludge thickening and filtration",
        "pH correction before discharge/reuse",
        "Polishing step if required"
    ]

for step in process_train:
    st.write(f"- {step}")

# -----------------------------
# Decision drivers
# -----------------------------

st.subheader("Key decision drivers")

drivers = []

if ni + co + mn > 100:
    drivers.append("Significant Ni/Co/Mn load")
if fe + al > 20:
    drivers.append("Fe/Al can support hydroxide precipitation and co-precipitation")
if ca + mg > 300:
    drivers.append("High Ca/Mg may increase scaling or sludge burden")
if sulfate > 30000:
    drivers.append("High sulfate / sodium sulfate-rich matrix")
if target_ph > 10:
    drivers.append("High pH increases Mg/Ca precipitation risk")
if initial_ph < 4:
    drivers.append("Acidic feed requires neutralization")

if not drivers:
    drivers.append("No dominant limiting factor identified")

for driver in drivers:
    st.write(f"- {driver}")

# -----------------------------
# Metal removal table
# -----------------------------

st.subheader("Estimated metal removal")

st.dataframe(df_results, use_container_width=True)

# -----------------------------
# Risk comments
# -----------------------------

st.subheader("Risk comments")

if sulfate > 50000:
    st.warning("Very high sulfate: sodium sulfate remains in solution and may require downstream management.")

if target_ph > 10:
    st.warning("High pH may increase Mg/Ca precipitation, scaling, sludge generation, and alkali consumption.")

if mn > 100 and target_ph < 10:
    st.warning("Manganese may not be fully removed at this pH. Higher pH or oxidation support may be required.")

if ca + mg > 500:
    st.warning("High hardness: consider scaling risk and sludge volume.")

if ni + co > 100 and target_ph < 9:
    st.warning("Ni and Co may need higher pH or polishing to reach strict targets.")

st.info(chemical_comment)

# -----------------------------
# Polishing recommendation
# -----------------------------

st.subheader("Polishing recommendation")

if ni + co + mn > 0:
    st.info(
        "If strict residual metal limits are required, consider a polishing step such as "
        "chelating ion exchange after precipitation and filtration."
    )
else:
    st.write("No transition metals entered; polishing may not be required.")

# -----------------------------
# Input summary
# -----------------------------

st.subheader("Input summary")

df_input = pd.DataFrame({
    "Parameter": [
        "Flowrate",
        "Initial pH",
        "Target precipitation pH",
        "Alkali",
        "Ni",
        "Co",
        "Mn",
        "Fe",
        "Al",
        "Ca",
        "Mg",
        "Sulfate"
    ],
    "Value": [
        flowrate,
        initial_ph,
        target_ph,
        alkali,
        ni,
        co,
        mn,
        fe,
        al,
        ca,
        mg,
        sulfate
    ],
    "Unit": [
        "m³/h",
        "-",
        "-",
        "-",
        "mg/L",
        "mg/L",
        "mg/L",
        "mg/L",
        "mg/L",
        "mg/L",
        "mg/L",
        "mg/L as SO₄"
    ]
})

st.dataframe(df_input, use_container_width=True)

# -----------------------------
# Written summary
# -----------------------------

st.subheader("Simple interpretation")

summary = f"""
This hypothetical black mass refinery wastewater contains dissolved Ni, Co, Mn, Fe, Al, Ca, Mg and sulfate.

The selected treatment concept is:

{treatment}

Reason:
{reason}

The target precipitation pH is {target_ph:.1f}, starting from an initial pH of {initial_ph:.1f}.
The selected alkali is {alkali}.

The estimated removed metal load is approximately {total_removed_kg_h:.2f} kg/h.

Main decision drivers:
{chr(10).join(["- " + d for d in drivers])}

Suggested process train:
{chr(10).join(["- " + step for step in process_train])}

This is a simplified screening-level tool only. It is not based on real industrial data and must not be used for design without laboratory precipitation tests, water chemistry validation, sludge testing, and safety review.
"""

st.text_area("Result summary", summary, height=420)
