"""
TalentScout Hiring Assistant
AI-powered recruitment chatbot for initial candidate screening
"""
import streamlit as st
import time
from datetime import datetime
import re
import streamlit.components.v1 as components
import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    
# Import our custom modules
from config import Config
from utils.groq_client import GroqClient, ConversationManager
from utils.prompt_templates import PromptTemplates
from utils.sentiment_analyzer import SentimentAnalyzer
from utils.data_handler import DataHandler, ConversationExporter
from utils.validators import InputValidator

# Page configuration
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon=Config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    """Load custom CSS styling"""
    st.markdown("""
    <style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* CRITICAL: Chat message text color fix */
    .stChatMessage[data-testid="assistant-message"],
    .stChatMessage[data-testid="assistant-message"] *,
    .stChatMessage[data-testid="assistant-message"] p,
    .stChatMessage[data-testid="assistant-message"] div,
    .stChatMessage[data-testid="assistant-message"] span,
    .stChatMessage[data-testid="assistant-message"] strong,
    .stChatMessage[data-testid="assistant-message"] em,
    .stChatMessage[data-testid="assistant-message"] .stMarkdown,
    .stChatMessage[data-testid="assistant-message"] .stMarkdown * {
        color: #000000 !important;
        background: transparent !important;
    }
    
    /* Assistant message background */
    .stChatMessage[data-testid="assistant-message"] {
        background-color: white !important;
        background: white !important;
        border-left: 4px solid #667eea !important;
    }
    
    /* User message */
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    .stChatMessage[data-testid="user-message"] p,
    .stChatMessage[data-testid="user-message"] div,
    .stChatMessage[data-testid="user-message"] span {
        color: white !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        padding: 10px 30px !important;
        font-weight: bold !important;
        transition: all 0.3s !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.messages = []
        st.session_state.candidate_data = {}
        st.session_state.current_stage = 'greeting'
        st.session_state.awaiting_field = None
        st.session_state.groq_client = None
        st.session_state.conversation_manager = None
        st.session_state.sentiment_analyzer = SentimentAnalyzer()
        st.session_state.data_handler = DataHandler(Config.DATA_FILE)
        st.session_state.tech_questions_asked = False
        st.session_state.conversation_complete = False
        st.session_state.sentiment_history = []
        st.session_state.language = "English"
        
        # NEW: For one-by-one questions
        st.session_state.technical_questions = []
        st.session_state.current_question_index = 0
        st.session_state.technical_answers = []
        
        # Initialize AI client
        try:
            st.session_state.groq_client = GroqClient()
            st.session_state.conversation_manager = ConversationManager(
                PromptTemplates.SYSTEM_PROMPT,
                Config.MAX_CONTEXT_LENGTH
            )
        except Exception as e:
            st.error(f"⚠️ Failed to initialize AI client: {str(e)}")
            st.stop()

def get_interview_progress():
    """Calculate interview progress percentage"""
    required_fields = ['name', 'email', 'phone', 'experience', 'position', 'location', 'tech_stack']
    completed = sum(1 for field in required_fields if field in st.session_state.candidate_data)
    
    if st.session_state.tech_questions_asked:
        completed += 1
        required_fields.append('technical_assessment')
    
    return (completed / len(required_fields)) * 100

def display_progress():
    """Display interview progress"""
    progress = get_interview_progress()
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.progress(progress / 100)
    with col2:
        st.metric("Progress", f"{int(progress)}%")
    with col3:
        stage_emoji = {
            'greeting': '👋',
            'info_gathering': '📝',
            'tech_stack': '💻',
            'technical_questions': '🎯',
            'closing': '✅'
        }
        st.metric("Stage", stage_emoji.get(st.session_state.current_stage, '📋'))

def get_bot_response(user_message):
    """Generate bot response using AI"""
    try:
        # Check for exit command
        if InputValidator.is_exit_command(user_message):
            return handle_exit()
        
        # Analyze sentiment
        sentiment = st.session_state.sentiment_analyzer.analyze_sentiment(user_message)
        st.session_state.sentiment_history.append(sentiment)
        
        # Add user message to conversation
        st.session_state.conversation_manager.add_message('user', user_message)
        
        # Generate response based on current stage
        if st.session_state.current_stage == 'greeting':
            response = generate_greeting()
            st.session_state.current_stage = 'info_gathering'
            st.session_state.awaiting_field = 'name'
        
        elif st.session_state.current_stage == 'info_gathering':
            response = handle_info_gathering(user_message)
        
        elif st.session_state.current_stage == 'tech_stack':
            response = handle_tech_stack(user_message)
        
        elif st.session_state.current_stage == 'technical_questions':
            response = handle_technical_questions(user_message)
        
        elif st.session_state.current_stage == 'closing':
            response = generate_closing()
            st.session_state.conversation_complete = True
        
        else:
            response = "I'm here to help with your application. Let's continue!"
        
        # Adjust response for sentiment if needed
        if sentiment['needs_support']:
            response = st.session_state.sentiment_analyzer.adjust_response_tone(response, sentiment)
        
        # Add bot response to conversation
        st.session_state.conversation_manager.add_message('assistant', response)
        
        return response
        
    except Exception as e:
        return f"I apologize, but I encountered an issue. Could you please repeat that? Error: {str(e)}"

def generate_greeting():
    """Generate initial greeting"""
    try:
        messages = st.session_state.conversation_manager.get_messages_for_api()
        language = st.session_state.get('language', 'English')
        greeting_prompt = f"{PromptTemplates.GREETING_PROMPT}\nIMPORTANT: Please generate this greeting in {language} language."
        
        messages.append({'role': 'user', 'content': greeting_prompt})
        response = st.session_state.groq_client.generate_response(messages)

        if not response or response.strip() == "":
            return "Hello! Welcome to TalentScout. I'm your AI hiring assistant. To get started, could you please tell me your full name?"

        return response
    except Exception as e:
        return "Hello! Welcome to TalentScout. I'm your AI hiring assistant. To get started, could you please tell me your full name?"


def handle_info_gathering(user_message):
    """Handle information gathering stage"""
    field = st.session_state.awaiting_field
    language = st.session_state.get('language', 'English')
    
    if field == 'name':
        is_valid, error = InputValidator.validate_name(user_message)
        if is_valid:
            st.session_state.candidate_data['name'] = user_message.strip()
            st.session_state.awaiting_field = 'email'
            return PromptTemplates.get_info_prompt('name', st.session_state.candidate_data, language)
        else:
            # --- FIX: Polite Greeting Handling ---
            if "greeting" in error.lower():
                # If the validator detected a greeting, reply politely but stay on the name step
                if language == "Hindi":
                    return "नमस्ते! आपसे मिलकर खुशी हुई। कृपया आवेदन शुरू करने के लिए अपना पूरा नाम बताएं?"
                elif language == "Spanish":
                    return "¡Hola! Encantado de conocerte. ¿Podrías escribir tu nombre completo para comenzar?"
                else:
                    return "Hello! It's great to connect with you. Could you please provide your full name to get started?"
            
            # For other errors (too short, numbers, etc.), show the standard error
            return f"I'm sorry, but {error}. Could you please provide your full name?"
    
    elif field == 'email':
        is_valid, error = InputValidator.validate_email(user_message)
        if is_valid:
            st.session_state.candidate_data['email'] = user_message.strip()
            st.session_state.awaiting_field = 'phone'
            return PromptTemplates.get_info_prompt('email', st.session_state.candidate_data, language)
        else:
            return f"{error}. Please try again."
    
    elif field == 'phone':
        is_valid, error = InputValidator.validate_phone(user_message)
        if is_valid:
            st.session_state.candidate_data['phone'] = user_message.strip()
            st.session_state.awaiting_field = 'experience'
            return PromptTemplates.get_info_prompt('phone', st.session_state.candidate_data, language)
        else:
            return f"{error}. Please provide a valid phone number."
    
    elif field == 'experience':
        is_valid, years, error = InputValidator.validate_experience(user_message)
        if is_valid:
            st.session_state.candidate_data['experience'] = years
            st.session_state.awaiting_field = 'position'
            return PromptTemplates.get_info_prompt('experience', st.session_state.candidate_data, language)
        else:
            return f"{error}. How many years of experience do you have?"
    
    elif field == 'position':
        is_valid, error = InputValidator.validate_position(user_message)
        if is_valid:
            st.session_state.candidate_data['position'] = user_message.strip()
            st.session_state.awaiting_field = 'location'
            return PromptTemplates.get_info_prompt('position', st.session_state.candidate_data, language)
        else:
            return f"{error}. What position are you applying for?"
    
    elif field == 'location':
        is_valid, error = InputValidator.validate_location(user_message)
        if is_valid:
            st.session_state.candidate_data['location'] = user_message.strip()
            st.session_state.current_stage = 'tech_stack'
            st.session_state.awaiting_field = None
            return PromptTemplates.get_info_prompt('location', st.session_state.candidate_data, language)
        else:
            return f"{error}. Where are you currently located?"
    
    return "Could you please provide that information again?"

def handle_tech_stack(user_message):
    """Handle tech stack input and generate questions"""
    is_valid, cleaned_tech, suggestions, error = InputValidator.validate_tech_stack(user_message)
    language = st.session_state.get('language', 'English')
    
    if is_valid:
        st.session_state.candidate_data['tech_stack'] = ', '.join(cleaned_tech)
        prompt = PromptTemplates.generate_individual_questions_prompt(
            st.session_state.candidate_data['tech_stack'],
            st.session_state.candidate_data['experience'],
            language
        )
        messages = [
            {'role': 'system', 'content': PromptTemplates.SYSTEM_PROMPT},
            {'role': 'user', 'content': prompt}
        ]
        questions_text = st.session_state.groq_client.generate_response(messages)
        questions = re.findall(r'\d+\.\s*(.+?)(?=\n\d+\.|\Z)', questions_text, re.DOTALL)
        questions = [q.strip() for q in questions if q.strip()]
        
        if questions and len(questions) >= 3:
            st.session_state.technical_questions = questions[:5]
            st.session_state.current_question_index = 0
            st.session_state.current_stage = 'technical_questions'
            total = len(st.session_state.technical_questions)
            return f"Great! I can see you work with {st.session_state.candidate_data['tech_stack']}. Let me ask you some technical questions to assess your skills.\n\n**Question 1 of {total}:**\n\n{st.session_state.technical_questions[0]}"
        else:
            st.session_state.current_stage = 'technical_questions'
            st.session_state.tech_questions_asked = True
            return f"Great! I can see you work with {st.session_state.candidate_data['tech_stack']}. Can you tell me about your experience with the main technologies you listed?"
    else:
        return f"{error} Please list the technologies you're proficient in."

def handle_technical_questions(user_message):
    """Handle technical question responses"""
    st.session_state.technical_answers.append({
        'question': st.session_state.technical_questions[st.session_state.current_question_index],
        'answer': user_message
    })
    st.session_state.current_question_index += 1
    if st.session_state.current_question_index < len(st.session_state.technical_questions):
        next_num = st.session_state.current_question_index + 1
        total = len(st.session_state.technical_questions)
        next_q = st.session_state.technical_questions[st.session_state.current_question_index]
        return f"Thank you for your answer!\n\n**Question {next_num} of {total}:**\n\n{next_q}"
    else:
        st.session_state.candidate_data['technical_responses'] = st.session_state.technical_answers
        st.session_state.tech_questions_asked = True
        st.session_state.current_stage = 'closing'
        return "Thank you for your detailed responses to all the technical questions! Let me wrap up our interview."

def generate_closing():
    """Generate closing message"""
    language = st.session_state.get('language', 'English')
    prompt = PromptTemplates.get_closing_prompt(
        st.session_state.candidate_data.get('name', 'candidate'),
        language
    )
    messages = [
        {'role': 'system', 'content': PromptTemplates.SYSTEM_PROMPT},
        {'role': 'user', 'content': prompt}
    ]
    closing = st.session_state.groq_client.generate_response(messages)
    st.session_state.candidate_data['conversation_history'] = st.session_state.conversation_manager.get_history()
    st.session_state.candidate_data['sentiment_summary'] = st.session_state.sentiment_analyzer.get_emotion_summary()
    st.session_state.data_handler.save_candidate(st.session_state.candidate_data)
    return closing

def handle_exit():
    """Handle exit command"""
    st.session_state.current_stage = 'closing'
    return "I understand you'd like to end our conversation. Thank you for your time! If you'd like to continue your application later, please feel free to return."

def display_sidebar():
    """Display sidebar with information and controls"""
    with st.sidebar:
        st.title(f"{Config.APP_ICON} {Config.COMPANY_NAME}")
        st.markdown("---")
        st.subheader("🌐 Language")
        language_options = ["English", "Hindi", "Spanish", "French", "German"]
        selected_language = st.selectbox("Choose Interface Language", language_options, index=0)
        st.session_state.language = selected_language
        st.markdown("---")
        
        if st.session_state.candidate_data:
            st.subheader("📋 Your Information")
            for key, value in st.session_state.candidate_data.items():
                if key not in ['conversation_history', 'technical_responses', 'sentiment_summary', 'timestamp', 'candidate_id']:
                    display_key = key.replace('_', ' ').title()
                    st.text(f"{display_key}: {value}")
        
        st.markdown("---")
        if st.session_state.sentiment_history:
            st.subheader("😊 Conversation Mood")
            latest_sentiment = st.session_state.sentiment_history[-1]
            sentiment_emoji = {'positive': '😊', 'slightly_positive': '🙂', 'neutral': '😐', 'slightly_negative': '😕', 'negative': '😟', 'uncertain': '🤔'}
            st.write(f"{sentiment_emoji.get(latest_sentiment['sentiment'], '😐')} {latest_sentiment['sentiment'].replace('_', ' ').title()}")
        
        st.markdown("---")
        st.subheader("🛠️ Controls")
        if st.button("🔄 Start New Interview"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        if st.button("💾 Export Transcript") and st.session_state.messages:
            filename = ConversationExporter.export_conversation(st.session_state.messages, st.session_state.candidate_data)
            if filename:
                st.success(f"✅ Exported to {filename}")
        
        st.markdown("---")
        st.subheader("📊 Statistics")
        stats = st.session_state.data_handler.get_statistics()
        st.metric("Total Candidates", stats['total_candidates'])
        st.metric("Avg Experience", f"{stats['avg_experience']} years")
        
        st.markdown("---")
        with st.expander("❓ Help"):
            st.write("""**How to use:**\n1. Answer questions honestly\n2. Provide accurate information\n3. Take your time with technical questions\n4. Type 'exit' to end anytime""")

def scroll_to_bottom():
    """Forces the page to scroll to the bottom"""
    js = """
    <script>
    function scrollToBottom() {
        const elements = window.parent.document.querySelectorAll('.stApp');
        if (elements.length > 0) {
            const main = elements[0];
            main.scrollTop = main.scrollHeight;
        }
    }
    scrollToBottom();
    setTimeout(scrollToBottom, 100);
    setTimeout(scrollToBottom, 500);
    </script>
    """
    components.html(js, height=0, width=0)

def main():
    """Main application"""
    load_css()
    init_session_state()
    display_sidebar()
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col2:
        st.title(f"{Config.APP_ICON} {Config.APP_TITLE}")
        st.markdown("**AI-Powered Initial Candidate Screening**")
        
        if not st.session_state.conversation_complete:
            display_progress()
        
        st.markdown("---")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if st.session_state.conversation_complete:
            st.success("✅ Interview Complete! Thank you for your time.")
            st.balloons()
            if st.button("Start Another Interview"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        elif not st.session_state.messages:
            with st.chat_message("assistant"):
                greeting = generate_greeting()
                st.markdown(greeting)
            st.session_state.messages.append({"role": "assistant", "content": greeting})
            st.session_state.current_stage = 'info_gathering'
            st.session_state.awaiting_field = 'name'
            st.rerun()
        else:
            if prompt := st.chat_input("Type your response here..."):
                with st.chat_message("user"):
                    st.markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = get_bot_response(prompt)
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        if st.session_state.conversation_complete:
                            with st.spinner("💾 Auto-saving transcript to GitHub..."):
                                try:
                                    ConversationExporter.export_conversation(st.session_state.messages, st.session_state.candidate_data)
                                except Exception as e:
                                    st.error(f"Auto-save failed: {e}")
                st.rerun()
    scroll_to_bottom()

if __name__ == "__main__":
    main()