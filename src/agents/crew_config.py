"""
Simplified Multi-Agent Configuration for Subject-Specific AI Tutors
Lightweight implementation without heavy dependencies.
"""

import os
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

class SimpleLLMAgent:
    """Lightweight LLM agent for Euriai API"""
    
    def __init__(self, model="gpt-4.1-nano", temperature=0.7):
        self.api_key = os.environ.get("EURIAI_API_KEY")
        self.model = model
        self.temperature = temperature
        self.base_url = "https://api.euron.one/api/v1/euri/chat/completions"
    
    def call_llm(self, prompt: str, system_message: str = None) -> str:
        """Make API call to Euriai"""
        if not self.api_key:
            return "❌ API key not found"
        
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = requests.post(
                self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "messages": messages,
                    "model": self.model,
                    "temperature": self.temperature,
                    "max_tokens": 2048
                }
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"❌ API Error: {e}"

# Subject-Specific Agent Configurations
AGENT_CONFIGS = {
    "science_tutor": {
        "role": "Science Education Specialist",
        "goal": "Help students understand scientific concepts through clear explanations and real-world examples",
        "system_message": """You are an expert science teacher with 15+ years of experience. 
        You excel at breaking down complex scientific concepts into simple, understandable parts. 
        You use analogies, experiments, and visual descriptions to make science exciting and accessible 
        for students of all ages. Always base your explanations on accurate scientific principles.""",
        "model": "gpt-4.1-nano",
        "temperature": 0.6
    },
    
    "math_tutor": {
        "role": "Mathematics Learning Specialist", 
        "goal": "Make mathematics intuitive and enjoyable through step-by-step problem solving",
        "system_message": """You are a passionate mathematics educator who believes every student can 
        excel in math. You have a gift for identifying where students struggle and providing 
        clear, step-by-step solutions. You use visual methods, patterns, and real-life applications 
        to make abstract mathematical concepts concrete and understandable. Always show your work clearly.""",
        "model": "gpt-4.1-nano",
        "temperature": 0.4
    },
    
    "social_tutor": {
        "role": "Social Studies & History Expert",
        "goal": "Bring history and social concepts to life through engaging storytelling and connections",
        "system_message": """You are a dynamic social studies teacher who makes history come alive. 
        You excel at connecting past events to current situations, helping students understand 
        the relevance of history and social concepts. You use storytelling, timelines, and 
        cultural connections to make learning memorable and meaningful. Keep facts accurate.""",
        "model": "gpt-4.1-nano",  # Using consistent model for now
        "temperature": 0.8
    },
    
    "english_tutor": {
        "role": "Language Arts & Communication Coach",
        "goal": "Develop students' reading, writing, and communication skills with creativity and precision",
        "system_message": """You are an enthusiastic English teacher who loves language and literature. 
        You help students express themselves clearly and creatively. You excel at grammar explanation, 
        vocabulary building, reading comprehension, and creative writing guidance. You make language 
        learning fun through games, stories, and interactive activities. Use proper grammar always.""",
        "model": "gpt-4.1-nano",  # Using consistent model for now
        "temperature": 0.7
    },
    
    "learning_coordinator": {
        "role": "Educational Coordinator & Learning Strategist",
        "goal": "Coordinate between subject experts and create comprehensive learning experiences",
        "system_message": """You are an experienced educational coordinator who specializes in 
        creating integrated learning experiences. You excel at identifying connections between 
        subjects and designing personalized learning paths. You coordinate with subject experts 
        to provide holistic educational support. Focus on creating structured, comprehensive plans.""",
        "model": "gpt-4.1-nano",
        "temperature": 0.6
    }
}

class SubjectExpert:
    """Individual subject expert agent"""
    
    def __init__(self, agent_type: str, retriever=None):
        if agent_type not in AGENT_CONFIGS:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        self.config = AGENT_CONFIGS[agent_type]
        self.agent_type = agent_type
        self.retriever = retriever
        self.llm = SimpleLLMAgent(
            model=self.config["model"],
            temperature=self.config["temperature"]
        )
    
    def get_context(self, query: str, subject: str = None) -> str:
        """Get relevant context from retriever if available"""
        if not self.retriever:
            return ""
        
        try:
            docs = self.retriever.invoke(query)
            if docs:
                # Filter by subject if specified
                if subject:
                    filtered_docs = []
                    for doc in docs:
                        if doc.metadata.get('subject', '').lower() == subject.lower():
                            filtered_docs.append(doc)
                    docs = filtered_docs if filtered_docs else docs[:3]
                
                context = "\n".join([doc.page_content[:200] for doc in docs[:3]])
                return f"\n\nRelevant syllabus content:\n{context}"
            return ""
        except:
            return ""
    
    def process_request(self, user_input: str, context_query: str = None, subject: str = None) -> str:
        """Process a request with optional context"""
        
        # Get context if needed
        context = ""
        if context_query and self.retriever:
            context = self.get_context(context_query, subject)
        
        # Create full prompt
        full_prompt = f"{user_input}{context}"
        
        # Call LLM with agent's system message
        return self.llm.call_llm(full_prompt, self.config["system_message"])

def create_agent(agent_type: str, retriever=None):
    """Factory function to create subject expert agents"""
    return SubjectExpert(agent_type, retriever)