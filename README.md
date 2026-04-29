# Heavy Metal Precipitation Demo (Black Mass Refinery – Hypothetical Case)

This is a simple Streamlit-based tool for **screening heavy metal removal** from a hypothetical black mass refinery wastewater stream.

The focus is on **hydroxide precipitation using pH adjustment** and basic process logic.

---

## What the tool does

The application takes basic inputs such as:

- Flowrate
- Initial pH and target precipitation pH
- Alkali type (NaOH or lime)
- Metal concentrations:
  - Ni, Co, Mn (target metals)
  - Fe, Al (co-precipitation support)
  - Ca, Mg (hardness / scaling risk)
- Sulfate concentration (sodium sulfate matrix)

Based on these inputs, it:

- Suggests a treatment route
- Explains the reasoning behind the selection
- Estimates which metals will precipitate at the selected pH
- Provides a simplified metal removal estimate
- Highlights risks such as:
  - Scaling (Ca/Mg)
  - Sludge generation
  - Incomplete Mn removal
- Suggests a process train
- Recommends polishing (e.g., ion exchange) if needed

---

## Typical treatment concept

The tool reflects a simplified process approach:
