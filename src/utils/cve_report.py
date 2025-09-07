# cve_report_app.py
"""
CVE Intelligence Report Generator (single-file)
- Uses Gemini 2.0 Flash via google-genai
- Hardcode your API key below (local testing only)
- Produces PDF only: concise (2-page aimed) or detailed report
"""

import os
import time
from io import BytesIO
from typing import Dict

import streamlit as st
from fpdf import FPDF

# IMPORTANT: Replace with your Gemini API key (for local testing only).
# Do NOT commit this file with your real key to a public repo.
API_KEY = "API Key"  # <-- REPLACE WITH YOUR KEY

# Model name (as requested)
MODEL_NAME = "gemini-2.0-flash"

# try importing google-genai and create a client
try:
    from google import genai
except Exception as exc:
    genai = None
    _genai_import_exc = exc

# -------------------- Helper utilities --------------------
def init_client(api_key: str):
    if genai is None:
        raise RuntimeError(f"google-genai is not installed: {_genai_import_exc}")
    # create single client explicitly with api_key
    return genai.Client(api_key=api_key)

def get_response_text(resp) -> str:
    """
    Extract textual content from a genai response object defensively.
    """
    if resp is None:
        return ""
    # Some SDKs expose .text
    if hasattr(resp, "text") and resp.text:
        return resp.text
    # Some SDKs provide candidates
    cand = getattr(resp, "candidates", None)
    if cand and len(cand) > 0:
        first = cand[0]
        # candidate content may be in .content or .text
        return getattr(first, "content", None) or getattr(first, "text", None) or str(first)
    # fallback
    return str(resp)

def break_long_words(text: str, max_len: int = 80) -> str:
    """
    Insert soft breaks in very long tokens (URLs or long words) so FPDF's multi_cell can wrap.
    We'll insert zero-width space characters (or spaces) for wrapping.
    """
    if not text:
        return text
    parts = []
    for token in text.split(" "):
        if len(token) <= max_len:
            parts.append(token)
        else:
            # break into chunks and join with a zero-width space (ZWSP) or simple space
            chunks = [token[i:i+max_len] for i in range(0, len(token), max_len)]
            parts.append(" ".join(chunks))
    return " ".join(parts)

def call_model(client, prompt: str) -> str:
    """
    Call the model in a conservative way (only model and contents).
    Do NOT pass unsupported kwargs like temperature to generate_content.
    """
    try:
        resp = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return get_response_text(resp) or ""
    except Exception as e:
        # return an error marker so the PDF shows the issue
        return f"[ERROR calling model: {e}]"

# -------------------- Prompt templates --------------------
# We'll make structured, explicit, citation-demanding prompts.
def build_cve_overview_prompt(cve_id: str, concise: bool) -> str:
    length = "concise (limit to ~150-250 words)" if concise else "detailed (include full fields and explanations)"
    return (
        f"You are a cyber threat intelligence analyst. Produce a structured CVE overview for {cve_id}.\n"
        f"Requirements (must follow):\n"
        f"1) Output fields as a short JSON-like block or bullet list: cve_id, title, official_description, affected_products (list), cvss_v3_vector, cvss_v3_score, severity_label, cwe_id (if any), published_date, last_modified.\n"
        f"2) Provide 1-line citation for each factual field (source title + URL) immediately after the field.\n"
        f"3) If authoritative sources (NVD, MITRE, vendor advisory, CISA) disagree on values, list discrepancies and cite sources.\n"
        f"4) Tone: technical and precise.\n"
        f"Produce the response in {length}."
    )

def build_exploit_search_prompt(cve_id: str, concise: bool) -> str:
    length = "brief technical summaries (each 2-4 lines)" if concise else "detailed technical descriptions, including code snippets or commands where present"
    return (
        f"You are a security researcher searching for public proof-of-concept (PoC) or exploit evidence for {cve_id}.\n"
        f"Search sources such as GitHub (repos/commits/issues), Reddit threads, Twitter posts, and Exploit-DB.\n"
        f"For each finding include: source type (GitHub/Reddit/Twitter/Exploit-DB), title, link, exact technical summary of what the PoC does (step-by-step), prerequisite conditions, observable artifacts, and a 1-line confidence rating.\n"
        f"Include citations (full URLs). Present results as numbered items with explicit technical detail. Use {length}."
    )

