"""Claude-backed contract analysis shared by the Streamlit UI and the API."""

from anthropic import Anthropic

from models import ContractAnalysis

MODEL = "claude-sonnet-5"

ANALYSIS_TOOL = {
    "name": "record_contract_analysis",
    "description": "Record a structured analysis of a contract.",
    "input_schema": ContractAnalysis.model_json_schema(),
}


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
