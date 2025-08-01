"""
Unified Interface for the AI Tutor System
This module provides a single entry point for the Gradio UI to interact with the AI tutor.
It uses the structured `tutor` module for all AI-related tasks.
"""
import os
import json
import logging
from dotenv import load_dotenv
from typing import Dict, List, Optional
from langchain_community.vectorstores import FAISS

from src.tutor.registry import create_agent, AGENT_CONFIGS
from src.utils.euriai_embeddings import EuriaiEmbeddings

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AI_Tutor:
    """The main interface for the AI Tutor application."""

    def __init__(self, vector_store_path="data/vector_store/faiss_index"):
        self.api_key = os.environ.get("EURIAI_API_KEY")
        self.retriever = None
        self.agents = {}

        if self.api_key and os.path.exists(vector_store_path):
            try:
                embeddings = EuriaiEmbeddings(model="gemini-embedding-001")
                vector_store = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)
                self.retriever = vector_store.as_retriever(search_kwargs={"k": 5})
            except Exception as e:
                logger.error(f"Error loading vector store: {e}")

        for agent_type in AGENT_CONFIGS.keys():
            self.agents[agent_type] = create_agent(agent_type, self.retriever)

    def _get_agent_for_subject(self, subject: str) -> Optional[object]:
        """Selects the best agent based on the subject."""
        subject_map = {
            "science": "science_tutor",
            "math": "math_tutor",
            "social studies": "social_tutor",
            "english": "english_tutor",
        }
        agent_key = subject_map.get(subject.lower(), "learning_coordinator")
        return self.agents.get(agent_key)

    def generate_learning_roadmap(self, grade: str, board: str, subject: str) -> str:
        """Generates a personalized learning roadmap using a specialized agent."""
        if not self.retriever:
            return "The AI Tutor is not fully initialized. Please run the setup process."

        agent = self._get_agent_for_subject(subject)
        query = f"Create a learning roadmap for a {grade} student studying {subject} for the {board} board."
        
        return agent.process_request(
            user_input=query,
            subject=subject,
            grade=grade,
            complexity="complex"
        )

    def generate_quiz(self, grade: str, subject: str, num_questions: int = 5) -> Optional[List[Dict]]:
        """Generates a quiz using the specialized agent for the selected subject."""
        agent = self._get_agent_for_subject(subject)
        if not agent:
            logger.error(f"No agent found for subject: {subject}")
            return None

        prompt = f"""
        Create a {num_questions}-question multiple-choice quiz for a {grade} grade student on the subject of {subject}.
        The quiz complexity should be reasoning.
        For each question, provide:
        - "question": The question text.
        - "options": A list of 4 possible answers.
        - "correct_answer": The index (0-3) of the correct answer in the options list.
        - "explanation": A brief, kid-friendly explanation for why the answer is correct.
        
        Return the quiz as a valid JSON list of objects only. Do not include any other text or formatting.
        """
        
        try:
            response = agent.process_request(
                user_input=prompt,
                subject=subject,
                grade=grade,
                complexity="reasoning"
            )
            return json.loads(response)
        except (json.JSONDecodeError, TypeError) as e:
            logger.error(f"Error parsing AI quiz response: {e}\nResponse was: {response}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred during quiz generation: {e}")
            return None

    def chat_with_tutor(self, message: str, subject: str, grade: str) -> str:
        """Handles chat interactions with the appropriate specialized tutor."""
        agent = self._get_agent_for_subject(subject)
        return agent.process_request(
            user_input=message,
            subject=subject,
            grade=grade,
            complexity="medium"
        )

# Global instance for the application to use
tutor_interface = AI_Tutor()
