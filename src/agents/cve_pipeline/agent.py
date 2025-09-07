from google.adk.agents import Agent, LlmAgent, ParallelAgent, SequentialAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools import google_search
import re

# ------------------------------------------------------------------
# CVE-focused multi-agent research & synthesis pipeline (complete)
# Produces a professional blog-style CVE report with extensive TI fields
# ------------------------------------------------------------------

CVEPATTERN = re.compile(r"\bCVE-\d{4}-\d+\b", re.IGNORECASE)

# -------------------------------
# Authoritative CVE intelligence
# -------------------------------
cve_core_agent = LlmAgent(
    name="cve_core_agent",
    model="gemini-2.0-flash",
    description="Fetch authoritative CVE metadata from NVD/MITRE/CISA/vendor sources.",
    instruction='''
You are an authoritative CVE intelligence extractor.

Given a CVE ID, gather authoritative metadata and references.

REQUIREMENTS:
1) Prioritize NVD, MITRE, CVE.org, CISA, vendor advisories and ExploitDB.
2) Extract and normalize:
   - cve_id
   - official_description
   - cvss_v3_v4_scores (list)
   - severity
   - cwe (if any)
   - affected_products (list)
   - exploitability_summary (public PoC? Metasploit? Active exploitation?)
   - publication_dates and last_modified (if available)
   - references: list of {"title":..., "link":...}
3) If sources disagree, list discrepancies with attribution.
4) Output as a JSON-like markdown block under top-level key "cve_core".

TOOLS: Use google_search and bias queries with site: filters (e.g., site:nvd.nist.gov).
    ''',
    tools=[google_search],
    output_key="cve_core"
)

# -------------------------------
# Open-source intel agents
# -------------------------------

youtube_agent = Agent(
    name="youtube_agent",
    model="gemini-2.0-flash",
    description="Finds and summarizes relevant YouTube videos/playlists.",
    instruction='''
Locate up to 5 authoritative YouTube results related to the CVE/topic.
For each: Title, Channel, Duration (if available), Link, 1-2 sentence summary, relevance note.
Bias results to vendor/security researcher channels when possible.
    ''',
    tools=[google_search],
    output_key="youtube_results"
)

reddit_agent = LlmAgent(
    name="reddit_agent",
    model="gemini-2.0-flash",
    description="Summarizes top Reddit discussions containing PoCs or analysis.",
    instruction='''
Find up to 5 Reddit threads relevant to the CVE/topic. For each: subreddit, title, link, 2-3 sentence summary, any PoC links, and a reliability note (verified/unverified).
    ''',
    tools=[google_search],
    output_key="reddit_results"
)

stackoverflow_agent = LlmAgent(
    name="stackoverflow_agent",
    model="gemini-2.0-flash",
    description="Fetches developer-focused posts and fixes from Stack Overflow.",
    instruction='''
Search Stack Overflow for posts relevant to the vulnerable component or CVE. Return up to 5 items: title, link, 1-line summary of solution/workaround.
    ''',
    tools=[google_search],
    output_key="stackoverflow_results"
)

twitter_agent = LlmAgent(
    name="twitter_agent",
    model="gemini-2.0-flash",
    description="Collects recent tweets/threads that discuss PoCs, active exploitation, or vendor notes.",
    instruction='''
Find up to 5 tweets or threads referencing the CVE/topic. For each: handle, date (if available), snippet, link, and short analysis (is it PoC / exploit / vendor comment?).
    ''',
    tools=[google_search],
    output_key="twitter_results"
)

github_agent = LlmAgent(
    name="github_agent",
    model="gemini-2.0-flash",
    description="Searches GitHub for PoCs, exploit modules, and remediation commits.",
    instruction='''
Find up to 5 GitHub items: repo or issue title, link, 1-2 sentence summary, and classification (PoC / exploit module / patch / discussion).
    ''',
    tools=[google_search],
    output_key="github_results"
)

news_agent = LlmAgent(
    name="news_agent",
    model="gemini-2.0-flash",
    description="Collects relevant news and technical blog writeups.",
    instruction='''
Collect up to 5 reputable news/blog articles analyzing the CVE. Provide title, publisher, date, 2-3 sentence summary, and link.
    ''',
    tools=[google_search],
    output_key="news_results"
)

