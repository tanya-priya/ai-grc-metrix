"""
AI-GRC Metrix — Autonomous GRC Audit, Risk Assessment & Mapping Dashboard
Pure Python / Streamlit implementation.  No raw HTML, CSS, JS, or unsafe markdown.
NIST SP 800-30 risk scoring with 5-framework analysis and bilingual UI.
"""

import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# 1.  LOCALIZATION DICTIONARY
# ─────────────────────────────────────────────────────────────────────────────
LOCALIZATION = {
    "en": {
        # Page chrome
        "page_title": "AI-GRC Metrix | Autonomous GRC Audit Dashboard",
        "app_title": "AI-GRC Metrix",
        "app_subtitle": "Autonomous GRC Audit · Risk Assessment · Regulatory Mapping",
        "lang_label": "Language",
        # Sidebar
        "sidebar_header": "Audit Configuration",
        "sidebar_profile_header": "Target Company Profile",
        "sidebar_profile_help": (
            "Paste or edit the company's security and data-privacy profile below. "
            "The engine will parse and map vulnerabilities automatically."
        ),
        "sidebar_run_button": "Run Audit",
        # Scorecard
        "scorecard_header": "Executive Scorecard",
        "score_health": "Overall Compliance Health Score",
        "score_posture": "Corporate Risk Posture",
        "score_findings": "Total Findings",
        "score_critical": "Critical Findings",
        "posture_critical": "CRITICAL",
        "posture_high": "HIGH",
        "posture_moderate": "MODERATE",
        "posture_low": "LOW",
        # Findings table
        "findings_header": "Detailed Audit Findings — NIST SP 800-30 Risk Assessment",
        "col_id": "ID",
        "col_framework": "Framework",
        "col_finding": "Finding",
        "col_article": "Violated Clause / Control",
        "col_likelihood": "Likelihood (1–5)",
        "col_impact": "Impact (1–5)",
        "col_risk_score": "Risk Score",
        "col_severity": "Severity",
        "col_recommendation": "Recommendation",
        # Framework summary
        "framework_header": "Framework Exposure Summary",
        "fw_col_framework": "Framework",
        "fw_col_findings": "Total Findings",
        "fw_col_critical": "Critical",
        "fw_col_high": "High",
        "fw_col_medium": "Medium",
        "fw_col_max_risk": "Max Risk Score",
        # Severity legend
        "legend_header": "NIST SP 800-30 Severity Scale",
        "legend_medium": "MEDIUM: Risk Score 1–8",
        "legend_high": "HIGH: Risk Score 9–16",
        "legend_critical": "CRITICAL: Risk Score 17–25",
        "legend_formula": "Formula: Risk Score = Likelihood × Impact",
        # Findings (audit content)
        "findings": [
            {
                "framework": "GDPR",
                "finding": (
                    "Pre-checked blanket consent box used during mobile onboarding covers "
                    "terms of service, data processing, AND targeted advertising tracking "
                    "simultaneously — a direct violation of the granularity and freely-given "
                    "consent requirements."
                ),
                "article": "Art. 7 & Recital 32 — Conditions for Consent",
                "likelihood": 5,
                "impact": 5,
                "recommendation": (
                    "Replace with separate, explicit opt-in checkboxes for each distinct "
                    "processing purpose.  Audit and purge all consent records obtained "
                    "via the pre-checked mechanism."
                ),
            },
            {
                "framework": "GDPR",
                "finding": (
                    "EU customer transaction data is dynamically mirrored and analytically "
                    "processed in a Mumbai data warehouse.  No Standard Contractual Clauses "
                    "(SCCs) or equivalent transfer mechanism are in place for this vector."
                ),
                "article": "Art. 46 — Transfers subject to appropriate safeguards",
                "likelihood": 5,
                "impact": 5,
                "recommendation": (
                    "Immediately execute EU SCCs (Module 2 or 4 as applicable) with the "
                    "Mumbai entity.  Conduct a Transfer Impact Assessment (TIA) and document "
                    "supplementary measures.  Consider data residency options as a long-term control."
                ),
            },
            {
                "framework": "DPDP Act",
                "finding": (
                    "Pre-checked consent employed during onboarding fails the DPDP Act's "
                    "requirement for free, specific, informed, and unambiguous consent from "
                    "data principals.  The bundling of unrelated purposes in a single checkbox "
                    "is non-compliant."
                ),
                "article": "Section 6 — Notice & Consent",
                "likelihood": 5,
                "impact": 4,
                "recommendation": (
                    "Re-design the onboarding consent flow to present a clear, itemised "
                    "notice per Section 5 before obtaining per-purpose consent.  Appoint a "
                    "Data Protection Officer (DPO) to oversee remediation."
                ),
            },
            {
                "framework": "DPDP Act",
                "finding": (
                    "Cross-border personal data transfer from Frankfurt to Mumbai without a "
                    "documented adequacy notification or government-approved transfer "
                    "mechanism may constitute unlawful processing under the Act."
                ),
                "article": "Section 16 — Transfer of Personal Data outside India",
                "likelihood": 4,
                "impact": 4,
                "recommendation": (
                    "Monitor the Central Government's whitelist of approved jurisdictions.  "
                    "Implement contractual safeguards and conduct a Data Protection Impact "
                    "Assessment (DPIA) covering the Frankfurt-to-Mumbai data flow."
                ),
            },
            {
                "framework": "SOC 2",
                "finding": (
                    "MFA is optional for marketing, administrative, and vendor-relationship "
                    "directory accounts.  These accounts can access shared SaaS tools and "
                    "internal systems, representing a significant credential-compromise risk."
                ),
                "article": "CC6.1 — Logical & Physical Access Controls",
                "likelihood": 4,
                "impact": 4,
                "recommendation": (
                    "Enforce MFA universally across all user tiers via directory-level policy "
                    "(e.g., Conditional Access in Azure AD / Okta).  Log and alert on any "
                    "MFA bypass events."
                ),
            },
            {
                "framework": "SOC 2",
                "finding": (
                    "Vendor cybersecurity assessments are performed once at onboarding using a "
                    "static questionnaire.  No periodic reassessment cadence is mandated, "
                    "leaving supply-chain risk continuously unmonitored."
                ),
                "article": "CC9.2 — Risk Management — Vendor & Business Partner Risk",
                "likelihood": 3,
                "impact": 4,
                "recommendation": (
                    "Implement an annual third-party risk reassessment programme with tiered "
                    "review frequencies based on criticality.  Automate evidence collection "
                    "via a GRC platform integration."
                ),
            },
            {
                "framework": "ISO 27001",
                "finding": (
                    "Production transactional databases perform full backups only once per week "
                    "to a single localised cloud storage tier with no geographic redundancy or "
                    "automated cross-region failover — violating availability and resilience controls."
                ),
                "article": "A.8.13 — Information Backup / A.17.1 — IT Continuity",
                "likelihood": 3,
                "impact": 5,
                "recommendation": (
                    "Move to daily incremental + weekly full backup schedules.  Replicate "
                    "backup sets to a geographically separate region.  Test restoration "
                    "procedures quarterly and document RTO/RPO targets in a formal BCP."
                ),
            },
            {
                "framework": "ISO 27001",
                "finding": (
                    "Vendor risk management relies on a static spreadsheet questionnaire with no "
                    "lifecycle management.  This is incompatible with an ISMS requiring documented, "
                    "repeatable supplier security review processes."
                ),
                "article": "A.5.19 / A.5.20 — Information Security in Supplier Relationships",
                "likelihood": 3,
                "impact": 3,
                "recommendation": (
                    "Formalise a Supplier Security Policy and integrate vendor assessments into "
                    "the ISMS document control system.  Define mandatory contractual security "
                    "clauses and audit rights for critical suppliers."
                ),
            },
            {
                "framework": "DORA",
                "finding": (
                    "A single-region backup strategy with no automated failover for production "
                    "transactional databases fails DORA's ICT continuity and recovery planning "
                    "requirements for financial entities servicing EU retail banking clients."
                ),
                "article": "Art. 11 — ICT Business Continuity Management",
                "likelihood": 4,
                "impact": 5,
                "recommendation": (
                    "Design a multi-region active-passive or active-active failover architecture. "
                    "Define and test RTO < 4 hours and RPO < 1 hour for critical payment systems. "
                    "Document this in the ICT continuity plan required by DORA."
                ),
            },
            {
                "framework": "DORA",
                "finding": (
                    "Third-party ICT provider (AWS Frankfurt) and analytics vendor (Mumbai warehouse) "
                    "are not subject to ongoing risk assessments as required for critical ICT "
                    "third-party service providers under DORA."
                ),
                "article": "Art. 28 — General Principles on ICT Third-Party Risk",
                "likelihood": 3,
                "impact": 4,
                "recommendation": (
                    "Classify ICT providers by criticality per DORA Art. 28(2).  For critical "
                    "providers, establish contractual audit rights, maintain a full ICT provider "
                    "register, and report concentration risk to the competent authority."
                ),
            },
        ],
    },
    "fr": {
        # Page chrome
        "page_title": "AI-GRC Metrix | Tableau de bord d'audit GRC autonome",
        "app_title": "AI-GRC Metrix",
        "app_subtitle": "Audit GRC autonome · Évaluation des risques · Cartographie réglementaire",
        "lang_label": "Langue",
        # Sidebar
        "sidebar_header": "Configuration de l'audit",
        "sidebar_profile_header": "Profil de l'entreprise cible",
        "sidebar_profile_help": (
            "Collez ou modifiez ci-dessous le profil de sécurité et de confidentialité "
            "des données de l'entreprise. Le moteur analysera et cartographiera "
            "automatiquement les vulnérabilités."
        ),
        "sidebar_run_button": "Lancer l'audit",
        # Scorecard
        "scorecard_header": "Tableau de bord exécutif",
        "score_health": "Score de santé de conformité globale",
        "score_posture": "Posture de risque de l'entreprise",
        "score_findings": "Nombre total de constats",
        "score_critical": "Constats critiques",
        "posture_critical": "CRITIQUE",
        "posture_high": "ÉLEVÉ",
        "posture_moderate": "MODÉRÉ",
        "posture_low": "FAIBLE",
        # Findings table
        "findings_header": "Constats d'audit détaillés — Évaluation des risques NIST SP 800-30",
        "col_id": "ID",
        "col_framework": "Cadre",
        "col_finding": "Constat",
        "col_article": "Clause / Contrôle violé",
        "col_likelihood": "Probabilité (1–5)",
        "col_impact": "Impact (1–5)",
        "col_risk_score": "Score de risque",
        "col_severity": "Sévérité",
        "col_recommendation": "Recommandation",
        # Framework summary
        "framework_header": "Résumé d'exposition par cadre",
        "fw_col_framework": "Cadre réglementaire",
        "fw_col_findings": "Total des constats",
        "fw_col_critical": "Critiques",
        "fw_col_high": "Élevés",
        "fw_col_medium": "Moyens",
        "fw_col_max_risk": "Score de risque max.",
        # Severity legend
        "legend_header": "Échelle de sévérité NIST SP 800-30",
        "legend_medium": "MOYEN : Score de risque 1–8",
        "legend_high": "ÉLEVÉ : Score de risque 9–16",
        "legend_critical": "CRITIQUE : Score de risque 17–25",
        "legend_formula": "Formule : Score de risque = Probabilité × Impact",
        # Findings (audit content — translated)
        "findings": [
            {
                "framework": "RGPD",
                "finding": (
                    "Une case à cocher pré-cochée et globale est utilisée lors de l'intégration "
                    "mobile, couvrant simultanément les conditions d'utilisation, le traitement "
                    "des données et le suivi publicitaire ciblé — en violation directe des "
                    "exigences de granularité et de consentement librement donné."
                ),
                "article": "Art. 7 & considérant 32 — Conditions applicables au consentement",
                "likelihood": 5,
                "impact": 5,
                "recommendation": (
                    "Remplacer par des cases à cocher opt-in distinctes pour chaque finalité "
                    "de traitement. Auditer et purger tous les enregistrements de consentement "
                    "obtenus via le mécanisme pré-coché."
                ),
            },
            {
                "framework": "RGPD",
                "finding": (
                    "Les données de transactions clients UE sont dynamiquement répliquées et "
                    "traitées dans un entrepôt de données à Mumbai.  Aucune Clause Contractuelle "
                    "Type (CCT) ni mécanisme de transfert équivalent n'est en place pour ce vecteur."
                ),
                "article": "Art. 46 — Transferts moyennant des garanties appropriées",
                "likelihood": 5,
                "impact": 5,
                "recommendation": (
                    "Exécuter immédiatement des CCT UE (Module 2 ou 4 selon le cas) avec "
                    "l'entité de Mumbai.  Réaliser une Analyse d'Impact du Transfert (AIT) "
                    "et documenter les mesures supplémentaires."
                ),
            },
            {
                "framework": "Loi DPDP",
                "finding": (
                    "Le consentement pré-coché lors de l'intégration ne satisfait pas à l'exigence "
                    "de consentement libre, spécifique, éclairé et non ambigu imposée par la loi "
                    "DPDP.  Le regroupement de finalités non liées en une seule case est non conforme."
                ),
                "article": "Article 6 — Avis et consentement",
                "likelihood": 5,
                "impact": 4,
                "recommendation": (
                    "Repenser le flux de consentement à l'intégration pour présenter un avis "
                    "détaillé par finalité conformément à l'article 5 avant d'obtenir le "
                    "consentement.  Nommer un Délégué à la Protection des Données (DPD)."
                ),
            },
            {
                "framework": "Loi DPDP",
                "finding": (
                    "Le transfert de données personnelles de Francfort à Mumbai sans notification "
                    "d'adéquation documentée ni mécanisme de transfert approuvé par le gouvernement "
                    "peut constituer un traitement illicite au titre de la loi."
                ),
                "article": "Article 16 — Transfert de données personnelles hors d'Inde",
                "likelihood": 4,
                "impact": 4,
                "recommendation": (
                    "Surveiller la liste blanche des juridictions approuvées par le gouvernement "
                    "central.  Mettre en œuvre des garanties contractuelles et réaliser une "
                    "Analyse d'Impact relative à la Protection des Données (AIPD)."
                ),
            },
            {
                "framework": "SOC 2",
                "finding": (
                    "L'AFM est facultatif pour les comptes marketing, administratifs et de "
                    "relations fournisseurs.  Ces comptes accèdent aux outils SaaS partagés "
                    "et aux systèmes internes, représentant un risque significatif de compromission "
                    "des identifiants."
                ),
                "article": "CC6.1 — Contrôles d'accès logiques et physiques",
                "likelihood": 4,
                "impact": 4,
                "recommendation": (
                    "Imposer l'AFM universellement sur toutes les catégories d'utilisateurs "
                    "via une politique au niveau du répertoire (ex. : Accès conditionnel Azure AD / Okta). "
                    "Journaliser et alerter sur tout contournement de l'AFM."
                ),
            },
            {
                "framework": "SOC 2",
                "finding": (
                    "Les évaluations de cybersécurité des fournisseurs sont effectuées une seule "
                    "fois à l'intégration à l'aide d'un questionnaire statique.  Aucune cadence "
                    "de réévaluation périodique n'est imposée, laissant le risque lié à la chaîne "
                    "d'approvisionnement continuellement non surveillé."
                ),
                "article": "CC9.2 — Gestion des risques fournisseurs et partenaires",
                "likelihood": 3,
                "impact": 4,
                "recommendation": (
                    "Mettre en place un programme annuel de réévaluation des risques tiers "
                    "avec des fréquences de révision échelonnées selon la criticité.  Automatiser "
                    "la collecte de preuves via une intégration à une plateforme GRC."
                ),
            },
            {
                "framework": "ISO 27001",
                "finding": (
                    "Les bases de données transactionnelles de production n'effectuent des "
                    "sauvegardes complètes qu'une fois par semaine vers un stockage cloud "
                    "localisé unique, sans redondance géographique ni basculement automatique "
                    "inter-régions — violant les contrôles de disponibilité et de résilience."
                ),
                "article": "A.8.13 — Sauvegarde des informations / A.17.1 — Continuité informatique",
                "likelihood": 3,
                "impact": 5,
                "recommendation": (
                    "Passer à des sauvegardes incrémentielles quotidiennes et complètes "
                    "hebdomadaires.  Répliquer les sauvegardes dans une région géographiquement "
                    "séparée.  Tester les procédures de restauration trimestriellement et "
                    "documenter les objectifs RTO/RPO dans un PCA formel."
                ),
            },
            {
                "framework": "ISO 27001",
                "finding": (
                    "La gestion des risques fournisseurs repose sur un questionnaire statique "
                    "sans gestion du cycle de vie.  Cela est incompatible avec un SMSI exigeant "
                    "des processus de révision de la sécurité des fournisseurs documentés et "
                    "reproductibles."
                ),
                "article": "A.5.19 / A.5.20 — Sécurité de l'information dans les relations fournisseurs",
                "likelihood": 3,
                "impact": 3,
                "recommendation": (
                    "Formaliser une Politique de Sécurité Fournisseurs et intégrer les évaluations "
                    "dans le système de contrôle documentaire du SMSI.  Définir des clauses "
                    "contractuelles de sécurité obligatoires et des droits d'audit pour les "
                    "fournisseurs critiques."
                ),
            },
            {
                "framework": "DORA",
                "finding": (
                    "Une stratégie de sauvegarde mono-région sans basculement automatique pour "
                    "les bases de données transactionnelles de production ne satisfait pas aux "
                    "exigences DORA en matière de continuité et de plans de reprise des TIC pour "
                    "les entités financières desservant des clients bancaires retail UE."
                ),
                "article": "Art. 11 — Gestion de la continuité des activités liées aux TIC",
                "likelihood": 4,
                "impact": 5,
                "recommendation": (
                    "Concevoir une architecture de basculement multi-régions actif-passif "
                    "ou actif-actif.  Définir et tester RTO < 4 heures et RPO < 1 heure "
                    "pour les systèmes de paiement critiques.  Documenter cela dans le plan "
                    "de continuité TIC requis par DORA."
                ),
            },
            {
                "framework": "DORA",
                "finding": (
                    "Le prestataire TIC tiers (AWS Francfort) et le fournisseur analytique "
                    "(entrepôt Mumbai) ne font pas l'objet d'évaluations de risques continues "
                    "telles qu'exigées pour les prestataires TIC tiers critiques sous DORA."
                ),
                "article": "Art. 28 — Principes généraux sur le risque lié aux tiers TIC",
                "likelihood": 3,
                "impact": 4,
                "recommendation": (
                    "Classer les prestataires TIC par criticité conformément à l'Art. 28(2) de "
                    "DORA.  Pour les prestataires critiques, établir des droits d'audit "
                    "contractuels, maintenir un registre complet des prestataires TIC et "
                    "signaler le risque de concentration à l'autorité compétente."
                ),
            },
        ],
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# 2.  NIST SP 800-30 RISK ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def calculate_risk_score(likelihood: int, impact: int) -> int:
    """Risk Score = Likelihood × Impact  (NIST SP 800-30)."""
    return likelihood * impact


def classify_severity(risk_score: int) -> str:
    """Categorise risk score into MEDIUM / HIGH / CRITICAL per NIST SP 800-30."""
    if risk_score <= 8:
        return "MEDIUM"
    elif risk_score <= 16:
        return "HIGH"
    else:
        return "CRITICAL"


def calculate_health_score(findings: list[dict]) -> float:
    """
    Dynamically compute Overall Compliance Health Score.

    Baseline: 100%.
    Deductions (proportional per finding):
      - CRITICAL : 7 points
      - HIGH     : 4 points
      - MEDIUM   : 1.5 points
    Score is clamped to [0, 100].
    """
    deduction_map = {"CRITICAL": 7.0, "HIGH": 4.0, "MEDIUM": 1.5}
    total_deduction = sum(
        deduction_map.get(classify_severity(f["risk_score"]), 0) for f in findings
    )
    return max(0.0, 100.0 - total_deduction)


def derive_risk_posture(health_score: float, lang_dict: dict) -> str:
    """Map the numeric health score to a descriptive risk posture label."""
    if health_score < 40:
        return lang_dict["posture_critical"]
    elif health_score < 65:
        return lang_dict["posture_high"]
    elif health_score < 80:
        return lang_dict["posture_moderate"]
    else:
        return lang_dict["posture_low"]


def build_findings_dataframe(lang_dict: dict) -> tuple[pd.DataFrame, list[dict]]:
    """
    Process raw findings from the localisation dict, compute risk scores
    and severity, and return both the display DataFrame and enriched records.
    """
    enriched = []
    for idx, f in enumerate(lang_dict["findings"], start=1):
        risk_score = calculate_risk_score(f["likelihood"], f["impact"])
        severity = classify_severity(risk_score)
        enriched.append(
            {
                "id": idx,
                "framework": f["framework"],
                "finding": f["finding"],
                "article": f["article"],
                "likelihood": f["likelihood"],
                "impact": f["impact"],
                "risk_score": risk_score,
                "severity": severity,
                "recommendation": f["recommendation"],
            }
        )

    df = pd.DataFrame(enriched)
    return df, enriched


def build_framework_summary(df: pd.DataFrame, lang_dict: dict) -> pd.DataFrame:
    """Aggregate per-framework exposure statistics."""
    rows = []
    for fw in df["framework"].unique():
        subset = df[df["framework"] == fw]
        rows.append(
            {
                lang_dict["fw_col_framework"]: fw,
                lang_dict["fw_col_findings"]: len(subset),
                lang_dict["fw_col_critical"]: len(subset[subset["severity"] == "CRITICAL"]),
                lang_dict["fw_col_high"]: len(subset[subset["severity"] == "HIGH"]),
                lang_dict["fw_col_medium"]: len(subset[subset["severity"] == "MEDIUM"]),
                lang_dict["fw_col_max_risk"]: int(subset["risk_score"].max()),
            }
        )
    return pd.DataFrame(rows)


# ─────────────────────────────────────────────────────────────────────────────
# 3.  DEFAULT COMPANY PROFILE TEXT
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_COMPANY_PROFILE = """\
# COMPANY SECURITY & DATA ACCURACY PROFILE: Vera Finance
## 1. Governance & Footprint
- **Entity Type:** Financial Technology SaaS platform orchestrating cross-border clearing.
- **Operations Base:** Bengaluru, Karnataka, India.
- **Client Base:** Explicitly services tier-1 retail banking operations inside the European Union (EU).

## 2. Privacy & Data Architecture
- **Consent Collection:** Users accept a pre-checked blanket consent box during mobile onboarding covering terms of service, processing, and targeted advertising tracking.
- **Cross-Border Processing:** European customer transactions are initially ingested via an AWS Frankfurt node, but are dynamically mirrored and processed in an analytical data warehouse located in Mumbai, India. No active Standard Contractual Clauses (SCCs) are configured for this vector.

## 3. Core Infrastructure Control (Access & Failover)
- **Identity & Access Management (IAM):** Multi-Factor Authentication (MFA) is strictly enforced for system root and core engineering teams, but remains completely optional for corporate marketing, administrative, and vendor-relationship directory accounts.
- **Business Continuity & Backups:** Production transactional databases execute full backups once a week to a localized single cloud storage tier with zero geographic distribution or automated cross-region failover.

## 4. Third-Party Exposure
- **Supply Chain Management:** Vendor cybersecurity performance reviews are executed once during initial supplier onboarding using a static internal questionnaire spreadsheet. No periodic reassessments are mandated.\
"""

# ─────────────────────────────────────────────────────────────────────────────
# 4.  SEVERITY COLOUR HELPERS  (native Streamlit — no HTML)
# ─────────────────────────────────────────────────────────────────────────────

SEVERITY_EMOJI = {
    "CRITICAL": "🔴",
    "HIGH": "🟠",
    "MEDIUM": "🟡",
}


def severity_label(severity: str) -> str:
    """Return an emoji-prefixed severity label for display in native tables."""
    return f"{SEVERITY_EMOJI.get(severity, '')} {severity}"


# ─────────────────────────────────────────────────────────────────────────────
# 5.  STREAMLIT APPLICATION
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    st.set_page_config(
        page_title="AI-GRC Metrix",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # ── 5.1  Language toggle (top-right via columns) ──────────────────────────
    header_col, lang_col = st.columns([5, 1])

    with lang_col:
        lang = st.radio(
            label="🌐 Language / Langue",
            options=["EN", "FR"],
            horizontal=True,
            index=0,
            key="language_toggle",
        )

    L = LOCALIZATION["en"] if lang == "EN" else LOCALIZATION["fr"]

    with header_col:
        st.title(f"🛡️  {L['app_title']}")
        st.caption(L["app_subtitle"])

    st.divider()

    # ── 5.2  Sidebar — Company Profile Input ─────────────────────────────────
    with st.sidebar:
        st.header(L["sidebar_header"])
        st.subheader(L["sidebar_profile_header"])
        st.caption(L["sidebar_profile_help"])

        company_profile = st.text_area(
            label=L["sidebar_profile_header"],
            value=DEFAULT_COMPANY_PROFILE,
            height=480,
            label_visibility="collapsed",
        )

        st.divider()
        run_audit = st.button(
            label=f"▶  {L['sidebar_run_button']}",
            type="primary",
            use_container_width=True,
        )

        # Always auto-run on first render; button triggers explicit re-run
        if "audit_run" not in st.session_state:
            st.session_state["audit_run"] = True
        if run_audit:
            st.session_state["audit_run"] = True

    if not st.session_state.get("audit_run"):
        st.info("Configure the company profile in the sidebar, then click **Run Audit**.")
        return

    # ── 5.3  Data computation ─────────────────────────────────────────────────
    df_findings, enriched_findings = build_findings_dataframe(L)
    health_score = calculate_health_score(enriched_findings)
    risk_posture = derive_risk_posture(health_score, L)
    total_findings = len(enriched_findings)
    critical_count = sum(1 for f in enriched_findings if f["severity"] == "CRITICAL")
    high_count = sum(1 for f in enriched_findings if f["severity"] == "HIGH")
    medium_count = sum(1 for f in enriched_findings if f["severity"] == "MEDIUM")

    # ── 5.4  Executive Scorecard ──────────────────────────────────────────────
    st.subheader(f"📊  {L['scorecard_header']}")

    m1, m2, m3, m4 = st.columns(4)

    health_delta_label = (
        f"{'▼' if health_score < 70 else '▲'} {abs(health_score - 100):.1f}pts from baseline"
        if lang == "EN"
        else f"{'▼' if health_score < 70 else '▲'} {abs(health_score - 100):.1f}pts de la base"
    )

    with m1:
        st.metric(
            label=f"🏥  {L['score_health']}",
            value=f"{health_score:.1f}%",
            delta=health_delta_label,
            delta_color="inverse",
        )
    with m2:
        st.metric(
            label=f"⚠️  {L['score_posture']}",
            value=risk_posture,
        )
    with m3:
        st.metric(
            label=f"📋  {L['score_findings']}",
            value=total_findings,
        )
    with m4:
        st.metric(
            label=f"🔴  {L['score_critical']}",
            value=critical_count,
            delta=f"+{high_count} HIGH  +{medium_count} MEDIUM"
            if lang == "EN"
            else f"+{high_count} ÉLEVÉ  +{medium_count} MOYEN",
            delta_color="off",
        )

    st.divider()

    # ── 5.5  NIST Severity Legend ─────────────────────────────────────────────
    with st.expander(f"📏  {L['legend_header']}", expanded=False):
        leg1, leg2, leg3, leg4 = st.columns(4)
        with leg1:
            st.info(f"🟡  {L['legend_medium']}")
        with leg2:
            st.warning(f"🟠  {L['legend_high']}")
        with leg3:
            st.error(f"🔴  {L['legend_critical']}")
        with leg4:
            st.success(f"🔢  {L['legend_formula']}")

    # ── 5.6  Framework Exposure Summary ──────────────────────────────────────
    st.subheader(f"🗺️  {L['framework_header']}")

    df_fw_summary = build_framework_summary(df_findings, L)
    st.dataframe(
        df_fw_summary,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # ── 5.7  Detailed Findings Table ──────────────────────────────────────────
    st.subheader(f"🔍  {L['findings_header']}")

    # Severity filter
    filter_label = "Filter by Severity" if lang == "EN" else "Filtrer par sévérité"
    all_label = "All" if lang == "EN" else "Toutes"
    severity_filter = st.selectbox(
        label=filter_label,
        options=[all_label, "CRITICAL", "HIGH", "MEDIUM"],
        index=0,
    )

    display_df = df_findings.copy()
    if severity_filter != all_label:
        display_df = display_df[display_df["severity"] == severity_filter]

    # Rename columns for display
    col_rename = {
        "id": L["col_id"],
        "framework": L["col_framework"],
        "finding": L["col_finding"],
        "article": L["col_article"],
        "likelihood": L["col_likelihood"],
        "impact": L["col_impact"],
        "risk_score": L["col_risk_score"],
        "severity": L["col_severity"],
        "recommendation": L["col_recommendation"],
    }
    display_df = display_df.rename(columns=col_rename)
    # Prefix severity with emoji
    sev_col = L["col_severity"]
    display_df[sev_col] = display_df[sev_col].apply(severity_label)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            L["col_id"]: st.column_config.NumberColumn(width="small"),
            L["col_framework"]: st.column_config.TextColumn(width="small"),
            L["col_likelihood"]: st.column_config.NumberColumn(width="small"),
            L["col_impact"]: st.column_config.NumberColumn(width="small"),
            L["col_risk_score"]: st.column_config.ProgressColumn(
                label=L["col_risk_score"],
                min_value=0,
                max_value=25,
                format="%d",
            ),
            L["col_severity"]: st.column_config.TextColumn(width="small"),
        },
    )

    st.divider()

    # ── 5.8  Per-Finding Detail Cards ─────────────────────────────────────────
    detail_header = "Finding Detail Cards" if lang == "EN" else "Fiches de détail des constats"
    with st.expander(f"📄  {detail_header}", expanded=False):
        for f in enriched_findings:
            sev = f["severity"]
            emoji = SEVERITY_EMOJI.get(sev, "")
            card_title = f"{emoji} [{f['framework']}] #{f['id']} — {sev}"

            with st.container(border=True):
                st.markdown(f"**{card_title}**")

                c1, c2, c3 = st.columns([1, 1, 1])
                with c1:
                    st.metric(
                        L["col_likelihood"] if lang == "EN" else "Probabilité",
                        f["likelihood"],
                    )
                with c2:
                    st.metric(
                        L["col_impact"] if lang == "EN" else "Impact",
                        f["impact"],
                    )
                with c3:
                    st.metric(
                        L["col_risk_score"],
                        f["risk_score"],
                    )

                st.write(f"**{L['col_article']}:** {f['article']}")
                st.write(f"**{L['col_finding']}:** {f['finding']}")
                st.write(f"**{L['col_recommendation']}:** {f['recommendation']}")

    # ── 5.9  Company Profile Preview ──────────────────────────────────────────
    profile_header = "Audited Company Profile" if lang == "EN" else "Profil d'entreprise audité"
    with st.expander(f"🏢  {profile_header}", expanded=False):
        st.text(company_profile)

    # ── 5.10  Footer ──────────────────────────────────────────────────────────
    st.divider()
    st.caption(
        "AI-GRC Metrix · NIST SP 800-30 Risk Engine · "
        "GDPR · DPDP Act · SOC 2 · ISO 27001 · DORA  |  "
        "For advisory purposes only — not legal or regulatory counsel."
        if lang == "EN"
        else
        "AI-GRC Metrix · Moteur de risque NIST SP 800-30 · "
        "RGPD · Loi DPDP · SOC 2 · ISO 27001 · DORA  |  "
        "À titre consultatif uniquement — ne constitue pas un conseil juridique ou réglementaire."
    )


if __name__ == "__main__":
    main()
