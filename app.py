import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Sodium Sulfate Polishing Demo",
    layout="wide"
)

st.title("Pretreatment DEMO tool for Sodium Sulfate rich effluent stream")

st.warning(
    "Disclaimer: This is a hypothetical educational tool only. "
    "It is not based on any real industrial stream, project, company data, or confidential information. "
    "Do not use it for design decisions. If you need a solution of your effluent then contact our water team expert Dr. Kuldeep Singh (kuldeeep.singh@adven.com)"
)

st.write(
    "A rule-based screening demo for sodium sulfate-rich effluent "
    "Pure hypothetical case for learning perspective."
)

# -----------------------------
# Sidebar inputs
# -----------------------------

st.sidebar.header("Stream data")

flowrate = st.sidebar.number_input("Flowrate (m³/h)", min_value=0.1, value=10.0)

initial_ph = st.sidebar.number_input("Initial pH", min_value=0.0, max_value=14.0, value=4.0)

target_final_ph = st.sidebar.number_input(
    "Target final pH before IEX",
    min_value=0.0,
    max_value=14.0,
    value=7.0
)

main_goal = st.sidebar.selectbox(
    "Main treatment objective",
    [
        "Clean sodium sulfate solution / IEX polishing",
        "Wastewater polishing only",
        "Ni/Co/Mn hydroxide precursor recovery",
        "Ni/Co/Mn carbonate precursor recovery"
    ]
)

preferred_base = st.sidebar.selectbox(
    "Preferred base for pH increase",
    ["NaOH", "Lime / Ca(OH)₂", "Na₂CO₃"]
)

preferred_acid = st.sidebar.selectbox(
    "Preferred acid for pH decrease",
    ["H₂SO₄", "HCl"]
)

st.sidebar.subheader("Dissolved species (mg/L)")

li = st.sidebar.number_input("Lithium, Li (mg/L)", min_value=0.0, value=500.0)
ni = st.sidebar.number_input("Nickel, Ni (mg/L)", min_value=0.0, value=2.0)
co = st.sidebar.number_input("Cobalt, Co (mg/L)", min_value=0.0, value=1.0)
mn = st.sidebar.number_input("Manganese, Mn (mg/L)", min_value=0.0, value=5.0)
cu = st.sidebar.number_input("Copper, Cu (mg/L)", min_value=0.0, value=0.5)
fe = st.sidebar.number_input("Iron, Fe (mg/L)", min_value=0.0, value=1.0)
al = st.sidebar.number_input("Aluminium, Al (mg/L)", min_value=0.0, value=1.0)
ca = st.sidebar.number_input("Calcium, Ca (mg/L)", min_value=0.0, value=50.0)
mg = st.sidebar.number_input("Magnesium, Mg (mg/L)", min_value=0.0, value=20.0)

sulfate = st.sidebar.number_input(
    "Sulfate level (mg/L as SO₄)",
    min_value=0.0,
    value=50000.0
)

suspended_solids = st.sidebar.number_input(
    "Suspended solids / precipitate carryover (mg/L)",
    min_value=0.0,
    value=20.0
)

# -----------------------------
# Data
# -----------------------------

metals = {
    "Li": li,
    "Ni": ni,
    "Co": co,
    "Mn": mn,
    "Cu": cu,
    "Fe": fe,
    "Al": al,
    "Ca": ca,
    "Mg": mg
}

heavy_metals_total = ni + co + mn + cu + fe + al
hardness_total = ca + mg
all_metals_total = sum(metals.values())

# -----------------------------
# Rule functions
# -----------------------------

def metal_level_category(heavy_metals_total):
    if heavy_metals_total < 5:
        return "Low residual metals"
    elif heavy_metals_total < 100:
        return "Moderate metals"
    else:
        return "High metals"


def estimate_stage_removal(metal, stage):
    if stage == "low_pH":
        if metal in ["Fe", "Al", "Cu"]:
            return 0.70
        return 0.05

    if stage == "high_pH":
        if metal in ["Ni", "Co"]:
            return 0.85
        if metal == "Mn":
            return 0.55
        if metal in ["Fe", "Al", "Cu"]:
            return 0.25
        if metal == "Mg":
            return 0.35
        if metal == "Ca":
            return 0.10
        return 0.02

    if stage == "iex":
        if metal in ["Ni", "Co", "Cu", "Fe", "Al"]:
            return 0.90
        if metal == "Mn":
            return 0.75
        if metal in ["Ca", "Mg"]:
            return 0.70
        if metal == "Li":
            return 0.02
        return 0.0

    return 0.0


