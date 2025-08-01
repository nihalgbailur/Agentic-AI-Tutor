# 🛠️ Troubleshooting Guide - Agentic AI Tutor

This guide helps you solve common issues with the AI Tutor. If you encounter problems, check here first!

---

## 🚨 Common Issues & Solutions

### 1. **"No syllabus found" - Wrong Subject Generated**

#### **Problem:**
You select "Karnataka 10th Math" but only have "CBSE 10th Science" PDF, yet the AI creates a Math roadmap anyway.

#### **Why This Happens:**
- The AI finds some documents (the Science PDF), but they don't match your request.
- The old version of the application would "guess" and create content from its general knowledge.
- This defeats the purpose of syllabus-based learning.

#### **Solution Applied:**
- The agent now performs strict metadata filtering to ensure that the retrieved documents exactly match the user's request.

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
1.  Add PDFs to the `data/syllabi/` folder.
2.  Use the correct naming convention: `Board_Grade_Subject.pdf` (e.g., `CBSE_10th_Science.pdf`).

#### **Problem C: "Failed to load vector store"**
```
Failed to load vector store: [Errno 2] No such file or directory
```

**Solution:**
```bash
# Run the setup script first
python setup.py
```

---

### 3. **API & Network Issues**

#### **Problem A: "AI request failed"**
```
❌ AI request failed: HTTPSConnectionPool
```

**Possible Causes & Solutions:**
1.  **No Internet**: Check your internet connection.
2.  **Wrong API Key**: Verify your API key in the `.env` file.
3.  **API Service Down**: The Euriai API might be temporarily unavailable. Try again in a few minutes.
4.  **Firewall/Proxy**: Check your network for any restrictions that might be blocking the connection.

---

### 4. **Virtual Environment Issues**

#### **Problem: "ModuleNotFoundError"**
```
ModuleNotFoundError: No module named 'gradio'
```

**Solution:**
```bash
# Make sure your virtual environment is activated
source venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt
```

---

## ✅ **Quick Health Check**

Run this checklist if something seems wrong:

- [ ] Virtual environment is activated (`source venv/bin/activate`).
- [ ] `.env` file exists with `EURIAI_API_KEY="your_key"`.
- [ ] PDFs are in `data/syllabi/` with the correct naming convention.
- [ ] `python setup.py` has been run successfully.
- [ ] The `data/vector_store/faiss_index/` folder exists and contains files.
- [ ] Your internet connection is working.
- [ ] You can access the local URL (e.g., `http://127.0.0.1:7860`) in your browser.

If all items are checked ✅, your AI Tutor should work perfectly! 🎓
