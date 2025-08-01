# 🤖 Agentic AI Tutor - Technical Deep Dive

## 📋 Overview
This document explains the complete technical workflow of the Agentic AI Tutor, from setup to user interaction. The project uses a Retrieval-Augmented Generation (RAG) architecture to create personalized learning roadmaps based on actual syllabus content.

---

## 🧠 AI Models Used

### 1. **Embedding Model: `text-embedding-3-small`**
- **Provider**: Euriai API
- **Purpose**: Convert text into numerical vectors for similarity search
- **Input**: Text chunks from PDFs or user queries
- **Output**: 1536-dimensional vectors
- **Used in**: PDF indexing and query processing

### 2. **Generation Model: `gpt-4.1-nano`**
- **Provider**: Euriai API  
- **Purpose**: Generate human-readable roadmaps and kid-friendly chat responses
- **Input**: Combined context + user prompt
- **Output**: Structured markdown text or conversational responses
- **Used in**: Roadmap generation and interactive chat

---

## 🔄 Complete Workflow

### Phase 1: One-Time Setup (`python setup.py`)

#### Step 1: Environment Check
```python
# Check if API key exists
EURIAI_API_KEY = os.environ.get("EURIAI_API_KEY")
if not EURIAI_API_KEY:
    exit("❌ API key missing")
```

#### Step 2: PDF Discovery
```python
# Scan for PDFs in data/syllabi/
pdf_files = glob.glob("data/syllabi/*.pdf")
# Expected format: Board_Grade_Subject.pdf
# Example: CBSE_10th_Science.pdf
```

#### Step 3: PDF Processing
```python
def parse_pdf(file_path, board, grade, subject):
    # Load PDF
    loader = PyPDFLoader(file_path)
    
    # Split into chunks (1000 chars, 100 overlap)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=100
    )
    documents = loader.load_and_split(text_splitter)
    
    # Add metadata to each chunk
    for doc in documents:
        doc.metadata.update({
            'board': board,    # CBSE
            'grade': grade,    # 10th  
            'subject': subject # Science
        })
    
    return documents
```

**Example chunk after processing:**
```python
{
    "page_content": "Light travels in straight lines. This is evident from the formation of shadows...",
    "metadata": {
        "board": "CBSE",
        "grade": "10th", 
        "subject": "Science",
        "source": "data/syllabi/CBSE_10th_Science.pdf",
        "page": 15
    }
}
```

#### Step 4: Text Embedding
```python
# Initialize embedding model
embedding_function = EuriaiEmbeddings(model="text-embedding-3-small")

# Convert each text chunk to vector
for chunk in documents:
    vector = embedding_function.embed_documents([chunk.page_content])
    # Result: [0.123, -0.456, 0.789, ...] (1536 numbers)
```

**API Call Example:**
```python
# Euriai Embedding API
POST https://api.euron.one/api/v1/euri/embeddings
Headers: {"Authorization": "Bearer <api_key>"}
Body: {
    "input": "Light travels in straight lines...",
    "model": "text-embedding-3-small"
}
Response: {
    "data": [{"embedding": [0.123, -0.456, ...]}]
}
```

#### Step 5: Vector Index Creation
```python
# Create FAISS index for fast similarity search
faiss_index = FAISS.from_documents(all_documents, embedding_function)

# Save to disk
faiss_index.save_local("data/vector_store/faiss_index")
```

**What FAISS stores:**
```
Vector Index Structure:
├── Document 1: [0.123, -0.456, ...] → "Light travels in straight lines..."
├── Document 2: [0.789, 0.012, ...] → "Laws of reflection state that..."
├── Document 3: [0.345, -0.678, ...] → "Refraction occurs when light..."
└── ... (hundreds more)
```

---

### Phase 2: Runtime (`python app.py`)

#### Step 1: Application Startup
```python
# Load the pre-built FAISS index
try:
    embeddings = EuriaiEmbeddings()
    vector_store = FAISS.load_local(
        "data/vector_store/faiss_index", 
        embeddings,
        allow_dangerous_deserialization=True
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 10})
    print("✅ AI Tutor ready!")
except:
    print("❌ Run 'python setup.py' first")
```

#### Step 2: User Input Processing
```python
# User selects:
grade = "10th"
board = "CBSE"  
subject = "Science"

# Create search query
query = f"{board} {grade} {subject} syllabus topics"
```

#### Step 3: Similarity Search (Retrieval)
```python
# Convert query to vector using same embedding model
query_vector = embeddings.embed_query(query)
# Result: [0.234, -0.567, 0.890, ...] (1536 numbers)

# Find most similar document chunks
docs = retriever.get_relevant_documents(query)
# Returns top 10 most similar chunks based on cosine similarity
```

**How similarity search works:**
```python
# Cosine similarity calculation
def cosine_similarity(vector_a, vector_b):
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    magnitude_a = sum(a * a for a in vector_a) ** 0.5
    magnitude_b = sum(b * b for b in vector_b) ** 0.5
    return dot_product / (magnitude_a * magnitude_b)

# FAISS efficiently finds highest similarity scores
similarity_scores = [
    0.89, # "Light and reflection topics" 
    0.85, # "Physics concepts for 10th grade"
    0.82, # "CBSE Science curriculum"
    ...
]
```

