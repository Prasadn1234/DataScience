"""In-memory store of analyzed contracts with TF-IDF based semantic search.

Kept dependency-light (scikit-learn only, no external embedding API) since
this is meant for demoing /api/search over whatever contracts have been
analyzed in the current process's lifetime.
"""

from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from models import ContractAnalysis


@dataclass
class StoredContract:
    contract_id: str
    text: str
    analysis: ContractAnalysis


class ContractStore:
    def __init__(self) -> None:
        self._contracts: dict[str, StoredContract] = {}

    def add(self, contract_id: str, text: str, analysis: ContractAnalysis) -> None:
        self._contracts[contract_id] = StoredContract(contract_id, text, analysis)

    def get(self, contract_id: str) -> StoredContract | None:
        return self._contracts.get(contract_id)

    def search(self, query: str, n_results: int = 5) -> list[tuple[StoredContract, float]]:
        if not self._contracts:
            return []

        contracts = list(self._contracts.values())
        corpus = [c.text for c in contracts] + [query]

        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(corpus)
        query_vector = tfidf_matrix[-1]
        document_vectors = tfidf_matrix[:-1]

        similarities = cosine_similarity(query_vector, document_vectors).flatten()
        ranked = sorted(zip(contracts, similarities), key=lambda pair: pair[1], reverse=True)
        return ranked[:n_results]
