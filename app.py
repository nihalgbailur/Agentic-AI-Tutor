import gradio as gr
import time
import random
from datetime import datetime
from src.agents.tutor_agent import TutorAgent
from src.agents.crew_tutor_agent import CrewTutorAgent, AutoGenTutorWrapper

# Kid-friendly CSS with bright colors and large buttons
CSS = """
.gradio-container { 
    max-width: 1200px !important; 
    margin: 0 auto !important; 
    font-family: 'Comic Sans MS', cursive, sans-serif !important;
    background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%) !important;
}

.main-title {
    background: linear-gradient(45deg, #00BFFF, #90EE90) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-size: 2.5em !important;
    font-weight: bold !important;
    text-align: center !important;
    margin: 20px 0 !important;
}

.big-button { 
    background: linear-gradient(45deg, #00BFFF, #1E90FF) !important; 
    color: white !important; 
    border-radius: 20px !important; 
    font-weight: bold !important;
    font-size: 18px !important;
    padding: 15px 30px !important;
    border: none !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    transition: all 0.3s ease !important;
}

.big-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 12px rgba(0,0,0,0.3) !important;
}

.success-button {
    background: linear-gradient(45deg, #90EE90, #32CD32) !important;
    color: white !important;
    border-radius: 20px !important;
    font-weight: bold !important;
    font-size: 18px !important;
    padding: 15px 30px !important;
}

.warning-button {
    background: linear-gradient(45deg, #FFB347, #FF8C00) !important;
    color: white !important;
    border-radius: 20px !important;
    font-weight: bold !important;
    font-size: 18px !important;
}

.kid-card {
    background: white !important;
    border-radius: 20px !important;
    padding: 20px !important;
    margin: 10px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    border: 3px solid #00BFFF !important;
}

.coin-display {
    background: linear-gradient(45deg, #FFD700, #FFA500) !important;
    color: #8B4513 !important;
    font-size: 24px !important;
    font-weight: bold !important;
    padding: 10px 20px !important;
    border-radius: 15px !important;
    text-align: center !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
}

.progress-bar {
    background: #e0e0e0 !important;
    border-radius: 10px !important;
    height: 20px !important;
    overflow: hidden !important;
}

.progress-fill {
    background: linear-gradient(45deg, #90EE90, #32CD32) !important;
    height: 100% !important;
    transition: width 0.3s ease !important;
}

.tab-nav {
    background: #00BFFF !important;
    color: white !important;
    font-size: 16px !important;
    font-weight: bold !important;
    border-radius: 15px 15px 0 0 !important;
}

.quiz-card {
    background: linear-gradient(135deg, #FFE4E1, #FFF0F5) !important;
    border-radius: 15px !important;
    padding: 20px !important;
    margin: 10px 0 !important;
    border-left: 5px solid #FF69B4 !important;
}

.attention-alert {
    background: linear-gradient(45deg, #FF6B6B, #FF8E8E) !important;
    color: white !important;
    border-radius: 15px !important;
    padding: 20px !important;
    text-align: center !important;
    font-size: 18px !important;
    font-weight: bold !important;
    animation: pulse 2s infinite !important;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

.parent-lock {
    background: linear-gradient(45deg, #8B4513, #A0522D) !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 15px !important;
    font-weight: bold !important;
}

.leaderboard-table {
    background: white !important;
    border-radius: 15px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
}

.video-container {
    border-radius: 20px !important;
    overflow: hidden !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
    background: black !important;
}

.webcam-preview {
    position: absolute !important;
    top: 20px !important;
    right: 20px !important;
    width: 200px !important;
    height: 150px !important;
    border-radius: 15px !important;
    border: 3px solid #00BFFF !important;
    background: #000 !important;
}

/* Make text larger for kids */
.gradio-container * {
    font-size: 16px !important;
}

.gradio-container h1, .gradio-container h2, .gradio-container h3 {
    color: #2E8B57 !important;
    font-weight: bold !important;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .gradio-container {
        max-width: 100% !important;
        padding: 10px !important;
    }
    
    .big-button {
        font-size: 16px !important;
        padding: 12px 20px !important;
    }
    
    .coin-display {
        font-size: 18px !important;
    }
}
"""

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

