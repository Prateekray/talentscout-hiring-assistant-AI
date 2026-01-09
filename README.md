# 🎯 TalentScout Hiring Assistant AI

![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Llama3-orange?style=for-the-badge)
![TextBlob](https://img.shields.io/badge/TextBlob-Sentiment-green?style=for-the-badge)

**TalentScout** is an intelligent AI-powered recruitment chatbot designed to streamline initial candidate screenings. Built on the **Groq LPU inference engine**, it conducts real-time technical interviews, validates candidate data, and analyzes sentiment to provide a comprehensive profile for recruiters.

---

## 🎥 Live Demo

**[Link to Streamlit App](https://talentscout-hiring-assistant-ai-id2fnzq8nkrygh75hlbklo.streamlit.app/)**
*(Optional: Add Loom Video Link Here)*

---

## 📋 Project Overview

### Purpose
To automate the initial screening phase of recruitment by intelligently gathering candidate details and generating tailored technical assessments based on the candidate's specific tech stack.

### ✨ Key Capabilities
* **🗣️ Context-Aware Conversation:** Remembers previous exchanges to maintain a natural flow using a rolling context window.
* **🛡️ Robust Input Validation:** Real-time validation for Email, Phone, and Experience inputs with helpful error feedback.
* **🧠 Adaptive Technical Testing:** Generates 3-5 conceptual and scenario-based questions tailored to the candidate's experience level (e.g., Junior vs. Senior).
* **❤️ Sentiment Analysis:** Uses **TextBlob** and keyword detection to analyze candidate confidence and frustration, adjusting the AI's tone dynamically.
* **📊 Data & Analytics:** Exports interview transcripts and saves candidate profiles to JSON/CSV for recruiter review.

---

## 🛠️ Technical Architecture

The application follows a modular architecture separating UI, Logic, and Data.

```mermaid
graph TD
    A[User Input] --> B[Input Validator]
    B --> C{Validation Pass?}
    C -- No --> D[Error Feedback]
    C -- Yes --> E[Sentiment Analyzer]
    E --> F[Prompt Engineer]
    F --> G[Groq API Client]
    G --> H[Llama 3.1-70b]
    H --> I[Context Manager]
    I --> J[Streamlit UI]
    J --> K[Data Handler / JSON Storage]
Technology StackComponentTechnologyPurposeLLM EngineGroq (Llama 3.1-70b)Ultra-low latency inference (<2s responses)FrontendStreamlit v1.31.0Interactive Chat UI and State ManagementNLPTextBlobSentiment Polarity & Subjectivity AnalysisValidationRegex & PythonData integrity for candidate detailsStorageJSON/PandasAtomic data persistence and CSV export🚀 Installation & SetupPrerequisitesPython 3.10+Groq API Key1. Clone the RepositoryBashgit clone [https://github.com/Prateekray/talentscout-hiring-assistant-AI.git](https://github.com/Prateekray/talentscout-hiring-assistant-AI.git)
cd talentscout-hiring-assistant-AI
2. Create Virtual EnvironmentBash# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
3. Install DependenciesBashpip install -r requirements.txt
4. Download NLP CorporaRequired for TextBlob to function correctly:Bashpython -m textblob.download_corpora
5. ConfigurationCreate a .env file in the root directory:Code snippetGROQ_API_KEY=your_actual_api_key_here
6. Run the AppBashstreamlit run app.py
🧠 Prompt Design StrategyWe utilized Persona-Based Prompting and Chain-of-Thought reasoning to ensure high-quality outputs.1. System Role Definition"You are the TalentScout Hiring Assistant... NEVER deviate from your hiring assistant role. NEVER discuss topics unrelated to job screening."2. Dynamic Question GenerationWe inject the candidate's specific context into the prompt to prevent generic questions.Pythonprompt = f"""
Generate 3-5 {difficulty} level questions for a candidate with 
{years} years of experience in {tech_stack}.
Constraints: No yes/no questions. Focus on real-world scenarios.
"""
3. Sentiment AdjustmentThe AI's response is post-processed based on sentiment scores. If a candidate is detected as "Frustrated", the system injects an instruction to "be more empathetic and encouraging" into the next prompt.💡 Challenges & SolutionsChallenge 1: Maintaining ContextProblem: The AI would "forget" the candidate's name or tech stack after a few turns.Solution: Implemented a ConversationManager class that maintains a rolling window of the last 10 messages and injects them into every API call, ensuring 100% context retention.Challenge 2: Handling Off-Topic InputsProblem: Users could distract the bot with questions like "What is the weather?"Solution: Added a "Fallback Logic" layer. If the input doesn't match the expected interview context, the system triggers a polite redirection prompt instead of answering the query.Challenge 3: NLTK/TextBlob Deployment ErrorsProblem: Streamlit Cloud crashed with Resource punkt not found.Solution: Added a runtime check in app.py to download tokenizer data programmatically on startup:Pythontry:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
Challenge 4: Data ConsistencyProblem: Concurrent users risked overwriting data in a simple JSON file.Solution: Implemented atomic writes and unique ID generation (Timestamp + Random) for every candidate profile to prevent conflicts.📂 Project StructurePlaintexttalentscout/
├── app.py                 # Main application entry point
├── requirements.txt       # Dependencies
├── .env                   # API Keys (Excluded from Git)
├── utils/
│   ├── groq_client.py     # API communication layer
│   ├── prompts.py         # Prompt templates
│   ├── sentiment.py       # TextBlob analysis logic
│   └── validators.py      # Input regex patterns
├── data/
│   └── candidates.json    # Local storage
└── assets/
    └── styles.css         # Custom UI styling