# ============================================================================
# WEEK 2.2: PROCESS ALL DOCUMENTS
# ============================================================================
#
# Assumes `contract_files` (from week1_data_discovery.py), `doc_processor`'s
# class `ContractDocumentProcessor` (from week2_document_processor.py), and
# `langfuse` are already in scope from earlier notebook cells.

# Initialize processor
doc_processor = ContractDocumentProcessor()

print("PROCESSING CONTRACT DOCUMENTS")
print("=" * 60)

# Process all categories
all_contract_docs = {}
for category, files in contract_files.items():
    if files:
        all_contract_docs[category] = doc_processor.process_category(files, category)
        print(f"{category}: {len(all_contract_docs[category])} documents processed")

# Flatten all documents
all_docs_flat = []
for docs in all_contract_docs.values():
    all_docs_flat.extend(docs)

print(f"\n" + "=" * 60)
print(f"TOTAL DOCUMENTS PROCESSED: {len(all_docs_flat)}")

# If no real documents, create sample data
if not all_docs_flat:
    print("\nNo documents found - creating sample data for demonstration...")
    sample_contract_text = """
MASTER SERVICE AGREEMENT

This Master Service Agreement ("Agreement") is entered into as of January 1, 2024
between TechCorp Inc. ("Client") and ServicePro LLC ("Provider").

1. DEFINITIONS
   "Services" means the professional services described in any Statement of Work.
   "Confidential Information" means any non-public information disclosed by either party.

2. SERVICES AND DELIVERABLES
   Provider shall perform the Services described in each Statement of Work.
   All deliverables shall meet the specifications set forth in the applicable SOW.

3. PAYMENT TERMS
   Client shall pay Provider within Net 30 days of invoice receipt.
   Late payments shall accrue interest at 1.5% per month.
   Total contract value: $500,000 over 24 months.

4. LIABILITY
   Provider's total liability shall not exceed the fees paid in the prior 12 months.
   Neither party shall be liable for consequential, indirect, or punitive damages.

5. INDEMNIFICATION
   Each party shall indemnify the other against third-party claims arising from
   their negligence or willful misconduct.

6. TERMINATION
   Either party may terminate with 30 days written notice.
   Client may terminate for cause immediately upon material breach.
"""

    all_docs_flat = [{
        'doc_id': 'SAMPLE-001',
        'filename': 'sample_msa.docx',
        'category': 'master_agreements',
        'full_text': sample_contract_text,
        'table_text': '',
        'sections': [{'header': '1. DEFINITIONS', 'position': 0}],
        'word_count': len(sample_contract_text.split())
    }]

    print(f"Sample document created with {all_docs_flat[0]['word_count']} words")

langfuse.flush()
