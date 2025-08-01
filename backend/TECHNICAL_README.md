# 🤖 Agentic AI Tutor - Technical Deep Dive

## 📋 Overview
This document explains the complete technical workflow of the Agentic AI Tutor, from setup to user interaction. The project uses a Retrieval-Augmented Generation (RAG) architecture to create personalized learning roadmaps based on actual syllabus content.

---

## 🧠 AI Models Used

### 1. **Embedding Model**
- **Provider**: Euriai API
- **Purpose**: Convert text into numerical vectors for similarity search
- **Input**: Text chunks from PDFs or user queries
- **Output**: High-dimensional vectors
- **Used in**: PDF indexing and query processing

### 2. **Generation Model**
- **Provider**: Euriai API  
- **Purpose**: Generate human-readable roadmaps and kid-friendly chat responses
- **Input**: Combined context + user prompt
- **Output**: Structured markdown text or conversational responses
- **Used in**: Roadmap generation and interactive chat

---

## 🔄 Complete Workflow

### Phase 1: One-Time Setup (`python setup.py`)

#### Step 1: Environment Check
- Checks for the `EURIAI_API_KEY` in the `.env` file.

#### Step 2: PDF Discovery
- Scans for PDFs in `data/syllabi/` with the format `Board_Grade_Subject.pdf`.

#### Step 3: PDF Processing
- Loads and splits PDFs into chunks.
- Adds metadata (`board`, `grade`, `subject`) to each chunk.

#### Step 4: Text Embedding
- Initializes the `EuriaiEmbeddings` model.
- Converts each text chunk into a vector using the Euriai API.

#### Step 5: Vector Index Creation
- Creates a FAISS index from the documents and their embeddings.
- Saves the index to `data/vector_store/faiss_index`.

---

### Phase 2: Runtime (`python app.py`)

#### Step 1: Application Startup
- Loads the pre-built FAISS index and initializes the `AI_Tutor` interface.

#### Step 2: User Input Processing
- The user selects `grade`, `board`, and `subject` in the Gradio UI.
- The application creates a search query based on the user's selections.

#### Step 3: Similarity Search (Retrieval)
- The agent converts the query to a vector.
- It then finds the most similar document chunks in the FAISS index.

#### Step 4: Context Preparation (Augmentation)
- The retrieved document chunks are combined to form the context.

#### Step 5: Prompt Engineering
- The agent creates a detailed prompt that includes the context and the user's original query.

#### Step 6: AI Generation
- The agent sends the final prompt to the Euriai API to generate the roadmap or chat response.

#### Step 7: UI Display
- The Gradio UI displays the formatted output to the user.

---

## 🔧 Key Technical Components

### File Structure & Responsibilities
```
├── app.py                    # Gradio UI + user interaction
├── setup.py                  # PDF processing + FAISS indexing
├── src/
│   ├── tutor/
│   │   ├── __init__.py
│   │   ├── framework.py      # Core model selection logic
│   │   ├── interface.py      # Bridge between UI and AI
│   │   ├── quizzes.py        # AI-powered quiz generation
│   │   └── registry.py       # Agent configurations
│   └── utils/
│       └── euriai_embeddings.py # Custom embedding wrapper
```

### Data Flow
```
PDF Files → Text Chunks → Embeddings → FAISS Index
    ↓
User Query → Query Embedding → Similarity Search → Context
    ↓
Context + Prompt → Generation Model → Final Roadmap
```

### API Endpoints Used
1.  **Embeddings**: `https://api.euron.one/api/v1/euri/embeddings`
2.  **Chat Completion**: `https://api.euron.one/api/v1/euri/chat/completions`

---

## 🚀 From Zero to Working System

### Initial State
- Empty Project + API Key

### After Setup
- Processed PDFs → Searchable Vector Database → Ready for Queries

### User Experience
- Student Input → Instant Syllabus-Based Roadmap → Personalized Learning Plan

This architecture ensures that every generated roadmap is both **educationally accurate** (based on real syllabi) and **pedagogically sound** (structured by advanced AI).
