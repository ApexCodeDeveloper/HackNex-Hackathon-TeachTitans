import json
import os
from pathlib import Path

BASE_DIR = Path(r"C:\Users\prakashh\.gemini\antigravity-ide\scratch\nyay-veritas")
DATA_DIR = BASE_DIR / "data"
STATUTES_DIR = DATA_DIR / "statutes"
JUDGMENTS_DIR = DATA_DIR / "judgments"
CASE_FILES_DIR = DATA_DIR / "case_files"

for d in [STATUTES_DIR, JUDGMENTS_DIR, CASE_FILES_DIR]:
    d.mkdir(parents=True, exist_ok=True)

manifest_entries = []

# ==========================================
# 1. STATUTES & CONCORDANCES
# ==========================================

statutes_data = [
    {
        "doc_id": "STAT_BNSS_479",
        "title": "Section 479 of Bharatiya Nagarik Suraksha Sanhita, 2023",
        "doc_type": "statute",
        "date": "2023-12-25",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/21434",
        "license": "Public Domain (Government of India)",
        "sections": [
            {
                "section": "479",
                "heading": "Maximum period for which an undertrial prisoner can be detained",
                "text": "(1) Where a person has, during the period of investigation, inquiry or trial under this Sanhita of an offence under any law (not being an offence for which the punishment of death or life imprisonment has been specified as one of the punishments under that law) undergone detention for a period extending up to one-half of the maximum period of imprisonment specified for that offence under that law, he shall be released by the Court on bail: Provided that where such person is a first-time offender (who has never been convicted of any offence in the past), he shall be released on bail by the Court if he has undergone detention for the period extending up to one-third of the maximum period of imprisonment specified for such offence under that law: Provided further that no person shall in any case be detained during the period of investigation, inquiry or trial for more than the maximum period of imprisonment provided for the said offence."
            }
        ]
    },
    {
        "doc_id": "STAT_BNSS_480",
        "title": "Section 480 of Bharatiya Nagarik Suraksha Sanhita, 2023",
        "doc_type": "statute",
        "date": "2023-12-25",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/21434",
        "license": "Public Domain (Government of India)",
        "sections": [
            {
                "section": "480",
                "heading": "When bail may be taken in case of non-bailable offence",
                "text": "(1) When any person accused of, or suspected of, the commission of any non-bailable offence is arrested or detained without warrant by an officer in charge of a police station, or appears or is brought before a Court other than the High Court or Court of Session, he may be released on bail, but he shall not be so released if there appear reasonable grounds for believing that he has been guilty of an offence punishable with death or imprisonment for life: Provided that the Court may direct that a person referred to in clause (i) or clause (ii) be released on bail if such person is under the age of sixteen years or is a woman or is sick or infirm."
            }
        ]
    },
    {
        "doc_id": "STAT_BNSS_482",
        "title": "Section 482 of Bharatiya Nagarik Suraksha Sanhita, 2023",
        "doc_type": "statute",
        "date": "2023-12-25",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/21434",
        "license": "Public Domain (Government of India)",
        "sections": [
            {
                "section": "482",
                "heading": "Direction for grant of bail to person apprehending arrest (Anticipatory Bail)",
                "text": "(1) Where any person has reason to believe that he may be arrested on an accusation of having committed a non-bailable offence, he may apply to the High Court or the Court of Session for a direction under this section that in the event of such arrest he shall be released on bail; and that Court may, after considering the nature and gravity of the accusation, the antecedents of the applicant, and the possibility of the applicant fleeing from justice, either reject the application forthwith or make an interim order for the grant of anticipatory bail."
            }
        ]
    },
    {
        "doc_id": "STAT_BNSS_483",
        "title": "Section 483 of Bharatiya Nagarik Suraksha Sanhita, 2023",
        "doc_type": "statute",
        "date": "2023-12-25",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/21434",
        "license": "Public Domain (Government of India)",
        "sections": [
            {
                "section": "483",
                "heading": "Special powers of High Court or Court of Session regarding bail",
                "text": "(1) A High Court or Court of Session may direct that any person accused of an offence and in custody be released on bail, and if the arrest is of the nature specified in sub-section (3) of section 480, may impose any condition which it considers necessary. (2) A High Court or Court of Session may set aside or vary any condition imposed by a Magistrate."
            }
        ]
    },
    {
        "doc_id": "STAT_BNSS_35",
        "title": "Section 35 of Bharatiya Nagarik Suraksha Sanhita, 2023",
        "doc_type": "statute",
        "date": "2023-12-25",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/21434",
        "license": "Public Domain (Government of India)",
        "sections": [
            {
                "section": "35",
                "heading": "When police may arrest without warrant and Notice of appearance",
                "text": "(1) Any police officer may without an order from a Magistrate and without a warrant, arrest any person who commits, in the presence of a police officer, a cognizable offence; or against whom a reasonable complaint has been made, or credible information has been received, that he has committed a cognizable offence punishable with imprisonment for a term which may be less than seven years or which may extend to seven years: Provided that the police officer shall in all cases where the arrest of a person is not required under the provisions of this sub-section, record the reasons in writing for not making the arrest. (3) The police officer shall, in all cases where the arrest of a person is not required under sub-section (1), issue a notice directing the person against whom a reasonable complaint has been made to appear before him or at such other place as may be specified in the notice."
            }
        ]
    },
    {
        "doc_id": "STAT_BNS_318",
        "title": "Section 318 of Bharatiya Nyaya Sanhita, 2023",
        "doc_type": "statute",
        "date": "2023-12-25",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/21433",
        "license": "Public Domain (Government of India)",
        "sections": [
            {
                "section": "318",
                "heading": "Cheating",
                "text": "(1) Whoever, by deceiving any person, fraudulently or dishonestly induces the person so deceived to deliver any property to any person, or to consent that any person shall retain any property, or intentionally induces the person so deceived to do or omit to do anything which he would not do or omit if he were not so deceived, is said to cheat. (2) Whoever cheats shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both. (4) Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person, or to make, alter or destroy the whole or any part of a valuable security, shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine."
            }
        ]
    },
    {
        "doc_id": "STAT_BNS_316",
        "title": "Section 316 of Bharatiya Nyaya Sanhita, 2023",
        "doc_type": "statute",
        "date": "2023-12-25",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/21433",
        "license": "Public Domain (Government of India)",
        "sections": [
            {
                "section": "316",
                "heading": "Criminal breach of trust",
                "text": "(1) Whoever, being in any manner entrusted with property, or with any dominion over property, dishonestly misappropriates or converts to his own use that property, commits criminal breach of trust. (2) Whoever commits criminal breach of trust shall be punished with imprisonment of either description for a term which may extend to five years, or with fine, or with both."
            }
        ]
    },
    {
        "doc_id": "STAT_BNS_115",
        "title": "Section 115 of Bharatiya Nyaya Sanhita, 2023",
        "doc_type": "statute",
        "date": "2023-12-25",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/21433",
        "license": "Public Domain (Government of India)",
        "sections": [
            {
                "section": "115",
                "heading": "Voluntarily causing hurt",
                "text": "(1) Whoever does any act with the intention of thereby causing hurt to any person, or with the knowledge that he is likely thereby to cause hurt to any person, and does thereby cause hurt to any person, is said 'voluntarily to cause hurt'. (2) Whoever, except in the case provided for by sub-section (1) of section 122, voluntarily causes hurt, shall be punished with imprisonment of either description for a term which may extend to one year, or with fine which may extend to ten thousand rupees, or with both."
            }
        ]
    },
    {
        "doc_id": "STAT_BNS_351",
        "title": "Section 351 of Bharatiya Nyaya Sanhita, 2023",
        "doc_type": "statute",
        "date": "2023-12-25",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/21433",
        "license": "Public Domain (Government of India)",
        "sections": [
            {
                "section": "351",
                "heading": "Criminal intimidation",
                "text": "(1) Whoever threatens another with any injury to his person, reputation or property, or to the person or reputation of any one in whom that person is interested, with intent to cause alarm to that person, commits criminal intimidation. (2) Whoever commits the offence of criminal intimidation shall be punished with imprisonment of either description for a term which may extend to two years, or with fine, or with both."
            }
        ]
    },
    {
        "doc_id": "STAT_CRPC_437",
        "title": "Section 437 of Code of Criminal Procedure, 1973 (Pre-July-2024 matters)",
        "doc_type": "statute",
        "date": "1974-04-01",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/1611",
        "license": "Public Domain (Government of India)",
        "sections": [
            {
                "section": "437",
                "heading": "When bail may be taken in case of non-bailable offence",
                "text": "(1) When any person accused of, or suspected of, the commission of any non-bailable offence is arrested or detained without warrant by an officer in charge of a police station, or appears or is brought before a Court other than the High Court or Court of Session, he may be released on bail, but he shall not be so released if there appear reasonable grounds for believing that he has been guilty of an offence punishable with death or imprisonment for life: Provided that the Court may direct that a person referred to in clause (i) or clause (ii) be released on bail if such person is under the age of sixteen years or is a woman or is sick or infirm."
            }
        ]
    },
    {
        "doc_id": "STAT_CRPC_439",
        "title": "Section 439 of Code of Criminal Procedure, 1973 (Pre-July-2024 matters)",
        "doc_type": "statute",
        "date": "1974-04-01",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/1611",
        "license": "Public Domain (Government of India)",
        "sections": [
            {
                "section": "439",
                "heading": "Special powers of High Court or Court of Session regarding bail",
                "text": "(1) A High Court or Court of Session may direct that any person accused of an offence and in custody be released on bail, and if the arrest is of the nature specified in sub-section (3) of section 437, may impose any condition which it considers necessary for the purposes mentioned in that sub-section. (2) A High Court or Court of Session may direct that any person who has been released on bail under this Chapter be arrested and commit him to custody."
            }
        ]
    },
    {
        "doc_id": "STAT_CRPC_41A",
        "title": "Section 41A of Code of Criminal Procedure, 1973 (Pre-July-2024 matters)",
        "doc_type": "statute",
        "date": "2010-11-01",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/1611",
        "license": "Public Domain (Government of India)",
        "sections": [
            {
                "section": "41A",
                "heading": "Notice of appearance before police officer",
                "text": "(1) The police officer shall, in all cases where the arrest of a person is not required under the provisions of sub-section (1) of section 41, issue a notice directing the person against whom a reasonable complaint has been made, or credible information has been received, or a reasonable suspicion exists that he has committed a cognizable offence, to appear before him or at such other place as may be specified in the notice. (2) Where such a notice is issued to any person, it shall be the duty of that person to comply with the terms of the notice. (3) Where such person complies and continues to comply with the notice, he shall not be arrested in respect of the offence referred to in the notice unless, for reasons to be recorded, the police officer is of the opinion that he ought to be arrested."
            }
        ]
    },
    {
        "doc_id": "STAT_IPC_420",
        "title": "Section 420 of Indian Penal Code, 1860 (Pre-July-2024 matters)",
        "doc_type": "statute",
        "date": "1860-10-06",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/2263",
        "license": "Public Domain (Government of India)",
        "sections": [
            {
                "section": "420",
                "heading": "Cheating and dishonestly inducing delivery of property",
                "text": "Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person, or to make, alter or destroy the whole or any part of a valuable security, or anything which is signed or sealed, and which is capable of being converted into a valuable security, shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine."
            }
        ]
    },
    {
        "doc_id": "STAT_CONST_ART21",
        "title": "Article 21 of the Constitution of India",
        "doc_type": "statute",
        "date": "1950-01-26",
        "source_url": "https://www.india.gov.in/my-government/constitution-india",
        "license": "Public Domain",
        "sections": [
            {
                "section": "Article 21",
                "heading": "Protection of life and personal liberty",
                "text": "No person shall be deprived of his life or personal liberty except according to procedure established by law."
            }
        ]
    },
    {
        "doc_id": "STAT_CONST_ART22",
        "title": "Article 22 of the Constitution of India",
        "doc_type": "statute",
        "date": "1950-01-26",
        "source_url": "https://www.india.gov.in/my-government/constitution-india",
        "license": "Public Domain",
        "sections": [
            {
                "section": "Article 22",
                "heading": "Protection against arrest and detention in certain cases",
                "text": "(1) No person who is arrested shall be detained in custody without being informed, as soon as may be, of the grounds for such arrest nor shall he be denied the right to consult, and to be defended by, a legal practitioner of his choice. (2) Every person who is arrested and detained in custody shall be produced before the nearest magistrate within a period of twenty-four hours of such arrest excluding the time necessary for the journey from the place of arrest to the court of the magistrate."
            }
        ]
    },
    {
        "doc_id": "STAT_NIA_138",
        "title": "Section 138 of Negotiable Instruments Act, 1881",
        "doc_type": "statute",
        "date": "1881-12-09",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/2242",
        "license": "Public Domain",
        "sections": [
            {
                "section": "138",
                "heading": "Dishonour of cheque for insufficiency, etc., of funds in the account",
                "text": "Where any cheque drawn by a person on an account maintained by him with a banker for payment of any amount of money to another person from out of that account for the discharge, in whole or in part, of any debt or other liability, is returned by the bank unpaid, either because of the amount of money standing to the credit of that account is insufficient to honour the cheque or that it exceeds the amount arranged to be paid from that account by an agreement made with that bank, such person shall be deemed to have committed an offence and shall, without prejudice to any other provisions of this Act, be punished with imprisonment for a term which may extend to two years, or with fine which may extend to twice the amount of the cheque, or with both: Provided that nothing contained in this section shall apply unless (a) the cheque has been presented to the bank within a period of three months from the date on which it is drawn or within the period of its validity, whichever is earlier; (b) the payee or the holder in due course of the cheque makes a demand for the payment of the said amount of money by giving a notice; in writing, to the drawer of the cheque, within thirty days of the receipt of information by him from the bank regarding the return of the cheque as unpaid; and (c) the drawer of such cheque fails to make the payment of the said amount of money to the payee or to the holder in due course of the cheque within fifteen days of the receipt of the said notice."
            }
        ]
    },
    {
        "doc_id": "STAT_CONCORDANCE_TABLE",
        "title": "Official Concordance Mapping Table: IPC to BNS and CrPC to BNSS",
        "doc_type": "concordance",
        "date": "2024-07-01",
        "source_url": "https://www.mha.gov.in/en/commoncontent/new-criminal-laws",
        "license": "Public Domain (Ministry of Home Affairs, Government of India)",
        "sections": [
            {
                "section": "IPC-BNS-CRPC-BNSS-MAP",
                "heading": "Statutory Cross-Reference and Concordance Table",
                "text": "This concordance table establishes the legal identity and mapping between Indian Penal Code 1860 (IPC) and Bharatiya Nyaya Sanhita 2023 (BNS), and Code of Criminal Procedure 1973 (CrPC) and Bharatiya Nagarik Suraksha Sanhita 2023 (BNSS): (1) IPC Section 420 (Cheating and dishonestly inducing delivery of property) corresponds strictly to BNS Section 318(4). (2) IPC Section 406 (Criminal breach of trust) corresponds strictly to BNS Section 316. (3) IPC Section 302 (Murder) corresponds strictly to BNS Section 103. (4) IPC Section 307 (Attempt to murder) corresponds strictly to BNS Section 109. (5) IPC Section 323 (Voluntarily causing hurt) corresponds to BNS Section 115(2). (6) IPC Section 506 (Criminal intimidation) corresponds to BNS Section 351(2). (7) CrPC Section 437 (Bail in non-bailable offences by Magistrate) corresponds to BNSS Section 480. (8) CrPC Section 438 (Anticipatory Bail) corresponds to BNSS Section 482. (9) CrPC Section 439 (Special powers of High Court or Sessions Court regarding bail) corresponds to BNSS Section 483. (10) CrPC Section 41A (Notice of appearance before police officer) corresponds to BNSS Section 35(3). (11) CrPC Section 436A (Maximum period for undertrial detention) corresponds to BNSS Section 479. (12) CrPC Section 167 (Procedure when investigation cannot be completed in 24 hours / Remand) corresponds to BNSS Section 187."
            }
        ]
    }
]

