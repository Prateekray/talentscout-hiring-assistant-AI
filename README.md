# 🎯 TalentScout Hiring Assistant

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/yourusername/talentscout-hiring-assistant)
[![Live Demo](https://img.shields.io/badge/Live-Demo-green)](https://talentscout-hiring-assistant-ai-id2fnzq8nkrygh75hlbklo.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B.svg)](https://streamlit.io)

An AI-powered chatbot for conducting initial candidate screenings with technical assessments.

---

## 🎥 Demo Links

- **🎬 Video Walkthrough:** [Watch on Loom](https://www.loom.com/share/f85506313c254275906a03456d6ed224)
- **🚀 Live Application:** [Try it on Streamlit Cloud](https://talentscout-hiring-assistant-ai-id2fnzq8nkrygh75hlbklo.streamlit.app/)
- **💻 Source Code:** [GitHub Repository](https://github.com/Prateekray/talentscout-hiring-assistant-AI)

---

## 📋 Project Overview

TalentScout Hiring Assistant conducts intelligent candidate screenings by:
- Collecting candidate information (Name, Email, Phone, Experience, Position, Location, Tech Stack)
- Generating tailored technical questions based on declared technologies
- Analyzing sentiment to adjust responses appropriately
- Maintaining conversation context throughout the interview

**Technology:** Python, Streamlit, Groq AI (Llama 3.3), TextBlob for sentiment analysis

---

## 🚀 Installation

### Prerequisites
- Python 3.10+
- Groq API key ([Get free key](https://console.groq.com))

### Setup Steps
```bash
# 1. Clone repository
git clone https://github.com/yourusername/talentscout-hiring-assistant.git
cd talentscout-hiring-assistant

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
python -m textblob.download_corpora

# 4. Create .env file with your API key
echo "GROQ_API_KEY=your_key_here" > .env

# 5. Run application
streamlit run app.py
```

Application opens at `http://localhost:8501`

---

## 📖 Usage

1. **Start Interview:** Bot greets automatically
2. **Provide Information:** Answer each question clearly
3. **Tech Stack:** List technologies (e.g., "Python, Django, PostgreSQL")
4. **Technical Questions:** Bot generates 3-5 tailored questions
5. **Exit:** Type `exit`, `quit`, `bye`, or similar keywords

---

## 🔧 Technical Details

**Architecture:**
```
User Input → Validation → Sentiment Analysis → Prompt Engineering → 
Groq AI → Response → Context Update → Display
```

**Tech Stack:**
- **AI Model:** Groq Llama 3.3-70b-versatile
- **Frontend:** Streamlit 1.31.0
- **Sentiment:** TextBlob 0.17.1
- **Data:** JSON storage with Pandas export

**Configuration** (`config.py`):
- Model: `llama-3.3-70b-versatile`
- Temperature: `0.7` (balanced creativity)
- Context: Last 10 messages maintained

**File Structure:**
```
├── app.py                     # Main application
├── config.py                  # Settings
├── utils/
│   ├── groq_client.py        # AI API wrapper
│   ├── prompt_templates.py   # Prompt engineering
│   ├── sentiment_analyzer.py # Emotion detection
│   ├── data_handler.py       # Data storage
│   └── validators.py         # Input validation
├── data/
│   └── candidates.json       # Stored data
└── README.md
```

---

## 🧠 Prompt Engineering

**System Prompt Strategy:**
- Strong role definition locks AI to hiring tasks
- Explicit "NEVER" rules prevent off-topic responses
- Clear conversation flow guides interview stages

**Technical Question Generation:**
```python
# Dynamic difficulty based on experience
if experience >= 5: difficulty = "advanced"
elif experience >= 3: difficulty = "intermediate"  
else: difficulty = "beginner"

# Prompt includes: tech stack, experience, difficulty level
# Output: 3-5 tailored questions covering different aspects
```

**Key Techniques:**
1. **Context Injection:** Include candidate data in prompts
2. **Constraint Setting:** Define output format and restrictions
3. **Sentiment Adaptation:** Adjust tone based on emotions
4. **Fallback Handling:** Redirect off-topic conversations
5. **Temperature Tuning:** 0.7 for consistent yet natural responses

---

## 💡 Challenges & Solutions

### Challenge 1: Maintaining Context
**Problem:** AI forgetting previous information  
**Solution:** Implemented `ConversationManager` maintaining last 10 messages in every API call

### Challenge 2: Off-Topic Responses
**Problem:** Users asking non-hiring questions  
**Solution:** Strong system prompt with explicit boundaries + fallback detection

### Challenge 3: Generic Questions
**Problem:** Technical questions not matching tech stack/experience  
**Solution:** Dynamic prompt construction with experience-based difficulty adjustment

### Challenge 4: Invalid Inputs
**Problem:** Users entering bad data formats  
**Solution:** Comprehensive validation with helpful error messages for each field type

### Challenge 5: Sentiment Detection
**Problem:** TextBlob missing nuanced emotions  
**Solution:** Hybrid approach combining polarity analysis with keyword-based emotion detection (85% accuracy)

### Challenge 6: Response Speed
**Problem:** 5-8 second delays  
**Solution:** Switched to Groq (4x faster), optimized prompts, limited context window (<2 sec average)

---

## ✨ Features Implemented

**Core Requirements:**
- ✅ Information gathering with validation
- ✅ Tech stack declaration
- ✅ Dynamic technical question generation
- ✅ Context-aware conversations
- ✅ Fallback mechanisms
- ✅ Exit command handling

**Bonus Features:**
- ✅ Sentiment analysis with response adaptation
- ✅ Custom UI with gradient design
- ✅ Progress tracking
- ✅ Data export (JSON, CSV, TXT)
- ✅ Real-time statistics
- ✅ Multilingual foundation (langdetect)
- ✅ Performance optimization

---

## 📄 License

MIT License

---

## 👨‍💻 Author

**[Prateek Ray]**
- GitHub: https://github.com/Prateekray
- LinkedIn: https://www.linkedin.com/in/prateek-ray-812474204/
- Email: prateekray534@gmail.com

---

<div align="center">

**Built for AI/ML Internship Assignment**

⭐ Star this repo if you found it helpful!

</div>