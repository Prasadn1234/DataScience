# ============================================================================
# WEEK 8.1: PRODUCTION SYSTEM CLASS
# ============================================================================
#
# Assumes `doc_processor`, `entity_extractor`, `vector_store`,
# `orchestrator`, `contract_kg`, and `metrics` (all Week 2-7 instances)
# are already in scope.
#
# Design note: the hints only gave method signatures, not detailed
# behavior, so this ties every earlier subsystem together as the natural
# top-level entry point: analyze_contract() runs entity/risk-indicator
# extraction, multi-agent risk orchestration, and knowledge-graph
# registration in one call, timing and recording success/failure via the
# Week 7 MetricsCollector; search_contracts() wraps the vector store;
# get_system_status() reports a snapshot across all subsystems.

import time
from typing import Dict


class ContractIntelligenceSystem:
    """
    Production entry point for the ContractIQ pipeline.
    """

    def __init__(self):
        self.doc_processor = doc_processor
        self.entity_extractor = entity_extractor
        self.vector_store = vector_store
        self.orchestrator = orchestrator
        self.knowledge_graph = contract_kg
        self.metrics = metrics

    def analyze_contract(self, contract_text: str, contract_id: str = "uploaded") -> Dict:
        """
        Run the full analysis pipeline on a contract's text: entity and
        risk-indicator extraction, multi-agent risk orchestration, and
        knowledge graph registration.

        Args:
            contract_text: Full contract text
            contract_id: Identifier for tracing/knowledge graph

        Returns:
            Dictionary with entities, risk indicators, and orchestration results
        """
        start = time.time()
        success = False
        try:
            entities = self.entity_extractor.extract_entities(contract_text)
            risk_indicators = self.entity_extractor.assess_risk_indicators(contract_text)

            orchestration = self.orchestrator.analyze_parallel(contract_text, contract_id)

            self.knowledge_graph.add_contract({
                'doc_id': contract_id,
                'filename': contract_id,
                'category': 'uploaded',
            })

            success = True
            return {
                'contract_id': contract_id,
                'entities': entities,
                'risk_indicators': risk_indicators,
                'overall_risk': orchestration['overall_risk'],
                'composite_score': orchestration['composite_score'],
                'agent_results': orchestration['results'],
                'consensus': orchestration['consensus'],
            }
        finally:
            elapsed_ms = (time.time() - start) * 1000
            self.metrics.record_latency('analyze_contract', elapsed_ms)
            self.metrics.record_success('analyze_contract', success)

    def search_contracts(self, query: str, n_results: int = 5) -> Dict:
        """
        Semantic search across all indexed contracts.

        Args:
            query: Search query text
            n_results: Number of results to return

        Returns:
            Dictionary with the query and its results
        """
        start = time.time()
        success = False
        try:
            results = self.vector_store.search("contracts_all", query, n_results=n_results)
            success = True
            return {'query': query, 'results': results}
        finally:
            elapsed_ms = (time.time() - start) * 1000
            self.metrics.record_latency('search_contracts', elapsed_ms)
            self.metrics.record_success('search_contracts', success)

    def get_system_status(self) -> Dict:
        """
        Snapshot of the system's current state.

        Returns:
            Dictionary with documents processed, knowledge graph size,
            and aggregated operation metrics
        """
        return {
            'documents_processed': len(self.doc_processor.processed_docs),
            'knowledge_graph_nodes': self.knowledge_graph.graph.number_of_nodes(),
            'knowledge_graph_edges': self.knowledge_graph.graph.number_of_edges(),
            'metrics_summary': self.metrics.get_summary(),
        }


print("ContractIntelligenceSystem class defined")
