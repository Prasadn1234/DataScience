# ============================================================================
# WEEK 2 CHECKPOINT - VALIDATION
# ============================================================================
#
# Assumes `doc_processor`, `all_docs_flat`, and `entity_extractor` are
# already in scope from the earlier Week 2.x cells.

print("WEEK 2 CHECKPOINT - Verification")
print("=" * 60)

checks = []

# Check 1: Document processor exists
checks.append(("DocumentProcessor initialized", doc_processor is not None))

# Check 2: load_docx method works
try:
    # Test with sample text (doesn't need real file)
    test_result = doc_processor.load_docx is not None
    checks.append(("load_docx() method exists", test_result))
except:
    checks.append(("load_docx() method exists", False))

# Check 3: Documents processed
checks.append(("Documents processed", len(all_docs_flat) > 0))

# Check 4: Entity extractor works
try:
    test_entities = entity_extractor.extract_entities("Contract value is $100,000")
    has_monetary = 'monetary_values' in test_entities
    checks.append(("Entity extraction works", has_monetary))
except Exception as e:
    checks.append(("Entity extraction works", False))
    print(f"  Error: {e}")

# Check 5: Risk assessment works
try:
    test_risks = entity_extractor.assess_risk_indicators("unlimited liability clause")
    has_high = len(test_risks.get('high_risk', [])) > 0
    checks.append(("Risk assessment works", has_high))
except Exception as e:
    checks.append(("Risk assessment works", False))
    print(f"  Error: {e}")

# Display results
all_passed = True
for check_name, check_result in checks:
    status = "PASS" if check_result else "FAIL"
    print(f"  [{status}] {check_name}")
    if not check_result:
        all_passed = False

print("\n" + "=" * 60)
if all_passed:
    print("ALL WEEK 2 CHECKPOINTS PASSED! Ready for Week 3.")
else:
    print("Some checkpoints FAILED. Review your implementation above.")
