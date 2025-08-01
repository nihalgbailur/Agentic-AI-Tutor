"""
Simplified Multi-Agent Tutor System
Lightweight implementation with specialized subject agents
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from src.utils.euriai_embeddings import EuriaiEmbeddings
from src.agents.crew_config import (
    create_agent, 
    AGENT_CONFIGS,
    SubjectExpert
)

load_dotenv()

class CrewTutorAgent:
    """Simplified multi-agent tutor system with subject specialization"""
    
    def __init__(self, vector_store_path="data/vector_store/faiss_index"):
        self.api_key = os.environ.get("EURIAI_API_KEY")
        self.retriever = None
        self.agents = {}
        
        # Initialize retriever
        if self.api_key and os.path.exists(vector_store_path):
            try:
                embeddings = EuriaiEmbeddings()
                vector_store = FAISS.load_local(
                    vector_store_path, 
                    embeddings, 
                    allow_dangerous_deserialization=True
                )
                self.retriever = vector_store.as_retriever(search_kwargs={"k": 10})
                
                # Initialize specialized agents
                self._initialize_agents()
                
            except Exception as e:
                print(f"Failed to initialize multi-agent system: {e}")
    
    def _initialize_agents(self):
        """Initialize all specialized subject agents"""
        agent_types = [
            "science_tutor", 
            "math_tutor", 
            "social_tutor", 
            "english_tutor", 
            "learning_coordinator"
        ]
        
        for agent_type in agent_types:
            try:
                self.agents[agent_type] = create_agent(agent_type, self.retriever)
                print(f"✅ Initialized {agent_type}")
            except Exception as e:
                print(f"❌ Failed to initialize {agent_type}: {e}")
    
    def get_subject_agent(self, subject: str):
        """Get the appropriate agent for a subject"""
        subject_mapping = {
            "science": "science_tutor",
            "math": "math_tutor", 
            "mathematics": "math_tutor",
            "social": "social_tutor",
            "social studies": "social_tutor",
            "history": "social_tutor",
            "english": "english_tutor",
            "language": "english_tutor"
        }
        
        agent_key = subject_mapping.get(subject.lower(), "learning_coordinator")
        return self.agents.get(agent_key)
    
    def generate_advanced_roadmap(self, grade: str, board: str, subject: str):
        """Generate roadmap using specialized agents"""
        
        if not self.retriever or not self.agents:
            return "🔧 Multi-agent system not initialized. Check your setup."
        
        # Get subject-specific agent
        primary_agent = self.get_subject_agent(subject)
        
        if not primary_agent:
            return "❌ Required agents not available. Check system setup."
        
        try:
            # Create roadmap generation prompt
            roadmap_prompt = f"""Create a comprehensive learning roadmap for {grade} grade {subject} ({board} board).
            
            Requirements:
            - Structure as weekly/monthly learning plan
            - Include key topics, learning objectives, and suggested activities
            - Make it age-appropriate for {grade} students
            - Use engaging, motivational language
            - Base content on the provided syllabus information
            
            Please create a detailed, structured learning roadmap in markdown format."""
            
            # Use subject expert agent to generate roadmap
            result = primary_agent.process_request(
                roadmap_prompt, 
                context_query=f"{board} {grade} {subject} syllabus topics",
                subject=subject
            )
            
            return f"""# 🎯 AI-Generated Learning Roadmap
*Created by specialized {subject} tutor agent*

{result}

