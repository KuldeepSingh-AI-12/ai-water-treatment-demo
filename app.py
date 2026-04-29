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

[data-baseweb="tab-list"] { background:var(--warm-grey) !important; border-radius:10px !important; padding:6px 8px !important; gap:6px !important; }
[data-baseweb="tab"] {
    border-radius:7px !important;
    font-family:'Nunito Sans',sans-serif !important;
    font-weight:600 !important;
    padding: 8px 20px !important;
    min-width: 130px !important;
    text-align: center !important;
    border: 1px solid transparent !important;
}
[aria-selected="true"] {
    background:var(--teal-mid) !important;
    color:#fff !important;
    border-color: var(--teal-dark) !important;
}
[aria-selected="false"] {
    background: rgba(255,255,255,0.6) !important;
    color: var(--teal-dark) !important;
    border-color: rgba(30,80,83,0.15) !important;
}
[aria-selected="false"]:hover {
    background: #fff !important;
    color: var(--teal-dark) !important;
}

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
.footer-logo img { width: 110px;  }
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
        help="Purchased equipment cost as starting point for CAPEX estimation")
    energy_price_eur_kwh = st.number_input("Energy price (€/kWh)", min_value=0.0, value=0.12)
    chemical_unit_cost   = st.number_input("Chemical cost (€/kg avg)", min_value=0.0, value=0.50)
    cost_method          = st.selectbox("CAPEX method", ["Lang Factor", "Hand-Chilton"],
        help="Lang: simple factor method ±50–100%. Hand-Chilton: equipment-type factors ±30–50%.")

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
    """
    Classify total heavy metal load (Ni+Co+Mn+Cu+Fe+Al).
    Thresholds based on:
    - <1 mg/L: trace level — direct IEX polishing feasible, no bulk precipitation needed
    - 1–10 mg/L: low — light pre-treatment + IEX
    - 10–100 mg/L: moderate — staged precipitation required before IEX
    - >100 mg/L: high — aggressive bulk precipitation mandatory before any polishing step
    Reference: hydroxide precipitation typically achieves 0.5–1.0 mg/L residual (EPA/ITRC guidance)
    """
    if hmt < 1:    return "Trace metals (< 1 mg/L)"
    elif hmt < 10:  return "Low metals (1–10 mg/L)"
    elif hmt < 100: return "Moderate metals (10–100 mg/L)"
    else:           return "High metals (> 100 mg/L)"

def estimate_stage_removal(metal, stage):
    """
    Stage removal efficiencies based on published hydroxide precipitation
    and chelating IEX selectivity data.
    Low-pH stage (pH ~4-5): targets Fe3+, Al3+, Cu2+ (precipitate at lower pH)
    High-pH stage (pH ~9-10): targets Ni2+, Co2+, Mn2+, residual hardness
    IEX (chelating iminodiacetate resin): selectivity Cu>Ni>Co>Fe>Mn>Ca>Mg>>Li/Na
    Source: Purolite S930/S920 data; AmberLite IRC748 technical literature
    """
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

# ── CONCENTRATION-BASED DECISION THRESHOLDS ──────────────────────────
# These drive ALL recommendation logic below.
# Based on: EPA chemical precipitation guidance, ITRC mining waste treatment,
# Purolite/DuPont AmberLite IEX design manuals, hydroxide solubility curves.

THRESH = {
    # Heavy metals (Ni+Co+Mn+Cu+Fe+Al)
    "hmt_trace":        1.0,   # mg/L — below this: no precipitation needed at all
    "hmt_low":         10.0,   # mg/L — below this: light pre-treatment only
    "hmt_bulk":       100.0,   # mg/L — above this: mandatory bulk precipitation

    # Individual metals
    "fe_al_cu_precip":  2.0,   # mg/L — Fe/Al/Cu: worth a low-pH precipitation stage
    "ni_co_mn_precip": 20.0,   # mg/L — Ni/Co/Mn: worth a high-pH precipitation stage
    "ni_co_mn_bulk":  100.0,   # mg/L — Ni/Co/Mn: bulk recovery viable

    # Suspended solids
    "ss_filtration":   10.0,   # mg/L — above this: dedicated filtration before IEX
    "ss_coag":         50.0,   # mg/L — above this: coagulation/flocculation needed

    # Hardness / Ca+Mg softening thresholds
    # Ca precipitates as CaCO3 at pH >9 (Ksp ~3.3e-9) or Ca(OH)2 at pH ~12.4 — lime softening typical
    # Mg precipitates as Mg(OH)2 at pH >10–11 (Ksp ~5.6e-12)
    # Lime softening (Ca(OH)2 addition) removes both: Ca as CaCO3, Mg as Mg(OH)2
    # Reference: Crittenden et al., MWH's Water Treatment, 3rd Ed.
    "hardness_warn":  100.0,   # mg/L Ca+Mg: starts to compete with chelating IEX resin
    "hardness_high":  300.0,   # mg/L Ca+Mg: significant resin capacity penalty — softening warranted
    "ca_precip":      200.0,   # mg/L Ca alone: Ca precipitation as CaCO3 is worth considering (lime/soda ash softening)
    "mg_precip":       50.0,   # mg/L Mg alone: Mg(OH)2 precipitation worth considering at pH 10–11
    "hardness_softening": 400.0,  # mg/L Ca+Mg: dedicated softening stage strongly recommended before IEX

    # Sulfate
    "so4_high":     30000.0,   # mg/L — sulfate-rich classification

    # pH window for IEX
    "iex_ph_low":       6.0,
    "iex_ph_high":      9.0,

    # Lithium recovery thresholds
    # Li2CO3 solubility ~13 g/L at 20°C, decreases with temperature — recovery by Na2CO3 precipitation
    # Market-grade Li2CO3 requires >99.5% purity — upstream Na2SO4 stream is already compatible
    # Typical Li recovery projects viable at >200 mg/L Li in feed
    # At >500 mg/L Li, concentration/crystallisation is economically attractive
    "li_recovery_low":  200.0,   # mg/L Li: Li recovery worth flagging as option
    "li_recovery_high": 400.0,   # mg/L Li: Li recovery strongly recommended (typical project threshold)
}


def ph_adjustment_strategy(ip, tfp, pbase, pacid):
    """pH strategy logic based on initial pH and precipitation requirements."""
    steps = []
    if ip < 3:
        steps.append(f"Strongly acidic feed (pH {ip}) — staged {pbase} addition required; rapid neutralisation risks fine precipitate formation, use slow controlled dosing.")
    elif ip < 5:
        steps.append(f"Acidic feed (pH {ip}) — controlled {pbase} dosing for staged precipitation; Fe/Al/Cu will begin precipitating around pH 4–5.")
    elif ip > 11:
        steps.append(f"Strongly alkaline feed (pH {ip}) — use {pacid} to reduce pH; check for carbonate/hydroxide precipitates already present in feed.")
    elif ip > 9:
        steps.append(f"Alkaline feed (pH {ip}) — {pacid} may be needed before IEX if resin requires neutral pH window.")
    else:
        steps.append(f"Feed pH {ip} is in moderate range — fine pH adjustment to target should be straightforward.")

    if tfp < THRESH["iex_ph_low"] or tfp > THRESH["iex_ph_high"]:
        steps.append(f"Target pH {tfp} is outside the typical IEX operating window (pH 6–9) — consult resin supplier; some resins tolerate pH 4–10 but efficiency drops outside this range.")
    else:
        steps.append(f"Target pH {tfp} is within the suitable IEX operating window (pH 6–9).")
    return steps


