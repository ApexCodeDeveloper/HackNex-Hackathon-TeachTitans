"""
NyayVeritas Integration Test Suite
Validates all core endpoints and agent functionality.
"""

import sys
from pathlib import Path
from fastapi.testclient import TestClient

BASE_DIR = Path(r"C:\Users\prakashh\.gemini\antigravity-ide\scratch\nyay-veritas")
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.server import app

def run_tests():
    client = TestClient(app)

    print("Test 1: GET / (Homepage)...")
    res = client.get("/")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert "VERTIFYCASE" in res.text
    print("  -> Passed!")

    print("\nTest 2: POST /api/draft (NyayVeritas Verified Draft)...")
    payload = {
        "task_prompt": "Draft regular bail application for Rajesh Sharma in FIR 142/2024 citing medical ailments and seizure status",
        "document_type": "bail_application",
        "run_baseline": False
    }
    res = client.post("/api/draft", json=payload)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    data = res.json()
    assert "draft_text" in data
    assert "verification_ledger" in data
    assert data["fabrication_gate"]["passed"] == True
    print(f"  -> Passed! Groundedness: {data['verification_ledger']['overall_groundedness_pct']}%, Fabrications: {data['fabrication_gate']['violations']}")

    print("\nTest 3: POST /api/draft (Baseline RAG Comparison)...")
    payload_base = {
        "task_prompt": "Draft regular bail application for Rajesh Sharma",
        "document_type": "bail_application",
        "run_baseline": True
    }
    res_base = client.post("/api/draft", json=payload_base)
    assert res_base.status_code == 200
    data_base = res_base.json()
    assert data_base["is_baseline"] == True
    print(f"  -> Passed! Baseline Groundedness: {data_base['verification_ledger']['overall_groundedness_pct']}%")

    print("\nTest 4: POST /api/chat (Grounded Legal Chat)...")
    chat_payload = {"query": "What is the maximum detention period under Section 479 BNSS for first-time offenders?"}
    res_chat = client.post("/api/chat", json=chat_payload)
    assert res_chat.status_code == 200
    chat_data = res_chat.json()
    assert not chat_data["is_refusal"]
    assert len(chat_data["retrieved_chunk_ids"]) > 0
    print(f"  -> Passed! Reply: {chat_data['reply'][:100]}...")

    print("\nTest 5: POST /api/chat (Refusal on ungrounded adversarial query)...")
    chat_adversarial = {"query": "Tell me about the secret alien penalty in Section 9999 of Mars Code 2099."}
    res_refusal = client.post("/api/chat", json=chat_adversarial)
    assert res_refusal.status_code == 200
    refusal_data = res_refusal.json()
    assert refusal_data["is_refusal"] == True
    print(f"  -> Passed! Correctly Refused: {refusal_data['reply'][:80]}...")

    print("\nTest 6: GET /api/chunk/CASE_142_FIR:P1:C1...")
    res_chunk = client.get("/api/chunk/CASE_142_FIR:P1:C1")
    assert res_chunk.status_code == 200
    chunk_data = res_chunk.json()
    assert chunk_data["chunk_id"] == "CASE_142_FIR:P1:C1"
    print(f"  -> Passed! Provenance: {chunk_data['provenance']['legal_hierarchy']}")

    print("\nTest 7: GET /api/eval (Ablation Benchmark Data)...")
    res_eval = client.get("/api/eval")
    assert res_eval.status_code == 200
    eval_d = res_eval.json()
    assert "ablation_table" in eval_d
    print(f"  -> Passed! {len(eval_d['ablation_table'])} ablation steps loaded.")

    print("\n==============================================")
    print("ALL 7 SYSTEM INTEGRATION TESTS PASSED 100%!")
    print("==============================================")

if __name__ == "__main__":
    run_tests()
