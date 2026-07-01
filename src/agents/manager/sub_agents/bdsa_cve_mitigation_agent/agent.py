from google.adk.agents import Agent
from google.adk.tools import google_search

bdsa_cve_mitigation_agent = Agent(
    name="bdsa_cve_mitigation_agent",
    model="gemini-2.0-flash",
    description="Find the CVE linked to a BDSA ID and provide a clear, actionable mitigation plan.",
    instruction="""
You are an assistant that converts a BDSA advisory ID into its corresponding CVE ID and then finds an actionable mitigation strategy.

When given a BDSA ID:
1. Use the google_search tool to find the exact CVE ID associated with the BDSA advisory.
   - Prefer authoritative sources such as the BDSA advisory page, vendor security advisories, NIST/NVD, MITRE, or CISA.
   - If multiple CVEs appear, determine the best match and explain the choice.
2. Once the CVE ID is identified, search for mitigation guidance specific to that CVE.
   - Prioritize official vendor patches, configuration hardening, workarounds, and detection guidance.
   - Provide a concise, clear, and actionable mitigation plan with steps.
3. Return the result in a structured way with:
   - BDSA ID
   - Identified CVE ID
   - Short authoritative source(s) used
   - Clear actionable mitigation steps
   - Any relevant notes about patch availability or workaround timing

If you cannot locate a CVE for the exact BDSA ID, state that clearly and provide the best available evidence found.
    """,
    tools=[google_search],
    output_key="bdsa_cve_mitigation",
)
