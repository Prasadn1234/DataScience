"""ContractIQ: AI-Driven Contract Intelligence.

Streamlit app that lets a user paste contract text and get a structured
AI analysis: parties, key dates, obligations, risky clauses, and a summary.
"""

import json
import os

import streamlit as st
from anthropic import Anthropic
from pydantic import BaseModel, Field

MODEL = "claude-sonnet-5"


class KeyDate(BaseModel):
    description: str = Field(description="What the date represents, e.g. 'Effective date'")
    date: str = Field(description="The date or deadline as written in the contract")


class Obligation(BaseModel):
    party: str = Field(description="The party responsible for the obligation")
    obligation: str = Field(description="A concise description of what they must do")


class RiskFlag(BaseModel):
    clause: str = Field(description="Short quote or reference to the clause in question")
    risk_level: str = Field(description="One of: low, medium, high")
    explanation: str = Field(description="Why this clause is risky or unusual")


class ContractAnalysis(BaseModel):
    contract_type: str = Field(description="The type of agreement, e.g. 'NDA', 'MSA', 'Lease'")
    parties: list[str] = Field(description="The parties entering into the contract")
    summary: str = Field(description="A plain-language summary of the contract, 3-5 sentences")
    key_dates: list[KeyDate] = Field(description="Important dates or deadlines in the contract")
    obligations: list[Obligation] = Field(description="Key obligations owed by each party")
    risks: list[RiskFlag] = Field(description="Clauses that are risky, unusual, or one-sided")
    recommended_actions: list[str] = Field(description="Suggested next steps before signing")


ANALYSIS_TOOL = {
    "name": "record_contract_analysis",
    "description": "Record a structured analysis of a contract.",
    "input_schema": ContractAnalysis.model_json_schema(),
}

RISK_COLOR = {"low": "🟢", "medium": "🟡", "high": "🔴"}


def analyze_contract(contract_text: str, api_key: str) -> ContractAnalysis:
    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        tools=[ANALYSIS_TOOL],
        tool_choice={"type": "tool", "name": "record_contract_analysis"},
        messages=[
            {
                "role": "user",
                "content": (
                    "Analyze the following contract and call the "
                    "record_contract_analysis tool with your findings.\n\n"
                    f"Contract Text:\n{contract_text}"
                ),
            }
        ],
    )
    for block in response.content:
        if block.type == "tool_use" and block.name == "record_contract_analysis":
            return ContractAnalysis.model_validate(block.input)
    raise ValueError("Model did not return a structured analysis.")


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
