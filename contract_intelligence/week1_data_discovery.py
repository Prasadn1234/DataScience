# ============================================================================
# WEEK 1.6: DATA DISCOVERY FUNCTION
# ============================================================================
#
# Assumes `langfuse`, `SESSION_ID`, and `IN_COLAB` are already defined by
# earlier Week 1 setup cells in the ContractIQ notebook.
#
# Root cause of "Total files discovered: 0":
#   DATA_DIR pointed at MyDrive/data/, which was empty (no category
#   subfolders). The 36 real contract documents are flat files in
#   MyDrive/Datasets/, categorized only by filename keyword (e.g.
#   "MSA sample 1.docx", "Redlined contract sample 2.docx"), not by
#   subfolder. This version matches files by filename pattern per the 8
#   categories from the ContractIQ problem statement, while still
#   supporting a subfolder-per-category layout if you organize the data
#   that way later.
import re
from pathlib import Path
from typing import Dict, List

CONTRACT_CATEGORIES: Dict[str, Dict[str, object]] = {
    "master_level_agreements": {
        "folder": "master_level_agreements",
        "patterns": [r"\bmsa\b", r"\bnda\b", r"rate\s*card"],
    },
    "transaction_contracts": {
        "folder": "transaction_contracts",
        "patterns": [r"\bsow\b", r"contract\s*renewal"],
    },
    "commercial_documents": {
        "folder": "commercial_documents",
        "patterns": [r"pricing\s*table"],
    },
    "financial_and_billing": {
        "folder": "financial_and_billing",
        "patterns": [r"invoice", r"credit\s*note", r"billing\s*schedule"],
    },
    "operational_documents": {
        "folder": "operational_documents",
        "patterns": [r"service\s*report", r"incident\s*(and)?\s*problem"],
    },
    "compliance_documents": {
        "folder": "compliance_documents",
        "patterns": [r"infosec", r"vend\w*\s*mgt\s*policy", r"industry\s*specific"],
    },
    "negotiation_history": {
        "folder": "negotiation_history",
        "patterns": [r"email\s*negotiation", r"redlined", r"risk\s*assessment"],
    },
    "governance": {
        "folder": "governance",
        "patterns": [r"post\s*project\s*review", r"renewal\s*negotiation\s*notes"],
    },
}

_EXTENSIONS = ("*.docx", "*.pdf", "*.xlsx")


def discover_contract_data(data_dir: Path) -> Dict[str, List[Path]]:
    """
    Discover all contract documents organized by category.
    """
    # 1. Create trace for data discovery
    trace = langfuse.trace(
        name="data-discovery",
        session_id=SESSION_ID,
        metadata={
            "data_dir": str(data_dir),
            "project": "contract-intel",
        },
    )
    # 2. Initialize discovered dictionary
    discovered: Dict[str, List[Path]] = {cat: [] for cat in CONTRACT_CATEGORIES.keys()}
    # 3. Check if data directory exists
    if not data_dir.exists():
        trace.update(
            output={
                "status": "missing_directory",
                "total_files": 0,
                "by_category": {cat: 0 for cat in discovered},
            }
        )
        print(f"Warning: Data directory not found: {data_dir}")
        return discovered

    # 4. Gather every candidate file once
    all_files: List[Path] = []
    for pattern in _EXTENSIONS:
        all_files.extend(data_dir.rglob(pattern))
    all_files = sorted(set(all_files))

    compiled_patterns = {
        cat: [re.compile(p, re.IGNORECASE) for p in info["patterns"]]
        for cat, info in CONTRACT_CATEGORIES.items()
    }
    folder_to_category = {
        info["folder"]: cat for cat, info in CONTRACT_CATEGORIES.items()
    }

    unmatched: List[Path] = []
    for file_path in all_files:
        # Prefer subfolder-per-category layout when present
        category = folder_to_category.get(file_path.parent.name.lower())
        if category is None:
            # Fall back to matching the filename against category keyword patterns
            stem = file_path.stem
            category = next(
                (
                    cat
                    for cat, patterns in compiled_patterns.items()
                    if any(p.search(stem) for p in patterns)
                ),
                None,
            )
        if category is not None:
            discovered[category].append(file_path)
        else:
            unmatched.append(file_path)

    for cat in discovered:
        discovered[cat] = sorted(set(discovered[cat]))

    # 5. Calculate and log totals
    totals_by_category = {cat: len(files) for cat, files in discovered.items()}
    total_files = sum(totals_by_category.values())
    trace.update(
        output={
            "status": "success",
            "total_files": total_files,
            "by_category": totals_by_category,
            "unmatched_files": [str(p) for p in unmatched],
        }
    )
    if unmatched:
        print(f"Note: {len(unmatched)} file(s) didn't match any category pattern:")
        for p in unmatched:
            print(f"  - {p}")
    return discovered


# Set up data path
if IN_COLAB:
    # Real contract documents live in MyDrive/Datasets/, not MyDrive/data/
    # (the latter was empty - that's why discovery returned 0 files before).
    DATA_DIR = Path("/content/drive/MyDrive/Datasets")
else:
    DATA_DIR = Path("../data")

# Run discovery
contract_files = discover_contract_data(DATA_DIR)
print("\nDiscovery Summary:")
total = 0
for cat, files in contract_files.items():
    if files:
        print(f"  {cat}: {len(files)} files")
        total += len(files)
print(f"\nTotal files discovered: {total}")