# Initialize AI Tutors (Basic + Advanced CrewAI)
try:
    # Basic single-agent tutor
    tutor_agent = TutorAgent()
    basic_ready = tutor_agent.retriever is not None
    
    # Advanced multi-agent CrewAI system
    crew_tutor = CrewTutorAgent()
    crew_ready = crew_tutor.retriever is not None and len(crew_tutor.agents) > 0
    
    # AutoGen wrapper for advanced integrations
    autogen_wrapper = AutoGenTutorWrapper(crew_tutor) if crew_ready else None
    
    print(f"🤖 Basic Tutor: {'✅' if basic_ready else '❌'}")
    print(f"🚀 CrewAI System: {'✅' if crew_ready else '❌'}")
    print(f"🔄 AutoGen Support: {'✅' if autogen_wrapper else '❌'}")
    
except Exception as e:
    print(f"Setup error: {e}")
    tutor_agent = None
    crew_tutor = None
    autogen_wrapper = None
    basic_ready = False
    crew_ready = False

# Sample quiz questions for different subjects
SAMPLE_QUIZZES = {
    "Math": [
        {"question": "What is 15 + 27? 🧮", "options": ["42", "41", "43", "40"], "correct": 0},
        {"question": "If a pizza has 8 slices and you eat 3, how many are left? 🍕", "options": ["4", "5", "6", "7"], "correct": 1},
        {"question": "What is 7 × 6? ✖️", "options": ["42", "36", "48", "35"], "correct": 0},
        {"question": "What is half of 24? ➗", "options": ["12", "10", "14", "11"], "correct": 0},
        {"question": "How many sides does a triangle have? 📐", "options": ["2", "3", "4", "5"], "correct": 1}
    ],
    "Science": [
        {"question": "What do plants need to make food? 🌱", "options": ["Sunlight", "Water", "Air", "All of the above"], "correct": 3},
        {"question": "Which planet is closest to the Sun? ☀️", "options": ["Venus", "Mercury", "Earth", "Mars"], "correct": 1},
        {"question": "What gas do we breathe in? 💨", "options": ["Carbon dioxide", "Oxygen", "Nitrogen", "Helium"], "correct": 1},
        {"question": "How many bones are in an adult human body? 🦴", "options": ["206", "205", "207", "204"], "correct": 0},
        {"question": "What is the largest mammal? 🐋", "options": ["Elephant", "Blue whale", "Giraffe", "Rhino"], "correct": 1}
    ],
    "Social Studies": [
        {"question": "Who was the first President of India? 🇮🇳", "options": ["Mahatma Gandhi", "Dr. Rajendra Prasad", "Nehru", "Dr. Kalam"], "correct": 1},
        {"question": "Which river is called the 'Ganga of the South'? 🏞️", "options": ["Krishna", "Godavari", "Cauvery", "Narmada"], "correct": 1},
        {"question": "In which year did India gain independence? 📅", "options": ["1946", "1947", "1948", "1949"], "correct": 1},
        {"question": "What is the capital of Karnataka? 🏛️", "options": ["Mumbai", "Chennai", "Bangalore", "Hyderabad"], "correct": 2},
        {"question": "Which freedom fighter is known as 'Father of the Nation'? 👨", "options": ["Subhas Chandra Bose", "Bhagat Singh", "Mahatma Gandhi", "Nehru"], "correct": 2}
    ],
    "English": [
        {"question": "What is the plural of 'child'? 👶", "options": ["childs", "children", "childes", "child"], "correct": 1},
        {"question": "Which is a verb in this sentence: 'The dog runs fast'? 🏃", "options": ["dog", "runs", "fast", "the"], "correct": 1},
        {"question": "What type of word is 'quickly'? ⚡", "options": ["noun", "verb", "adjective", "adverb"], "correct": 3},
        {"question": "Which word rhymes with 'cat'? 🐱", "options": ["dog", "bat", "bird", "fish"], "correct": 1},
        {"question": "What is the opposite of 'happy'? 😊", "options": ["glad", "sad", "excited", "calm"], "correct": 1}
    ]
}