def multistage_removal(concentration, metal):
    remaining = concentration

    removed_low = remaining * estimate_stage_removal(metal, "low_pH")
    remaining -= removed_low

    removed_high = remaining * estimate_stage_removal(metal, "high_pH")
    remaining -= removed_high

    removed_iex = remaining * estimate_stage_removal(metal, "iex")
    remaining -= removed_iex

    return removed_low, removed_high, removed_iex, remaining


def ph_adjustment_strategy(initial_ph, target_final_ph, preferred_base, preferred_acid):
    steps = []

    if initial_ph < 5:
        steps.append(
            f"Initial pH is acidic. Use controlled {preferred_base} dosing for staged precipitation."
        )
    elif initial_ph > 10:
        steps.append(
            f"Initial pH is high. Use controlled {preferred_acid} dosing to reduce pH before IEX if needed."
        )
    else:
        steps.append(
            "Initial pH is moderate. Fine pH adjustment may be enough before polishing."
        )

    if target_final_ph < 6 or target_final_ph > 9:
        steps.append(
            "Target final pH is outside a conservative IEX polishing window; check resin supplier recommendations."
        )
    else:
        steps.append(
            "Target final pH is suitable for a typical polishing step, subject to resin supplier confirmation."
        )

    return steps


def select_treatment_goal(main_goal, level, sulfate, suspended_solids):
    if main_goal == "Clean sodium sulfate solution / IEX polishing":
        treatment = "Multistage precipitation + filtration + chelating IEX polishing"
        reason = (
            "The goal is a clean sodium sulfate-rich solution. Bulk solids and precipitated metals should be removed "
            "before final chelating ion exchange polishing."
        )

    elif main_goal == "Wastewater polishing only":
        treatment = "pH precipitation + solid-liquid separation + optional IEX"
        reason = (
            "The goal is residual metal reduction. Precipitation handles bulk removal, while IEX can polish remaining metals."
        )

    elif main_goal == "Ni/Co/Mn hydroxide precursor recovery":
        treatment = "Impurity removal + Ni/Co/Mn hydroxide co-precipitation"
        reason = (
            "The objective is recovery of Ni/Co/Mn as hydroxide precursor. Impurity control before co-precipitation is important."
        )

    else:
        treatment = "Impurity removal + Ni/Co/Mn carbonate co-precipitation"
        reason = (
            "The objective is recovery of Ni/Co/Mn as carbonate precursor. Carbonate precipitation and pH control are important."
        )

    if level == "Low residual metals":
        reason += " Since residual metals are low, IEX polishing becomes more relevant than aggressive bulk precipitation."

    if sulfate > 30000:
        reason += " The solution is sulfate-rich, so sodium sulfate management remains the main downstream consideration."

    if suspended_solids > 10:
        reason += " Suspended solids should be removed before IEX to reduce fouling/pressure drop."

    return treatment, reason


def process_train(main_goal, initial_ph, target_final_ph, preferred_base, preferred_acid):
    base_steps = [
        "Feed equalization tank",
        "Bag filtration / cartridge filtration to remove large suspended solids",
        "Stage 1 pH adjustment for early precipitating metals such as Fe, Al and Cu",
        "Stage 1 solid-liquid separation or sludge removal",
        "Stage 2 pH adjustment for Ni, Co and Mn precipitation",
        "Coagulation / flocculation, either in-situ or ex-situ, if fine particles remain",
        "Clarification, lamella settling, filter press or other solid-liquid separation",
        "Sand filter / multimedia filter / cartridge filter to protect the IEX resin",
        "Final pH balancing before ion exchange polishing",
        "Chelating ion exchange resin polishing",
        "Clean sodium sulfate-rich solution"
    ]

    if main_goal == "Ni/Co/Mn hydroxide precursor recovery":
        base_steps.insert(
            5,
            "Controlled NaOH addition for Ni/Co/Mn hydroxide precursor formation"
        )

    if main_goal == "Ni/Co/Mn carbonate precursor recovery":
        base_steps.insert(
            5,
            "Controlled Na₂CO₃ addition for Ni/Co/Mn carbonate precursor formation"
        )

    if initial_ph > target_final_ph:
        base_steps.append(f"Use {preferred_acid} carefully if pH needs to be reduced before IEX.")
    elif initial_ph < target_final_ph:
        base_steps.append(f"Use {preferred_base} carefully if pH needs to be increased for precipitation.")

    return base_steps


