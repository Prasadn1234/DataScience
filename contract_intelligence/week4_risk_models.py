# ============================================================================
# WEEK 4.1: PYDANTIC MODELS
# ============================================================================

from typing import List

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langfuse.callback import CallbackHandler as LangfuseCallbackHandler


class LegalRiskAssessment(BaseModel):
    """
    Structured output for legal risk analysis.
    """

    # PROVIDED - contract type
    contract_type: str = Field(description="Type of contract (MSA, NDA, SOW, etc.)")

    # Overall risk level
    risk_level: str = Field(description="Overall risk level: LOW, MEDIUM, HIGH, CRITICAL")

    # Liability exposure
    liability_exposure: str = Field(description="Summary of the contract's liability exposure")

    # IP risks
    ip_risks: List[str] = Field(default_factory=list, description="Identified intellectual property risks")

    # Indemnification issues
    indemnification_issues: List[str] = Field(default_factory=list, description="Identified indemnification issues")

    # Compliance gaps
    compliance_gaps: List[str] = Field(default_factory=list, description="Identified regulatory or policy compliance gaps")

    # Recommended changes
    recommended_changes: List[str] = Field(default_factory=list, description="Recommended contract changes to mitigate risk")

    # Confidence score
    confidence: float = Field(ge=0.0, le=1.0, description="Model's confidence in this assessment, 0.0 to 1.0")


print("LegalRiskAssessment model defined")
print(f"Fields: {list(LegalRiskAssessment.model_fields.keys())}")


# ============================================================================
# FINANCIAL RISK ASSESSMENT MODEL
# ============================================================================

class FinancialRiskAssessment(BaseModel):
    """
    Structured output for financial risk analysis.
    """

    total_contract_value: str = Field(description="Total estimated contract value")
    payment_terms: str = Field(description="Summary of payment terms")

    # Pricing risks
    pricing_risks: List[str] = Field(default_factory=list, description="Identified pricing risks")

    # Penalty clauses
    penalty_clauses: List[str] = Field(default_factory=list, description="Identified penalty clauses")

    # Cash flow impact
    cash_flow_impact: str = Field(description="Summary of the contract's cash flow impact")

    # Financial exposure
    financial_exposure: str = Field(description="Summary of the contract's financial exposure")

    # Overall risk level
    risk_level: str = Field(description="Overall risk level: LOW, MEDIUM, HIGH, CRITICAL")

    # Confidence score
    confidence: float = Field(ge=0.0, le=1.0, description="Model's confidence in this assessment, 0.0 to 1.0")


print("FinancialRiskAssessment model defined")
print(f"Fields: {list(FinancialRiskAssessment.model_fields.keys())}")