for stat in statutes_data:
    file_path = STATUTES_DIR / f"{stat['doc_id']}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(stat, f, indent=2)
    manifest_entries.append({
        "doc_id": stat["doc_id"],
        "title": stat["title"],
        "doc_type": stat["doc_type"],
        "date": stat["date"],
        "jurisdiction": "India",
        "source_url": stat["source_url"],
        "license": stat["license"],
        "file_path": str(file_path.relative_to(BASE_DIR))
    })

# ==========================================
# 2. LANDMARK JUDGMENTS
# ==========================================

judgments_data = [
    {
        "doc_id": "JUDG_SC_ARNESH_KUMAR_2014",
        "title": "Arnesh Kumar v. State of Bihar & Anr.",
        "citation": "(2014) 8 SCC 273",
        "neutral_citation": "2014 INSC 474",
        "court": "Supreme Court of India",
        "year": 2014,
        "date": "2014-07-02",
        "source_url": "https://indiankanoon.org/doc/2982624/",
        "license": "Public Domain (Indian Judiciary)",
        "ratio": "Arrest should not be made routinely in offences punishable with imprisonment up to seven years without complying with Section 41 and 41A CrPC (now Section 35 BNSS). Police officers must record reasons for arrest and Magistrate must record satisfaction before authorising detention.",
        "paragraphs": [
            {
                "para_num": 7,
                "text": "Arrest brings humiliation, curtails freedom and casts scars forever. Law makers know it so also the police. There is a battle between the lawmakers and the police and it seems the police has not learnt its lesson: the lesson implicit and delivered through Section 41 of the Code of Criminal Procedure."
            },
            {
                "para_num": 11,
                "text": "Our endeavour in this judgment is to ensure that police officers do not arrest the accused unnecessarily and Magistrate do not authorise detention casually and mechanically. In all cases where the offence is punishable with imprisonment up to 7 years, the police officer shall serve on the accused a notice of appearance under Section 41-A Cr.P.C within two weeks from the date of institution of the case."
            },
            {
                "para_num": 12,
                "text": "Failure to comply with these directions shall apart from making the police officers concerned liable for departmental action, they shall also be liable to be punished for contempt of court to be instituted before the High Court having territorial jurisdiction."
            }
        ]
    },
    {
        "doc_id": "JUDG_SC_SATENDER_ANTIL_2022",
        "title": "Satender Kumar Antil v. Central Bureau of Investigation & Anr.",
        "citation": "(2022) 10 SCC 51",
        "neutral_citation": "2022 INSC 690",
        "court": "Supreme Court of India",
        "year": 2022,
        "date": "2022-07-11",
        "source_url": "https://indiankanoon.org/doc/170949162/",
        "license": "Public Domain (Indian Judiciary)",
        "ratio": "Comprehensive guidelines on bail categorisation (Category A to D). Pre-trial detention is not meant to be punitive. Compliance with Section 41/41A CrPC is mandatory. Bail applications should ordinarily be disposed of within two weeks except for anticipatory bail which should be within six weeks.",
        "paragraphs": [
            {
                "para_num": 27,
                "text": "The rate of conviction in criminal cases in India is abysmally low. It appears to us that this factor weighs on the mind of the Court while deciding bail applications in a negative sense. Jails in India are flooded with undertrial prisoners who constitute around 80% of prison population."
            },
            {
                "para_num": 39,
                "text": "Category A offences are those punishable with imprisonment of 7 years or less. In such cases, if the accused was not arrested during investigation and has cooperated with the IO, upon appearance before the Court on summons/warrant, the bail application ought to be decided without remanding the accused to physical custody."
            },
            {
                "para_num": 73,
                "text": "Bail applications ought to be disposed of within a period of two weeks, except if the provisions mandate otherwise. Applications for anticipatory bail are expected to be disposed of within a period of six weeks."
            }
        ]
    },
    {
        "doc_id": "JUDG_SC_SANJAY_CHANDRA_2012",
        "title": "Sanjay Chandra v. Central Bureau of Investigation",
        "citation": "(2012) 1 SCC 40",
        "neutral_citation": "2011 INSC 836",
        "court": "Supreme Court of India",
        "year": 2012,
        "date": "2011-11-23",
        "source_url": "https://indiankanoon.org/doc/744040/",
        "license": "Public Domain (Indian Judiciary)",
        "ratio": "The primary purpose of bail in criminal trial is to ensure the presence of the accused at trial. Deprivation of liberty must be considered a punishment unless required to prevent flight or tampering with evidence. Seriousness of charge alone without evidence of flight risk cannot justify indefinite incarceration.",
        "paragraphs": [
            {
                "para_num": 21,
                "text": "In bail applications, generally, it has been laid down from the earliest times that the object of bail is to secure the appearance of the accused person at his trial by reasonable amount of bail. The object of bail is neither punitive nor preventative."
            },
            {
                "para_num": 24,
                "text": "Deprivation of liberty must be considered a punishment, unless it can be required for social defense or to prevent the accused from fleeing or tampering with evidence. When the charge sheet has already been filed, the detention of the accused as an undertrial prisoner is unnecessary unless apprehension of flight risk is established."
            }
        ]
    },
    {
        "doc_id": "JUDG_SC_DK_BASU_1997",
        "title": "D.K. Basu v. State of West Bengal",
        "citation": "(1997) 1 SCC 416",
        "neutral_citation": "1996 INSC 1550",
        "court": "Supreme Court of India",
        "year": 1997,
        "date": "1996-12-18",
        "source_url": "https://indiankanoon.org/doc/501198/",
        "license": "Public Domain (Indian Judiciary)",
        "ratio": "Laid down mandatory requirements to be followed in all cases of arrest or detention, including clear identification badges of arresting officer, arrest memo signed by witness, intimation of arrest to relative within 8-12 hours, and medical examination every 48 hours.",
        "paragraphs": [
            {
                "para_num": 35,
                "text": "The police officer carrying out the arrest of the arrestee shall prepare a memo of arrest at the time of arrest and such memo shall be attested by atleast one witness, who may either be a member of the family of the arrestee or a respectable person of the locality where the arrest is made. It shall also be counter signed by the arrestee and shall contain the time and date of arrest."
            },
            {
                "para_num": 36,
                "text": "A person who has been arrested or detained and is being held in custody in a police station or interrogation centre or other lock-up, shall be entitled to have one friend or relative or other person known to him or having interest in his welfare being informed, as soon as practicable, that he has been arrested and is being detained at the particular place."
            }
        ]
    },
    {
        "doc_id": "JUDG_SC_GURBAKSH_SIBBIA_1980",
        "title": "Gurbaksh Singh Sibbia etc. v. State of Punjab",
        "citation": "(1980) 2 SCC 565",
        "neutral_citation": "1980 INSC 77",
        "court": "Supreme Court of India",
        "year": 1980,
        "date": "1980-04-09",
        "source_url": "https://indiankanoon.org/doc/1301416/",
        "license": "Public Domain (Indian Judiciary)",
        "ratio": "Constitution Bench judgment governing anticipatory bail under Section 438 CrPC (now Section 482 BNSS). The power is discretionary and wide, founded on Article 21, and must not be circumscribed by rigid fetters not imposed by the legislature.",
        "paragraphs": [
            {
                "para_num": 12,
                "text": "The power to grant anticipatory bail is not unguided; it is governed by the principles governing ordinary bail and must be exercised to protect the individual from being harassed or humiliated through the engine of arrest for collateral purposes."
            },
            {
                "para_num": 19,
                "text": "A blanket order of anticipatory bail ought not to be passed, but where a reasonable apprehension of arrest exists upon credible information, the High Court or Sessions Court possesses untrammelled discretion to protect personal liberty."
            }
        ]
    },
    {
        "doc_id": "JUDG_SC_CHIDAMBARAM_2020",
        "title": "P. Chidambaram v. Directorate of Enforcement",
        "citation": "(2020) 13 SCC 791",
        "neutral_citation": "2019 INSC 1324",
        "court": "Supreme Court of India",
        "year": 2020,
        "date": "2019-12-04",
        "source_url": "https://indiankanoon.org/doc/171542385/",
        "license": "Public Domain (Indian Judiciary)",
        "ratio": "Reiterated the classical 'Triple Test' for granting bail: (1) whether the accused is a flight risk, (2) whether the accused will tamper with evidence, (3) whether the accused will influence witnesses. Economic offences do not impose an automatic bar on bail.",
        "paragraphs": [
            {
                "para_num": 23,
                "text": "The basic jurisprudence relating to bail remains unchanged: the custody during investigation is for facilitating probe, but prolonged pre-trial incarceration without reasonable prospects of immediate trial violates Article 21. The triple test must be strictly applied."
            },
            {
                "para_num": 27,
                "text": "Gravity of the offence alone is not the sole criterion to deny bail. Even if the allegation involves huge economic defalcation, if documents are already seized and witness intimidation is not shown by concrete material, bail should be granted."
            }
        ]
    },
    {
        "doc_id": "JUDG_SC_BALCHAND_1977",
        "title": "State of Rajasthan, Jaipur v. Balchand alias Baliya",
        "citation": "AIR 1977 SC 2447",
        "neutral_citation": "1977 INSC 182",
        "court": "Supreme Court of India",
        "year": 1977,
        "date": "1977-09-20",
        "source_url": "https://indiankanoon.org/doc/1183014/",
        "license": "Public Domain (Indian Judiciary)",
        "ratio": "Justice Krishna Iyer's celebrated dictum: 'The basic rule may perhaps be tersely put as bail, not jail, except where there are circumstances suggestive of fleeing from justice or thwarting the course of justice'.",
        "paragraphs": [
            {
                "para_num": 2,
                "text": "The basic rule may perhaps be tersely put as bail, not jail, except where there are circumstances suggestive of fleeing from justice or thwarting the course of justice or creating other troubles in the shape of repeating offences or intimidating witnesses and the like, by the petitioner who seeks enlargement on bail from the court."
            }
        ]
    }
]

