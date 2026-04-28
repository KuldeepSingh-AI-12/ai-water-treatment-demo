# Cr(VI) Treatment Selection Demo

This is a simple Streamlit-based tool for preliminary screening of hexavalent chromium (Cr(VI)) removal from industrial water streams.

## What the tool does

The application takes basic water quality and process inputs:

- Flowrate
- Inlet Cr(VI) concentration
- Target outlet concentration
- pH
- Sulfate concentration
- COD (organic load)
- Resin bed volume and depth

Based on these inputs, it:

- Suggests a treatment route
- Explains the reasoning behind the selection
- Performs basic hydraulic checks (BV/h, EBCT)
- Provides a simplified ion exchange capacity estimate
- Highlights potential risks (fouling, competing ions, pH limits)

## Treatment options considered

The tool uses rule-based logic to recommend among:

- Chemical reduction + Cr(III) precipitation
- Ion exchange (strong-base anion resin)
- Adsorption / polishing
- Combined treatment approaches

## Engineering logic

The decision is based on:

- Cr(VI) concentration level
- Required removal efficiency
- Organic load (COD → fouling risk)
- Competing ions (e.g., sulfate)
- pH conditions

This mimics an early-stage process selection approach used in concept development.

## Important note

This is a **screening-level tool only**.

Final process design requires:
- Full water chemistry analysis
- Pilot or laboratory testing
- Resin supplier validation
- Safety and environmental assessment

## Live demo

You can access the app here:

👉 https://ai-water-treatment-demo-fmx6c4qvrcamqu35kxdxoh.streamlit.app/

## Technologies used

- Python
- Streamlit
- Pandas

## Why this project

This project demonstrates how rule-based logic can support early-stage decision-making in industrial water treatment and process engineering.

It is intended as a simple example of digital tools applied to real engineering problems.
