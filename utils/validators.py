"""
Input Validators for TalentScout Hiring Assistant
Validates user inputs for data quality
"""
import re
from config import Config

class InputValidator:
    """Validates various types of user inputs"""
    
    @staticmethod
    def validate_email(email):
        """
        Validate email format
        
        Args:
            email: Email string to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not email or len(email.strip()) == 0:
            return False, "Email cannot be empty"
        
        email = email.strip()
        
        # Basic email regex pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            return False, "Please enter a valid email format (e.g., name@example.com)"
        
        # Additional checks
        if email.count('@') != 1:
            return False, "Email must contain exactly one @ symbol"
        
        if len(email) > 254:
            return False, "Email is too long"
        
        return True, None
    
    @staticmethod
    def validate_phone(phone):
        """
        Validate phone number format
        
        Args:
            phone: Phone number string
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not phone or len(phone.strip()) == 0:
            return False, "Phone number cannot be empty"
        
        phone = phone.strip()
        
        # Remove common formatting characters
        cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
        
        # Check if it contains only digits (after removing formatting)
        if not cleaned.isdigit():
            return False, "Phone number should contain only digits and formatting characters"
        
        # Check length (most phone numbers are 7-15 digits)
        if len(cleaned) < 7 or len(cleaned) > 15:
            return False, "Phone number should be between 7 and 15 digits"
        
        return True, None
    
    @staticmethod
    def validate_experience(experience):
        """
        Validate years of experience
        
        Args:
            experience: Experience string or number
            
        Returns:
            tuple: (is_valid, cleaned_value, error_message)
        """
        if not experience:
            return False, None, "Years of experience cannot be empty"
        
        experience_str = str(experience).strip()
        
        # Try to extract number from string
        numbers = re.findall(r'\d+\.?\d*', experience_str)
        
        if not numbers:
            return False, None, "Please enter a valid number of years (e.g., 3 or 3.5)"
        
        try:
            years = float(numbers[0])
            
            if years < 0:
                return False, None, "Years of experience cannot be negative"
            
            if years > 50:
                return False, None, "Please enter a realistic number of years (0-50)"
            
            return True, years, None
            
        except ValueError:
            return False, None, "Please enter a valid number"
    
    @staticmethod
    def validate_name(name):
        """
        Validate name - FIXED to reject greetings
        
        Args:
            name: Name string
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not name or len(name.strip()) == 0:
            return False, "Name cannot be empty"
        
        name = name.strip()
        
        # --- NEW: Check for common greetings ---
        # This prevents the bot from accepting "Hi", "Hello", etc. as a name
        common_greetings = {
            'hi', 'hello', 'hey', 'greetings', 'good morning', 
            'good afternoon', 'good evening', 'yo', 'sup', 'hola', 
            'namaste', 'bonjour', 'hallo', 'hii', 'heyy'
        }
        
        # Check if the input is JUST a greeting (case insensitive)
        if name.lower() in common_greetings:
            return False, "Please provide your full name, not just a greeting."
        
        # Also check if it looks like "Hi I am..." but is too short to be a full sentence
        # (This is optional but helpful, kept simple for now)
        
        # --- EXISTING CHECKS ---
        
        if len(name) < 2:
            return False, "Name must be at least 2 characters"
        
        if len(name) > 100:
            return False, "Name is too long"
        
        # Check for reasonable characters (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-Z\s\-'\.]+$", name):
            return False, "Name should contain only letters, spaces, hyphens, and apostrophes"
        
        return True, None
    
    @staticmethod
    def validate_tech_stack(tech_stack):
        """
        Validate and clean tech stack input
        
        Args:
            tech_stack: Tech stack string
            
        Returns:
            tuple: (is_valid, cleaned_list, suggestions, error_message)
        """
        if not tech_stack or len(tech_stack.strip()) == 0:
            return False, [], [], "Tech stack cannot be empty. Please list your technologies."
        
        # Split by common separators
        technologies = re.split(r'[,;/\n]+', tech_stack)
        
        # Clean and filter
        cleaned = []
        for tech in technologies:
            tech = tech.strip()
            if tech and len(tech) > 1:
                cleaned.append(tech)
        
        if not cleaned:
            return False, [], [], "Please enter at least one technology"
        
        # Get suggestions for typos or matches
        suggestions = InputValidator._get_tech_suggestions(cleaned)
        
        return True, cleaned, suggestions, None
    
    @staticmethod
    def _get_tech_suggestions(tech_list):
        """Get suggestions for technology names"""
        suggestions = []
        
        # Flatten all tech categories
        all_known_tech = []
        for category in Config.TECH_CATEGORIES.values():
            all_known_tech.extend([t.lower() for t in category])
        
        for tech in tech_list:
            tech_lower = tech.lower()
            
            # Check for close matches
            for known_tech in all_known_tech:
                if known_tech in tech_lower or tech_lower in known_tech:
                    if tech.lower() != known_tech:
                        suggestions.append({
                            'input': tech,
                            'suggestion': known_tech.title()
                        })
                    break
        
        return suggestions
    
    @staticmethod
    def validate_position(position):
        """
        Validate position/role
        
        Args:
            position: Position string
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not position or len(position.strip()) == 0:
            return False, "Position cannot be empty"
        
        position = position.strip()
        
        if len(position) < 3:
            return False, "Position must be at least 3 characters"
        
        if len(position) > 100:
            return False, "Position description is too long"
        
        return True, None
    
    @staticmethod
    def validate_location(location):
        """
        Validate location
        
        Args:
            location: Location string
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not location or len(location.strip()) == 0:
            return False, "Location cannot be empty"
        
        location = location.strip()
        
        if len(location) < 2:
            return False, "Location must be at least 2 characters"
        
        if len(location) > 100:
            return False, "Location is too long"
        
        return True, None
    
    @staticmethod
    def is_exit_command(text):
        """
        Check if user wants to exit
        
        Args:
            text: User input
            
        Returns:
            bool: True if exit command detected
        """
        if not text:
            return False
        
        text_lower = text.lower().strip()
        
        return text_lower in Config.EXIT_KEYWORDS or \
               any(keyword in text_lower for keyword in Config.EXIT_KEYWORDS)
    
    @staticmethod
    def sanitize_input(text):
        """
        Sanitize user input
        
        Args:
            text: User input
            
        Returns:
            str: Sanitized text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove potentially harmful characters (basic sanitization)
        text = re.sub(r'[<>{}\\]', '', text)
        
        return text.strip()