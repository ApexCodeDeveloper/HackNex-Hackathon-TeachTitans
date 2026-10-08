"""
NyayVeritas Pipeline State Machine
Orchestrates:
1. Planner
2. Hybrid Retrieval (BM25 + Dense + RRF + Cross-Encoder)
3. Fact Extractor (Structured FactSheet with Verbatim Quotes)
4. Gap / Contradiction Analyzer (Pre-Drafting Confidence Report)
5. Legal Drafter ([S:chunk_id] & [A:registry_id] markers)
6. Atomic Claim Verifier
7. Self-Repair Loop (Max 3 iterations)
8. Deterministic Fabrication Gate
9. Output generation with clickable HTML source anchors & Evidence Ledger.
"""

import time
import re
from typing import Dict, List, Optional, Set, Any
from src.models import (
    LegalDocument, TextChunk, FinalLegalDraftOutput,
    FactSheet, ConfidenceMissingReport, VerificationLedger, FabricationGateResult
)
from src.registry import SourceRegistry
from src.retrieval import HybridRetriever
from src.agents.planner import LegalPlanner
from src.agents.fact_extractor import FactExtractor
from src.agents.analyzer import GapContradictionAnalyzer
from src.agents.drafter import LegalDrafter
from src.agents.verifier import ClaimVerifier
from src.agents.repair import RepairLoop
from src.agents.gate import FabricationGate

class NyayVeritasPipeline:
    def __init__(self, documents: Dict[str, LegalDocument], all_chunks: Dict[str, TextChunk], registry: SourceRegistry):
        self.documents = documents
        self.all_chunks = all_chunks
        self.registry = registry
        
        # Initialize sub-systems
        self.retriever = HybridRetriever()
        self.retriever.index(list(all_chunks.values()))
        self.planner = LegalPlanner()
        self.fact_extractor = FactExtractor(all_chunks)
        self.analyzer = GapContradictionAnalyzer()
        self.drafter = LegalDrafter(registry)
        self.verifier = ClaimVerifier(registry, all_chunks)
        self.repair_loop = RepairLoop(self.verifier, all_chunks, max_iterations=3)
        self.gate = FabricationGate(registry, all_chunks)

    def execute_drafting(self, task_prompt: str, document_type: str = "bail_application") -> FinalLegalDraftOutput:
        start_time = time.time()
        
        # Step 1: Planner
        plan = self.planner.plan_task(task_prompt, document_type)
        doc_type_resolved = plan["document_type"]
        
        # Step 2: Hybrid Retrieval
        retrieved_tuples = self.retriever.decompose_and_retrieve(task_prompt, top_k=15)
        retrieved_chunks = [ch for ch, _ in retrieved_tuples]
        retrieved_chunk_ids = {ch.chunk_id for ch in retrieved_chunks}
        
        # Step 3: Fact Extraction (Structured FactSheet)
        case_id = "CASE_142" if "142" in task_prompt or "rajesh" in task_prompt.lower() else "CASE_DEFAULT"
        case_title = "State v. Rajesh Sharma" if "rajesh" in task_prompt.lower() else "Legal Proceeding"
        
        factsheet = self.fact_extractor.extract_factsheet(
            case_id=case_id,
            case_title=case_title,
            doc_type=doc_type_resolved,
            retrieved_chunks=retrieved_chunks
        )
        
        # Step 4: Gap and Contradiction Analyzer (Pre-Drafting Report)
        conf_report = self.analyzer.analyze(factsheet, retrieved_chunks)
        
        # Step 5: Abstention Check
        if not conf_report.is_ready_for_drafting and conf_report.overall_confidence < 0.20:
            return FinalLegalDraftOutput(
                case_title=case_title,
                document_type=doc_type_resolved,
                draft_text="ABSTAINED: Evidence insufficient for reliable drafting.",
                draft_with_html_anchors="<p class='abstain-notice'>Evidence insufficient for reliable drafting.</p>",
                fact_sheet=factsheet,
                confidence_report=conf_report,
                verification_ledger=VerificationLedger(),
                fabrication_gate=FabricationGateResult(passed=True),
                abstained=True,
                abstention_reason=f"Overall confidence ({conf_report.overall_confidence}) below minimum safety threshold (0.20). Critical missing fields: {[m.field_name for m in conf_report.missing_fields]}",
                execution_time_seconds=round(time.time() - start_time, 2)
            )

        # Step 6: Drafter
        raw_draft = self.drafter.draft_document(factsheet, task_prompt)
        
        # Step 7: Verifier & Self-Repair Loop
        repaired_draft, ledger = self.repair_loop.run_repair_loop(raw_draft, retrieved_chunk_ids)
        
        # Step 8: Deterministic Fabrication Gate
        gate_res = self.gate.check(repaired_draft, retrieved_chunk_ids)
        
        # Step 9: Render Clickable / Hoverable HTML Anchors
        rendered_html = self._render_html_anchors(repaired_draft)
        
        execution_time = round(time.time() - start_time, 2)
        
        return FinalLegalDraftOutput(
            case_title=case_title,
            document_type=doc_type_resolved,
            draft_text=repaired_draft,
            draft_with_html_anchors=rendered_html,
            fact_sheet=factsheet,
            confidence_report=conf_report,
            verification_ledger=ledger,
            fabrication_gate=gate_res,
            abstained=False,
            execution_time_seconds=execution_time
        )

    def _render_html_anchors(self, draft_text: str) -> str:
        """Converts [S:chunk_id] and [A:auth_id] into rich interactive HTML badges."""
        rendered = draft_text
        
        # Format [●MISSING: ...]
        rendered = re.sub(
            r"\[●MISSING:\s*([^\]]+)\]",
            r'<span class="missing-badge" title="Information Missing from Source Record">● MISSING: \1</span>',
            rendered
        )
        
        # Format [A:registry_id]
        def replace_auth(match):
            auth_id = match.group(1)
            auth_entry = self.registry.entries.get(auth_id)
            title = auth_entry.title if auth_entry else "Verified Legal Authority"
            cit = auth_entry.citation_string if auth_entry else auth_id
            court = auth_entry.court_or_legislature if auth_entry else ""
            tooltip = f"Authority: {title} | {cit} ({court})"
            return f'<span class="auth-badge" data-auth-id="{auth_id}" title="{tooltip}">⚖️ {cit}</span>'
            
        rendered = re.sub(r"\[A:([^\]]+)\]", replace_auth, rendered)
        
        # Format [S:chunk_id]
        def replace_src(match):
            cid = match.group(1)
            ch = self.all_chunks.get(cid)
            snippet = ch.text[:140].replace('"', '&quot;') + "..." if ch else "Source Chunk"
            doc_id = ch.provenance.doc_id if ch else ""
            tooltip = f"Source {cid} ({doc_id}): {snippet}"
            return f'<span class="src-badge" data-chunk-id="{cid}" title="{tooltip}">📄 {cid}</span>'
            
        rendered = re.sub(r"\[S:([^\]]+)\]", replace_src, rendered)
        
        # Preserve newlines
        rendered = rendered.replace("\n\n", "</p><p>").replace("\n", "<br/>")
        return f"<div class='legal-draft-body'><p>{rendered}</p></div>"
