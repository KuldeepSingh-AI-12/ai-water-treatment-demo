# Sodium Sulfate Polishing & Heavy Metal Removal Demo  
### (Black Mass Refinery – Conceptual Engineering Tool)

This project is a **Streamlit-based screening tool** for treating sulfate-rich industrial streams, inspired by typical **battery recycling / black mass refinery leachates**.

The tool focuses on **multi-stage precipitation + filtration + ion exchange polishing** to achieve a **clean sodium sulfate solution**.

---

## 🔍 Objective

To simulate a **realistic industrial treatment route** for:

- Removal of residual heavy metals (Ni, Co, Mn, Fe, Al, Cu)
- Control of hardness (Ca, Mg)
- Production of a **clean Na₂SO₄-rich solution**
- Evaluation of **IEX polishing suitability**

---

## ⚙️ What the Tool Does

The application takes inputs such as:

- Flowrate
- Initial and target pH
- Metal concentrations (Li, Ni, Co, Mn, Fe, Al, Cu, Ca, Mg)
- Sulfate concentration
- Suspended solids
- Chemical selection (NaOH / Lime / Na₂CO₃ / acids)

Based on this, it:

- Suggests a **complete treatment train**
- Simulates **multi-stage precipitation**
- Estimates **metal removal per stage**
- Evaluates **ion exchange suitability**
- Highlights **process risks and limitations**

---

## 🏗️ Typical Process Configuration

The tool reflects a realistic industrial approach:
Bag / cartridge filtration
→ Stage 1: Low-pH precipitation (Fe, Al, Cu)
→ Solid-liquid separation
→ Stage 2: High-pH precipitation (Ni, Co, Mn)
→ Coagulation / flocculation (if needed)
→ Clarifier / filter press
→ Sand / multimedia filtration
→ pH adjustment (IEX-compatible range)
→ Chelating ion exchange polishing
→ Clean sodium sulfate solution

---

## 🧪 Engineering Basis

The logic is based on established principles:

### 1. Multi-stage precipitation
- Fe³⁺, Al³⁺, Cu²⁺ → precipitate at lower pH
- Ni²⁺, Co²⁺ → require higher pH
- Mn²⁺ → most difficult, may need higher pH or oxidation

### 2. Filtration importance
- Suspended solids must be removed before IEX
- Protects resin from fouling and pressure drop

### 3. Ion exchange polishing
Chelating ion exchange resins are used for:
- Final removal of trace heavy metals
- Polishing sodium sulfate solutions

Example: Lewatit® TP 208 is used for removal of heavy metals and alkaline earth ions from brine and process streams. It operates across a wide pH range and is commonly applied in polishing applications. 

### 4. Hardness impact
- Ca²⁺ and Mg²⁺:
  - Increase sludge formation
  - Compete on resin
  - Reduce IEX efficiency

---

## 📊 Key Features

- Stage-wise removal estimation:
  - Low-pH precipitation
  - High-pH precipitation
  - IEX polishing
- IEX suitability scoring
- pH adjustment strategy (NaOH vs acid)
- Risk identification:
  - Scaling
  - Fouling
  - Incomplete removal
- Process decision logic

---

## ⚠️ Important Disclaimer

This tool is a **conceptual and educational simulator only**.

- It is entirely hypothetical  
- It is NOT based on any real industrial stream, project, or company data  
- It does NOT include rigorous thermodynamic or kinetic modeling  

For real applications, the following are required:

- Full water chemistry analysis  
- Speciation modeling (e.g., PHREEQC)  
- Jar testing / pilot trials  
- Resin supplier validation  
- Sludge handling assessment  
- Safety and environmental review  

---

## 🌐 Live Demo

👉 https://ai-water-treatment-demo-fmx6c4qvrcamqu35kxdxoh.streamlit.app/

---

## 🛠️ Technologies

- Python  
- Streamlit  
- Pandas  

---

## 💡 Why This Project

This project demonstrates how **domain knowledge + simple logic models** can be translated into:

- Practical engineering tools  
- Early-stage decision support systems  
- Digital concept screening platforms  

It also shows the potential to integrate:

👉 AI-assisted process selection  
👉 Automated treatment train generation  
👉 Engineering copilots for water treatment  

---

## 🚀 Future Improvements

- Thermodynamic modeling (PHREEQC integration)
- Sludge production estimation
- Chemical dosing calculation (NaOH, acid)
- Resin breakthrough modeling
- Cost estimation (CAPEX / OPEX)
- AI-based decision assistant
