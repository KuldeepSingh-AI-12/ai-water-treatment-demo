import streamlit as st
import pandas as pd
import math

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Adven | Water Treatment Concept Tool",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="💧"
)

# ─────────────────────────────────────────────
# ADVEN BRAND COLOURS & GLOBAL CSS
# Primary dark teal  : #1E5053
# Medium teal        : #0F6E69
# Warm orange accent : #FF5F15
# Light warm grey    : #E8E2D9
# Soft warm grey     : #EFEAE4
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Nunito+Sans:wght@300;400;500;600&display=swap');

:root {
    --teal-dark:   #1E5053;
    --teal-mid:    #0F6E69;
    --teal-light:  #1a8c86;
    --orange:      #FF5F15;
    --warm-grey:   #E8E2D9;
    --soft-grey:   #EFEAE4;
    --text-dark:   #1a1a1a;
    --text-muted:  #5c5c5c;
}

.stApp {
    background: linear-gradient(135deg, #EFEAE4 0%, #f7f4ef 50%, #E8E2D9 100%);
    font-family: 'Nunito Sans', sans-serif;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--teal-dark) 0%, var(--teal-mid) 60%, #0a5550 100%);
    border-right: 3px solid var(--orange);
}
[data-testid="stSidebar"] * { color: #e8f5f4 !important; font-family: 'Nunito Sans', sans-serif !important; }

/* Input fields: white background with dark text so values are readable */
[data-testid="stSidebar"] .stNumberInput input,
[data-testid="stSidebar"] .stNumberInput input:focus,
[data-testid="stSidebar"] input[type="number"] {
    background: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.4) !important;
    color: #1a1a1a !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
}

/* Selectbox: white background with dark text */
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.4) !important;
    color: #1a1a1a !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="select"] div {
    color: #1a1a1a !important;
}

/* Stepper +/- buttons — solid white bg, dark icon, hover orange */
[data-testid="stSidebar"] .stNumberInput button,
[data-testid="stSidebar"] [data-testid="stNumberInputStepDown"],
[data-testid="stSidebar"] [data-testid="stNumberInputStepUp"],
[data-testid="stSidebar"] .stNumberInput [data-testid="baseButton-minimal"] {
    background: #ffffff !important;
    color: #1E5053 !important;
    border: 1px solid #b0c4c4 !important;
    border-radius: 4px !important;
    opacity: 1 !important;
    min-width: 28px !important;
    font-weight: 700 !important;
}
[data-testid="stSidebar"] .stNumberInput button:hover,
[data-testid="stSidebar"] [data-testid="stNumberInputStepDown"]:hover,
[data-testid="stSidebar"] [data-testid="stNumberInputStepUp"]:hover {
    background: #FF5F15 !important;
    color: #ffffff !important;
    border-color: #FF5F15 !important;
}
[data-testid="stSidebar"] .stNumberInput button svg,
[data-testid="stSidebar"] .stNumberInput button p {
    color: #1E5053 !important;
    fill: #1E5053 !important;
    stroke: #1E5053 !important;
}

h1, h2, h3 { font-family: 'Plus Jakarta Sans', sans-serif !important; color: var(--teal-dark) !important; }

.hero-banner {
    background: linear-gradient(135deg, var(--teal-dark) 0%, var(--teal-mid) 55%, var(--teal-light) 100%);
    border-radius: 16px; padding: 36px 40px; margin-bottom: 28px;
    position: relative; overflow: hidden;
    box-shadow: 0 8px 32px rgba(30,80,83,0.25);
}
.hero-banner::before {
    content:''; position:absolute; top:-60px; right:-60px;
    width:260px; height:260px; border-radius:50%;
    background:rgba(255,95,21,0.15);
}
.hero-title { font-family:'Plus Jakarta Sans',sans-serif; font-size:2.1rem; font-weight:800; color:#ffffff !important; margin:0 0 6px 0; }
.hero-subtitle { font-family:'Nunito Sans',sans-serif; font-size:1.05rem; color:rgba(255,255,255,0.80); margin:0 0 12px 0; }
.hero-badge { display:inline-block; background:var(--orange); color:#fff !important; font-family:'Plus Jakarta Sans',sans-serif;
    font-size:0.72rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase;
    padding:4px 12px; border-radius:20px; }

.section-header { font-family:'Plus Jakarta Sans',sans-serif; font-size:1.15rem; font-weight:700; color:var(--teal-dark) !important;
    border-left:4px solid var(--orange); padding-left:12px; margin:28px 0 14px 0; letter-spacing:0.01em; }

.metric-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:24px; }
.metric-card { background:#fff; border-radius:12px; padding:18px 20px; border-top:4px solid var(--teal-mid);
    box-shadow:0 2px 12px rgba(30,80,83,0.08); }
.metric-card.accent { border-top-color:var(--orange); }
.metric-label { font-family:'Nunito Sans',sans-serif; font-size:0.75rem; font-weight:500; color:var(--text-muted);
    text-transform:uppercase; letter-spacing:0.06em; margin-bottom:6px; }