def build_mitre_prompt(cve_id: str, concise: bool) -> str:
    return (
        f"Map {cve_id} to MITRE ATT&CK techniques. For each technique include: Technique ID (e.g., T1059), Name, Tactic, a 2-4 sentence rationale tying the CVE's exploitation behaviour to the technique, and a detection idea (log source + signature idea). Provide citations for the mapping."
        + ("\nMake this concise." if concise else "\nMake this comprehensive and technical.")
    )

def build_exploitation_scenarios_prompt(cve_id: str, concise: bool) -> str:
    return (
        f"Write 2 exploitation scenarios for {cve_id} (attacker goals: remote code exec, privilege escalation, or data exfiltration). For each scenario include:\n"
        f"- Title\n- Prerequisites (network access, auth, config)\n- Step-by-step numbered chain of actions the attacker performs (include commands, payloads, file names if known)\n- Expected impact\n- Observable artifacts/IOCs\n- Short containment checklist\nProvide citations for any factual claims or example commands. { 'Keep short bullets' if concise else 'Provide rich technical detail.' }"
    )

def build_mitigation_prompt(cve_id: str, concise: bool) -> str:
    return (
        f"Produce a prioritized mitigation and detection plan for {cve_id}. Include Immediate/Short-term/Long-term actions. For each action include: Why it helps, How to implement (commands/config snippets), Validation steps (how to confirm fix), and Rollback notes.\n"
        f"Also include top 6 detection queries (SIEM pseudocode or Sigma-like rules) with log sources.\n"
        f"Require citations for recommended commands/configs."
        + ("\nKeep concise." if concise else "\nProvide thorough implementation details.")
    )

def build_references_prompt(cve_id: str) -> str:
    return f"List all references (title + full URL) you used to support claims about {cve_id}. Number them and include source type (NVD/MITRE/GitHub/Blog/Exploit-DB/etc.)."

# -------------------- PDF rendering helper --------------------
class PDFReport:
    def __init__(self, title: str, author: str = "CVE Intelligence Generator"):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.title = title
        self.author = author
        self._init_styles()

    def _init_styles(self):
        # call once to set fonts (FPDF uses font files available by default)
        pass

    def add_title_page(self, cve_id: str, report_type: str):
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 18)
        self.pdf.cell(0, 10, self.title, ln=True, align="C")
        self.pdf.ln(4)
        self.pdf.set_font("Arial", "", 12)
        self.pdf.cell(0, 8, f"CVE: {cve_id}", ln=True, align="C")
        self.pdf.ln(8)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(0, 6, f"Report type: {report_type}", ln=True, align="C")
        self.pdf.ln(6)
        self.pdf.cell(0, 6, f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
        self.pdf.ln(10)

    def add_section(self, heading: str, text: str):
        epw = self.pdf.w - self.pdf.l_margin - self.pdf.r_margin
        # Heading
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.multi_cell(epw, 7, heading)
        self.pdf.ln(1)
        # Body
        self.pdf.set_font("Arial", "", 10)
        # Use multi_cell for wrapped text. Ensure long tokens have spaces.
        safe_text = break_long_words(text, max_len=90)
        for para in safe_text.split("\n\n"):
            # further split paragraphs into lines if extremely long
            self.pdf.multi_cell(epw, 5, para)
            self.pdf.ln(1)

    def output_bytes(self) -> bytes:
        # FPDF.output(dest="S") returns a bytearray in recent versions
        return bytes(self.pdf.output(dest="S"))

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="CVE Intelligence PDF Generator", layout="wide")
st.title("CVE Intelligence PDF Generator — Gemini 2.0 Flash")

st.markdown(
    """
**Notes**
- The API key is hardcoded in this script (top `API_KEY` variable). Replace it before running.
- The app calls Gemini 2.0 Flash. Be mindful of API usage/costs.
"""
)

# Inputs
cve_input = st.text_input("CVE ID (e.g. CVE-2025-32433)", value="")
report_mode = st.selectbox("Report length", ["Concise (2-page aimed)", "Detailed (full)"])
generate_btn = st.button("Generate PDF Report")

