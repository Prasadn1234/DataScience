"""Shared Pydantic models for ContractIQ analysis results."""

from pydantic import BaseModel, Field


class KeyDate(BaseModel):
    description: str = Field(description="What the date represents, e.g. 'Effective date'")
    date: str = Field(description="The date or deadline as written in the contract")


class Obligation(BaseModel):
    party: str = Field(description="The party responsible for the obligation")
    obligation: str = Field(description="A concise description of what they must do")


class RiskFlag(BaseModel):
    clause: str = Field(description="Short quote or reference to the clause in question")
    risk_level: str = Field(description="One of: low, medium, high")
    explanation: str = Field(description="Why this clause is risky or unusual")


class ContractAnalysis(BaseModel):
    contract_type: str = Field(description="The type of agreement, e.g. 'NDA', 'MSA', 'Lease'")
    parties: list[str] = Field(description="The parties entering into the contract")
    summary: str = Field(description="A plain-language summary of the contract, 3-5 sentences")
    key_dates: list[KeyDate] = Field(description="Important dates or deadlines in the contract")
    obligations: list[Obligation] = Field(description="Key obligations owed by each party")
    risks: list[RiskFlag] = Field(description="Clauses that are risky, unusual, or one-sided")
    recommended_actions: list[str] = Field(description="Suggested next steps before signing")
