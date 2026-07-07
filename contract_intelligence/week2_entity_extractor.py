# ============================================================================
# WEEK 2.4: CONTRACT ENTITY EXTRACTOR
# ============================================================================

import re
from typing import Dict, List


class ContractEntityExtractor:
    """
    Extract contract-specific entities using pattern matching.
    """

    def __init__(self):
        # Extraction patterns (PROVIDED)
        self.patterns = {
            'parties': r'(?:between|by and between)\s+([A-Z][A-Za-z\s]+(?:Inc\.|LLC|Ltd\.|Corp\.)?)',
            'effective_date': r'(?:effective\s+(?:as\s+of\s+)?(?:date)?:?\s*)(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|[A-Z][a-z]+\s+\d{1,2},?\s+\d{4})',
            'monetary_values': r'\$([\d,]+(?:\.\d{2})?)',
            'percentages': r'(\d+(?:\.\d+)?\s*%)',
            'durations': r'(\d+)\s*(?:years?|months?|days?)',
            'notice_periods': r'(?:notice\s+(?:period)?\s*(?:of)?\s*)(\d+)\s*(?:days?)',
        }

        # Risk indicators (PROVIDED)
        self.risk_indicators = {
            'high_risk': [
                'unlimited liability', 'indemnify', 'consequential damages',
                'punitive damages', 'sole discretion', 'automatic renewal'
            ],
            'medium_risk': [
                'liability cap', 'limitation of liability', 'force majeure',
                'material breach', 'termination for convenience'
            ],
            'low_risk': [
                'mutual indemnification', 'standard terms', 'annual review'
            ]
        }

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract all entities from contract text.

        Args:
            text: Contract text

        Returns:
            Dictionary mapping entity types to found values
        """
        entities = {}

        for entity_type, pattern in self.patterns.items():
            entities[entity_type] = re.findall(pattern, text, re.IGNORECASE)

        return entities

    def assess_risk_indicators(self, text: str) -> Dict[str, List[str]]:
        """
        Identify risk indicators in contract text.

        Args:
            text: Contract text

        Returns:
            Dictionary with found risk indicators by level
        """
        found_risks = {'high_risk': [], 'medium_risk': [], 'low_risk': []}
        text_lower = text.lower()

        for level, indicators in self.risk_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    found_risks[level].append(indicator)

        return found_risks


# Initialize extractor
entity_extractor = ContractEntityExtractor()

print("ContractEntityExtractor class defined")
