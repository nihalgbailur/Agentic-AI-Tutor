# 🚀 Agentic AI Tutor - Advanced Backend System

## 📋 Overview

This advanced backend system extends your existing AI tutor with comprehensive features for syllabus management, attention monitoring, gamification, and adaptive learning. The system is built with modular architecture and integrates seamlessly with your existing Gradio frontend.

## 🏗️ Architecture

```
src/backend/
├── __init__.py                 # Package initialization
├── main.py                     # Main integration & API layer
├── syllabus_manager.py         # PDF download, parsing, RAG indexing
├── attention_monitor.py        # OpenCV attention tracking
├── quiz_generator.py           # Adaptive quiz generation
├── gamification_engine.py     # Coins, perks, achievements
└── test_backend.py            # Comprehensive testing suite
```

## 🔧 Components

### 1. Syllabus Manager (`syllabus_manager.py`)
- **Download**: Fetches official syllabi from education boards
- **Parse**: Extracts text from PDFs using PyPDF2
- **Index**: Creates FAISS vector database with embeddings
- **Query**: RAG-powered syllabus content retrieval

**Key Features:**
- Multi-board support (Karnataka, ICSE)
- Fallback sample content when downloads fail
- Semantic search across syllabus content
- Topic extraction and organization

### 2. Attention Monitor (`attention_monitor.py`)
- **Face Detection**: OpenCV-based face/eye tracking
- **Attention Scoring**: Real-time attention level calculation
- **Alert System**: Socratic question triggers for low attention
- **Privacy-First**: Local processing, optional webcam

**Key Features:**
- Configurable sensitivity levels
- Attention trend analysis
- Parental controls for webcam usage
- Simulation mode for testing without camera

### 3. Quiz Generator (`quiz_generator.py`)
- **Adaptive Difficulty**: Adjusts based on student performance
- **Subject-Specific**: 400+ questions across Math, Science, Social Studies, English
- **Progress Tracking**: Individual student analytics
- **Revision System**: Personalized study recommendations

**Key Features:**
- Grade-wise question banks (5th-8th)
- Multiple difficulty levels (easy, medium, hard)
- Topic-based weak area identification
- Detailed performance analytics

### 4. Gamification Engine (`gamification_engine.py`)
- **Coin System**: Earn coins for activities (videos: 20, quizzes: 10-50)
- **Achievement System**: 10+ unlockable achievements
- **Perk Shop**: 10+ purchasable upgrades and cosmetics
- **Leaderboards**: Multi-metric ranking system

**Key Features:**
- Level progression with XP system
- Streak tracking and bonuses
- Daily challenges and rewards
- Parent-controlled spending limits

### 5. Main Integration (`main.py`)
- **Unified API**: Single interface for all backend features
- **Session Management**: Learning session state tracking
- **Parent Controls**: Comprehensive parental oversight
- **Error Handling**: Robust error recovery and logging

## 🚀 Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Backend
```python
from src.backend.main import AgenticTutorBackend

# Initialize backend
backend = AgenticTutorBackend()

# Setup learning session
result = backend.setup_learning_session("6th", "Karnataka State Board", "Math")
```

### 3. Test Installation
```bash
python src/backend/test_backend.py
```

## 🔌 Frontend Integration

### Quick Integration with Your Existing App

Add these imports to your `app.py`:

```python
# Add to imports
from src.backend.main import (
    setup_learning, generate_roadmap, create_quiz, 
    submit_quiz, get_student_dashboard, start_video_session,
    complete_video_session, check_attention_alert, purchase_perk
)
```

### Enhanced Functions for Your Existing Features

Replace your existing functions with these enhanced versions:

