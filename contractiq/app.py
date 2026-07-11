"""ContractIQ: AI-Driven Contract Intelligence.

Streamlit app that lets a user paste contract text and get a structured
AI analysis: parties, key dates, obligations, risky clauses, and a summary.
"""

import json
import os

import streamlit as st

from analyzer import analyze_contract
from models import ContractAnalysis

RISK_COLOR = {"low": "🟢", "medium": "🟡", "high": "🔴"}


def render_analysis(analysis: ContractAnalysis) -> None:
    st.subheader(f"{analysis.contract_type}")
    st.write(analysis.summary)

    st.markdown("**Parties**")
    st.write(", ".join(analysis.parties) if analysis.parties else "—")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Key Dates**")
        if analysis.key_dates:
            for kd in analysis.key_dates:
                st.write(f"- **{kd.description}:** {kd.date}")
        else:
            st.write("—")

    with col2:
        st.markdown("**Obligations**")
        if analysis.obligations:
            for ob in analysis.obligations:
                st.write(f"- **{ob.party}:** {ob.obligation}")
        else:
            st.write("—")

    st.markdown("**Risk Flags**")
    if analysis.risks:
        for risk in analysis.risks:
            icon = RISK_COLOR.get(risk.risk_level.lower(), "⚪")
            with st.expander(f"{icon} {risk.risk_level.upper()} — {risk.clause}"):
                st.write(risk.explanation)
    else:
        st.write("No notable risks flagged.")

    st.markdown("**Recommended Actions**")
    if analysis.recommended_actions:
        for action in analysis.recommended_actions:
            st.write(f"- {action}")
    else:
        st.write("—")


def main() -> None:
    st.set_page_config(page_title="ContractIQ", page_icon="📄", layout="wide")
    st.title("ContractIQ: AI-Driven Contract Intelligence")

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    with st.sidebar:
        st.header("Settings")
        api_key_input = st.text_input(
            "Anthropic API Key",
            value=api_key,
            type="password",
            help="Reads from ANTHROPIC_API_KEY by default; you can override it here.",
        )
        api_key = api_key_input or api_key

    st.header("Analyze Contract")
    contract_text = st.text_area(
        "Contract Text",
        height=350,
        placeholder="Paste the full text of the contract here...",
    )

    if st.button("Analyze Contract", type="primary"):
        if not contract_text.strip():
            st.warning("Please paste some contract text to analyze.")
        elif not api_key:
            st.error("Please provide an Anthropic API key in the sidebar.")
        else:
            with st.spinner("Analyzing contract..."):
                try:
                    analysis = analyze_contract(contract_text, api_key)
                except Exception as exc:  # surfaces API/parsing errors to the user
                    st.error(f"Analysis failed: {exc}")
                else:
                    render_analysis(analysis)
                    with st.expander("Raw analysis (JSON)"):
                        st.code(json.dumps(analysis.model_dump(), indent=2), language="json")


if __name__ == "__main__":
    main()