# Validate client initialization
client = None
client_error = None
if API_KEY.startswith("ya29.") or (API_KEY and not API_KEY.startswith("ya29.")):
    # attempt to init; if API_KEY not replaced, still attempt but show warning later
    try:
        client = init_client(API_KEY)
    except Exception as e:
        client_error = str(e)
else:
    client_error = "Please set your API_KEY at the top of the script."

if client_error:
    st.error(f"GenAI client initialization error: {client_error}")
    st.stop()

if generate_btn:
    if not cve_input.strip():
        st.warning("Enter a CVE ID first.")
    else:
        concise = report_mode.startswith("Concise")
        # show spinner while generating
        with st.spinner("Calling Gemini and preparing report (may take a minute)..."):
            # collect outputs
            outputs: Dict[str, str] = {}

            try:
                # 1) CVE overview (authoritative)
                prompt = build_cve_overview_prompt(cve_input.strip(), concise)
                outputs["Overview"] = call_model(client, prompt)

                # 2) Exploits / PoC (GitHub / Reddit / Twitter / Exploit-DB)
                prompt = build_exploit_search_prompt(cve_input.strip(), concise)
                outputs["PoCs"] = call_model(client, prompt)

                # 3) MITRE mapping
                prompt = build_mitre_prompt(cve_input.strip(), concise)
                outputs["MITRE Mapping"] = call_model(client, prompt)

                # 4) Exploitation scenarios
                prompt = build_exploitation_scenarios_prompt(cve_input.strip(), concise)
                outputs["Exploitation Scenarios"] = call_model(client, prompt)

                # 5) Mitigation & Detection guidance
                prompt = build_mitigation_prompt(cve_input.strip(), concise)
                outputs["Mitigation & Detection"] = call_model(client, prompt)

                # 6) References list
                prompt = build_references_prompt(cve_input.strip())
                outputs["References"] = call_model(client, prompt)
            except Exception as e:
                st.error(f"Fatal error calling model: {e}")
                st.stop()

            # Build PDF
            report_title = f"CVE Intelligence Report"
            pdf = PDFReport(title=report_title)
            pdf.add_title_page(cve_input.strip(), report_mode)

            # Which sections for concise vs detailed
            if concise:
                # Aim for concise: include overview, one-line PoC summary, short mitigation & references.
                pdf.add_section("1) CVE Overview", outputs.get("Overview", "No data"))
                pdf.add_section("2) Exploitability / PoC (summary)", outputs.get("PoCs", "No data"))
                pdf.add_section("3) Mitigation & Detection (summary)", outputs.get("Mitigation & Detection", "No data"))
                pdf.add_section("4) References", outputs.get("References", "No data"))
                # Add a small footer note
                pdf.pdf.add_page()
                pdf.add_section("Appendix: Additional details (if needed)", "For the full technical breakdown, generate the Detailed report.")
            else:
                # Detailed: include everything
                pdf.add_section("1) CVE Overview", outputs.get("Overview", "No data"))
                pdf.add_section("2) Exploitability / PoC (detailed)", outputs.get("PoCs", "No data"))
                pdf.add_section("3) MITRE ATT&CK Mapping & TTPs", outputs.get("MITRE Mapping", "No data"))
                pdf.add_section("4) Exploitation Scenarios", outputs.get("Exploitation Scenarios", "No data"))
                pdf.add_section("5) Mitigation & Detection", outputs.get("Mitigation & Detection", "No data"))
                pdf.add_section("6) References", outputs.get("References", "No data"))

            # Provide PDF download
            pdf_bytes = pdf.output_bytes()
            filename = f"{cve_input.strip()}_{('concise' if concise else 'detailed')}_report.pdf"
            st.success("Report generated.")
            st.download_button("Download PDF", data=pdf_bytes, file_name=filename, mime="application/pdf")

            # Optional: show raw outputs (collapsed)
            with st.expander("Raw agent outputs (for debugging)"):
                for k, v in outputs.items():
                    st.subheader(k)
                    st.text(v[:1000] + ("...\n(Truncated)" if len(v) > 1000 else ""))