gov_agent = LlmAgent(
    name="gov_agent",
    model="gemini-2.0-flash",
    description="Collects CERT/vendor advisories and authoritative guidance.",
    instruction='''
Collect authoritative advisories from NVD, MITRE, CISA, vendor advisories, and national CERTs. For each: title, issuer, date, summary, and link. Capture CVSS vectors if present.
    ''',
    tools=[google_search],
    output_key="gov_results"
)

# -------------------------------
# MITRE ATT&CK lookup & TTP mapping
# -------------------------------
mitre_lookup_agent = LlmAgent(
    name="mitre_lookup_agent",
    model="gemini-2.0-flash",
    description="Automatically searches MITRE ATT&CK and mapping resources to identify candidate techniques.",
    instruction='''
Using CVE core and open-source findings, search for MITRE ATT&CK techniques that map to this CVE's behaviour (e.g., RCE -> T1059, privilege escalation -> T1068).
For each technique include: Technique ID, Name, Tactic, short rationale, and a detection idea (log source + what to look for).
Output as a JSON-like structure under key "mitre_techniques".
    ''',
    tools=[google_search],
    output_key="mitre_techniques"
)

ttp_mapping_agent = LlmAgent(
    name="ttp_mapping_agent",
    model="gemini-2.0-flash",
    description="Prioritizes MITRE techniques into probable attack chains and provides detection priorities.",
    instruction='''
Consume mitre_techniques and other OSINT. Produce:
1) Technique table (ID | Name | Tactic | Confidence | Rationale)
2) 3 likely attack chains (ordered list of technique IDs with brief explanation)
3) Top 5 prioritized detection recommendations (log source + rule idea)
Output under key "ttp_map" as markdown or JSON-like text.
    ''',
    output_key="ttp_map"
)

# -------------------------------
# Exploitation scenarios
# -------------------------------
exploitation_agent = LlmAgent(
    name="exploitation_agent",
    model="gemini-2.0-flash",
    description="Writes 3-5 realistic exploitation scenarios, with prerequisites, step-by-step chain, artifacts, and quick containment actions.",
    instruction='''
Based on cve_core, ttp_map, mitre_techniques, and OSINT outputs, write 3-5 exploitation scenarios. For each scenario include:
- Title and summary
- Prerequisites (network exposure, auth, config)
- Step-by-step exploitation chain (numbered) referencing MITRE IDs
- Expected impact
- Observable artifacts/IOCs (file names, processes, network patterns)
- Short containment checklist
Output under key "exploitation_scenarios" as markdown.
    ''',
    output_key="exploitation_scenarios"
)

# -------------------------------
# Risk assessment & mitigation (single output key)
# -------------------------------
mitigation_risk_agent = LlmAgent(
    name="mitigation_risk_agent",
    model="gemini-2.0-flash",
    description="Produces a formal risk assessment, remediation SLA, IoCs, threat-actor notes, and an extensive mitigation plan.",
    instruction='''
Produce a single JSON-like object under key "mitigation_risk_output" containing the following sections:
- risk_assessment: {criticality, likelihood, impact_confidentiality, impact_integrity, impact_availability, affected_asset_types, evidence_of_active_exploitation (yes/no/unknown with sources)}
- remediation_sla: suggested timelines (Emergency: <24h, High: 24-72h, Normal: 72h-14d) with rationale
- threat_actor_usage: any known APT or criminal actor activity linked to this CVE (with sources). If none known, say 'none known'.
- iocs: list of indicators (ip, domain, file hash) discovered in OSINT with source attribution
- mitigation_plan: ordered list of mitigation steps with priority tags (Immediate, Short-term, Medium-term, Long-term). Each step should include: Why it helps, How to implement (commands/configs when possible), Validation steps, and Rollback notes.
- detection_hunting: top 8 SIEM/hunting checks (give example query pseudo-code or Sigma-like description) and log sources.

Use cve_core, mitre_techniques, ttp_map, exploitation_scenarios, and gov_results as inputs. Cite sources inline where possible in the text values.
    ''',
    output_key="mitigation_risk_output"
)

