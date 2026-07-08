# ============================================================================
# WEEK 7 CHECKPOINT - VALIDATION
# ============================================================================
#
# Assumes `metrics` and `SESSION_ID` are already in scope.

print("WEEK 7 CHECKPOINT - Verification")
print("=" * 60)

checks = []

# Check 1: Metrics collector exists
checks.append(("MetricsCollector initialized", metrics is not None))

# Check 2: Latencies recorded
try:
    has_latencies = len(metrics.latencies) > 0
    checks.append(("Latencies recorded", has_latencies))
except:
    checks.append(("Latencies recorded", False))

# Check 3: Success rates recorded
try:
    has_successes = len(metrics.successes) > 0 or len(metrics.failures) > 0
    checks.append(("Success rates recorded", has_successes))
except:
    checks.append(("Success rates recorded", False))

# Check 4: Summary works
try:
    summary = metrics.get_summary()
    checks.append(("get_summary() works", 'latencies' in summary and 'success_rates' in summary))
except:
    checks.append(("get_summary() works", False))

# Check 5: Session ID exists
checks.append(("Session tracking active", SESSION_ID is not None))

# Display results
all_passed = True
for check_name, check_result in checks:
    status = "PASS" if check_result else "FAIL"
    print(f"  [{status}] {check_name}")
    if not check_result:
        all_passed = False

print("\n" + "=" * 60)
if all_passed:
    print("ALL WEEK 7 CHECKPOINTS PASSED! Ready for Week 8.")
else:
    print("Some checkpoints FAILED. Review your implementation above.")