.metric-value { font-family:'Plus Jakarta Sans',sans-serif; font-size:1.55rem; font-weight:700; color:var(--teal-dark); line-height:1; }
.metric-sub { font-size:0.78rem; color:var(--text-muted); margin-top:4px; }

.result-card { background:#fff; border-radius:12px; padding:20px 24px; margin-bottom:16px;
    box-shadow:0 2px 10px rgba(30,80,83,0.07); border-left:5px solid var(--teal-mid); }
.result-card.orange { border-left-color:var(--orange); }

.process-flow { display:flex; flex-direction:column; gap:8px; margin:12px 0; }
.process-step { display:flex; align-items:flex-start; gap:12px; background:#fff; border-radius:10px;
    padding:12px 16px; box-shadow:0 1px 6px rgba(30,80,83,0.06); }
.step-num { background:var(--teal-mid); color:#fff; font-family:'Plus Jakarta Sans',sans-serif; font-weight:700;
    font-size:0.8rem; min-width:28px; height:28px; border-radius:50%;
    display:flex; align-items:center; justify-content:center; flex-shrink:0; margin-top:1px; }
.step-text { font-family:'Nunito Sans',sans-serif; font-size:0.9rem; color:var(--text-dark); line-height:1.45; }

.iex-gauge-wrap { display:flex; align-items:center; gap:16px; background:#fff; border-radius:12px;
    padding:20px 24px; box-shadow:0 2px 10px rgba(30,80,83,0.07); margin-bottom:14px; }
.iex-score-big { font-family:'Plus Jakarta Sans',sans-serif; font-size:3rem; font-weight:800; color:var(--teal-dark); line-height:1; min-width:80px; }
.iex-bar-bg { background:var(--warm-grey); border-radius:999px; height:14px; overflow:hidden; margin-bottom:6px; }
.iex-bar-fill { height:100%; border-radius:999px; }

.driver-list { display:flex; flex-wrap:wrap; gap:8px; margin-top:8px; }
.driver-chip { background:var(--soft-grey); border:1px solid var(--warm-grey); color:var(--teal-dark);
    font-family:'Nunito Sans',sans-serif; font-size:0.82rem; padding:5px 12px; border-radius:20px; line-height:1.3; }

