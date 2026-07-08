# ============================================================================
# WEEK 7.3: METRICS COLLECTOR
# ============================================================================

from typing import Dict, List
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class MetricsCollector:
    """
    Collect and aggregate system metrics.
    """

    latencies: Dict[str, List[float]] = field(default_factory=dict)
    successes: Dict[str, int] = field(default_factory=dict)
    failures: Dict[str, int] = field(default_factory=dict)
    start_time: datetime = field(default_factory=datetime.now)

    def record_latency(self, operation: str, latency_ms: float):
        """
        Record latency for an operation.
        """
        if operation not in self.latencies:
            self.latencies[operation] = []
        self.latencies[operation].append(latency_ms)

    def record_success(self, operation: str, success: bool):
        """
        Record success or failure for an operation.
        """
        if success:
            self.successes[operation] = self.successes.get(operation, 0) + 1
        else:
            self.failures[operation] = self.failures.get(operation, 0) + 1

    def get_summary(self) -> Dict:
        """
        Get aggregated metrics summary.

        Returns dict with:
        - avg_latency per operation
        - success_rate per operation
        - total_operations
        """

        summary = {
            'session_duration': (datetime.now() - self.start_time).total_seconds(),
            'latencies': {},
            'success_rates': {}
        }

        # Calculate average latencies
        for op, times in self.latencies.items():
            summary['latencies'][op] = {
                'avg_ms': sum(times) / len(times) if times else 0,
                'count': len(times)
            }

        # Calculate success rates
        for op in set(list(self.successes.keys()) + list(self.failures.keys())):
            s = self.successes.get(op, 0)
            f = self.failures.get(op, 0)
            total = s + f
            summary['success_rates'][op] = {
                'rate': s / total if total > 0 else 0,
                'total': total
            }

        return summary


# Initialize metrics collector
metrics = MetricsCollector()

print("MetricsCollector initialized")
