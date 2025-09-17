# Agentic AI

An Agentic AI System that can perform various tasks like fetching information, generating Cypher queries, summarizing logs, images, and videos, and gathering Threat Intelligence.

## Table of Contents

1. [Setup and Installation](#setup-and-installation)
   - [Setting up the Environment](#setting-up-the-environment)
   - [Setting Up API Keys](#setting-up-api-keys)
2. [Downloading the Repository](#downloading-the-repository)
3. [Folder Structure and Organization](#folder-structure-and-organization)
4. [Creating and Working with Agents](#creating-and-working-with-agents)
5. [More Information](#more-information)

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
To get started with Agentic AI, you'll first need to clone this repository or download the zip folder from the dropdown that is available.

## Folder Structure and Organization
In ADK, every agent is organized within its own folder. The system necessitates a single root agent, which is capable of having multiple subordinate agents. Below is a sample file structure:

<img width="350" height="500" alt="image" src="https://github.com/user-attachments/assets/1a39b433-2f7d-4380-aeaa-604dff6f4e1f" />

## Creating and Working with Agents
In an Agentic AI system, agents are the building blocks that allow the system to function autonomously. Each agent is designed to perform specific tasks and can work independently or in conjunction with other agents to achieve complex objectives. Parallel and Sequential Execution: Agents can perform tasks in parallel, making the system efficient and capable of handling multiple requests simultaneously. They can also operate in a sequential manner, where tasks are dependent on the output or completion of preceding tasks. This flexibility allows for tailored workflows depending on the complexity and nature of the job. New agents can be developed under the current root agent, each tailored to handle specific roles. Each root agent requires a .env file where the API key can be provided and can be used for all other sub agents across the system.


