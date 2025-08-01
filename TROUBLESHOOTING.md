# 🛠️ Troubleshooting Guide - Agentic AI Tutor

This guide helps you solve common issues with the AI Tutor. If you encounter problems, check here first!

---

## 🚨 Common Issues & Solutions

### 1. **"No syllabus found" - Wrong Subject Generated**

#### **Problem:**
You select "Karnataka 10th Math" but only have "CBSE 10th Science" PDF, yet the AI creates a Math roadmap anyway.

#### **Why This Happens:**
- AI finds some documents (Science PDF) but they don't match your request
- Old version would "guess" and create content from general knowledge
- This defeats the purpose of syllabus-based learning

#### **Solution Applied:**
```python
# Added strict metadata filtering in tutor_agent.py
matching_docs = []
for doc in docs:
    metadata = doc.metadata
    if (metadata.get('board', '').upper() == board.upper() and 
        metadata.get('grade', '') == grade and 
        metadata.get('subject', '').upper() == subject.upper()):
        matching_docs.append(doc)
```

#### **Now You'll See:**
```
📚 **No syllabus found for Karnataka 10th Math**

**What I have available:**
• CBSE 10th Science

**To add Karnataka 10th Math:**
1. Add a PDF named `Karnataka_10th_Math.pdf` to `data/syllabi/`
2. Run `python setup.py` to process it
3. Then try again!
```

---

### 2. **Setup Errors**

#### **Problem A: "EURIAI_API_KEY not found"**
```
❌ EURIAI_API_KEY not found in .env file
```

**Solution:**
```bash
# Create .env file with your API key
echo 'EURIAI_API_KEY="your_actual_api_key_here"' > .env
```

#### **Problem B: "No PDFs found"**
```
📁 No PDFs found in data/syllabi/
```

**Solution:**
1. Add PDFs to `data/syllabi/` folder
2. Use correct naming: `Board_Grade_Subject.pdf`
3. Examples: `CBSE_10th_Science.pdf`, `ICSE_9th_Math.pdf`

#### **Problem C: "Failed to load vector store"**
```
Failed to load vector store: [Errno 2] No such file or directory
```

**Solution:**
```bash
# Run setup first
python setup.py
```

---

### 3. **Chat Interface Issues**

#### **Problem: Gradio Warning About Chatbot Type**
```
UserWarning: You have not specified a value for the `type` parameter. 
Defaulting to the 'tuples' format for chatbot messages
```

**What This Means:**
- Just a warning, doesn't break functionality
- Gradio is updating their chatbot format
- App still works perfectly

**Solution (Optional):**
```python
# In app.py, update chatbot to:
chatbot = gr.Chatbot(
    height=400,
    type="messages",  # Add this line
    placeholder="👋 Hi there! I'm ready to help you learn!"
)
```

---

### 4. **API & Network Issues**

#### **Problem A: "AI request failed"**
```
❌ AI request failed: HTTPSConnectionPool
```

**Possible Causes & Solutions:**
1. **No Internet**: Check your connection
2. **Wrong API Key**: Verify your `.env` file
3. **API Service Down**: Try again in a few minutes
4. **Firewall/Proxy**: Check network restrictions

#### **Problem B: "Embedding API error"**
```
Embedding API error: 401 Unauthorized
```

**Solution:**
- Double-check your API key in `.env`
- Make sure there are no extra spaces around the key

---

### 5. **PDF Processing Issues**

#### **Problem A: "Error parsing PDF"**
```
❌ Error with CBSE_10th_Science.pdf: Cannot read an empty file
```

**Solution:**
- Ensure PDF file is not corrupted
- Download PDF again from official source
- Check file size (should be > 0 bytes)

#### **Problem B: "Wrong format" warnings**
```
⚠️ Skipping filename.pdf (wrong format)
```

**Solution:**
Use correct naming format:
- ✅ `CBSE_10th_Science.pdf`
- ✅ `Karnataka_8th_Math.pdf`  
- ❌ `science.pdf`
- ❌ `math_grade10.pdf`

---

### 6. **Virtual Environment Issues**

#### **Problem: "ModuleNotFoundError"**
```
ModuleNotFoundError: No module named 'gradio'
```

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### **Problem: "externally-managed-environment"**
```
error: externally-managed-environment
```

**Solution:**
```bash
# Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 7. **Performance Issues**

#### **Problem A: "Setup takes too long"**
- **Normal**: 30-60 seconds per PDF
- **Slow Internet**: Can take 2-3 minutes
- **Large PDFs**: More content = more time

**What's Happening:**
- Each PDF chunk needs to be embedded
- API calls to Euriai for embeddings
- FAISS index creation

#### **Problem B: "App response is slow"**
- **Normal**: 2-5 seconds for roadmap
- **First Query**: May be slower (loading index)

---

### 8. **Kid Chat Issues**

#### **Problem: "Chat responses too complex"**
If AI responses are too advanced for young kids:

**Solution in Code:**
```python
# The prompt already includes kid-friendly rules:
- Use simple words and short sentences
- Be encouraging and positive
- Use emojis to make it fun
- Keep answers short (2-3 sentences max)
```

#### **Problem: "Chat doesn't use syllabus"**
If chat gives general answers instead of syllabus-based ones:

**What Happens:**
- Chat tries to find relevant syllabus content first
- If nothing matches, gives general kid-friendly response
- This is intentional for better user experience

---

## 🔧 Debug Mode

### **Enable Detailed Logging:**
```python
# In app.py, change:
demo.launch(debug=True)  # Already enabled

# In setup.py, add print statements to see what's happening:
print(f"Processing chunk {i+1}/{len(all_documents)}")
```

### **Check What's in Your Vector Store:**
```python
# Add this to test your index:
from langchain_community.vectorstores import FAISS
from src.utils.euriai_embeddings import EuriaiEmbeddings

embeddings = EuriaiEmbeddings()
vector_store = FAISS.load_local("data/vector_store/faiss_index", embeddings, allow_dangerous_deserialization=True)

# Test search
docs = vector_store.similarity_search("science topics", k=5)
for doc in docs:
    print(f"Subject: {doc.metadata.get('subject')}")
    print(f"Content: {doc.page_content[:100]}...")
    print("---")
```

---

## 📞 Getting Help

### **Still Having Issues?**

1. **Check the logs** in your terminal for error messages
2. **Verify file structure:**
   ```
   Agentic-AI-Tutor/
   ├── .env (with your API key)
   ├── data/syllabi/YourPDF.pdf
   ├── data/vector_store/faiss_index/
   └── src/agents/tutor_agent.py
   ```
3. **Test API connection:**
   ```bash
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', 'Found' if os.environ.get('EURIAI_API_KEY') else 'Missing')"
   ```

### **Reporting Bugs:**
When reporting issues, include:
- Error message (full text)
- What you were trying to do
- Your PDF filenames
- Operating system

---

## ✅ **Quick Health Check**

Run this checklist if something seems wrong:

- [ ] Virtual environment activated (`source venv/bin/activate`)
- [ ] `.env` file exists with `EURIAI_API_KEY="your_key"`
- [ ] PDFs in `data/syllabi/` with correct naming
- [ ] Ran `python setup.py` successfully
- [ ] See `data/vector_store/faiss_index/` folder with files
- [ ] Internet connection working
- [ ] Can access `http://127.0.0.1:7860` in browser

If all items are checked ✅, your AI Tutor should work perfectly! 🎓

---

*This troubleshooting guide is based on real issues encountered during development and testing. It will be updated as more solutions are discovered.*