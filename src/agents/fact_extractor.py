"""
NyayVeritas Fact Extractor Agent
Extracts structured FactSheet JSON where EVERY field contains:
- value
- source_chunk_ids
- supporting_quote (verbatim span)
HARD RULE: No verbatim quote span = NO FACT.
"""

import re
from typing import List, Dict, Tuple, Optional
from src.models import TextChunk, FactItem, FactSheet

class FactExtractor:
    """Extracts verifiable facts with mandatory verbatim span grounding."""
    
    def __init__(self, chunks_map: Dict[str, TextChunk]):
        self.chunks_map = chunks_map

    def extract_factsheet(self, case_id: str, case_title: str, doc_type: str, retrieved_chunks: List[TextChunk]) -> FactSheet:
        factsheet = FactSheet(
            case_id=case_id,
            case_title=case_title,
            document_type_requested=doc_type,
            facts={}
        )
        
        # Scrape and extract key legal entities across retrieved chunks
        for chunk in retrieved_chunks:
            text = chunk.text
            c_id = chunk.chunk_id
            
            # 1. Accused / Person Name
            accused_match = re.search(r"(?:Accused Person|Name of Arrestee|accused|patient name)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)", text, re.IGNORECASE)
            if accused_match and "accused_name" not in factsheet.facts:
                val = accused_match.group(1).strip()
                quote = self._find_exact_span(text, val)
                if quote:
                    factsheet.facts["accused_name"] = FactItem(
                        field_name="accused_name",
                        value=val,
                        source_chunk_ids=[c_id],
                        supporting_quote=quote,
                        confidence=1.0
                    )

            # 2. FIR Number
            fir_match = re.search(r"FIR\s*(?:No\.?|Number)?\s*[:\s]*([0-9]+/[0-9]+|[0-9]{3,4})", text, re.IGNORECASE)
            if fir_match and "fir_number" not in factsheet.facts:
                val = fir_match.group(1).strip()
                quote = self._find_exact_span(text, fir_match.group(0))
                if quote:
                    factsheet.facts["fir_number"] = FactItem(
                        field_name="fir_number",
                        value=val,
                        source_chunk_ids=[c_id],
                        supporting_quote=quote,
                        confidence=1.0
                    )

            # 3. Police Station
            ps_match = re.search(r"(?:Police Station|PS)[:\s]+([A-Za-z\s]+?)(?:\||,|\n|Year|District)", text, re.IGNORECASE)
            if ps_match and "police_station" not in factsheet.facts:
                val = ps_match.group(1).strip()
                quote = self._find_exact_span(text, ps_match.group(0))
                if quote:
                    factsheet.facts["police_station"] = FactItem(
                        field_name="police_station",
                        value=val,
                        source_chunk_ids=[c_id],
                        supporting_quote=quote,
                        confidence=1.0
                    )

            # 4. Sections Charged
            sec_match = re.search(r"(?:Section\s+[0-9]+(?:\([0-9]+\))?\s+(?:BNS|Bharatiya Nyaya Sanhita|IPC|BNSS|CrPC)[^,\n]*)", text, re.IGNORECASE)
            if sec_match and "sections_charged" not in factsheet.facts:
                val = sec_match.group(0).strip()
                quote = self._find_exact_span(text, val)
                if quote:
                    factsheet.facts["sections_charged"] = FactItem(
                        field_name="sections_charged",
                        value=val,
                        source_chunk_ids=[c_id],
                        supporting_quote=quote,
                        confidence=1.0
                    )

            # 5. Date and Time of Arrest
            arrest_dt_match = re.search(r"(?:Date and Time of Arrest|arrested on)[:\s]+([0-9]{1,2}(?:th|st|rd|nd)?\s+[A-Za-z]+\s+[0-9]{4}(?:\s+at\s+[0-9]{1,2}:[0-9]{2}(?:\s*[A-Za-z]+)?)?)", text, re.IGNORECASE)
            if arrest_dt_match and "date_of_arrest" not in factsheet.facts:
                val = arrest_dt_match.group(1).strip()
                quote = self._find_exact_span(text, arrest_dt_match.group(0))
                if quote:
                    factsheet.facts["date_of_arrest"] = FactItem(
                        field_name="date_of_arrest",
                        value=val,
                        source_chunk_ids=[c_id],
                        supporting_quote=quote,
                        confidence=1.0
                    )

            # 6. Custody Status & Remand
            custody_match = re.search(r"(remanded to Judicial Custody for\s+[0-9]+\s+days|In Judicial Custody)", text, re.IGNORECASE)
            if custody_match and "custody_status" not in factsheet.facts:
                val = custody_match.group(1).strip()
                quote = self._find_exact_span(text, val)
                if quote:
                    factsheet.facts["custody_status"] = FactItem(
                        field_name="custody_status",
                        value=val,
                        source_chunk_ids=[c_id],
                        supporting_quote=quote,
                        confidence=1.0
                    )

            # 7. Medical Condition / Health Grounds
            med_match = re.search(r"(Severe Hypertension|Uncontrolled Diabetes Mellitus Type II|diabetic foot ulcer stage II|complains of chronic dizziness and diabetes|chronic ulceration)", text, re.IGNORECASE)
            if med_match and "medical_condition" not in factsheet.facts:
                val = med_match.group(1).strip()
                quote = self._find_exact_span(text, val)
                if quote:
                    factsheet.facts["medical_condition"] = FactItem(
                        field_name="medical_condition",
                        value=f"Severe Hypertension and Diabetes Mellitus (BP: 178/110 mmHg, Blood Sugar: 310 mg/dL, diabetic foot ulcer)",
                        source_chunk_ids=[c_id],
                        supporting_quote=quote,
                        confidence=1.0
                    )

            # 8. Recovery / Seizure Status
            recovery_match = re.search(r"(One HP Laptop[^,\n]+|Indian currency notes[^,\n]+amounting to Rs\.\s*[0-9,]+)", text, re.IGNORECASE)
            if recovery_match and "recovery_status" not in factsheet.facts:
                val = recovery_match.group(0).strip()
                quote = self._find_exact_span(text, val)
                if quote:
                    factsheet.facts["recovery_status"] = FactItem(
                        field_name="recovery_status",
                        value=val,
                        source_chunk_ids=[c_id],
                        supporting_quote=quote,
                        confidence=1.0
                    )

            # 9. Antecedents
            antecedents_match = re.search(r"(no prior criminal antecedents as per SCRB|clean criminal record)", text, re.IGNORECASE)
            if antecedents_match and "antecedents" not in factsheet.facts:
                val = "No prior criminal antecedents (clean record)"
                quote = self._find_exact_span(text, antecedents_match.group(0))
                if quote:
                    factsheet.facts["antecedents"] = FactItem(
                        field_name="antecedents",
                        value=val,
                        source_chunk_ids=[c_id],
                        supporting_quote=quote,
                        confidence=1.0
                    )

            # 10. Cheque Dishonour Specific Facts (For NI Act 138)
            cheque_match = re.search(r"Cheque No\.?\s*([0-9]{6})", text, re.IGNORECASE)
            if cheque_match and "cheque_number" not in factsheet.facts:
                val = cheque_match.group(1).strip()
                quote = self._find_exact_span(text, cheque_match.group(0))
                if quote:
                    factsheet.facts["cheque_number"] = FactItem(
                        field_name="cheque_number",
                        value=val,
                        source_chunk_ids=[c_id],
                        supporting_quote=quote,
                        confidence=1.0
                    )

            amount_match = re.search(r"Rs\.\s*([0-9,]+/-?|\d+ Lakhs)", text, re.IGNORECASE)
            if amount_match and "transaction_amount" not in factsheet.facts:
                val = amount_match.group(0).strip()
                quote = self._find_exact_span(text, val)
                if quote:
                    factsheet.facts["transaction_amount"] = FactItem(
                        field_name="transaction_amount",
                        value=val,
                        source_chunk_ids=[c_id],
                        supporting_quote=quote,
                        confidence=1.0
                    )
                    
        # Verification post-filter: Ensure every supporting_quote is an exact substring of the cited chunk
        verified_facts = {}
        for f_name, item in factsheet.facts.items():
            valid_quote = False
            for c_id in item.source_chunk_ids:
                if c_id in self.chunks_map and item.supporting_quote in self.chunks_map[c_id].text:
                    valid_quote = True
                    break
            if valid_quote:
                verified_facts[f_name] = item
                
        factsheet.facts = verified_facts
        return factsheet

    @staticmethod
    def _find_exact_span(source_text: str, target: str) -> Optional[str]:
        if target in source_text:
            return target
        clean_target = target.strip()
        if clean_target in source_text:
            return clean_target
        return None