def select_treatment_goal(mg_, mets, s, ss, ip, hmt, ht):
    """
    Concentration-aware treatment concept selection.
    Logic tiers:
    1. If all metals essentially zero → simple filtration / pH correction only, check Li/Ca/Mg
    2. If metals trace (<1 mg/L total) → direct IEX polishing, no precipitation
    3. If metals low (1–10 mg/L) → light pre-treatment + IEX
    4. If moderate (10–100 mg/L) → staged precipitation + IEX
    5. If high (>100 mg/L) → aggressive bulk precipitation, IEX optional finishing
    Ca/Mg softening and Li recovery flagged as additional concepts throughout.
    """
    fe_al_cu  = mets["Fe"] + mets["Al"] + mets["Cu"]
    ni_co_mn  = mets["Ni"] + mets["Co"] + mets["Mn"]
    li_conc   = mets["Li"]
    ca_conc   = mets["Ca"]
    mg_conc   = mets["Mg"]
    need_low_ph_precip  = fe_al_cu  > THRESH["fe_al_cu_precip"]
    need_high_ph_precip = ni_co_mn  > THRESH["ni_co_mn_precip"]
    need_bulk_precip    = hmt       > THRESH["hmt_bulk"]
    need_filtration     = ss        > THRESH["ss_filtration"]
    is_sulfate_rich     = s         > THRESH["so4_high"]
    hardness_concern    = ht        > THRESH["hardness_warn"]
    need_softening      = ht        > THRESH["hardness_softening"]
    ca_softening        = ca_conc   > THRESH["ca_precip"]
    mg_softening        = mg_conc   > THRESH["mg_precip"]
    li_recovery_flag    = li_conc   > THRESH["li_recovery_low"]
    li_recovery_strong  = li_conc   > THRESH["li_recovery_high"]
    metals_negligible   = hmt       < 0.5
    metals_trace        = hmt       < THRESH["hmt_trace"]
    metals_low          = hmt       < THRESH["hmt_low"]

    # ── Helper: build Ca/Mg and Li addendum text ──
    def _hardness_addendum():
        notes = []
        if need_softening:
            notes.append(
                f"Ca ({ca_conc:.0f} mg/L) + Mg ({mg_conc:.0f} mg/L) = {ht:.0f} mg/L — "
                "LIME SOFTENING STAGE REQUIRED before IEX: Ca removed as CaCO₃ (pH 9–10), "
                "Mg removed as Mg(OH)₂ (pH 10–11 excess lime). Recarbonation (CO₂) needed after softening."
            )
        elif ca_softening and mg_softening:
            notes.append(
                f"Elevated hardness (Ca {ca_conc:.0f} mg/L, Mg {mg_conc:.0f} mg/L) — "
                "lime softening or soda ash treatment recommended before IEX to protect resin capacity."
            )
        elif ca_softening:
            notes.append(
                f"Ca = {ca_conc:.0f} mg/L — consider soda ash (Na₂CO₃) or lime softening to remove Ca as CaCO₃ "
                "before IEX; reduces resin capacity consumption."
            )
        elif mg_softening:
            notes.append(
                f"Mg = {mg_conc:.0f} mg/L — Mg(OH)₂ precipitation at pH 10–11 possible; "
                "partly removed during high-pH metal precipitation if present."
            )
        elif hardness_concern:
            notes.append(
                f"Moderate hardness ({ht:.0f} mg/L) — Ca/Mg will consume some IEX resin capacity; "
                "factor into resin volume sizing."
            )
        return " ".join(notes)

    def _li_addendum():
        if li_recovery_strong:
            return (
                f" LITHIUM RECOVERY OPPORTUNITY: Li = {li_conc:.0f} mg/L — at this concentration, "
                "Li recovery as Li₂CO₃ or LiOH·H₂O is commercially attractive. "
                "Li₂CO₃ (battery-grade, >99.5% purity) precipitates from concentrated solution using Na₂CO₃ "
                "(solubility ~13 g/L at 20°C, decreasing at elevated temperature). "
                "Recommended route: evaporative concentration of Na₂SO₄ mother liquor → selective Li₂CO₃ crystallisation "
                "→ or electrodialysis/nanofiltration for Li concentration followed by LiOH conversion via lime. "
                "Li remains in solution through all precipitation stages — it reports to the cleaned Na₂SO₄ stream."
            )
        elif li_recovery_flag:
            return (
                f" LITHIUM NOTE: Li = {li_conc:.0f} mg/L — Li is not removed by hydroxide precipitation or standard IEX. "
                "It remains concentrated in the Na₂SO₄ product stream. "
                f"At {li_conc:.0f} mg/L, Li recovery by Na₂CO₃ precipitation or membrane concentration is worth evaluating "
                "depending on feed volume and market conditions (Li₂CO₃ ~$15–25/kg battery grade)."
            )
        elif li_conc > 0:
            return (
                f" Li = {li_conc:.0f} mg/L — Li passes through all treatment stages unaffected and "
                "concentrates in the final Na₂SO₄ product. Monitor Li in product specification."
            )
        return ""

    # ── CASE A: Negligible metals ──
    if metals_negligible and not need_filtration:
        t = "pH correction + direct sodium sulfate product"
        if need_softening or ca_softening or mg_softening:
            t = "pH correction + Ca/Mg softening + direct sodium sulfate product"
        r = (f"Heavy metals negligible ({hmt:.2f} mg/L) — no metal precipitation needed. "
             "Focus on pH correction and product quality.")
        h = _hardness_addendum()
        if h: r += " " + h
        if is_sulfate_rich:
            r += " Sodium sulfate product is essentially clean — downstream concentration/crystallisation may be the primary next step."
        r += _li_addendum()
        return t, r

    if metals_negligible and need_filtration:
        t = "Mechanical filtration + pH correction"
        if need_softening or ca_softening:
            t = "Mechanical filtration + Ca/Mg softening + pH correction"
        r = (f"Heavy metals negligible ({hmt:.2f} mg/L), SS = {ss:.0f} mg/L — filtration is the primary treatment step. "
             "No chemical precipitation for metals is needed.")
        h = _hardness_addendum()
        if h: r += " " + h
        r += _li_addendum()
        return t, r

    # ── CASE B: Trace metals (<1 mg/L total), direct IEX viable ──
    if metals_trace:
        if mg_ in ["Ni/Co/Mn hydroxide precursor recovery", "Ni/Co/Mn carbonate precursor recovery"]:
            t = "Insufficient Ni/Co/Mn for precursor recovery — consider IEX polishing instead"
            r = (f"Ni/Co/Mn combined ({ni_co_mn:.2f} mg/L) is too low for economic precursor recovery. "
                 "Chelating IEX polishing is more appropriate at this concentration level.")
        else:
            t = "Direct chelating IEX polishing — no bulk precipitation required"
            r = (f"Total heavy metals are trace level ({hmt:.2f} mg/L). "
                 "At these concentrations, bulk pH precipitation is not cost-effective and would generate unnecessary sludge. "
                 "Direct chelating IEX polishing (e.g. iminodiacetate resin) is the appropriate technology. "
                 "Selectivity sequence for iminodiacetate resin: Cu > Ni > Co > Fe > Mn > Ca > Mg >> Li/Na.")
        if need_filtration:
            r += f" Suspended solids ({ss:.1f} mg/L) must be removed by filtration before the IEX column to prevent fouling."
        h = _hardness_addendum()
        if h: r += " | HARDNESS: " + h
        r += _li_addendum()
        return t, r

    # ── CASE C: Low metals (1–10 mg/L), light pre-treatment ──
    if metals_low:
        if mg_ in ["Ni/Co/Mn hydroxide precursor recovery", "Ni/Co/Mn carbonate precursor recovery"]:
            t = "Single-stage precipitation for Ni/Co/Mn precursor + filtration"
            r = (f"Ni/Co/Mn at {ni_co_mn:.2f} mg/L — marginal for precursor recovery but feasible as a single high-pH precipitation stage. "
                 "Product purity will be limited by co-precipitation of Ca/Mg impurities.")
        elif need_high_ph_precip:
            t = "Light pH adjustment + single-stage precipitation + filtration + IEX polishing"
            r = (f"Metals are in the low range ({hmt:.2f} mg/L total). A single high-pH precipitation stage for Ni/Co/Mn "
                 f"({ni_co_mn:.2f} mg/L) followed by filtration and IEX polishing is appropriate. "
                 "Full multistage precipitation is not warranted at this level.")
        elif need_low_ph_precip:
            t = "Single low-pH precipitation step (Fe/Al/Cu) + filtration + IEX polishing"
            r = (f"Fe/Al/Cu ({fe_al_cu:.2f} mg/L) justify a single low-pH precipitation step (pH ~4–5). "
                 f"Ni/Co/Mn ({ni_co_mn:.2f} mg/L) are low enough for IEX polishing without further precipitation. ")
        else:
            t = "Mechanical filtration + pH correction + chelating IEX polishing"
            r = (f"Dissolved metals are low ({hmt:.2f} mg/L total) and no individual metal group crosses the precipitation threshold. "
                 "A single-pass through a chelating IEX column after pH correction and filtration is the most cost-effective route.")
        if is_sulfate_rich:
            r += " Sodium sulfate matrix passes through chelating IEX without interference — Na⁺ and SO₄²⁻ have negligible affinity for iminodiacetate resin."
        h = _hardness_addendum()
        if h: r += " | HARDNESS: " + h
        r += _li_addendum()
        return t, r

    # ── CASE D: Moderate metals (10–100 mg/L) ──
    # Determine how many precipitation stages are actually needed based on which metals are present.
    # Reference: Marchioretto et al. (2005) — Fe(III) precipitates pH 1.3–4, Al pH 3.5–6,
    # Ni/Co require pH 9–10, Mn needs pH 10+ for hydroxide (sulfide at pH 6–7).
    # Lewis (2010) — metal sulfide selectivity: Cu > Ni > Co > Fe > Mn >> Mg, Ca.
    # KEY RULE: only include a stage if the relevant metals are actually present above threshold.
    both_groups   = need_low_ph_precip and need_high_ph_precip   # Fe/Al/Cu AND Ni/Co/Mn both elevated
    only_low_ph   = need_low_ph_precip and not need_high_ph_precip  # only Fe/Al/Cu
    only_high_ph  = need_high_ph_precip and not need_low_ph_precip  # only Ni/Co/Mn (your exact scenario)

    if not need_bulk_precip:
        if mg_ == "Ni/Co/Mn hydroxide precursor recovery":
            if need_low_ph_precip:
                t = "Low-pH impurity removal (Fe/Al/Cu) + single high-pH Ni/Co/Mn hydroxide co-precipitation"
                r = (f"Fe/Al/Cu ({fe_al_cu:.2f} mg/L) must be removed first at pH 4–5 (Fe(OH)₃ forms at pH 1.3, Al(OH)₃ at pH 3.5 — Marchioretto et al., 2005). "
                     f"Then raise pH to 9–10 for controlled Ni/Co/Mn hydroxide precursor formation ({ni_co_mn:.2f} mg/L). Two stages needed.")
            else:
                t = "Single high-pH Ni/Co/Mn hydroxide co-precipitation — no low-pH stage required"
                r = (f"Fe/Al/Cu are below the precipitation threshold ({fe_al_cu:.2f} mg/L) — no low-pH impurity removal stage is needed. "
                     f"Proceed directly to controlled NaOH dosing at pH 9–10 for Ni/Co/Mn hydroxide precursor formation ({ni_co_mn:.2f} mg/L). "
                     "Single-stage precipitation is sufficient. Coagulation/flocculation recommended to improve fine particle settling (Marchioretto et al., 2005).")
        elif mg_ == "Ni/Co/Mn carbonate precursor recovery":
            if need_low_ph_precip:
                t = "Low-pH impurity removal (Fe/Al/Cu) + single-stage Ni/Co/Mn carbonate precipitation"
                r = (f"Fe/Al/Cu ({fe_al_cu:.2f} mg/L) removed first at low pH, then Na₂CO₃ dosing for Ni/Co/Mn carbonate precursor ({ni_co_mn:.2f} mg/L).")
            else:
                t = "Single-stage Ni/Co/Mn carbonate precipitation — no low-pH stage required"
                r = (f"Fe/Al/Cu are negligible ({fe_al_cu:.2f} mg/L) — skip low-pH stage entirely. "
                     f"Direct Na₂CO₃ dosing for Ni/Co/Mn carbonate precipitation ({ni_co_mn:.2f} mg/L). "
                     "Carbonate dosing must be controlled to avoid Ca co-precipitation if hardness is elevated.")
        elif mg_ == "Wastewater polishing only":
            if both_groups:
                t = "Two-stage hydroxide precipitation + solid-liquid separation + optional IEX polishing"
                r = (f"Both low-pH metals (Fe/Al/Cu: {fe_al_cu:.2f} mg/L) and high-pH metals (Ni/Co/Mn: {ni_co_mn:.2f} mg/L) are elevated. "
                     "Stage 1 at pH 4–5 removes Fe/Al/Cu; Stage 2 at pH 9–10 removes Ni/Co/Mn. "
                     "Hydroxide precipitation typically achieves 0.5–1.0 mg/L residual (EPA guidance). IEX adds a polishing safety margin.")
            elif only_low_ph:
                t = "Single low-pH precipitation stage (Fe/Al/Cu) + filtration + optional IEX"
                r = (f"Only Fe/Al/Cu ({fe_al_cu:.2f} mg/L) exceed the precipitation threshold. Ni/Co/Mn ({ni_co_mn:.2f} mg/L) are low — IEX polishing handles residuals. "
                     "One precipitation stage at pH 4–5 is sufficient. No high-pH stage warranted.")
            else:
                t = "Single high-pH precipitation stage (Ni/Co/Mn) + filtration + optional IEX"
                r = (f"Only Ni/Co/Mn ({ni_co_mn:.2f} mg/L) exceed the threshold. Fe/Al/Cu ({fe_al_cu:.2f} mg/L) are negligible — no low-pH stage needed. "
                     "One precipitation stage at pH 9–10 is sufficient. "
                     "Coagulation/flocculation (polymer addition) is recommended to improve settling of fine Ni/Co/Mn hydroxide particles "
                     "(Marchioretto et al., 2005 — fine hydroxide particles can be colloidal and pass standard filters).")
        else:
            # Clean Na2SO4 / IEX polishing goal
            if both_groups:
                t = "Two-stage precipitation (low-pH + high-pH) + filtration + chelating IEX polishing"
                r = (f"Both Fe/Al/Cu ({fe_al_cu:.2f} mg/L, precipitate pH 4–5) and Ni/Co/Mn ({ni_co_mn:.2f} mg/L, precipitate pH 9–10) are elevated — two stages are required. "
                     "Stage 1 pH 4–5 removes Fe/Al/Cu; Stage 2 pH 9–10 removes Ni/Co/Mn. "
                     "Each stage followed by solid-liquid separation before the next. Chelating IEX polishing as final step.")
            elif only_low_ph:
                t = "Single low-pH precipitation (Fe/Al/Cu) + filtration + chelating IEX polishing"
                r = (f"Only Fe/Al/Cu ({fe_al_cu:.2f} mg/L) are above the precipitation threshold (Ni/Co/Mn: {ni_co_mn:.2f} mg/L — below threshold). "
                     "One low-pH stage at pH 4–5 is sufficient for bulk removal. Chelating IEX handles residual Ni/Co/Mn polishing. "
                     "Fe(OH)₃ and Al(OH)₃ also co-precipitate trace Cr, Pb, Zn by adsorption (Marchioretto et al., 2005).")
            else:
                # only_high_ph: the exact scenario the user described — Ni/Co/Mn only
                t = "Single high-pH precipitation stage (Ni/Co/Mn only) + coagulation/flocculation + filtration + IEX polishing"
                r = (f"Fe/Al/Cu are negligible ({fe_al_cu:.2f} mg/L) — no low-pH precipitation stage is needed or warranted. "
                     f"Only Ni/Co/Mn ({ni_co_mn:.2f} mg/L) require treatment: a single high-pH precipitation stage at pH 9–10 using {pbase} is sufficient. "
                     "IMPORTANT: Ni/Co/Mn hydroxides form as very fine colloidal particles — coagulation/flocculation with a polymer aid is strongly recommended "
                     "before solid-liquid separation to improve settling and reduce IEX fouling (Marchioretto et al., 2005; Lewis, 2010). "
                     "Chelating IEX polishing removes residual Ni/Co/Mn after filtration.")
        if is_sulfate_rich:
            r += f" Sodium sulfate ({s:.0f} mg/L SO₄) is unaffected by hydroxide precipitation — it remains in solution as desired."
        return t, r

    # ── CASE E: High metals (>100 mg/L) ──
    # At this load, always need aggressive bulk precipitation.
    # Single vs two-stage still depends on which groups are present.
    both_groups  = need_low_ph_precip and need_high_ph_precip
    only_high_ph = need_high_ph_precip and not need_low_ph_precip
    only_low_ph  = need_low_ph_precip and not need_high_ph_precip

    if mg_ == "Ni/Co/Mn hydroxide precursor recovery":
        if need_low_ph_precip:
            t = "Bulk Fe/Al/Cu impurity removal (low-pH) + controlled Ni/Co/Mn hydroxide precursor recovery (high-pH)"
            r = (f"High load — Fe/Al/Cu ({fe_al_cu:.1f} mg/L) must be removed at pH 4–5 before precursor precipitation. "
                 f"Then controlled NaOH to pH 9–10 for Ni/Co/Mn hydroxide precursor ({ni_co_mn:.1f} mg/L). "
                 "Coagulation/flocculation essential for fine particle separation at both stages.")
        else:
            t = "Single-stage bulk Ni/Co/Mn hydroxide precursor recovery — no Fe/Al/Cu removal needed"
            r = (f"Fe/Al/Cu negligible ({fe_al_cu:.1f} mg/L). High Ni/Co/Mn ({ni_co_mn:.1f} mg/L) — single high-pH precipitation stage. "
                 "Tight pH control (9–10) essential. Coagulation/flocculation + lamella settling for solid-liquid separation.")
    elif mg_ == "Ni/Co/Mn carbonate precursor recovery":
        if need_low_ph_precip:
            t = "Bulk impurity removal (low-pH) + Ni/Co/Mn carbonate precursor recovery"
            r = (f"Remove Fe/Al/Cu ({fe_al_cu:.1f} mg/L) at low pH first, then Na₂CO₃ for Ni/Co/Mn ({ni_co_mn:.1f} mg/L) carbonate precipitation.")
        else:
            t = "Single-stage bulk Ni/Co/Mn carbonate precipitation — no Fe/Al/Cu stage needed"
            r = (f"Fe/Al/Cu negligible ({fe_al_cu:.1f} mg/L). Direct Na₂CO₃ dosing for high Ni/Co/Mn ({ni_co_mn:.1f} mg/L). "
                 "Ca co-precipitation risk — check hardness ({ht:.0f} mg/L Ca+Mg).")
    elif mg_ == "Wastewater polishing only":
        if both_groups:
            t = "Two-stage bulk hydroxide precipitation + sulfide polishing + solid-liquid separation"
            r = (f"High load with both groups elevated — two-stage hydroxide precipitation required. "
                 f"Stage 1 (pH 4–5) for Fe/Al/Cu ({fe_al_cu:.1f} mg/L); Stage 2 (pH 9–10) for Ni/Co/Mn ({ni_co_mn:.1f} mg/L). "
                 "For stringent limits, sulfide polishing (TMT-15 or Na₂S) achieves 3–5 orders of magnitude lower residual than hydroxide alone (Lewis, 2010).")
        elif only_high_ph:
            t = "Single high-pH bulk precipitation (Ni/Co/Mn) + coagulation/flocculation + sulfide polishing"
            r = (f"Fe/Al/Cu negligible ({fe_al_cu:.1f} mg/L) — skip low-pH stage. "
                 f"High Ni/Co/Mn ({ni_co_mn:.1f} mg/L) — single stage pH 9–10 precipitation. "
                 "Coagulation/flocculation mandatory — Ni/Co/Mn hydroxides form very fine colloidal particles (Marchioretto et al., 2005). "
                 "Sulfide polishing (Na₂S or biogenic H₂S) as final step for stringent discharge limits (Lewis, 2010).")
        else:
            t = "Single low-pH bulk precipitation (Fe/Al/Cu) + filtration + IEX polishing"
            r = (f"Ni/Co/Mn low ({ni_co_mn:.1f} mg/L) — no high-pH stage needed. "
                 f"Bulk Fe/Al/Cu ({fe_al_cu:.1f} mg/L) removed at pH 4–5. IEX polishing handles residual Ni/Co/Mn.")
    else:
        if both_groups:
            t = "Two-stage bulk precipitation (pH 4–5 then pH 9–10) + coagulation + filtration + IEX finishing"
            r = (f"High load with both metal groups: Fe/Al/Cu ({fe_al_cu:.1f} mg/L) precipitate at pH 4–5, "
                 f"Ni/Co/Mn ({ni_co_mn:.1f} mg/L) at pH 9–10. Two stages with intermediate solid-liquid separation required. "
                 "Coagulation/flocculation at each stage. IEX polishing only after bulk metals below ~10 mg/L.")
        elif only_high_ph:
            t = "Single high-pH bulk precipitation (Ni/Co/Mn only) + coagulation/flocculation + filtration + IEX polishing"
            r = (f"Fe/Al/Cu are negligible ({fe_al_cu:.1f} mg/L) — no low-pH stage needed. "
                 f"High Ni/Co/Mn ({ni_co_mn:.1f} mg/L) require a single high-pH stage at pH 9–10 with {pbase}. "
                 "CRITICAL: Ni/Co/Mn hydroxides precipitate as very fine colloidal particles — coagulation/flocculation (anionic polymer) "
                 "is essential before solid-liquid separation (lamella settler or filter press). "
                 "Without flocculation, fine particles will foul IEX resin and pass conventional filters (Marchioretto et al., 2005). "
                 "Chelating IEX polishing for final product quality.")
        else:
            t = "Single low-pH bulk precipitation (Fe/Al/Cu) + filtration + IEX polishing"
            r = (f"Ni/Co/Mn below bulk threshold ({ni_co_mn:.1f} mg/L). Fe/Al/Cu ({fe_al_cu:.1f} mg/L) bulk removal at pH 4–5. "
                 "IEX polishing handles residual metals.")
    if is_sulfate_rich:
        r += f" Sodium sulfate ({s:.0f} mg/L SO₄) passes through hydroxide precipitation unaffected — remains in solution as desired."
    # Append Ca/Mg and Li notes to ALL cases
    h = _hardness_addendum()
    if h: r += " | HARDNESS: " + h
    r += _li_addendum()
    return t, r


