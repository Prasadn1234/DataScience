# ============================================================================
# VISUALIZE KNOWLEDGE GRAPH
# ============================================================================
#
# Assumes `contract_kg` is already in scope (from week6_build_kg.py).

print("KNOWLEDGE GRAPH VISUALIZATION")
print("=" * 60)

# Create visualizations
try:
    contract_kg.visualize_matplotlib()
except Exception as e:
    print(f"Matplotlib visualization error: {e}")

try:
    contract_kg.visualize_interactive("contract_knowledge_graph.html")
except Exception as e:
    print(f"PyVis visualization error: {e}")
