# ============================================================================
# INITIALIZE ORCHESTRATOR
# ============================================================================
#
# Assumes `ContractRiskOrchestrator` (week5_orchestrator.py), and
# `legal_agent`, `financial_agent`, `operational_agent`, `vector_store`
# (earlier Week 3-4 cells) are already in scope.

# Create orchestrator
orchestrator = ContractRiskOrchestrator()

print("ContractRiskOrchestrator initialized")
print(f"  Risk weights: {orchestrator.risk_weights}")
