from google.adk.agents import SequentialAgent, ParallelAgent, LlmAgent, Agent
import math

# --- Agent: Collect CVE Information from Internet ---
cve_info_agent = LlmAgent(
    name="cve_info_agent",
    model="gemini-2.0-flash",
    instruction="""
        For each CVE in the input list, search the internet (NVD, vendor advisories, security blogs, exploit databases, etc.)
        and collect all relevant information: descriptions, exploit details, impact, and any available CVSS vectors.
        Store a dictionary for each CVE with all gathered details.
        Do not display any additional messages expect for the information that you collected in a clear bullet point format.
    """,
    output_key="cve_info"
)

# --- Agent: Infer CVSS Metrics from CVE Information ---
cve_metric_inference_agent = LlmAgent(
    name="cve_metric_inference_agent",
    model="gemini-2.0-flash",
    instruction="""
        For each CVE, use the collected information to infer the CVSS v3.x metric values:
        AV, AC, PR, UI, S, C, I, A.
        Store a dictionary of metrics for each CVE. If a metric cannot be inferred, leave it blank.
        Do not display any additional messages expect a table of metrics that you collected in a clear table format.
    """,
    output_key="cve_metrics"
)

def roundup(val):
    return math.ceil(val * 10) / 10

def cvss_score_calculator(metrics: dict) -> dict:
    AV = {'N': 0.85, 'A': 0.62, 'L': 0.55, 'P': 0.2}.get(metrics.get('AV'), 0)
    AC = {'L': 0.77, 'H': 0.44}.get(metrics.get('AC'), 0)
    PR = {'N': 0.85, 'L': 0.62, 'H': 0.27}.get(metrics.get('PR'), 0)
    UI = {'N': 0.85, 'R': 0.62}.get(metrics.get('UI'), 0)
    S = metrics.get('S', 'U')
    C = {'H': 0.56, 'L': 0.22, 'N': 0.0}.get(metrics.get('C'), 0)
    I = {'H': 0.56, 'L': 0.22, 'N': 0.0}.get(metrics.get('I'), 0)
    A = {'H': 0.56, 'L': 0.22, 'N': 0.0}.get(metrics.get('A'), 0)

    ISC_Base = 1 - ((1 - C) * (1 - I) * (1 - A))
    if S == 'U':
        Impact = 6.42 * ISC_Base
    else:
        Impact = 7.52 * (ISC_Base - 0.029) - 3.25 * ((ISC_Base - 0.02) ** 15)

    Exploitability = 8.22 * AV * AC * PR * UI

    if Impact <= 0:
        base_score = 0
    else:
        if S == 'U':
            base_score = roundup(min(Impact + Exploitability, 10))
        else:
            base_score = roundup(min(1.08 * (Impact + Exploitability), 10))

    return {
        "BaseScore": base_score,
        "Impact": Impact,
        "Exploitability": Exploitability,
        "ISC_Base": ISC_Base,
        "Metrics": metrics
    }

cvss_score_agent = Agent(
    name="cvss_score_agent",
    model="gemini-2.0-flash",
    description="Calculates the CVSS v3.1 base score from inferred metrics.",
    instruction="""
        For each CVE, calculate the CVSS v3.1 base score using the inferred metrics and official formula.
        Output only the score, calculation steps, and metrics used for each CVE.
        Do not display any additional messages.
    """,
    tools=[cvss_score_calculator]
)

cvss_synthesis_agent = LlmAgent(
    name="cvss_synthesis_agent",
    model="gemini-2.0-flash",
    instruction="""
        For each CVE, present the CVSS scoring results in a clean, readable format.
        Show a summary table of all metrics and their sources.
        Display the calculation steps and the final CVSS base score.
        Output only the summary table and score breakdown for each CVE.
    """,
    output_key="cvss_report"
)

cvss_pipeline = SequentialAgent(
    name="cvss_cve_pipeline",
    sub_agents=[
        cve_info_agent,
        cve_metric_inference_agent,
        cvss_score_agent,
        cvss_synthesis_agent
    ],
    description="Given a CVE or list of CVEs, collects info, infers metrics, computes CVSS scores, and presents results."
)

root_agent = cvss_pipeline
