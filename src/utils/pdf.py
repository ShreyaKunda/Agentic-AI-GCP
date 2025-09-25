import streamlit as st
import requests
from requests.exceptions import RequestException, Timeout
import json
import time
import io
from datetime import datetime, timedelta
import random
import re

st.set_page_config(page_title="Research and Summarization Agent", layout="wide")

# App styling: inject a compact CSS theme to improve visuals (no icons, just clean styling)
st.markdown("""
<style>
:root{--bg:#f4f6f8;--card:#ffffff;--muted:#6b7280;--accent:#2563eb;--accent-2:#1e40af}
/* App background and container spacing */
div[data-testid="stAppViewContainer"] > .main > div {
    background: var(--bg);
    padding-top: 18px;
}
div.block-container{padding:28px 32px 40px 32px;}

/* Sidebar styling: light, like a modern site */
div[data-testid="stSidebar"] {
    background: #ffffff;
    color: #0f172a;
    padding-top: 18px;
    border-right: 1px solid rgba(15,23,42,0.06);
}
div[data-testid="stSidebar"] h1, div[data-testid="stSidebar"] h2, div[data-testid="stSidebar"] h3, div[data-testid="stSidebar"] p {
    color: #0f172a !important;
}

/* Headings */
h1, h2, h3 { color: #0f172a; font-weight:700; }
.markdown-text-container p { color:#0f172a; line-height:1.6; font-size:15px; }

/* Buttons - flat, professional */
button, .stButton>button {
    background: linear-gradient(90deg,var(--accent),var(--accent-2)) !important;
    color: #fff !important;
    border: none !important;
    padding: 8px 14px !important;
    border-radius: 8px !important;
    box-shadow: 0 6px 18px rgba(30,64,175,0.08) !important;
    transition: transform .12s ease, box-shadow .12s ease !important;
}
button:hover, .stButton>button:hover{ transform: translateY(-2px) !important; }
.stDownloadButton>button{ background: linear-gradient(90deg,#0ea5e9,#0284c7) !important; box-shadow: 0 6px 18px rgba(2,132,199,0.06) !important; }

/* Cards / panels */
.card, .stMetric, .stProgress { border-radius: 10px; }
.stMetric>div>div{ background: #fff; padding:10px; box-shadow: 0 6px 18px rgba(2,6,23,0.04); border-radius:10px }

/* Progress bar - modern blue */
div.stProgress > div > div > div {
  background: linear-gradient(90deg,var(--accent),var(--accent-2)) !important;
  border-radius: 8px !important;
}

/* Code blocks and preformatted text */
pre, code { background:#0f172a; color:#e6eef8; padding:8px; border-radius:8px; }

/* Links */
a { color: #2563eb !important; text-decoration: none; }

@media (max-width: 768px){ div.block-container{ padding:16px } }

</style>
""", unsafe_allow_html=True)

# Configuration
GEMINI_API_KEY = ""  # Replace with your actual Gemini API key

class ResearchAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.headers = {"Content-Type": "application/json"}
    
    def call_gemini(self, prompt):
        """Make API call to Gemini with retries and exponential backoff.

        Returns the text on success or a descriptive error string on failure.
        """
        payload = {
            "contents": [
                {"role": "user", "parts": [{"text": prompt}]}
            ]
        }

        max_retries = 3
        base_timeout = 60  # seconds per request
        for attempt in range(1, max_retries + 1):
            try:
                resp = requests.post(
                    f"{self.endpoint}?key={self.api_key}",
                    headers=self.headers,
                    json=payload,
                    timeout=base_timeout
                )

                if resp.status_code == 200:
                    try:
                        return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                    except Exception:
                        return f"Error: unexpected response format (status=200)."

                # Non-200 response: for 429 or 5xx we retry, otherwise return error
                status = resp.status_code
                text = resp.text
                if status in (429, 500, 502, 503, 504):
                    # Retryable server-side or rate limit errors
                    wait = (2 ** (attempt - 1)) + random.uniform(0, 1)
                    time.sleep(wait)
                    continue
                else:
                    return f"API Error {status}: {text}"

            except Timeout:
                # Request timed out
                if attempt < max_retries:
                    wait = (2 ** (attempt - 1)) + random.uniform(0, 1)
                    time.sleep(wait)
                    continue
                return "Error: request timed out after several attempts."
            except RequestException as e:
                # Generic network error
                if attempt < max_retries:
                    wait = (2 ** (attempt - 1)) + random.uniform(0, 1)
                    time.sleep(wait)
                    continue
                return f"Network error: {str(e)}"

        return "Error: failed to get a response after multiple attempts."
    
    def research_web_articles(self, topic):
        """Generate web article research using Gemini"""
        prompt = f"""
        Act as a comprehensive research specialist. For the topic "{topic}", generate exactly 4 detailed research sources from web articles.

        For each source, provide the following structure:

        ## Source [NUMBER]: [Descriptive Title]
        
        **Summary of Source:**
        [Provide a comprehensive 4-5 sentence summary of what this source covers about {topic}, including the main approach, methodology, and conclusions]
        
        **Technical Details:**
        [Provide in-depth technical details including:
        - Specific algorithms, protocols, or methodologies used
        - Technical architecture and design patterns
        - Performance metrics, benchmarks, or measurements
        - System requirements and constraints
        - Technical challenges and how they were addressed
        - Implementation specifics and technical considerations
        This should be 6-8 sentences of detailed technical information]
        
        **Implementation Workflow:**
        Step 1: [Detailed first implementation step with technical specifics]
        Step 2: [Detailed second implementation step with technical specifics]
        Step 3: [Detailed third implementation step with technical specifics]
        Step 4: [Detailed fourth implementation step with technical specifics]
        Step 5: [Detailed fifth implementation step with technical specifics]
        
        **Code Examples and Details:**
        [Provide specific code snippets, configuration examples, or technical implementation details. Include:
        - Code structure and key functions
        - Configuration parameters and settings
        - API calls or database queries
        - Error handling mechanisms
        - Performance optimization techniques
        Should be 4-5 detailed technical examples]
        
        **Tools and Technologies Used:**
        - Primary Tool 1: [Tool name and specific usage details]
        - Primary Tool 2: [Tool name and specific usage details]
        - Supporting Library 1: [Library name and integration details]
        - Supporting Library 2: [Library name and integration details]
        - Development Environment: [Specific environment details]
        
        **Key Takeaways:**
        • [Specific actionable insight with technical context]
        • [Specific performance or security insight]
        • [Specific implementation best practice]
        • [Specific limitation or consideration]
        • [Specific future implication or recommendation]
        
        **References and Further Reading:**
        • Research Paper: [Specific paper title and key contribution]
        • Documentation: [Specific technical documentation]
        • Case Study: [Specific real-world implementation]
        • Related Tool: [Specific tool or framework]
        
        ---
        
        Focus on providing deep technical content that goes beyond general explanations. Each source should offer specific, actionable technical information about "{topic}".
        """
        return self.call_gemini(prompt)
    
    def research_youtube_content(self, topic):
        """Generate YouTube content research using Gemini"""
        prompt = f"""
        Act as a technical video content analyst. For the topic "{topic}", generate exactly 4 detailed video content analyses.

        For each video source, provide the following structure:

        ## Video Analysis [NUMBER]: [Descriptive Content Title]
        
        **Summary of Source:**
        [Provide a comprehensive 4-5 sentence summary of what this video content covers about {topic}, including the educational approach, target audience, and key learning outcomes]
        
        **Technical Details:**
        [Provide in-depth technical details covered in the video including:
        - Specific technical concepts and methodologies explained
        - System architecture and design principles discussed
        - Performance analysis and optimization techniques
        - Security considerations and implementation details
        - Troubleshooting approaches and debugging methods
        - Real-world applications and use cases
        This should be 6-8 sentences of detailed technical information]
        
        **Implementation Workflow:**
        Step 1: [Detailed implementation step as demonstrated in video]
        Step 2: [Detailed configuration or setup step]
        Step 3: [Detailed execution or deployment step]
        Step 4: [Detailed testing or validation step]
        Step 5: [Detailed optimization or maintenance step]
        
        **Code Examples and Details:**
        [Provide specific code examples, commands, or configurations shown in the video:
        - Command line instructions and parameters
        - Code structure and implementation patterns
        - Configuration files and settings
        - Database schemas or API endpoints
        - Testing procedures and validation methods
        Should be 4-5 detailed technical examples]
        
        **Tools and Technologies Used:**
        - Primary Platform: [Platform name and specific version/configuration]
        - Development Tools: [Specific tools demonstrated]
        - Libraries/Frameworks: [Specific libraries with usage context]
        - Testing Tools: [Specific testing or monitoring tools]
        - Deployment Environment: [Specific environment setup]
        
        **Key Takeaways:**
        • [Specific technical insight with practical application]
        • [Specific performance or security consideration]
        • [Specific best practice or optimization technique]
        • [Specific common mistake or pitfall to avoid]
        • [Specific advanced technique or future consideration]
        
        **References and Further Reading:**
        • Official Documentation: [Specific documentation referenced]
        • Related Tutorial: [Specific follow-up learning resource]
        • Research Source: [Academic or industry research mentioned]
        • Community Resource: [Specific community or forum reference]
        
        ---
        
        Focus on technical educational content that provides deep implementation details and practical knowledge about "{topic}".
        """
        return self.call_gemini(prompt)
    
    def research_github_repos(self, topic):
        """Generate GitHub repository research using Gemini"""
        prompt = f"""
        Act as a code repository analyst. For the topic "{topic}", generate exactly 4 detailed repository analyses.

        For each repository, provide the following structure:

        ## Repository Analysis [NUMBER]: [Descriptive Project Name]
        
        **Summary of Source:**
        [Provide a comprehensive 4-5 sentence summary of what this repository provides for {topic}, including the main functionality, target use cases, and architectural approach]
        
        **Technical Details:**
        [Provide in-depth technical details including:
        - Core algorithms and data structures implemented
        - System architecture and design patterns used
        - Performance characteristics and scalability features
        - Security mechanisms and validation approaches
        - Integration capabilities and API design
        - Memory management and resource optimization
        This should be 6-8 sentences of detailed technical information]
        
        **Implementation Workflow:**
        Step 1: [Detailed installation and environment setup]
        Step 2: [Detailed configuration and initialization process]
        Step 3: [Detailed integration and deployment steps]
        Step 4: [Detailed testing and validation procedures]
        Step 5: [Detailed customization and optimization steps]
        
        **Code Examples and Details:**
        [Provide specific code examples and implementation details:
        - Core function implementations and usage patterns
        - Configuration examples and parameter settings
        - API usage examples and integration patterns
        - Error handling and exception management
        - Performance monitoring and debugging approaches
        Should be 4-5 detailed code examples with explanations]
        
        **Tools and Technologies Used:**
        - Programming Language: [Language with specific version and features used]
        - Core Dependencies: [Major libraries and their specific roles]
        - Build Tools: [Build system and compilation details]
        - Testing Framework: [Testing tools and methodologies]
        - Deployment Tools: [Deployment and orchestration tools]
        
        **Key Takeaways:**
        • [Specific implementation insight with technical context]
        • [Specific performance optimization or efficiency gain]
        • [Specific architectural decision and its benefits]
        • [Specific limitation or trade-off to consider]
        • [Specific extension or customization possibility]
        
        **References and Further Reading:**
        • Core Algorithm: [Specific algorithm or research paper implemented]
        • Related Projects: [Similar or complementary repositories]
        • Technical Documentation: [Detailed implementation guides]
        • Research Background: [Academic or industry research basis]
        
        ---
        
        Focus on providing deep technical analysis of code implementations and practical usage for "{topic}".
        """
        return self.call_gemini(prompt)
    
    def research_reddit_discussions(self, topic):
        """Generate Reddit discussion research using Gemini"""
        prompt = f"""
        Act as a community discussion analyst. For the topic "{topic}", generate exactly 4 detailed discussion analyses.

        For each discussion, provide the following structure:

        ## Discussion Analysis [NUMBER]: [Descriptive Discussion Theme]
        
        **Summary of Source:**
        [Provide a comprehensive 4-5 sentence summary of what this discussion covers about {topic}, including the main questions raised, community expertise level, and key debate points]
        
        **Technical Details:**
        [Provide in-depth technical details discussed by the community including:
        - Specific technical challenges and problem-solving approaches
        - Implementation experiences and lessons learned
        - Performance issues and optimization strategies
        - Security vulnerabilities and mitigation techniques
        - Integration problems and solution approaches
        - Best practices and common pitfalls identified by practitioners
        This should be 6-8 sentences of detailed technical community insights]
        
        **Implementation Workflow:**
        Step 1: [Detailed implementation approach suggested by community]
        Step 2: [Detailed setup or configuration process discussed]
        Step 3: [Detailed execution or deployment approach]
        Step 4: [Detailed testing or validation methods shared]
        Step 5: [Detailed troubleshooting or maintenance practices]
        
        **Code Examples and Details:**
        [Provide specific code examples, configurations, or technical solutions shared:
        - Code snippets and implementation examples shared by users
        - Configuration files and setup instructions
        - Command-line tools and script examples
        - Debugging approaches and diagnostic techniques
        - Performance tuning and optimization code
        Should be 4-5 detailed technical examples from community contributions]
        
        **Tools and Technologies Used:**
        - Primary Tools: [Specific tools discussed with user experiences]
        - Alternative Solutions: [Alternative approaches debated]
        - Monitoring Tools: [Specific monitoring or diagnostic tools mentioned]
        - Development Environment: [Specific environment setups discussed]
        - Integration Platforms: [Specific platforms and their trade-offs]
        
        **Key Takeaways:**
        • [Specific community insight with practical implications]
        • [Specific performance or scalability lesson learned]
        • [Specific security or reliability consideration]
        • [Specific common mistake identified by practitioners]
        • [Specific emerging trend or future direction]
        
        **References and Further Reading:**
        • Community Resource: [Specific community-recommended resource]
        • Expert Recommendation: [Specific tool or approach recommended by experts]
        • Related Discussion: [Related technical discussion or thread]
        • External Resource: [External documentation or guide mentioned]
        
        ---
        
        Focus on real-world practitioner experiences and community-driven technical insights about "{topic}".
        """
        return self.call_gemini(prompt)
    
    def research_twitter_content(self, topic):
        """Generate Twitter/X content research using Gemini"""
        prompt = f"""
        Act as a social media technical content analyst. For the topic "{topic}", generate exactly 3 detailed expert content analyses.

        For each expert content source, provide the following structure:

        ## Expert Analysis [NUMBER]: [Descriptive Content Theme]
        
        **Summary of Source:**
        [Provide a comprehensive 4-5 sentence summary of what this expert content covers about {topic}, including the expert's perspective, key arguments, and professional insights shared]
        
        **Technical Details:**
        [Provide in-depth technical details shared by the expert including:
        - Specific technical analysis and professional assessment
        - Industry trends and emerging technology patterns
        - Performance benchmarks and comparative analysis
        - Security implications and risk assessments
        - Implementation challenges from industry experience
        - Technical predictions and future technology directions
        This should be 6-8 sentences of detailed expert technical insights]
        
        **Implementation Workflow:**
        Step 1: [Detailed approach recommended by the expert]
        Step 2: [Detailed strategy or methodology suggested]
        Step 3: [Detailed implementation or deployment advice]
        Step 4: [Detailed validation or assessment approach]
        Step 5: [Detailed optimization or scaling recommendations]
        
        **Code Examples and Details:**
        [Provide specific technical examples, approaches, or methodologies shared:
        - Technical architecture patterns recommended
        - Implementation strategies and design decisions
        - Performance optimization techniques
        - Security implementation approaches
        - Monitoring and diagnostic methods
        Should be 4-5 detailed technical recommendations with context]
        
        **Tools and Technologies Used:**
        - Industry-Standard Tools: [Specific tools recommended with rationale]
        - Emerging Technologies: [New or trending tools discussed]
        - Integration Platforms: [Specific platforms and their advantages]
        - Monitoring Solutions: [Specific monitoring or analytics tools]
        - Development Frameworks: [Specific frameworks and their use cases]
        
        **Key Takeaways:**
        • [Specific expert insight with industry context]
        • [Specific trend prediction with technical implications]
        • [Specific best practice with professional rationale]
        • [Specific risk or challenge with mitigation approach]
        • [Specific opportunity or innovation with implementation potential]
        
        **References and Further Reading:**
        • Industry Report: [Specific industry analysis or whitepaper]
        • Professional Resource: [Specific professional or enterprise resource]
        • Research Study: [Specific research or case study referenced]
        • Expert Network: [Specific professional community or network]
        
        ---
        
        Focus on high-level expert insights and industry-grade technical analysis of "{topic}".
        """
        return self.call_gemini(prompt)
    
    def generate_comprehensive_analysis(self, topic, research_data):
        """Generate final comprehensive analysis"""
        prompt = f"""
        You are an expert technical analyst. Based on the following research data about "{topic}", create a comprehensive technical report.

        Research Data Collected:
        {research_data}

        Generate a detailed report with these sections:

        ## Executive Summary
        [Concise overview of key findings]

        ## Technical Deep Dive
        [Detailed technical analysis with specific implementation details]

        ## Current Trends and Developments
        [Based on the "research" data, what are the latest trends]

        ## Implementation Strategies
        [Practical approaches and best practices]

        ## Tools and Technologies
        [Specific tools mentioned in research with detailed usage]

        ## Risk Assessment and Mitigation
        [Security considerations and mitigation strategies]

        ## Future Outlook
        [Predictions based on current research trends]

        ## Key Takeaways
        [5-7 bullet points of critical insights]

        ## References and Further Reading
        [Organize all the researched sources by platform]

        Make this report comprehensive, technical, and actionable. Use the research data to support all claims and recommendations.
        """
        return self.call_gemini(prompt)

