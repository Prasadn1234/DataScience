# ============================================================================
# WEEK 2.1: DOCUMENT PROCESSOR CLASS
# ============================================================================
#
# Note: `process_category()` is mentioned in the class docstring's
# "YOU MUST IMPLEMENT" list but wasn't part of the pasted skeleton, so it
# isn't implemented here. Share that stub separately and it can be added.

from pathlib import Path
from typing import Any, Dict, List, Optional

from docx import Document as DocxDocument
import re
import hashlib


class ContractDocumentProcessor:
    """
    Production-grade document processor for contract analysis.

    YOU MUST IMPLEMENT:
    - load_docx(): Load and parse a DOCX file
    - extract_tables(): Extract text from tables
    - extract_sections(): Identify document sections
    - process_category(): Process all documents in a category
    """

    def __init__(self):
        self.supported_formats = ['.docx']
        self.processed_docs = []

        # Section header patterns (PROVIDED)
        self.section_patterns = [
            r'^(\d+\.\s+[A-Z][A-Z\s]+)$',      # "1. DEFINITIONS"
            r'^(\d+\.\d+\s+.+)$',              # "1.1 Term"
            r'^(ARTICLE\s+[IVXLCDM]+)',          # "ARTICLE I"
            r'^(SECTION\s+\d+)',                # "SECTION 1"
            r'^(Schedule\s+[A-Z0-9]+)',          # "Schedule A"
            r'^(Exhibit\s+[A-Z0-9]+)',           # "Exhibit A"
        ]

    def load_docx(self, file_path: Path, trace_parent=None) -> Optional[Dict[str, Any]]:
        """
        Load and parse a DOCX contract file.

        Args:
            file_path: Path to the DOCX file
            trace_parent: Parent trace for nested spans

        Returns:
            Dictionary with parsed document data, or None on error
        """

        # Create span for tracing (if parent exists)
        span = trace_parent.span(name=f"load-{file_path.name}") if trace_parent else None

        try:
            # Load the DOCX file
            doc = DocxDocument(file_path)

            # Extract paragraph text
            full_text = "\n".join(
                p.text for p in doc.paragraphs if p.text.strip()
            )

            # Extract table text
            table_text = self.extract_tables(doc)

            # Generate unique doc_id
            doc_id = hashlib.md5(file_path.name.encode("utf-8")).hexdigest()

            # Extract sections
            sections = self.extract_sections(full_text)

            # End span if exists
            if span:
                span.end(output={"status": "success", "text_length": len(full_text)})

            return {
                'doc_id': doc_id,
                'filename': file_path.name,
                'file_path': str(file_path),
                'full_text': full_text,
                'table_text': table_text,
                'sections': sections,
                'word_count': len(full_text.split())
            }

        except Exception as e:
            if span:
                span.end(output={"status": "error", "error": str(e)})
            print(f"Error loading {file_path}: {e}")
            return None

    def extract_tables(self, doc) -> str:
        """
        Extract text from all tables in a document.

        Args:
            doc: A python-docx Document object

        Returns:
            String containing all table text
        """
        table_texts = []

        for table in doc.tables:
            for row in table.rows:
                cells = [cell.text.strip() for cell in row.cells]
                table_texts.append(" | ".join(cells))

        return "\n".join(table_texts)

    def extract_sections(self, text: str) -> List[Dict[str, str]]:
        """
        Extract sections from document text using regex patterns.

        Args:
            text: Full document text

        Returns:
            List of dictionaries with section info
        """
        sections: List[Dict[str, str]] = []
        compiled_patterns = [re.compile(p) for p in self.section_patterns]

        current_header: Optional[str] = None
        current_lines: List[str] = []
        current_start: int = 0

        for position, line in enumerate(text.split("\n")):
            stripped = line.strip()
            match = next(
                (p.match(stripped) for p in compiled_patterns if p.match(stripped)),
                None,
            )
            if match:
                if current_header is not None:
                    sections.append({
                        "header": current_header,
                        "content": "\n".join(current_lines).strip(),
                        "start_line": current_start,
                    })
                current_header = match.group(1)
                current_lines = []
                current_start = position
            elif current_header is not None:
                current_lines.append(line)

        if current_header is not None:
            sections.append({
                "header": current_header,
                "content": "\n".join(current_lines).strip(),
                "start_line": current_start,
            })

        return sections


print("ContractDocumentProcessor class defined")
