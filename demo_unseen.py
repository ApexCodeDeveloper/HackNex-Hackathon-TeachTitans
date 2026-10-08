"""
NyayVeritas - Demo Script for UNSEEN Documents
Allows hackathon judges to drop any unseen document (case file, contract, notice, or order)
into the drop folder or pass it via CLI, instantly ingesting it, validating it against the
closed-world canonical registry, and generating a verified draft with zero hallucinations.
"""

import sys
import argparse
from pathlib import Path
import json

# Ensure UTF-8 stdout for Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(r"C:\Users\prakashh\.gemini\antigravity-ide\scratch\nyay-veritas")
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.ingest import LegalIngestor
from src.registry import SourceRegistry
from src.pipeline import NyayVeritasPipeline

def main():
    parser = argparse.ArgumentParser(description="NyayVeritas: Run Verifier on UNSEEN judge documents")
    parser.add_argument("--file", type=str, help="Path to unseen document (.txt, .json, .pdf)", default=None)
    parser.add_argument("--task", type=str, help="Drafting or review task", default="Draft regular bail application citing health condition and arrest details")
    args = parser.parse_args()

    data_dir = BASE_DIR / "data"
    drop_dir = BASE_DIR / "data" / "unseen_drop"
    drop_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("VERTIFYCASE: AGENTIC LEGAL ASSISTANT WITH HARD VERIFIABILITY")
    print("=" * 70)
    print("Initializing canonical corpus & registry...")

    ingestor = LegalIngestor(str(data_dir))
    documents, all_chunks = ingestor.ingest_all()
    registry = SourceRegistry()
    registry.build_from_documents(documents)

    # Ingest unseen file
    unseen_path = Path(args.file) if args.file else None
    if not unseen_path:
        # Check drop folder for any files
        dropped_files = list(drop_dir.glob("*.txt")) + list(drop_dir.glob("*.json"))
        if dropped_files:
            unseen_path = dropped_files[0]
        else:
            # Create a sample unseen document for demonstration
            sample_unseen = drop_dir / "unseen_fir_2024_delhi.txt"
            sample_unseen.write_text(
                """FIRST INFORMATION REPORT (UNSEEN JUDGE TEST DOCUMENT)
Police Station: Tughlak Road, New Delhi | FIR No: 331/2024 | Date: 18-09-2024
Sections: Section 318(4) BNS 2023.
Accused: Mohit Aggarwal, s/o R.K. Aggarwal, r/o 12 Jor Bagh, New Delhi.
Arrest Memo: Arrested on 20-09-2024 at 14:00 hours at Jor Bagh residence.
MLC Report: AIIMS Trauma Centre MLC 9912/24 shows cardiac arrhythmia and severe asthma.
Seizure Memo: Seized Apple MacBook Pro Serial C02X8812 and Rs. 3,20,000 cash.
Custody: Accused remanded to Judicial Custody on 21-09-2024. Clean antecedents.""",
                encoding="utf-8"
            )
            unseen_path = sample_unseen
            print(f"Created sample unseen test file at: {unseen_path}")

    print(f"\n[INGESTION] Ingesting Unseen Document: {unseen_path.name}")
    unseen_doc = ingestor.ingest_unseen_file(unseen_path)
    print(f"-> Parsed {len(unseen_doc.chunks)} legal chunks with char/line offsets.")

    # Run Pipeline
    pipeline = NyayVeritasPipeline(documents, all_chunks, registry)
    print(f"\n[ORCHESTRATION] Executing Task: '{args.task}'")
    output = pipeline.execute_drafting(args.task, document_type="bail_application")

    print("\n" + "=" * 70)
    print("1. CONFIDENCE & MISSING-INFO REPORT (Pre-Drafting)")
    print("=" * 70)
    print(f"Overall Confidence Score: {output.confidence_report.overall_confidence * 100:.1f}%")
    print(f"Facts Extracted: {output.confidence_report.facts_extracted_count}")
    print(f"Contradictions Flagged: {output.confidence_report.contradictions_count}")
    print(f"Missing Mandatory Fields: {output.confidence_report.missing_critical_fields_count}")
    for note in output.confidence_report.advisory_notes:
        print(f"  * {note}")

    print("\n" + "=" * 70)
    print("2. VERIFIED LEGAL DRAFT (With Explicit Grounding Markers)")
    print("=" * 70)
    print(output.draft_text)

    print("\n" + "=" * 70)
    print("3. MACHINE-READABLE EVIDENCE LEDGER (Atomic Claim Verification)")
    print("=" * 70)
    for c in output.verification_ledger.claims:
        auth_str = f" [Auth: {c.cited_authority_ids}]" if c.cited_authority_ids else ""
        chunk_str = f" [Chunks: {c.cited_chunk_ids}]" if c.cited_chunk_ids else ""
        print(f"[{c.claim_id}] Verdict: {c.status.value.upper()} | Score: {c.entailment_score:.2f}")
        print(f"  Claim: {c.sentence_text[:90]}...")
        print(f"  Grounding: {chunk_str}{auth_str}")
        print(f"  Explanation: {c.entailment_explanation}\n")

    print("=" * 70)
    print("4. DETERMINISTIC FABRICATION GATE STATUS")
    print("=" * 70)
    print(f"Gate Status: {'PASSED (Zero Fabrications)' if output.fabrication_gate.passed else 'FAILED'}")
    if output.fabrication_gate.violations:
        for v in output.fabrication_gate.violations:
            print(f"  - Violation: {v}")
    print(f"Total Execution Time: {output.execution_time_seconds:.2f}s")
    print("=" * 70)

if __name__ == "__main__":
    main()
