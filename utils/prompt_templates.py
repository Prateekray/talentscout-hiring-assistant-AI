"""
Prompt templates for TalentScout Hiring Assistant
This is the core of our prompt engineering strategy
"""

class PromptTemplates:
    """Collection of carefully engineered prompts"""
    
    # System prompt - This LOCKS the AI into hiring assistant mode
    SYSTEM_PROMPT = """You are the TalentScout Hiring Assistant, an AI recruiter for TalentScout, a leading technology recruitment agency.

YOUR ROLE:
- Conduct initial candidate screening interviews
- Gather essential candidate information professionally
- Ask relevant technical questions based on candidate's tech stack
- Maintain a friendly yet professional tone
- Stay strictly focused on the hiring process

CRITICAL RULES:
1. NEVER deviate from your hiring assistant role
2. NEVER discuss topics unrelated to job screening (politics, personal advice, general questions)
3. NEVER generate inappropriate or off-topic content
4. If asked about non-hiring topics, politely redirect: "I'm here to help with your job application. Let's continue with the screening process."
5. Always maintain context and remember what the candidate has already told you
6. Be encouraging and supportive throughout the interview

CONVERSATION FLOW:
1. Greet and introduce yourself
2. Collect: Name, Email, Phone, Years of Experience, Desired Position, Location
3. Ask about their tech stack
4. Generate 3-5 relevant technical questions per technology
5. Thank them and explain next steps

Be conversational, warm, and professional. Make candidates feel comfortable while gathering quality information."""

    # Greeting prompt (Used as base, language instruction added dynamically in app.py)
    GREETING_PROMPT = """Generate a warm, professional greeting for a candidate starting their screening interview with TalentScout.

Requirements:
- Welcome them to TalentScout
- Briefly explain you'll be gathering their information and asking technical questions
- Be friendly and encouraging
- Keep it concise (2-3 sentences)
- End by asking for their full name

Generate the greeting now:"""

    # Information gathering prompts - NOW MULTILINGUAL
    @staticmethod
    def get_info_prompt(field_name, candidate_data, language="English"):
        """Generate prompt for gathering specific information in the selected language"""
        
        # Translation dictionary for static info-gathering questions
        # This ensures the bot speaks the correct language even during the data collection phase
        translations = {
            "English": {
                "name": "Great! Now, could you please provide your email address?",
                "email": "Thank you! What's the best phone number to reach you?",
                "phone": "Perfect! How many years of professional experience do you have?",
                "experience": "Excellent! What position(s) are you interested in applying for?",
                "position": "Great choice! Where are you currently located? (City, State/Country)",
                "location": """Thank you! Now, let's talk about your technical skills. 

Please list your tech stack - the programming languages, frameworks, databases, and tools you're proficient in. 

For example: "Python, Django, PostgreSQL, Docker, AWS" or "JavaScript, React, Node.js, MongoDB"

What technologies do you work with?"""
            },
            "Hindi": {
                "name": "बहुत बढ़िया! अब, क्या आप कृपया अपना ईमेल पता (email address) बता सकते हैं?",
                "email": "धन्यवाद! आपसे संपर्क करने के लिए सबसे अच्छा फोन नंबर क्या है?",
                "phone": "उत्तम! आपके पास कितने वर्षों का पेशेवर अनुभव (experience) है?",
                "experience": "बढ़िया! आप किस पद (position) के लिए आवेदन करना चाहते हैं?",
                "position": "बहुत अच्छा! आप वर्तमान में कहाँ स्थित हैं? (शहर, राज्य/देश)",
                "location": """धन्यवाद! अब, चलिए आपके तकनीकी कौशल (technical skills) के बारे में बात करते हैं।

कृपया अपना टेक स्टैक (tech stack) बताएं - वे प्रोग्रामिंग भाषाएं, फ्रेमवर्क, डेटाबेस और टूल जिनमें आप कुशल हैं।

उदाहरण के लिए: "Python, Django, PostgreSQL, Docker, AWS" या "JavaScript, React, Node.js, MongoDB"

आप किन तकनीकों के साथ काम करते हैं?"""
            },
            "Spanish": {
                "name": "¡Genial! Ahora, ¿podrías proporcionar tu dirección de correo electrónico?",
                "email": "¡Gracias! ¿Cuál es el mejor número de teléfono para contactarte?",
                "phone": "¡Perfecto! ¿Cuántos años de experiencia profesional tienes?",
                "experience": "¡Excelente! ¿A qué puesto(s) te interesa aplicar?",
                "position": "¡Buena elección! ¿Dónde te encuentras actualmente? (Ciudad, Estado/País)",
                "location": """¡Gracias! Ahora hablemos de tus habilidades técnicas.

Por favor enumera tu tech stack: los lenguajes de programación, frameworks, bases de datos y herramientas que dominas.

Por ejemplo: "Python, Django, PostgreSQL, Docker, AWS" o "JavaScript, React, Node.js, MongoDB"

¿Con qué tecnologías trabajas?"""
            },
            "French": {
                "name": "Super ! Maintenant, pourriez-vous fournir votre adresse e-mail ?",
                "email": "Merci ! Quel est le meilleur numéro de téléphone pour vous joindre ?",
                "phone": "Parfait ! Combien d'années d'expérience professionnelle avez-vous ?",
                "experience": "Excellent ! Pour quel(s) poste(s) souhaitez-vous postuler ?",
                "position": "Très bien ! Où êtes-vous actuellement situé ? (Ville, Pays)",
                "location": """Merci ! Parlons maintenant de vos compétences techniques.

Veuillez énumérer votre stack technique - les langages de programmation, frameworks, bases de données et outils que vous maîtrisez.

Par exemple : "Python, Django, PostgreSQL, Docker, AWS" ou "JavaScript, React, Node.js, MongoDB"

Avec quelles technologies travaillez-vous ?"""
            },
            "German": {
                "name": "Großartig! Könnten Sie bitte Ihre E-Mail-Adresse angeben?",
                "email": "Danke! Unter welcher Telefonnummer können wir Sie am besten erreichen?",
                "phone": "Perfekt! Wie viele Jahre Berufserfahrung haben Sie?",
                "experience": "Ausgezeichnet! Für welche Position(en) möchten Sie sich bewerben?",
                "position": "Gute Wahl! Wo befinden Sie sich derzeit? (Stadt, Land)",
                "location": """Danke! Lassen Sie uns nun über Ihre technischen Fähigkeiten sprechen.

Bitte listen Sie Ihren Tech-Stack auf – die Programmiersprachen, Frameworks, Datenbanken und Tools, die Sie beherrschen.

Zum Beispiel: "Python, Django, PostgreSQL, Docker, AWS" oder "JavaScript, React, Node.js, MongoDB"

Mit welchen Technologien arbeiten Sie?"""
            }
        }

        # Default to English if language not found
        lang_dict = translations.get(language, translations["English"])
        
        return lang_dict.get(field_name, "Please provide the requested information.")
    
    # NEW: Generate individual questions for one-by-one asking
    @staticmethod
    def generate_individual_questions_prompt(tech_stack, experience_years, language="English"):
        """Generate prompt for creating 3-5 individual technical questions"""
        
        difficulty = "beginner to intermediate"
        if experience_years >= 5:
            difficulty = "intermediate to advanced"
        elif experience_years >= 3:
            difficulty = "intermediate"
        
        # Added Language Instruction
        prompt = f"""Generate exactly 3 to 5 technical questions for a candidate with {experience_years} years of experience in: {tech_stack}

IMPORTANT: The candidate speaks {language}. You MUST generate the questions in {language}.

REQUIREMENTS:
- Questions should be {difficulty} level
- Each question should be clear, specific, and standalone
- Mix of conceptual and practical questions
- Avoid yes/no questions
- Each question tests real-world skills

FORMAT (IMPORTANT):
Return ONLY a numbered list. One question per line. No extra text.

Example:
1. [Question 1 in {language}]
2. [Question 2 in {language}]
3. [Question 3 in {language}]

Now generate 3-5 questions in {language}:"""
        
        return prompt
    
    # Technical question generation prompt (KEEP for backward compatibility)
    @staticmethod
    def generate_tech_questions_prompt(tech_stack, experience_years):
        """Generate prompt for creating technical questions"""
        
        difficulty = "beginner to intermediate"
        if experience_years >= 5:
            difficulty = "intermediate to advanced"
        elif experience_years >= 3:
            difficulty = "intermediate"
        
        prompt = f"""You are interviewing a candidate with {experience_years} years of experience who listed the following tech stack:
{tech_stack}

Generate exactly 3-5 relevant technical questions to assess their proficiency. 

REQUIREMENTS:
1. Questions should be {difficulty} level
2. Mix of conceptual, practical, and scenario-based questions
3. Each question should be clear and specific
4. Avoid yes/no questions
5. Questions should assess real-world problem-solving ability
6. Cover different aspects of their tech stack

Format your response EXACTLY like this:

**Technical Assessment Questions:**

1. [Question about technology 1]

2. [Question about technology 2]

3. [Question about technology 3]

4. [Question about technology 4]

5. [Question about technology 5]

Generate the questions now:"""
        
        return prompt
    
    # Fallback handling
    FALLBACK_PROMPT = """The candidate said: "{user_input}"

This seems unclear or off-topic for a hiring interview. Generate a polite response that:
1. Acknowledges their message
2. Gently redirects back to the interview process
3. Asks the next relevant question based on what information we still need

Current interview stage: {stage}
Information collected so far: {collected_info}

Generate your response:"""
    
    # Closing prompt
    @staticmethod
    def get_closing_prompt(candidate_name, language="English"):
        """Generate closing message"""
        
        return f"""Generate a professional closing message for {candidate_name} that:

1. Thanks them for completing the screening interview
2. Mentions that the TalentScout team will review their responses
3. States they'll hear back within 3-5 business days
4. Wishes them well
5. Keeps it warm and encouraging (2-3 sentences)

IMPORTANT: Generate this message in {language}.

Generate the closing message now:"""
    
    # Sentiment-aware response adjustment
    @staticmethod
    def adjust_for_sentiment(sentiment, base_response):
        """Prompt for adjusting response based on sentiment"""
        
        if sentiment == "negative" or sentiment == "very_negative":
            return f"""The candidate seems frustrated or upset. Adjust this response to be more empathetic and supportive:

"{base_response}"

Make it more encouraging and understanding while maintaining professionalism."""
        
        return base_response
    
    # Context-aware response
    @staticmethod
    def context_aware_prompt(user_message, conversation_history, current_stage):
        """Generate context-aware response"""
        
        context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[-6:]])
        
        return f"""CONVERSATION HISTORY:
{context}

CURRENT STAGE: {current_stage}

CANDIDATE'S LATEST MESSAGE: "{user_message}"

Based on the context, generate an appropriate response that:
1. Addresses their message directly
2. Maintains conversation flow
3. Stays focused on the hiring process
4. Moves to the next appropriate step

Your response:"""


