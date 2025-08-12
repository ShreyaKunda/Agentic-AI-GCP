# Agentic AI

An Agentic AI System that can perform various tasks like fetching information, generating Cypher queries, and summarizing logs, images, and videos.

## Table of Contents

1. [Setup and Installation](#setup-and-installation)
   - [Setting up the Environment](#setting-up-the-environment)
   - [Setting Up API Keys](#setting-up-api-keys)
2. [Downloading the Repository](#downloading-the-repository)
3. [Folder Structure and Organization](#folder-structure-and-organization)
4. [Creating and Working with Agents
5. [How to Use](#how-to-use)

---

# Setup and Installation

### Setting up the Environment

#### Create virtual environment and activate it
```bash
python -m venv .venv
```
For Linux
```bash
source .venv/bin/activate
```
For Windows and Powershell
```bash
.venv\Scripts\activate.bat
.venv\Scripts\Activate.ps1
```

Install dependencies
```bash
pip install -r requirements.txt
```

### Setting Up API Keys:
a. Create an account in Google Cloud https://cloud.google.com/?hl=en and create a new project.

b. Go to https://aistudio.google.com/apikey and create an API Key.

c. Assign the API key to the project.

d. Navigate to the project folder and create a .env file.

e. Open the .env file and replace the placeholder with your API key:
```bash
GOOGLE_API_KEY=your_api_key_here
```

## Downloading the Repository
To get started with Agentic AI, you'll first need to clone repository by following these steps:
 
```bash
git clone https://github.com/ShreyaKunda/Agentic-AI.git
```

## Folder Structure and Organization
In ADK, every agent is organized within its own folder. The system necessitates a single root agent, which is capable of having multiple subordinate agents. Below is a sample file structure:

<img width="350" height="500" alt="image" src="https://github.com/user-attachments/assets/1a39b433-2f7d-4380-aeaa-604dff6f4e1f" />
