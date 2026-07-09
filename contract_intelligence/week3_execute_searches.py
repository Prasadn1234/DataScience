# ============================================================================
# EXECUTE SEARCHES
# ============================================================================
#
# Assumes `vector_store`, `test_queries`, and `langfuse` are already in
# scope. Uses vector_store.search_traced(), which returns the raw
# ChromaDB query result shape (documents/metadatas/distances as
# lists-of-lists) rather than search()'s flattened list of dicts.

for i, query in enumerate(test_queries, 1):
    print(f"\n[Query {i}] '{query}'")
    print("-" * 60)

    results = vector_store.search_traced("contracts_all", query, n_results=2)

    if results['documents'] and results['documents'][0]:
        for j, (doc, meta, dist) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            similarity = 1 - dist
            print(f"\n  Result {j+1} (Similarity: {similarity:.3f})")
            print(f"  Source: {meta['filename']} ({meta['category']})")
            print(f"  Preview: {doc[:150]}...")
    else:
        print("  No results found")

langfuse.flush()
