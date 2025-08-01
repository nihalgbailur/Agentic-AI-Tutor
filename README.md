# Agentic AI Tutor 🤖

Welcome to the Agentic AI Tutor! This is a free, open-source educational tool designed to help students learn more effectively. Using the power of AI, our tutor can create personalized learning roadmaps and answer questions based on your specific school syllabus.

## ✨ Features

-   **Personalized Learning Roadmaps**: Get a custom, week-by-week study plan based on your grade, board, and subject.
-   **Interactive Chat Tutor**: Ask questions about your subject and get clear, simple answers based on your syllabus.
-   **Syllabus-Powered**: All roadmaps and answers are generated using the syllabus you provide, ensuring the information is relevant to your studies.

---

## 📚 For Our Users: How to Use the Tutor

Getting started with your AI Tutor is as easy as 1-2-3!

1.  **Start Your Journey**: When you launch the app, click the **"Click Here to Start!"** button.
2.  **Tell Us What You're Learning**: On the main screen, use the dropdown menus to select your **Grade**, **Board** (like CBSE or ICSE), and **Subject**.
3.  **Generate Your Roadmap**: Click the **"🚀 Generate My Roadmap"** button. The AI will think for a moment and then create a personalized study plan just for you!
4.  **Chat with Your Tutor**: After generating your roadmap, click on the **"💬 Chat with Your Tutor"** tab. You can ask any question about the subject you selected, and the AI will help you understand it.

---

## 💻 For Developers: Technical Guide

This section provides a technical overview for developers who want to set up, run, or contribute to the project.

### Project Overview

The Agentic AI Tutor is a Python application built with Gradio. It leverages a Retrieval-Augmented Generation (RAG) pipeline to provide syllabus-aware educational content.

-   **Backend**: Python, LangChain
-   **Frontend**: Gradio
-   **AI/LLM**: Euriai API (`gpt-4.1-nano`)
-   **Embeddings**: Euriai API (`text-embedding-3-small`)
-   **Vector Store**: FAISS (for local similarity search)

### Project Structure

```
Agentic-AI-Tutor/
├── .env                  # API keys (create manually)
├── app.py                # Main Gradio app
├── setup.py              # Setup script to process PDFs
├── requirements.txt      # Dependencies
├── data/
│   ├── syllabi/          # Your syllabus PDFs go here
│   └── vector_store/     # AI index storage
└── src/
    ├── agents/
    │   └── tutor_agent.py # AI tutor logic
    └── utils/
        ├── euriai_embeddings.py # AI embeddings
        └── pdf_parser.py   # PDF processing
```

### Setup and Installation

Follow these steps to get the project running locally:

**1. Clone the Repository**
```bash
git clone https://github.com/your-username/Agentic-AI-Tutor.git
cd Agentic-AI-Tutor
```

**2. Create and Activate a Virtual Environment**
```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Set Up Your API Key**
- Create a file named `.env` in the root of the project.
- Add your Euriai API key to this file:
  ```
  EURIAI_API_KEY="your_euriai_api_key_here"
  ```

**5. Add Syllabus PDFs**
- Place your syllabus documents into the `data/syllabi/` folder.
- **Important**: Files must be named in the format `Board_Grade_Subject.pdf` (e.g., `CBSE_10th_Science.pdf`).

**6. Run the Setup Script**
This script will process your PDFs and create the searchable FAISS vector index. You only need to run this once, or whenever you add new syllabi.
```bash
python setup.py
```

**7. Launch the Application**
```bash
python3 app.py
```
Open the local URL provided in your terminal (e.g., `http://127.0.0.1:7860`) in your browser.

### How It Works: The RAG Pipeline

1.  **Indexing (`setup.py`)**: The `EuriaiEmbeddings` model converts the text chunks from your syllabus PDFs into numerical vectors, which are then stored in a local FAISS index.
2.  **Retrieval**: When a user makes a request (e.g., asks a question), the agent uses `EuriaiEmbeddings` to convert the query into a vector. It then searches the FAISS index to find the most relevant syllabus chunks (the "context").
3.  **Generation**: The retrieved context is combined with the user's original query into a detailed prompt. This final prompt is sent to the `euriai` `gpt-4.1-nano` model, which generates the final, user-facing answer or roadmap.

---

## 🔧 Technical Deep Dive

### Euriai API Integration Methods

Our project uses the Euriai API for both text generation and embeddings. There are two ways to integrate with Euriai:

