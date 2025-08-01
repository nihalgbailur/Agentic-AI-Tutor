# 🚀 Agentic AI Tutor - Frontend-Backend Integration

This guide helps you run the complete Agentic AI Tutor application with both the beautiful React frontend and the powerful FastAPI backend.

## 🏗️ **Architecture Overview**

- **Frontend**: React.js with beautiful modern UI (Port 3000)
- **Backend**: FastAPI with AI tutor functionality (Port 8000)
- **Communication**: REST API calls from frontend to backend

---

## ⚡ **Quick Start**

### **1. Backend Setup**

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create .env file with your API key:
echo 'EURIAI_API_KEY="your_euriai_api_key_here"' > .env

# Add syllabus PDFs to data/syllabi/ with format: Board_Grade_Subject.pdf
# Example: CBSE_10th_Science.pdf

# Process PDFs (run once when you add new PDFs)
python setup.py

# Start the backend server
python api.py
# Backend will run on http://localhost:8000
```

### **2. Frontend Setup** (in a new terminal)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the frontend development server
npm start
# Frontend will run on http://localhost:3000
```

---

## 🔗 **API Integration Details**

The frontend now makes real API calls to your backend:

### **Key API Endpoints Used:**
- `POST /verify_parent` - Parent authentication
- `POST /generate_roadmap` - AI-powered learning roadmaps
- `POST /chat_with_tutor` - AI chat responses
- `POST /generate_quiz` - Dynamic quiz generation
- `POST /calculate_quiz_score` - Quiz scoring with AI feedback
- `GET /get_video_for_subject` - Educational video retrieval
- `POST /buy_perk` - Gamification features
- And more...

### **Frontend Features Connected:**
- ✅ Beautiful loading states for all API calls
- ✅ Error handling with user-friendly messages
- ✅ Real-time chat with AI tutor
- ✅ Interactive quiz system with immediate feedback
- ✅ Personalized learning roadmap generation
- ✅ Gamification with coins and perks
- ✅ Parent dashboard with real analytics
- ✅ Video learning integration

---

## 🎯 **How to Use**

1. **Start Both Servers**: Make sure both backend (port 8000) and frontend (port 3000) are running
2. **Open Application**: Visit `http://localhost:3000` in your browser
3. **Set Up Learning**: Choose your grade, board, and subject
4. **Generate Roadmap**: Click "Create My Learning Plan" for AI-generated study plan
5. **Interactive Learning**: Use chat, quizzes, and videos powered by your backend AI
6. **Track Progress**: Earn coins, buy perks, and monitor learning analytics

---

## 🛠️ **Troubleshooting**

### **"API connection failed" errors:**
- Make sure backend is running on port 8000
- Check if `.env` file exists with valid `EURIAI_API_KEY`
- Verify PDFs are in `data/syllabi/` and `python setup.py` was run

### **Frontend won't start:**
- Run `npm install` in frontend directory
- Make sure Node.js is installed

### **CORS errors:**
- Backend includes CORS middleware for frontend communication
- If issues persist, restart both servers

### **No roadmap generated:**
- Ensure you have PDFs in the correct format in `data/syllabi/`
- Check backend logs for API key or PDF processing errors

---

## 📁 **Project Structure**

```
Agentic-AI-Tutor/
├── frontend/                 # React frontend
│   ├── src/App.js            # Main app with API integration
│   ├── package.json          # Frontend dependencies
│   └── public/               # Static assets
├── backend/                  # FastAPI backend
│   ├── api.py                # Main API server
│   ├── src/tutor/            # AI tutor logic
│   ├── data/syllabi/         # Your PDF syllabi
│   └── requirements.txt      # Backend dependencies
└── README_INTEGRATION.md     # This file
```

---

## 🌟 **Key Features Working**

- **AI-Powered Learning**: Real syllabus-based roadmaps and explanations
- **Beautiful UI**: Modern, responsive design with smooth animations
- **Real-time Chat**: Direct communication with AI tutor
- **Interactive Quizzes**: Dynamic question generation and scoring
- **Gamification**: Coin system, perks, and progress tracking
- **Parent Dashboard**: Analytics and monitoring for parents
- **Video Integration**: Educational video recommendations
- **Mobile Responsive**: Works perfectly on all devices

---

## 🚀 **Next Steps**

Your AI Tutor is now fully integrated! The beautiful frontend communicates seamlessly with your powerful AI backend. Students can now enjoy:

- Personalized learning experiences
- Real-time AI assistance
- Interactive educational content
- Gamified learning progression
- Comprehensive progress tracking

**Ready to revolutionize education!** 🎓✨