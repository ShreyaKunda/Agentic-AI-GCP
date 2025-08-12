from google.adk.agents import Agent, LlmAgent, ParallelAgent, SequentialAgent 
from google.adk.tools.tool_context import ToolContext
from google.adk.tools import google_search

# --- Existing YouTube Summarizer Agent ---
youtube_summarizer = Agent(
    name="youtube_summarizer",
    model="gemini-2.0-flash",
    description="Finds YouTube playlists/links for a topic and summarizes each one.",
    instruction="""
        You are an assistant that searches YouTube for playlists or links related to a given topic and summarizes each one.

        When a topic is provided:
        1. Use the google search tool to find relevant playlists or video links.
        2. For the top 5 results, summarize each using the video summarizer.
        3. For each result, provide the title, link, and a concise summary of its content and learning objectives.
        4. Ensure the summaries are clear, accurate, and reflect the overall content of the videos.
        5. Include the source link for each video in the summary, along with the video title.
        6. If the video is a playlist, summarize the entire playlist content.
    """,
    tools=[google_search],
    output_key="youtube_results"
)

# --- Reddit Research Agent ---
reddit_agent = LlmAgent(
    name="reddit_agent",
    model="gemini-2.0-flash",
    instruction="""
        You are an assistant that searches Reddit for a given topic and summarizes the top 5 results and their discussions.

        When a topic is provided:
        1. Use the google search tool to search Reddit for the topic.
        2. Retrieve the top 5 relevant posts and their main discussion threads.
        3. Put a heading for each post and its discussion.
        4. Provide a concise summary for each result, making it easy to understand the main takeaways.
        5. Ensure the summaries are clear, accurate, and reflect the overall sentiment and important details from the discussions.
        6. Include the source link for each post in the summary, along with the post title.
    """,
    description="Searches Reddit and summarizes top 5 relevant posts.",
    tools=[google_search],
    output_key="reddit_results"
)

# --- Stack Overflow Research Agent ---
stackoverflow_agent = LlmAgent(
    name="stackoverflow_agent",
    model="gemini-2.0-flash",
    instruction="""
        You are an AI assistant specializing in programming Q&A on Stack Overflow.

        Given the topic, search Stack Overflow using the provided Stack Overflow Search tool.

        Fetch the top 5 relevant questions or answers with their links.

        For each, provide a concise summary of the problem and solution (1-2 sentences).

        Output only the list of 5 links and their summaries in a clear format.
    """,
    description="Searches Stack Overflow and summarizes top 5 relevant Q&A.",
    tools=[google_search],
    output_key="stackoverflow_results"
)

# --- Twitter Research Agent ---
twitter_agent = LlmAgent(
    name="twitter_agent",
    model="gemini-2.0-flash",
    instruction="""
        You are a cybersecurity assistant monitoring Twitter (X) for the latest threat intelligence related to the topic.

        When given a topic:
        1. Use the google search tool to find recent tweets or threads mentioning the topic.
        2. Extract the top 5 tweets, including the handle, timestamp, content snippet, and a link to the tweet.
        3. Summarize the key threat intelligence or opinions expressed in the tweets.
        4. Present each tweet with a heading (handle and date), followed by the summary and source link.
    """,
    description="Searches Twitter for latest relevant threat intelligence tweets.",
    tools=[google_search],
    output_key="twitter_results"
)

# --- GitHub Research Agent ---
github_agent = LlmAgent(
    name="github_agent",
    model="gemini-2.0-flash",
    instruction="""
        You are an assistant that searches GitHub for repositories, issues, and discussions related to cybersecurity topics.

        When given a topic:
        1. Use the google search tool to find relevant GitHub repositories or issues mentioning the topic.
        2. Select the top 5 repositories or issues.
        3. For each, provide the repository or issue title, a brief description, and a link.
        4. Summarize the main points such as vulnerability details, tools, or research findings.
        5. Present each result with a heading (title), summary, and source link.
    """,
    description="Searches GitHub for security-related repos and issues.",
    tools=[google_search],
    output_key="github_results"
)