```python
# Enhanced roadmap generation
def generate_roadmap_interface(grade, board, subject, use_crewai=True):
    """Enhanced with syllabus RAG integration"""
    if use_crewai and crew_ready:
        # Use your existing CrewAI system
        roadmap = crew_tutor.generate_advanced_roadmap(grade, board, subject)
        return roadmap
    else:
        # Use new backend with RAG
        setup_learning(grade, board, subject)
        return generate_roadmap(grade, board, subject)

# Enhanced quiz system
def start_quiz_session(subject):
    """Enhanced with adaptive difficulty"""
    quiz_data = create_quiz("auto", 5)  # Auto-adjusting difficulty
    if quiz_data.get('success'):
        return quiz_data
    else:
        # Fallback to your existing system
        return generate_quiz(subject)

# Enhanced video completion
def complete_video_watching(subject):
    """Enhanced with attention tracking and coins"""
    result = complete_video_session()
    if result.get('success'):
        coins = result.get('coins_earned', 20)
        return f"🎉 Great job! Earned {coins} coins! Attention: {result.get('attention_level', 100):.0f}%"
    else:
        # Fallback to existing system
        return complete_video_watching_original(subject)
```

### New Features You Can Add

```python
# New gamification tab content
def get_enhanced_rewards():
    """Get comprehensive rewards data"""
    dashboard = get_student_dashboard()
    return {
        'coins': dashboard['stats']['current_coins'],
        'level': dashboard['stats']['level'],
        'achievements': dashboard['achievements'],
        'available_perks': dashboard['available_perks']
    }

# New parent dashboard
def get_parent_control_panel():
    """Get parent oversight panel"""
    from src.backend.main import get_parent_dashboard
    return get_parent_dashboard()

# Attention monitoring for videos
def monitor_video_attention():
    """Check attention during video watching"""
    alert_data = check_attention_alert()
    if alert_data.get('alert'):
        return alert_data['question']  # Socratic question
    return None
```

## 🎮 Key Features in Action

### 1. Adaptive Learning Flow
```python
# Student starts session
setup_learning("6th", "Karnataka State Board", "Math")

# Generate personalized roadmap using RAG
roadmap = generate_roadmap()

# Create adaptive quiz
quiz = create_quiz("auto", 5)

# Submit and get personalized feedback
result = submit_quiz([0, 1, 2, 0, 1], 120.0)
# Result includes: score, coins, level up, weak topics, next difficulty
```

### 2. Attention-Aware Video Learning
```python
# Start video with attention monitoring
start_video_session("video_url", "Fractions Basics")

# Periodic attention checks (call every 30 seconds)
alert = check_attention_alert()
if alert['alert']:
    show_socratic_question(alert['question'])

# Complete session with attention-based rewards
result = complete_video_session()
# Coins vary based on attention level: 20-30 coins
```

### 3. Comprehensive Gamification
```python
# Get student progress
dashboard = get_student_dashboard()
# Shows: level, coins, achievements, streaks, progress

# Purchase perks
purchase_perk("speed_boost")  # Extra quiz time
purchase_perk("hint_helper")  # Quiz hints
purchase_perk("double_coins") # 2x coins for 24 hours
```

## 📊 Data Storage

### Local Files Created
```
data/
├── syllabi/              # Downloaded PDFs
│   ├── Karnataka_State_Board_6th_Math.pdf
│   └── ICSE_7th_Science.pdf
├── vector_store/         # FAISS indices
│   ├── syllabus.index
│   └── metadata.json
└── cache/               # Game & progress data
    ├── gamification.json
    ├── quiz_progress.json
    ├── attention_settings.json
    └── parent_settings.json
```

## 🔒 Privacy & Parental Controls

### Privacy Features
- **Local Processing**: All data stays on device
- **Optional Webcam**: Parents can disable attention monitoring
- **No Personal Data**: Anonymous student profiles
- **Secure Storage**: Local JSON files only

### Parent Controls
```python
# Update parental settings
update_parent_settings(
    webcam_enabled=True,
    attention_monitoring=True,
    study_time_limit=120,  # minutes per day
    daily_quiz_limit=10,
    difficulty_auto_adjust=True
)

# Get comprehensive parent dashboard
parent_data = get_parent_dashboard()
# Includes: progress, attention reports, time spent, recommendations
```

## 🧪 Testing

### Run Complete Test Suite
```bash
python src/backend/test_backend.py
```

