# ============================================================================
# WEEK 6.2: KNOWLEDGE GRAPH METHODS
# ============================================================================
#
# Assumes `ContractKnowledgeGraph` (week6_knowledge_graph.py) is already
# in scope.

from typing import Dict, List


def add_contract(self, doc: Dict):
    """
    Add a contract document to the knowledge graph.

    Args:
        doc: Document dictionary with doc_id, filename, category
    """

    doc_id = doc.get('doc_id', 'UNKNOWN')

    # Add contract node
    self.graph.add_node(
        doc_id,
        type='CONTRACT',
        color='#2ecc71',
        filename=doc.get('filename', ''),
    )

    # Link to category
    category = doc.get('category', 'unknown')
    if category not in self.graph:
        self.graph.add_node(category, type='CATEGORY', color='#1abc9c')
    self.graph.add_edge(doc_id, category, relation='BELONGS_TO')

def get_risk_mitigations(self, risk: str) -> List[str]:
    """
    Get clauses that mitigate a specific risk.

    Args:
        risk: Risk type name

    Returns:
        List of mitigating clause names
    """

    mitigations = []
    for source, _target, data in self.graph.in_edges(risk, data=True):
        if data.get('relation') == 'MITIGATES':
            mitigations.append(source)

    return mitigations

def get_clause_concerns(self, clause: str) -> List[str]:
    """
    Get concerns addressed by a clause type.

    Args:
        clause: Clause type name

    Returns:
        List of concern names
    """

    concerns = []
    for _source, target, data in self.graph.out_edges(clause, data=True):
        if data.get('relation') == 'ADDRESSES':
            concerns.append(target)

    return concerns

# Add methods to class
ContractKnowledgeGraph.add_contract = add_contract
ContractKnowledgeGraph.get_risk_mitigations = get_risk_mitigations
ContractKnowledgeGraph.get_clause_concerns = get_clause_concerns

print("Query methods added to ContractKnowledgeGraph")
