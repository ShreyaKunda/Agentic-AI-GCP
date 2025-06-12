from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def summarize_threat_log(log_entry: str, tool_context: ToolContext) -> dict:
    """Summarize a cyber threat log entry, extracting key information like attack type, affected system, and timestamp."""
    print(f"--- Tool: summarize_threat_log called for log_entry: {log_entry} ---")

    attack_types = ["malware", "phishing", "sql injection", "ddos", "ransomware"]
    affected_systems = ["server", "database", "network", "workstation", "cloud"]
    
    # Default response in case we cannot extract key details
    summary = {
        "attack_type": "unknown",
        "affected_system": "unknown",
        "timestamp": "unknown",
        "log_entry": log_entry,
        "summary": "",
        "detailed_summary": ""
    }
    
    # Find attack type
    for attack in attack_types:
        if attack in log_entry.lower():
            summary["attack_type"] = attack
    
    # Find affected system
    for system in affected_systems:
        if system in log_entry.lower():
            summary["affected_system"] = system
    
    # Extract timestamp (a simplified example, assuming timestamp is included in the format [YYYY-MM-DD HH:MM:SS])
    import re
    timestamp_match = re.search(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", log_entry)
    if timestamp_match:
        summary["timestamp"] = timestamp_match.group(1)

    # Generate a detailed summary
    summary["summary"] = f"Attack Type: {summary['attack_type']}\nAffected System: {summary['affected_system']}\nTimestamp: {summary['timestamp']}"
    summary["detailed_summary"] = f"{summary['summary']}\n\nDetailed Log Entry:\n{log_entry}"

    return {"status": "success", "summary": summary, "log_entry": log_entry}


# Create the Cyber Threat Log Summarizing Agent
log_summarizer = Agent(
    name="log_summarizer",
    model="gemini-2.0-flash",
    description="An agent that summarizes cyber threat logs, extracting key details like attack type, affected system, timestamp and all the details.",
    instruction=""" 
You are an agent that summarizes cyber threat logs. Given a log entry, you should:
1. Extract key details such as the attack type, affected system, timestamp and all the details.
2. Return a summary containing these details.
3. The Summary should be structured and detailed enough with sections like Attacker, Affected System, Timestamp, commands used to perform an attack with a simple exaplanation and what the command does, how does it affect the target and so on.
4. Make sure to properly format the response with each heading or sub heading in a new line. 
5. Maintain proper space between each heading or sub heading.
Example log entry:
[2023-08-01 14:30:00] Phishing attack detected on cloud system: Suspicious email activity reported from IP 192.168.1.1.

Example response:
"Here is the summary for the given log entry:
Attacker: Kali Linux 
Attack Type: Phishing
Affected System: Cloud
Timestamp: 2023-08-01 14:30:00
Commands used: 
Effect on the system:

Detailed Summary:
 At [2023-08-01 14:30:00] a phishing attack was detected on cloud system: Suspicious email activity reported from IP 192.168.1.1.
 
""",
    tools=[summarize_threat_log],
)