### Test Individual Components
```python
# Test syllabus system
from src.backend.syllabus_manager import test_syllabus_manager
test_syllabus_manager()

# Test quiz system  
from src.backend.quiz_generator import test_quiz_generator
test_quiz_generator()

# Test gamification
from src.backend.gamification_engine import test_gamification_engine
test_gamification_engine()
```

## 🎯 Sample Usage Scenarios

### Scenario 1: New Student Journey
1. Student selects grade/board/subject → **setup_learning()**
2. System downloads/indexes syllabus → **SyllabusManager**
3. Generates personalized roadmap → **generate_roadmap()**
4. Student watches video → **start_video_session() + attention monitoring**
5. Takes adaptive quiz → **create_quiz() + submit_quiz()**
6. Earns coins and achievements → **GamificationEngine**
7. Parents review progress → **get_parent_dashboard()**

### Scenario 2: Returning Student
1. System loads previous progress → **GamificationEngine**
2. Adapts difficulty based on history → **QuizGenerator**
3. Focuses on weak topics → **generate_revision_summary()**
4. Maintains study streak → **update_activity()**
5. Unlocks new achievements → **check_achievements()**

## 🔮 Future Enhancements

### Planned Features
- **Voice Commands**: Speech recognition for accessibility
- **Mobile App**: React Native frontend
- **Teacher Dashboard**: Classroom management
- **Content Creator Tools**: Custom quiz/video creation
- **Advanced Analytics**: Learning pattern analysis
- **Multi-Language Support**: Regional language content

### Integration Opportunities
- **Google Classroom**: Assignment sync
- **Khan Academy**: Video integration  
- **Zoom**: Virtual classroom features
- **WhatsApp**: Progress notifications for parents

## 🐛 Troubleshooting

### Common Issues

**Issue**: "No module named 'backend'"
```bash
# Solution: Install in development mode
pip install -e .
```

**Issue**: OpenCV camera access denied
```bash
# Solution: Grant camera permissions or disable webcam
update_parent_settings(webcam_enabled=False)
```

**Issue**: FAISS index corruption
```bash
# Solution: Clear and rebuild index
rm data/vector_store/*
python -c "from src.backend.main import setup_learning; setup_learning('6th', 'Karnataka', 'Math')"
```

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now all backend operations will show detailed logs
```

## 📚 API Reference

### Core Functions
- `setup_learning(grade, board, subject)` → Setup learning session
- `generate_roadmap()` → Create personalized study plan  
- `create_quiz(difficulty, num_questions)` → Generate adaptive quiz
- `submit_quiz(answers, time_taken)` → Score quiz and update progress
- `get_student_dashboard()` → Comprehensive student stats
- `start_video_session(url, title)` → Begin attention-monitored video
- `complete_video_session()` → End video and award coins
- `purchase_perk(perk_id)` → Buy upgrades with coins
- `get_parent_dashboard()` → Parent oversight panel

### Advanced Functions
- `check_attention_alert()` → Get real-time attention status
- `generate_revision_summary()` → Create focused study guide
- `update_parent_settings(**settings)` → Configure parental controls
- `export_progress_report()` → Generate comprehensive report

## 🤝 Contributing

### Code Structure
- **Modular Design**: Each component is independent
- **Error Handling**: Comprehensive try/catch blocks  
- **Logging**: Detailed operation logs
- **Testing**: Unit tests for all components
- **Documentation**: Inline code documentation

### Adding New Features
1. Create new module in `src/backend/`
2. Add tests in `test_backend.py`
3. Integrate in `main.py`
4. Update this README

---

## 🎉 Conclusion

This backend system transforms your AI tutor from a simple chat interface into a comprehensive, adaptive learning platform. With features like attention monitoring, gamification, and personalized content delivery, it provides an engaging and effective learning experience while maintaining privacy and parental control.

The modular architecture ensures easy integration with your existing CrewAI system while providing extensive new capabilities that will keep students engaged and learning effectively.

**Ready to supercharge your AI tutor? Let's make learning an adventure! 🚀**