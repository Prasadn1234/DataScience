# ============================================================================
# WEEK 4.5: OPERATIONAL RISK AGENT
# ============================================================================
#
# Assumes `OperationalRiskAssessment` (week4_risk_models.py), `ChatOpenAI`,
# `ChatPromptTemplate`, `PydanticOutputParser`, and `get_langfuse_handler`
# (week4_langfuse_handler.py) are already in scope.

class OperationalRiskAgent:
    """
    Operational Risk Assessment Agent.

    Expert persona should focus on:
    - Service scope and deliverables
    - SLA requirements
    - Delivery risks and timelines
    - Resource and dependency management
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model

        # Create parser for OperationalRiskAssessment
        self.parser = PydanticOutputParser(pydantic_object=OperationalRiskAssessment)

        # Create prompt with operations expert persona
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert operations manager specializing in contract risk analysis.
            Analyze contracts for service scope, SLA requirements, delivery risks,
            resource requirements, and dependency risks. Provide clear, actionable
            mitigation strategies.

            {format_instructions}"""),
            ("human", """Analyze the following contract for operational risks:

            {contract_text}

            Provide a comprehensive operational risk assessment.""")
        ])

    def analyze(self, contract_text: str, doc_id: str = "unknown") -> OperationalRiskAssessment:
        """Analyze contract for operational risks."""

        # Create traced handler
        handler = get_langfuse_handler(
            trace_name=f"operational-risk-analysis-{doc_id}",
            tags=["operational", "risk-assessment"],
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


print("OperationalRiskAgent class defined")
