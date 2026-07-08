# ============================================================================
# KNOWLEDGE GRAPH QUERIES
# ============================================================================
#
# Assumes `contract_kg` and `langfuse` are already in scope.

print("\nKNOWLEDGE GRAPH QUERIES")
print("=" * 60)

# Query 1: Risk mitigations
print("\n1. Risk Mitigation Strategies:")
for risk in ['UNLIMITED_LIABILITY', 'IP_INFRINGEMENT', 'DATA_BREACH']:
    mitigations = contract_kg.get_risk_mitigations(risk)
    print(f"   {risk}: {mitigations}")

# Query 2: Clause concerns
print("\n2. Clause Concerns:")
for clause in ['INDEMNIFICATION', 'CONFIDENTIALITY', 'TERMINATION']:
    concerns = contract_kg.get_clause_concerns(clause)
    print(f"   {clause}: {concerns}")

# Query 3: Graph statistics
print("\n3. Graph Statistics:")
print(f"   Total nodes: {contract_kg.graph.number_of_nodes()}")
print(f"   Total edges: {contract_kg.graph.number_of_edges()}")

# Node type distribution
type_counts = {}
for _, data in contract_kg.graph.nodes(data=True):
    t = data.get('type', 'OTHER')
    type_counts[t] = type_counts.get(t, 0) + 1

print("\n4. Node Type Distribution:")
for t, count in sorted(type_counts.items()):
    print(f"   {t}: {count}")

langfuse.flush()
