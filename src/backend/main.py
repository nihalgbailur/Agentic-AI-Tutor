"""
Main Backend Integration Module
Integrates all backend components and provides unified API for the frontend
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import asyncio
from datetime import datetime

# Import all backend modules
from .syllabus_manager import SyllabusManager
from .attention_monitor import AttentionMonitor, get_attention_monitor
from .quiz_generator import QuizGenerator
from .gamification_engine import GamificationEngine, get_gamification_engine

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgenticTutorBackend:
    """
    Main backend class that integrates all components
    Provides unified API for the Gradio frontend
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        
        # Initialize all backend components
        logger.info("Initializing Agentic Tutor Backend...")
        
        try:
            self.syllabus_manager = SyllabusManager(data_dir)
            self.attention_monitor = get_attention_monitor()
            self.quiz_generator = QuizGenerator(data_dir)
            self.gamification_engine = get_gamification_engine()
            
            # Backend state
            self.current_session = {
                "grade": None,
                "board": None,
                "subject": None,
                "student_id": "default_student",
                "active_quiz": None,
                "video_session": None
            }
            
            # Parent settings
            self.parent_settings = self._load_parent_settings()
            
            logger.info("✅ Backend initialization complete")
            
        except Exception as e:
            logger.error(f"❌ Backend initialization failed: {e}")
            raise
    
    def _load_parent_settings(self) -> Dict:
        """Load parent control settings"""
        default_settings = {
            "webcam_enabled": True,
            "attention_monitoring": True,
            "study_time_limit": 120,  # minutes
            "daily_quiz_limit": 10,
            "content_filtering": True,
            "progress_reports": True,
            "difficulty_auto_adjust": True
        }
        
        # Load from file if exists
        settings_file = self.data_dir / "cache" / "parent_settings.json"
        try:
            if settings_file.exists():
                import json
                with open(settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    default_settings.update(loaded_settings)
        except Exception as e:
            logger.error(f"Failed to load parent settings: {e}")
        
        return default_settings
    
    def _save_parent_settings(self):
        """Save parent control settings"""
        try:
            import json
            settings_file = self.data_dir / "cache" / "parent_settings.json"
            settings_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(settings_file, 'w') as f:
                json.dump(self.parent_settings, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save parent settings: {e}")
    
    # ========================================
    # SYLLABUS MANAGEMENT API
    # ========================================
    
    def setup_learning_session(self, grade: str, board: str, subject: str) -> Dict:
        """
        Set up a new learning session with syllabus download and indexing
        
        Args:
            grade: Student's grade (5th, 6th, 7th, 8th)
            board: Education board (Karnataka State Board, ICSE)
            subject: Subject (Math, Science, Social Studies, English)
            
        Returns:
            Setup result with syllabus status
        """
        try:
            logger.info(f"Setting up learning session: {grade} {board} {subject}")
            
            # Update session state
            self.current_session.update({
                "grade": grade,
                "board": board,
                "subject": subject
            })
            
            # Download and index syllabus
            pdf_path = self.syllabus_manager.download_syllabus(board, grade, subject)
            
            if pdf_path:
                # Parse and index the syllabus
                indexing_success = self.syllabus_manager.parse_and_index_syllabus(pdf_path)
                
                if indexing_success:
                    # Get syllabus topics
                    topics = self.syllabus_manager.get_syllabus_topics(board, grade, subject)
                    
                    return {
                        "success": True,
                        "message": f"✅ Ready to learn {subject} for {grade} grade!",
                        "syllabus_available": True,
                        "topics_found": len(topics),
                        "topics": topics[:10],  # First 10 topics
                        "pdf_path": pdf_path
                    }
                else:
                    return {
                        "success": True,
                        "message": "⚠️ Syllabus downloaded but indexing failed. Using backup content.",
                        "syllabus_available": False,
                        "topics": [],
                        "pdf_path": pdf_path
                    }
            else:
                return {
                    "success": True,
                    "message": "⚠️ Could not download official syllabus. Using sample content.",
                    "syllabus_available": False,
                    "topics": [],
                    "pdf_path": None
                }
                
        except Exception as e:
            logger.error(f"Failed to setup learning session: {e}")
            return {
                "success": False,
                "message": f"❌ Setup failed: {str(e)}",
                "syllabus_available": False
            }
    
    def generate_learning_roadmap(self, grade: str = None, board: str = None, subject: str = None) -> str:
        """
        Generate personalized learning roadmap using RAG
        
        Returns:
            Formatted learning roadmap as markdown string
        """
        try:
            # Use session data if not provided
            grade = grade or self.current_session["grade"]
            board = board or self.current_session["board"]
            subject = subject or self.current_session["subject"]
            
            if not all([grade, board, subject]):
                return "❌ Please set up your learning session first!"
            
            # Query syllabus for relevant content
            topics_query = f"topics chapters units {subject} {grade}"
            syllabus_content = self.syllabus_manager.query_syllabus(
                topics_query, board, grade, subject, top_k=10
            )
            
            # Get student progress for personalization
            student_stats = self.gamification_engine.get_student_stats()
            quiz_report = self.quiz_generator.get_student_report(subject, grade)
            
            # Generate roadmap based on content and progress
            roadmap = self._create_personalized_roadmap(
                grade, board, subject, syllabus_content, student_stats, quiz_report
            )
            
            return roadmap
            
        except Exception as e:
            logger.error(f"Failed to generate roadmap: {e}")
            return f"❌ Failed to generate roadmap: {str(e)}"
    
    def _create_personalized_roadmap(self, grade: str, board: str, subject: str, 
                                   syllabus_content: List[Dict], student_stats: Dict, 
                                   quiz_report: Dict) -> str:
        """Create personalized learning roadmap"""
        
        # Extract topics from syllabus content
        topics = []
        if syllabus_content:
            for content in syllabus_content:
                text = content['text']
                # Simple topic extraction (could be enhanced with NLP)
                lines = text.split('\n')
                for line in lines:
                    if any(keyword in line.lower() for keyword in ['chapter', 'unit', 'topic', 'lesson']):
                        if len(line.strip()) < 100:
                            topics.append(line.strip())
        
        # If no topics from syllabus, use default topics
        if not topics:
            default_topics = {
                "Math": ["Numbers and Operations", "Algebra Basics", "Geometry", "Measurement", "Data and Graphs"],
                "Science": ["Living Things", "Matter and Energy", "Earth and Space", "Forces and Motion", "Environment"],
                "Social Studies": ["History", "Geography", "Civics", "Economics", "Culture"],
                "English": ["Reading Comprehension", "Grammar", "Writing", "Speaking", "Literature"]
            }
            topics = default_topics.get(subject, ["General Topics"])
        
        # Remove duplicates and limit
        topics = list(dict.fromkeys(topics))[:8]
        
        # Analyze student level
        level = student_stats.get('level', 1)
        total_quizzes = student_stats.get('total_quizzes', 0)
        
        if total_quizzes == 0:
            experience_level = "Beginner"
            focus = "Building foundation"
        elif total_quizzes < 10:
            experience_level = "Learning"
            focus = "Practicing basics"
        elif level < 5:
            experience_level = "Intermediate"
            focus = "Strengthening concepts"
        else:
            experience_level = "Advanced"
            focus = "Mastering skills"
        
        # Create roadmap
        roadmap = f"""
# 🎯 **Your Personalized Learning Roadmap**
## {subject} - {grade} Grade ({board})

---

### 👋 **Welcome, Young Scholar!**
You're at the **{experience_level}** level! Your current focus: **{focus}**

📊 **Your Progress So Far:**
- 🏆 Level: {level}
- 🎯 Quizzes Completed: {total_quizzes}
- 🪙 Coins Earned: {student_stats.get('total_coins', 0)}
- 🔥 Study Streak: {student_stats.get('streak_days', 0)} days

---

### 📚 **Learning Path for This Month**

"""
        
        # Add weekly breakdown
        weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
        topics_per_week = len(topics) // 4 if len(topics) >= 4 else 1
        
        for i, week in enumerate(weeks):
            start_idx = i * topics_per_week
            end_idx = start_idx + topics_per_week if i < 3 else len(topics)
            week_topics = topics[start_idx:end_idx]
            
            if week_topics:
                roadmap += f"\n#### 🗓️ **{week}**\n"
                roadmap += f"**Focus Areas:**\n"
                for topic in week_topics:
                    roadmap += f"- 📖 {topic}\n"
                
                roadmap += f"\n**Weekly Goals:**\n"
                roadmap += f"- ✅ Complete 2-3 quizzes on these topics\n"
                roadmap += f"- 📺 Watch 1-2 educational videos\n"
                roadmap += f"- 💪 Practice for 20-30 minutes daily\n\n"
        
        # Add weak areas if available
        if quiz_report and quiz_report.get('weak_topics'):
            roadmap += "\n### 🎯 **Extra Practice Needed**\n"
            roadmap += "Based on your quiz performance, focus more on:\n"
            for topic in quiz_report['weak_topics'][:3]:
                roadmap += f"- 🔄 {topic} (needs improvement)\n"
            roadmap += "\n"
        
        # Add daily routine
        roadmap += """
### 📅 **Daily Learning Routine**

**🌅 Start Your Day:**
1. 📝 Review yesterday's learning (5 minutes)
2. 🎯 Set today's learning goal

**🎓 Study Time (20-30 minutes):**
1. 📖 Read/review concepts (10 minutes)
2. 📺 Watch educational video (5-10 minutes)
3. 🧠 Take practice quiz (5-10 minutes)

**🌙 End Your Day:**
1. ✨ Review what you learned
2. 🎉 Celebrate your progress!

---

### 🏆 **Motivation & Tips**

💡 **Study Tips:**
- 🍎 Take breaks every 20 minutes
- 🗣️ Explain concepts out loud
- ✍️ Take notes in your own words
- 🤝 Study with family or friends

🎮 **Gamification Goals:**
- 🎯 Complete daily quizzes to earn coins
- 🔥 Maintain your study streak
- 🏅 Unlock new achievements
- 🛍️ Buy cool perks in the shop

💪 **Remember:** Every expert was once a beginner. You're doing great! 🌟

---

*This roadmap is personalized based on your progress and will update as you learn more!*
"""
        
        return roadmap.strip()
    
    # ========================================
    # QUIZ AND ASSESSMENT API
    # ========================================
    
    def create_quiz(self, difficulty: str = "auto", num_questions: int = 5) -> Dict:
        """
        Create a new quiz based on current session
        
        Args:
            difficulty: Difficulty level or "auto"
            num_questions: Number of questions
            
        Returns:
            Quiz data for frontend
        """
        try:
            if not all([self.current_session["grade"], self.current_session["board"], self.current_session["subject"]]):
                return {"error": "Please set up your learning session first!"}
            
            # Generate quiz
            quiz_session = self.quiz_generator.generate_quiz(
                self.current_session["grade"],
                self.current_session["board"],
                self.current_session["subject"],
                difficulty,
                num_questions
            )
            
            # Store active quiz
            self.current_session["active_quiz"] = quiz_session
            
            # Format for frontend
            questions_data = []
            for i, question in enumerate(quiz_session.questions):
                questions_data.append({
                    "id": i,
                    "question": question.question,
                    "options": question.options,
                    "topic": question.topic,
                    "difficulty": question.difficulty
                })
            
            return {
                "success": True,
                "quiz_id": quiz_session.session_id,
                "subject": quiz_session.subject,
                "difficulty": quiz_session.difficulty_level,
                "total_questions": quiz_session.total_questions,
                "questions": questions_data,
                "topics": quiz_session.topics_covered
            }
            
        except Exception as e:
            logger.error(f"Failed to create quiz: {e}")
            return {"error": f"Failed to create quiz: {str(e)}"}
    
    def submit_quiz(self, answers: List[int], time_taken: float) -> Dict:
        """
        Submit quiz answers and get results
        
        Args:
            answers: List of selected answer indices
            time_taken: Time taken in seconds
            
        Returns:
            Quiz results and gamification updates
        """
        try:
            if not self.current_session["active_quiz"]:
                return {"error": "No active quiz found!"}
            
            quiz_session = self.current_session["active_quiz"]
            
            # Score the quiz
            quiz_result = self.quiz_generator.score_quiz(quiz_session, answers, time_taken)
            
            # Update gamification
            coins_earned = quiz_result.get("coins_earned", 0)
            percentage = quiz_result.get("percentage", 0)
            
            # Award coins with potential multipliers
            multipliers = {}
            if percentage == 100:
                multipliers["perfect_score"] = 2.0
            
            gamification_result = self.gamification_engine.award_coins(
                coins_earned, 
                f"Quiz completion - {percentage:.0f}%",
                multipliers
            )
            
            # Update activity tracking
            self.gamification_engine.update_activity("quiz", score=percentage)
            
            # Clear active quiz
            self.current_session["active_quiz"] = None
            
            # Combine results
            combined_result = {
                **quiz_result,
                "gamification": gamification_result,
                "new_achievements": gamification_result.get("new_achievements", []),
                "current_coins": gamification_result.get("current_coins", 0),
                "level": gamification_result.get("level", 1)
            }
            
            return combined_result
            
        except Exception as e:
            logger.error(f"Failed to submit quiz: {e}")
            return {"error": f"Failed to submit quiz: {str(e)}"}
    
    def generate_revision_summary(self, focus_topics: List[str] = None) -> Dict:
        """
        Generate revision summary for current subject
        
        Args:
            focus_topics: Specific topics to focus on
            
        Returns:
            Revision content
        """
        try:
            grade = self.current_session["grade"]
            board = self.current_session["board"]
            subject = self.current_session["subject"]
            
            if not all([grade, board, subject]):
                return {"error": "Please set up your learning session first!"}
            
            revision = self.quiz_generator.generate_revision_summary(
                grade, board, subject, focus_topics
            )
            
            return {
                "success": True,
                "revision": revision
            }
            
        except Exception as e:
            logger.error(f"Failed to generate revision: {e}")
            return {"error": f"Failed to generate revision: {str(e)}"}
    
    # ========================================
    # ATTENTION MONITORING API
    # ========================================
    
    def start_attention_monitoring(self) -> Dict:
        """Start attention monitoring if enabled"""
        try:
            if not self.parent_settings.get("attention_monitoring", True):
                return {
                    "success": False,
                    "message": "Attention monitoring disabled by parent"
                }
            
            if not self.parent_settings.get("webcam_enabled", True):
                return {
                    "success": False,
                    "message": "Webcam disabled by parent"
                }
            
            success = self.attention_monitor.start_monitoring()
            
            if success:
                return {
                    "success": True,
                    "message": "Attention monitoring started"
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to start attention monitoring"
                }
                
        except Exception as e:
            logger.error(f"Failed to start attention monitoring: {e}")
            return {"success": False, "message": str(e)}
    
    def stop_attention_monitoring(self) -> Dict:
        """Stop attention monitoring"""
        try:
            self.attention_monitor.stop_monitoring()
            return {"success": True, "message": "Attention monitoring stopped"}
        except Exception as e:
            logger.error(f"Failed to stop attention monitoring: {e}")
            return {"success": False, "message": str(e)}
    
    def get_attention_level(self) -> float:
        """Get current attention level (0-100)"""
        try:
            return self.attention_monitor.get_attention_level()
        except Exception as e:
            logger.error(f"Failed to get attention level: {e}")
            return 50.0  # Default neutral level
    
    def get_attention_report(self) -> Dict:
        """Get comprehensive attention report"""
        try:
            return self.attention_monitor.get_attention_report()
        except Exception as e:
            logger.error(f"Failed to get attention report: {e}")
            return {"error": str(e)}
    
    # ========================================
    # GAMIFICATION API
    # ========================================
    
    def get_student_dashboard(self) -> Dict:
        """Get comprehensive student dashboard data"""
        try:
            stats = self.gamification_engine.get_student_stats()
            achievements = self.gamification_engine.get_achievements_summary()
            available_perks = self.gamification_engine.get_available_perks()
            leaderboard = self.gamification_engine.get_leaderboard("total_coins", 10)
            
            return {
                "stats": stats,
                "achievements": achievements,
                "available_perks": available_perks[:6],  # Top 6 perks
                "leaderboard": leaderboard,
                "current_session": self.current_session
            }
            
        except Exception as e:
            logger.error(f"Failed to get student dashboard: {e}")
            return {"error": str(e)}
    
    def purchase_perk(self, perk_id: str) -> Dict:
        """Purchase a perk with coins"""
        try:
            result = self.gamification_engine.purchase_perk(perk_id)
            return result
        except Exception as e:
            logger.error(f"Failed to purchase perk: {e}")
            return {"success": False, "error": str(e)}
    
    def get_leaderboard(self, metric: str = "total_coins") -> List[Dict]:
        """Get leaderboard for specified metric"""
        try:
            leaderboard = self.gamification_engine.get_leaderboard(metric, 10)
            return [asdict(entry) for entry in leaderboard]
        except Exception as e:
            logger.error(f"Failed to get leaderboard: {e}")
            return []
    
    # ========================================
    # VIDEO LEARNING API
    # ========================================
    
    def start_video_session(self, video_url: str, video_title: str) -> Dict:
        """Start a video learning session with attention tracking"""
        try:
            # Start attention monitoring if enabled
            attention_result = self.start_attention_monitoring()
            
            # Create video session
            self.current_session["video_session"] = {
                "url": video_url,
                "title": video_title,
                "start_time": datetime.now(),
                "attention_alerts": 0,
                "total_attention": 0
            }
            
            return {
                "success": True,
                "message": f"Started video session: {video_title}",
                "attention_monitoring": attention_result.get("success", False)
            }
            
        except Exception as e:
            logger.error(f"Failed to start video session: {e}")
            return {"success": False, "error": str(e)}
    
    def complete_video_session(self) -> Dict:
        """Complete video session and award coins"""
        try:
            if not self.current_session["video_session"]:
                return {"error": "No active video session"}
            
            video_session = self.current_session["video_session"]
            
            # Calculate watch time
            start_time = video_session["start_time"]
            watch_time = (datetime.now() - start_time).total_seconds() / 60  # minutes
            
            # Base coins for video completion
            base_coins = 20
            
            # Bonus for good attention
            attention_level = self.get_attention_level()
            attention_bonus = 1.0
            if attention_level >= 80:
                attention_bonus = 1.5
            elif attention_level >= 60:
                attention_bonus = 1.2
            
            # Award coins
            total_coins = int(base_coins * attention_bonus)
            gamification_result = self.gamification_engine.award_coins(
                total_coins,
                f"Video completion: {video_session['title']}",
                {"attention_bonus": attention_bonus}
            )
            
            # Update activity
            self.gamification_engine.update_activity("video", minutes=watch_time)
            
            # Stop attention monitoring
            self.stop_attention_monitoring()
            
            # Clear video session
            self.current_session["video_session"] = None
            
            return {
                "success": True,
                "coins_earned": total_coins,
                "watch_time_minutes": round(watch_time, 1),
                "attention_level": round(attention_level, 1),
                "attention_bonus": attention_bonus,
                "gamification": gamification_result
            }
            
        except Exception as e:
            logger.error(f"Failed to complete video session: {e}")
            return {"error": str(e)}
    
    def check_attention_alert(self) -> Dict:
        """Check if attention alert should be triggered"""
        try:
            if not self.current_session.get("video_session"):
                return {"alert": False}
            
            attention_level = self.get_attention_level()
            
            # Trigger alert if attention is low
            if attention_level < 50:
                # Generate Socratic question
                subject = self.current_session.get("subject", "general")
                questions = [
                    f"What's the most interesting thing you've learned about {subject} so far?",
                    "Can you think of a real-world example of what you just watched?",
                    "What question would you ask if the teacher was here right now?",
                    "How does this topic connect to something you already know?",
                    "If you had to explain this to a friend, what would you say?"
                ]
                
                import random
                question = random.choice(questions)
                
                # Update alert count
                self.current_session["video_session"]["attention_alerts"] += 1
                
                return {
                    "alert": True,
                    "attention_level": attention_level,
                    "question": question,
                    "alert_count": self.current_session["video_session"]["attention_alerts"]
                }
            
            return {"alert": False, "attention_level": attention_level}
            
        except Exception as e:
            logger.error(f"Failed to check attention alert: {e}")
            return {"alert": False, "error": str(e)}
    
    # ========================================
    # PARENT CONTROLS API
    # ========================================
    
    def update_parent_settings(self, **settings) -> Dict:
        """Update parent control settings"""
        try:
            self.parent_settings.update(settings)
            self._save_parent_settings()
            
            # Apply settings immediately
            if "attention_monitoring" in settings or "webcam_enabled" in settings:
                if not settings.get("attention_monitoring", True) or not settings.get("webcam_enabled", True):
                    self.stop_attention_monitoring()
            
            return {
                "success": True,
                "message": "Parent settings updated",
                "settings": self.parent_settings
            }
            
        except Exception as e:
            logger.error(f"Failed to update parent settings: {e}")
            return {"success": False, "error": str(e)}
    
    def get_parent_dashboard(self) -> Dict:
        """Get parent dashboard with progress and controls"""
        try:
            student_stats = self.gamification_engine.get_student_stats()
            attention_report = self.get_attention_report()
            
            # Get subject-wise progress
            subjects = ["Math", "Science", "Social Studies", "English"]
            subject_progress = {}
            
            for subject in subjects:
                quiz_report = self.quiz_generator.get_student_report(subject, self.current_session.get("grade", "6th"))
                subject_progress[subject] = quiz_report
            
            return {
                "student_stats": student_stats,
                "attention_report": attention_report,
                "subject_progress": subject_progress,
                "settings": self.parent_settings,
                "session_info": self.current_session
            }
            
        except Exception as e:
            logger.error(f"Failed to get parent dashboard: {e}")
            return {"error": str(e)}
    
    def export_progress_report(self) -> str:
        """Export comprehensive progress report"""
        try:
            dashboard_data = self.get_parent_dashboard()
            
            # Format as readable report
            report = f"""
# Student Progress Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overall Statistics
- Current Level: {dashboard_data['student_stats']['level']}
- Total Coins Earned: {dashboard_data['student_stats']['total_coins']}
- Study Streak: {dashboard_data['student_stats']['streak_days']} days
- Total Quizzes: {dashboard_data['student_stats']['total_quizzes']}
- Total Videos: {dashboard_data['student_stats']['total_videos']}
- Study Time: {dashboard_data['student_stats']['study_minutes']} minutes

## Subject Performance
"""
            
            for subject, progress in dashboard_data.get('subject_progress', {}).items():
                if 'total_quizzes' in progress and progress['total_quizzes'] > 0:
                    report += f"""
### {subject}
- Quizzes Completed: {progress['total_quizzes']}
- Average Score: {progress['average_score']:.1f}%
- Current Difficulty: {progress['current_difficulty']}
- Strong Topics: {', '.join(progress.get('strong_topics', ['None']))}
- Areas for Improvement: {', '.join(progress.get('weak_topics', ['None']))}
"""
            
            if 'attention_report' in dashboard_data and dashboard_data['attention_report']:
                attention = dashboard_data['attention_report']
                report += f"""
## Attention & Focus
- Average Attention: {attention.get('average_attention', 0):.1f}%
- Peak Attention: {attention.get('peak_attention', 0):.1f}%
- Attention Alerts: {attention.get('total_alerts', 0)}
- Recommendation: {attention.get('recommendation', 'Keep up the good work!')}
"""
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to export progress report: {e}")
            return f"Error generating report: {str(e)}"

# Global backend instance
_backend_instance = None

def get_backend() -> AgenticTutorBackend:
    """Get global backend instance"""
    global _backend_instance
    if _backend_instance is None:
        _backend_instance = AgenticTutorBackend()
    return _backend_instance

# Convenience functions for frontend integration
def setup_learning(grade: str, board: str, subject: str) -> Dict:
    """Setup learning session - convenient frontend function"""
    return get_backend().setup_learning_session(grade, board, subject)

def generate_roadmap(grade: str = None, board: str = None, subject: str = None) -> str:
    """Generate learning roadmap - convenient frontend function"""
    return get_backend().generate_learning_roadmap(grade, board, subject)

def create_quiz(difficulty: str = "auto", num_questions: int = 5) -> Dict:
    """Create quiz - convenient frontend function"""
    return get_backend().create_quiz(difficulty, num_questions)

def submit_quiz(answers: List[int], time_taken: float) -> Dict:
    """Submit quiz - convenient frontend function"""
    return get_backend().submit_quiz(answers, time_taken)

def get_student_dashboard() -> Dict:
    """Get student dashboard - convenient frontend function"""
    return get_backend().get_student_dashboard()

def start_video_session(video_url: str, video_title: str) -> Dict:
    """Start video session - convenient frontend function"""
    return get_backend().start_video_session(video_url, video_title)

def complete_video_session() -> Dict:
    """Complete video session - convenient frontend function"""
    return get_backend().complete_video_session()

def check_attention_alert() -> Dict:
    """Check attention alert - convenient frontend function"""
    return get_backend().check_attention_alert()

def purchase_perk(perk_id: str) -> Dict:
    """Purchase perk - convenient frontend function"""
    return get_backend().purchase_perk(perk_id)

def get_parent_dashboard() -> Dict:
    """Get parent dashboard - convenient frontend function"""
    return get_backend().get_parent_dashboard()

def update_parent_settings(**settings) -> Dict:
    """Update parent settings - convenient frontend function"""
    return get_backend().update_parent_settings(**settings)

# Test function
def test_backend():
    """Test the integrated backend system"""
    print("🧪 Testing Agentic Tutor Backend...")
    
    backend = AgenticTutorBackend()
    
    # Test learning session setup
    print("\n1. Testing learning session setup...")
    setup_result = backend.setup_learning_session("6th", "Karnataka State Board", "Math")
    print(f"Setup result: {setup_result['success']}")
    
    # Test roadmap generation
    print("\n2. Testing roadmap generation...")
    roadmap = backend.generate_learning_roadmap()
    print(f"Roadmap length: {len(roadmap)} characters")
    
    # Test quiz creation
    print("\n3. Testing quiz creation...")
    quiz_result = backend.create_quiz("medium", 3)
    print(f"Quiz created: {quiz_result.get('success', False)}")
    
    # Test quiz submission
    if quiz_result.get('success'):
        print("\n4. Testing quiz submission...")
        sample_answers = [0, 1, 0]  # Sample answers
        submit_result = backend.submit_quiz(sample_answers, 60.0)
        print(f"Quiz score: {submit_result.get('percentage', 0)}%")
    
    # Test student dashboard
    print("\n5. Testing student dashboard...")
    dashboard = backend.get_student_dashboard()
    print(f"Student level: {dashboard['stats']['level']}")
    print(f"Current coins: {dashboard['stats']['current_coins']}")
    
    # Test attention monitoring
    print("\n6. Testing attention monitoring...")
    attention_start = backend.start_attention_monitoring()
    print(f"Attention monitoring: {attention_start['success']}")
    
    if attention_start['success']:
        import time
        time.sleep(2)  # Brief monitoring
        attention_level = backend.get_attention_level()
        print(f"Attention level: {attention_level}%")
        backend.stop_attention_monitoring()
    
    print("\n✅ Backend testing complete!")

if __name__ == "__main__":
    test_backend()