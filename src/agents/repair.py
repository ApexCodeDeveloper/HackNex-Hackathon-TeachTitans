"""
NyayVeritas Self-Repair Loop Agent
Iteratively inspects claims that fail verification (PARTIAL, UNSUPPORTED, CONTRADICTED).
Executes conservative repairs:
1. Search retrieved corpus for supporting chunk
2. If unsupported, downgrade claim to explicit [●MISSING: ... — not found in sources] placeholder
3. Never invent new facts.
Runs for a maximum of 3 iterations.
"""

import re
from typing import List, Dict, Tuple, Set, Optional
from src.models import VerificationLedger, VerificationStatus, ClaimVerificationVerdict, TextChunk
from src.agents.verifier import ClaimVerifier

class RepairLoop:
    """Repairs ungrounded draft claims without hallucination."""
    def __init__(self, verifier: ClaimVerifier, chunks_map: Dict[str, TextChunk], max_iterations: int = 3):
        self.verifier = verifier
        self.chunks_map = chunks_map
        self.max_iterations = max_iterations

    def run_repair_loop(self, draft_text: str, retrieved_chunk_ids: Set[str]) -> Tuple[str, VerificationLedger]:
        current_draft = draft_text
        ledger = self.verifier.verify_draft(current_draft, retrieved_chunk_ids)
        iteration = 0
        repaired_count = 0

        while iteration < self.max_iterations and (ledger.unsupported_count > 0 or ledger.partial_count > 0 or ledger.fabrication_count > 0):
            iteration += 1
            modified = False
            lines = current_draft.split("\n")
            new_lines = []

            for line in lines:
                new_line = line
                for claim_verdict in ledger.claims:
                    if claim_verdict.sentence_text in new_line and claim_verdict.status != VerificationStatus.SUPPORTED:
                        # Attempt Repair
                        repaired_sent = self._repair_sentence(claim_verdict, retrieved_chunk_ids)
                        if repaired_sent != claim_verdict.sentence_text:
                            new_line = new_line.replace(claim_verdict.sentence_text, repaired_sent)
                            modified = True
                            repaired_count += 1
                new_lines.append(new_line)

            if not modified:
                break

            current_draft = "\n".join(new_lines)
            ledger = self.verifier.verify_draft(current_draft, retrieved_chunk_ids)

        ledger.repair_iterations_run = iteration
        ledger.repaired_claims_count = repaired_count
        return current_draft, ledger

    def _repair_sentence(self, verdict: ClaimVerificationVerdict, retrieved_chunk_ids: Set[str]) -> str:
        orig = verdict.sentence_text
        clean = re.sub(r"\[[SA]:[^\]]+\]", "", orig).strip()

        # If fabricated authority, try to strip or downgrade
        if verdict.status == VerificationStatus.FABRICATED_CITATION:
            # Replace unregistered citation with placeholder
            repaired = re.sub(r"\[A:[^\]]+\]", "[●MISSING: authority not in corpus registry]", orig)
            repaired = re.sub(r"\[S:[^\]]+\]", "[●MISSING: source chunk not in verified set]", repaired)
            return repaired

        # If unsupported empirical claim, search if another retrieved chunk supports it
        if verdict.status in [VerificationStatus.UNSUPPORTED, VerificationStatus.PARTIAL]:
            # Scan all retrieved chunks for high overlap
            claim_words = set(re.findall(r"\w+", clean.lower()))
            best_chunk_id = None
            best_overlap = 0.0

            for cid in retrieved_chunk_ids:
                if cid in self.chunks_map:
                    c_text = self.chunks_map[cid].text.lower()
                    overlap = len([w for w in claim_words if len(w) > 3 and w in c_text])
                    if overlap > best_overlap and overlap >= 3:
                        best_overlap = overlap
                        best_chunk_id = cid

            if best_chunk_id:
                # Attach the verified chunk
                return f"{clean} [S:{best_chunk_id}]"
            else:
                # Downgrade to explicit placeholder
                return f"[●MISSING: {clean[:60]}... — not found in sources]"

        return orig