def process_train(mg_, mets, ip, tfp, pbase, pacid, hmt, ss):
    """
    Builds a tailored process train based on actual feed concentrations.
    Steps are only included when the concentration data justifies them.
    """
    fe_al_cu = mets["Fe"] + mets["Al"] + mets["Cu"]
    ni_co_mn = mets["Ni"] + mets["Co"] + mets["Mn"]
    metals_negligible   = hmt  < 0.5
    metals_trace        = hmt  < THRESH["hmt_trace"]
    need_low_ph_precip  = fe_al_cu > THRESH["fe_al_cu_precip"]
    need_high_ph_precip = ni_co_mn > THRESH["ni_co_mn_precip"]
    need_bulk_precip    = hmt   > THRESH["hmt_bulk"]
    need_filtration     = ss    > THRESH["ss_filtration"]
    need_coag           = ss    > THRESH["ss_coag"]

    steps = ["Feed equalization / holding tank"]

    # Solids removal
    if need_coag:
        steps.append(f"Coarse screening + coagulation/flocculation (suspended solids {ss:.0f} mg/L — high load)")
        steps.append("Lamella clarifier or DAF for primary solids removal")
        steps.append("Cartridge / bag filtration for fine particle polishing")
    elif need_filtration:
        steps.append(f"Bag filtration / cartridge filtration (suspended solids {ss:.0f} mg/L)")
    else:
        steps.append("Strainer / in-line filter (suspended solids low — precautionary only)")

    # Negligible metals: skip all precipitation
    if metals_negligible:
        steps.append(f"pH correction to target {tfp} using {pbase if tfp > ip else pacid}")
        steps.append("Final quality check — sodium sulfate product")
        return steps

    # Trace metals: direct IEX, no precipitation
    if metals_trace:
        steps.append(f"pH adjustment to {tfp} (IEX operating window pH 6–9) using {pbase if tfp > ip else pacid}")
        steps.append("Chelating ion exchange resin polishing — direct feed (iminodiacetate type recommended)")
        steps.append("Clean sodium sulfate-rich product solution")
        return steps

    # Low/moderate: selective precipitation only where needed
    if need_low_ph_precip:
        stage_label = "Stage 1" if need_high_ph_precip else "Single stage"
        steps.append(f"{stage_label} pH adjustment to pH 4–5 using {pbase} — Fe/Al/Cu precipitation ({fe_al_cu:.1f} mg/L; Fe(OH)₃ forms pH 1.3, Al(OH)₃ pH 3.5)")
        steps.append(f"{stage_label} solid-liquid separation — filter press or lamella settler")

    if need_high_ph_precip or need_bulk_precip:
        stage_label = "Stage 2" if need_low_ph_precip else "Single stage"
        if mg_ == "Ni/Co/Mn hydroxide precursor recovery":
            steps.append(f"{stage_label} controlled NaOH addition to pH 9–10 — Ni/Co/Mn hydroxide precursor formation ({ni_co_mn:.1f} mg/L)")
        elif mg_ == "Ni/Co/Mn carbonate precursor recovery":
            steps.append(f"{stage_label} controlled Na₂CO₃ addition — Ni/Co/Mn carbonate precursor formation ({ni_co_mn:.1f} mg/L)")
        else:
            steps.append(f"{stage_label} pH adjustment to pH 9–10 using {pbase} — Ni/Co/Mn precipitation ({ni_co_mn:.1f} mg/L)")
        steps.append(f"{stage_label} coagulation / flocculation (anionic polymer recommended) — Ni/Co/Mn hydroxides form very fine colloidal particles")
        steps.append(f"{stage_label} solid-liquid separation — clarifier / lamella settling / filter press")

    elif need_low_ph_precip:
        # Low-pH only: still add coag note since fine Fe/Al hydroxide particles form
        steps.append("Coagulation / flocculation (polymer aid) — Fe/Al/Cu hydroxides may form fine colloidal particles")

    # Sulfide polishing for very high metals or stringent limits
    if hmt > THRESH["hmt_bulk"] and mg_ == "Wastewater polishing only":
        steps.append("Sulfide polishing stage (TMT-15 or Na₂S) — for stringent discharge limits, metal sulfides have lower solubility than hydroxides")

    # Filtration before IEX
    if need_low_ph_precip or need_high_ph_precip:
        steps.append("Sand filter / multimedia filter / cartridge filter — protect IEX resin from particulates")

    # pH correction before IEX (only if not already in window)
    if need_low_ph_precip or need_high_ph_precip:
        steps.append(f"Final pH balancing to {tfp} before ion exchange (IEX window: pH {THRESH['iex_ph_low']}–{THRESH['iex_ph_high']})")

    # ── Ca/Mg softening — add dedicated step if hardness is high ──
    # Ca precipitates as CaCO3 (lime softening, pH 9–10) or removed by Na2CO3 (soda ash)
    # Mg precipitates as Mg(OH)2 at pH 10–11 (excess lime needed)
    # If Ca or Mg are elevated and IEX is the next step, softening protects resin capacity.
    ca_val = mets.get("Ca", 0)
    mg_val = mets.get("Mg", 0)
    ht_local = ca_val + mg_val
    need_softening = ht_local > THRESH["hardness_softening"]
    ca_only_softening = ca_val > THRESH["ca_precip"] and mg_val <= THRESH["mg_precip"]
    mg_only_softening = mg_val > THRESH["mg_precip"] and ca_val <= THRESH["ca_precip"]

    if need_softening:
        steps.append(
            f"Lime softening stage — Ca ({ca_val:.1f} mg/L) removed as CaCO3 at pH 9–10 using Ca(OH)₂; "
            f"Mg ({mg_val:.1f} mg/L) removed as Mg(OH)₂ requires pH 10–11 (excess lime); "
            "Recarbonation step needed to lower pH before IEX. "
            "Sludge: Ca/Mg sludge is separate from metal hydroxide sludge — handle separately."
        )
        steps.append("Clarification / settling of Ca/Mg softening precipitates + recarbonation (CO₂ dosing) to reduce pH")
    elif ca_only_softening:
        steps.append(
            f"Ca softening consideration — Ca = {ca_val:.1f} mg/L. "
            "Ca can be removed as CaCO3 by soda ash (Na₂CO₃) addition or lime at pH 9–10. "
            "This reduces IEX resin loading. Check if Ca removal is required for product quality."
        )
    elif mg_val > THRESH["mg_precip"] and ht_local > THRESH["hardness_high"]:
        steps.append(
            f"Mg softening consideration — Mg = {mg_val:.1f} mg/L. "
            "Mg(OH)₂ precipitation requires pH 10–11 (excess lime). "
            "For IEX protection, consider softening pre-step if hardness significantly loads resin."
        )

    # IEX only if metals warrant it
    if not metals_negligible and mg_ != "Ni/Co/Mn hydroxide precursor recovery" and mg_ != "Ni/Co/Mn carbonate precursor recovery":
        steps.append("Chelating ion exchange resin polishing (iminodiacetate type; selectivity: Cu>Ni>Co>Fe>Mn>Ca>Mg)")

    li_val = mets.get("Li", 0)
    if li_val > THRESH["li_recovery_high"]:
        steps.append(
            f"LITHIUM RECOVERY STEP (optional downstream): Li = {li_val:.0f} mg/L — "
            "Li concentrates in cleaned Na₂SO₄ stream. Recovery options: "
            "(a) Evaporative concentration → Na₂CO₃ addition → Li₂CO₃ crystallisation (Ksp ~8.7×10⁻⁴, solubility decreases at 60–80°C); "
            "(b) Nanofiltration/electrodialysis for selective Li concentration; "
            "(c) Lime conversion of Li₂CO₃ → LiOH·H₂O (battery grade). "
            "Consult lithium recovery specialist before committing to route."
        )
    elif li_val > THRESH["li_recovery_low"]:
        steps.append(
            f"LITHIUM NOTE: Li = {li_val:.0f} mg/L — passes through all stages into Na₂SO₄ product stream. "
            "Li recovery by Na₂CO₃ precipitation or membrane concentration worth evaluating at this concentration."
        )
    steps.append("Clean sodium sulfate-rich product solution")
    return steps


