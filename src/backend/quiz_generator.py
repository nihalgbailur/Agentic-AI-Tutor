"""
Quiz and Revision Generator Module
Creates adaptive quizzes and revision summaries using LLM and RAG
"""

import json
import random
import logging
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import re

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Question:
    """Data class for quiz questions"""
    id: str
    question: str
    options: List[str]
    correct_answer: int
    explanation: str
    difficulty: str
    topic: str
    question_type: str  # 'mcq', 'short_answer', 'true_false'

@dataclass
class QuizSession:
    """Data class for quiz session data"""
    session_id: str
    grade: str
    board: str
    subject: str
    questions: List[Question]
    user_answers: List[int]
    score: int
    total_questions: int
    time_taken: float
    timestamp: datetime
    difficulty_level: str
    topics_covered: List[str]

@dataclass
class StudentProgress:
    """Data class for student progress tracking"""
    subject: str
    total_quizzes: int
    average_score: float
    strong_topics: List[str]
    weak_topics: List[str]
    last_quiz_date: datetime
    improvement_trend: str
    recommended_difficulty: str

class QuizGenerator:
    """Generates adaptive quizzes and tracks student progress"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.cache_dir = self.data_dir / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Load question banks
        self.question_banks = self._load_question_banks()
        
        # Load student progress
        self.student_progress = self._load_student_progress()
        
        # Quiz settings
        self.default_quiz_length = 10
        self.difficulty_levels = ["easy", "medium", "hard"]
        self.question_types = ["mcq", "true_false", "short_answer"]
        
        # Adaptive learning parameters
        self.score_thresholds = {
            "easy": {"promote": 80, "demote": 40},
            "medium": {"promote": 85, "demote": 50},
            "hard": {"promote": 90, "demote": 60}
        }
    
    def _load_question_banks(self) -> Dict:
        """Load pre-built question banks"""
        question_banks = {
            "Math": {
                "5th": self._get_math_questions_5th(),
                "6th": self._get_math_questions_6th(),
                "7th": self._get_math_questions_7th(),
                "8th": self._get_math_questions_8th()
            },
            "Science": {
                "5th": self._get_science_questions_5th(),
                "6th": self._get_science_questions_6th(),
                "7th": self._get_science_questions_7th(),
                "8th": self._get_science_questions_8th()
            },
            "Social Studies": {
                "5th": self._get_social_questions_5th(),
                "6th": self._get_social_questions_6th(),
                "7th": self._get_social_questions_7th(),
                "8th": self._get_social_questions_8th()
            },
            "English": {
                "5th": self._get_english_questions_5th(),
                "6th": self._get_english_questions_6th(),
                "7th": self._get_english_questions_7th(),
                "8th": self._get_english_questions_8th()
            }
        }
        return question_banks
    
    def _get_math_questions_5th(self) -> List[Question]:
        """Math questions for 5th grade"""
        return [
            Question(
                id="math_5_1", 
                question="What is 15 + 27?",
                options=["42", "41", "43", "40"],
                correct_answer=0,
                explanation="15 + 27 = 42. Add the ones place: 5 + 7 = 12, write 2 carry 1. Add tens: 1 + 2 + 1 = 4.",
                difficulty="easy",
                topic="Addition",
                question_type="mcq"
            ),
            Question(
                id="math_5_2",
                question="If a pizza has 8 slices and you eat 3, how many are left?",
                options=["4", "5", "6", "7"],
                correct_answer=1,
                explanation="8 - 3 = 5. When you subtract 3 from 8, you get 5 slices remaining.",
                difficulty="easy",
                topic="Subtraction",
                question_type="mcq"
            ),
            Question(
                id="math_5_3",
                question="What is 7 × 6?",
                options=["42", "36", "48", "35"],
                correct_answer=0,
                explanation="7 × 6 = 42. You can think of it as 7 groups of 6 or 6 groups of 7.",
                difficulty="medium",
                topic="Multiplication",
                question_type="mcq"
            ),
            Question(
                id="math_5_4",
                question="Which fraction is larger: 1/2 or 1/4?",
                options=["1/2", "1/4", "They are equal", "Cannot determine"],
                correct_answer=0,
                explanation="1/2 is larger than 1/4. Half of something is bigger than a quarter of the same thing.",
                difficulty="medium",
                topic="Fractions",
                question_type="mcq"
            ),
            Question(
                id="math_5_5",
                question="How many sides does a triangle have?",
                options=["2", "3", "4", "5"],
                correct_answer=1,
                explanation="A triangle has 3 sides. That's why it's called a triangle - 'tri' means three.",
                difficulty="easy",
                topic="Geometry",
                question_type="mcq"
            )
        ]
    
    def _get_math_questions_6th(self) -> List[Question]:
        """Math questions for 6th grade"""
        return [
            Question(
                id="math_6_1",
                question="What is 144 ÷ 12?",
                options=["12", "11", "13", "10"],
                correct_answer=0,
                explanation="144 ÷ 12 = 12. You can check: 12 × 12 = 144.",
                difficulty="medium",
                topic="Division",
                question_type="mcq"
            ),
            Question(
                id="math_6_2",
                question="Convert 0.75 to a fraction:",
                options=["3/4", "7/10", "75/100", "3/5"],
                correct_answer=0,
                explanation="0.75 = 75/100 = 3/4 when simplified by dividing both by 25.",
                difficulty="medium",
                topic="Decimals and Fractions",
                question_type="mcq"
            ),
            Question(
                id="math_6_3",
                question="What is the area of a rectangle with length 8 cm and width 5 cm?",
                options=["40 sq cm", "13 sq cm", "26 sq cm", "35 sq cm"],
                correct_answer=0,
                explanation="Area = length × width = 8 × 5 = 40 square centimeters.",
                difficulty="medium",
                topic="Area and Perimeter",
                question_type="mcq"
            )
        ]
    
    def _get_math_questions_7th(self) -> List[Question]:
        """Math questions for 7th grade"""
        return [
            Question(
                id="math_7_1",
                question="Solve: 2x + 5 = 13",
                options=["x = 4", "x = 3", "x = 5", "x = 6"],
                correct_answer=0,
                explanation="2x + 5 = 13 → 2x = 13 - 5 → 2x = 8 → x = 4",
                difficulty="hard",
                topic="Algebra",
                question_type="mcq"
            ),
            Question(
                id="math_7_2",
                question="What is 25% of 80?",
                options=["20", "15", "25", "30"],
                correct_answer=0,
                explanation="25% = 1/4, so 1/4 of 80 = 80 ÷ 4 = 20",
                difficulty="medium",
                topic="Percentages",
                question_type="mcq"
            )
        ]
    
    def _get_math_questions_8th(self) -> List[Question]:
        """Math questions for 8th grade"""
        return [
            Question(
                id="math_8_1",
                question="What is the square root of 144?",
                options=["12", "11", "13", "14"],
                correct_answer=0,
                explanation="√144 = 12 because 12 × 12 = 144",
                difficulty="medium",
                topic="Square Roots",
                question_type="mcq"
            ),
            Question(
                id="math_8_2",
                question="In a right triangle, if one angle is 90° and another is 30°, what's the third angle?",
                options=["60°", "70°", "50°", "45°"],
                correct_answer=0,
                explanation="Angles in a triangle sum to 180°. So 180° - 90° - 30° = 60°",
                difficulty="hard",
                topic="Triangles",
                question_type="mcq"
            )
        ]
    
    def _get_science_questions_5th(self) -> List[Question]:
        """Science questions for 5th grade"""
        return [
            Question(
                id="science_5_1",
                question="What do plants need to make food?",
                options=["Sunlight only", "Water only", "Sunlight, water, and air", "Soil only"],
                correct_answer=2,
                explanation="Plants need sunlight, water, and carbon dioxide from air to make food through photosynthesis.",
                difficulty="easy",
                topic="Plant Life",
                question_type="mcq"
            ),
            Question(
                id="science_5_2",
                question="Which planet is closest to the Sun?",
                options=["Venus", "Mercury", "Earth", "Mars"],
                correct_answer=1,
                explanation="Mercury is the closest planet to the Sun in our solar system.",
                difficulty="medium",
                topic="Solar System",
                question_type="mcq"
            ),
            Question(
                id="science_5_3",
                question="What gas do we breathe in that our body needs?",
                options=["Carbon dioxide", "Oxygen", "Nitrogen", "Helium"],
                correct_answer=1,
                explanation="We breathe in oxygen, which our body needs for cellular respiration.",
                difficulty="easy",
                topic="Human Body",
                question_type="mcq"
            )
        ]
    
    def _get_science_questions_6th(self) -> List[Question]:
        """Science questions for 6th grade"""
        return [
            Question(
                id="science_6_1",
                question="What is the process by which water changes from liquid to gas?",
                options=["Condensation", "Evaporation", "Precipitation", "Freezing"],
                correct_answer=1,
                explanation="Evaporation is when water changes from liquid to gas due to heat.",
                difficulty="medium",
                topic="Water Cycle",
                question_type="mcq"
            ),
            Question(
                id="science_6_2",
                question="Which type of simple machine is a see-saw?",
                options=["Pulley", "Lever", "Inclined plane", "Wheel and axle"],
                correct_answer=1,
                explanation="A see-saw is a type of lever with a fulcrum in the middle.",
                difficulty="medium",
                topic="Simple Machines",
                question_type="mcq"
            )
        ]
    
    def _get_science_questions_7th(self) -> List[Question]:
        """Science questions for 7th grade"""
        return [
            Question(
                id="science_7_1",
                question="What is the basic unit of life?",
                options=["Tissue", "Cell", "Organ", "Organism"],
                correct_answer=1,
                explanation="The cell is the basic unit of life. All living things are made of cells.",
                difficulty="medium",
                topic="Cell Biology",
                question_type="mcq"
            ),
            Question(
                id="science_7_2",
                question="What happens to the speed of sound in warmer air?",
                options=["It decreases", "It increases", "It stays the same", "It stops"],
                correct_answer=1,
                explanation="Sound travels faster in warmer air because molecules move more quickly.",
                difficulty="hard",
                topic="Sound",
                question_type="mcq"
            )
        ]
    
    def _get_science_questions_8th(self) -> List[Question]:
        """Science questions for 8th grade"""
        return [
            Question(
                id="science_8_1",
                question="What is the chemical symbol for water?",
                options=["H2O", "CO2", "NaCl", "O2"],
                correct_answer=0,
                explanation="H2O represents water - 2 hydrogen atoms and 1 oxygen atom.",
                difficulty="easy",
                topic="Chemistry",
                question_type="mcq"
            ),
            Question(
                id="science_8_2",
                question="What force keeps planets in orbit around the Sun?",
                options=["Magnetic force", "Gravity", "Electric force", "Nuclear force"],
                correct_answer=1,
                explanation="Gravity is the force that keeps planets in orbit around the Sun.",
                difficulty="medium",
                topic="Forces and Motion",
                question_type="mcq"
            )
        ]
    
    # Simplified implementations for other subjects (Social Studies, English)
    def _get_social_questions_5th(self) -> List[Question]:
        return [
            Question(
                id="social_5_1",
                question="Who was the first President of India?",
                options=["Mahatma Gandhi", "Dr. Rajendra Prasad", "Jawaharlal Nehru", "Dr. APJ Abdul Kalam"],
                correct_answer=1,
                explanation="Dr. Rajendra Prasad was the first President of India from 1950 to 1962.",
                difficulty="medium",
                topic="Indian History",
                question_type="mcq"
            )
        ]
    
    def _get_social_questions_6th(self) -> List[Question]:
        return [
            Question(
                id="social_6_1",
                question="Which river is known as the 'Ganga of the South'?",
                options=["Krishna", "Godavari", "Cauvery", "Narmada"],
                correct_answer=1,
                explanation="The Godavari river is often called the 'Ganga of the South' due to its importance.",
                difficulty="medium",
                topic="Geography",
                question_type="mcq"
            )
        ]
    
    def _get_social_questions_7th(self) -> List[Question]:
        return [
            Question(
                id="social_7_1",
                question="In which year did India gain independence?",
                options=["1946", "1947", "1948", "1949"],
                correct_answer=1,
                explanation="India gained independence from British rule on August 15, 1947.",
                difficulty="easy",
                topic="Freedom Struggle",
                question_type="mcq"
            )
        ]
    
    def _get_social_questions_8th(self) -> List[Question]:
        return [
            Question(
                id="social_8_1",
                question="What is the capital of Karnataka?",
                options=["Mumbai", "Chennai", "Bangalore", "Hyderabad"],
                correct_answer=2,
                explanation="Bangalore (now Bengaluru) is the capital city of Karnataka state.",
                difficulty="easy",
                topic="Indian States",
                question_type="mcq"
            )
        ]
    
    def _get_english_questions_5th(self) -> List[Question]:
        return [
            Question(
                id="english_5_1",
                question="What is the plural of 'child'?",
                options=["childs", "children", "childes", "child"],
                correct_answer=1,
                explanation="The plural of 'child' is 'children'. It's an irregular plural form.",
                difficulty="easy",
                topic="Grammar",
                question_type="mcq"
            )
        ]
    
    def _get_english_questions_6th(self) -> List[Question]:
        return [
            Question(
                id="english_6_1",
                question="Which is a verb in this sentence: 'The dog runs fast'?",
                options=["dog", "runs", "fast", "the"],
                correct_answer=1,
                explanation="'Runs' is the verb as it shows the action the dog is performing.",
                difficulty="medium",
                topic="Parts of Speech",
                question_type="mcq"
            )
        ]
    
    def _get_english_questions_7th(self) -> List[Question]:
        return [
            Question(
                id="english_7_1",
                question="What type of word is 'quickly'?",
                options=["noun", "verb", "adjective", "adverb"],
                correct_answer=3,
                explanation="'Quickly' is an adverb because it describes how an action is performed.",
                difficulty="medium",
                topic="Adverbs",
                question_type="mcq"
            )
        ]
    
    def _get_english_questions_8th(self) -> List[Question]:
        return [
            Question(
                id="english_8_1",
                question="Which word rhymes with 'cat'?",
                options=["dog", "bat", "bird", "fish"],
                correct_answer=1,
                explanation="'Bat' rhymes with 'cat' because they both end with the '-at' sound.",
                difficulty="easy",
                topic="Phonics",
                question_type="mcq"
            )
        ]
    
    def _load_student_progress(self) -> Dict:
        """Load student progress from cache"""
        progress_file = self.cache_dir / "quiz_progress.json"
        try:
            if progress_file.exists():
                with open(progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load student progress: {e}")
        
        return {}
    
    def _save_student_progress(self):
        """Save student progress to cache"""
        try:
            progress_file = self.cache_dir / "quiz_progress.json"
            with open(progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.student_progress, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save student progress: {e}")
    
    def generate_quiz(self, grade: str, board: str, subject: str, 
                     difficulty: str = "auto", num_questions: int = None,
                     topics: List[str] = None) -> QuizSession:
        """
        Generate an adaptive quiz
        
        Args:
            grade: Student's grade
            board: Education board
            subject: Subject for the quiz
            difficulty: Difficulty level or "auto" for adaptive
            num_questions: Number of questions (default: 10)
            topics: Specific topics to focus on
            
        Returns:
            QuizSession object
        """
        try:
            if num_questions is None:
                num_questions = self.default_quiz_length
            
            # Get student's current level
            if difficulty == "auto":
                difficulty = self._get_adaptive_difficulty(subject, grade)
            
            # Get available questions
            questions_pool = self._get_questions_pool(grade, subject, difficulty, topics)
            
            if not questions_pool:
                logger.warning(f"No questions available for {subject} {grade}")
                questions_pool = self._get_fallback_questions(subject, grade)
            
            # Select questions
            selected_questions = self._select_questions(questions_pool, num_questions, difficulty)
            
            # Create quiz session
            session_id = f"quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"
            
            quiz_session = QuizSession(
                session_id=session_id,
                grade=grade,
                board=board,
                subject=subject,
                questions=selected_questions,
                user_answers=[],
                score=0,
                total_questions=len(selected_questions),
                time_taken=0.0,
                timestamp=datetime.now(),
                difficulty_level=difficulty,
                topics_covered=list(set(q.topic for q in selected_questions))
            )
            
            logger.info(f"Generated quiz with {len(selected_questions)} questions for {subject} {grade}")
            return quiz_session
            
        except Exception as e:
            logger.error(f"Failed to generate quiz: {e}")
            return self._create_fallback_quiz(grade, board, subject)
    
    def _get_adaptive_difficulty(self, subject: str, grade: str) -> str:
        """Determine difficulty level based on student progress"""
        progress_key = f"{subject}_{grade}"
        
        if progress_key not in self.student_progress:
            return "easy"  # Start with easy for new students
        
        progress = self.student_progress[progress_key]
        recent_score = progress.get("recent_average", 50)
        
        if recent_score >= 80:
            return "medium" if progress.get("current_difficulty", "easy") == "easy" else "hard"
        elif recent_score >= 60:
            return "medium"
        else:
            return "easy"
    
    def _get_questions_pool(self, grade: str, subject: str, difficulty: str, topics: List[str]) -> List[Question]:
        """Get pool of questions matching criteria"""
        if subject not in self.question_banks or grade not in self.question_banks[subject]:
            return []
        
        questions = self.question_banks[subject][grade]
        
        # Filter by difficulty
        if difficulty != "auto":
            questions = [q for q in questions if q.difficulty == difficulty]
        
        # Filter by topics if specified
        if topics:
            questions = [q for q in questions if q.topic in topics]
        
        return questions
    
    def _select_questions(self, questions_pool: List[Question], num_questions: int, difficulty: str) -> List[Question]:
        """Select questions from pool with balanced difficulty and topics"""
        if len(questions_pool) <= num_questions:
            return questions_pool
        
        # Group by topics
        topic_groups = {}
        for q in questions_pool:
            if q.topic not in topic_groups:
                topic_groups[q.topic] = []
            topic_groups[q.topic].append(q)
        
        # Select questions to ensure topic diversity
        selected = []
        questions_per_topic = max(1, num_questions // len(topic_groups))
        
        for topic, topic_questions in topic_groups.items():
            topic_selection = random.sample(topic_questions, min(questions_per_topic, len(topic_questions)))
            selected.extend(topic_selection)
        
        # Fill remaining slots randomly
        remaining = num_questions - len(selected)
        if remaining > 0:
            remaining_pool = [q for q in questions_pool if q not in selected]
            if remaining_pool:
                selected.extend(random.sample(remaining_pool, min(remaining, len(remaining_pool))))
        
        return selected[:num_questions]
    
    def _get_fallback_questions(self, subject: str, grade: str) -> List[Question]:
        """Get fallback questions when specific criteria not met"""
        # Try to get questions from any grade in the subject
        if subject in self.question_banks:
            all_questions = []
            for g, questions in self.question_banks[subject].items():
                all_questions.extend(questions)
            return all_questions
        
        return []
    
    def _create_fallback_quiz(self, grade: str, board: str, subject: str) -> QuizSession:
        """Create a basic fallback quiz"""
        fallback_question = Question(
            id="fallback_1",
            question=f"This is a sample question for {subject}. What is your favorite topic in {subject}?",
            options=["Option A", "Option B", "Option C", "Option D"],
            correct_answer=0,
            explanation="This is a sample explanation.",
            difficulty="easy",
            topic="General",
            question_type="mcq"
        )
        
        return QuizSession(
            session_id=f"fallback_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            grade=grade,
            board=board,
            subject=subject,
            questions=[fallback_question],
            user_answers=[],
            score=0,
            total_questions=1,
            time_taken=0.0,
            timestamp=datetime.now(),
            difficulty_level="easy",
            topics_covered=["General"]
        )
    
    def score_quiz(self, quiz_session: QuizSession, user_answers: List[int], time_taken: float) -> Dict:
        """
        Score a completed quiz and update student progress
        
        Args:
            quiz_session: The quiz session
            user_answers: List of user's answers (indices)
            time_taken: Time taken to complete quiz in seconds
            
        Returns:
            Dictionary with scoring results
        """
        try:
            quiz_session.user_answers = user_answers
            quiz_session.time_taken = time_taken
            
            # Calculate score
            correct_answers = 0
            question_results = []
            
            for i, question in enumerate(quiz_session.questions):
                user_answer = user_answers[i] if i < len(user_answers) else -1
                is_correct = user_answer == question.correct_answer
                
                if is_correct:
                    correct_answers += 1
                
                question_results.append({
                    "question": question.question,
                    "user_answer": question.options[user_answer] if 0 <= user_answer < len(question.options) else "No answer",
                    "correct_answer": question.options[question.correct_answer],
                    "is_correct": is_correct,
                    "explanation": question.explanation,
                    "topic": question.topic
                })
            
            quiz_session.score = correct_answers
            percentage = (correct_answers / quiz_session.total_questions) * 100
            
            # Update student progress
            self._update_student_progress(quiz_session, percentage)
            
            # Generate performance feedback
            feedback = self._generate_feedback(percentage, quiz_session.difficulty_level, question_results)
            
            # Determine coins earned (this should match the gamification system)
            coins_earned = self._calculate_coins(percentage, quiz_session.difficulty_level)
            
            result = {
                "score": correct_answers,
                "total": quiz_session.total_questions,
                "percentage": round(percentage, 1),
                "time_taken": round(time_taken, 1),
                "difficulty": quiz_session.difficulty_level,
                "coins_earned": coins_earned,
                "feedback": feedback,
                "question_results": question_results,
                "topics_performance": self._analyze_topic_performance(question_results),
                "next_difficulty": self._recommend_next_difficulty(percentage, quiz_session.difficulty_level)
            }
            
            logger.info(f"Quiz scored: {correct_answers}/{quiz_session.total_questions} ({percentage:.1f}%)")
            return result
            
        except Exception as e:
            logger.error(f"Failed to score quiz: {e}")
            return {
                "score": 0,
                "total": quiz_session.total_questions,
                "percentage": 0,
                "feedback": "Error occurred while scoring quiz.",
                "coins_earned": 10  # Consolation coins
            }
    
    def _update_student_progress(self, quiz_session: QuizSession, percentage: float):
        """Update student progress tracking"""
        progress_key = f"{quiz_session.subject}_{quiz_session.grade}"
        
        if progress_key not in self.student_progress:
            self.student_progress[progress_key] = {
                "total_quizzes": 0,
                "scores": [],
                "recent_scores": [],
                "topic_performance": {},
                "current_difficulty": "easy",
                "last_quiz_date": None
            }
        
        progress = self.student_progress[progress_key]
        progress["total_quizzes"] += 1
        progress["scores"].append(percentage)
        progress["recent_scores"] = progress["scores"][-10:]  # Keep last 10 scores
        progress["last_quiz_date"] = datetime.now().isoformat()
        progress["current_difficulty"] = quiz_session.difficulty_level
        
        # Update topic performance
        for question, user_answer_info in zip(quiz_session.questions, 
                                             [{"is_correct": ua == q.correct_answer} 
                                              for ua, q in zip(quiz_session.user_answers, quiz_session.questions)]):
            topic = question.topic
            if topic not in progress["topic_performance"]:
                progress["topic_performance"][topic] = {"correct": 0, "total": 0}
            
            progress["topic_performance"][topic]["total"] += 1
            if user_answer_info["is_correct"]:
                progress["topic_performance"][topic]["correct"] += 1
        
        self._save_student_progress()
    
    def _calculate_coins(self, percentage: float, difficulty: str) -> int:
        """Calculate coins earned based on performance"""
        base_coins = {
            "easy": 10,
            "medium": 20,
            "hard": 30
        }
        
        base = base_coins.get(difficulty, 10)
        
        if percentage >= 90:
            return base * 3
        elif percentage >= 80:
            return base * 2
        elif percentage >= 60:
            return int(base * 1.5)
        elif percentage >= 40:
            return base
        else:
            return max(5, base // 2)  # Consolation coins
    
    def _generate_feedback(self, percentage: float, difficulty: str, question_results: List[Dict]) -> str:
        """Generate encouraging feedback based on performance"""
        if percentage >= 90:
            feedback = "🌟 Outstanding performance! You're a true scholar! 🌟"
        elif percentage >= 80:
            feedback = "🎉 Excellent work! You really understand this material! 🎉"
        elif percentage >= 70:
            feedback = "👏 Great job! You're making good progress! 👏"
        elif percentage >= 60:
            feedback = "👍 Good effort! Keep practicing and you'll improve! 👍"
        elif percentage >= 40:
            feedback = "💪 You're on the right track! Review the topics and try again! 💪"
        else:
            feedback = "🌱 Every expert was once a beginner! Don't give up! 🌱"
        
        # Add difficulty-specific encouragement
        if difficulty == "hard" and percentage >= 60:
            feedback += " Tackling hard questions shows great courage! 🦸‍♀️"
        elif difficulty == "easy" and percentage >= 80:
            feedback += " Ready to try medium difficulty next time? 🚀"
        
        return feedback
    
    def _analyze_topic_performance(self, question_results: List[Dict]) -> Dict:
        """Analyze performance by topic"""
        topic_stats = {}
        for result in question_results:
            topic = result["topic"]
            if topic not in topic_stats:
                topic_stats[topic] = {"correct": 0, "total": 0}
            
            topic_stats[topic]["total"] += 1
            if result["is_correct"]:
                topic_stats[topic]["correct"] += 1
        
        # Convert to percentages
        topic_performance = {}
        for topic, stats in topic_stats.items():
            percentage = (stats["correct"] / stats["total"]) * 100
            topic_performance[topic] = {
                "percentage": round(percentage, 1),
                "correct": stats["correct"],
                "total": stats["total"]
            }
        
        return topic_performance
    
    def _recommend_next_difficulty(self, percentage: float, current_difficulty: str) -> str:
        """Recommend difficulty for next quiz"""
        thresholds = self.score_thresholds.get(current_difficulty, {"promote": 80, "demote": 50})
        
        if percentage >= thresholds["promote"]:
            if current_difficulty == "easy":
                return "medium"
            elif current_difficulty == "medium":
                return "hard"
            else:
                return "hard"  # Stay at hard
        elif percentage < thresholds["demote"]:
            if current_difficulty == "hard":
                return "medium"
            elif current_difficulty == "medium":
                return "easy"
            else:
                return "easy"  # Stay at easy
        else:
            return current_difficulty  # Stay at current level
    
    def generate_revision_summary(self, grade: str, board: str, subject: str, 
                                 topics: List[str] = None) -> Dict:
        """
        Generate revision summary based on student progress
        
        Args:
            grade: Student's grade
            board: Education board
            subject: Subject to revise
            topics: Specific topics to focus on
            
        Returns:
            Dictionary with revision content
        """
        try:
            progress_key = f"{subject}_{grade}"
            
            # Get weak topics from progress
            weak_topics = []
            if progress_key in self.student_progress:
                topic_performance = self.student_progress[progress_key].get("topic_performance", {})
                for topic, stats in topic_performance.items():
                    if stats["total"] > 0:
                        percentage = (stats["correct"] / stats["total"]) * 100
                        if percentage < 70:  # Consider <70% as weak
                            weak_topics.append(topic)
            
            # Focus on specified topics or weak topics
            focus_topics = topics if topics else weak_topics[:5]  # Top 5 weak topics
            
            if not focus_topics:
                focus_topics = ["General Review"]
            
            # Generate revision content
            revision_content = {
                "subject": subject,
                "grade": grade,
                "focus_topics": focus_topics,
                "summary": self._generate_topic_summaries(subject, grade, focus_topics),
                "key_points": self._generate_key_points(subject, grade, focus_topics),
                "practice_tips": self._generate_practice_tips(subject, focus_topics),
                "recommended_study_time": self._calculate_study_time(len(focus_topics)),
                "next_quiz_recommendation": {
                    "difficulty": self._get_adaptive_difficulty(subject, grade),
                    "topics": focus_topics[:3]  # Focus on top 3 weak topics
                }
            }
            
            logger.info(f"Generated revision summary for {subject} {grade} covering {len(focus_topics)} topics")
            return revision_content
            
        except Exception as e:
            logger.error(f"Failed to generate revision summary: {e}")
            return self._generate_fallback_revision(subject, grade)
    
    def _generate_topic_summaries(self, subject: str, grade: str, topics: List[str]) -> Dict[str, str]:
        """Generate brief summaries for each topic"""
        summaries = {}
        
        # This would typically use LLM or pre-written content
        # For now, providing basic summaries
        for topic in topics:
            if subject == "Math":
                summaries[topic] = f"Review {topic}: Practice problems step by step, understand formulas, and solve examples."
            elif subject == "Science":
                summaries[topic] = f"Study {topic}: Read concepts, understand processes, and relate to real-world examples."
            elif subject == "Social Studies":
                summaries[topic] = f"Learn about {topic}: Remember key facts, dates, and understand cause-and-effect relationships."
            elif subject == "English":
                summaries[topic] = f"Practice {topic}: Read examples, understand rules, and apply in writing and speaking."
            else:
                summaries[topic] = f"Review the key concepts and practice problems related to {topic}."
        
        return summaries
    
    def _generate_key_points(self, subject: str, grade: str, topics: List[str]) -> List[str]:
        """Generate key points to remember"""
        key_points = []
        
        for topic in topics:
            if subject == "Math":
                key_points.extend([
                    f"Practice {topic} problems daily",
                    f"Understand the logic behind {topic} formulas",
                    f"Use visual aids for {topic} concepts"
                ])
            elif subject == "Science":
                key_points.extend([
                    f"Observe {topic} in everyday life",
                    f"Conduct simple experiments related to {topic}",
                    f"Draw diagrams to understand {topic}"
                ])
            # Add more subjects as needed
        
        return key_points[:10]  # Limit to 10 key points
    
    def _generate_practice_tips(self, subject: str, topics: List[str]) -> List[str]:
        """Generate practice tips"""
        tips = [
            "Study in short, focused sessions (20-30 minutes)",
            "Take breaks between study sessions",
            "Review previous day's learning before starting new topics",
            "Practice explaining concepts out loud",
            "Use flashcards for quick revision"
        ]
        
        # Add subject-specific tips
        if subject == "Math":
            tips.extend([
                "Solve problems without looking at solutions first",
                "Check your answers by working backwards",
                "Practice mental math daily"
            ])
        elif subject == "Science":
            tips.extend([
                "Connect new concepts to what you already know",
                "Watch educational videos for visual learning",
                "Ask 'why' and 'how' questions"
            ])
        
        return tips
    
    def _calculate_study_time(self, num_topics: int) -> str:
        """Calculate recommended study time"""
        minutes_per_topic = 15
        total_minutes = num_topics * minutes_per_topic
        
        if total_minutes < 60:
            return f"{total_minutes} minutes"
        else:
            hours = total_minutes // 60
            remaining_minutes = total_minutes % 60
            if remaining_minutes > 0:
                return f"{hours} hour(s) {remaining_minutes} minutes"
            else:
                return f"{hours} hour(s)"
    
    def _generate_fallback_revision(self, subject: str, grade: str) -> Dict:
        """Generate fallback revision when specific data not available"""
        return {
            "subject": subject,
            "grade": grade,
            "focus_topics": ["General Review"],
            "summary": {"General Review": f"Review all {subject} topics covered so far in {grade} grade."},
            "key_points": [
                "Review your notes regularly",
                "Practice problems daily",
                "Ask questions when you don't understand",
                "Connect new learning to previous knowledge"
            ],
            "practice_tips": [
                "Study in a quiet environment",
                "Take regular breaks",
                "Practice explaining concepts to others",
                "Use multiple learning methods"
            ],
            "recommended_study_time": "30 minutes",
            "next_quiz_recommendation": {
                "difficulty": "easy",
                "topics": ["General Review"]
            }
        }
    
    def get_student_report(self, subject: str, grade: str) -> Dict:
        """Generate comprehensive student progress report"""
        progress_key = f"{subject}_{grade}"
        
        if progress_key not in self.student_progress:
            return {
                "subject": subject,
                "grade": grade,
                "message": "No quiz data available yet. Take your first quiz to see progress!"
            }
        
        progress = self.student_progress[progress_key]
        
        # Calculate statistics
        scores = progress.get("scores", [])
        recent_scores = progress.get("recent_scores", [])
        
        avg_score = sum(scores) / len(scores) if scores else 0
        recent_avg = sum(recent_scores) / len(recent_scores) if recent_scores else 0
        
        # Analyze improvement trend
        if len(scores) >= 2:
            trend = "improving" if recent_avg > avg_score else "stable" if recent_avg == avg_score else "needs_attention"
        else:
            trend = "insufficient_data"
        
        # Topic analysis
        topic_performance = progress.get("topic_performance", {})
        strong_topics = []
        weak_topics = []
        
        for topic, stats in topic_performance.items():
            if stats["total"] > 0:
                percentage = (stats["correct"] / stats["total"]) * 100
                if percentage >= 80:
                    strong_topics.append(topic)
                elif percentage < 60:
                    weak_topics.append(topic)
        
        return {
            "subject": subject,
            "grade": grade,
            "total_quizzes": progress.get("total_quizzes", 0),
            "average_score": round(avg_score, 1),
            "recent_average": round(recent_avg, 1),
            "improvement_trend": trend,
            "strong_topics": strong_topics,
            "weak_topics": weak_topics,
            "current_difficulty": progress.get("current_difficulty", "easy"),
            "last_quiz_date": progress.get("last_quiz_date"),
            "recommendations": self._generate_recommendations(trend, weak_topics, avg_score)
        }
    
    def _generate_recommendations(self, trend: str, weak_topics: List[str], avg_score: float) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        if trend == "improving":
            recommendations.append("🎉 Great progress! Keep up the excellent work!")
        elif trend == "needs_attention":
            recommendations.append("📈 Focus on consistent practice to improve your scores.")
        
        if weak_topics:
            recommendations.append(f"💪 Spend extra time on: {', '.join(weak_topics[:3])}")
        
        if avg_score >= 80:
            recommendations.append("🚀 Ready for more challenging questions!")
        elif avg_score < 60:
            recommendations.append("📚 Review basic concepts and practice regularly.")
        
        recommendations.append("🎯 Take quizzes regularly to track your progress.")
        
        return recommendations

# Test function
def test_quiz_generator():
    """Test the quiz generator"""
    generator = QuizGenerator()
    
    # Test quiz generation
    quiz = generator.generate_quiz("6th", "Karnataka State Board", "Math", "medium", 5)
    print(f"Generated quiz: {quiz.session_id}")
    print(f"Questions: {len(quiz.questions)}")
    for i, q in enumerate(quiz.questions):
        print(f"{i+1}. {q.question}")
        for j, option in enumerate(q.options):
            print(f"   {chr(65+j)}. {option}")
        print()
    
    # Test scoring
    sample_answers = [0, 1, 0, 1, 1]  # Sample answers
    result = generator.score_quiz(quiz, sample_answers, 120.0)
    print(f"Score: {result['score']}/{result['total']} ({result['percentage']}%)")
    print(f"Feedback: {result['feedback']}")
    
    # Test revision generation
    revision = generator.generate_revision_summary("6th", "Karnataka State Board", "Math")
    print(f"Revision topics: {revision['focus_topics']}")

if __name__ == "__main__":
    test_quiz_generator()