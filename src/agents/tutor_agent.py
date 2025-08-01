import os
import requests
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from src.utils.euriai_embeddings import EuriaiEmbeddings

load_dotenv()

class TutorAgent:
    """AI Tutor that creates roadmaps based on syllabus content."""
    
    def __init__(self, vector_store_path="data/vector_store/faiss_index"):
        self.api_key = os.environ.get("EURIAI_API_KEY")
        self.retriever = None
        
        if self.api_key and os.path.exists(vector_store_path):
            try:
                embeddings = EuriaiEmbeddings()
                vector_store = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)
                self.retriever = vector_store.as_retriever(search_kwargs={"k": 10})
            except Exception as e:
                print(f"Failed to load vector store: {e}")

    def _call_ai(self, prompt: str):
        """Call Euriai API with the given prompt."""
        if not self.api_key:
            return "❌ API key not found. Check your .env file."
            
        try:
            response = requests.post(
                "https://api.euron.one/api/v1/euri/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "messages": [{"role": "user", "content": prompt}],
                    "model": "gpt-4.1-nano",
                    "max_tokens": 2048,
                    "temperature": 0.7,
                }
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"❌ AI request failed: {e}"

    def generate_roadmap(self, grade: str, board: str, subject: str):
        """Generate a learning roadmap based on syllabus content."""
        if not self.retriever:
            return "🔧 Setup needed: Run 'python setup.py' first"

        # Find relevant syllabus content with metadata filtering
        query = f"{board} {grade} {subject} syllabus topics"
        docs = self.retriever.get_relevant_documents(query)
        
        # Filter documents to match exact board, grade, and subject
        matching_docs = []
        for doc in docs:
            metadata = doc.metadata
            if (metadata.get('board', '').upper() == board.upper() and 
                metadata.get('grade', '') == grade and 
                metadata.get('subject', '').upper() == subject.upper()):
                matching_docs.append(doc)
        
        if not matching_docs:
            # Check what we actually have
            available_subjects = set()
            for doc in docs[:5]:  # Check first few docs
                meta = doc.metadata
                available_subjects.add(f"{meta.get('board', 'Unknown')} {meta.get('grade', 'Unknown')} {meta.get('subject', 'Unknown')}")
            
            available_list = "\n".join([f"• {subj}" for subj in available_subjects])
            
            return f"""📚 **No syllabus found for {board} {grade} {subject}**

**What I have available:**
{available_list}

**To add {board} {grade} {subject}:**
1. Add a PDF named `{board}_{grade}_{subject}.pdf` to `data/syllabi/`
2. Run `python setup.py` to process it
3. Then try again!"""
        
        context = "\n".join([doc.page_content for doc in matching_docs])
        
        # Create roadmap prompt with strict instructions
        prompt = f"""Create a weekly study plan for a {grade} student studying {subject} ({board} board).

IMPORTANT: The content below is from the official {board} {grade} {subject} syllabus. Create the plan ONLY based on this content.

Syllabus Content:
{context}

Make it friendly and organized with weeks/months. Use markdown formatting.
"""
        
        return self._call_ai(prompt)

    def chat_with_kid(self, user_message: str, grade: str = None, board: str = None, subject: str = None):
        """Kid-friendly chat assistant for children under 10."""
        if not self.api_key:
            return "🤖 Hi! I need to be set up first. Ask a grown-up to help!"

        # If they selected a subject, try to find relevant info
        context = ""
        if all([grade, board, subject]) and self.retriever:
            try:
                query = f"{user_message} {board} {grade} {subject}"
                docs = self.retriever.get_relevant_documents(query)
                if docs:
                    context = "\n".join([doc.page_content[:200] for doc in docs[:3]])  # Shorter context for kids
            except:
                pass  # If search fails, just use general chat

        # Kid-friendly prompt
        prompt = f"""You are a super friendly AI tutor talking to a child under 10 years old. 

IMPORTANT RULES:
- Use simple words and short sentences
- Be encouraging and positive
- Use emojis to make it fun
- Explain things like talking to a curious kid
- If you don't know something, say "That's a great question! Let me think..."
- Keep answers short (2-3 sentences max)

Child's question: "{user_message}"

{f"Here's some info from their syllabus: {context}" if context else ""}

Response (remember: simple, fun, encouraging):"""

        return self._call_ai(prompt)