def decision_drivers(mg_, mets, s, ss, ip, tfp, hmt, ht):
    """Concentration-based decision drivers — only flag what is actually relevant."""
    fe_al_cu = mets["Fe"] + mets["Al"] + mets["Cu"]
    ni_co_mn = mets["Ni"] + mets["Co"] + mets["Mn"]
    drivers  = []

    if hmt < 0.5:
        drivers.append(f"All metals essentially zero — no precipitation warranted, focus on pH and SS control")
    elif hmt < THRESH["hmt_trace"]:
        drivers.append(f"Trace metals ({hmt:.2f} mg/L) — direct IEX polishing is the most cost-effective route")
    elif hmt < THRESH["hmt_low"]:
        drivers.append(f"Low metals ({hmt:.1f} mg/L) — selective pre-treatment only where concentration thresholds are crossed")
    else:
        drivers.append(f"Moderate-to-high metals ({hmt:.1f} mg/L) — staged precipitation is the primary technology")

    if fe_al_cu > THRESH["fe_al_cu_precip"]:
        drivers.append(f"Fe/Al/Cu = {fe_al_cu:.2f} mg/L — low-pH precipitation stage (pH 4–5) is justified")
    if ni_co_mn > THRESH["ni_co_mn_precip"]:
        drivers.append(f"Ni/Co/Mn = {ni_co_mn:.2f} mg/L — high-pH precipitation stage (pH 9–10) is justified")
    ca_val = mets.get("Ca", 0)
    mg_val = mets.get("Mg", 0)
    if ca_val > THRESH["ca_precip"]:
        drivers.append(f"Ca = {ca_val:.1f} mg/L — Ca precipitates as CaCO3 at pH 9–10 (lime or soda ash softening applicable)")
    if mg_val > THRESH["mg_precip"]:
        drivers.append(f"Mg = {mg_val:.1f} mg/L — Mg(OH)₂ precipitation at pH 10–11; may be removed partially during high-pH metal precipitation stage")
    if ht > THRESH["hardness_softening"]:
        drivers.append(f"Very high hardness ({ht:.1f} mg/L) — dedicated lime softening stage strongly recommended to protect IEX resin capacity")
    elif ht > THRESH["hardness_high"]:
        drivers.append(f"High hardness ({ht:.1f} mg/L) — significant IEX resin capacity penalty; softening pre-step or resin oversizing needed")
    elif ht > THRESH["hardness_warn"]:
        drivers.append(f"Moderate hardness ({ht:.1f} mg/L) — Ca/Mg compete with chelating resin; factor into IEX sizing")
    if s > THRESH["so4_high"]:
        drivers.append(f"Sulfate = {s:.0f} mg/L — sodium sulfate matrix remains in solution through all precipitation stages (desired outcome)")
    if ss > THRESH["ss_filtration"]:
        drivers.append(f"Suspended solids = {ss:.1f} mg/L — filtration before IEX is essential to prevent fouling")
    if tfp < THRESH["iex_ph_low"] or tfp > THRESH["iex_ph_high"]:
        drivers.append(f"Target pH {tfp} is outside IEX operating window (6–9) — pH correction step required")
    # Lithium drivers
    li_val = mets.get("Li", 0)
    if li_val > THRESH["li_recovery_high"]:
        drivers.append(f"LITHIUM RECOVERY OPPORTUNITY: Li = {li_val:.0f} mg/L — Li₂CO₃ crystallisation commercially viable; Li concentrates in Na₂SO₄ product stream")
    elif li_val > THRESH["li_recovery_low"]:
        drivers.append(f"Li = {li_val:.0f} mg/L — Li recovery worth evaluating (Na₂CO₃ precipitation or membrane concentration route)")
    elif li_val > 0:
        drivers.append(f"Li = {li_val:.0f} mg/L — Li is inert to all precipitation stages; passes through and reports to Na₂SO₄ product")
    if not drivers:
        drivers.append("Feed is essentially clean — minimal treatment required")
    return drivers


