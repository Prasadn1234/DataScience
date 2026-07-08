# ============================================================================
# WEEK 7.2: ADD CUSTOM SCORES
# ============================================================================
#
# Assumes `orch_result`, `langfuse`, and `SESSION_ID` are already in scope.

print("\nADDING CUSTOM SCORES TO TRACES")
print("=" * 60)

# Score the orchestration result

if 'orch_result' in dir() and orch_result:
    doc_id = orch_result['doc_id']
    overall_risk = orch_result['overall_risk']

    # Map risk to score (higher = better/lower risk)
    risk_score_map = {
        'LOW': 1.0,
        'MEDIUM': 0.7,
        'HIGH': 0.4,
        'CRITICAL': 0.1,
        'UNKNOWN': 0.5
    }

    score = risk_score_map.get(overall_risk, 0.5)

    # Create trace and add score
    score_trace = langfuse.trace(
        name=f"risk-scoring-{doc_id}",
        session_id=SESSION_ID,
        input={"doc_id": doc_id, "overall_risk": overall_risk},
    )
    langfuse.score(
        trace_id=score_trace.id,
        name="contract-risk-score",
        value=score,
        comment=f"Overall risk: {overall_risk}, composite score: {orch_result.get('composite_score')}",
    )

    print(f"\nScored {doc_id}:")
    print(f"  Risk Level: {overall_risk}")
    print(f"  Score: {score}")
else:
    print("No orchestration results to score.")

langfuse.flush()
print("\nScores sent to Langfuse!")