#### Step 4: Context Preparation (Augmentation)
```python
# Combine retrieved document chunks
context = "\n".join([doc.page_content for doc in docs])

# Example combined context:
context = """
Light travels in straight lines. This is evident from the formation of shadows...

Laws of reflection state that the angle of incidence equals the angle of reflection...

Refraction occurs when light passes from one medium to another...

The human eye works on the principle of refraction...
"""
```

#### Step 5: Prompt Engineering
```python
prompt = f"""Create a weekly study plan for a {grade} student studying {subject} ({board} board).

Syllabus Content:
{context}

Make it friendly and organized with weeks/months. Use markdown formatting.
If the content doesn't match the request, say "Sorry, I don't have the right syllabus for this subject."
"""
```

#### Step 6: AI Generation
```python
# Call Euriai Generation API
response = requests.post(
    "https://api.euron.one/api/v1/euri/chat/completions",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "messages": [{"role": "user", "content": prompt}],
        "model": "gpt-4.1-nano",
        "max_tokens": 2048,
        "temperature": 0.7
    }
)

# Extract generated roadmap
roadmap = response.json()['choices'][0]['message']['content']
```

**API Response Example:**
```markdown
# Science Learning Roadmap (10th Grade, CBSE)

## Week 1: Light - Reflection and Refraction
- Understanding how light travels
- Laws of reflection with mirror experiments
- Practice problems on angle calculations

## Week 2: Human Eye and Vision
- Structure of the human eye
- Common vision defects and corrections
- Lens formula applications

## Week 3: Natural Phenomena
- Rainbow formation and dispersion
- Atmospheric refraction effects
- Twinkling of stars explanation
...
```

#### Step 7: UI Display
```python
# Gradio displays the formatted roadmap
gr.Markdown(roadmap)
```

---

## 🔧 Key Technical Components

### File Structure & Responsibilities
```
├── app.py                    # Gradio UI + user interaction
├── setup.py                  # PDF processing + FAISS indexing
├── src/agents/tutor_agent.py # RAG logic + API calls
└── src/utils/euriai_embeddings.py # Custom embedding wrapper
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
1. **Embeddings**: `https://api.euron.one/api/v1/euri/embeddings`
2. **Chat Completion**: `https://api.euron.one/api/v1/euri/chat/completions`

---

## 📊 Performance Characteristics

### Setup Phase (One-time)
- **Time**: 30-60 seconds per PDF
- **API Calls**: ~50-100 embedding requests per PDF
- **Storage**: ~10-50MB per processed PDF

### Runtime Phase (Per query)
- **Time**: 2-5 seconds per roadmap
- **API Calls**: 1 embedding + 1 generation request
- **Memory**: Loads entire FAISS index (~50-100MB)

---

## 🔍 Why This Architecture Works

### 1. **Accuracy via RAG**
- Grounds AI responses in actual syllabus content
- Prevents hallucination of incorrect topics
- Ensures curriculum compliance

### 2. **Speed via Pre-processing**
- Heavy lifting done once during setup
- Runtime queries are fast (pre-built index)
- No real-time PDF parsing needed

### 3. **Scalability via Vector Search**
- FAISS enables sub-second search through thousands of documents
- Easily add new subjects/boards without code changes
- Embedding similarity handles semantic matching

### 4. **Flexibility via Metadata**
- Each chunk tagged with board/grade/subject
- Enables precise filtering during retrieval
- Supports multiple curricula simultaneously

---

## 🚀 From Zero to Working System

### Initial State
```
Empty Project + API Key
```

### After Setup
```
Processed PDFs → Searchable Vector Database → Ready for Queries
```

### User Experience
```
Student Input → Instant Syllabus-Based Roadmap → Personalized Learning Plan
```

This architecture ensures that every generated roadmap is both **educationally accurate** (based on real syllabi) and **pedagogically sound** (structured by advanced AI).

---

## 💬 Kid-Friendly Chat Feature

### Chat Workflow
```
Child's Question → Context Search → Kid-Friendly Prompt → Simple Answer
```

### Chat-Specific Processing
```python
def chat_with_kid(user_message, grade, board, subject):
    # 1. Try to find relevant syllabus content
    context = retriever.get_relevant_documents(f"{user_message} {board} {grade} {subject}")
    
    # 2. Create kid-friendly prompt
    prompt = f"""You are a super friendly AI tutor talking to a child under 10 years old.
    
    RULES:
    - Use simple words and short sentences
    - Be encouraging and positive  
    - Use emojis to make it fun
    - Keep answers short (2-3 sentences max)
    
    Child's question: "{user_message}"
    Syllabus context: {context}
    """
    
    # 3. Generate kid-appropriate response
    return gpt_4_1_nano.generate(prompt)
```

### Example Chat Interactions
```
Child: "What is light?"
AI: "🌟 Light is like invisible rays that help us see! It comes from the sun, light bulbs, and fire. Without light, everything would be dark! ✨"

Child: "Why do plants need water?"  
AI: "🌱 Plants drink water just like you drink juice! Water helps them grow big and strong. It's like food for plants! 💧"

Child: "How do magnets work?"
AI: "🧲 Magnets are like invisible hands that can pull metal things! Some sides stick together and some push away. It's like magic! ✨"
```

This dual-mode system provides both structured learning (roadmaps) and interactive support (chat) tailored for young learners.