def iex_suitability(tfp, ss, ht, hmt):
    """
    IEX suitability scoring — penalise each condition that would harm resin performance.
    Based on chelating IEX design criteria from resin vendor literature
    (Purolite S930, DuPont AmberLite IRC748).
    """
    score = 100; comments = []
    if hmt < 0.5:
        comments.append("Metals negligible — IEX not required; pH correction and filtration sufficient.")
        return 100, "IEX not required for this feed", comments
    if tfp < THRESH["iex_ph_low"] or tfp > THRESH["iex_ph_high"]:
        score -= 25
        comments.append(f"Target pH {tfp} outside IEX window (6–9) — resin efficiency will be reduced.")
    if ss > THRESH["ss_filtration"]:
        score -= 25
        comments.append(f"Suspended solids {ss:.1f} mg/L — must be removed before resin to prevent fouling and pressure drop.")
    if ht > THRESH["hardness_high"]:
        score -= 20
        comments.append(f"High Ca/Mg ({ht:.1f} mg/L) will compete for iminodiacetate resin sites and shorten run length.")
    elif ht > THRESH["hardness_warn"]:
        score -= 10
        comments.append(f"Moderate hardness ({ht:.1f} mg/L) — some resin capacity consumed by Ca/Mg; factor into sizing.")
    if hmt > THRESH["hmt_bulk"]:
        score -= 30
        comments.append(f"Heavy metals too high ({hmt:.1f} mg/L) for direct IEX — bulk precipitation must reduce load below ~10 mg/L first.")
    elif hmt > THRESH["hmt_low"]:
        score -= 15
        comments.append(f"Metals {hmt:.1f} mg/L — precipitation pre-treatment recommended before IEX to protect resin capacity.")

    score = max(score, 0)
    if score >= 80:   status = "Good candidate for IEX polishing"
    elif score >= 50: status = "Possible, but pre-treatment should be improved first"
    elif score >= 25: status = "Poor IEX candidate — significant pre-treatment required"
    else:             status = "Not suitable for direct IEX — bulk treatment must come first"
    if not comments:
        comments.append("Feed conditions are well-suited for direct chelating IEX polishing.")
    return score, status, comments


# ─────────────────────────────────────────────
# CAPEX / OPEX — LANG + HAND-CHILTON METHODS
# ─────────────────────────────────────────────
def capex_opex_estimate(equip_keur, flow_m3h, pbase, chem_unit, energy_eur_kwh, method="Lang"):
    """
    Two methods:
    1. Lang Factor (Peters, Timmerhaus & West, Plant Design and Economics, 5th Ed.)
       - Simple: TIC = f_lang × C_equipment
       - f_lang = 4.7 for fluid process plants (pumps, tanks, reactors)
       - Accuracy: Class 5, ±50–100%

    2. Hand-Chilton Method (Hand 1958 / Chilton 1960, refined by Ulrich & Vasudevan 2004)
       - More detailed: applies individual installation factors per equipment type
       - Typical factors for water treatment: tanks f=3.1, pumps f=3.5, heat exchangers f=3.5,
         packed columns f=4.0, vessels/reactors f=4.2, instrumentation f=1.5
       - Accuracy: Class 4, ±30–50%
       - Reference: Ulrich G.D. & Vasudevan P.T., Chemical Engineering Process Design and Economics, 2004

    Both use 8,000 h/yr operating basis (continuous 24/7).
    """
    op_hours = 8000

    # ── Lang Method ──
    lang_f   = 4.7
    capex_lang = equip_keur * lang_f

    # ── Hand-Chilton Method ──
    # Decompose equipment cost into typical water treatment equipment mix:
    # 40% tanks/vessels, 20% pumps, 15% instrumentation/controls,
    # 15% separation equipment (settlers, filters), 10% miscellaneous
    hc_factors = {
        "Tanks & reactors (40%)":        (0.40, 4.2),
        "Pumps & piping (20%)":          (0.20, 3.5),
        "Instrumentation (15%)":         (0.15, 2.5),
        "Separation / filtration (15%)": (0.15, 3.8),
        "Misc. (10%)":                   (0.10, 3.5),
    }
    hc_breakdown = {}
    capex_hc = 0.0
    for label, (frac, factor) in hc_factors.items():
        item_equip = equip_keur * frac
        item_tIC   = item_equip * factor
        hc_breakdown[label] = {"equip_keur": round(item_equip,1), "factor": factor,
                                "installed_keur": round(item_tIC,1)}
        capex_hc += item_tIC

    # Select CAPEX based on method
    capex_keur = capex_lang if method == "Lang" else capex_hc

    # ── OPEX (shared logic) ──
    base_dose     = 2.0 if pbase == "Lime / Ca(OH)₂" else (0.55 if pbase == "Na₂CO₃" else 1.2)
    chem_kg_yr    = base_dose * flow_m3h * op_hours
    chem_cost     = chem_kg_yr * chem_unit / 1000
    energy_kwh_yr = 0.15 * flow_m3h * op_hours
    energy_cost   = energy_kwh_yr * energy_eur_kwh / 1000
    labour_maint  = capex_keur * 0.05
    opex_keur_yr  = chem_cost + energy_cost + labour_maint
    opex_eur_m3   = (opex_keur_yr * 1000) / (flow_m3h * op_hours) if flow_m3h > 0 else 0

    return {
        "capex_keur":           round(capex_keur, 0),
        "capex_lang_keur":      round(capex_lang, 0),
        "capex_hc_keur":        round(capex_hc, 0),
        "hc_breakdown":         hc_breakdown,
        "lang_factor":          lang_f,
        "opex_keur_yr":         round(opex_keur_yr, 1),
        "opex_eur_m3":          round(opex_eur_m3, 3),
        "chem_cost_keur_yr":    round(chem_cost, 1),
        "energy_cost_keur_yr":  round(energy_cost, 1),
        "labour_maint_keur_yr": round(labour_maint, 1),
        "method":               method,
    }