# Sample video content (in real app, these would be YouTube/educational video URLs)
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

# Parent authentication
def verify_parent_pin(pin):
    """Verify parent PIN (default: 1234 for MVP)"""
    if pin == "1234":
        game_state.parent_authenticated = True
        return True, "✅ Parent access granted!"
    return False, "❌ Wrong PIN. Try again!"

def logout_parent():
    """Logout parent"""
    game_state.parent_authenticated = False
    return "👋 Parent logged out!"

# Video and attention monitoring
def get_video_for_subject(subject):
    """Get random video for subject"""
    if subject in SAMPLE_VIDEOS:
        video = random.choice(SAMPLE_VIDEOS[subject])
        return video
    return {"title": "Sample Video 📺", "duration": "15:00", "url": "https://www.youtube.com/embed/dQw4w9WgXcQ"}

def simulate_attention_check():
    """Simulate attention monitoring (in real app, this would use webcam/AI)"""
    # Simulate random attention dips
    attention_level = random.randint(60, 100)
    game_state.attention_score = attention_level
    
    if attention_level < 80:
        questions = [
            "Hey there! 👋 What was the last thing you learned?",
            "Quick check! 🧠 Can you tell me one interesting fact from the video?",
            "Stay focused! 💪 What do you think happens next?",
            "Attention buddy! 👀 What's your favorite part so far?"
        ]
        return random.choice(questions)
    return None

def complete_video_watching(subject):
    """Award coins for watching video"""
    coins_earned = 20
    game_state.add_coins(coins_earned)
    game_state.videos_watched += 1
    game_state.daily_progress["videos"] += 1
    return f"🎉 Great job! You earned {coins_earned} coins for watching the video! 🎉"

# Quiz functionality
def generate_quiz(subject, grade=None):
    """Generate quiz questions for subject"""
    if subject in SAMPLE_QUIZZES:
        questions = random.sample(SAMPLE_QUIZZES[subject], min(5, len(SAMPLE_QUIZZES[subject])))
        return questions
    return []

def calculate_quiz_score(answers, correct_answers):
    """Calculate quiz score and award coins"""
    correct = sum(1 for a, c in zip(answers, correct_answers) if a == c)
    total = len(correct_answers)
    percentage = (correct / total) * 100 if total > 0 else 0
    
    # Award coins based on performance
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
        "coins": coins,
        "emoji": emoji,
        "message": message
    }

# Gamification functions
def get_coin_display():
    """Get current coin display"""
    return f"🪙 {game_state.coins} Coins"

def buy_perk(perk_index):
    """Buy a perk from the shop"""
    if 0 <= perk_index < len(PERKS_SHOP):
        perk = PERKS_SHOP[perk_index]
        if game_state.spend_coins(perk["cost"]):
            game_state.unlocked_perks.append(perk["name"])
            return f"🎉 You bought {perk['name']}! Enjoy your new perk!"
        else:
            return f"❌ Not enough coins! You need {perk['cost']} coins but only have {game_state.coins}."
    return "❌ Invalid perk selection."

def get_leaderboard():
    """Get personal leaderboard/progress"""
    return f"""
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

def get_parent_dashboard():
    """Get parent dashboard data"""
    if not game_state.parent_authenticated:
        return "🔒 Please log in as parent first!"
    
    return f"""
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

