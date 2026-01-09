"""
Data Handler for TalentScout Hiring Assistant
Manages candidate data storage and retrieval
"""
import json
import os
from datetime import datetime
import pandas as pd

class DataHandler:
    """Handles candidate data storage and management"""
    
    def __init__(self, data_file="data/candidates.json"):
        """Initialize data handler"""
        self.data_file = data_file
        self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self):
        """Create data file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump([], f)
    
    def save_candidate(self, candidate_data):
        """
        Save candidate data to file
        
        Args:
            candidate_data: Dictionary containing candidate information
            
        Returns:
            bool: Success status
        """
        try:
            # Add timestamp and ID
            candidate_data['timestamp'] = datetime.now().isoformat()
            candidate_data['candidate_id'] = self._generate_candidate_id()
            
            # Load existing data
            candidates = self.load_all_candidates()
            
            # Append new candidate
            candidates.append(candidate_data)
            
            # Save back to file
            with open(self.data_file, 'w') as f:
                json.dump(candidates, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error saving candidate: {str(e)}")
            return False
    
    def load_all_candidates(self):
        """Load all candidates from file"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading candidates: {str(e)}")
            return []
    
    def get_candidate_by_id(self, candidate_id):
        """Get specific candidate by ID"""
        candidates = self.load_all_candidates()
        for candidate in candidates:
            if candidate.get('candidate_id') == candidate_id:
                return candidate
        return None
    
    def get_candidate_by_email(self, email):
        """Get candidate by email"""
        candidates = self.load_all_candidates()
        for candidate in candidates:
            if candidate.get('email', '').lower() == email.lower():
                return candidate
        return None
    
    def _generate_candidate_id(self):
        """Generate unique candidate ID"""
        candidates = self.load_all_candidates()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        count = len(candidates) + 1
        return f"TS{timestamp}{count:04d}"
    
    def export_to_csv(self, output_file="data/candidates_export.csv"):
        """Export candidates to CSV"""
        try:
            candidates = self.load_all_candidates()
            if not candidates:
                return False
            
            df = pd.DataFrame(candidates)
            df.to_csv(output_file, index=False)
            return True
            
        except Exception as e:
            print(f"Error exporting to CSV: {str(e)}")
            return False
    
    def get_statistics(self):
        """Get statistics about stored candidates"""
        candidates = self.load_all_candidates()
        
        if not candidates:
            return {
                'total_candidates': 0,
                'positions': {},
                'avg_experience': 0,
                'tech_stack_summary': {}
            }
        
        # Calculate statistics
        positions = {}
        total_experience = 0
        all_tech = []
        
        for candidate in candidates:
            # Count positions
            pos = candidate.get('position', 'Unknown')
            positions[pos] = positions.get(pos, 0) + 1
            
            # Sum experience
            try:
                exp = float(candidate.get('experience', 0))
                total_experience += exp
            except:
                pass
            
            # Collect tech stack
            tech_stack = candidate.get('tech_stack', '')
            if tech_stack:
                all_tech.extend([t.strip() for t in tech_stack.split(',')])
        
        # Count tech occurrences
        tech_counts = {}
        for tech in all_tech:
            tech_counts[tech] = tech_counts.get(tech, 0) + 1
        
        # Get top 10 technologies
        top_tech = dict(sorted(tech_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        
        return {
            'total_candidates': len(candidates),
            'positions': positions,
            'avg_experience': round(total_experience / len(candidates), 1) if candidates else 0,
            'tech_stack_summary': top_tech
        }
    
    def clear_all_data(self):
        """Clear all candidate data (use with caution!)"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump([], f)
            return True
        except Exception as e:
            print(f"Error clearing data: {str(e)}")
            return False


class ConversationExporter:
    """Export conversation transcripts"""
    
    @staticmethod
    def export_conversation(conversation_history, candidate_data, filename=None):
        """
        Export conversation to text file
        
        Args:
            conversation_history: List of conversation messages
            candidate_data: Dictionary of candidate information
            filename: Output filename (optional)
            
        Returns:
            str: Filename of exported conversation
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            candidate_name = candidate_data.get('name', 'Unknown').replace(' ', '_')
            filename = f"data/transcript_{candidate_name}_{timestamp}.txt"
        
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                # Header
                f.write("=" * 60 + "\n")
                f.write("TALENTSCOUT HIRING ASSISTANT - INTERVIEW TRANSCRIPT\n")
                f.write("=" * 60 + "\n\n")
                
                # Candidate Information
                f.write("CANDIDATE INFORMATION:\n")
                f.write("-" * 60 + "\n")
                for key, value in candidate_data.items():
                    if key not in ['timestamp', 'candidate_id', 'conversation_history']:
                        f.write(f"{key.upper()}: {value}\n")
                f.write("\n")
                
                # Conversation
                f.write("CONVERSATION TRANSCRIPT:\n")
                f.write("-" * 60 + "\n\n")
                
                for msg in conversation_history:
                    role = "ASSISTANT" if msg['role'] == 'assistant' else "CANDIDATE"
                    f.write(f"{role}:\n{msg['content']}\n\n")
                
                # Footer
                f.write("=" * 60 + "\n")
                f.write(f"Transcript generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n")
            
            return filename
            
        except Exception as e:
            print(f"Error exporting conversation: {str(e)}")
            return None