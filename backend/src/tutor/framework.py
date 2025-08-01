"""
Optimized EuriAI Framework for AI Tutor
Uses only available models from EuriAI dashboard
"""

from euriai import EuriaiClient
import os
import time
from typing import Dict, Optional, List
from dotenv import load_dotenv

load_dotenv()

class EuriaiModelFramework:
    """Intelligent model selection and routing for educational AI"""
    
    def __init__(self):
        self.client = EuriaiClient(
            api_key=os.environ.get("EURIAI_API_KEY"),
            model="gpt-4.1-nano"  # Default
        )
        self.usage_stats = {}
        
    def select_optimal_model(self, 
                           task_type: str,
                           complexity: str = "medium",
                           speed_priority: str = "balanced",
                           subject: str = "general") -> str:
        """Selects the best model based on the task, complexity, and subject."""
        selection_matrix = {
            "chat": {"simple": "gemini-2.5-flash", "medium": "gpt-4.1-nano", "complex": "gpt-4.1-mini"},
            "math": {"simple": "gpt-4.1-mini", "medium": "deepseek-r1-distill-llama-70b", "complex": "gemini-2.5-pro"},
            "science": {"simple": "gemini-2.5-flash", "medium": "gpt-4.1-mini", "complex": "gemini-2.5-pro"},
            "creative": {"simple": "gpt-4.1-nano", "medium": "gpt-4.1-mini", "complex": "gemini-2.5-pro"},
            "reasoning": {"simple": "gpt-4.1-mini", "medium": "llama-4-scout-17b-16e-instruct", "complex": "gemini-2.5-pro"},
        }
        
        model = selection_matrix.get(task_type, {}).get(complexity, "gpt-4.1-nano")
        
        # Subject-specific overrides for high-complexity tasks
        if complexity == "complex":
            if subject == "math":
                model = "deepseek-r1-distill-llama-70b"
            elif subject == "science":
                model = "gemini-2.5-pro"

        return model
    
    def _adapt_prompt_for_chat(self, prompt: str, grade: str) -> str:
        """Applies a kid-friendly persona ONLY for conversational chat."""
        grade_adaptations = {
            "5th": "Explain in very simple terms for a 10-year-old. Use easy words and fun examples.",
            "6th": "Explain clearly for an 11-year-old student. Use examples they can relate to.",
            "7th": "Explain for a 12-year-old. Be thorough but clear.",
            "8th": "Explain for a 13-year-old preparing for high school."
        }
        adaptation = grade_adaptations.get(grade, "Explain clearly for a middle school student.")
        
        return f"""
        {adaptation}
        Use emojis to make it fun. Be encouraging and positive.
        
        Student's question: "{prompt}"
        """

    def generate_response(self,
                         prompt: str,
                         task_type: str = "chat", 
                         complexity: str = "medium",
                         speed_priority: str = "balanced",
                         subject: str = "general",
                         grade: str = "6th",
                         temperature: float = 0.7,
                         max_tokens: int = 4096) -> Dict:
        """Generates a response with intelligent model selection and appropriate prompting."""
        
        selected_model = self.select_optimal_model(task_type, complexity, speed_priority, subject)
        
        # Adapt prompt only for chat tasks
        final_prompt = self._adapt_prompt_for_chat(prompt, grade) if task_type == "chat" else prompt
        
        start_time = time.time()
        
        try:
            self.client.model = selected_model
            response = self.client.generate_completion(
                prompt=final_prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            parsed_content = self._parse_completion_response(response)
            self._track_usage(selected_model, response_time, len(parsed_content))
            
            return {
                "response": parsed_content,
                "model_used": selected_model,
                "response_time": response_time,
                "success": True
            }
            
        except Exception as e:
            return self._fallback_response(str(e))
    
    def _fallback_response(self, error: str) -> Dict:
        """Provides a generic fallback response."""
        return {
            "response": f"🤖 I'm having a little trouble right now. Please try again! Error: {error}",
            "model_used": "fallback",
            "response_time": 0,
            "success": False
        }
    
    def _parse_completion_response(self, response: Dict) -> str:
        """Safely extracts content from the AI's response, handling errors."""
        try:
            choice = response.get('choices', [{}])[0]
            message = choice.get('message', {})
            content = message.get('content')

            if content:
                return content.strip()
            
            finish_reason = choice.get('finish_reason', 'unknown')
            if finish_reason == 'length':
                return "Error: The response was too long and got cut off. Please try a more specific question."
            else:
                return f"Error: The AI response was empty. Finish reason: {finish_reason}"

        except (KeyError, IndexError, TypeError) as e:
            return f"Error parsing response: {str(response)} - Exception: {e}"

    def _track_usage(self, model: str, response_time: float, response_length: int):
        """Tracks model usage statistics."""
        if model not in self.usage_stats:
            self.usage_stats[model] = {"calls": 0, "total_time": 0, "total_tokens": 0}
        
        stats = self.usage_stats[model]
        stats["calls"] += 1
        stats["total_time"] += response_time
        stats["total_tokens"] += response_length

# Global instance for easy access
euriai_framework = EuriaiModelFramework()
