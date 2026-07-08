# ============================================================================
# WEEK 7.4: SIMULATED METRICS
# ============================================================================
#
# Assumes `metrics` (week7_metrics_collector.py), `langfuse`, and
# `SESSION_ID` are already in scope.

import random

# Simulate some metrics (in production, these would come from actual operations)
print("\nSIMULATED METRICS COLLECTION")
print("=" * 60)

operations = ['embedding', 'legal_agent', 'financial_agent', 'operational_agent', 'search']

for _ in range(20):
    op = random.choice(operations)
    latency = random.uniform(100, 2000)  # 100ms to 2s
    success = random.random() > 0.1  # 90% success rate

    metrics.record_latency(op, latency)
    metrics.record_success(op, success)

# Get summary
summary = metrics.get_summary()

print(f"\nSession Duration: {summary['session_duration']:.1f} seconds")
print("\nLatencies (avg ms):")
for op, data in summary['latencies'].items():
    print(f"  {op}: {data['avg_ms']:.1f}ms ({data['count']} calls)")

print("\nSuccess Rates:")
for op, data in summary['success_rates'].items():
    print(f"  {op}: {data['rate']*100:.1f}% ({data['total']} total)")

# Log metrics to Langfuse
langfuse.trace(
    name="metrics-summary",
    session_id=SESSION_ID,
    input={"type": "metrics"},
    output=summary
)

langfuse.flush()
