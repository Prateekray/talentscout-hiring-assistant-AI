"""
Groq API Client for TalentScout Hiring Assistant
Handles all AI interactions with error handling and retry logic
"""
import time
from groq import Groq
from config import Config

class GroqClient:
    """Wrapper for Groq API with error handling"""
    
    def __init__(self):
        """Initialize Groq client"""
        try:
            Config.validate()
            self.client = Groq(api_key=Config.GROQ_API_KEY)
            self.model = Config.GROQ_MODEL
            self.temperature = Config.TEMPERATURE
            self.max_tokens = Config.MAX_TOKENS
        except Exception as e:
            raise Exception(f"Failed to initialize Groq client: {str(e)}")
    
    def generate_response(self, messages, temperature=None, max_tokens=None):
        """
        Generate response from Groq API
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Override default temperature
            max_tokens: Override default max tokens
            
        Returns:
            str: Generated response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                top_p=1,
                stream=False
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return self._handle_error(e)
    
    def generate_streaming_response(self, messages, temperature=None):
        """
        Generate streaming response from Groq API
        
        Args:
            messages: List of message dictionaries
            temperature: Override default temperature
            
        Yields:
            str: Chunks of generated response
        """
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=self.max_tokens,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield self._handle_error(e)
    
    def quick_generation(self, system_prompt, user_prompt, temperature=0.7):
        """
        Quick generation for simple tasks
        
        Args:
            system_prompt: System instruction
            user_prompt: User message
            temperature: Temperature setting
            
        Returns:
            str: Generated response
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        return self.generate_response(messages, temperature=temperature)
    
    def _handle_error(self, error):
        """Handle API errors gracefully"""
        error_msg = str(error).lower()
        
        if "rate limit" in error_msg:
            return "I'm processing many requests right now. Let me try again in a moment..."
        elif "api key" in error_msg:
            return "There's a configuration issue. Please contact support."
        elif "timeout" in error_msg:
            return "The request took too long. Could you please try again?"
        elif "connection" in error_msg:
            return "I'm having trouble connecting. Please check your internet connection."
        else:
            return f"I encountered an issue: {str(error)}. Let's continue - please repeat your last message."
    
    def validate_response(self, response):
        """Validate that response is appropriate"""
        if not response or len(response.strip()) == 0:
            return False
        
        # Check for common error patterns
        error_patterns = ["error", "failed", "unable to", "cannot process"]
        response_lower = response.lower()
        
        for pattern in error_patterns:
            if pattern in response_lower and len(response) < 100:
                return False
        
        return True
    
    def generate_with_retry(self, messages, max_retries=3):
        """
        Generate response with retry logic
        
        Args:
            messages: List of message dictionaries
            max_retries: Maximum number of retry attempts
            
        Returns:
            str: Generated response
        """
        for attempt in range(max_retries):
            try:
                response = self.generate_response(messages)
                
                if self.validate_response(response):
                    return response
                
                # If response invalid, retry with slightly higher temperature
                time.sleep(1)
                
            except Exception as e:
                if attempt == max_retries - 1:
                    return self._handle_error(e)
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return "I'm having trouble generating a response. Could you please rephrase your message?"
    
    def test_connection(self):
        """Test if Groq API is accessible"""
        try:
            test_messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'OK' if you can hear me."}
            ]
            
            response = self.generate_response(test_messages, temperature=0)
            return "OK" in response.upper() or "ok" in response.lower()
            
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False


class ConversationManager:
    """Manages conversation context and history"""
    
    def __init__(self, system_prompt, max_context_length=10):
        """
        Initialize conversation manager
        
        Args:
            system_prompt: System instruction for the AI
            max_context_length: Maximum messages to keep in context
        """
        self.system_prompt = system_prompt
        self.max_context_length = max_context_length
        self.conversation_history = []
    
    def add_message(self, role, content):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
        
        # Trim history if too long (keep system prompt + recent messages)
        if len(self.conversation_history) > self.max_context_length:
            self.conversation_history = self.conversation_history[-self.max_context_length:]
    
    def get_messages_for_api(self):
        """Get formatted messages for API call"""
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.conversation_history)
        return messages
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_history(self):
        """Get conversation history"""
        return self.conversation_history.copy()
    
    def get_last_n_messages(self, n):
        """Get last n messages from history"""
        return self.conversation_history[-n:] if n <= len(self.conversation_history) else self.conversation_history.copy()