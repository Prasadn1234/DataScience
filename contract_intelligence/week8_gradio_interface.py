# ============================================================================
# WEEK 8.2: GRADIO INTERFACE
# ============================================================================
#
# Assumes `contract_system` (week8_init_system.py) is already in scope.
#
# Only the two UI function signatures were hinted, so the shape of a
# readable text summary (rather than a raw dict/JSON dump) and the Blocks
# layout are design choices. demo.launch() is left out of this cell -
# construct the interface here, launch it from a separate cell.

import gradio as gr


def analyze_contract_ui(contract_text: str) -> str:
    """
    Gradio-facing wrapper around ContractIntelligenceSystem.analyze_contract().
    """
    if not contract_text or not contract_text.strip():
        return "Please paste contract text to analyze."

    try:
        result = contract_system.analyze_contract(contract_text, contract_id="ui-upload")
    except Exception as e:
        return f"Analysis failed: {e}"

    lines = [
        f"Overall Risk: {result['overall_risk']}",
        f"Composite Score: {result['composite_score']:.2f}",
        "",
        "Agent Results:",
    ]
    for agent_name, agent_result in result['agent_results'].items():
        if agent_result and agent_result.get('result'):
            risk = agent_result['result'].get('risk_level', 'N/A')
            lines.append(f"  - {agent_name}: {risk}")
        else:
            lines.append(f"  - {agent_name}: failed")

    if result['consensus'].get('key_findings'):
        lines.append("")
        lines.append("Key Findings:")
        for finding in result['consensus']['key_findings']:
            lines.append(f"  - {finding}")

    if result['consensus'].get('all_recommendations'):
        lines.append("")
        lines.append("Recommendations:")
        for rec in result['consensus']['all_recommendations']:
            lines.append(f"  - {rec}")

    return "\n".join(lines)


def search_contracts_ui(query: str) -> str:
    """
    Gradio-facing wrapper around ContractIntelligenceSystem.search_contracts().
    """
    if not query or not query.strip():
        return "Please enter a search query."

    try:
        search_result = contract_system.search_contracts(query, n_results=5)
    except Exception as e:
        return f"Search failed: {e}"

    results = search_result['results']
    if not results:
        return "No results found."

    lines = [f"Results for: '{query}'", ""]
    for i, r in enumerate(results, 1):
        filename = r['metadata'].get('filename', 'unknown')
        category = r['metadata'].get('category', 'unknown')
        similarity = r['similarity']
        preview = r['document'][:150]
        lines.append(f"{i}. {filename} ({category}) - similarity: {similarity:.3f}")
        lines.append(f"   {preview}...")
        lines.append("")

    return "\n".join(lines)


# Build the Gradio interface
with gr.Blocks(title="ContractIQ") as demo:
    gr.Markdown("# ContractIQ: AI-Driven Contract Intelligence")

    with gr.Tab("Analyze Contract"):
        contract_input = gr.Textbox(label="Contract Text", lines=15, placeholder="Paste contract text here...")
        analyze_button = gr.Button("Analyze")
        analyze_output = gr.Textbox(label="Analysis Result", lines=20)
        analyze_button.click(fn=analyze_contract_ui, inputs=contract_input, outputs=analyze_output)

    with gr.Tab("Search Contracts"):
        search_input = gr.Textbox(label="Search Query", placeholder="e.g. payment terms and liability")
        search_button = gr.Button("Search")
        search_output = gr.Textbox(label="Search Results", lines=20)
        search_button.click(fn=search_contracts_ui, inputs=search_input, outputs=search_output)

print("Gradio interface defined")
