# ============================================================================
# INITIALIZE AND POPULATE KNOWLEDGE GRAPH
# ============================================================================
#
# Assumes `ContractKnowledgeGraph` (week6_knowledge_graph.py + methods from
# week6_kg_methods.py), `all_docs_flat`, `langfuse`, and `SESSION_ID` are
# already in scope.

# Create knowledge graph
contract_kg = ContractKnowledgeGraph()

# Add all processed contracts
for doc in all_docs_flat:
    contract_kg.add_contract(doc)

# Log to Langfuse
langfuse.trace(
    name="knowledge-graph-built",
    session_id=SESSION_ID,
    input={"contracts_added": len(all_docs_flat)},
    output={
        "nodes": contract_kg.graph.number_of_nodes(),
        "edges": contract_kg.graph.number_of_edges()
    }
)

print(f"Contract Knowledge Graph Built:")
print(f"  Nodes: {contract_kg.graph.number_of_nodes()}")
print(f"  Edges: {contract_kg.graph.number_of_edges()}")
