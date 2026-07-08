# ============================================================================
# WEEK 5.1: MULTI-AGENT ORCHESTRATOR
# ============================================================================
#
# Assumes `legal_agent`, `financial_agent`, `operational_agent`, and
# `vector_store` are already in scope from earlier notebook cells.
#
# Note: the class docstring's TODO list also mentions analyze_parallel(),
# _build_consensus(), and _calculate_composite_score(), but only
# _execute_agent() was part of the pasted skeleton, so only that is
# implemented here. Share the other stubs separately and they can be added.

from enum import Enum
from typing import Dict

from tenacity import retry, stop_after_attempt, wait_exponential
import concurrent.futures


class RiskDimension(Enum):
    """Risk dimensions for orchestration."""
    LEGAL = "legal"
    FINANCIAL = "financial"
    OPERATIONAL = "operational"


class ContractRiskOrchestrator:
    """
    Multi-agent orchestrator with parallel execution.
    """

    def __init__(self):
        self.legal_agent = legal_agent
        self.financial_agent = financial_agent
        self.operational_agent = operational_agent
        self.vector_store = vector_store

        # Risk weights (provided)
        self.risk_weights = {
            RiskDimension.LEGAL: 0.4,       # Legal carries most weight
            RiskDimension.FINANCIAL: 0.35,  # Financial is second
            RiskDimension.OPERATIONAL: 0.25 # Operational is third
        }

        # Risk level scores (provided)
        self.risk_scores = {
            'LOW': 1,
            'MEDIUM': 2,
            'HIGH': 3,
            'CRITICAL': 4
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _execute_agent(self, agent_type: RiskDimension, contract_text: str, doc_id: str) -> Dict:
        """
        Execute a single agent with retry logic.

        Args:
            agent_type: Which agent to run
            contract_text: Contract to analyze
            doc_id: Document identifier

        Returns:
            Dictionary with agent type and result
        """

        try:
            # Select and run appropriate agent
            if agent_type == RiskDimension.LEGAL:
                result = self.legal_agent.analyze(contract_text, doc_id)
            elif agent_type == RiskDimension.FINANCIAL:
                result = self.financial_agent.analyze(contract_text, doc_id)
            elif agent_type == RiskDimension.OPERATIONAL:
                result = self.operational_agent.analyze(contract_text, doc_id)
            else:
                raise ValueError(f"Unknown agent type: {agent_type}")

            return {
                'agent': agent_type.value,
                'result': result.model_dump() if result else None
            }

        except Exception as e:
            print(f"Agent {agent_type.value} failed: {e}")
            raise  # Re-raise for retry


print("ContractRiskOrchestrator class started")
print("TODO: Implement analyze_parallel(), _build_consensus(), _calculate_composite_score()")


# ============================================================================
# WEEK 5.2: PARALLEL EXECUTION METHOD
# ============================================================================
#
# References self._build_consensus() and self._calculate_composite_score(),
# which aren't implemented yet (not part of any pasted skeleton so far).
# Python only resolves those at call time, so this method can be added now
# and wired up correctly once those two land.

def analyze_parallel(self, contract_text: str, doc_id: str) -> Dict:
    """
    Run all agents in parallel and build consensus.

    Args:
        contract_text: Contract to analyze
        doc_id: Document identifier

    Returns:
        Dictionary with all results, consensus, and composite score
    """

    # Create orchestration trace
    trace = langfuse.trace(
        name=f"orchestration-{doc_id}",
        session_id=SESSION_ID,
        input={"doc_id": doc_id, "text_length": len(contract_text)}
    )

    results = {}

    # Run agents in parallel using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all agent tasks
        futures = {
            executor.submit(self._execute_agent, agent_type, contract_text, doc_id): agent_type
            for agent_type in RiskDimension
        }

        # Collect results as they complete
        for future in concurrent.futures.as_completed(futures):
            agent_type = futures[future]
            try:
                # Store the full {'agent': ..., 'result': ...} dict returned by
                # _execute_agent - _build_consensus/_calculate_composite_score
                # expect to reach into result['result']. Keyed by agent_type.value
                # (a plain string) so results prints/iterates cleanly downstream.
                results[agent_type.value] = future.result()
            except Exception as e:
                print(f"Agent {agent_type.value} failed after retries: {e}")
                results[agent_type.value] = None

    # Build consensus
    consensus = self._build_consensus(results)

    # Calculate composite score
    composite_score = self._calculate_composite_score(results)

    # Determine overall risk level
    if composite_score < 1.5:
        overall_risk = "LOW"
    elif composite_score < 2.5:
        overall_risk = "MEDIUM"
    elif composite_score < 3.5:
        overall_risk = "HIGH"
    else:
        overall_risk = "CRITICAL"

    # Update trace
    trace.update(output={
        "overall_risk": overall_risk,
        "composite_score": composite_score
    })

    return {
        'doc_id': doc_id,
        'results': results,
        'consensus': consensus,
        'composite_score': composite_score,
        'overall_risk': overall_risk
    }

# Add method to class
ContractRiskOrchestrator.analyze_parallel = analyze_parallel

print("analyze_parallel() method added")


# ============================================================================
# WEEK 5.3: CONSENSUS BUILDING
# ============================================================================

def _build_consensus(self, results: Dict) -> Dict:
    """
    Build consensus from multiple agent results.

    Args:
        results: Dictionary of agent results ({str agent name: {'agent', 'result'} or None})

    Returns:
        Consensus dictionary with aggregated findings
    """

    consensus = {
        'risk_levels': {},
        'key_findings': [],
        'all_recommendations': []
    }

    # Field per model that best summarizes its headline risk, for key_findings
    highlight_field = {
        'legal': 'liability_exposure',
        'financial': 'financial_exposure',
        'operational': 'service_scope',
    }
    # Different models name their remediation list differently
    recommendation_fields = ('recommended_changes', 'mitigation_strategies')

    # Extract risk level from each agent result
    for dimension, result in results.items():
        if result and 'result' in result and result['result']:
            agent_name = result['agent']
            inner = result['result']

            risk_level = inner.get('risk_level')
            consensus['risk_levels'][agent_name] = risk_level

            field = highlight_field.get(agent_name)
            if field and inner.get(field):
                consensus['key_findings'].append(f"{agent_name}: {risk_level} risk - {inner[field]}")

            # Aggregate recommendations from all agents
            for rec_field in recommendation_fields:
                consensus['all_recommendations'].extend(inner.get(rec_field, []))

    # Flag when agents agree, since that's the strongest signal for common themes
    levels_seen = list(consensus['risk_levels'].values())
    if len(levels_seen) > 1 and len(set(levels_seen)) == 1:
        consensus['key_findings'].append(f"All agents agree: {levels_seen[0]} risk")

    return consensus

# Add method to class
ContractRiskOrchestrator._build_consensus = _build_consensus


def _calculate_composite_score(self, results: Dict) -> float:
    """
    Calculate weighted composite risk score.

    Args:
        results: Dictionary of agent results ({str agent name: {'agent', 'result'} or None})

    Returns:
        Weighted composite score (1.0 to 4.0)

    Formula:
    composite = sum(weight * risk_score) for each agent
    """

    total_weight = 0
    weighted_sum = 0

    # Calculate weighted sum, skipping any dimension whose agent failed or
    # returned an unrecognized risk level
    for dimension in RiskDimension:
        result = results.get(dimension.value)
        if not result or not result.get('result'):
            continue

        risk_level = result['result'].get('risk_level')
        score = self.risk_scores.get(risk_level)
        if score is None:
            continue

        weight = self.risk_weights[dimension]
        weighted_sum += weight * score
        total_weight += weight

    # Avoid division by zero
    if total_weight == 0:
        return 2.5  # Default to medium

    return weighted_sum / total_weight

# Add methods to class
ContractRiskOrchestrator._calculate_composite_score = _calculate_composite_score

print("Consensus methods added")