---
*Generated using multi-agent system with subject expertise*"""
            
        except Exception as e:
            return f"❌ Error generating roadmap: {e}"
    
    def multi_agent_chat(self, user_message: str, grade: str = None, board: str = None, 
                        subject: str = None, age: int = None):
        """Handle chat using appropriate specialist agent"""
        
        if not self.agents:
            return "🤖 Hi! I need to be set up first. Ask a grown-up to help!"
        
        # Determine which agent should handle this
        if subject:
            primary_agent = self.get_subject_agent(subject)
        else:
            # Use coordinator for general questions
            primary_agent = self.agents.get("learning_coordinator")
        
        if not primary_agent:
            return "❌ No appropriate agent available for this question."
        
        try:
            # Create age-appropriate chat prompt
            age_context = ""
            if age and age < 10:
                age_context = f"Answer in very simple words for a {age}-year-old child. Use fun examples and emojis!"
            elif age:
                age_context = f"Answer appropriately for a {age}-year-old student."
            
            chat_prompt = f"""{age_context}
            
            Student's question: {user_message}
            
            Please provide a helpful, encouraging response."""
            
            # Use subject expert agent
            result = primary_agent.process_request(
                chat_prompt,
                context_query=user_message if subject else None,
                subject=subject
            )
            
            return result
            
        except Exception as e:
            return f"❌ Error processing question: {e}"
    
    def cross_subject_learning(self, topic: str, subject1: str, subject2: str, grade: str):
        """Create integrated learning experiences across subjects"""
        
        agent1 = self.get_subject_agent(subject1)
        agent2 = self.get_subject_agent(subject2)
        coordinator = self.agents.get("learning_coordinator")
        
        if not all([agent1, agent2, coordinator]):
            return "❌ Required agents not available for cross-subject integration."
        
        try:
            # Create cross-subject integration prompt
            integration_prompt = f"""Create an integrated learning activity that connects {subject1} with {subject2} around the topic of "{topic}" for {grade} grade students.
            
            Requirements:
            - Show clear connections between {subject1} and {subject2}
            - Create engaging, hands-on activities
            - Ensure age-appropriateness for {grade} students
            - Include learning objectives for both subjects
            - Provide step-by-step activity instructions
            - Include materials needed and assessment criteria
            
            Make it educational, fun, and meaningful!"""
            
            # Use coordinator to create integrated activity
            result = coordinator.process_request(
                integration_prompt,
                context_query=f"{topic} {subject1} {subject2} {grade}",
                subject=None  # Cross-subject, so no specific subject filter
            )
            
            return f"""# 🌟 Integrated Learning Activity
*Connecting {subject1} and {subject2}*

{result}

---
*Created through multi-agent collaboration*"""
            
        except Exception as e:
            return f"❌ Error creating integrated activity: {e}"
    
    def get_agent_expertise(self, subject: str = None):
        """Get information about available agents and their expertise"""
        
        if subject:
            agent = self.get_subject_agent(subject)
            if agent:
                config_key = None
                for key, agent_obj in self.agents.items():
                    if agent_obj == agent:
                        config_key = key
                        break
                
                if config_key and config_key in AGENT_CONFIGS:
                    config = AGENT_CONFIGS[config_key]
                    return f"""## 🎓 {config['role']}

**Expertise:** {config['goal']}

**Background:** {config['system_message'][:200]}...

**Model:** {config['model']} (Temperature: {config['temperature']})"""
            
            return f"No specialized agent found for {subject}"
        
        # Return all agents
        expertise_info = "# 🤖 Available AI Tutors\n\n"
        
        for agent_key, config in AGENT_CONFIGS.items():
            expertise_info += f"""## {config['role']}
- **Goal:** {config['goal']}
- **Model:** {config['model']}
- **Temperature:** {config['temperature']}

"""
        
        return expertise_info
    
    def health_check(self):
        """Check the health of all agents"""
        status = {
            "api_key": bool(self.api_key),
            "retriever": self.retriever is not None,
            "agents_initialized": len(self.agents),
            "available_agents": list(self.agents.keys())
        }
        
        return status

# Simple Multi-Agent Integration Support
class AutoGenTutorWrapper:
    """Simplified wrapper for multi-agent integration"""
    
    def __init__(self, crew_agent: CrewTutorAgent):
        self.crew_agent = crew_agent
    
    def get_agent_config(self, subject: str):
        """Get agent configuration for a subject"""
        
        agent = self.crew_agent.get_subject_agent(subject)
        if not agent:
            return None
        
        # Basic configuration
        config = {
            "name": f"{subject}_tutor",
            "role": agent.config.get("role", f"{subject} tutor"),
            "system_message": agent.config.get("system_message", ""),
            "model": agent.config.get("model", "gpt-4.1-nano"),
            "temperature": agent.config.get("temperature", 0.7)
        }
        
        return config
    
    def create_agent_configs(self, subjects: List[str]):
        """Create configurations for multiple subjects"""
        
        configs = []
        for subject in subjects:
            config = self.get_agent_config(subject)
            if config:
                configs.append(config)
        
        return configs