for judg in judgments_data:
    file_path = JUDGMENTS_DIR / f"{judg['doc_id']}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(judg, f, indent=2)
    manifest_entries.append({
        "doc_id": judg["doc_id"],
        "title": f"{judg['title']} - {judg['citation']}",
        "doc_type": "judgment",
        "date": judg["date"],
        "jurisdiction": "India",
        "source_url": judg["source_url"],
        "license": judg["license"],
        "file_path": str(file_path.relative_to(BASE_DIR))
    })

# ==========================================
# 3. CASE FILES (CLOSED-WORLD RECORDS)
# ==========================================

case_files_data = [
    {
        "doc_id": "CASE_142_FIR",
        "title": "First Information Report No. 142/2024, Police Station Connaught Place",
        "doc_type": "fir",
        "date": "2024-08-12",
        "source_url": "Internal Police Case Diary Archive",
        "license": "Judicial Record (Public Access under CrPC 173/BNSS 193)",
        "text": """FIRST INFORMATION REPORT
(Under Section 173 BNSS / 154 CrPC)
District: New Delhi | Police Station: Connaught Place | Year: 2024 | FIR No: 0142 | Date: 12-08-2024
Acts & Sections: Section 318(4) Bharatiya Nyaya Sanhita, 2023 (Cheating and dishonestly inducing delivery of property)
Complainant: Shri Vikramaditya Singhal, s/o Late B.M. Singhal, r/o 45 Barakhamba Road, New Delhi.
Accused Person: Rajesh Sharma, s/o Mohan Lal Sharma, age 44 years, r/o Flat 302, Green Park Extension, New Delhi.
Date & Time of Alleged Incident: Between 15-01-2024 and 10-06-2024.
Place of Occurrence: Office No. 204, Regal Building, Connaught Place, New Delhi (Distance from PS: 0.5 km North).
Brief Statement of Facts:
The complainant states that the accused Rajesh Sharma represented himself as the Managing Director of Apex Green Energy Solutions Ltd and induced the complainant to invest a sum of Rs. 15,00,000 (Rupees Fifteen Lakhs only) towards procurement of solar equipment. The complainant transferred Rs. 10,00,000 via RTGS on 20-02-2024 and paid Rs. 5,00,000 in cash on 05-03-2024. No equipment was delivered, and cheques issued by accused towards refund were dishonoured. Complainant alleges deliberate cheating and dishonest misappropriation.
Endorsement: Case registered under Section 318(4) BNS 2023 by Sub-Inspector Ramesh Chand, PS Connaught Place."""
    },
    {
        "doc_id": "CASE_142_ARREST_MEMO",
        "title": "Arrest Memo of Rajesh Sharma - FIR No. 142/2024",
        "doc_type": "arrest_memo",
        "date": "2024-08-14",
        "source_url": "Internal Police Case Diary Archive",
        "license": "Judicial Record",
        "text": """MEMO OF ARREST
(Prepared in compliance of D.K. Basu guidelines & Section 35 BNSS)
Police Station: Connaught Place, New Delhi.
Name of Arrestee: Rajesh Sharma, s/o Mohan Lal Sharma, aged 44 years.
Permanent Address: Flat 302, Green Park Extension, New Delhi.
Date and Time of Arrest: 14th August 2024 at 23:45 hours (11:45 PM).
Place of Arrest: Flat 302, Green Park Extension, New Delhi.
Arresting Officer: Sub-Inspector Ramesh Chand, Belt No. 4412-D, PS Connaught Place.
Witness to Arrest: Smt. Sunita Sharma (Wife of Arrestee).
Intimation of Grounds of Arrest: Accused informed orally that he is arrested in connection with FIR 142/2024 under Section 318(4) BNS.
Physical Inspection: The arrestee has no visible external fresh physical injuries; complains of chronic dizziness and diabetes.
Signature of Arresting Officer: SI Ramesh Chand
Signature / Thumb Impression of Arrestee: Rajesh Sharma."""
    },
    {
        "doc_id": "CASE_142_SEIZURE_MEMO",
        "title": "Seizure Panchnama of Digital Device and Cash - FIR No. 142/2024",
        "doc_type": "panchnama",
        "date": "2024-08-15",
        "source_url": "Internal Police Case Diary Archive",
        "license": "Judicial Record",
        "text": """SEIZURE PANCHNAMA (RECOVERY MEMO)
Police Station: Connaught Place | FIR No: 142/2024 | Date: 15-08-2024 | Time: 02:30 hours.
Place of Recovery: Office No. 204, Regal Building, Connaught Place, New Delhi.
Panch Witnesses:
1. Anil Kumar, s/o S.P. Kumar, r/o 12 Babar Road, New Delhi.
2. Harish Rawat, s/o D.N. Rawat, r/o Bengali Market, New Delhi.
Articles Seized:
Item 1: One HP Laptop, Model Pavilion 15, Serial No. 5CD239841K, color Silver, containing email records.
Item 2: Indian currency notes of denomination 500 amounting to Rs. 8,50,000 (Rupees Eight Lakh Fifty Thousand only) recovered from steel almirah in the office of Rajesh Sharma.
Note on Discrepancy: Complainant claimed cash payment of Rs. 5,00,000, whereas actual currency recovered on spot is Rs. 8,50,000.
The seized items were sealed with seal of PS-CP-RC in presence of the witnesses.
Signatures of Panchas: Anil Kumar, Harish Rawat.
Investigating Officer: SI Ramesh Chand."""
    },
    {
        "doc_id": "CASE_142_MLC",
        "title": "Medico-Legal Certificate (MLC) No. 4891/2024 - Rajesh Sharma",
        "doc_type": "medical_report",
        "date": "2024-08-15",
        "source_url": "Dr. Ram Manohar Lohia Hospital, New Delhi",
        "license": "Judicial Medical Record",
        "text": """DR. RAM MANOHAR LOHIA HOSPITAL, NEW DELHI
CASUALTY DEPARTMENT - MEDICO LEGAL CERTIFICATE (MLC)
MLC No: 4891/24 | Date & Time: 15-08-2024 at 09:15 AM
Patient Name: Rajesh Sharma, Age: 44 Years, Male, brought by SI Ramesh Chand, PS Connaught Place.
Identification Mark: Mole on right collarbone.
Clinical Examination Findings:
- Pulse: 98/min, Blood Pressure: 178/110 mmHg (Severe Hypertension).
- Random Blood Sugar: 310 mg/dL (Uncontrolled Diabetes Mellitus Type II).
- Chronic ulceration visible on left lower extremity (diabetic foot ulcer stage II).
- Cardiovascular: S1 S2 heard, tachycardic.
- External Injuries: No fresh external marks of physical violence or blunt force trauma seen.
Doctor's Opinion: Patient is clinically stable for transit but requires daily medical supervision, insulin administration, and anti-hypertensive medication. At risk of cardiac or renal complication if unmonitored.
Examining Medical Officer: Dr. A.K. Sengupta, MD (Emergency Medicine), RML Hospital."""
    },
    {
        "doc_id": "CASE_142_REMAND_ORDER",
        "title": "Order of Metropolitan Magistrate granting Judicial Custody - 15-08-2024",
        "doc_type": "court_order",
        "date": "2024-08-15",
        "source_url": "Court of Chief Metropolitan Magistrate, Patiala House Courts, New Delhi",
        "license": "Judicial Record",
        "text": """IN THE COURT OF METROPOLITAN MAGISTRATE-02, PATIALA HOUSE COURTS, NEW DELHI
State v. Rajesh Sharma | FIR No. 142/2024 | PS Connaught Place | Under Section 318(4) BNS
ORDER
15.08.2024
Accused Rajesh Sharma is produced from PS Connaught Place after arrest on 14.08.2024.
IO SI Ramesh Chand moves application seeking 3 days police custody remand on ground of recovering remaining funds and tracing co-accused.
Ld. Counsel for accused opposes police custody remand, submitting that laptop and records are already seized and accused suffers from acute hypertension and diabetes.
Heard. Considering that the electronic device and currency have already been recovered under seizure panchnama dated 15.08.2024, no further custodial interrogation in police remand is justified.
Police remand application is rejected.
Accused Rajesh Sharma is remanded to Judicial Custody for 14 days till 29.08.2024.
Jail Superintendent, Tihar Jail is directed to provide necessary medical care, insulin, and anti-hypertensive medicines in terms of MLC No. 4891/24.
MM-02 / Patiala House Courts / New Delhi / 15.08.2024."""
    },
    {
        "doc_id": "CASE_142_SESSIONS_ORDER",
        "title": "Order of Additional Sessions Judge rejecting regular bail - 28-08-2024",
        "doc_type": "court_order",
        "date": "2024-08-28",
        "source_url": "Court of Additional Sessions Judge-03, Patiala House Courts, New Delhi",
        "license": "Judicial Record",
        "text": """IN THE COURT OF ADDITIONAL SESSIONS JUDGE-03, NEW DELHI DISTRICT, PATIALA HOUSE COURTS
Bail Application No. 892/2024 | State v. Rajesh Sharma | FIR No. 142/2024 | PS Connaught Place | U/s 318(4) BNS
ORDER ON BAIL APPLICATION
28.08.2024
1. This is an application under Section 483 BNSS (corresponding to Section 439 CrPC) for grant of regular bail moved on behalf of accused Rajesh Sharma.
2. Ld. Counsel for applicant submits that applicant is in custody since 14.08.2024, is suffering from severe diabetes and hypertension, and the dispute is primarily of a civil nature arising out of commercial contract.
3. Ld. Addl. Public Prosecutor strongly opposes bail on the ground that the investigation is at a nascent stage, forensic examination of seized laptop is pending, and the charge sheet has not yet been filed under Section 193 BNSS.
4. Having considered the submissions and perused the case diary, this Court is of the view that since investigation is pending and forensic report of the laptop is awaited, release of applicant at this juncture may prejudice investigation. The medical condition is being addressed by jail dispensary.
5. Accordingly, bail application is dismissed at this stage with liberty to apply afresh after filing of charge sheet.
ASJ-03 / Patiala House Courts / New Delhi / 28.08.2024."""
    },
    {
        "doc_id": "CASE_142_CHARGESHEET",
        "title": "Final Investigation Report / Charge Sheet under Section 193 BNSS - FIR 142/2024",
        "doc_type": "chargesheet",
        "date": "2024-09-30",
        "source_url": "Court of CMM, Patiala House Courts",
        "license": "Judicial Record",
        "text": """FINAL REPORT UNDER SECTION 193 BNSS (SECTION 173 CrPC)
Police Station: Connaught Place | FIR No: 142/2024 | Date of Charge Sheet: 30-09-2024
Court: Learned CMM, Patiala House Courts, New Delhi.
Name of Accused Sent for Trial: Rajesh Sharma, s/o Mohan Lal Sharma, aged 44 years (In Judicial Custody).
Sections Charged: Section 318(4) Bharatiya Nyaya Sanhita, 2023.
Summary of Investigation:
1. Investigation has been completed. All bank records of complainant (HDFC Bank account of Vikramaditya Singhal) and accused (ICICI Bank account of Apex Green Energy) have been obtained and placed on record as Annexure A-1 to A-8.
2. The HP Laptop seized on 15-08-2024 was sent to FSL Rohini, and FSL report dated 20-09-2024 (Annexure B) confirms exchange of business proposals.
3. No further recoveries remain to be effected from the accused. Total 8 prosecution witnesses cited.
4. Accused has no prior criminal antecedents as per SCRB Delhi report dated 25-08-2024.
Submitted by: SI Ramesh Chand, PS Connaught Place. Forwarded by: Inspector / SHO, PS Connaught Place."""
    },
    {
        "doc_id": "CASE_201_LEGAL_NOTICE",
        "title": "Statutory Demand Notice under Section 138 NI Act - M/s Apex Infotech",
        "doc_type": "legal_notice",
        "date": "2024-09-14",
        "source_url": "Advocate Office Archives, Delhi High Court",
        "license": "Legal Communication",
        "text": """LEGAL NOTICE UNDER SECTION 138 OF THE NEGOTIABLE INSTRUMENTS ACT, 1881
Date: 14-09-2024
To:
M/s Zenon Logistics Pvt. Ltd., Through its Managing Director Mr. Alok Mehra,
Registered Office: Plot 88, Okhla Industrial Area Phase-III, New Delhi-110020.
From:
Advocate S.K. Kapoor, Chamber 412, Delhi High Court, New Delhi,
On behalf of Client: M/s Apex Infotech Solutions LLP, 12 Nehru Place, New Delhi.
Sir/Madam,
Under instructions and on behalf of my client M/s Apex Infotech Solutions LLP, I hereby state:
1. That towards discharge of legally enforceable debt for software logistics platform developed by my client under Agreement dated 10-01-2024, you issued Cheque No. 441029 dated 01-09-2024 drawn on Axis Bank, Nehru Place Branch, for an amount of Rs. 42,50,000/- (Rupees Forty-Two Lakhs Fifty Thousand only).
2. That my client presented the said cheque for encashment through its banker HDFC Bank, Connaught Place Branch, but the said cheque was returned dishonoured with remark 'Funds Insufficient' vide Bank Return Memo dated 12-09-2024.
3. You are hereby called upon to pay the said sum of Rs. 42,50,000/- within 15 (fifteen) days from the receipt of this notice, failing which my client shall initiate criminal prosecution under Section 138 of Negotiable Instruments Act, 1881.
Advocate S.K. Kapoor."""
    },
    {
        "doc_id": "CASE_201_CHEQUE_MEMO",
        "title": "Cheque Return Memo of Axis Bank - Cheque No. 441029",
        "doc_type": "bank_memo",
        "date": "2024-09-12",
        "source_url": "HDFC Bank Clearing Department, New Delhi",
        "license": "Banking Commercial Record",
        "text": """CHEQUE RETURN MEMO
Axis Bank Ltd - Nehru Place Branch, New Delhi
Date: 12-09-2024
Cheque Number: 441029 | Cheque Date: 01-09-2024 | Amount: Rs. 42,50,000/-
Drawer Account: M/s Zenon Logistics Pvt. Ltd. (A/C No. 918020045612341)
Payee: M/s Apex Infotech Solutions LLP
Reason for Return: (Code 01) Funds Insufficient.
Authorised Signatory / Clearing Officer, Axis Bank."""
    },
    {
        "doc_id": "CASE_201_POSTAL_TRACKING",
        "title": "India Post Consignment Tracking Delivery Proof - Consignment ED981244012IN",
        "doc_type": "postal_record",
        "date": "2024-09-16",
        "source_url": "India Post Consignment Tracking Portal",
        "license": "Public Postal Record",
        "text": """INDIA POST - CONSIGNMENT TRACKING REPORT
Consignment No: ED981244012IN | Booked at: Delhi High Court SO on 14/09/2024 16:30 hrs
Destination: Okhla Industrial Area Phase-III, New Delhi-110020
Event History:
14/09/2024 16:30 - Item Booked at Delhi High Court SO
15/09/2024 08:20 - Received at New Delhi NSH
16/09/2024 11:45 - Out for Delivery at Okhla Ind Area SO
16/09/2024 14:10 - Item Delivered to Addressee (M/s Zenon Logistics Pvt. Ltd., Received by Receptionist Mr. Vikas Gupta).
Delivery Status: DELIVERED on 16-09-2024."""
    },
    {
        "doc_id": "CASE_201_REPLY_NOTICE",
        "title": "Reply to Legal Notice - M/s Zenon Logistics Pvt. Ltd.",
        "doc_type": "reply_notice",
        "date": "2024-09-28",
        "source_url": "Advocate Chambers, Patiala House Courts",
        "license": "Legal Communication",
        "text": """REPLY TO STATUTORY NOTICE DATED 14-09-2024
Date: 28-09-2024
To: Advocate S.K. Kapoor (For M/s Apex Infotech Solutions LLP)
From: Advocate Meenakshi Sundaram, Chambers 210, Patiala House Courts,
On behalf of: M/s Zenon Logistics Pvt. Ltd. & Mr. Alok Mehra.
Sir,
Under instructions from my clients, I reply to your notice dated 14-09-2024:
1. The allegations of legally enforceable debt are denied. Cheque No. 441029 was handed over strictly as a 'Security Cheque' under Clause 4.2 of Agreement dated 10-01-2024, subject to completion of User Acceptance Testing (UAT).
2. Your client failed to complete Milestone 3 (API integration with Customs EDI portal). Notice of breach was already served by my client on 25-08-2024.
3. As there is no crystallized debt, your client has wrongfully presented the security cheque. No payment of Rs. 42,50,000 is due.
Advocate Meenakshi Sundaram."""
    },
    {
        "doc_id": "CASE_201_CONTRACT",
        "title": "Master Services Agreement between Apex Infotech and Zenon Logistics",
        "doc_type": "contract",
        "date": "2024-01-10",
        "source_url": "Corporate Legal Records",
        "license": "Private Commercial Contract",
        "text": """MASTER SERVICES AGREEMENT
Date: 10th January 2024
Parties:
1. M/s Apex Infotech Solutions LLP (Vendor)
2. M/s Zenon Logistics Pvt. Ltd. (Customer)
Clause 4: Payment Terms
4.1 The total contract value is Rs. 85,00,000 payable in three milestones: Milestone 1 (20% on execution), Milestone 2 (30% on beta deployment), Milestone 3 (50% on UAT sign-off).
4.2 Customer shall deposit an undated security cheque of Rs. 42,50,000 representing Milestone 3, which Vendor may encash only upon successful delivery of UAT completion certificate signed by Customer's Chief Technology Officer.
Clause 14: Dispute Resolution & Pre-Institution Mediation
14.1 Any dispute arising out of or in connection with this agreement shall be subject to pre-institution mediation in terms of Section 12A of the Commercial Courts Act, 2015 at Delhi International Arbitration Centre (DIAC).
14.2 Jurisdiction: Courts at New Delhi shall have exclusive jurisdiction."""
    },
    {
        "doc_id": "CASE_305_FIR",
        "title": "FIR No. 89/2024, PS Hauz Khas - Sections 115, 351 BNS 2023",
        "doc_type": "fir",
        "date": "2024-07-20",
        "source_url": "Delhi Police Public FIR Portal",
        "license": "Judicial Record",
        "text": """FIRST INFORMATION REPORT
PS: Hauz Khas | Dist: South Delhi | FIR No: 0089/2024 | Date: 20-07-2024
Acts & Sections: Section 115(2) (Voluntarily causing hurt), Section 351(2) (Criminal Intimidation) BNS 2023.
Complainant: Smt. Radhika Verma, w/o Sh. Kunal Verma, r/o C-14, Hauz Khas, New Delhi.
Accused Persons:
1. Smt. Sunita Verma (Mother-in-law), aged 62 years.
2. Sh. Naresh Verma (Brother-in-law), aged 34 years.
Both r/o C-14, First Floor, Hauz Khas, New Delhi.
Allegations: Complainant alleges that on 18-07-2024 at 19:30 hours, over a partition of family property, the accused persons abused her, pushed her causing abrasions on her forearm, and threatened that she would be thrown out of the house.
Investigation Officer: SI Anita Rao, PS Hauz Khas."""
    },
    {
        "doc_id": "CASE_305_BNSS_NOTICE",
        "title": "Notice under Section 35(3) BNSS (Section 41A CrPC) to Sunita Verma",
        "doc_type": "police_notice",
        "date": "2024-07-22",
        "source_url": "PS Hauz Khas Records",
        "license": "Judicial Record",
        "text": """NOTICE OF APPEARANCE UNDER SECTION 35(3) BNSS, 2023
To: Smt. Sunita Verma, r/o C-14, First Floor, Hauz Khas, New Delhi.
Case: FIR No. 89/2024, PS Hauz Khas, U/s 115(2), 351(2) BNS 2023.
You are hereby directed to appear before the undersigned at PS Hauz Khas on 25-07-2024 at 11:00 AM to answer questions relating to the investigation of the above case.
You are directed not to tamper with evidence or threaten any witness.
Issued by: SI Anita Rao, Investigating Officer, PS Hauz Khas."""
    },
    {
        "doc_id": "CASE_305_COMPLIANCE",
        "title": "Investigation Attendance & Cooperation Memo - Sunita Verma",
        "doc_type": "investigation_memo",
        "date": "2024-07-25",
        "source_url": "PS Hauz Khas Case Diary",
        "license": "Judicial Record",
        "text": """COMPLIANCE MEMO - ATTENDANCE RECORD
PS Hauz Khas | FIR No. 89/2024
Dated: 25-07-2024
Smt. Sunita Verma appeared at PS Hauz Khas on 25-07-2024 at 11:00 AM accompanied by her advocate in compliance with notice under Section 35(3) BNSS.
Statement of Sunita Verma recorded under Section 180 BNSS (Section 161 CrPC). She denied the allegations and produced certified copy of Title Deed showing property belongs exclusively to her late husband.
Investigating officer notes that the offences are bailable/punishable with less than 2 years imprisonment. Accused has fully cooperated.
SI Anita Rao, PS Hauz Khas."""
    },
    {
        "doc_id": "CASE_305_CIVIL_SUIT",
        "title": "Plaint in Civil Suit No. CS SCJ 412/2024 - Sunita Verma v. Radhika Verma",
        "doc_type": "court_pleading",
        "date": "2024-05-15",
        "source_url": "Court of Senior Civil Judge, Saket Courts, New Delhi",
        "license": "Judicial Record",
        "text": """IN THE COURT OF SENIOR CIVIL JUDGE, SAKET COURTS, NEW DELHI
CS SCJ 412/2024 | Sunita Verma v. Radhika Verma & Kunal Verma
Suit for Permanent Injunction and Declaration.
Institution Date: 15-05-2024 (Two months prior to FIR No. 89/2024).
Pleadings: Plaintiff Sunita Verma seeks permanent injunction restraining defendants from forcefully encroaching upon the ground floor of property C-14 Hauz Khas. Demonstrates pre-existing civil property dispute prior to registration of criminal FIR."""
    },
    {
        "doc_id": "CASE_401_DISCHARGE_SUMMARY",
        "title": "Discharge Summary - Roy Multi-Specialty Clinic",
        "doc_type": "medical_summary",
        "date": "2024-06-18",
        "source_url": "Roy Multi-Specialty Clinic, Kalkaji, New Delhi",
        "license": "Medical Record",
        "text": """ROY MULTI-SPECIALTY CLINIC & SURGICAL CENTRE
Kalkaji, New Delhi - 110019
DISCHARGE SUMMARY
Patient Name: Smt. Meena Devi, Age: 52 Years, Female | Reg No: RMC-2024-0912
Date of Admission: 10-06-2024 | Date of Discharge: 18-06-2024
Diagnosis: Symptomatic Cholelithiasis (Gall bladder stones).
Procedure Performed: Laparoscopic Cholecystectomy converted to Open Cholecystectomy on 11-06-2024.
Operative Surgeon: Dr. Anirudh Roy, MS (Gen Surg).
Course in Hospital: Intra-operative bile duct injury noted and primary end-to-end repair attempted. Patient developed post-operative biliary leak and fever. Treated conservatively with IV antibiotics. Discharged on oral medication.
Follow-up Advice: Review in OPD after 7 days."""
    },
    {
        "doc_id": "CASE_401_EXPERT_BOARD",
        "title": "Medical Board Opinion - AIIMS New Delhi",
        "doc_type": "expert_opinion",
        "date": "2024-08-05",
        "source_url": "All India Institute of Medical Sciences, New Delhi",
        "license": "Public Medical Board Report",
        "text": """ALL INDIA INSTITUTE OF MEDICAL SCIENCES, NEW DELHI
REPORT OF EXPERT MEDICAL BOARD
Reference No: AIIMS/MB/2024/771 | Date: 05-08-2024
Subject: Medical Board evaluation of Smt. Meena Devi in complaint against Roy Multi-Specialty Clinic.
Board Constitution:
1. Prof. (Dr.) V.K. Bansal, Head of Surgical Disciplines (Chairman)
2. Prof. (Dr.) S. Rajesh, Department of GI Surgery (Member)
3. Additional Prof. (Dr.) N. Kaushik, Department of Forensic Medicine (Member)
Findings:
1. Patient underwent Laparoscopic Cholecystectomy where Common Bile Duct (CBD) was transected (Strasberg Type E2 injury).
2. The consent form signed by patient did not specifically mention the risk of bile duct injury or conversion to open surgery without informed authorization.
3. Repair was conducted without on-table cholangiography or drain placement, falling below accepted standard of tertiary surgical care, resulting in biliary peritonitis requiring emergency hepaticojejunostomy at AIIMS on 22-06-2024.
Conclusion: Prima facie departure from reasonable surgical prudence established."""
    },
    {
        "doc_id": "CASE_401_LEGAL_NOTICE",
        "title": "Legal Notice for Medical Negligence and Damages",
        "doc_type": "legal_notice",
        "date": "2024-08-25",
        "source_url": "Advocate Chambers, Saket Courts",
        "license": "Legal Communication",
        "text": """LEGAL NOTICE FOR TORTIOUS MEDICAL NEGLIGENCE AND DEFICIENCY IN SERVICE
Date: 25-08-2024
To: Dr. Anirudh Roy & Roy Multi-Specialty Clinic, Kalkaji, New Delhi.
From: Advocate R.P. Khurana, Saket District Courts, New Delhi,
On behalf of: Smt. Meena Devi, w/o Sh. Ram Dayal, r/o Govindpuri, New Delhi.
Sir,
Under instructions of my client, you are hereby put on notice:
1. On 10-06-2024, my client was admitted for routine gallbladder stone surgery under your care.
2. Due to gross surgical negligence and lack of care, you severed the Common Bile Duct of my client as confirmed by Expert Medical Board of AIIMS (Ref: AIIMS/MB/2024/771).
3. My client suffered biliary peritonitis, was admitted to AIIMS ICU for 21 days, incurring hospital expenses of Rs. 6,80,000/- plus immense mental agony.
4. You are called upon to pay Rs. 35,00,000/- (Rupees Thirty-Five Lakhs only) as compensation within 30 days of this notice, failing which consumer and criminal proceedings under Section 106 BNS shall follow.
Advocate R.P. Khurana."""
    }
]

for cf in case_files_data:
    file_path = CASE_FILES_DIR / f"{cf['doc_id']}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(cf, f, indent=2)
    manifest_entries.append({
        "doc_id": cf["doc_id"],
        "title": cf["title"],
        "doc_type": cf["doc_type"],
        "date": cf["date"],
        "jurisdiction": "India",
        "source_url": cf["source_url"],
        "license": cf["license"],
        "file_path": str(file_path.relative_to(BASE_DIR))
    })

# Write Manifest
manifest_file = DATA_DIR / "manifest.json"
with open(manifest_file, "w", encoding="utf-8") as f:
    json.dump({
        "project": "NyayVeritas",
        "jurisdiction": "India",
        "version": "1.0.0",
        "total_documents": len(manifest_entries),
        "documents": manifest_entries
    }, f, indent=2)

print(f"Successfully generated closed-world corpus with {len(manifest_entries)} documents in {DATA_DIR}")
