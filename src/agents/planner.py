"""
NyayVeritas Planner Agent
Decomposes a legal drafting or case review task into formal information needs,
required legal sections, landmark authorities, and mandatory case facts.
"""

from typing import Dict, List, Any
from src.models import AuthorityType

class LegalPlanner:
    """Plans information gathering based on legal document type and Indian procedure."""
    
    REQUIRED_FACTS = {
        "bail_application": [
            ("accused_name", "Name and identity of applicant"),
            ("fir_number", "First Information Report number and year"),
            ("police_station", "Territorial Police Station"),
            ("sections_charged", "Substantive penal sections invoked"),
            ("date_of_arrest", "Exact date and time of arrest"),
            ("custody_status", "Current custody status (Judicial Custody / Police Custody)"),
            ("chargesheet_status", "Whether chargesheet under Sec 193 BNSS / 173 CrPC filed"),
            ("medical_condition", "Medical ailments, MLC findings or infirmity"),
            ("recovery_completed", "Whether recoveries / seizures have been effected"),
            ("antecedents", "Criminal antecedents / clean record")
        ],
        "legal_notice_138": [
            ("payee_name", "Complainant / Payee entity"),
            ("drawer_name", "Drawer / Accused company or person"),
            ("cheque_number", "Dishonoured cheque number"),
            ("cheque_amount", "Cheque amount in figures and words"),
            ("cheque_date", "Date of issuance of cheque"),
            ("dishonour_date", "Date of bank return memo"),
            ("dishonour_reason", "Specific return reason (e.g. Funds Insufficient)"),
            ("statutory_demand_period", "Mandatory 15-day payment demand window")
        ],
        "affidavit": [
            ("deponent_name", "Full name and age of deponent"),
            ("deponent_address", "Residential address"),
            ("verification_clause", "Knowledge vs belief verification clause"),
            ("case_title", "Cause title of court proceeding")
        ],
        "petition": [
            ("petitioner_name", "Petitioner particulars"),
            ("respondent_name", "Respondent state or authority"),
            ("relief_sought", "Specific prayer / relief"),
            ("statutory_provision", "Enabling statutory section or Constitutional Article")
        ]
    }
    
    TARGET_AUTHORITIES = {
        "bail_application": [
            "STAT_BNSS_483", "STAT_BNSS_480", "STAT_BNSS_479",
            "JUDG_SC_ARNESH_KUMAR_2014", "JUDG_SC_SATENDER_ANTIL_2022",
            "JUDG_SC_SANJAY_CHANDRA_2012", "JUDG_SC_BALCHAND_1977",
            "STAT_CONST_ART21"
        ],
        "legal_notice_138": [
            "STAT_NIA_138"
        ],
        "anticipatory_bail": [
            "STAT_BNSS_482", "STAT_BNSS_35",
            "JUDG_SC_GURBAKSH_SIBBIA_1980", "JUDG_SC_ARNESH_KUMAR_2014"
        ]
    }

    def plan_task(self, prompt: str, doc_type: str = "bail_application") -> Dict[str, Any]:
        doc_type_clean = doc_type.lower()
        if "notice" in prompt.lower() or "138" in prompt.lower() or "cheque" in prompt.lower():
            doc_type_clean = "legal_notice_138"
        elif "anticipatory" in prompt.lower():
            doc_type_clean = "anticipatory_bail"
        elif "bail" in prompt.lower():
            doc_type_clean = "bail_application"
            
        req_fields = self.REQUIRED_FACTS.get(doc_type_clean, self.REQUIRED_FACTS["bail_application"])
        target_auths = self.TARGET_AUTHORITIES.get(doc_type_clean, self.TARGET_AUTHORITIES["bail_application"])
        
        search_queries = [
            f"Case records FIR arrest memo medical condition chargesheet {prompt}",
            f"Statutory provisions {' '.join(target_auths[:4])}",
            f"Landmark Supreme Court guidelines bail {doc_type_clean}"
        ]
        
        return {
            "document_type": doc_type_clean,
            "required_fields": req_fields,
            "target_authorities": target_auths,
            "search_queries": search_queries,
            "procedural_regime": "BNSS_2023" if "2024" in prompt or "bnss" in prompt.lower() else "CRPC_1973"
        }
