"""
Configuration settings for TalentScout Hiring Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = "llama-3.3-70b-versatile"  # Latest stable model (Dec 2024)
    
    # Application Settings
    APP_TITLE = "TalentScout Hiring Assistant"
    APP_ICON = "🎯"
    COMPANY_NAME = "TalentScout"
    
    # Conversation Settings
    MAX_CONTEXT_LENGTH = 10  # Number of previous messages to maintain
    TEMPERATURE = 0.7  # Balance between creativity and consistency
    MAX_TOKENS = 1024
    
    # Tech Stack Categories (for validation and suggestions)
    TECH_CATEGORIES = {
        "languages": [
            "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", 
            "TypeScript", "Ruby", "PHP", "Swift", "Kotlin", "Scala"
        ],
        "frontend": [
            "React", "Vue.js", "Angular", "Svelte", "Next.js", "Nuxt.js",
            "HTML", "CSS", "Tailwind CSS", "Bootstrap", "Material-UI"
        ],
        "backend": [
            "Node.js", "Django", "Flask", "FastAPI", "Spring Boot", 
            "Express.js", ".NET", "Ruby on Rails", "Laravel"
        ],
        "databases": [
            "PostgreSQL", "MySQL", "MongoDB", "Redis", "Cassandra",
            "SQLite", "Oracle", "DynamoDB", "Elasticsearch"
        ],
        "cloud": [
            "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform",
            "Jenkins", "GitHub Actions", "CircleCI"
        ],
        "ml_ai": [
            "TensorFlow", "PyTorch", "scikit-learn", "Keras", "Pandas",
            "NumPy", "OpenCV", "Hugging Face", "LangChain"
        ],
        "mobile": [
            "React Native", "Flutter", "Swift", "Kotlin", "Ionic"
        ],
        "tools": [
            "Git", "Jira", "Linux", "Postman", "VS Code", "IntelliJ"
        ]
    }
    
    # Exit keywords
    EXIT_KEYWORDS = [
        "exit", "quit", "bye", "goodbye", "end", "stop", 
        "terminate", "close", "leave", "done"
    ]
    
    # Data storage
    DATA_FILE = "data/candidates.json"
    
    # UI Colors
    PRIMARY_COLOR = "#2E86AB"
    SECONDARY_COLOR = "#A23B72"
    SUCCESS_COLOR = "#06D6A0"
    WARNING_COLOR = "#F18F01"
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        return True