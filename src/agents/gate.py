"""
NyayVeritas Deterministic Fabrication Gate
The hard deterministic gatekeeper:
Regex-extracts every citation, statute section, case name, and chunk ID in the draft.
Rejects the draft if any authority is not in the canonical registry or retrieved set.
This MUST run on every output.
"""

import re
from typing import Set, List, Dict, Tuple
from src.models import FabricationGateResult, TextChunk
from src.registry import SourceRegistry

class FabricationGate:
    """Deterministic post-check fabrication gate."""
    def __init__(self, registry: SourceRegistry, chunks_map: Dict[str, TextChunk]):
        self.registry = registry
        self.chunks_map = chunks_map

    def check(self, draft_text: str, retrieved_chunk_ids: Set[str]) -> FabricationGateResult:
        unregistered_auths: List[str] = []
        unretrieved_chunks: List[str] = []
        hallucinated_sections: List[str] = []
        violations: List[str] = []

        # 1. Check Authority Markers [A:registry_id]
        cited_auth_ids = re.findall(r"\[A:([^\]]+)\]", draft_text)
        for a_id in cited_auth_ids:
            if not self.registry.validate_citation(a_id):
                unregistered_auths.append(a_id)
                violations.append(f"Unregistered Authority: '[A:{a_id}]' not found in canonical Source Registry.")

        # 2. Check Chunk Markers [S:chunk_id]
        cited_chunk_ids = re.findall(r"\[S:([^\]]+)\]", draft_text)
        for c_id in cited_chunk_ids:
            if c_id not in self.chunks_map:
                unretrieved_chunks.append(c_id)
                violations.append(f"Fictitious Chunk ID: '[S:{c_id}]' does not exist in ingested corpus.")
            elif c_id not in retrieved_chunk_ids:
                unretrieved_chunks.append(c_id)
                violations.append(f"Unretrieved Chunk: '[S:{c_id}]' was not in the retrieved context for this task.")

        # 3. Regex-extract all statutory section mentions in raw text
        # e.g., "Section 420", "Section 302", "Section 500"
        raw_sections = re.findall(r"\bSection\s+([0-9]{1,4}(?:\([0-9a-zA-Z]+\))?)", draft_text, re.IGNORECASE)
        for sec in raw_sections:
            # Check if this section is known in registry or concordance table
            known = False
            for reg_id, entry in self.registry.entries.items():
                if any(sec in s for s in entry.key_sections):
                    known = True
                    break
            # Also check concordance
            if not known:
                for k, v in self.registry.concordance_map.items():
                    if sec in k or sec in v[0]:
                        known = True
                        break
            if not known:
                hallucinated_sections.append(sec)
                violations.append(f"Hallucinated / Unverifiable Statute Section: 'Section {sec}' not grounded in corpus.")

        # 4. Regex-extract raw case citations (e.g., "(2014) 8 SCC 273", "v. State")
        case_v_matches = re.findall(r"([A-Z][A-Za-z\s\.]+v\.\s+[A-Z][A-Za-z\s\.]+)", draft_text)
        for case_name in case_v_matches:
            c_clean = case_name.strip()
            # If length is reasonable for a case name
            if 6 < len(c_clean) < 60:
                auth = self.registry.find_authority(c_clean)
                if not auth:
                    unregistered_auths.append(c_clean)
                    violations.append(f"Fabricated / Unverified Case Citation: '{c_clean}' not in canonical registry.")

        passed = len(violations) == 0
        return FabricationGateResult(
            passed=passed,
            unregistered_authorities=unregistered_auths,
            unretrieved_chunks=unretrieved_chunks,
            hallucinated_sections=hallucinated_sections,
            violations=violations
        )
