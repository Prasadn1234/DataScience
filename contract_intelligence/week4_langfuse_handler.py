# ============================================================================
# WEEK 4.2: LANGFUSE CALLBACK HANDLER (PROVIDED)
# ============================================================================
#
# Assumes `os`, `SESSION_ID`, and `LangfuseCallbackHandler` (imported in
# week4_risk_models.py as `from langfuse.callback import CallbackHandler as
# LangfuseCallbackHandler`) are already in scope.

def get_langfuse_handler(trace_name: str, tags: List[str] = None) -> LangfuseCallbackHandler:
    """
    Create a Langfuse callback handler for LangChain.

    This traces:
    - Prompt formatting
    - LLM calls (input/output/tokens)
    - Output parsing
    - Errors
    """
    return LangfuseCallbackHandler(
        secret_key=os.environ.get('LANGFUSE_SECRET_KEY'),
        public_key=os.environ.get('LANGFUSE_PUBLIC_KEY'),
        host=os.environ.get('LANGFUSE_HOST'),
        session_id=SESSION_ID,
        trace_name=trace_name,
        tags=tags or []
    )


print("get_langfuse_handler() factory defined")