# --- News Feeds and Security Blogs Agent ---
news_blogs_agent = LlmAgent(
    name="news_blogs_agent",
    model="gemini-2.0-flash",
    instruction="""
        You are an assistant that searches for recent cybersecurity news articles and blog posts.

        When given a topic:
        1. Use the google search tool to find recent news or blog posts related to the topic from trusted security blogs and news sites.
        2. Select the top 5 articles.
        3. For each article, provide the title, source, a concise summary, and a link.
        4. Summarize the key points and insights relevant to cybersecurity.
        5. Present each article with a heading (title), summary, and source link.
    """,
    description="Finds and summarizes cybersecurity news and blog articles.",
    tools=[google_search],
    output_key="news_blogs_results"
)

# --- Government and CERT Websites Agent ---
gov_cert_agent = LlmAgent(
    name="gov_cert_agent",
    model="gemini-2.0-flash",
    instruction="""
        You are an assistant that searches official government and CERT websites for cybersecurity advisories and alerts.

        When given a topic:
        1. Use the google search tool to find recent advisories, alerts, or publications from official CERT, NIST, or government websites related to the topic.
        2. Select the top 5 relevant documents or alerts.
        3. For each, provide the title, issuing authority, a concise summary of the advisory, and a link.
        4. Present each advisory with a heading (title and issuing authority), summary, and source link.
    """,
    description="Searches government and CERT sites for cybersecurity advisories.",
    tools=[google_search],
    output_key="gov_cert_results"
)

# --- Parallel Agent combining all research agents ---
parallel_research_agent = ParallelAgent(
    name="parallel_research_agent",
    sub_agents=[
        youtube_summarizer,
        reddit_agent,
        stackoverflow_agent,
        twitter_agent,
        github_agent,
        news_blogs_agent,
        gov_cert_agent,
    ],
    description="Runs multiple cybersecurity research agents concurrently to gather comprehensive information."
)

# --- Merger Agent to synthesize all results ---
merger_agent = LlmAgent(
    name="research_synthesis_agent",
    model="gemini-2.0-flash",
    instruction="""
        You are an AI assistant tasked with combining research findings from YouTube, Reddit, Stack Overflow, Twitter, GitHub, cybersecurity news/blogs, and government/CERT advisories into a structured report.

        Synthesize the results below, clearly labeling each section.

        Use only the information provided; do not add external info.

        Input Summaries:

        YouTube Results:
        {youtube_results}

        Reddit Results:
        {reddit_results}

        Stack Overflow Results:
        {stackoverflow_results}

        Twitter Results:
        {twitter_results}

        GitHub Results:
        {github_results}

        News and Blogs Results:
        {news_blogs_results}

        Government and CERT Results:
        {gov_cert_results}

        Output format:

        ## Cybersecurity Research Summary on the Topic

        ### YouTube Findings
        [Summarize and integrate the YouTube video summaries]

        ### Reddit Findings
        [Summarize and integrate the Reddit post summaries]

        ### Stack Overflow Findings
        [Summarize and integrate the Stack Overflow Q&A summaries]

        ### Twitter Findings
        [Summarize and integrate the Twitter threat intelligence summaries]

        ### GitHub Findings
        [Summarize and integrate the GitHub repositories and issues summaries]

        ### News and Blogs Findings
        [Summarize and integrate the cybersecurity news and blog article summaries]

        ### Government and CERT Findings
        [Summarize and integrate official advisories and alerts]

        ### Overall Insights
        [Provide a brief overall conclusion based only on above findings]

        Output *only* the structured report in this format.
    """,
    description="Combines findings from all research agents into one coherent report."
)

# --- Sequential Agent to run parallel then merge ---
sequential_pipeline_agent = SequentialAgent(
    name="cybersecurity_research_pipeline",
    sub_agents=[parallel_research_agent, merger_agent],
    description="Runs a comprehensive cybersecurity research pipeline and synthesizes results."
)

# --- Root agent ---
root_agent = sequential_pipeline_agent