# Keep backward-compat alias
def lang_capex_opex(equip_keur, flow_m3h, pbase, chem_unit, energy_eur_kwh):
    return capex_opex_estimate(equip_keur, flow_m3h, pbase, chem_unit, energy_eur_kwh, "Lang")


# ─────────────────────────────────────────────
# CHEMICAL CONSUMPTION — FULL MASS BALANCE
# ─────────────────────────────────────────────
def chemical_consumption(flow, ip, tfp, pbase, pacid, ss, mets, hmt, ht, sulfate_mgL, need_low_precip, need_high_precip, pbase_used):
    """
    Full mass-balance based chemical consumption.
    8,000 h/yr continuous operation basis.

    Sources:
    - NaOH/H2SO4 neutralisation: stoichiometric from titration curves,
      typical buffering factor 1.2-1.5x for industrial streams
    - Coagulant (FeCl3 or alum): 0.3-0.6 kg/kg SS removed (WEF MOP 8)
    - Polymer flocculant: 0.5-2 g/m3 for settling improvement
    - NaOCl for Mn oxidation: 0.77 kg NaOCl per kg Mn (stoichiometric Mn2+ → MnO2)
    - IEX resin life: Purolite S930/AmberLite IRC748 typically 3-5 years service life,
      regenerated with H2SO4 (150-200 g/L), ~2 BV acid per regeneration
    - IEX capacity: iminodiacetate chelating resin ~0.8-1.2 eq/L wet volume
    """
    op_h   = 8000
    results = {}

    def _add(key, reagent, kg_m3, note=""):
        kg_h  = round(kg_m3 * flow, 3)
        t_yr  = round(kg_m3 * flow * op_h / 1000, 2)
        results[key] = {"reagent": reagent, "kg_per_m3": round(kg_m3,4),
                        "kg_per_h": kg_h, "t_per_yr": t_yr, "note": note}

    ph_delta = tfp - ip

    # ── 1. Base for pH increase (neutralisation + precipitation) ──
    if ph_delta > 0:
        # Neutralisation stoichiometry + buffer factor 1.3 for industrial stream
        buf = 1.3
        if pbase == "Lime / Ca(OH)₂":
            # Ca(OH)2 MW=74, H2SO4 MW=98; 1 mol H2SO4 needs 1 mol Ca(OH)2
            # Rough: 0.5 kg Ca(OH)2/pH unit/m3 × buffer
            kg_m3 = 0.5 * abs(ph_delta) * buf
            note  = "Ca(OH)₂ — lower cost, adds Ca hardness, produces CaCO₃/Ca(OH)₂ sludge"
        elif pbase == "Na₂CO₃":
            kg_m3 = 0.55 * abs(ph_delta) * buf
            note  = "Na₂CO₃ (soda ash) — used for carbonate precipitation of Ca, CO₃²⁻ adds to Na₂SO₄ stream"
        else:  # NaOH
            kg_m3 = 0.40 * abs(ph_delta) * buf
            note  = "NaOH (50% solution typical) — clean, no Ca addition, preferred for Na₂SO₄ purity"
        _add("base", pbase, kg_m3, note)

    # ── 2. Acid for pH decrease ──
    elif ph_delta < 0:
        if pacid == "H₂SO₄":
            kg_m3 = 0.30 * abs(ph_delta) * 1.3
            note  = "H₂SO₄ (98% conc.) — preferred to keep Na₂SO₄ matrix; adds SO₄²⁻ (desired)"
        else:
            kg_m3 = 0.34 * abs(ph_delta) * 1.3
            note  = "HCl — introduces Cl⁻; may affect Na₂SO₄ product purity if Cl spec is tight"
        _add("acid", pacid, kg_m3, note)

    # ── 3. Coagulant (FeCl3) for metal precipitation stages ──
    if need_low_precip or need_high_precip:
        # Typical FeCl3 dose 20-80 mg/L; use 40 mg/L as indicative for industrial stream
        fecl3_kg_m3 = 0.040
        _add("coagulant", "FeCl₃ (coagulant, indicative)", fecl3_kg_m3,
             "Iron coagulant aids colloid destabilisation; dose 20–80 mg/L depending on turbidity and metals load")

    # ── 4. Polymer flocculant ──
    if ss > 10 or need_low_precip or need_high_precip:
        floc_kg_m3 = 0.0015 + ss * 0.00005  # 1.5–3 g/m3 range
        _add("flocculant", "Anionic polymer flocculant", floc_kg_m3,
             "Anionic polyacrylamide; dose 1–3 g/m3; improves settling of fine hydroxide precipitates (Marchioretto et al., 2005)")

    # ── 5. NaOCl for Mn oxidation (if Mn present and high pH needed) ──
    mn_conc = mets.get("Mn", 0)
    if mn_conc > 0.5 and need_high_precip:
        # Mn2+ + NaOCl → MnO2 + NaCl; MW: Mn=55, NaOCl=74.5
        # Stoichiometric: 74.5/55 = 1.35 kg NaOCl per kg Mn; +20% excess
        mn_load_kg_m3 = mn_conc / 1000  # mg/L → kg/m3
        naocl_kg_m3   = mn_load_kg_m3 * 1.35 * 1.2
        _add("naocl", "NaOCl (sodium hypochlorite, 12%)", naocl_kg_m3,
             f"For Mn oxidation — Mn²⁺ + NaOCl → MnO₂↓ + NaCl; stoichiometric + 20% excess. Mn={mn_conc:.1f} mg/L")

    # ── 6. Na2CO3 for Li2CO3 recovery (if Li high) ──
    li_conc = mets.get("Li", 0)
    if li_conc > THRESH["li_recovery_low"]:
        # Li2CO3 precipitation: 2Li+ + Na2CO3 → Li2CO3↓ + 2Na+
        # MW: Li=6.94, Na2CO3=106; stoichiometric: 106/(2×6.94) = 7.64 kg Na2CO3 per kg Li
        # Li reports 100% to product stream, assume recovery downstream
        li_load_kg_m3   = li_conc / 1000
        na2co3_kg_m3    = li_load_kg_m3 * 7.64 * 1.1  # +10% excess
        _add("na2co3_li", "Na₂CO₃ (for Li₂CO₃ recovery, downstream)", na2co3_kg_m3,
             f"2Li⁺ + Na₂CO₃ → Li₂CO₃↓ + 2Na⁺; Li={li_conc:.0f} mg/L. Requires concentration step first. Indicative only.")

    # ── 7. IEX resin consumption ──
    # Estimate resin volume from metal load
    # Chelating resin capacity: ~0.9 eq/L wet; typical run length 48-72h between regen
    # At 8000 h/yr operation, ~110-167 regeneration cycles/yr
    # Resin life: ~4 years → annual replacement 25% of inventory
    # Resin sizing: total metal equivalents to be removed per cycle
    total_metal_load_eq_h = 0  # equivalents/h
    metal_valence = {"Ni":2,"Co":2,"Mn":2,"Cu":2,"Fe":3,"Al":3,"Ca":2,"Mg":2,"Li":1}
    metal_mw      = {"Ni":58.7,"Co":58.9,"Mn":54.9,"Cu":63.5,"Fe":55.8,"Al":27.0,"Ca":40.1,"Mg":24.3,"Li":6.94}
    for m, conc in mets.items():
        if conc > 0 and m in metal_valence:
            mol_h   = (conc / 1000 * flow) / metal_mw[m]  # mol/h
            eq_h    = mol_h * metal_valence[m]
            total_metal_load_eq_h += eq_h

    if total_metal_load_eq_h > 0:
        # Assume 48h run between regenerations, 0.9 eq/L resin capacity
        regen_interval_h     = 48
        resin_vol_L          = (total_metal_load_eq_h * regen_interval_h) / 0.9
        regen_per_yr         = op_h / regen_interval_h
        # H2SO4 regenerant: 200 g/L, 2 bed volumes (BV = resin_vol_L/1000 m3)
        h2so4_per_regen_kg   = 0.200 * 2 * resin_vol_L  # kg H2SO4 per regen
        h2so4_yr_t           = h2so4_per_regen_kg * regen_per_yr / 1000
        # Water rinse: 10 BV per regen
        rinse_water_m3_yr    = 10 * (resin_vol_L / 1000) * regen_per_yr
        # Annual resin replacement (25% of inventory, ~€8-12/L for chelating resin)
        resin_replace_L_yr   = resin_vol_L * 0.25
        resin_replace_keur   = resin_replace_L_yr * 10.0 / 1000  # €10/L average

        results["iex_resin"] = {
            "reagent":          "Chelating IEX resin (iminodiacetate)",
            "resin_volume_L":   round(resin_vol_L, 0),
            "regen_per_yr":     round(regen_per_yr, 0),
            "h2so4_regen_t_yr": round(h2so4_yr_t, 2),
            "rinse_water_m3_yr":round(rinse_water_m3_yr, 0),
            "resin_replace_L_yr": round(resin_replace_L_yr, 0),
            "resin_replace_keur_yr": round(resin_replace_keur, 1),
            "note": (f"Sizing: {resin_vol_L:.0f} L resin @ 48h run, 0.9 eq/L capacity. "
                     f"{regen_per_yr:.0f} regen/yr. Resin life 4 yr → {resin_replace_L_yr:.0f} L/yr replacement @ ~€10/L. "
                     "H₂SO₄ regenerant 200 g/L × 2 BV per cycle. Confirm with resin vendor (Purolite S930 / AmberLite IRC748).")
        }
    return results


