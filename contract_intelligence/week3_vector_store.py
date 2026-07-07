# ============================================================================
# WEEK 3.1: CHROMADB VECTOR STORE
# ============================================================================
#
# Assumes `langfuse`, `SESSION_ID`, and `traced_embedding(text, name)` (a
# Langfuse-traced embedding call, presumably wrapping the OpenAI
# text-embedding-3-small client) are already defined by earlier notebook
# cells.
#
# Note: `search_with_filter()` is mentioned in the class docstring's TODO
# list but wasn't part of the pasted skeleton, so it isn't implemented
# here. Share that stub separately and it can be added.

from typing import Dict, List

import chromadb


class ContractVectorStore:
    """
    ChromaDB-based vector store with Langfuse observability.
    """

    def __init__(self, persist_directory: str = "./chroma_contracts_db"):
        """
        Initialize ChromaDB with persistent storage.
        """

        # Create persistent client
        self.client = chromadb.PersistentClient(path=persist_directory)

        self.embedding_model = "text-embedding-3-small"
        self.collections = {}

        # Log initialization to Langfuse
        langfuse.trace(
            name="vectorstore-init",
            session_id=SESSION_ID,
            input={"persist_directory": persist_directory}
        )

        print(f"ChromaDB initialized at: {persist_directory}")

    def create_collection(self, name: str):
        """
        Create or get a collection.

        Args:
            name: Collection name

        Returns:
            ChromaDB collection
        """

        # ChromaDB defaults to L2 distance; force cosine so that
        # similarity = 1 - distance (used in search()) is meaningful.
        collection = self.client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"},
        )

        self.collections[name] = collection
        return collection

    def add_documents(self, collection_name: str, documents: List[Dict]):
        """
        Index documents into a collection.

        Args:
            collection_name: Target collection name
            documents: List of document dictionaries
        """

        # Create trace for indexing
        trace = langfuse.trace(
            name=f"index-{collection_name}",
            session_id=SESSION_ID,
            input={"doc_count": len(documents)}
        )

        # Get or create collection
        collection = self.create_collection(collection_name)

        ids = []
        embeddings = []
        docs = []
        metadatas = []

        for i, doc in enumerate(documents):
            # Generate embedding (text truncated to stay under embedding-model limits)
            truncated_text = doc['full_text'][:8000]
            embedding = traced_embedding(truncated_text, f"embed-{doc['doc_id']}")

            # Prepare metadata
            metadata = {
                "filename": doc.get("filename", ""),
                "category": doc.get("category", ""),
                "word_count": doc.get("word_count", 0),
            }

            ids.append(doc["doc_id"])
            embeddings.append(embedding)
            docs.append(truncated_text)
            metadatas.append(metadata)

            # Progress indicator
            if (i + 1) % 5 == 0:
                print(f"  Indexed {i + 1}/{len(documents)} documents...")

        # Add all to collection
        if ids:
            collection.add(ids=ids, embeddings=embeddings, documents=docs, metadatas=metadatas)

        trace.update(output={"indexed": len(documents)})
        print(f"Indexed {len(documents)} documents into '{collection_name}'")

    def search(self, collection_name: str, query: str, n_results: int = 5) -> List[Dict]:
        """
        Semantic search across documents.

        Args:
            collection_name: Collection to search
            query: Search query text
            n_results: Number of results to return

        Returns:
            List of result dictionaries with document, metadata, and score
        """

        # Create trace for search
        trace = langfuse.trace(
            name="semantic-search",
            session_id=SESSION_ID,
            input={"query": query, "collection": collection_name}
        )

        # Get collection
        collection = self.collections.get(collection_name) or self.create_collection(collection_name)

        # Generate query embedding
        query_embedding = traced_embedding(query, "query-embedding")

        # Query collection
        results = collection.query(query_embeddings=[query_embedding], n_results=n_results)

        # Format results
        formatted = []
        result_docs = results.get("documents") or [[]]
        result_metadatas = results.get("metadatas") or [[]]
        result_distances = results.get("distances") or [[]]

        for document, metadata, distance in zip(result_docs[0], result_metadatas[0], result_distances[0]):
            formatted.append({
                "document": document,
                "metadata": metadata,
                "similarity": 1 - distance,
            })

        trace.update(output={"results_count": len(formatted)})
        return formatted


print("ContractVectorStore class defined")
