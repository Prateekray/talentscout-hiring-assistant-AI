"""
Sentiment Analysis for TalentScout Hiring Assistant
Detects candidate emotions to adjust chatbot responses
"""
from textblob import TextBlob
import re

class SentimentAnalyzer:
    """Analyzes sentiment and emotions in candidate messages"""
    
    def __init__(self):
        """Initialize sentiment analyzer"""
        self.sentiment_history = []
        
        # Emotion keywords for enhanced detection
        self.positive_keywords = [
            'great', 'excited', 'happy', 'love', 'awesome', 'perfect',
            'excellent', 'wonderful', 'fantastic', 'amazing', 'good',
            'nice', 'thanks', 'appreciate', 'glad', 'pleased'
        ]
        
        self.negative_keywords = [
            'confused', 'frustrated', 'angry', 'upset', 'disappointed',
            'worried', 'nervous', 'anxious', 'difficult', 'hard',
            'struggle', 'problem', 'issue', 'hate', 'bad', 'terrible'
        ]
        
        self.uncertainty_keywords = [
            'maybe', 'perhaps', 'not sure', 'unsure', 'confused',
            'don\'t know', 'uncertain', 'unclear', 'guess'
        ]
    
    def analyze_sentiment(self, text):
        """
        Analyze sentiment of text
        
        Args:
            text: User message
            
        Returns:
            dict: Sentiment analysis results
        """
        if not text or len(text.strip()) == 0:
            return self._default_sentiment()
        
        # TextBlob analysis
        blob = TextBlob(text.lower())
        polarity = blob.sentiment.polarity  # -1 to 1
        subjectivity = blob.sentiment.subjectivity  # 0 to 1
        
        # Keyword-based emotion detection
        emotions = self._detect_emotions(text.lower())
        
        # Classify sentiment
        sentiment_label = self._classify_sentiment(polarity, emotions)
        
        # Confidence level
        confidence = self._calculate_confidence(polarity, subjectivity, emotions)
        
        result = {
            'polarity': round(polarity, 2),
            'subjectivity': round(subjectivity, 2),
            'sentiment': sentiment_label,
            'emotions': emotions,
            'confidence': confidence,
            'needs_support': self._needs_emotional_support(sentiment_label, emotions)
        }
        
        # Track sentiment history
        self.sentiment_history.append(result)
        
        return result
    
    def _classify_sentiment(self, polarity, emotions):
        """Classify sentiment into categories"""
        # Check emotions first (more specific)
        if 'frustrated' in emotions or 'angry' in emotions:
            return 'negative'
        if 'confused' in emotions or 'uncertain' in emotions:
            return 'uncertain'
        if 'excited' in emotions or 'happy' in emotions:
            return 'positive'
        
        # Fallback to polarity
        if polarity >= 0.3:
            return 'positive'
        elif polarity <= -0.3:
            return 'negative'
        elif -0.1 <= polarity <= 0.1:
            return 'neutral'
        elif polarity > 0:
            return 'slightly_positive'
        else:
            return 'slightly_negative'
    
    def _detect_emotions(self, text):
        """Detect specific emotions from keywords"""
        emotions = []
        
        # Check positive emotions
        for keyword in self.positive_keywords:
            if keyword in text:
                if keyword in ['excited', 'love', 'amazing', 'fantastic']:
                    emotions.append('excited')
                elif keyword in ['thanks', 'appreciate']:
                    emotions.append('grateful')
                else:
                    emotions.append('happy')
                break
        
        # Check negative emotions
        for keyword in self.negative_keywords:
            if keyword in text:
                if keyword in ['confused', 'unclear']:
                    emotions.append('confused')
                elif keyword in ['frustrated', 'angry', 'upset']:
                    emotions.append('frustrated')
                elif keyword in ['worried', 'nervous', 'anxious']:
                    emotions.append('anxious')
                else:
                    emotions.append('unhappy')
                break
        
        # Check uncertainty
        for keyword in self.uncertainty_keywords:
            if keyword in text:
                emotions.append('uncertain')
                break
        
        return list(set(emotions))  # Remove duplicates
    
    def _calculate_confidence(self, polarity, subjectivity, emotions):
        """Calculate confidence in sentiment analysis"""
        confidence = 0.5  # Base confidence
        
        # Strong polarity increases confidence
        if abs(polarity) > 0.5:
            confidence += 0.3
        elif abs(polarity) > 0.3:
            confidence += 0.2
        
        # Emotions detected increases confidence
        if emotions:
            confidence += 0.2
        
        # High subjectivity with emotions is more reliable
        if subjectivity > 0.6 and emotions:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _needs_emotional_support(self, sentiment, emotions):
        """Determine if response needs emotional support"""
        negative_sentiments = ['negative', 'slightly_negative']
        negative_emotions = ['frustrated', 'confused', 'anxious', 'unhappy']
        
        if sentiment in negative_sentiments:
            return True
        
        if any(emotion in negative_emotions for emotion in emotions):
            return True
        
        return False
    
    def _default_sentiment(self):
        """Return default neutral sentiment"""
        return {
            'polarity': 0.0,
            'subjectivity': 0.0,
            'sentiment': 'neutral',
            'emotions': [],
            'confidence': 0.5,
            'needs_support': False
        }
    
    def get_sentiment_trend(self):
        """Get overall sentiment trend from history"""
        if len(self.sentiment_history) < 2:
            return 'stable'
        
        recent = self.sentiment_history[-3:]
        polarities = [s['polarity'] for s in recent]
        
        # Check if improving or declining
        if len(polarities) >= 2:
            if polarities[-1] > polarities[-2] + 0.2:
                return 'improving'
            elif polarities[-1] < polarities[-2] - 0.2:
                return 'declining'
        
        return 'stable'
    
    def get_average_sentiment(self):
        """Get average sentiment from history"""
        if not self.sentiment_history:
            return self._default_sentiment()
        
        avg_polarity = sum(s['polarity'] for s in self.sentiment_history) / len(self.sentiment_history)
        avg_subjectivity = sum(s['subjectivity'] for s in self.sentiment_history) / len(self.sentiment_history)
        
        return {
            'polarity': round(avg_polarity, 2),
            'subjectivity': round(avg_subjectivity, 2),
            'sentiment': self._classify_sentiment(avg_polarity, []),
            'message_count': len(self.sentiment_history)
        }
    
    def adjust_response_tone(self, response, sentiment_result):
        """
        Adjust response tone based on sentiment
        
        Args:
            response: Original chatbot response
            sentiment_result: Sentiment analysis result
            
        Returns:
            str: Adjusted response
        """
        if not sentiment_result['needs_support']:
            return response
        
        # Add supportive phrases for negative sentiment
        supportive_prefixes = [
            "I understand this might be challenging. ",
            "No worries at all! ",
            "I appreciate your honesty. ",
            "That's completely okay. "
        ]
        
        # Check if response already has supportive language
        if any(prefix.lower() in response.lower() for prefix in supportive_prefixes):
            return response
        
        # Add appropriate prefix based on emotions
        emotions = sentiment_result['emotions']
        
        if 'confused' in emotions or 'uncertain' in emotions:
            prefix = "No problem, let me clarify. "
        elif 'frustrated' in emotions:
            prefix = "I understand this can be frustrating. "
        elif 'anxious' in emotions:
            prefix = "There's no need to worry! "
        else:
            prefix = supportive_prefixes[0]
        
        return prefix + response
    
    def clear_history(self):
        """Clear sentiment history"""
        self.sentiment_history = []
    
    def get_emotion_summary(self):
        """Get summary of detected emotions"""
        if not self.sentiment_history:
            return "No emotions detected yet"
        
        all_emotions = []
        for result in self.sentiment_history:
            all_emotions.extend(result['emotions'])
        
        if not all_emotions:
            return "Neutral conversation tone"
        
        # Count emotions
        emotion_counts = {}
        for emotion in all_emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Get most common emotion
        most_common = max(emotion_counts, key=emotion_counts.get)
        
        return f"Predominantly {most_common} ({emotion_counts[most_common]} occurrences)"