# ─────────────────────────────────────────────
# COMPUTE
# ─────────────────────────────────────────────
level        = metal_level_category(heavy_metals_total)
treatment, reason = select_treatment_goal(main_goal, metals, sulfate, suspended_solids, initial_ph, heavy_metals_total, hardness_total)
steps        = process_train(main_goal, metals, initial_ph, target_final_ph, preferred_base, preferred_acid, heavy_metals_total, suspended_solids)
drivers      = decision_drivers(main_goal, metals, sulfate, suspended_solids, initial_ph, target_final_ph, heavy_metals_total, hardness_total)
ph_strategy  = ph_adjustment_strategy(initial_ph, target_final_ph, preferred_base, preferred_acid)
iex_score, iex_status, iex_comments = iex_suitability(target_final_ph, suspended_solids, hardness_total, heavy_metals_total)
lang_est     = capex_opex_estimate(equipment_cost_keur, flowrate, preferred_base, chemical_unit_cost, energy_price_eur_kwh, "Lang" if cost_method=="Lang Factor" else "Hand-Chilton")
need_low_precip  = (metals["Fe"]+metals["Al"]+metals["Cu"]) > THRESH["fe_al_cu_precip"]
need_high_precip = (metals["Ni"]+metals["Co"]+metals["Mn"]) > THRESH["ni_co_mn_precip"]
chem_est     = chemical_consumption(flowrate, initial_ph, target_final_ph, preferred_base, preferred_acid,
                   suspended_solids, metals, heavy_metals_total, hardness_total, sulfate,
                   need_low_precip, need_high_precip, preferred_base)

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
      <img src="data:image/png;base64,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" style="height:52px;" alt="Adven">
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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Results Overview",
    "Process Train",
    "Block Flow Diagram",
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
# TAB 2 — Process Train (dynamic)
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">Suggested Process Train</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.85rem;color:#555;margin-bottom:12px;">Steps are generated dynamically from the feed composition entered in the sidebar. Change any parameter and the process train updates automatically.</div>', unsafe_allow_html=True)
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
# TAB 3 — Block Flow Diagram
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Block Flow Diagram — Auto-generated from Process Train</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.85rem;color:#555;margin-bottom:16px;">The BFD below updates automatically based on your feed composition and treatment objective. Each block represents a process unit; streams flow left to right.</div>', unsafe_allow_html=True)

    # ── Build BFD blocks from process steps ──
    def classify_step(s):
        s_lo = s.lower()
        if "equali" in s_lo:                                return ("Feed", "#5c8a8a", "●")
        if "bag" in s_lo or "cartridge" in s_lo or "strainer" in s_lo or "screen" in s_lo:
            return ("Coarse\nFiltration", "#5c8a8a", "▣")
        if "coagulat" in s_lo or "flocculat" in s_lo:      return ("Coag /\nFloc", "#5c8a8a", "◈")
        if "stage 1" in s_lo or "low-ph" in s_lo or "low_ph" in s_lo or "ph 4" in s_lo:
            return ("Stage 1\nPrecip.\n(pH 4–5)", "#0F6E69", "⬡")
        if "stage 2" in s_lo or "high-ph" in s_lo or "high_ph" in s_lo or "ph 9" in s_lo:
            return ("Stage 2\nPrecip.\n(pH 9–10)", "#0F6E69", "⬡")
        if "single stage" in s_lo and ("ph 4" in s_lo or "low" in s_lo):
            return ("Precipitation\n(pH 4–5)", "#0F6E69", "⬡")
        if "single stage" in s_lo and ("ph 9" in s_lo or "high" in s_lo or "naoh" in s_lo or "ni/co/mn" in s_lo):
            return ("Precipitation\n(pH 9–10)", "#0F6E69", "⬡")
        if "lime soften" in s_lo:                           return ("Lime\nSoftening", "#0F6E69", "⬡")
        if "solid-liquid" in s_lo or "clarifi" in s_lo or "settler" in s_lo or "lamella" in s_lo or "filter press" in s_lo:
            return ("Solid-Liquid\nSep.", "#1E5053", "⬢")
        if "sand filter" in s_lo or "multimedia" in s_lo or "cartridge filter" in s_lo:
            return ("Guard\nFiltration", "#5c8a8a", "▣")
        if "ph balanc" in s_lo or "final ph" in s_lo or "ph correct" in s_lo or "recarbonation" in s_lo:
            return ("pH\nAdjust.", "#7a7a00", "◆")
        if "ion exchange" in s_lo or "iex" in s_lo or "chelating" in s_lo:
            return ("IEX\nPolishing", "#FF5F15", "⬟")
        if "naoh addition" in s_lo or "hydroxide precursor" in s_lo:
            return ("Hydroxide\nPrecip.", "#0F6E69", "⬡")
        if "na₂co₃ addition" in s_lo or "carbonate precursor" in s_lo:
            return ("Carbonate\nPrecip.", "#0F6E69", "⬡")
        if "lithium recovery" in s_lo or "li₂co₃" in s_lo:
            return ("Li₂CO₃\nRecovery", "#8B0000", "★")
        if "clean sodium" in s_lo or "product" in s_lo:    return ("Product\nNa₂SO₄", "#1a5c1a", "●")
        if "quality check" in s_lo:                         return ("Quality\nCheck", "#1a5c1a", "●")
        if "ph correction" in s_lo:                         return ("pH\nCorrection", "#7a7a00", "◆")
        if "mechanical filtration" in s_lo:                 return ("Filtration", "#5c8a8a", "▣")
        return None

    bfd_blocks = []
    for step in steps:
        cls = classify_step(step)
        if cls:
            label, color, sym = cls
            # deduplicate consecutive same labels
            if not bfd_blocks or bfd_blocks[-1][0] != label:
                bfd_blocks.append((label, color, sym))

    # ── Render as SVG ──
    BW, BH, GAP, ROWS_MAX = 110, 70, 44, 3
    # Layout: wrap into rows of max ROWS_MAX
    n = len(bfd_blocks)
    import math
    n_per_row = min(n, max(4, math.ceil(n / ROWS_MAX)))
    rows = [bfd_blocks[i:i+n_per_row] for i in range(0, n, n_per_row)]
    n_rows = len(rows)
    max_cols = max(len(r) for r in rows)

    SVG_W = max_cols * (BW + GAP) + 60
    SVG_H = n_rows  * (BH + 60) + 60

    svg_lines = [f'<svg viewBox="0 0 {SVG_W} {SVG_H}" xmlns="http://www.w3.org/2000/svg" '
                 f'style="background:#f7f4ef;border-radius:12px;font-family:Nunito Sans,sans-serif;">']

    # Title
    svg_lines.append(f'<text x="20" y="28" font-size="13" font-weight="700" fill="#1E5053">Block Flow Diagram — {main_goal[:40]}</text>')

    for ri, row in enumerate(rows):
        y_top = 50 + ri * (BH + 60)
        for ci, (label, color, sym) in enumerate(row):
            x = 20 + ci * (BW + GAP)
            cx = x + BW // 2
            cy = y_top + BH // 2

            # Block shadow
            svg_lines.append(f'<rect x="{x+3}" y="{y_top+3}" width="{BW}" height="{BH}" rx="8" fill="rgba(0,0,0,0.08)"/>')
            # Block fill
            svg_lines.append(f'<rect x="{x}" y="{y_top}" width="{BW}" height="{BH}" rx="8" fill="{color}" stroke="#fff" stroke-width="1.5"/>')

            # Label (split on \n)
            lines_lbl = label.split("\n")
            lh = 14
            start_y = cy - (len(lines_lbl)-1)*lh/2
            for li2, ln in enumerate(lines_lbl):
                svg_lines.append(f'<text x="{cx}" y="{start_y + li2*lh}" text-anchor="middle" dominant-baseline="middle" font-size="10.5" font-weight="600" fill="#ffffff">{ln}</text>')

            # Arrow to next block (same row)
            if ci < len(row)-1:
                ax1 = x + BW
                ax2 = x + BW + GAP
                ay  = y_top + BH // 2
                svg_lines.append(f'<line x1="{ax1}" y1="{ay}" x2="{ax2-6}" y2="{ay}" stroke="#1E5053" stroke-width="2"/>')
                svg_lines.append(f'<polygon points="{ax2},{ay} {ax2-8},{ay-4} {ax2-8},{ay+4}" fill="#1E5053"/>')

        # Down-arrow to next row
        if ri < n_rows - 1:
            last_ci = len(row) - 1
            lx = 20 + last_ci * (BW + GAP) + BW // 2
            ly1 = y_top + BH
            ly2 = y_top + BH + 56
            # bend line to start of next row
            nx  = 20 + BW // 2
            svg_lines.append(f'<polyline points="{lx},{ly1} {lx},{ly2-28} {nx},{ly2-28} {nx},{ly2-6}" fill="none" stroke="#1E5053" stroke-width="2"/>')
            svg_lines.append(f'<polygon points="{nx},{ly2} {nx-5},{ly2-8} {nx+5},{ly2-8}" fill="#1E5053"/>')

    svg_lines.append("</svg>")
    bfd_svg = "\n".join(svg_lines)
    st.markdown(bfd_svg, unsafe_allow_html=True)

    # Legend
    legend_items = [
        ("#5c8a8a", "Feed / Filtration"), ("#0F6E69", "Precipitation / Softening"),
        ("#1E5053", "Solid-Liquid Sep."), ("#7a7a00", "pH Adjustment"),
        ("#FF5F15", "IEX Polishing"),    ("#8B0000", "Li Recovery"),
        ("#1a5c1a", "Product"),
    ]
    leg_html = '<div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:12px;">' + "".join(
        [f'<span style="display:flex;align-items:center;gap:5px;font-size:0.78rem;color:#444;">' +
         f'<span style="width:14px;height:14px;border-radius:3px;background:{c};display:inline-block;"></span>{l}</span>'
         for c,l in legend_items]) + '</div>'
    st.markdown(leg_html, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4 (was TAB 3) — CAPEX / OPEX
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">CAPEX Estimation</div>', unsafe_allow_html=True)
    method_name = lang_est["method"]
    is_hc = method_name == "Hand-Chilton"
    acc   = "±30–50%" if is_hc else "±50–100%"
    cls   = "Class 4" if is_hc else "Class 5"

    if is_hc:
        st.markdown(f"""
        <div style="font-size:0.85rem;color:#555;margin-bottom:18px;line-height:1.6;">
        <b>Hand-Chilton Method</b> (Ulrich & Vasudevan, 2004) applies individual installation factors per equipment category.
        More accurate than the simple Lang factor because it accounts for the different cost build-up ratios of different equipment types.
        {cls} estimate, accuracy {acc}.
        <br><em>TIC = Σ (equipment fraction × Hand-Chilton factor × C_equip)</em>
        </div>""", unsafe_allow_html=True)
        # Show breakdown
        hc_rows = [{"Equipment Category": k, "Equip. cost (k€)": v["equip_keur"],
                     "H-C Factor": v["factor"], "Installed cost (k€)": v["installed_keur"]}
                   for k, v in lang_est["hc_breakdown"].items()]
        hc_rows.append({"Equipment Category": "TOTAL", "Equip. cost (k€)": equipment_cost_keur,
                         "H-C Factor": "—", "Installed cost (k€)": lang_est["capex_hc_keur"]})
        st.dataframe(pd.DataFrame(hc_rows), use_container_width=True, hide_index=True)
    else:
        st.markdown(f"""
        <div style="font-size:0.85rem;color:#555;margin-bottom:18px;line-height:1.6;">
        <b>Lang Factor Method</b> (Peters, Timmerhaus & West, 5th Ed.) multiplies purchased equipment cost
        by a single factor covering all installation costs. Lang factor = <b>{lang_est["lang_factor"]}</b> for fluid-process plants.
        {cls} estimate, accuracy {acc}.
        <br><em>CAPEX = {equipment_cost_keur:.0f} k€ × {lang_est["lang_factor"]} = <b>{lang_est["capex_keur"]:.0f} k€</b></em>
        </div>""", unsafe_allow_html=True)

    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        st.markdown(f"""<div class="cost-card" style="border-top:4px solid #1E5053;">
          <div class="cost-title">CAPEX ({method_name})</div>
          <div class="cost-value">{lang_est["capex_keur"]:,.0f}<span class="cost-unit">k€</span></div>
          <div class="cost-note">Accuracy: {acc}</div></div>""", unsafe_allow_html=True)
    with col_c2:
        st.markdown(f"""<div class="cost-card" style="border-top:4px solid #FF5F15;">
          <div class="cost-title">Annual OPEX</div>
          <div class="cost-value">{lang_est["opex_keur_yr"]:,.1f}<span class="cost-unit">k€/yr</span></div>
          <div class="cost-note">{lang_est["opex_eur_m3"]:.3f} €/m³ · 8,000 h/yr</div></div>""", unsafe_allow_html=True)
    with col_c3:
        payback = lang_est["capex_keur"] / lang_est["opex_keur_yr"] if lang_est["opex_keur_yr"] > 0 else 0
        st.markdown(f"""<div class="cost-card" style="border-top:4px solid #0F6E69;">
          <div class="cost-title">Reference Payback</div>
          <div class="cost-value">{payback:.1f}<span class="cost-unit">yr</span></div>
          <div class="cost-note">CAPEX / OPEX ratio (illustrative)</div></div>""", unsafe_allow_html=True)

    if is_hc:
        st.markdown(f"""<div style="font-size:0.82rem;color:#888;margin:8px 0 16px 0;">
        Lang equivalent: {lang_est["capex_lang_keur"]:,.0f} k€ | 
        Hand-Chilton: {lang_est["capex_hc_keur"]:,.0f} k€ | 
        Difference: {abs(lang_est["capex_hc_keur"]-lang_est["capex_lang_keur"]):,.0f} k€</div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">OPEX Breakdown</div>', unsafe_allow_html=True)
    opex_df = pd.DataFrame({
        "Cost Item":  ["Chemicals (base/acid)", "Energy (pump + aeration est.)", "Labour + Maintenance (5% CAPEX/yr)", "Total OPEX"],
        "k€/yr":      [lang_est["chem_cost_keur_yr"], lang_est["energy_cost_keur_yr"],
                       lang_est["labour_maint_keur_yr"], lang_est["opex_keur_yr"]]
    })
    st.dataframe(opex_df, use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div class="custom-disclaimer" style="margin-top:16px;">
    📌 <strong>Methodology:</strong> {cls} ({acc}) — early-stage screening only.
    Lang: Peters, Timmerhaus & West, <em>Plant Design and Economics for Chemical Engineers</em>, 5th Ed.
    Hand-Chilton: Ulrich & Vasudevan, <em>Chemical Engineering Process Design and Economics</em>, 2nd Ed., 2004.
    A proper Class 3 estimate requires vendor quotations, detailed P&IDs, and site-specific data.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 5 — Chemical Consumption
# ══════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">Chemical Consumption — Full Mass Balance (8,000 h/yr)</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.85rem;color:#555;margin-bottom:16px;line-height:1.6;">All chemical quantities calculated from feed composition mass balance. IEX resin sized from actual metal equivalents load. <b>Confirm all doses by jar testing and vendor data before design.</b></div>', unsafe_allow_html=True)

    # Separate IEX from regular chemicals
    chem_regular = {k:v for k,v in chem_est.items() if k != "iex_resin"}
    iex_data     = chem_est.get("iex_resin", None)

    if not chem_regular and not iex_data:
        st.markdown('<div class="result-card">No significant chemical addition required for current inputs.</div>', unsafe_allow_html=True)

    # Regular chemicals table
    if chem_regular:
        st.markdown('<div class="section-header" style="font-size:1rem;">Process Chemicals</div>', unsafe_allow_html=True)
        chem_rows = []
        for key, val in chem_regular.items():
            chem_rows.append({
                "Chemical":        val["reagent"],
                "kg/m³":           val["kg_per_m3"],
                "kg/h":            val["kg_per_h"],
                "t/yr":            val["t_per_yr"],
                "Note":            val.get("note",""),
            })
        st.dataframe(pd.DataFrame(chem_rows), use_container_width=True, hide_index=True)

    # IEX resin section
    if iex_data:
        st.markdown('<div class="section-header" style="font-size:1rem;">IEX Resin & Regeneration (8,000 h/yr, 48h cycle)</div>', unsafe_allow_html=True)
        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        with col_r1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Resin Volume</div><div class="metric-value">{iex_data["resin_volume_L"]:,.0f}</div><div class="metric-sub">litres</div></div>', unsafe_allow_html=True)
        with col_r2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Regenerations/yr</div><div class="metric-value">{iex_data["regen_per_yr"]:.0f}</div><div class="metric-sub">cycles/yr</div></div>', unsafe_allow_html=True)
        with col_r3:
            st.markdown(f'<div class="metric-card accent"><div class="metric-label">H₂SO₄ regen.</div><div class="metric-value">{iex_data["h2so4_regen_t_yr"]:.1f}</div><div class="metric-sub">t/yr</div></div>', unsafe_allow_html=True)
        with col_r4:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Resin replacement</div><div class="metric-value">{iex_data["resin_replace_keur_yr"]:.1f}</div><div class="metric-sub">k€/yr (~25%/yr)</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="custom-disclaimer" style="margin-top:8px;">⚙️ {iex_data["note"]}</div>', unsafe_allow_html=True)

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
# TAB 6 — Summary Report
# ══════════════════════════════════════════════
with tab6:
    st.markdown('<div class="section-header">Concept Summary Report</div>', unsafe_allow_html=True)
    chem_lines = ""
    for key, val in chem_est.items():
        if key == "iex_resin":
            chem_lines += (f"  - {val['reagent']}: {val['resin_volume_L']:.0f} L resin | "
                           f"{val['regen_per_yr']:.0f} regen/yr | "
                           f"{val['h2so4_regen_t_yr']:.2f} t H₂SO₄/yr | "
                           f"resin replacement {val['resin_replace_keur_yr']:.1f} k€/yr\n")
        else:
            chem_lines += f"  - {val['reagent']}: {val['kg_per_m3']} kg/m³ | {val['kg_per_h']} kg/h | {val['t_per_yr']} t/yr\n"
    if not chem_lines:
        chem_lines = "  No major chemical addition required with current inputs.\n"

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
