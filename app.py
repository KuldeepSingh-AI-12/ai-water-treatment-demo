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

/* Stepper buttons keep light colour */
[data-testid="stSidebar"] .stNumberInput button {
    color: #1E5053 !important;
    background: rgba(255,255,255,0.85) !important;
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

.footer { background:linear-gradient(90deg, var(--teal-dark), var(--teal-mid)); border-radius:12px;
    padding:20px 28px; margin-top:40px; display:flex; align-items:center; justify-content:space-between; }
.footer-left { font-family:'Plus Jakarta Sans',sans-serif; font-size:1.1rem; font-weight:700; color:#fff; }
.footer-right { font-family:'Nunito Sans',sans-serif; font-size:0.8rem; color:rgba(255,255,255,0.65); text-align:right; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Stream Parameters")
    flowrate        = st.number_input("Flowrate (m³/h)", min_value=0.1, value=10.0)
    initial_ph      = st.number_input("Initial pH", min_value=0.0, max_value=14.0, value=4.0)
    target_final_ph = st.number_input("Target final pH before IEX", min_value=0.0, max_value=14.0, value=7.0)

    st.markdown("### 🎯 Treatment Objective")
    main_goal       = st.selectbox("Main treatment objective", [
        "Clean sodium sulfate solution / IEX polishing",
        "Wastewater polishing only",
        "Ni/Co/Mn hydroxide precursor recovery",
        "Ni/Co/Mn carbonate precursor recovery"
    ])
    preferred_base  = st.selectbox("Preferred base for pH increase", ["NaOH", "Lime / Ca(OH)₂", "Na₂CO₃"])
    preferred_acid  = st.selectbox("Preferred acid for pH decrease", ["H₂SO₄", "HCl"])

    st.markdown("### 🧪 Dissolved Species (mg/L)")
    li = st.number_input("Lithium, Li",   min_value=0.0, value=500.0)
    ni = st.number_input("Nickel, Ni",    min_value=0.0, value=2.0)
    co = st.number_input("Cobalt, Co",    min_value=0.0, value=1.0)
    mn = st.number_input("Manganese, Mn", min_value=0.0, value=5.0)
    cu = st.number_input("Copper, Cu",    min_value=0.0, value=0.5)
    fe = st.number_input("Iron, Fe",      min_value=0.0, value=1.0)
    al = st.number_input("Aluminium, Al", min_value=0.0, value=1.0)
    ca = st.number_input("Calcium, Ca",   min_value=0.0, value=50.0)
    mg = st.number_input("Magnesium, Mg", min_value=0.0, value=20.0)

    st.markdown("### 💧 Other Parameters")
    sulfate          = st.number_input("Sulfate, SO₄ (mg/L)",     min_value=0.0, value=50000.0)
    suspended_solids = st.number_input("Suspended solids (mg/L)", min_value=0.0, value=20.0)

    st.markdown("### 💰 Cost Estimation (Lang Method)")
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
st.markdown("""
<div class="hero-banner">
  <div class="hero-title">💧 Water Treatment Concept Tool</div>
  <div class="hero-subtitle">Sodium sulfate stream · Pretreatment screening · Early-stage concept development</div>
  <span class="hero-badge">Adven Internal Demo</span>
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
    "📊 Results Overview",
    "⚗️ Process Train",
    "💰 CAPEX / OPEX",
    "🧴 Chemical Consumption",
    "📄 Summary Report"
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
st.markdown("""
<div class="footer">
  <div class="footer-left">💧 Adven</div>
  <div class="footer-right">
    Water Treatment Concept Tool · Internal Demo<br>
    Not for design decisions · Educational use only
  </div>
</div>
""", unsafe_allow_html=True)
