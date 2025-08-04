from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
import requests

def article_summarizer(url: str, tool_context: ToolContext) -> dict:
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove all script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get the text from the HTML content
        text = soup.get_text()

        # Break the text into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())

        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

        # Remove special characters and digits
        text = ' '.join(chunk for chunk in chunks if chunk)

        # Tokenize the text into sentences
        sentences = sent_tokenize(text)

        # Remove stopwords and stem the words
        stop_words = set(stopwords.words('english'))
        stemmer = PorterStemmer()
        stemmed_sentences = []
        for sentence in sentences:
            words = word_tokenize(sentence)
            stemmed_words = [stemmer.stem(word) for word in words if word.lower() not in stop_words]
            stemmed_sentences.append(' '.join(stemmed_words))

        # Calculate the frequency of each word
        word_freq = {}
        for sentence in stemmed_sentences:
            words = sentence.split()
            for word in words:
                if word not in word_freq:
                    word_freq[word] = 1
                else:
                    word_freq[word] += 1

        # Rank the sentences based on the frequency of their words
        ranked_sentences = []
        for sentence in stemmed_sentences:
            words = sentence.split()
            score = sum(word_freq[word] for word in words)
            ranked_sentences.append((sentence, score))

        # Sort the sentences based on their score
        ranked_sentences.sort(key=lambda x: x[1], reverse=True)

        # Select the top 5 sentences as the summary
        summary = []
        for sentence, score in ranked_sentences[:5]:
            summary.append(sentence)

        # Join the summary sentences into a single string
        summary_text = ' '.join(summary)

        return {"status": "success", "summary": summary_text, "url": url}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Create the Article Summarizer Agent
article_summarizer = Agent(
    name="article_summarizer",
    model="gemini-2.0-flash",
    description="An agent that summarizes articles or blog posts.",
    instruction=""" 
You are an agent that summarizes articles or blog posts. Given a URL, you should:
1. Read the article carefully.
2. Provide a summary in 10-15 lines with all the key points highlighted.

""",
    tools=[article_summarizer],
)
