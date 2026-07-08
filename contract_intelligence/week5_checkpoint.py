# ============================================================================
# WEEK 5 CHECKPOINT - VALIDATION
# ============================================================================
#
# Assumes `orchestrator` and `orch_result` are already in scope from
# earlier notebook cells.

print("WEEK 5 CHECKPOINT - Verification")
print("=" * 60)

checks = []

# Check 1: Orchestrator initialized
checks.append(("Orchestrator initialized", orchestrator is not None))

# Check 2: Risk weights configured
try:
    has_weights = len(orchestrator.risk_weights) == 3
    checks.append(("Risk weights configured", has_weights))
except:
    checks.append(("Risk weights configured", False))

# Check 3: Orchestration produced results
try:
    checks.append(("Orchestration completed", orch_result is not None))
except:
    checks.append(("Orchestration completed", False))

# Check 4: All agents ran
try:
    if orch_result:
        agent_count = len(orch_result.get('results', {}))
        checks.append(("All 3 agents ran", agent_count == 3))
    else:
        checks.append(("All 3 agents ran", False))
except:
    checks.append(("All 3 agents ran", False))

# Check 5: Composite score calculated
try:
    if orch_result:
        score = orch_result.get('composite_score', 0)
        checks.append(("Composite score valid", 1.0 <= score <= 4.0))
    else:
        checks.append(("Composite score valid", False))
except:
    checks.append(("Composite score valid", False))

# Check 6: Overall risk determined
try:
    if orch_result:
        risk = orch_result.get('overall_risk', '')
        valid_risks = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        checks.append(("Overall risk determined", risk in valid_risks))
    else:
        checks.append(("Overall risk determined", False))
except:
    checks.append(("Overall risk determined", False))

# Display results
all_passed = True
for check_name, check_result in checks:
    status = "PASS" if check_result else "FAIL"
    print(f"  [{status}] {check_name}")
    if not check_result:
        all_passed = False

print("\n" + "=" * 60)
if all_passed:
    print("ALL WEEK 5 CHECKPOINTS PASSED! Ready for Week 6.")
else:
    print("Some checkpoints FAILED. Review your implementation above.")
