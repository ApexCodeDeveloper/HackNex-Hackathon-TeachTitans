from __future__ import annotations
from typing import List, Dict, Optional, Any, Union
from enum import Enum
from pydantic import BaseModel, Field

class AuthorityType(str, Enum):
    STATUTE = "STATUTE"
    JUDGMENT = "JUDGMENT"
    CONCORDANCE_MAP = "CONCORDANCE_MAP"
    CASE_RECORD = "CASE_RECORD"

class VerificationStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    PARTIAL = "PARTIAL"
    UNSUPPORTED = "UNSUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    FABRICATED_CITATION = "FABRICATED_CITATION"

class ChunkProvenance(BaseModel):
    doc_id: str
    chunk_id: str
    parent_chunk_id: Optional[str] = None
    page_num: int = 1
    line_start: int = 1
    line_end: int = 1
    char_start: int = 0
    char_end: int = 0
    doc_type: str = "general"
    section_heading: Optional[str] = None
    legal_hierarchy: Optional[str] = None

class TextChunk(BaseModel):
    chunk_id: str
    text: str
    provenance: ChunkProvenance
    is_parent: bool = False
    child_chunk_ids: List[str] = Field(default_factory=list)

class LegalDocument(BaseModel):
    doc_id: str
    title: str
    doc_type: str  # fir, chargesheet, order, notice, contract, statute, judgment, concordance
    date: str
    jurisdiction: str = "India"
    source_url: str = ""
    license: str = "Public Domain"
    raw_text: str = ""
    chunks: List[TextChunk] = Field(default_factory=list)

class SourceRegistryEntry(BaseModel):
    registry_id: str  # e.g. "AUTH:BNS_103", "AUTH:SC_ARNESH_KUMAR_2014"
    authority_type: AuthorityType
    title: str
    citation_string: str  # e.g. "(2014) 8 SCC 273", "Section 479, BNSS 2023"
    neutral_citation: Optional[str] = None
    court_or_legislature: str  # "Supreme Court of India", "Parliament of India"
    year: int
    effective_date: Optional[str] = None
    key_sections: List[str] = Field(default_factory=list)
    source_chunk_ids: List[str] = Field(default_factory=list)
    canonical_text_snippet: str
    is_corpus_verified: bool = True

class FactItem(BaseModel):
    field_name: str
    value: str
    source_chunk_ids: List[str]
    supporting_quote: str  # MUST be verbatim span from one of source_chunk_ids
    confidence: float = 1.0
    is_inferred: bool = False

class FactSheet(BaseModel):
    case_id: str
    case_title: str
    document_type_requested: str  # "bail_application", "legal_notice", "affidavit", "petition"
    facts: Dict[str, FactItem] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ContradictionItem(BaseModel):
    contradiction_id: str
    field_name: str
    doc_a: str
    doc_b: str
    chunk_a: str
    chunk_b: str
    value_a: str
    value_b: str
    quote_a: str
    quote_b: str
    severity: str = "HIGH"  # CRITICAL, HIGH, MEDIUM
    explanation: str

class MissingInfoItem(BaseModel):
    field_name: str
    legal_significance: str
    document_type_required: str
    status: str = "MISSING"  # MISSING or PARTIAL
    resolution_advice: str

class ConfidenceMissingReport(BaseModel):
    overall_confidence: float
    facts_extracted_count: int
    contradictions_count: int
    missing_critical_fields_count: int
    contradictions: List[ContradictionItem] = Field(default_factory=list)
    missing_fields: List[MissingInfoItem] = Field(default_factory=list)
    is_ready_for_drafting: bool = True
    advisory_notes: List[str] = Field(default_factory=list)

class DraftClaim(BaseModel):
    claim_id: str
    sentence_text: str
    cited_chunk_ids: List[str] = Field(default_factory=list)
    cited_authority_ids: List[str] = Field(default_factory=list)
    contains_placeholder: bool = False
    placeholder_text: Optional[str] = None

class ClaimVerificationVerdict(BaseModel):
    claim_id: str
    sentence_text: str
    status: VerificationStatus
    registry_check_passed: bool
    quote_span_check_passed: bool
    entailment_score: float
    entailment_explanation: str
    cited_chunk_ids: List[str]
    cited_authority_ids: List[str]
    found_quote_spans: List[str] = Field(default_factory=list)
    repaired_sentence: Optional[str] = None

class VerificationLedger(BaseModel):
    claims: List[ClaimVerificationVerdict] = Field(default_factory=list)
    overall_groundedness_pct: float = 0.0
    fabrication_count: int = 0
    supported_count: int = 0
    partial_count: int = 0
    unsupported_count: int = 0
    contradicted_count: int = 0
    repaired_claims_count: int = 0
    repair_iterations_run: int = 0

class FabricationGateResult(BaseModel):
    passed: bool
    unregistered_authorities: List[str] = Field(default_factory=list)
    unretrieved_chunks: List[str] = Field(default_factory=list)
    hallucinated_sections: List[str] = Field(default_factory=list)
    violations: List[str] = Field(default_factory=list)

class FinalLegalDraftOutput(BaseModel):
    case_title: str
    document_type: str
    draft_text: str
    draft_with_html_anchors: str
    fact_sheet: FactSheet
    confidence_report: ConfidenceMissingReport
    verification_ledger: VerificationLedger
    fabrication_gate: FabricationGateResult
    abstained: bool = False
    abstention_reason: Optional[str] = None
    execution_time_seconds: float = 0.0