def main():
    # Initialize the research agent
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_api_key_here":
        st.error("Please set your Gemini API key in the code!")
        st.stop()
    
    agent = ResearchAgent(GEMINI_API_KEY)
    
    # Initialize session state
    if 'research_completed' not in st.session_state:
        st.session_state.research_completed = False
    if 'research_results' not in st.session_state:
        st.session_state.research_results = {}
    if 'comprehensive_report' not in st.session_state:
        st.session_state.comprehensive_report = ""
    if 'current_topic' not in st.session_state:
        st.session_state.current_topic = ""
    
    # Sidebar Navigation
    with st.sidebar:
        st.title("Research Navigator")
        st.markdown("---")
        
        if st.session_state.research_completed:
            st.markdown("### View Results")
            
            platform_options = ["Comprehensive Report"] + [platform for platform in st.session_state.research_results.keys()]
            
            selected_view = st.selectbox(
                "Select Platform to View:",
                platform_options,
                index=0
            )
            
            st.markdown("---")
            st.markdown("### Research Topic")
            st.info(f"**{st.session_state.current_topic}**")
            
            st.markdown("---")
            st.markdown("### Research Stats")
            # Count sources by crude '## Source' headings inside each platform text
            total_sources = sum(len(str(data.get('text','')).split("##")) - 1 for data in st.session_state.research_results.values() if data and data.get('text'))
            st.metric("Total Sources Found", total_sources)
            st.metric("Platforms Searched", len(st.session_state.research_results.keys()))
            
            if st.button("Start New Research", use_container_width=True):
                st.session_state.research_completed = False
                st.session_state.research_results = {}
                st.session_state.comprehensive_report = ""
                st.session_state.current_topic = ""
                st.rerun()
        else:
            st.markdown("## Platforms Available for Research")
            st.markdown("""
            <ul style='font-size:16px;line-height:2;'>
                <li><b>Web Articles</b></li>
                <li> <b>YouTube Videos</b></li>
                <li> <b>GitHub Repositories</b></li>
                <li> <b>Reddit Discussions</b></li>
                <li> <b>Twitter/X Threads</b></li>
            </ul>
            """, unsafe_allow_html=True)
    
    # Main Content Area
    st.title("Research and Summarization Agent")
    st.markdown("Agent that retrieves information from across the web and provides detailed summaries.")

    if not st.session_state.research_completed:
        st.markdown("""
        <div style='background-color:#f8f9fa;padding:30px 30px 10px 30px;border-radius:12px;margin-bottom:20px;'>
            <h2 style='color:#222;text-align:center;'>Comprehensive Research Agent</h2>
            <p style='text-align:center;color:#555;font-size:18px;'></p>
        </div>
        """, unsafe_allow_html=True)

        topic = st.text_input(
            "Research Topic",
            placeholder="e.g., DMA Attacks, Zero Trust Architecture, Machine Learning Security",
            help="Enter a technical topic you want to research across multiple platforms"
        )

        st.markdown("<h4 style='margin-top:30px;'>Choose the platforms from which you would like to retrieve information.</h4>", unsafe_allow_html=True)
        col1, col2, col3, col4, col5 = st.columns(5)
        platforms = {}
        with col1:
            platforms["Web Articles"] = st.checkbox("Web Articles", value=True)
        with col2:
            platforms["YouTube"] = st.checkbox("YouTube", value=True)
        with col3:
            platforms["GitHub"] = st.checkbox("GitHub", value=True)
        with col4:
            platforms["Reddit"] = st.checkbox("Reddit", value=True)
        with col5:
            platforms["Twitter/X"] = st.checkbox("Twitter/X", value=False)
        research_platforms = [platform for platform, selected in platforms.items() if selected]

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div style='color:#888;font-size:15px;text-align:center;'></div>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        if st.button("Start Research", type="primary", disabled=not topic or not research_platforms, use_container_width=True):
            if topic and research_platforms:
                st.session_state.current_topic = topic
                progress_container = st.container()
                with progress_container:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    total_steps = len(research_platforms) + 1
                    current_step = 0
                    research_results = {}
                    for platform in research_platforms:
                        current_step += 1
                        progress = current_step / total_steps
                        progress_bar.progress(progress)
                        status_text.text(f"Researching {platform}... ({current_step}/{total_steps})")
                        # helper to attach per-source URLs into the returned text
                        def attach_urls_to_sources(text: str):
                            """Scan top-level '##' sections. For each section, find the first URL in that section and
                            insert a 'Source URL: <url>' line after the header. Returns (modified_text, list_of_urls).
                            """
                            if not text:
                                return text, []
                            url_re = re.compile(r"https?://[\w\-\.\/%&?=+#~:@,()\[\]\$]+")
                            # find all header positions
                            headers = [m for m in re.finditer(r'(?m)^##\s+(.*)$', text)]
                            if not headers:
                                # no clear sections; just extract urls globally
                                urls = url_re.findall(text)
                                # dedupe
                                seen = set(); uniq = []
                                for u in urls:
                                    if u not in seen:
                                        seen.add(u); uniq.append(u)
                                return text, uniq

                            parts = []
                            urls_found = []
                            last_end = 0
                            for i, h in enumerate(headers):
                                start = h.start()
                                header_line = h.group(0)
                                header_title = h.group(1).strip()
                                # block content runs from end of this header line to start of next header or end
                                next_start = headers[i+1].start() if i+1 < len(headers) else len(text)
                                block = text[h.end():next_start]
                                # search for first URL in block
                                m = url_re.search(block)
                                insert_line = ''
                                if m:
                                    url = m.group(0)
                                    urls_found.append(url)
                                    insert_line = f"\n\nSource URL: {url}\n"
                                # reconstruct this part: header line + optional insert + block
                                parts.append(header_line + '\n' + insert_line + block)
                                last_end = next_start

                            # if there is any prefix before the first header, keep it
                            prefix = text[:headers[0].start()]
                            new_text = prefix + '\n'.join(parts)
                            # dedupe urls_found preserving order
                            seen = set(); uniq = []
                            for u in urls_found:
                                if u not in seen:
                                    seen.add(u); uniq.append(u)
                            return new_text, uniq

                        if platform == "Web Articles":
                            result_text = agent.research_web_articles(topic)
                            modified, urls = attach_urls_to_sources(result_text)
                            research_results["Web Articles"] = {"text": modified, "urls": urls}
                        elif platform == "YouTube":
                            result_text = agent.research_youtube_content(topic)
                            modified, urls = attach_urls_to_sources(result_text)
                            research_results["YouTube"] = {"text": modified, "urls": urls}
                        elif platform == "GitHub":
                            result_text = agent.research_github_repos(topic)
                            modified, urls = attach_urls_to_sources(result_text)
                            research_results["GitHub"] = {"text": modified, "urls": urls}
                        elif platform == "Reddit":
                            result_text = agent.research_reddit_discussions(topic)
                            modified, urls = attach_urls_to_sources(result_text)
                            research_results["Reddit"] = {"text": modified, "urls": urls}
                        elif platform == "Twitter/X":
                            result_text = agent.research_twitter_content(topic)
                            modified, urls = attach_urls_to_sources(result_text)
                            research_results["Twitter/X"] = {"text": modified, "urls": urls}
                        time.sleep(2)
                    # Always generate comprehensive analysis
                    current_step += 1
                    progress_bar.progress(1.0)
                    status_text.text("Generating comprehensive analysis...")
                    research_data = ""
                    for platform, data in research_results.items():
                        text = data.get('text') if isinstance(data, dict) else str(data)
                        research_data += f"\n\n## {platform.upper()} RESEARCH:\n{text}"
                    comprehensive_report = agent.generate_comprehensive_analysis(topic, research_data)
                    st.session_state.comprehensive_report = comprehensive_report
                    st.session_state.research_results = research_results
                    st.session_state.research_completed = True
                    progress_bar.empty()
                    status_text.empty()
                    st.success("Research completed successfully!")
                    time.sleep(1)
                    st.rerun()
            else:
                st.warning("Please enter a topic and select at least one research platform.")
    
    else:
        # Display Results Based on Sidebar Selection
        st.markdown("---")
        
        # Get current selection from sidebar
        platform_options = ["Comprehensive Report"] + [platform for platform in st.session_state.research_results.keys()]
        selected_view = st.selectbox(
            "Select View:",
            platform_options,
            index=0
        )
        
        if selected_view == "Comprehensive Report":
            st.markdown("# Comprehensive Research Report")
            st.markdown(f"### Topic: *{st.session_state.current_topic}*")
            st.markdown("---")
            
            if st.session_state.comprehensive_report:
                st.markdown(st.session_state.comprehensive_report)
                # Show per-platform source URLs (if available)
                all_platform_urls = []
                for platform, data in st.session_state.research_results.items():
                    if isinstance(data, dict):
                        urls = data.get('urls', [])
                        if urls:
                            st.markdown(f"### {platform} - Source URLs")
                            for u in urls:
                                st.markdown(f"- [{u}]({u})")
                            all_platform_urls.extend(urls)
                # Provide a downloadable PDF of the full comprehensive report
                try:
                    from fpdf import FPDF

                    class StyledPDF(FPDF):
                        def header(self):
                            # Small header on all pages except cover
                            if self.page_no() > 1:
                                self.set_font("Arial", "B", 12)
                                self.set_y(10)
                                hdr = getattr(self, 'report_title', '')
                                self.cell(0, 6, hdr, ln=True, align='C')
                                self.ln(2)

                        def footer(self):
                            self.set_y(-12)
                            self.set_font('Arial', 'I', 8)
                            page_text = f"Page {self.page_no()}/{{nb}}"
                            self.cell(0, 10, page_text, align='C')

                    def create_pdf_bytes(title: str, topic: str, content: str, platform_urls: list | None = None) -> bytes:
                        # Helpers for links and sanitization
                        def sanitize_text(s: str) -> str:
                            # Replace common unicode characters that PyFPDF can't encode
                            replacements = {
                                '\u2022': '-',  # bullet
                                '\u2013': '-',  # en-dash
                                '\u2014': '-',  # em-dash
                                '\u2018': "'",
                                '\u2019': "'",
                                '\u201c': '"',
                                '\u201d': '"',
                            }
                            for k, v in replacements.items():
                                s = s.replace(k, v)
                            try:
                                s.encode('latin-1')
                            except Exception:
                                s = s.encode('latin-1', errors='ignore').decode('latin-1')
                            return s

                        md_link_re = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
                        url_re = re.compile(r"https?://[^\s)\]>]+")

                        # Extract links and replace inline with [n]
                        def extract_and_number_links(raw: str):
                            links = []
                            def replace_md(m):
                                label = m.group(1)
                                url = m.group(2)
                                try:
                                    idx = links.index(url) + 1
                                except ValueError:
                                    links.append(url)
                                    idx = len(links)
                                return f"{label} [{idx}]"

                            text = md_link_re.sub(replace_md, raw)
                            # now replace bare URLs
                            def replace_url(m):
                                url = m.group(0)
                                try:
                                    idx = links.index(url) + 1
                                except ValueError:
                                    links.append(url)
                                    idx = len(links)
                                return f"[{idx}]"

                            text = url_re.sub(replace_url, text)
                            return text, links

                        def count_lines_for_toc(pdf_obj: FPDF, entries_count: int, line_height: float = 6) -> int:
                            avail = pdf_obj.h - pdf_obj.t_margin - pdf_obj.b_margin - 20
                            per_page = max(1, int(avail // line_height))
                            return (entries_count + per_page - 1) // per_page

                        # Rendering routine used in both passes
                        def render_content(pdf_obj: StyledPDF, text: str, record_headings: list = None, line_height: float = 6):
                            in_code = False
                            pdf_obj.set_font('Arial', size=11)
                            for line in text.splitlines():
                                stripped = line.strip()
                                if stripped.startswith('```'):
                                    in_code = not in_code
                                    if in_code:
                                        pdf_obj.set_font('Courier', size=9)
                                        pdf_obj.set_text_color(40, 40, 40)
                                    else:
                                        pdf_obj.set_font('Arial', size=11)
                                        pdf_obj.set_text_color(0, 0, 0)
                                    continue

                                if in_code:
                                    pdf_obj.multi_cell(0, 5, line)
                                    continue

                                if stripped.startswith('## '):
                                    # heading
                                    heading = sanitize_text(stripped[3:].strip())
                                    pdf_obj.ln(2)
                                    pdf_obj.set_font('Arial', 'B', 14)
                                    pdf_obj.cell(0, 7, heading, ln=True)
                                    pdf_obj.ln(1)
                                    pdf_obj.set_font('Arial', size=11)
                                    pdf_obj.set_text_color(0, 0, 0)
                                    pdf_obj.line(pdf_obj.l_margin, pdf_obj.get_y(), pdf_obj.w - pdf_obj.r_margin, pdf_obj.get_y())
                                    pdf_obj.ln(3)
                                    if record_headings is not None:
                                        record_headings.append((heading, pdf_obj.page_no()))
                                elif stripped.startswith('### '):
                                    sub = sanitize_text(stripped[4:].strip())
                                    pdf_obj.set_font('Arial', 'B', 12)
                                    pdf_obj.cell(0, 6, sub, ln=True)
                                    pdf_obj.set_font('Arial', size=11)
                                    pdf_obj.ln(1)
                                elif stripped.startswith('- '):
                                    pdf_obj.set_x(pdf_obj.l_margin + 6)
                                    pdf_obj.multi_cell(0, line_height, sanitize_text(stripped[2:].strip()))
                                elif stripped == '':
                                    pdf_obj.ln(3)
                                else:
                                    pdf_obj.multi_cell(0, line_height, sanitize_text(line))

                        # First, extract links and number them in the content
                        numbered_content, links = extract_and_number_links(content)
                        # incorporate platform-provided URLs (from searches) as well
                        if platform_urls:
                            for u in platform_urls:
                                if u not in links:
                                    links.append(u)

                        # First pass: render content into a temp PDF to record headings and page counts
                        temp = StyledPDF()
                        temp.report_title = title
                        temp.alias_nb_pages()
                        temp.set_auto_page_break(auto=True, margin=15)
                        temp.add_page()
                        headings = []
                        render_content(temp, numbered_content, record_headings=headings, line_height=7)

                        # Determine how many TOC pages we'll need
                        toc_pages = count_lines_for_toc(temp, len(headings), line_height=6)

                        # Final PDF
                        pdf = StyledPDF()
                        pdf.report_title = title
                        pdf.alias_nb_pages()
                        pdf.set_auto_page_break(auto=True, margin=15)

                        # Cover
                        pdf.add_page()
                        pdf.set_font("Arial", "B", 20)
                        pdf.ln(20)
                        pdf.cell(0, 10, title, ln=True, align='C')
                        pdf.ln(6)
                        pdf.set_font("Arial", size=14)
                        pdf.cell(0, 8, f"Topic: {topic}", ln=True, align='C')
                        pdf.ln(4)
                        pdf.set_font("Arial", size=11)
                        pdf.cell(0, 7, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
                        pdf.ln(12)
                        pdf.set_font("Arial", "I", 10)
                        pdf.multi_cell(0, 6, sanitize_text("This comprehensive research report was generated by the Comprehensive Research Agent. The following document contains collected research, technical analysis, and references."))

                        # Table of Contents
                        pdf.add_page()
                        pdf.set_font("Arial", "B", 16)
                        pdf.cell(0, 10, "Table of Contents", ln=True)
                        pdf.ln(4)
                        pdf.set_font("Arial", size=11)
                        # compute page number offset: cover=1 + toc_pages
                        offset = 1 + toc_pages
                        for heading, page_no in headings:
                            display_page = page_no + offset
                            # write TOC line with dotted spacing
                            left = sanitize_text(heading)
                            right = str(display_page)
                            # simple layout: title then page number right-aligned
                            pdf.cell(0, 6, f"{left}", ln=True)

                        # Content (again)
                        pdf.add_page()
                        render_content(pdf, numbered_content, record_headings=None, line_height=7)

                        # References section
                        if links:
                            pdf.add_page()
                            pdf.set_font('Arial', 'B', 14)
                            pdf.cell(0, 8, 'References', ln=True)
                            pdf.ln(4)
                            pdf.set_font('Arial', size=11)
                            for i, url in enumerate(links, start=1):
                                pdf.set_text_color(0, 0, 255)
                                pdf.write(6, f"[{i}] ")
                                pdf.write(6, sanitize_text(url), link=url)
                                pdf.ln(6)
                                pdf.set_text_color(0, 0, 0)

                        pdf_bytes = pdf.output(dest="S")
                        if isinstance(pdf_bytes, str):
                            pdf_bytes = pdf_bytes.encode('latin-1', errors='replace')
                        return pdf_bytes

                        def sanitize_text(s: str) -> str:
                            # Replace common unicode characters that PyFPDF can't encode
                            replacements = {
                                '\u2022': '-',  # bullet
                                '\u2013': '-',  # en-dash
                                '\u2014': '-',  # em-dash
                                '\u2018': "'",
                                '\u2019': "'",
                                '\u201c': '"',
                                '\u201d': '"',
                            }
                            for k, v in replacements.items():
                                s = s.replace(k, v)
                            # Ensure the string can be encoded to latin-1; if not, drop unsupported chars
                            try:
                                s.encode('latin-1')
                            except Exception:
                                s = s.encode('latin-1', errors='ignore').decode('latin-1')
                            return s

                        md_link_re = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
                        url_re = re.compile(r"https?://[^\s)\]>]+")

                        def write_text_with_links(pdf_obj: StyledPDF, text: str, line_height: float = 6):
                            """Write a paragraph using multi_cell for wrapping, then render any links found as separate clickable lines.

                            This guarantees wrapping and clickable links even when inline linking is hard to wrap.
                            """
                            raw = text
                            # find markdown links and replace with label in the paragraph; collect urls
                            links = []
                            def md_repl(m):
                                label = m.group(1)
                                url = m.group(2)
                                links.append((label, url))
                                return label

                            paragraph = md_link_re.sub(md_repl, raw)
                            # find bare URLs too
                            for m in url_re.finditer(paragraph):
                                u = m.group(0)
                                links.append((u, u))

                            paragraph = sanitize_text(paragraph)
                            # print paragraph with wrapping
                            pdf_obj.multi_cell(0, line_height, paragraph)

                            # print links below the paragraph as clickable entries
                            for label, url in links:
                                try:
                                    pdf_obj.set_text_color(0, 0, 255)
                                    pdf_obj.write(line_height, sanitize_text(f"Link: "))
                                    pdf_obj.write(line_height, sanitize_text(label), link=url)
                                    pdf_obj.ln(line_height)
                                finally:
                                    pdf_obj.set_text_color(0, 0, 0)

                        # Cover page
                        pdf.add_page()
                        pdf.set_font("Arial", "B", 20)
                        pdf.ln(20)
                        pdf.cell(0, 10, title, ln=True, align='C')
                        pdf.ln(6)
                        pdf.set_font("Arial", size=14)
                        pdf.cell(0, 8, f"Topic: {topic}", ln=True, align='C')
                        pdf.ln(4)
                        pdf.set_font("Arial", size=11)
                        pdf.cell(0, 7, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
                        pdf.ln(12)
                        pdf.set_font("Arial", "I", 10)
                        pdf.multi_cell(0, 6, sanitize_text("This comprehensive research report was generated by the Comprehensive Research Agent. The following document contains collected research, technical analysis, and references."))

                        # Build simple table of contents (no page numbers)
                        headings = []
                        for raw in content.splitlines():
                            if raw.startswith('## '):
                                headings.append((1, sanitize_text(raw[3:].strip())))
                            elif raw.startswith('### '):
                                headings.append((2, sanitize_text(raw[4:].strip())))

                        if headings:
                            pdf.add_page()
                            pdf.set_font("Arial", "B", 16)
                            pdf.cell(0, 10, "Table of Contents", ln=True)
                            pdf.ln(4)
                            pdf.set_font("Arial", size=11)
                            for level, h in headings:
                                indent = '    ' * (level - 1)
                                pdf.cell(0, 6, f"{indent}- {h}", ln=True)

                        # Content pages
                        pdf.add_page()
                        pdf.set_font("Arial", size=11)

                        in_code_block = False

                        # sanitize content upfront
                        content = sanitize_text(content)

                        for line in content.splitlines():
                            stripped = line.strip()
                            if stripped.startswith('```'):
                                in_code_block = not in_code_block
                                if in_code_block:
                                    pdf.set_font('Courier', size=9)
                                    pdf.set_text_color(40, 40, 40)
                                else:
                                    pdf.set_font('Arial', size=11)
                                    pdf.set_text_color(0, 0, 0)
                                continue

                            if in_code_block:
                                # Render code lines in monospace
                                pdf.multi_cell(0, 5, line)
                                continue

                            if stripped.startswith('## '):
                                # Main section
                                pdf.ln(2)
                                pdf.set_font('Arial', 'B', 14)
                                pdf.cell(0, 7, stripped[3:].strip(), ln=True)
                                pdf.ln(1)
                                pdf.set_font('Arial', size=11)
                                pdf.set_text_color(0, 0, 0)
                                pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
                                pdf.ln(3)
                            elif stripped.startswith('### '):
                                # Subsection
                                pdf.set_font('Arial', 'B', 12)
                                pdf.cell(0, 6, stripped[4:].strip(), ln=True)
                                pdf.set_font('Arial', size=11)
                                pdf.ln(1)
                            elif stripped.startswith('- '):
                                # Bullet list (normalized)
                                bullet = '- '
                                pdf.set_x(pdf.l_margin + 4)
                                write_text_with_links(pdf, f"{bullet}{stripped[2:].strip()}", line_height=6)
                            elif stripped == '':
                                pdf.ln(3)
                            else:
                                # Normal paragraph - write with link handling
                                write_text_with_links(pdf, line, line_height=6)

                        pdf_bytes = pdf.output(dest="S")
                        if isinstance(pdf_bytes, str):
                            pdf_bytes = pdf_bytes.encode('latin-1', errors='replace')
                        return pdf_bytes

                    # pass platform-collected URLs into the PDF generator so References include them
                    platform_urls = []
                    for v in st.session_state.research_results.values():
                        if isinstance(v, dict):
                            platform_urls.extend(v.get('urls', []))
                    # deduplicate while preserving order
                    seen = set(); uniq_platform_urls = []
                    for u in platform_urls:
                        if u not in seen:
                            seen.add(u); uniq_platform_urls.append(u)

                    pdf_bytes = create_pdf_bytes("Comprehensive Research Report", st.session_state.current_topic, st.session_state.comprehensive_report, platform_urls=uniq_platform_urls)
                    st.download_button(
                        label="Download Report (PDF)",
                        data=pdf_bytes,
                        file_name=f"{st.session_state.current_topic.replace(' ', '_')}_research_report.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.warning(f"Could not generate PDF: {e}")
            else:
                st.info("Comprehensive analysis was not generated for this research session.")
        
        else:
            # Display platform-specific results
            platform_name = selected_view
            
            st.markdown(f"# {platform_name} Research Results")
            st.markdown(f"### Topic: *{st.session_state.current_topic}*")
            st.markdown("---")
            
            if platform_name in st.session_state.research_results:
                stored = st.session_state.research_results[platform_name]
                if isinstance(stored, dict):
                    st.markdown(stored.get('text', ''))
                    urls = stored.get('urls', [])
                else:
                    st.markdown(str(stored))
                    urls = []

                if urls:
                    st.markdown('---')
                    st.markdown('**Source URLs:**')
                    for u in urls:
                        st.markdown(f"- [{u}]({u})")
            else:
                st.error(f"No research data found for {platform_name}")

    # Footer
    st.markdown("---")
    
if __name__ == "__main__":
    main()
