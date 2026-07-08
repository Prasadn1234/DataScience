# ============================================================================
# WEEK 5.4: TEST ORCHESTRATION
# ============================================================================
#
# Assumes `orchestrator`, `all_docs_flat`, and `langfuse` are already in
# scope from earlier notebook cells.

print("MULTI-AGENT ORCHESTRATION TEST")
print("=" * 60)

# Get test contract
if all_docs_flat:
    test_doc = all_docs_flat[0]
    test_text = test_doc['full_text']
    test_id = test_doc['doc_id']
else:
    test_text = "Sample contract text"
    test_id = "TEST-001"

print(f"Analyzing document: {test_id}")
print(f"Text length: {len(test_text)} characters")
print("\nRunning agents in parallel...")
print("-" * 40)

# Run orchestration
try:
    orch_result = orchestrator.analyze_parallel(test_text[:8000], test_id)

    print("\nORCHESTRATION RESULTS")
    print("=" * 60)
    print(f"Overall Risk: {orch_result['overall_risk']}")
    print(f"Composite Score: {orch_result['composite_score']:.2f}")

    print("\nIndividual Agent Results:")
    for agent, result in orch_result['results'].items():
        if result and 'result' in result:
            risk = result['result'].get('risk_level', 'N/A')
            conf = result['result'].get('confidence', 0)
            print(f"  {agent}: {risk} (confidence: {conf:.2f})")

    print("\nConsensus:")
    print(f"  Risk Levels: {orch_result['consensus'].get('risk_levels', {})}")

except Exception as e:
    print(f"Orchestration failed: {e}")
    orch_result = None

langfuse.flush()
print("\nOrchestration trace sent to Langfuse!")