# -------------------------------
# Final merger: produce blog-style professional report
# -------------------------------
cve_merger_agent = LlmAgent(
    name="cve_merger_agent",
    model="gemini-2.0-flash",
    description="Synthesizes every input into a professional, copy-paste-ready blog-style CVE report with source citations and per-source summaries.",
    instruction='''
Using ONLY the inputs provided to this agent, produce a polished, professional, blog-style CVE report (markdown) that is copy-paste ready for publication.

REQUIRED STRUCTURE (use exact section headings):

# CVE Intelligence Report: {cve_core.cve_id}

## TL;DR (1-2 sentences)

## 1) CVE Overview (Authoritative)
- CVE ID:
- Short description:
- CVSS v3/v4 scores & vectors:
- Severity:
- CWE(s):
- Affected products/versions:
- Exploitability summary (public PoC / Metasploit / active exploitation):
- Authoritative references (bullet list of title + link)

## 2) Key Findings (summarized, per source)
- **Government / CERT advisories:** short bullets with links
- **News & Blogs:** short bullets with links
- **GitHub (PoCs / modules):** bullets with link + classification
- **Twitter (top chatter):** bullets with snippet + link
- **Reddit (discussions / PoCs):** bullets with link + reliability note
- **YouTube (explainers / demos):** bullets with link + short note
- **Stack Overflow (developer fixes/workarounds):** bullets with link

## 3) MITRE ATT&CK Mapping & TTPs
- Table of relevant techniques (ID | Name | Tactic | Confidence | Rationale)
- Likely attack chains (numbered)

## 4) Exploitation Scenarios
- Insert scenarios from exploitation_scenarios with artifacts and containment steps

## 5) Risk Assessment & Remediation SLA
- Insert risk_assessment summary (from mitigation_risk_output)
- Remediation SLA suggestions with justification

## 6) Actionable Mitigation Plan (Prioritized)
- Present mitigation_plan items clearly grouped by Immediate / Short-term / Medium / Long-term
- For each item include commands/config snippets or configuration values where practical and validation steps

## 7) Detection & Hunting Guidance
- Insert detection_hunting checks and example queries

## 8) IoCs & Threat Actor Notes
- List IoCs (with sources) and any threat actor usage notes

## Appendix: Full References & Raw Source Summaries
- Provide a numbered list of every link discovered by the sub-agents with a 1-line summary for each so readers can click-through.

STYLE: Professional, concise, actionable. Use bullet lists, short clear paragraphs, and include all source links. Do NOT invent external facts; rely only on the inputs.

Output the complete markdown under the output key "final_blog_report".
    ''',
    output_key="final_blog_report"
)

# -------------------------------
# Pipeline wiring
# -------------------------------
parallel_research = ParallelAgent(
    name="parallel_research",
    sub_agents=[
        cve_core_agent,
        youtube_agent,
        reddit_agent,
        stackoverflow_agent,
        twitter_agent,
        github_agent,
        news_agent,
        gov_agent,
    ],
    description="Run authoritative CVE intel and open-source collection in parallel."
)

cve_pipeline = SequentialAgent(
    name="cve_pipeline",
    sub_agents=[
        parallel_research,
        mitre_lookup_agent,
        ttp_mapping_agent,
        exploitation_agent,
        mitigation_risk_agent,
        cve_merger_agent,
    ],
    description="End-to-end CVE pipeline producing a blog-style final report with TI and mitigation."
)

# Router helper (optional): run cve pipeline if input contains CVE else raise or run generic

def run_research(user_input: str, tool_context: ToolContext):
    if CVEPATTERN.search(user_input or ""):
        result = cve_pipeline.run(user_input, tool_context=tool_context)
        # Only return the final blog report
        return result.get("final_blog_report", "No report generated.")
    else:
        result = cve_pipeline.run(user_input, tool_context=tool_context)
        return result.get("final_blog_report", "No report generated.")

# Export root_agent for the ADK loader
root_agent = cve_pipeline
