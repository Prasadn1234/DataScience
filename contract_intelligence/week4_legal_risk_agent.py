# ============================================================================
# WEEK 4.3: LEGAL RISK AGENT
# ============================================================================
#
# Assumes `LegalRiskAssessment` (week4_risk_models.py), `ChatOpenAI`,
# `ChatPromptTemplate`, `PydanticOutputParser`, and `get_langfuse_handler`
# (week4_langfuse_handler.py) are already in scope.

class LegalRiskAgent:
    """
    Legal Risk Assessment Agent with Langfuse tracing.

    Architecture:
    1. Prompt template with expert legal persona
    2. ChatOpenAI LLM
    3. PydanticOutputParser for structured output
    4. LangChain LCEL chain
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model

        # Create output parser
        self.parser = PydanticOutputParser(pydantic_object=LegalRiskAssessment)

        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert contract attorney specializing in legal risk analysis.
            Analyze contracts for liability exposure, IP risks, indemnification issues,
            and compliance gaps. Provide clear, actionable recommendations.

            {format_instructions}"""),
            ("human", """Analyze the following contract for legal risks:

            {contract_text}

            Provide a comprehensive legal risk assessment.""")
        ])

    def analyze(self, contract_text: str, doc_id: str = "unknown") -> LegalRiskAssessment:
        """
        Analyze contract for legal risks.

        Args:
            contract_text: Contract text to analyze
            doc_id: Document identifier for tracing

        Returns:
            LegalRiskAssessment structured output
        """

        # Create traced handler
        handler = get_langfuse_handler(
            trace_name=f"legal-risk-analysis-{doc_id}",
            tags=["legal", "risk-assessment"],
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


print("LegalRiskAgent class defined")
