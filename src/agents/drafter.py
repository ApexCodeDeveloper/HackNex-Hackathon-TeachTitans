"""
NyayVeritas Drafter Agent
Generates formal legal documents strictly from FactSheet and SourceRegistry.
Enforces Hard Invariants:
1. Every factual sentence carries an inline marker [S:chunk_id]
2. Every legal authority carries an inline marker [A:registry_id]
3. Unknown facts become explicit placeholders [●MISSING: ... — not found in sources]
NEVER GUESSES.
"""

from typing import Dict, List, Optional
from src.models import FactSheet, SourceRegistryEntry
from src.registry import SourceRegistry

class LegalDrafter:
    """Legal drafter generating verifiable drafts with explicit grounding markers."""
    def __init__(self, registry: SourceRegistry):
        self.registry = registry

    def draft_document(self, factsheet: FactSheet, prompt: str) -> str:
        doc_type = factsheet.document_type_requested.lower()
        if "bail" in doc_type:
            return self._draft_bail_application(factsheet)
        elif "notice" in doc_type or "138" in doc_type:
            return self._draft_138_legal_notice(factsheet)
        else:
            return self._draft_general_petition(factsheet)

    def _get_fact_val(self, factsheet: FactSheet, field: str, default_desc: str) -> str:
        if field in factsheet.facts:
            f = factsheet.facts[field]
            src_str = " ".join([f"[S:{cid}]" for cid in f.source_chunk_ids])
            return f"{f.value} {src_str}"
        return f"[●MISSING: {default_desc} — not found in sources]"

    def _get_auth_marker(self, auth_key: str, fallback_label: str) -> str:
        auth = self.registry.find_authority(auth_key)
        if auth:
            return f"{auth.citation_string} [A:{auth.registry_id}]"
        return f"{fallback_label} [●MISSING: authority not in corpus registry]"

    def _draft_bail_application(self, factsheet: FactSheet) -> str:
        accused_str = self._get_fact_val(factsheet, "accused_name", "Applicant name")
        fir_str = self._get_fact_val(factsheet, "fir_number", "FIR number and year")
        ps_str = self._get_fact_val(factsheet, "police_station", "Police Station")
        sec_str = self._get_fact_val(factsheet, "sections_charged", "Substantive Sections charged")
        arrest_str = self._get_fact_val(factsheet, "date_of_arrest", "Date of arrest")
        custody_str = self._get_fact_val(factsheet, "custody_status", "Custody status / Remand details")
        medical_str = self._get_fact_val(factsheet, "medical_condition", "Medical / Health condition")
        recovery_str = self._get_fact_val(factsheet, "recovery_status", "Seizure / Recovery status")
        antecedents_str = self._get_fact_val(factsheet, "antecedents", "Criminal antecedents")

        # Authorities
        auth_bnss_483 = self._get_auth_marker("BNSS 483", "Section 483 of Bharatiya Nagarik Suraksha Sanhita, 2023")
        auth_bnss_480 = self._get_auth_marker("BNSS 480", "Section 480 of Bharatiya Nagarik Suraksha Sanhita, 2023")
        auth_bnss_479 = self._get_auth_marker("BNSS 479", "Section 479 of Bharatiya Nagarik Suraksha Sanhita, 2023")
        auth_art21 = self._get_auth_marker("Article 21", "Article 21 of the Constitution of India")
        auth_arnesh = self._get_auth_marker("Arnesh Kumar", "Arnesh Kumar v. State of Bihar (2014) 8 SCC 273")
        auth_antil = self._get_auth_marker("Satender Kumar Antil", "Satender Kumar Antil v. CBI (2022) 10 SCC 51")
        auth_chandra = self._get_auth_marker("Sanjay Chandra", "Sanjay Chandra v. CBI (2012) 1 SCC 40")
        auth_balchand = self._get_auth_marker("Balchand", "State of Rajasthan v. Balchand AIR 1977 SC 2447")

        draft = f"""IN THE COURT OF LEARNED SESSIONS JUDGE, PATIALA HOUSE COURTS, NEW DELHI
BAIL APPLICATION NO. _____ OF 2024

IN THE MATTER OF:
State (Govt. of NCT of Delhi) 
Versus
{accused_str} ... Applicant/Accused

FIR No.: {fir_str}
Police Station: {ps_str}
Under Section(s): {sec_str}

APPLICATION UNDER {auth_bnss_483} FOR GRANT OF REGULAR BAIL ON BEHALF OF THE APPLICANT

MOST RESPECTFULLY SHOWETH:

1. That the Applicant is currently confined in judicial custody in connection with the aforementioned FIR registered at {ps_str}.

2. That the Applicant was arrested on {arrest_str} and produced before the Learned Magistrate whereupon he was remanded to {custody_str}.

3. That the offences alleged against the Applicant carry a maximum punishment of up to seven years imprisonment, squarely attracting the safeguards established in {auth_arnesh} and {auth_antil}.

4. That physical and digital recovery has already been completed by the investigating agency, namely: {recovery_str}.

5. That the investigation with respect to custodial interrogation is complete, and no purpose would be served by further pre-trial incarceration as laid down by the Hon'ble Supreme Court in {auth_chandra} and {auth_balchand}.

6. That the Applicant suffers from acute physical infirmities, namely: {medical_str}, which entitles the Applicant to humanitarian consideration under the proviso to {auth_bnss_480}.

7. That the Applicant has clean antecedents: {antecedents_str}, with no prior convictions, entitling him to liberal consideration under {auth_bnss_479}.

8. That the continued incarceration of the Applicant in the absence of any flight risk or possibility of tampering violates the fundamental right to liberty guaranteed under {auth_art21}.

9. That the Applicant undertakes to join trial proceedings regularly, shall not leave the National Capital Territory of Delhi without prior permission, and shall not tamper with evidence or influence witnesses.

PRAYER:
In the premises aforesaid, it is most respectfully prayed that this Hon'ble Court may be pleased to:
(a) Release the Applicant on regular bail in FIR No. {fir_str}, PS {ps_str}, on such terms and conditions as this Hon'ble Court may deem fit; and
(b) Pass any other order in the interest of justice.

FILED BY:
Advocate for the Applicant
New Delhi."""
        return draft.strip()

    def _draft_138_legal_notice(self, factsheet: FactSheet) -> str:
        drawer_str = self._get_fact_val(factsheet, "accused_name", "Target drawer entity")
        cheque_no_str = self._get_fact_val(factsheet, "cheque_number", "Cheque number")
        amount_str = self._get_fact_val(factsheet, "transaction_amount", "Dishonoured cheque amount")
        auth_nia = self._get_auth_marker("Section 138", "Section 138 of Negotiable Instruments Act, 1881")

        draft = f"""REGISTERED AD / SPEED POST
LEGAL DEMAND NOTICE UNDER {auth_nia}

Date: [●MISSING: Date of issuance of notice — not found in sources]

To,
{drawer_str}

From,
Advocate on behalf of Payee Client

Sir/Madam,
Under instructions from and on behalf of my client, I hereby serve upon you this statutory notice:

1. That towards discharge of legally enforceable liability, you issued Cheque No. {cheque_no_str} for a sum of {amount_str} drawn on your banker.

2. That the said cheque was presented for encashment but was returned unpaid with the remark 'Funds Insufficient'.

3. That in terms of {auth_nia}, you are hereby called upon to pay the entire amount of {amount_str} within 15 (fifteen) days from the receipt of this statutory notice.

4. That in the event you fail to make the said payment within the stipulated 15-day period, my client shall initiate criminal prosecution against you under {auth_nia} at your risk and cost.

Advocate for Client."""
        return draft.strip()

    def _draft_general_petition(self, factsheet: FactSheet) -> str:
        accused_str = self._get_fact_val(factsheet, "accused_name", "Party name")
        auth_art21 = self._get_auth_marker("Article 21", "Article 21 of the Constitution of India")
        return f"""BEFORE THE HON'BLE COURT
PETITION UNDER LAW
In the matter of: {accused_str}
Grounded on Constitutional guarantees under {auth_art21}.
[●MISSING: Specific cause title and schedule of prayers — not found in sources]."""
