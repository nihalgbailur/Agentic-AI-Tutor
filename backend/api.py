"""
API backend for the Agentic AI Tutor, replacing the Gradio UI.
This exposes the core functionality via REST endpoints for a React frontend.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from datetime import datetime

from src.tutor.interface import tutor_interface

# Game state management
class GameState:
    def __init__(self):
        self.coins = 100  # Starting coins
        self.total_coins_earned = 100
        self.streak_days = 0
        self.quizzes_completed = 0
        self.videos_watched = 0
        self.current_level = 1
        self.unlocked_perks = []
        self.daily_progress = {"videos": 0, "quizzes": 0, "study_time": 0}
        self.attention_score = 100
        self.parent_authenticated = False
        
    def add_coins(self, amount):
        self.coins += amount
        self.total_coins_earned += amount
        
    def spend_coins(self, amount):
        if self.coins >= amount:
            self.coins -= amount
            return True
        return False

# Global game state
game_state = GameState()

# AI Tutor Initialization
try:
    tutor_ready = tutor_interface.retriever is not None
    print(f"🤖 AI Tutor System: {'✅ Ready' if tutor_ready else '❌ Not Ready'}")
except Exception as e:
    print(f"AI Tutor Initialization Error: {e}")
    tutor_ready = False

# Sample video content
SAMPLE_VIDEOS = {
    "Math": [
        {"title": "Fun with Fractions! 🥧", "duration": "15:30", "url": "https://www.youtube.com/embed/dQw4w9WgXcQ"},
        {"title": "Multiplication Magic ✨", "duration": "12:45", "url": "https://www.youtube.com/embed/dQw4w9WgXcQ"},
        {"title": "Geometry Adventures 📐", "duration": "18:20", "url": "https://www.youtube.com/embed/dQw4w9WgXcQ"}
    ],
    "Science": [
        {"title": "Amazing Animals 🦁", "duration": "16:15", "url": "https://www.youtube.com/embed/dQw4w9WgXcQ"},
        {"title": "Space Exploration 🚀", "duration": "14:30", "url": "https://www.youtube.com/embed/dQw4w9WgXcQ"},
        {"title": "Plant Life Cycle 🌱", "duration": "13:45", "url": "https://www.youtube.com/embed/dQw4w9WgXcQ"}
    ],
    "Social Studies": [
        {"title": "Indian History Heroes 🇮🇳", "duration": "17:00", "url": "https://www.youtube.com/embed/dQw4w9WgXcQ"},
        {"title": "Geography Fun 🗺️", "duration": "15:20", "url": "https://www.youtube.com/embed/dQw4w9WgXcQ"},
        {"title": "Culture & Traditions 🎭", "duration": "16:40", "url": "https://www.youtube.com/embed/dQw4w9WgXcQ"}
    ],
    "English": [
        {"title": "Story Time Adventures 📚", "duration": "14:15", "url": "https://www.youtube.com/embed/dQw4w9WgXcQ"},
        {"title": "Grammar Made Easy 📝", "duration": "12:30", "url": "https://www.youtube.com/embed/dQw4w9WgXcQ"},
        {"title": "Poetry Corner 🎵", "duration": "11:45", "url": "https://www.youtube.com/embed/dQw4w9WgXcQ"}
    ]
}

PERKS_SHOP = [
    {"name": "Golden Star Badge ⭐", "cost": 50, "description": "Show everyone you're a star student!"},
    {"name": "Super Learner Avatar 🦸", "cost": 100, "description": "Unlock a cool superhero avatar!"},
    {"name": "Speed Boost ⚡", "cost": 75, "description": "Get extra time for quizzes!"},
    {"name": "Hint Helper 💡", "cost": 30, "description": "Get one free hint per quiz!"},
    {"name": "Rainbow Theme 🌈", "cost": 80, "description": "Make your app colorful!"},
    {"name": "Music Mode 🎵", "cost": 60, "description": "Study with background music!"}
]

# Pydantic models for requests
class ParentPinRequest(BaseModel):
    pin: str

class VideoRequest(BaseModel):
    subject: str

class QuizRequest(BaseModel):
    subject: str
    grade: str

class QuizScoreRequest(BaseModel):
    answers: list[int]
    correct_answers: list[int]

class PerkBuyRequest(BaseModel):
    perk_index: int

class RoadmapRequest(BaseModel):
    grade: str
    board: str
    subject: str

class ChatRequest(BaseModel):
    message: str
    subject: str
    grade: str

# FastAPI app
app = FastAPI(title="Agentic AI Tutor API")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "tutor_ready": tutor_ready}

@app.post("/verify_parent")
def api_verify_parent(req: ParentPinRequest):
    if req.pin == "1234":
        game_state.parent_authenticated = True
        return {"success": True, "message": "✅ Parent access granted!"}
    return {"success": False, "message": "❌ Wrong PIN. Try again!"}

@app.post("/logout_parent")
def api_logout_parent():
    game_state.parent_authenticated = False
    return {"message": "👋 Parent logged out!"}

@app.get("/get_video_for_subject")
def api_get_video_for_subject(subject: str):
    if subject in SAMPLE_VIDEOS:
        video = random.choice(SAMPLE_VIDEOS[subject])
        return video
    return {"title": "Sample Video 📺", "duration": "15:00", "url": "https://www.youtube.com/embed/dQw4w9WgXcQ"}

@app.get("/simulate_attention_check")
def api_simulate_attention_check():
    attention_level = random.randint(60, 100)
    game_state.attention_score = attention_level
    
    if attention_level < 80:
        questions = [
            "Hey there! 👋 What was the last thing you learned?",
            "Quick check! 🧠 Can you tell me one interesting fact from the video?",
            "Stay focused! 💪 What do you think happens next?",
            "Attention buddy! 👀 What's your favorite part so far?"
        ]
        return {
            "needs_check": True,
            "socratic_question": random.choice(questions), 
            "attention_level": attention_level
        }
    return {
        "needs_check": False,
        "socratic_question": None,
        "attention_level": attention_level
    }

@app.post("/complete_video_watching")
def api_complete_video_watching(req: VideoRequest):
    coins_earned = 20
    game_state.add_coins(coins_earned)
    game_state.videos_watched += 1
    game_state.daily_progress["videos"] += 1
    return {"message": f"🎉 Great job! You earned {coins_earned} coins for watching the video! 🎉", "coins_earned": coins_earned, "coins": game_state.coins}

@app.post("/generate_quiz")
def api_generate_quiz(req: QuizRequest):
    if not req.subject or not req.grade:
        raise HTTPException(status_code=400, detail="Subject and grade are required")
    questions = tutor_interface.generate_quiz(grade=req.grade, subject=req.subject, num_questions=5)
    return {"questions": questions or []}

@app.post("/calculate_quiz_score")
def api_calculate_quiz_score(req: QuizScoreRequest):
    correct = sum(1 for a, c in zip(req.answers, req.correct_answers) if a == c)
    total = len(req.correct_answers)
    percentage = (correct / total) * 100 if total > 0 else 0
    
    if percentage >= 80:
        coins = 50
        emoji = "🎉"
        message = "Amazing! You're a superstar!"
    elif percentage >= 60:
        coins = 30
        emoji = "👏"
        message = "Great job! Keep it up!"
    elif percentage >= 40:
        coins = 20
        emoji = "👍"
        message = "Good effort! Try again to improve!"
    else:
        coins = 10
        emoji = "💪"
        message = "Keep practicing! You'll get better!"
    
    game_state.add_coins(coins)
    game_state.quizzes_completed += 1
    game_state.daily_progress["quizzes"] += 1
    
    return {
        "score": f"{correct}/{total}",
        "percentage": percentage,
        "coins_earned": coins,
        "emoji": emoji,
        "message": message
    }

@app.get("/coin_display")
def api_get_coin_display():
    return {"display": f"🪙 {game_state.coins} Coins", "coins": game_state.coins}

@app.post("/buy_perk")
def api_buy_perk(req: PerkBuyRequest):
    if 0 <= req.perk_index < len(PERKS_SHOP):
        perk = PERKS_SHOP[req.perk_index]
        if game_state.spend_coins(perk["cost"]):
            game_state.unlocked_perks.append(perk["name"])
            return {"message": f"🎉 You bought {perk['name']}! Enjoy your new perk!", "success": True}
        else:
            return {"message": f"❌ Not enough coins! You need {perk['cost']} coins but only have {game_state.coins}.", "success": False}
    return {"message": "❌ Invalid perk selection.", "success": False}

@app.get("/leaderboard")
def api_get_leaderboard():
    progress = f"""
    🏆 **Your Progress** 🏆
    
    📊 **Stats:**
    - 🪙 Total Coins Earned: {game_state.total_coins_earned}
    - 🎯 Quizzes Completed: {game_state.quizzes_completed}
    - 📺 Videos Watched: {game_state.videos_watched}
    - 🔥 Current Level: {game_state.current_level}
    
    🎁 **Unlocked Perks:** {', '.join(game_state.unlocked_perks) if game_state.unlocked_perks else 'None yet - visit the shop!'}
    
    📈 **Today's Progress:**
    - Videos: {game_state.daily_progress["videos"]} 📺
    - Quizzes: {game_state.daily_progress["quizzes"]} 🎯
    """
    return {"leaderboard": progress}

@app.get("/parent_dashboard")
def api_get_parent_dashboard():
    if not game_state.parent_authenticated:
        raise HTTPException(status_code=403, detail="🔒 Please log in as parent first!")
    
    dashboard = f"""
    👨‍👩‍👧‍👦 **Parent Dashboard** 👨‍👩‍👧‍👦
    
    📊 **Child's Progress:**
    - 🎯 Quizzes Completed: {game_state.quizzes_completed}
    - 📺 Videos Watched: {game_state.videos_watched}
    - 🪙 Coins Earned: {game_state.total_coins_earned}
    - 👀 Average Attention Score: {game_state.attention_score}%
    
    ⚙️ **Settings:**
    - Webcam Monitoring: {"✅ Enabled" if True else "❌ Disabled"}
    - Study Reminders: {"✅ Enabled" if True else "❌ Disabled"}
    - Screen Time Limit: 2 hours/day
    
    📈 **Weekly Summary:**
    Your child is doing great! They've maintained good focus and are learning consistently.
    
    💡 **Recommendations:**
    - Encourage more Science videos
    - Practice Math quizzes for better scores
    - Celebrate achievements with family time!
    """
    return {"dashboard": dashboard}

@app.post("/generate_roadmap")
def api_generate_roadmap(req: RoadmapRequest):
    if not tutor_ready:
        raise HTTPException(status_code=503, detail="The AI Tutor is not ready. Please check the setup.")
    if not all([req.grade, req.board, req.subject]):
        raise HTTPException(status_code=400, detail="Please select a grade, board, and subject to create a roadmap.")
    
    roadmap = tutor_interface.generate_learning_roadmap(req.grade, req.board, req.subject)
    return {"roadmap": roadmap}

@app.post("/chat_with_tutor")
def api_chat_with_tutor(req: ChatRequest):
    if not tutor_ready:
        return {"response": "The AI Tutor is currently offline. Please try again later."}
    
    try:
        bot_response = tutor_interface.chat_with_tutor(req.message, req.subject, req.grade)
        return {"response": bot_response}
    except Exception as e:
        # Fallback response if AI API fails
        fallback_responses = {
            "hello": f"Hello! I'm your AI tutor for {req.subject}. How can I help you learn today? 🤖",
            "hi": f"Hi there! Ready to explore {req.subject}? What would you like to learn? 📚",
            "help": f"I'm here to help you with {req.subject}! You can ask me questions about concepts, problems, or explanations. What specific topic interests you?",
        }
        
        response = fallback_responses.get(req.message.lower().strip(), 
            f"I understand you're asking about '{req.message}' in {req.subject}. While I'm having some connection issues with the advanced AI right now, I can still help! Could you be more specific about what you'd like to learn? 🎓")
        
        return {"response": response}

# Add more endpoints if needed (e.g., for daily progress reset, etc.)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AI Tutor API...")
    uvicorn.run("api:app", host="localhost", port=8000, reload=False)