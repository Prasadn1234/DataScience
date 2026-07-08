# ============================================================================
# WEEK 7.1: OBSERVABILITY SUMMARY
# ============================================================================
#
# Assumes `SESSION_ID` and `os` are already in scope.
#
# Trace names below were cross-checked against the actual langfuse.trace()/
# trace_name= calls in the Week 1-6 implementations in this repo. The Week 4
# names were corrected (were "legal-agent-{doc_id}" etc., actual code uses
# "legal-risk-analysis-{doc_id}" etc.). "entity-extraction-batch" under Week 2
# doesn't correspond to any langfuse call in week2_entity_extractor.py as
# implemented here - left as-is since it may belong to a cell not shared in
# this session, but worth double-checking against your actual notebook.

print("LANGFUSE OBSERVABILITY SUMMARY")
print("=" * 70)
print(f"\nSession ID: {SESSION_ID}")
print(f"\nTraces created during this session:")
print()
print("Week 1: Environment Setup")
print("  - taxonomy-definition")
print("  - data-discovery")
print("  - test-embedding-*, test-completion-*")
print()
print("Week 2: Document Processing & EDA")
print("  - process-{category}")
print("  - entity-extraction-batch")
print()
print("Week 3: Vector Store & Embeddings")
print("  - vectorstore-init")
print("  - index-contracts_all")
print("  - embed-{doc_id}")
print("  - semantic-search")
print()
print("Week 4: Single Agent Design")
print("  - legal-risk-analysis-{doc_id}")
print("  - financial-risk-analysis-{doc_id}")
print("  - operational-risk-analysis-{doc_id}")
print()
print("Week 5: Multi-Agent Orchestration")
print("  - orchestration-{doc_id}")
print()
print("Week 6: Knowledge Graph")
print("  - knowledge-graph-init")
print("  - knowledge-graph-built")
print()
print(f"View all traces at: {os.environ.get('LANGFUSE_HOST')}/project")
