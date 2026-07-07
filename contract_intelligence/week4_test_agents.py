# ============================================================================
# WEEK 4.6: TEST AGENTS
# ============================================================================
#
# Assumes `legal_agent`, `financial_agent`, `operational_agent` (instances
# of the three Week 4.x agent classes), `all_docs_flat`, and `langfuse` are
# already in scope. Real ChatOpenAI calls inside analyze() need a valid
# OPENAI_API_KEY at runtime.

print("TESTING RISK ASSESSMENT AGENTS")
print("=" * 60)

# Get test contract text
if all_docs_flat:
    test_text = all_docs_flat[0]['full_text']
    test_id = all_docs_flat[0]['doc_id']
else:
    test_text = "Sample contract with liability and payment terms."
    test_id = "TEST-001"

print(f"Testing on document: {test_id}")
print(f"Text length: {len(test_text)} characters")

# Test Legal Agent
print("\n" + "-" * 40)
print("LEGAL RISK AGENT")
print("-" * 40)
try:
    legal_result = legal_agent.analyze(test_text[:8000], test_id)
    print(f"Risk Level: {legal_result.risk_level}")
    print(f"Contract Type: {legal_result.contract_type}")
    print(f"Confidence: {legal_result.confidence}")
except Exception as e:
    print(f"Error: {e}")
    legal_result = None

# Test Financial Agent
print("\n" + "-" * 40)
print("FINANCIAL RISK AGENT")
print("-" * 40)
try:
    financial_result = financial_agent.analyze(test_text[:8000], test_id)
    print(f"Risk Level: {financial_result.risk_level}")
    print(f"Contract Value: {financial_result.total_contract_value}")
    print(f"Confidence: {financial_result.confidence}")
except Exception as e:
    print(f"Error: {e}")
    financial_result = None

# Test Operational Agent
print("\n" + "-" * 40)
print("OPERATIONAL RISK AGENT")
print("-" * 40)
try:
    operational_result = operational_agent.analyze(test_text[:8000], test_id)
    print(f"Risk Level: {operational_result.risk_level}")
    print(f"Service Scope: {operational_result.service_scope[:100]}...")
    print(f"Confidence: {operational_result.confidence}")
except Exception as e:
    print(f"Error: {e}")
    operational_result = None

langfuse.flush()
print("\nAll agent traces sent to Langfuse!")