#### Method 1: Raw API (Current Implementation)
```python
import requests

response = requests.post(
    "https://api.euron.one/api/v1/euri/chat/completions",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "messages": [{"role": "user", "content": prompt}],
        "model": "gpt-4.1-nano",
        "temperature": 0.7
    }
)
```

#### Method 2: Euriai Python SDK (Alternative)
```python
from euriai import EuriaiClient

client = EuriaiClient(
    api_key="your_api_key_here",
    model="gpt-4.1-nano"
)

response = client.generate_completion(
    prompt="Write a short poem about artificial intelligence.",
    temperature=0.7,
    max_tokens=300
)
```

#### Why We Use Raw API
- ✅ **Educational Value**: Better understanding of HTTP requests and API structure
- ✅ **Lightweight**: Only requires `requests` library, no additional dependencies
- ✅ **Full Control**: Complete control over headers, error handling, and request formatting
- ✅ **Transparency**: Clear visibility into what data is being sent and received

#### When to Consider SDK
- **Rapid Prototyping**: When you need to build features quickly
- **Advanced Features**: If Euriai releases SDK-only features
- **Error Handling**: SDK may provide better built-in error handling
- **Code Simplicity**: Cleaner, more readable code for complex operations

---

## 🤖 Multi-Agent System Analysis

### Current Architecture: Subject-Based Agents

Our current implementation uses subject-specific agents:
```python
agents = {
    "science_tutor": "Science Education Specialist",
    "math_tutor": "Mathematics Learning Specialist", 
    "social_tutor": "Social Studies & History Expert",
    "english_tutor": "Language Arts & Communication Coach"
}
```

### Best Use Cases for CrewAI Multi-Agent Systems

#### 1. 🔥 Complex Problem Solving (Recommended)
```python
# Student: "I'm struggling with word problems in math"
# 
# Multi-Agent Workflow:
# 1. Math Agent: Analyzes mathematical concepts
# 2. English Agent: Identifies reading comprehension issues  
# 3. Learning Coordinator: Creates integrated solution
#
# Result: Addresses both math and language barriers
```

#### 2. 🎓 Adaptive Learning Assessment
```python
# Multi-Agent Workflow:
# 1. Assessment Agent: Identifies knowledge gaps
# 2. Pedagogy Agent: Designs teaching approach
# 3. Practice Agent: Creates exercises
# 4. Progress Agent: Monitors improvement
```

#### 3. 🧠 Task-Based Specialization (Alternative Architecture)
```python
# Instead of subject-based, use task-based agents:
study_buddy_crew = {
    "explainer": "Breaks down complex concepts simply",
    "practice_generator": "Creates age-appropriate exercises", 
    "motivator": "Provides encouragement and feedback",
    "progress_tracker": "Monitors learning and adjusts difficulty"
}
```

### UI Complexity Analysis

#### ❌ Features That May Be Too Complex for Kids Under 10:
- **"Meet Your Tutors" Tab**: Technical details about agents
- **"Connect Subjects" Tab**: Forced cross-subject integration
- **Multi-Agent Toggle**: Technical system choices

#### ✅ Features Kids Actually Need:
- **Simple Chat**: "Ask me anything about Math/Science/English"
- **Learning Roadmap**: "Here's your weekly plan"
- **Subject Selection**: Basic dropdowns (Grade, Board, Subject)
- **Age-Appropriate Responses**: Automatic based on age selection

#### Recommended Simplification:
```
Current UI (Complex):
├── 📅 My Learning Plan
├── 💬 Ask Questions  
├── 🌟 Connect Subjects (Remove)
├── 🤖 Meet Your Tutors (Remove)
└── 🚀 Advanced Toggle (Make Invisible)

Simplified UI (Kid-Friendly):
├── 📅 My Learning Plan
└── 💬 Ask Questions
```

### Smart Agent Routing (Behind the Scenes)
```python
# Invisible to users, but intelligent routing:
def route_to_appropriate_agent(subject, question_type, age):
    if subject == "Math" and "word problem" in question:
        return [math_agent, english_agent, coordinator]  # Multi-agent
    elif subject == "Science" and age < 8:
        return science_agent.with_simple_mode()  # Single agent, simple
    else:
        return get_subject_expert(subject)  # Standard routing
```

### Core Insight
**Multi-agent systems provide value through intelligence, not complexity. The sophistication should be invisible to young users while providing better educational outcomes.**

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features, bug fixes, or improvements, please feel free to open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