def decision_drivers(main_goal, metals, sulfate, suspended_solids, initial_ph, target_final_ph):
    drivers = []

    if ni + co + mn < 10 and main_goal == "Clean sodium sulfate solution / IEX polishing":
        drivers.append("Residual transition metals are low, so polishing is more important than bulk precipitation")

    if metals["Fe"] + metals["Al"] + metals["Cu"] > 2:
        drivers.append("Fe/Al/Cu can precipitate earlier and may form fine solids")

    if metals["Ni"] + metals["Co"] + metals["Mn"] > 20:
        drivers.append("Ni/Co/Mn may require a higher-pH precipitation stage before polishing")

    if hardness_total > 100:
        drivers.append("Ca/Mg may load the chelating resin and reduce polishing capacity")

    if sulfate > 30000:
        drivers.append("Sodium sulfate-rich matrix should remain mostly in solution")

    if suspended_solids > 10:
        drivers.append("Suspended solids can foul IEX; filtration before resin is important")

    if target_final_ph < 6 or target_final_ph > 9:
        drivers.append("Final pH may need adjustment before IEX polishing")

    if not drivers:
        drivers.append("No dominant limiting factor identified")

    return drivers


def iex_suitability(target_final_ph, suspended_solids, hardness_total, heavy_metals_total):
    score = 100
    comments = []

    if target_final_ph < 6 or target_final_ph > 9:
        score -= 25
        comments.append("pH should be adjusted before IEX polishing.")

    if suspended_solids > 10:
        score -= 25
        comments.append("Solids carryover is too high; improve filtration before resin.")

    if hardness_total > 300:
        score -= 20
        comments.append("High Ca/Mg may consume chelating resin capacity.")

    if heavy_metals_total > 100:
        score -= 20
        comments.append("Metals are high; use precipitation first, not direct IEX.")

    if score >= 80:
        status = "Good candidate for IEX polishing"
    elif score >= 50:
        status = "Possible, but pre-treatment should be improved"
    else:
        status = "Not ideal for direct IEX; improve precipitation/filtration first"

    if not comments:
        comments.append("Conditions look reasonable for polishing-level IEX screening.")

    return score, status, comments


# -----------------------------
# Calculations
# -----------------------------

level = metal_level_category(heavy_metals_total)
treatment, reason = select_treatment_goal(main_goal, level, sulfate, suspended_solids)
steps = process_train(main_goal, initial_ph, target_final_ph, preferred_base, preferred_acid)
drivers = decision_drivers(main_goal, metals, sulfate, suspended_solids, initial_ph, target_final_ph)
ph_strategy = ph_adjustment_strategy(initial_ph, target_final_ph, preferred_base, preferred_acid)
iex_score, iex_status, iex_comments = iex_suitability(
    target_final_ph,
    suspended_solids,
    hardness_total,
    heavy_metals_total
)

results = []
total_removed_kg_h = 0
total_remaining_metals = 0

for metal, conc in metals.items():
    removed_low, removed_high, removed_iex, remaining = multistage_removal(conc, metal)

    total_removed = removed_low + removed_high + removed_iex
    removed_kg_h = flowrate * total_removed / 1000

    total_removed_kg_h += removed_kg_h
    total_remaining_metals += remaining

    results.append({
        "Species": metal,
        "Inlet (mg/L)": round(conc, 3),
        "Removed in Stage 1 low-pH precip. (mg/L)": round(removed_low, 3),
        "Removed in Stage 2 high-pH precip. (mg/L)": round(removed_high, 3),
        "Removed by IEX polishing (mg/L)": round(removed_iex, 3),
        "Final remaining (mg/L)": round(remaining, 4),
        "Total removed (kg/h)": round(removed_kg_h, 4)
    })

df_results = pd.DataFrame(results)

