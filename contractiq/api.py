"""ContractIQ FastAPI backend: health check, contract analysis, and search."""

import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from analyzer import analyze_contract
from models import ContractAnalysis
from store import ContractStore

app = FastAPI(title="ContractIQ API")
store = ContractStore()


class AnalyzeRequest(BaseModel):
    contract_text: str
    contract_id: str


class AnalyzeResponse(BaseModel):
    contract_id: str
    analysis: ContractAnalysis


class SearchRequest(BaseModel):
    query: str
    n_results: int = 5


class SearchResultItem(BaseModel):
    contract_id: str
    similarity: float
    contract_type: str
    summary: str


class SearchResponse(BaseModel):
    results: list[SearchResultItem]


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest) -> AnalyzeResponse:
    if not req.contract_text.strip():
        raise HTTPException(status_code=400, detail="contract_text must not be empty")
    if not req.contract_id.strip():
        raise HTTPException(status_code=400, detail="contract_id must not be empty")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY is not configured")

    try:
        analysis = analyze_contract(req.contract_text, api_key)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Analysis failed: {exc}") from exc

    store.add(req.contract_id, req.contract_text, analysis)
    return AnalyzeResponse(contract_id=req.contract_id, analysis=analysis)


@app.post("/api/search", response_model=SearchResponse)
def search(req: SearchRequest) -> SearchResponse:
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="query must not be empty")

    results = store.search(req.query, req.n_results)
    return SearchResponse(
        results=[
            SearchResultItem(
                contract_id=contract.contract_id,
                similarity=float(similarity),
                contract_type=contract.analysis.contract_type,
                summary=contract.analysis.summary,
            )
            for contract, similarity in results
        ]
    )
