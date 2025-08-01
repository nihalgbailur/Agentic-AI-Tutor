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
-   **AI/LLM**: Euriai API
-   **Embeddings**: Euriai API
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
    ├── tutor/
    │   ├── __init__.py
    │   ├── framework.py
    │   ├── interface.py
    │   ├── quizzes.py
    │   └── registry.py
    └── utils/
        └── euriai_embeddings.py # AI embeddings
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
3.  **Generation**: The retrieved context is combined with the user's original query into a detailed prompt. This final prompt is sent to the Euriai API, which generates the final, user-facing answer or roadmap.

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features, bug fixes, or improvements, please feel free to open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