# Enhanced learning functions (keeping compatibility with existing backend)
def generate_roadmap_interface(grade, board, subject, use_crewai=True):
    """Generate roadmap with option for basic or advanced multi-agent system."""
    if not basic_ready and not crew_ready:
        return "⚠️ Setup needed - check README for instructions"
    if not all([grade, board, subject]):
        return "Please select grade, board, and subject first"
    
    # Use CrewAI if available and requested, otherwise fallback to basic
    if use_crewai and crew_ready:
        yield "🚀 Activating specialized AI tutors..."
        yield f"🎓 Consulting {subject} expert agent..."
        roadmap = crew_tutor.generate_advanced_roadmap(grade, board, subject)
        yield roadmap
    elif basic_ready:
        yield "🧠 Creating your learning plan..."
        roadmap = tutor_agent.generate_roadmap(grade, board, subject)
        yield roadmap
    else:
        yield "❌ No tutor agents available. Please check setup."

def chat_with_tutor(message, history, grade, board, subject, use_crewai=True, age=10):
    """Handle chat messages using appropriate tutor system."""
    if not basic_ready and not crew_ready:
        bot_response = "🤖 Hi! I need to be set up first. Ask a grown-up to help!"
    elif use_crewai and crew_ready:
        # Use specialized subject agent
        bot_response = crew_tutor.multi_agent_chat(message, grade, board, subject, age)
    elif basic_ready:
        # Use basic single agent
        bot_response = tutor_agent.chat_with_kid(message, grade, board, subject)
    else:
        bot_response = "❌ No tutor agents available."
    
    # Convert to messages format
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": bot_response})
    return "", history

def cross_subject_activity(topic, subject1, subject2, grade):
    """Generate cross-subject learning activities using CrewAI."""
    if not crew_ready:
        return "⚠️ Advanced multi-agent system needed for cross-subject activities."
    
    if not all([topic, subject1, subject2, grade]):
        return "Please fill in all fields for cross-subject activity."
    
    return crew_tutor.cross_subject_learning(topic, subject1, subject2, grade)

def show_agent_expertise(subject=""):
    """Show information about available AI tutor agents."""
    if crew_ready:
        return crew_tutor.get_agent_expertise(subject if subject else None)
    else:
        return "⚠️ Advanced agent system not available. Only basic tutor is active."

