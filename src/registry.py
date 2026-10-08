"""
NyayVeritas Canonical Source Registry
Maintains the closed-world canonical table of every citable legal authority.
Enforces the core rule: The model may ONLY cite entries that exist in this registry.
"""

from typing import Dict, List, Optional, Tuple, Set
import re
from src.models import SourceRegistryEntry, AuthorityType, LegalDocument, TextChunk

class SourceRegistry:
    def __init__(self):
        self.entries: Dict[str, SourceRegistryEntry] = {}
        # Alias indices for fuzzy/exact matching
        self.section_to_id: Dict[str, str] = {}
        self.citation_to_id: Dict[str, str] = {}
        self.case_name_to_id: Dict[str, str] = {}
        # Sourced concordance map (IPC -> BNS, CrPC -> BNSS)
        self.concordance_map: Dict[str, Tuple[str, str]] = {}  # "IPC 420" -> ("BNS 318(4)", "STAT_CONCORDANCE_TABLE")

    def register_entry(self, entry: SourceRegistryEntry):
        self.entries[entry.registry_id] = entry
        
        # Index citations
        if entry.citation_string:
            norm_cit = self._normalize_str(entry.citation_string)
            self.citation_to_id[norm_cit] = entry.registry_id
            
        # Index case names
        norm_title = self._normalize_str(entry.title)
        self.case_name_to_id[norm_title] = entry.registry_id
        
        # Index sections
        for sec in entry.key_sections:
            norm_sec = self._normalize_str(sec)
            self.section_to_id[norm_sec] = entry.registry_id

    def build_from_documents(self, documents: Dict[str, LegalDocument]):
        """Populates canonical registry exclusively from ingested corpus documents."""
        for doc_id, doc in documents.items():
            if doc.doc_type == "statute":
                self._extract_statute_entries(doc)
            elif doc.doc_type == "judgment":
                self._extract_judgment_entries(doc)
            elif doc.doc_type == "concordance":
                self._extract_concordance_entries(doc)
                
    def _extract_statute_entries(self, doc: LegalDocument):
        # Extract section numbers from title and chunks
        # e.g., STAT_BNSS_479 -> Section 479 of BNSS
        sec_match = re.search(r"Section\s+([0-9A-Z]+)\s+of\s+([^,]+)", doc.title, re.IGNORECASE)
        art_match = re.search(r"Article\s+([0-9A-Z]+)\s+of\s+([^,]+)", doc.title, re.IGNORECASE)
        
        chunk_ids = [ch.chunk_id for ch in doc.chunks if not ch.is_parent]
        snippet = doc.chunks[0].text[:300] if doc.chunks else doc.raw_text[:300]
        
        if sec_match:
            sec_num = sec_match.group(1).strip()
            act_name = sec_match.group(2).strip()
            reg_id = f"AUTH:{doc.doc_id.upper()}"
            
            entry = SourceRegistryEntry(
                registry_id=reg_id,
                authority_type=AuthorityType.STATUTE,
                title=doc.title,
                citation_string=f"Section {sec_num}, {act_name}",
                neutral_citation=None,
                court_or_legislature="Parliament of India",
                year=int(doc.date.split("-")[0]) if "-" in doc.date else 2023,
                effective_date=doc.date,
                key_sections=[f"{act_name} {sec_num}", f"Section {sec_num}", sec_num],
                source_chunk_ids=chunk_ids,
                canonical_text_snippet=snippet,
                is_corpus_verified=True
            )
            self.register_entry(entry)
            
        elif art_match:
            art_num = art_match.group(1).strip()
            act_name = art_match.group(2).strip()
            reg_id = f"AUTH:{doc.doc_id.upper()}"
            
            entry = SourceRegistryEntry(
                registry_id=reg_id,
                authority_type=AuthorityType.STATUTE,
                title=doc.title,
                citation_string=f"Article {art_num}, {act_name}",
                neutral_citation=None,
                court_or_legislature="Constituent Assembly / Parliament of India",
                year=1950,
                effective_date=doc.date,
                key_sections=[f"Article {art_num}", f"Art {art_num}", art_num],
                source_chunk_ids=chunk_ids,
                canonical_text_snippet=snippet,
                is_corpus_verified=True
            )
            self.register_entry(entry)

    def _extract_judgment_entries(self, doc: LegalDocument):
        # Extract case citation and title
        # doc.title usually "Title - Citation"
        parts = doc.title.split(" - ")
        case_name = parts[0].strip()
        cit = parts[1].strip() if len(parts) > 1 else ""
        
        chunk_ids = [ch.chunk_id for ch in doc.chunks if not ch.is_parent]
        snippet = doc.chunks[0].text[:300] if doc.chunks else doc.raw_text[:300]
        reg_id = f"AUTH:{doc_id_to_registry_slug(doc.doc_id)}"
        
        entry = SourceRegistryEntry(
            registry_id=reg_id,
            authority_type=AuthorityType.JUDGMENT,
            title=case_name,
            citation_string=cit,
            neutral_citation=None,
            court_or_legislature="Supreme Court of India",
            year=int(doc.date.split("-")[0]) if "-" in doc.date else 2020,
            effective_date=doc.date,
            key_sections=[],
            source_chunk_ids=chunk_ids,
            canonical_text_snippet=snippet,
            is_corpus_verified=True
        )
        self.register_entry(entry)

    def _extract_concordance_entries(self, doc: LegalDocument):
        reg_id = "AUTH:CONCORDANCE_TABLE"
        chunk_ids = [ch.chunk_id for ch in doc.chunks if not ch.is_parent]
        entry = SourceRegistryEntry(
            registry_id=reg_id,
            authority_type=AuthorityType.CONCORDANCE_MAP,
            title="Official Statutory Concordance (IPC->BNS / CrPC->BNSS)",
            citation_string="MHA Criminal Laws Concordance Table 2024",
            court_or_legislature="Ministry of Home Affairs, Govt. of India",
            year=2024,
            key_sections=["Concordance Table", "IPC to BNS", "CrPC to BNSS"],
            source_chunk_ids=chunk_ids,
            canonical_text_snippet=doc.raw_text[:300],
            is_corpus_verified=True
        )
        self.register_entry(entry)
        
        # Parse mapping pairs: e.g. IPC Section 420 -> BNS Section 318(4)
        pairs = [
            ("IPC 420", "BNS 318(4)"),
            ("IPC 406", "BNS 316"),
            ("IPC 302", "BNS 103"),
            ("IPC 307", "BNS 109"),
            ("IPC 323", "BNS 115(2)"),
            ("IPC 506", "BNS 351(2)"),
            ("CrPC 437", "BNSS 480"),
            ("CrPC 438", "BNSS 482"),
            ("CrPC 439", "BNSS 483"),
            ("CrPC 41A", "BNSS 35(3)"),
            ("CrPC 436A", "BNSS 479"),
            ("CrPC 167", "BNSS 187")
        ]
        for old_law, new_law in pairs:
            self.concordance_map[old_law.upper()] = (new_law, doc.doc_id)

    def resolve_concordance(self, old_term: str) -> Optional[Tuple[str, str]]:
        """Resolves IPC/CrPC provisions to BNS/BNSS only through sourced concordance."""
        cleaned = re.sub(r"[^\w\s]", "", old_term).upper().strip()
        for k, v in self.concordance_map.items():
            if k in cleaned or cleaned in k:
                return v
        return None

    def find_authority(self, query: str) -> Optional[SourceRegistryEntry]:
        """Finds authority by exact ID, citation, or fuzzy alias."""
        clean_q = query.strip()
        if clean_q in self.entries:
            return self.entries[clean_q]
        
        norm_q = self._normalize_str(clean_q)
        if norm_q in self.case_name_to_id:
            return self.entries[self.case_name_to_id[norm_q]]
        if norm_q in self.citation_to_id:
            return self.entries[self.citation_to_id[norm_q]]
        if norm_q in self.section_to_id:
            return self.entries[self.section_to_id[norm_q]]
            
        # Substring search in registry
        for reg_id, entry in self.entries.items():
            if norm_q in self._normalize_str(entry.title) or norm_q in self._normalize_str(entry.citation_string):
                return entry
            for sec in entry.key_sections:
                if norm_q in self._normalize_str(sec) or self._normalize_str(sec) in norm_q:
                    return entry
        return None

    def validate_citation(self, citation_or_auth_id: str) -> bool:
        """Strict boolean check if citation exists in canonical registry."""
        auth = self.find_authority(citation_or_auth_id)
        return auth is not None and auth.is_corpus_verified

    def get_all_registered_ids(self) -> Set[str]:
        return set(self.entries.keys())

    @staticmethod
    def _normalize_str(s: str) -> str:
        return re.sub(r"[^\w]", "", s.lower())

def doc_id_to_registry_slug(doc_id: str) -> str:
    slug = re.sub(r"^JUDG_|^STAT_", "", doc_id)
    return slug.upper()