class ValidationPrompts:
    """Prompts for input validation"""
    
    @staticmethod
    def validate_email_prompt(email):
        """Check if email looks valid"""
        return f"""Is this a valid email format? "{email}"
        
Respond with only: VALID or INVALID"""
    
    @staticmethod
    def validate_phone_prompt(phone):
        """Check if phone looks valid"""
        return f"""Is this a reasonable phone number format? "{phone}"
        
Respond with only: VALID or INVALID"""
    
    @staticmethod
    def extract_tech_stack_prompt(user_input):
        """Extract technologies from user's message"""
        return f"""Extract all technology names from this message: "{user_input}"

List them separated by commas. Only include actual technology names (languages, frameworks, databases, tools).

If no technologies found, respond with: NONE

Technologies:"""


class PersonalizationPrompts:
    """Prompts for personalized interactions"""
    
    @staticmethod
    def personalize_for_experience(experience_years):
        """Adjust tone based on experience"""
        if experience_years < 2:
            return "Use an encouraging, mentoring tone suitable for junior candidates."
        elif experience_years < 5:
            return "Use a professional, collaborative tone suitable for mid-level candidates."
        else:
            return "Use a respectful, peer-level tone suitable for senior candidates."
    
    @staticmethod
    def personalize_for_role(position):
        """Adjust focus based on desired role"""
        role_lower = position.lower()
        
        if "senior" in role_lower or "lead" in role_lower:
            return "Focus on leadership, architecture, and strategic thinking in questions."
        elif "junior" in role_lower or "entry" in role_lower:
            return "Focus on fundamentals, learning ability, and potential in questions."
        else:
            return "Focus on practical skills and problem-solving ability in questions."