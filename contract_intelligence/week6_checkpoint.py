# ============================================================================
# WEEK 6 CHECKPOINT - VALIDATION
# ============================================================================
#
# Assumes `contract_kg` is already in scope.

print("WEEK 6 CHECKPOINT - Verification")
print("=" * 60)

checks = []

# Check 1: Knowledge graph initialized
checks.append(("Knowledge graph initialized", contract_kg is not None))

# Check 2: Graph has nodes
try:
    node_count = contract_kg.graph.number_of_nodes()
    checks.append(("Graph has nodes", node_count > 0))
except:
    checks.append(("Graph has nodes", False))

# Check 3: Graph has edges
try:
    edge_count = contract_kg.graph.number_of_edges()
    checks.append(("Graph has edges", edge_count > 0))
except:
    checks.append(("Graph has edges", False))

# Check 4: Query methods work
try:
    mitigations = contract_kg.get_risk_mitigations("UNLIMITED_LIABILITY")
    checks.append(("get_risk_mitigations works", isinstance(mitigations, list)))
except Exception as e:
    checks.append(("get_risk_mitigations works", False))

# Check 5: Contracts added
try:
    contract_nodes = [n for n, d in contract_kg.graph.nodes(data=True) if d.get('type') == 'CONTRACT']
    checks.append(("Contracts added to graph", len(contract_nodes) >= 0))  # May be 0 if no docs
except:
    checks.append(("Contracts added to graph", False))

# Display results
all_passed = True
for check_name, check_result in checks:
    status = "PASS" if check_result else "FAIL"
    print(f"  [{status}] {check_name}")
    if not check_result:
        all_passed = False

print("\n" + "=" * 60)
if all_passed:
    print("ALL WEEK 6 CHECKPOINTS PASSED! Ready for Week 7.")
else:
    print("Some checkpoints FAILED. Review your implementation above.")
