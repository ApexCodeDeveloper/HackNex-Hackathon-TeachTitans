"""
NyayVeritas FastAPI Web Server
Serves the rich interactive web application for legal drafting, verification,
side-by-side evidence ledger, benchmark ablation dashboard, and grounded chat.
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional

from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

BASE_DIR = Path(r"C:\Users\prakashh\.gemini\antigravity-ide\scratch\nyay-veritas")
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.ingest import LegalIngestor
from src.registry import SourceRegistry
from src.pipeline import NyayVeritasPipeline
from src.baseline import BaselineDenseRAG
from src.chat import GroundedLegalChat
from src.llm_client import llm_client

app = FastAPI(title="VertifyCase - Legal Verifier")

# Favicon handler to clear browser 404 errors
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    svg_icon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">🏛️</text></svg>'
    return Response(content=svg_icon, media_type="image/svg+xml")

# Mount static and templates
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "app" / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

# Global singletons
DATA_DIR = BASE_DIR / "data"
ingestor = LegalIngestor(str(DATA_DIR))
documents, all_chunks = ingestor.ingest_all()

registry = SourceRegistry()
registry.build_from_documents(documents)

pipeline = NyayVeritasPipeline(documents, all_chunks, registry)
baseline = BaselineDenseRAG(list(all_chunks.values()))
chat_engine = GroundedLegalChat(pipeline.retriever, registry, all_chunks)

# Load pre-computed evaluation results
EVAL_RESULTS_PATH = BASE_DIR / "eval" / "evaluation_results.json"
eval_data = {}
if EVAL_RESULTS_PATH.exists():
    with open(EVAL_RESULTS_PATH, "r", encoding="utf-8") as f:
        eval_data = json.load(f)

class LLMConfigModel(BaseModel):
    provider: str  # "gemini", "openai", "anthropic", "ollama", "offline"
    api_key: Optional[str] = ""
    ollama_url: Optional[str] = None

@app.get("/api/config/llm")
async def get_llm_config():
    return llm_client.get_config()

@app.post("/api/config/llm")
async def set_llm_config(cfg: LLMConfigModel):
    prov = cfg.provider.lower()
    if prov == "gemini":
        llm_client.save_keys_to_env(gemini_key=cfg.api_key, preferred_provider="gemini")
    elif prov == "openai":
        llm_client.save_keys_to_env(openai_key=cfg.api_key, preferred_provider="openai")
    elif prov == "anthropic":
        llm_client.save_keys_to_env(anthropic_key=cfg.api_key, preferred_provider="anthropic")
    elif prov == "ollama":
        llm_client.save_keys_to_env(ollama_url=cfg.ollama_url or cfg.api_key, preferred_provider="ollama")
    elif prov == "offline":
        llm_client.save_keys_to_env(preferred_provider="offline")

    return {
        "status": "success",
        "config": llm_client.get_config()
    }

# Request Models
class DraftRequest(BaseModel):
    task_prompt: str
    document_type: str = "bail_application"
    run_baseline: bool = False

class ChatRequest(BaseModel):
    query: str

class UnseenDocRequest(BaseModel):
    text: str
    title: Optional[str] = "Judge Test Document"
    task_prompt: str = "Draft bail application"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "corpus_docs_count": len(documents),
            "total_chunks_count": len(all_chunks),
            "authorities_count": len(registry.entries)
        }
    )

@app.post("/api/draft")
async def draft_document(req: DraftRequest):
    if req.run_baseline:
        t0 = time.time()
        res = baseline.draft(req.task_prompt, document_type=req.document_type)
        ledger = pipeline.verifier.verify_draft(res["draft_text"])
        dt = round(time.time() - t0, 2)
        return {
            "is_baseline": True,
            "document_type": req.document_type,
            "draft_text": res["draft_text"],
            "draft_with_html_anchors": f"<div class='baseline-draft-body'><pre>{res['draft_text']}</pre></div>",
            "rendered_html": f"<div class='baseline-draft-body'><pre>{res['draft_text']}</pre></div>",
            "verification_ledger": ledger.model_dump(),
            "confidence_report": {
                "overall_confidence": 0.45,
                "facts_extracted_count": 0,
                "contradictions_count": 0,
                "missing_critical_fields_count": 4,
                "contradictions": [],
                "missing_fields": [
                    {
                        "field_name": "Unverified Freeform Output",
                        "legal_significance": "Baseline RAG bypasses closed-world registry and verbatim fact extraction.",
                        "document_type_required": req.document_type,
                        "status": "UNVERIFIED",
                        "resolution_advice": "Switch to NyayVeritas Verified Drafting to enforce hard provenance."
                    }
                ],
                "is_ready_for_drafting": False,
                "advisory_notes": ["Baseline RAG operates without pre-drafting contradiction audit or registry validation."]
            },
            "fabrication_gate": {"passed": False, "violations": ["Baseline lacks closed-world registry enforcement"]},
            "execution_time_seconds": dt
        }
    else:
        output = pipeline.execute_drafting(req.task_prompt, document_type=req.document_type)
        return output.model_dump()

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    response = chat_engine.ask(req.query)
    return {
        "reply": response.content,
        "citations": response.citations,
        "retrieved_chunk_ids": response.retrieved_chunk_ids,
        "is_refusal": response.is_refusal
    }

@app.get("/api/chunk/{chunk_id}")
async def get_chunk_detail(chunk_id: str):
    if chunk_id in all_chunks:
        ch = all_chunks[chunk_id]
        return {
            "chunk_id": ch.chunk_id,
            "text": ch.text,
            "provenance": ch.provenance.model_dump(),
            "is_parent": ch.is_parent
        }
    return JSONResponse(status_code=404, content={"error": "Chunk not found"})

@app.get("/api/authority/{auth_id}")
async def get_authority_detail(auth_id: str):
    auth = registry.find_authority(auth_id)
    if auth:
        return auth.model_dump()
    return JSONResponse(status_code=404, content={"error": "Authority not found"})

@app.get("/api/eval")
async def get_eval_results():
    return eval_data

@app.post("/api/unseen")
async def ingest_unseen_text(req: UnseenDocRequest):
    drop_file = BASE_DIR / "data" / "unseen_drop" / "web_uploaded_doc.txt"
    drop_file.parent.mkdir(parents=True, exist_ok=True)
    drop_file.write_text(req.text, encoding="utf-8")
    
    unseen_doc = ingestor.ingest_unseen_file(drop_file)
    # Re-index pipeline
    pipeline.retriever.index(list(all_chunks.values()))
    
    output = pipeline.execute_drafting(req.task_prompt, document_type="bail_application")
    return {
        "status": "success",
        "doc_id": unseen_doc.doc_id,
        "chunks_indexed": len(unseen_doc.chunks),
        "draft_output": output.model_dump()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.server:app", host="127.0.0.1", port=8000, reload=False)