ph_change_index = abs(target_final_ph - initial_ph) * flowrate

# -----------------------------
# Dashboard
# -----------------------------

st.subheader("Key screening results")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Metal level", level)
col2.metric("IEX suitability score", f"{iex_score}/100")
col3.metric("Removed load", f"{total_removed_kg_h:.2f} kg/h")
col4.metric("pH adjustment index", f"{ph_change_index:.1f}")

st.subheader("Recommended treatment concept")
st.success(treatment)

st.subheader("Why this route?")
st.write(reason)

st.subheader("pH adjustment strategy")
for item in ph_strategy:
    st.write(f"- {item}")

st.subheader("Suggested process train")
for i, step in enumerate(steps, start=1):
    st.write(f"{i}. {step}")

st.subheader("IEX polishing suitability")
st.info(iex_status)
for comment in iex_comments:
    st.write(f"- {comment}")

st.subheader("Key decision drivers")
for driver in drivers:
    st.write(f"- {driver}")

# -----------------------------
# Removal table
# -----------------------------

st.subheader("Estimated staged metal removal")

st.dataframe(df_results, use_container_width=True)

# -----------------------------
# Warnings / risks
# -----------------------------

st.subheader("Risk comments")

if suspended_solids > 10:
    st.warning("Solids carryover may foul IEX resin. Add or improve bag filtration, sand filtration, or cartridge filtration.")

if hardness_total > 300:
    st.warning("High Ca/Mg can consume chelating resin capacity and may reduce run length.")

if ni + co + mn > 100:
    st.warning("Ni/Co/Mn are not just polishing-level contaminants; bulk precipitation should be prioritized.")

if sulfate > 50000:
    st.warning("Very high sulfate: sodium sulfate remains the main dissolved salt and may need downstream concentration/crystallization depending on reuse target.")

if target_final_ph < 6 or target_final_ph > 9:
    st.warning("Final pH should be balanced before IEX. Check selected resin supplier guidance.")

if preferred_base == "Lime / Ca(OH)₂":
    st.warning("Lime may lower chemical cost but can add Ca load and increase sludge/scaling risk.")

if preferred_acid == "HCl":
    st.warning("HCl may introduce chloride. For sodium sulfate product quality, H₂SO₄ may be preferred if compatible.")

# -----------------------------
# Input summary
# -----------------------------

st.subheader("Input summary")

df_input = pd.DataFrame({
    "Parameter": [
        "Flowrate",
        "Initial pH",
        "Target final pH before IEX",
        "Main goal",
        "Preferred base",
        "Preferred acid",
        "Li",
        "Ni",
        "Co",
        "Mn",
        "Cu",
        "Fe",
        "Al",
        "Ca",
        "Mg",
        "Sulfate",
        "Suspended solids"
    ],
    "Value": [
        flowrate,
        initial_ph,
        target_final_ph,
        main_goal,
        preferred_base,
        preferred_acid,
        li,
        ni,
        co,
        mn,
        cu,
        fe,
        al,
        ca,
        mg,
        sulfate,
        suspended_solids
    ],
    "Unit": [
        "m³/h",
        "-",
        "-",
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
        "mg/L",
        "mg/L",
        "mg/L as SO₄",
        "mg/L"
    ]
})

st.dataframe(df_input, use_container_width=True)

# -----------------------------
# Written summary
# -----------------------------

st.subheader("Simple interpretation")

summary = f"""
This hypothetical sodium sulfate-rich stream contains low to moderate residual metals after upstream battery recycling / black mass treatment.

Main objective:
{main_goal}

Recommended concept:
{treatment}

Reason:
{reason}

Suggested route:
{chr(10).join([str(i) + ". " + step for i, step in enumerate(steps, start=1)])}

IEX suitability:
{iex_status} ({iex_score}/100)

Main decision drivers:
{chr(10).join(["- " + d for d in drivers])}

Estimated total removed metal load:
{total_removed_kg_h:.2f} kg/h

Estimated total remaining dissolved metal concentration after staged treatment:
{total_remaining_metals:.3f} mg/L

Important note:
This is a simplified educational model only. It does not include rigorous thermodynamics, kinetics, complexation, ionic strength effects, actual jar testing data, resin breakthrough curves, or real plant data.
"""

st.text_area("Result summary", summary, height=520)
