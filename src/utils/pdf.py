import streamlit as st
import requests

st.set_page_config(page_title="Gemini Technical Research Agent", layout="centered")
st.title("Gemini Technical Research Agent")

topic = st.text_input("Enter a technical topic (e.g., DMA Attacks)")

GEMINI_API_KEY = "AIzaSyDz0w1AFsub5z8yz660obdjq1HFIDaP1so"  # Replace with your actual Gemini API key

def gemini_report(topic, api_key):
    instructions = (
        "You are an expert technical analyst. Given the topic below, generate a comprehensive technical report with the following sections: "
        "1. Summary. "
        "2. In-depth technical details. "
        "3. Implementation workflow details. "
        "4. Mitigation strategies in extreme technical terms. "
        "5. Tools and how they are used in detail. "
        "6. Key takeaways. "
        "7. References and resources. "
        "Format the output using markdown with clear section headings (e.g., ## Summary, ## Technical Details, etc.). "
        "Be concise, accurate, and ensure each section is easy to read."
    )
    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    prompt = f"{instructions}\nTopic: {topic}"
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": prompt}]}
        ]
    }
    resp = requests.post(f"{endpoint}?key={api_key}", headers=headers, json=payload)
    if resp.status_code == 200:
        try:
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return str(resp.json())
    return f"API Error: {resp.text}"

if st.button("Generate Report"):
    if not topic:
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Generating report..."):
            report = gemini_report(topic, GEMINI_API_KEY)
            st.markdown(report)

st.markdown("---")
st.info("Enter a topic and click 'Generate Report' for a comprehensive technical report powered by Gemini 2.0 Flash.")