with gr.Blocks(css=CSS, theme=gr.themes.Soft(), title="Agentic AI Tutor - Your After-School Adventure! 🚀") as demo:
    
    # State variables for the app
    current_screen = gr.State("welcome")
    quiz_questions = gr.State([])
    quiz_answers = gr.State([])
    current_video = gr.State({})
    user_grade = gr.State("")
    user_board = gr.State("")
    user_subject = gr.State("")
    
    # Welcome Screen
    with gr.Group(visible=True) as welcome_screen:
        gr.HTML("""
        <div style="text-align: center; padding: 40px;">
            <h1 class="main-title">🚀 Agentic AI Tutor - Your After-School Adventure! 🚀</h1>
            <p style="font-size: 20px; color: #2E8B57; margin: 20px 0;">
                Welcome to the most fun way to learn! 🌟<br/>
                Watch videos, take quizzes, earn coins, and become a learning superstar! 💫
            </p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                pass  # Empty space for centering
            with gr.Column(scale=2):
                start_guest_btn = gr.Button(
                    "🎮 Start as Guest - Let's Learn!", 
                    elem_classes=["big-button"],
                    size="lg"
                )
                gr.Markdown("*No login needed - jump right into learning!*")
                
                with gr.Accordion("👨‍👩‍👧‍👦 Parent Login", open=False):
                    parent_pin = gr.Textbox(
                        label="🔐 Enter Parent PIN", 
                        type="password", 
                        placeholder="Enter PIN (default: 1234)",
                        max_lines=1
                    )
                    parent_login_btn = gr.Button("🔓 Parent Login", elem_classes=["parent-lock"])
                    parent_status = gr.Markdown("")
            with gr.Column(scale=1):
                pass  # Empty space for centering
    
    # Selection Screen
    with gr.Group(visible=False) as selection_screen:
        gr.HTML("""
        <div style="text-align: center; padding: 30px;">
            <h2 style="color: #2E8B57;">📚 Let's Set Up Your Learning Adventure! 📚</h2>
            <p style="font-size: 18px;">Tell us about yourself so we can create the perfect learning experience!</p>
        </div>
        """)
        
        with gr.Row():
            grade_dd = gr.Dropdown(
                label="📚 What grade are you in?", 
                choices=["5th", "6th", "7th", "8th"],
                elem_classes=["kid-card"]
            )
            board_dd = gr.Dropdown(
                label="🏫 What school board?", 
                choices=["Karnataka State Board", "ICSE"],
                elem_classes=["kid-card"]
            )
            subject_dd = gr.Dropdown(
                label="📖 What subject do you want to explore today?", 
                choices=["Math", "Science", "Social Studies", "English"],
                elem_classes=["kid-card"]
            )
        
        begin_btn = gr.Button(
            "🌟 Begin My Learning Journey!", 
            elem_classes=["big-button"],
            size="lg"
        )
        selection_status = gr.Markdown("")
    
    # Main Learning Interface
    with gr.Group(visible=False) as main_interface:
        # Top navigation with coin display
        with gr.Row():
            coin_display = gr.Markdown(get_coin_display(), elem_classes=["coin-display"])
            gr.Markdown("") # Spacer
            back_to_home_btn = gr.Button("🏠 Home", size="sm")
        
        # Main content tabs
        with gr.Tabs() as main_tabs:
            # Home/Dashboard Tab
            with gr.TabItem("🏠 Home", elem_classes=["tab-nav"]):
                gr.Markdown("### 🌟 Welcome to Your Learning Dashboard! 🌟")
                
                # Quick stats
                with gr.Row():
                    with gr.Column():
                        daily_progress = gr.Markdown("""
                        📈 **Today's Progress:**
                        - Videos Watched: 0 📺
                        - Quizzes Completed: 0 🎯
                        - Coins Earned: 0 🪙
                        """, elem_classes=["kid-card"])
                    
                    with gr.Column():
                        quick_actions = gr.HTML("""
                        <div class="kid-card">
                            <h3>🚀 Quick Actions</h3>
                            <p>Ready to learn something new?</p>
                        </div>
                        """)
                
                # Generate learning plan
                with gr.Group():
                    gr.Markdown("### 📅 Get Your Personalized Learning Plan!")
                    plan_btn = gr.Button("🎯 Create My Learning Plan!", elem_classes=["success-button"], size="lg")
                    learning_plan = gr.Markdown("Click above to get your customized study plan! 📚")
            
            # Video Learning Tab
            with gr.TabItem("📺 Watch & Learn", elem_classes=["tab-nav"]):
                gr.Markdown("### 🎬 Educational Videos - Learn by Watching! 🎬")
                
                # Video selection and player
                with gr.Row():
                    with gr.Column(scale=3):
                        video_title = gr.Markdown("**Select a video to start learning!**")
                        video_player = gr.HTML("""
                        <div class="video-container" style="height: 400px; display: flex; align-items: center; justify-content: center; background: #f0f0f0; border-radius: 20px;">
                            <p style="font-size: 18px; color: #666;">🎬 Video will appear here 🎬</p>
                        </div>
                        """)
                        
                        # Video controls
                        with gr.Row():
                            load_video_btn = gr.Button("📺 Load Video for Current Subject", elem_classes=["big-button"])
                            complete_video_btn = gr.Button("✅ I Finished Watching!", elem_classes=["success-button"])
                    
                    with gr.Column(scale=1):
                        # Attention monitoring (simulated)
                        gr.Markdown("### 👀 Focus Helper")
                        attention_monitor = gr.HTML("""
                        <div class="webcam-preview" style="position: relative; width: 100%; height: 200px; background: #000; border-radius: 15px; display: flex; align-items: center; justify-content: center;">
                            <p style="color: white; text-align: center;">📹 Attention Monitor<br/>(Simulated)</p>
                        </div>
                        """)
                        
                        attention_status = gr.Markdown("✅ Great focus! Keep it up! 👍")
                        check_attention_btn = gr.Button("🔍 Check My Focus", size="sm")
                
                # Attention alerts and Socratic questions
                attention_alert = gr.Markdown("", visible=False, elem_classes=["attention-alert"])
                socratic_question = gr.Textbox(
                    label="💭 Quick Thinking Question",
                    placeholder="Answer will appear here when you need a focus check...",
                    visible=False,
                    lines=3
                )
                answer_socratic_btn = gr.Button("💡 Submit Answer", visible=False, elem_classes=["warning-button"])
                
                video_completion_msg = gr.Markdown("")
            
            # Quiz Tab
            with gr.TabItem("🎯 Quiz Time", elem_classes=["tab-nav"]):
                gr.Markdown("### 🧠 Test Your Knowledge - Quiz Challenge! 🧠")
                
                # Quiz interface
                with gr.Group():
                    quiz_intro = gr.Markdown("""
                    🎯 **Ready for a fun quiz?** 
                    
                    Answer questions about what you've learned and earn coins! 
                    The better you do, the more coins you get! 💰
                    """, elem_classes=["quiz-card"])
                    
                    start_quiz_btn = gr.Button("🚀 Start Quiz!", elem_classes=["big-button"], size="lg")
                    
                    # Quiz questions (initially hidden)
                    quiz_container = gr.Group(visible=False)
                    with quiz_container:
                        quiz_timer = gr.Markdown("⏰ Time: 10:00")
                        current_question = gr.Markdown("")
                        
                        # Answer options
                        answer_option_0 = gr.Button("", visible=False, elem_classes=["quiz-card"])
                        answer_option_1 = gr.Button("", visible=False, elem_classes=["quiz-card"])
                        answer_option_2 = gr.Button("", visible=False, elem_classes=["quiz-card"])
                        answer_option_3 = gr.Button("", visible=False, elem_classes=["quiz-card"])
                        
                        quiz_progress = gr.Markdown("")
                        submit_quiz_btn = gr.Button("📝 Submit Quiz", elem_classes=["success-button"], visible=False)
                    
                    # Quiz results
                    quiz_results = gr.Markdown("")
            
            # Rewards/Gamification Tab
            with gr.TabItem("🏆 Rewards & Shop", elem_classes=["tab-nav"]):
                gr.Markdown("### 🎁 Your Rewards & Achievements! 🎁")
                
                with gr.Row():
                    # Progress display
                    with gr.Column():
                        progress_display = gr.Markdown(get_leaderboard(), elem_classes=["kid-card"])
                        refresh_progress_btn = gr.Button("🔄 Refresh Progress", size="sm")
                    
                    # Perk shop
                    with gr.Column():
                        gr.Markdown("### 🛍️ Perk Shop")
                        shop_display = gr.HTML(f"""
                        <div class="kid-card">
                            {''.join([f'''
                            <div style="margin: 10px 0; padding: 15px; background: #f9f9f9; border-radius: 10px; border-left: 4px solid #FFD700;">
                                <strong>{perk["name"]}</strong><br/>
                                <small>{perk["description"]}</small><br/>
                                <span style="color: #FF8C00; font-weight: bold;">💰 {perk["cost"]} coins</span>
                            </div>
                            ''' for i, perk in enumerate(PERKS_SHOP)])}
                        </div>
                        """)
                        
                        perk_selector = gr.Dropdown(
                            label="Choose a perk to buy:",
                            choices=[f"{i}: {perk['name']} ({perk['cost']} coins)" for i, perk in enumerate(PERKS_SHOP)],
                            value=None
                        )
                        buy_perk_btn = gr.Button("💳 Buy Perk!", elem_classes=["warning-button"])
                        perk_result = gr.Markdown("")
            
            # Chat Tab (Enhanced from original)
            with gr.TabItem("💬 Chat with AI Tutor", elem_classes=["tab-nav"]):
                gr.Markdown("### 🤖 Ask Your AI Tutor Anything! 🤖")
                
                chatbot = gr.Chatbot(
                    height=400,
                    placeholder="👋 Hi there! I'm your friendly AI tutor! Ask me anything about your studies! 😊",
                    elem_classes=["chat-bubble"],
                    type="messages"
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="Ask me about Math, Science, or anything you're curious about!",
                        label="💭 Your Question",
                        scale=4,
                        lines=2
                    )
                    send_btn = gr.Button("📤 Send", elem_classes=["big-button"], scale=1)
                
                clear_chat_btn = gr.Button("🧹 Clear Chat", size="sm")
            
            # Parent Dashboard (Protected)
            with gr.TabItem("👨‍👩‍👧‍👦 Parent Dashboard", elem_classes=["tab-nav"]):
                parent_dashboard_content = gr.Markdown(get_parent_dashboard(), elem_classes=["parent-lock"])
                logout_parent_btn = gr.Button("🚪 Logout Parent", visible=False, elem_classes=["warning-button"])
    
    # Event Handlers
    def switch_to_selection():
        return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)
    
    def handle_parent_login(pin):
        success, message = verify_parent_pin(pin)
        return message
    
    def setup_learning(grade, board, subject):
        if not all([grade, board, subject]):
            return "❌ Please select all options!", gr.update(visible=True), gr.update(visible=False), "", "", ""
        
        # Store selections
        return (
            f"✅ Great! Let's start learning {subject} for {grade} grade!",
            gr.update(visible=False),
            gr.update(visible=True),
            grade, board, subject
        )
    
    def load_video_for_subject(subject):
        if not subject:
            return "Please select a subject first!", "", ""
        
        video = get_video_for_subject(subject)
        video_html = f"""
        <div class="video-container">
            <iframe width="100%" height="400" 
                    src="{video['url']}" 
                    frameborder="0" 
                    allowfullscreen>
            </iframe>
        </div>
        """
        return f"**Now Playing: {video['title']} ({video['duration']})**", video_html, video
    
    def check_attention():
        alert = simulate_attention_check()
        if alert:
            return (
                gr.update(value=f"🚨 **Focus Check!** 🚨\n\n{alert}", visible=True),
                gr.update(visible=True),
                gr.update(visible=True),
                "⚠️ Pay attention! Answer the question above."
            )
        else:
            return (
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                "✅ Excellent focus! Keep watching! 👍"
            )
    
    def handle_socratic_answer(answer):
        if answer.strip():
            return (
                gr.update(visible=False),
                gr.update(value="", visible=False),
                gr.update(visible=False),
                "👏 Great answer! Back to learning!"
            )
        return "", "", "", "Please write an answer first!"
    
    def start_quiz_session(subject):
        if not subject:
            return "Please select a subject first!", gr.update(visible=False), [], ""
        
        questions = generate_quiz(subject)
        if not questions:
            return "No quiz available for this subject yet!", gr.update(visible=False), [], ""
        
        first_question = questions[0]
        question_display = f"""
        **Question 1 of {len(questions)}:**
        
        {first_question['question']}
        """
        
        return (
            "",
            gr.update(visible=True),
            questions,
            question_display,
            gr.update(value=first_question['options'][0], visible=True),
            gr.update(value=first_question['options'][1], visible=True),
            gr.update(value=first_question['options'][2], visible=True),
            gr.update(value=first_question['options'][3], visible=True),
            f"📊 Progress: 0/{len(questions)} answered"
        )
    
    def submit_quiz_final(questions, answers):
        if not questions or not answers:
            return "No quiz data available!"
        
        correct_answers = [q['correct'] for q in questions]
        result = calculate_quiz_score(answers, correct_answers)
        
        result_text = f"""
        ## 🎉 Quiz Complete! 🎉
        
        **Your Score:** {result['score']} ({result['percentage']:.0f}%)
        
        **{result['emoji']} {result['message']} {result['emoji']}**
        
        **Coins Earned:** 🪙 {result['coins']}
        
        **Total Coins:** 🪙 {game_state.coins}
        
        ---
        
        ### 📊 Question Review:
        {''.join([f"**Q{i+1}:** {q['question']}<br/>**Your answer:** {q['options'][answers[i]] if i < len(answers) else 'Not answered'}<br/>**Correct:** {q['options'][q['correct']]}<br/><br/>" for i, q in enumerate(questions)])}
        """
        
        return result_text, get_coin_display()
    
    def update_coin_display():
        return get_coin_display()
    
    def buy_selected_perk(perk_selection):
        if not perk_selection:
            return "Please select a perk first!"
        
        perk_index = int(perk_selection.split(":")[0])
        result = buy_perk(perk_index)
        return result
    
    # Connect all the events
    start_guest_btn.click(
        fn=switch_to_selection,
        outputs=[welcome_screen, selection_screen, main_interface]
    )
    
    parent_login_btn.click(
        fn=handle_parent_login,
        inputs=[parent_pin],
        outputs=[parent_status]
    )
    
    begin_btn.click(
        fn=setup_learning,
        inputs=[grade_dd, board_dd, subject_dd],
        outputs=[selection_status, selection_screen, main_interface, user_grade, user_board, user_subject]
    )
    
    load_video_btn.click(
        fn=load_video_for_subject,
        inputs=[user_subject],
        outputs=[video_title, video_player, current_video]
    )
    
    complete_video_btn.click(
        fn=lambda s: (complete_video_watching(s), update_coin_display()),
        inputs=[user_subject],
        outputs=[video_completion_msg, coin_display]
    )
    
    check_attention_btn.click(
        fn=check_attention,
        outputs=[attention_alert, socratic_question, answer_socratic_btn, attention_status]
    )
    
    answer_socratic_btn.click(
        fn=handle_socratic_answer,
        inputs=[socratic_question],
        outputs=[attention_alert, socratic_question, answer_socratic_btn, attention_status]
    )
    
    start_quiz_btn.click(
        fn=lambda s: start_quiz_session(s),
        inputs=[user_subject],
        outputs=[quiz_intro, quiz_container, quiz_questions, current_question, 
                answer_option_0, answer_option_1, answer_option_2, answer_option_3, quiz_progress]
    )
    
    refresh_progress_btn.click(
        fn=get_leaderboard,
        outputs=[progress_display]
    )
    
    buy_perk_btn.click(
        fn=buy_selected_perk,
        inputs=[perk_selector],
        outputs=[perk_result]
    )
    
    # Chat functionality (enhanced from original)
    send_btn.click(
        fn=chat_with_tutor,
        inputs=[msg, chatbot, user_grade, user_board, user_subject, gr.State(True), gr.State(12)],
        outputs=[msg, chatbot]
    )
    
    msg.submit(
        fn=chat_with_tutor,
        inputs=[msg, chatbot, user_grade, user_board, user_subject, gr.State(True), gr.State(12)],
        outputs=[msg, chatbot]
    )
    
    clear_chat_btn.click(
        fn=lambda: ([], ""),
        outputs=[chatbot, msg]
    )
    
    # Learning plan generation (from original)
    plan_btn.click(
        fn=generate_roadmap_interface,
        inputs=[user_grade, user_board, user_subject, gr.State(True)],
        outputs=[learning_plan]
    )

if __name__ == "__main__":
    print("🚀 Starting AI Tutor...")
    demo.launch(debug=True)
