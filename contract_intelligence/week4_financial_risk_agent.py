# ============================================================================
# WEEK 4.4: FINANCIAL RISK AGENT
# ============================================================================
#
# Assumes `FinancialRiskAssessment` (week4_risk_models.py), `ChatOpenAI`,
# `ChatPromptTemplate`, `PydanticOutputParser`, and `get_langfuse_handler`
# (week4_langfuse_handler.py) are already in scope.

class FinancialRiskAgent:
    """
    Financial Risk Assessment Agent.

    Expert persona should focus on:
    - Pricing and contract value
    - Payment terms and cash flow
    - Financial penalties and exposure
    - Cost escalation risks
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model

        # Create parser for FinancialRiskAssessment
        self.parser = PydanticOutputParser(pydantic_object=FinancialRiskAssessment)

        # Create prompt with financial expert persona
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert financial analyst specializing in contract risk analysis.
            Analyze contracts for pricing risks, payment terms, cash flow impact,
            penalty clauses, and overall financial exposure. Provide clear, actionable
            recommendations to reduce financial risk.

            {format_instructions}"""),
            ("human", """Analyze the following contract for financial risks:

            {contract_text}

            Provide a comprehensive financial risk assessment.""")
        ])

    def analyze(self, contract_text: str, doc_id: str = "unknown") -> FinancialRiskAssessment:
        """Analyze contract for financial risks."""

        # Create traced handler
        handler = get_langfuse_handler(
            trace_name=f"financial-risk-analysis-{doc_id}",
            tags=["financial", "risk-assessment"],
        )

        # Create LLM with callback
        llm = ChatOpenAI(model=self.model, temperature=0, callbacks=[handler])

        # Build chain
        chain = self.prompt | llm | self.parser

        # Invoke chain
        result = chain.invoke({
            "contract_text": contract_text,
            "format_instructions": self.parser.get_format_instructions(),
        })

        return result


print("FinancialRiskAgent class defined")