.cost-grid { display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-bottom:8px; }
.cost-card { background:#fff; border-radius:12px; padding:18px 20px; box-shadow:0 2px 10px rgba(30,80,83,0.07); }
.cost-title { font-family:'Plus Jakarta Sans',sans-serif; font-size:0.78rem; font-weight:700; color:var(--text-muted);
    text-transform:uppercase; letter-spacing:0.07em; margin-bottom:8px; }
.cost-value { font-family:'Plus Jakarta Sans',sans-serif; font-size:1.6rem; font-weight:700; color:var(--teal-dark); }
.cost-unit { font-size:0.8rem; color:var(--text-muted); margin-left:4px; }
.cost-note { font-size:0.75rem; color:var(--text-muted); margin-top:4px; font-style:italic; }

.custom-warning { background:rgba(255,95,21,0.08); border-left:4px solid var(--orange); border-radius:8px;
    padding:12px 16px; font-family:'Nunito Sans',sans-serif; font-size:0.88rem; color:#7a2e00; margin-bottom:10px; }
.custom-disclaimer { background:rgba(30,80,83,0.07); border:1px solid rgba(30,80,83,0.2); border-radius:10px;
    padding:14px 18px; font-size:0.82rem; color:var(--text-muted); margin-bottom:24px; line-height:1.55; }

[data-testid="stDataFrame"] { border-radius:10px !important; overflow:hidden; box-shadow:0 2px 10px rgba(30,80,83,0.07) !important; }

[data-baseweb="tab-list"] { background:var(--warm-grey) !important; border-radius:10px !important; padding:4px !important; gap:4px !important; }
[data-baseweb="tab"] { border-radius:7px !important; font-family:'Nunito Sans',sans-serif !important; font-weight:500 !important; }
[aria-selected="true"] { background:var(--teal-mid) !important; color:#fff !important; }

textarea { font-family:'Nunito Sans',sans-serif !important; font-size:0.87rem !important; border-radius:8px !important; }

/* Dropdown caret — make visible in sidebar */
[data-testid="stSidebar"] [data-baseweb="select"] svg,
[data-testid="stSidebar"] .stSelectbox svg {
    fill: #1E5053 !important;
    color: #1E5053 !important;
    opacity: 1 !important;
}

/* Sidebar logo area */
.sidebar-logo-wrap {
    padding: 20px 16px 12px 16px;
    border-bottom: 1px solid rgba(255,255,255,0.15);
    margin-bottom: 8px;
}
.sidebar-logo-wrap img { width: 120px; }

.footer { background:linear-gradient(90deg, var(--teal-dark), var(--teal-mid)); border-radius:12px;
    padding:22px 32px; margin-top:40px; display:flex; align-items:center; justify-content:space-between; }
.footer-logo img { width: 110px; filter: brightness(0) invert(1); opacity: 0.92; }
.footer-right { font-family:'Nunito Sans',sans-serif; font-size:0.8rem; color:rgba(255,255,255,0.65); text-align:right; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f'<div class="sidebar-logo-wrap"><img src="data:image/png;base64,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" alt="Adven"></div>',
        unsafe_allow_html=True
    )
    st.markdown("### Stream Parameters")
    flowrate        = st.number_input("Flowrate (m³/h)", min_value=0.1, value=10.0)
    initial_ph      = st.number_input("Initial pH", min_value=0.0, max_value=14.0, value=4.0)
    target_final_ph = st.number_input("Target final pH before IEX", min_value=0.0, max_value=14.0, value=7.0)

    st.markdown("### Treatment Objective")
    main_goal       = st.selectbox("Main treatment objective", [
        "Clean sodium sulfate solution / IEX polishing",
        "Wastewater polishing only",
        "Ni/Co/Mn hydroxide precursor recovery",
        "Ni/Co/Mn carbonate precursor recovery"
    ])
    preferred_base  = st.selectbox("Preferred base for pH increase", ["NaOH", "Lime / Ca(OH)₂", "Na₂CO₃"])
    preferred_acid  = st.selectbox("Preferred acid for pH decrease", ["H₂SO₄", "HCl"])

    st.markdown("### Dissolved Species (mg/L)")
    li = st.number_input("Lithium, Li",   min_value=0.0, value=500.0)
    ni = st.number_input("Nickel, Ni",    min_value=0.0, value=2.0)
    co = st.number_input("Cobalt, Co",    min_value=0.0, value=1.0)
    mn = st.number_input("Manganese, Mn", min_value=0.0, value=5.0)
    cu = st.number_input("Copper, Cu",    min_value=0.0, value=0.5)
    fe = st.number_input("Iron, Fe",      min_value=0.0, value=1.0)
    al = st.number_input("Aluminium, Al", min_value=0.0, value=1.0)
    ca = st.number_input("Calcium, Ca",   min_value=0.0, value=50.0)
    mg = st.number_input("Magnesium, Mg", min_value=0.0, value=20.0)

    st.markdown("### Other Parameters")
    sulfate          = st.number_input("Sulfate, SO₄ (mg/L)",     min_value=0.0, value=50000.0)
    suspended_solids = st.number_input("Suspended solids (mg/L)", min_value=0.0, value=20.0)

    st.markdown("### Cost Estimation (Lang Method)")
    equipment_cost_keur  = st.number_input("Major equipment cost (k€)", min_value=0.0, value=500.0,
        help="Purchased equipment cost as starting point for Lang factor CAPEX estimation")
    energy_price_eur_kwh = st.number_input("Energy price (€/kWh)", min_value=0.0, value=0.12)
    chemical_unit_cost   = st.number_input("Chemical cost (€/kg avg)", min_value=0.0, value=0.50)

    st.markdown("---")
    st.markdown('<span style="font-size:0.75rem;color:rgba(255,255,255,0.45);">Adven Water Treatment Concept Tool · Internal Demo</span>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
metals = {"Li": li, "Ni": ni, "Co": co, "Mn": mn,
          "Cu": cu, "Fe": fe, "Al": al, "Ca": ca, "Mg": mg}
heavy_metals_total = ni + co + mn + cu + fe + al
hardness_total     = ca + mg


# ─────────────────────────────────────────────
# RULE FUNCTIONS
# ─────────────────────────────────────────────
def metal_level_category(hmt):
    if hmt < 5: return "Low residual metals"
    elif hmt < 100: return "Moderate metals"
    else: return "High metals"

def estimate_stage_removal(metal, stage):
    if stage == "low_pH":
        if metal in ["Fe", "Al", "Cu"]: return 0.70
        return 0.05
    if stage == "high_pH":
        if metal in ["Ni", "Co"]: return 0.85
        if metal == "Mn": return 0.55
        if metal in ["Fe", "Al", "Cu"]: return 0.25
        if metal == "Mg": return 0.35
        if metal == "Ca": return 0.10
        return 0.02
    if stage == "iex":
        if metal in ["Ni", "Co", "Cu", "Fe", "Al"]: return 0.90
        if metal == "Mn": return 0.75
        if metal in ["Ca", "Mg"]: return 0.70
        if metal == "Li": return 0.02
        return 0.0
    return 0.0

def multistage_removal(concentration, metal):
    r = concentration
    r_low  = r * estimate_stage_removal(metal, "low_pH");  r -= r_low
    r_high = r * estimate_stage_removal(metal, "high_pH"); r -= r_high
    r_iex  = r * estimate_stage_removal(metal, "iex");     r -= r_iex
    return r_low, r_high, r_iex, r

def ph_adjustment_strategy(ip, tfp, pbase, pacid):
    steps = []
    if ip < 5:
        steps.append(f"Initial pH is acidic — use controlled {pbase} dosing for staged precipitation.")
    elif ip > 10:
        steps.append(f"Initial pH is high — use controlled {pacid} dosing before IEX if needed.")
    else:
        steps.append("Initial pH is moderate — fine adjustment may be sufficient before polishing.")
    if tfp < 6 or tfp > 9:
        steps.append("Target final pH is outside typical IEX window — check resin supplier recommendations.")
    else:
        steps.append("Target final pH is suitable for polishing, subject to resin confirmation.")
    return steps

def select_treatment_goal(mg_, level, s, ss):
    if mg_ == "Clean sodium sulfate solution / IEX polishing":
        t = "Multistage precipitation + filtration + chelating IEX polishing"
        r = ("Goal is a clean sodium sulfate-rich solution. Bulk solids and precipitated metals should be removed "
             "before final chelating IEX polishing.")
    elif mg_ == "Wastewater polishing only":
        t = "pH precipitation + solid-liquid separation + optional IEX"
        r = "Goal is residual metal reduction. Precipitation for bulk removal; IEX to polish residual metals."
    elif mg_ == "Ni/Co/Mn hydroxide precursor recovery":
        t = "Impurity removal + Ni/Co/Mn hydroxide co-precipitation"
        r = "Objective is Ni/Co/Mn hydroxide precursor recovery. Impurity control before co-precipitation is essential."
    else:
        t = "Impurity removal + Ni/Co/Mn carbonate co-precipitation"
        r = "Objective is Ni/Co/Mn carbonate precursor recovery. Carbonate precipitation and pH control are critical."
    if level == "Low residual metals":
        r += " Residual metals are low, so IEX polishing is more relevant than aggressive bulk precipitation."
    if s > 30000:
        r += " Sulfate-rich matrix — sodium sulfate management is the main downstream consideration."
    if ss > 10:
        r += " Suspended solids should be removed before IEX to reduce fouling/pressure drop."
    return t, r

def process_train(mg_, ip, tfp, pbase, pacid):
    base_steps = [
        "Feed equalization tank",
        "Bag / cartridge filtration — remove large suspended solids",
        "Stage 1 pH adjustment — early precipitation of Fe, Al, Cu",
        "Stage 1 solid-liquid separation / sludge removal",
        "Stage 2 pH adjustment — Ni, Co, Mn precipitation",
        "Coagulation / flocculation (in-situ or ex-situ) if fine particles remain",
        "Clarification / lamella settling / filter press",
        "Sand filter / multimedia filter / cartridge filter to protect IEX",
        "Final pH balancing before ion exchange polishing",
        "Chelating ion exchange resin polishing",
        "Clean sodium sulfate-rich product solution"
    ]
    if mg_ == "Ni/Co/Mn hydroxide precursor recovery":
        base_steps.insert(5, "Controlled NaOH addition — Ni/Co/Mn hydroxide precursor formation")
    if mg_ == "Ni/Co/Mn carbonate precursor recovery":
        base_steps.insert(5, "Controlled Na₂CO₃ addition — Ni/Co/Mn carbonate precursor formation")
    if ip > tfp:
        base_steps.append(f"Use {pacid} carefully if pH reduction is required before IEX.")
    elif ip < tfp:
        base_steps.append(f"Use {pbase} carefully if pH increase is needed for precipitation.")
    return base_steps

def decision_drivers(mg_, mets, s, ss, ip, tfp):
    drivers = []
    if mets["Ni"]+mets["Co"]+mets["Mn"] < 10 and mg_ == "Clean sodium sulfate solution / IEX polishing":
        drivers.append("Residual transition metals low — polishing more important than bulk precipitation")
    if mets["Fe"]+mets["Al"]+mets["Cu"] > 2:
        drivers.append("Fe/Al/Cu can precipitate early and form fine solids")
    if mets["Ni"]+mets["Co"]+mets["Mn"] > 20:
        drivers.append("Ni/Co/Mn require higher-pH precipitation before polishing")
    if hardness_total > 100:
        drivers.append("Ca/Mg may load chelating resin and reduce polishing capacity")
    if s > 30000:
        drivers.append("Sodium sulfate-rich matrix — keep in solution through treatment")
    if ss > 10:
        drivers.append("Suspended solids can foul IEX — filtration before resin is critical")
    if tfp < 6 or tfp > 9:
        drivers.append("Final pH needs adjustment before IEX polishing")
    if not drivers:
        drivers.append("No dominant limiting factor identified")
    return drivers

def iex_suitability(tfp, ss, ht, hmt):
    score = 100; comments = []
    if tfp < 6 or tfp > 9: score -= 25; comments.append("pH should be adjusted before IEX polishing.")
    if ss > 10:             score -= 25; comments.append("Solids carryover too high — improve filtration before resin.")
    if ht > 300:            score -= 20; comments.append("High Ca/Mg may consume chelating resin capacity.")
    if hmt > 100:           score -= 20; comments.append("Metals are high — use precipitation first, not direct IEX.")
    if score >= 80:   status = "Good candidate for IEX polishing"
    elif score >= 50: status = "Possible, but pre-treatment should be improved"
    else:             status = "Not ideal for direct IEX — improve precipitation/filtration first"
    if not comments:
        comments.append("Conditions look reasonable for polishing-level IEX screening.")
    return score, status, comments


# ─────────────────────────────────────────────
# LANG METHOD CAPEX / OPEX
# ─────────────────────────────────────────────
def lang_capex_opex(equip_keur, flow_m3h, pbase, chem_unit, energy_eur_kwh):
    lang_factor   = 4.7
    capex_keur    = equip_keur * lang_factor
    op_hours      = 8000
    base_dose     = 2.0 if pbase == "Lime / Ca(OH)₂" else (0.55 if pbase == "Na₂CO₃" else 1.2)
    chem_kg_yr    = base_dose * flow_m3h * op_hours
    chem_cost     = chem_kg_yr * chem_unit / 1000
    energy_kwh_yr = 0.15 * flow_m3h * op_hours
    energy_cost   = energy_kwh_yr * energy_eur_kwh / 1000
    labour_maint  = capex_keur * 0.05
    opex_keur_yr  = chem_cost + energy_cost + labour_maint
    opex_eur_m3   = (opex_keur_yr * 1000) / (flow_m3h * op_hours) if flow_m3h > 0 else 0
    return {
        "capex_keur": round(capex_keur, 0),
        "opex_keur_yr": round(opex_keur_yr, 1),
        "opex_eur_m3": round(opex_eur_m3, 3),
        "chem_cost_keur_yr": round(chem_cost, 1),
        "energy_cost_keur_yr": round(energy_cost, 1),
        "labour_maint_keur_yr": round(labour_maint, 1),
        "lang_factor": lang_factor
    }


# ─────────────────────────────────────────────
# CHEMICAL CONSUMPTION
# ─────────────────────────────────────────────
def chemical_consumption(flow, ip, tfp, pbase, pacid, ss):
    ph_delta = tfp - ip
    results  = {}
    if ph_delta > 0:
        factor = 0.45 if pbase == "Lime / Ca(OH)₂" else (0.55 if pbase == "Na₂CO₃" else 0.35)
        kg_m3  = factor * abs(ph_delta)
        results["base"] = {"reagent": pbase, "kg_per_m3": round(kg_m3,3),
            "kg_per_h": round(kg_m3*flow,2), "t_per_yr": round(kg_m3*flow*8000/1000,1)}
    elif ph_delta < 0:
        factor = 0.28 if pacid == "H₂SO₄" else 0.32
        kg_m3  = factor * abs(ph_delta)
        results["acid"] = {"reagent": pacid, "kg_per_m3": round(kg_m3,3),
            "kg_per_h": round(kg_m3*flow,2), "t_per_yr": round(kg_m3*flow*8000/1000,1)}
    if ss > 10:
        floc = 0.020 + ss * 0.0002
        results["flocculant"] = {"reagent": "Polymer flocculant (indicative)", "kg_per_m3": round(floc,4),
            "kg_per_h": round(floc*flow,3), "t_per_yr": round(floc*flow*8000/1000,2)}
    return results


# ─────────────────────────────────────────────
# COMPUTE
# ─────────────────────────────────────────────
level        = metal_level_category(heavy_metals_total)
treatment, reason = select_treatment_goal(main_goal, level, sulfate, suspended_solids)
steps        = process_train(main_goal, initial_ph, target_final_ph, preferred_base, preferred_acid)
drivers      = decision_drivers(main_goal, metals, sulfate, suspended_solids, initial_ph, target_final_ph)
ph_strategy  = ph_adjustment_strategy(initial_ph, target_final_ph, preferred_base, preferred_acid)
iex_score, iex_status, iex_comments = iex_suitability(target_final_ph, suspended_solids, hardness_total, heavy_metals_total)
lang_est     = lang_capex_opex(equipment_cost_keur, flowrate, preferred_base, chemical_unit_cost, energy_price_eur_kwh)
chem_est     = chemical_consumption(flowrate, initial_ph, target_final_ph, preferred_base, preferred_acid, suspended_solids)

results = []; total_removed_kg_h = 0; total_remaining_metals = 0
for metal, conc in metals.items():
    r_low, r_high, r_iex, remaining = multistage_removal(conc, metal)
    total_removed  = r_low + r_high + r_iex
    removed_kg_h   = flowrate * total_removed / 1000
    total_removed_kg_h    += removed_kg_h
    total_remaining_metals += remaining
    results.append({
        "Species": metal, "Inlet (mg/L)": round(conc,3),
        "Stage 1 low-pH (mg/L)": round(r_low,3),
        "Stage 2 high-pH (mg/L)": round(r_high,3),
        "IEX polishing (mg/L)": round(r_iex,3),
        "Final remaining (mg/L)": round(remaining,4),
        "Load removed (kg/h)": round(removed_kg_h,4)
    })
df_results       = pd.DataFrame(results)
ph_change_index  = abs(target_final_ph - initial_ph) * flowrate

warnings_list = []
if suspended_solids > 10: warnings_list.append("Solids carryover may foul IEX resin. Improve bag/sand/cartridge filtration.")
if hardness_total > 300:  warnings_list.append("High Ca/Mg can consume chelating resin capacity and reduce run length.")
if ni + co + mn > 100:    warnings_list.append("Ni/Co/Mn not just polishing-level — bulk precipitation should be prioritised.")
if sulfate > 50000:       warnings_list.append("Very high sulfate: may need downstream concentration/crystallisation for reuse.")
if target_final_ph < 6 or target_final_ph > 9: warnings_list.append("Final pH should be balanced before IEX — consult resin supplier guidance.")
if preferred_base == "Lime / Ca(OH)₂": warnings_list.append("Lime may lower chemical cost but adds Ca load and increases sludge/scaling risk.")
if preferred_acid == "HCl": warnings_list.append("HCl introduces chloride — for Na₂SO₄ product purity, H₂SO₄ may be preferred.")


# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero-banner">
  <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:16px;">
    <div>
      <div class="hero-title">Water Treatment Concept Tool</div>
      <div class="hero-subtitle">Sodium sulfate stream &nbsp;·&nbsp; Pretreatment screening &nbsp;·&nbsp; Early-stage concept development</div>
      <span class="hero-badge">Internal Demo</span>
    </div>
    <div style="flex-shrink:0;">
      <img src="data:image/png;base64,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" style="height:52px;filter:brightness(0) invert(1);opacity:0.92;" alt="Adven">
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="custom-disclaimer">
⚠️ <strong>Disclaimer:</strong> Hypothetical educational tool only — not based on real project, company data, or confidential information.
Do not use for design decisions. For expert consultation: <strong>Dr. Kuldeep Singh</strong> — <em>kuldeeep.singh@adven.com</em>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Results Overview",
    "Process Train",
    "CAPEX / OPEX",
    "Chemical Consumption",
    "Summary Report"
])


# ══════════════════════════════════════════════
# TAB 1
# ══════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">Key Screening Metrics</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="metric-grid">
      <div class="metric-card">
        <div class="metric-label">Metal Level</div>
        <div class="metric-value" style="font-size:1.2rem;">{level}</div>
        <div class="metric-sub">{heavy_metals_total:.1f} mg/L heavy metals</div>
      </div>
      <div class="metric-card accent">
        <div class="metric-label">IEX Suitability Score</div>
        <div class="metric-value">{iex_score}<span style="font-size:1rem;color:#888;">/100</span></div>
        <div class="metric-sub">Polishing readiness</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Metal Load Removed</div>
        <div class="metric-value">{total_removed_kg_h:.2f}</div>
        <div class="metric-sub">kg/h across all stages</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">pH Adjustment Index</div>
        <div class="metric-value">{ph_change_index:.1f}</div>
        <div class="metric-sub">|ΔpH| × flowrate</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.markdown('<div class="section-header">Recommended Treatment Concept</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="result-card orange">
          <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.05rem;font-weight:700;color:#c44000;margin-bottom:8px;">{treatment}</div>
          <div style="font-size:0.88rem;color:#555;line-height:1.55;">{reason}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">pH Adjustment Strategy</div>', unsafe_allow_html=True)
        for s_ in ph_strategy:
            st.markdown(f'<div class="result-card" style="padding:12px 16px;margin-bottom:8px;"><div style="font-size:0.88rem;color:#333;">🔬 {s_}</div></div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="section-header">IEX Polishing Readiness</div>', unsafe_allow_html=True)
        bar_col = "#0F6E69" if iex_score >= 80 else ("#FF5F15" if iex_score >= 50 else "#cc2200")
        st.markdown(f"""
        <div class="iex-gauge-wrap">
          <div class="iex-score-big" style="color:{bar_col};">{iex_score}</div>
          <div style="flex:1;">
            <div style="font-family:'Nunito Sans';font-size:0.82rem;color:#555;margin-bottom:6px;">{iex_status}</div>
            <div class="iex-bar-bg"><div class="iex-bar-fill" style="width:{iex_score}%;background:{bar_col};"></div></div>
            <div style="font-size:0.75rem;color:#888;">{iex_score}/100</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        for c_ in iex_comments:
            st.markdown(f'<div class="result-card" style="padding:10px 14px;margin-bottom:6px;font-size:0.85rem;">{c_}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-header">Key Decision Drivers</div>', unsafe_allow_html=True)
        chips = '<div class="driver-list">' + "".join([f'<span class="driver-chip">{d}</span>' for d in drivers]) + '</div>'
        st.markdown(chips, unsafe_allow_html=True)

    if warnings_list:
        st.markdown('<div class="section-header">⚠️ Risk Comments</div>', unsafe_allow_html=True)
        for w in warnings_list:
            st.markdown(f'<div class="custom-warning">⚠️ {w}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Estimated Staged Metal Removal</div>', unsafe_allow_html=True)
    st.dataframe(df_results, use_container_width=True, hide_index=True)
    st.markdown(f'<div style="font-size:0.82rem;color:#555;margin-top:4px;"><b>Total load removed:</b> {total_removed_kg_h:.3f} kg/h &nbsp;|&nbsp; <b>Remaining dissolved metals:</b> {total_remaining_metals:.3f} mg/L</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 2
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">Suggested Process Train</div>', unsafe_allow_html=True)
    flow_html = '<div class="process-flow">'
    for i, step in enumerate(steps, 1):
        nc = "#FF5F15" if i == len(steps) else "#0F6E69"
        flow_html += f'<div class="process-step"><div class="step-num" style="background:{nc};">{i}</div><div class="step-text">{step}</div></div>'
    flow_html += '</div>'
    st.markdown(flow_html, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Input Parameter Summary</div>', unsafe_allow_html=True)
    df_input = pd.DataFrame({
        "Parameter": ["Flowrate","Initial pH","Target final pH","Main objective","Preferred base","Preferred acid",
                      "Li","Ni","Co","Mn","Cu","Fe","Al","Ca","Mg","Sulfate","Suspended solids"],
        "Value":     [flowrate,initial_ph,target_final_ph,main_goal,preferred_base,preferred_acid,
                      li,ni,co,mn,cu,fe,al,ca,mg,sulfate,suspended_solids],
        "Unit":      ["m³/h","-","-","-","-","-",
                      "mg/L","mg/L","mg/L","mg/L","mg/L","mg/L","mg/L","mg/L","mg/L","mg/L as SO₄","mg/L"]
    })
    st.dataframe(df_input, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════
# TAB 3
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">CAPEX Estimation — Lang Factor Method</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:0.85rem;color:#555;margin-bottom:18px;line-height:1.6;">
    The <b>Lang factor method</b> estimates total installed plant cost by multiplying purchased major equipment cost
    by a factor covering piping, instrumentation, civil works, electrical, engineering, and contingency.
    For a fluid/mixed-process water treatment plant the Lang factor is <b>{lang_est["lang_factor"]}</b>.
    <br><em>CAPEX = {equipment_cost_keur:.0f} k€ × {lang_est["lang_factor"]} = <b>{lang_est["capex_keur"]:.0f} k€</b></em>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="cost-grid">
      <div class="cost-card" style="border-top:4px solid #1E5053;">
        <div class="cost-title">Estimated CAPEX</div>
        <div class="cost-value">{lang_est["capex_keur"]:,.0f}<span class="cost-unit">k€</span></div>
        <div class="cost-note">Lang factor {lang_est["lang_factor"]} · equipment cost {equipment_cost_keur:.0f} k€</div>
      </div>
      <div class="cost-card" style="border-top:4px solid #FF5F15;">
        <div class="cost-title">Estimated Annual OPEX</div>
        <div class="cost-value">{lang_est["opex_keur_yr"]:,.1f}<span class="cost-unit">k€/yr</span></div>
        <div class="cost-note">{lang_est["opex_eur_m3"]:.3f} €/m³ treated · 8,000 h/yr basis</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">OPEX Breakdown</div>', unsafe_allow_html=True)
    opex_df = pd.DataFrame({
        "Cost Item":  ["Chemicals (base/acid)", "Energy (pump + aeration)", "Labour + Maintenance (5% CAPEX/yr)", "Total OPEX"],
        "k€/yr":      [lang_est["chem_cost_keur_yr"], lang_est["energy_cost_keur_yr"],
                       lang_est["labour_maint_keur_yr"], lang_est["opex_keur_yr"]]
    })
    st.dataframe(opex_df, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="custom-disclaimer" style="margin-top:16px;">
    📌 <strong>Methodology note:</strong> Class 5 order-of-magnitude estimates (±50–100% accuracy).
    For early-stage screening only. A proper Class 3/2 estimate requires vendor quotations, site data, and detailed design.
    Based on Lang/Chilton approach — see Peters, Timmerhaus & West, <em>Plant Design and Economics for Chemical Engineers</em>.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">Chemical Consumption Estimates</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.85rem;color:#555;margin-bottom:16px;line-height:1.6;">Indicative dosing rates based on pH adjustment target and suspended solids. <b>Confirm by jar testing before design.</b></div>', unsafe_allow_html=True)

    if not chem_est:
        st.markdown('<div class="result-card">No significant pH adjustment or chemical addition required for current inputs.</div>', unsafe_allow_html=True)
    else:
        for key, val in chem_est.items():
            icon = "🧪" if key == "base" else ("⚗️" if key == "acid" else "🌀")
            st.markdown(f"""
            <div class="result-card {'orange' if key == 'acid' else ''}">
              <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1rem;font-weight:700;color:#1E5053;margin-bottom:10px;">{icon} {val['reagent']}</div>
              <div style="display:flex;gap:32px;flex-wrap:wrap;">
                <div><div class="metric-label">Dose rate</div><div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.3rem;font-weight:700;color:#0F6E69;">{val['kg_per_m3']} <span style="font-size:0.8rem;color:#888;">kg/m³</span></div></div>
                <div><div class="metric-label">Flow rate</div><div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.3rem;font-weight:700;color:#0F6E69;">{val['kg_per_h']} <span style="font-size:0.8rem;color:#888;">kg/h</span></div></div>
                <div><div class="metric-label">Annual</div><div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.3rem;font-weight:700;color:#0F6E69;">{val['t_per_yr']} <span style="font-size:0.8rem;color:#888;">t/yr</span></div></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Metal Removal Overview</div>', unsafe_allow_html=True)
    metals_load = []
    for metal, conc in metals.items():
        r_low, r_high, r_iex, remaining = multistage_removal(conc, metal)
        removal_pct = ((conc - remaining) / conc * 100) if conc > 0 else 0
        metals_load.append({
            "Metal": metal, "Inlet (mg/L)": round(conc,3), "Final (mg/L)": round(remaining,4),
            "Overall removal (%)": round(removal_pct,1),
            "Load inlet (kg/h)": round(conc*flowrate/1000,4),
            "Load outlet (kg/h)": round(remaining*flowrate/1000,5)
        })
    st.dataframe(pd.DataFrame(metals_load), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════
# TAB 5
# ══════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">Concept Summary Report</div>', unsafe_allow_html=True)
    chem_lines = ""
    for key, val in chem_est.items():
        chem_lines += f"  - {val['reagent']}: {val['kg_per_m3']} kg/m³ | {val['kg_per_h']} kg/h | {val['t_per_yr']} t/yr\n"
    if not chem_lines:
        chem_lines = "  No major pH adjustment required with current inputs.\n"

    summary = f"""
════════════════════════════════════════════════════════════════
ADVEN | WATER TREATMENT CONCEPT SCREENING REPORT
════════════════════════════════════════════════════════════════

STREAM: Sodium sulfate-rich effluent (hypothetical)
TOOL:   Early-stage concept screening demo v2

──────────────────────────────────────────────────────────────
1. STREAM INPUTS
──────────────────────────────────────────────────────────────
  Flowrate:            {flowrate} m³/h
  Initial pH:          {initial_ph}
  Target final pH:     {target_final_ph}
  Sulfate:             {sulfate} mg/L as SO₄
  Suspended solids:    {suspended_solids} mg/L
  Objective:           {main_goal}
  Preferred base:      {preferred_base}
  Preferred acid:      {preferred_acid}

  Dissolved metals (mg/L):
  Li={li}  Ni={ni}  Co={co}  Mn={mn}  Cu={cu}
  Fe={fe}  Al={al}  Ca={ca}  Mg={mg}

──────────────────────────────────────────────────────────────
2. TREATMENT RECOMMENDATION
──────────────────────────────────────────────────────────────
  Metal level:         {level}
  Recommended concept: {treatment}
  Rationale:
  {reason}

──────────────────────────────────────────────────────────────
3. SUGGESTED PROCESS TRAIN
──────────────────────────────────────────────────────────────
{chr(10).join([f"  {i}. {s}" for i, s in enumerate(steps, 1)])}

──────────────────────────────────────────────────────────────
4. IEX POLISHING SUITABILITY
──────────────────────────────────────────────────────────────
  Score:    {iex_score}/100
  Status:   {iex_status}
  Comments:
{chr(10).join([f"  - {c}" for c in iex_comments])}

──────────────────────────────────────────────────────────────
5. KEY DECISION DRIVERS
──────────────────────────────────────────────────────────────
{chr(10).join([f"  - {d}" for d in drivers])}

──────────────────────────────────────────────────────────────
6. CHEMICAL CONSUMPTION (INDICATIVE)
──────────────────────────────────────────────────────────────
{chem_lines}
──────────────────────────────────────────────────────────────
7. CAPEX / OPEX ESTIMATE (LANG METHOD — CLASS 5, ±50–100%)
──────────────────────────────────────────────────────────────
  Equipment cost input:  {equipment_cost_keur:.0f} k€
  Lang factor:           {lang_est["lang_factor"]}
  Estimated CAPEX:       {lang_est["capex_keur"]:,.0f} k€
  Estimated OPEX:        {lang_est["opex_keur_yr"]:,.1f} k€/yr
  Specific OPEX:         {lang_est["opex_eur_m3"]:.3f} €/m³  (8,000 h/yr)

──────────────────────────────────────────────────────────────
8. METAL REMOVAL SUMMARY
──────────────────────────────────────────────────────────────
  Total load removed:    {total_removed_kg_h:.3f} kg/h
  Remaining dissolved:   {total_remaining_metals:.3f} mg/L

──────────────────────────────────────────────────────────────
9. RISK NOTES
──────────────────────────────────────────────────────────────
{chr(10).join([f"  ⚠ {w}" for w in warnings_list]) if warnings_list else "  No major risk flags for current inputs."}

──────────────────────────────────────────────────────────────
DISCLAIMER
──────────────────────────────────────────────────────────────
Simplified educational model only. Does not include rigorous
thermodynamics, kinetics, complexation, ionic strength effects,
jar testing data, resin breakthrough curves, or real plant data.
Contact: Dr. Kuldeep Singh — kuldeeep.singh@adven.com
════════════════════════════════════════════════════════════════
"""
    st.text_area("Full Screening Report", summary, height=620)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  <div class="footer-logo">
    <img src="data:image/png;base64,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" alt="Adven">
  </div>
  <div class="footer-right">
    Water Treatment Concept Tool &nbsp;·&nbsp; Internal Demo<br>
    Not for design decisions &nbsp;·&nbsp; Educational use only
  </div>
</div>
""", unsafe_allow_html=True)
