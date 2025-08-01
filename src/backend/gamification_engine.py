"""
Gamification Engine Module
Manages coins, perks, achievements, and leaderboards for student engagement
"""

import json
import time
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import random

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AchievementType(Enum):
    QUIZ_MASTER = "quiz_master"
    STREAK_KEEPER = "streak_keeper"
    SUBJECT_EXPERT = "subject_expert"
    ATTENTION_CHAMPION = "attention_champion"
    EARLY_BIRD = "early_bird"
    CONSISTENCY_KING = "consistency_king"

@dataclass
class Achievement:
    """Data class for achievements"""
    id: str
    name: str
    description: str
    icon: str
    requirement: Dict
    reward_coins: int
    rarity: str  # common, rare, epic, legendary
    unlocked: bool = False
    unlock_date: Optional[datetime] = None

@dataclass
class Perk:
    """Data class for purchasable perks"""
    id: str
    name: str
    description: str
    cost: int
    icon: str
    effect: Dict
    category: str  # cosmetic, functional, boost
    owned: bool = False
    purchase_date: Optional[datetime] = None

@dataclass
class StudentProfile:
    """Data class for student gamification profile"""
    student_id: str
    total_coins: int
    current_coins: int
    level: int
    experience_points: int
    streak_days: int
    longest_streak: int
    total_quizzes: int
    total_videos: int
    study_minutes: int
    achievements: List[str]
    owned_perks: List[str]
    last_activity: datetime
    join_date: datetime

@dataclass
class LeaderboardEntry:
    """Data class for leaderboard entries"""
    rank: int
    student_id: str
    display_name: str
    score: int
    metric: str  # coins, level, streak, etc.

class GamificationEngine:
    """Manages all gamification aspects of the learning app"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.cache_dir = self.data_dir / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Load gamification data
        self.student_profiles = self._load_student_profiles()
        self.achievements = self._initialize_achievements()
        self.perks = self._initialize_perks()
        self.daily_challenges = self._load_daily_challenges()
        
        # Current session data
        self.current_student = self._get_or_create_student("default_student")
        
        # Level system
        self.level_requirements = self._calculate_level_requirements()
        
        # Coin multipliers
        self.coin_multipliers = {
            "quiz_completion": 1.0,
            "perfect_score": 2.0,
            "streak_bonus": 1.5,
            "daily_challenge": 1.25,
            "attention_bonus": 1.1
        }
    
    def _load_student_profiles(self) -> Dict[str, StudentProfile]:
        """Load student profiles from cache"""
        profiles_file = self.cache_dir / "gamification.json"
        
        try:
            if profiles_file.exists():
                with open(profiles_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Convert to StudentProfile objects
                profiles = {}
                for student_id, profile_data in data.items():
                    # Convert datetime strings back to datetime objects
                    if 'last_activity' in profile_data:
                        profile_data['last_activity'] = datetime.fromisoformat(profile_data['last_activity'])
                    if 'join_date' in profile_data:
                        profile_data['join_date'] = datetime.fromisoformat(profile_data['join_date'])
                    
                    profiles[student_id] = StudentProfile(**profile_data)
                
                return profiles
        except Exception as e:
            logger.error(f"Failed to load student profiles: {e}")
        
        return {}
    
    def _save_student_profiles(self):
        """Save student profiles to cache"""
        try:
            profiles_file = self.cache_dir / "gamification.json"
            
            # Convert StudentProfile objects to dictionaries
            data = {}
            for student_id, profile in self.student_profiles.items():
                profile_dict = asdict(profile)
                # Convert datetime objects to strings
                if profile_dict['last_activity']:
                    profile_dict['last_activity'] = profile_dict['last_activity'].isoformat()
                if profile_dict['join_date']:
                    profile_dict['join_date'] = profile_dict['join_date'].isoformat()
                data[student_id] = profile_dict
            
            with open(profiles_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Failed to save student profiles: {e}")
    
    def _get_or_create_student(self, student_id: str) -> StudentProfile:
        """Get existing student profile or create new one"""
        if student_id not in self.student_profiles:
            self.student_profiles[student_id] = StudentProfile(
                student_id=student_id,
                total_coins=100,  # Starting coins
                current_coins=100,
                level=1,
                experience_points=0,
                streak_days=0,
                longest_streak=0,
                total_quizzes=0,
                total_videos=0,
                study_minutes=0,
                achievements=[],
                owned_perks=[],
                last_activity=datetime.now(),
                join_date=datetime.now()
            )
            self._save_student_profiles()
        
        return self.student_profiles[student_id]
    
    def _initialize_achievements(self) -> Dict[str, Achievement]:
        """Initialize achievement definitions"""
        achievements = {
            "first_quiz": Achievement(
                id="first_quiz",
                name="Quiz Rookie 🎯",
                description="Complete your first quiz",
                icon="🎯",
                requirement={"quizzes_completed": 1},
                reward_coins=25,
                rarity="common"
            ),
            "quiz_master": Achievement(
                id="quiz_master",
                name="Quiz Master 🏆",
                description="Complete 50 quizzes",
                icon="🏆",
                requirement={"quizzes_completed": 50},
                reward_coins=200,
                rarity="epic"
            ),
            "perfect_score": Achievement(
                id="perfect_score",
                name="Perfect Scholar ⭐",
                description="Score 100% on a quiz",
                icon="⭐",
                requirement={"perfect_quiz": 1},
                reward_coins=50,
                rarity="rare"
            ),
            "streak_week": Achievement(
                id="streak_week",
                name="Week Warrior 🔥",
                description="Study for 7 days in a row",
                icon="🔥",
                requirement={"streak_days": 7},
                reward_coins=75,
                rarity="rare"
            ),
            "streak_month": Achievement(
                id="streak_month",
                name="Monthly Champion 👑",
                description="Study for 30 days in a row",
                icon="👑",
                requirement={"streak_days": 30},
                reward_coins=300,
                rarity="legendary"
            ),
            "math_expert": Achievement(
                id="math_expert",
                name="Math Wizard 🧮",
                description="Score above 80% in 10 Math quizzes",
                icon="🧮",
                requirement={"subject_mastery": {"Math": 10}},
                reward_coins=150,
                rarity="epic"
            ),
            "science_expert": Achievement(
                id="science_expert",
                name="Science Explorer 🔬",
                description="Score above 80% in 10 Science quizzes",
                icon="🔬",
                requirement={"subject_mastery": {"Science": 10}},
                reward_coins=150,
                rarity="epic"
            ),
            "attention_champion": Achievement(
                id="attention_champion",
                name="Focus Master 👁️",
                description="Maintain >90% attention for 30 minutes",
                icon="👁️",
                requirement={"attention_mastery": 30},
                reward_coins=100,
                rarity="rare"
            ),
            "early_bird": Achievement(
                id="early_bird",
                name="Early Bird 🌅",
                description="Study before 8 AM for 5 days",
                icon="🌅",
                requirement={"early_study_days": 5},
                reward_coins=75,
                rarity="rare"
            ),
            "coin_collector": Achievement(
                id="coin_collector",
                name="Coin Collector 💰",
                description="Earn 1000 total coins",
                icon="💰",
                requirement={"total_coins": 1000},
                reward_coins=100,
                rarity="rare"
            ),
            "video_enthusiast": Achievement(
                id="video_enthusiast",
                name="Video Enthusiast 📺",
                description="Watch 25 educational videos",
                icon="📺",
                requirement={"videos_watched": 25},
                reward_coins=75,
                rarity="common"
            )
        }
        
        return achievements
    
    def _initialize_perks(self) -> Dict[str, Perk]:
        """Initialize purchasable perks"""
        perks = {
            "golden_star": Perk(
                id="golden_star",
                name="Golden Star Badge ⭐",
                description="Show everyone you're a star student!",
                cost=50,
                icon="⭐",
                effect={"type": "cosmetic", "display_badge": "golden_star"},
                category="cosmetic"
            ),
            "superhero_avatar": Perk(
                id="superhero_avatar",
                name="Super Learner Avatar 🦸",
                description="Unlock a cool superhero avatar!",
                cost=100,
                icon="🦸",
                effect={"type": "cosmetic", "avatar": "superhero"},
                category="cosmetic"
            ),
            "speed_boost": Perk(
                id="speed_boost",
                name="Speed Boost ⚡",
                description="Get extra time for quizzes!",
                cost=75,
                icon="⚡",
                effect={"type": "functional", "quiz_time_bonus": 30},  # 30 extra seconds
                category="functional"
            ),
            "hint_helper": Perk(
                id="hint_helper",
                name="Hint Helper 💡",
                description="Get one free hint per quiz!",
                cost=30,
                icon="💡",
                effect={"type": "functional", "quiz_hints": 1},
                category="functional"
            ),
            "rainbow_theme": Perk(
                id="rainbow_theme",
                name="Rainbow Theme 🌈",
                description="Make your app colorful!",
                cost=80,
                icon="🌈",
                effect={"type": "cosmetic", "theme": "rainbow"},
                category="cosmetic"
            ),
            "music_mode": Perk(
                id="music_mode",
                name="Study Music 🎵",
                description="Study with background music!",
                cost=60,
                icon="🎵",
                effect={"type": "functional", "background_music": True},
                category="functional"
            ),
            "double_coins": Perk(
                id="double_coins",
                name="Double Coins 💎",
                description="Earn 2x coins for 24 hours!",
                cost=200,
                icon="💎",
                effect={"type": "boost", "coin_multiplier": 2.0, "duration": 24},  # 24 hours
                category="boost"
            ),
            "skip_question": Perk(
                id="skip_question",
                name="Question Skip 🔄",
                description="Skip one question per quiz!",
                cost=40,
                icon="🔄",
                effect={"type": "functional", "quiz_skips": 1},
                category="functional"
            ),
            "lucky_charm": Perk(
                id="lucky_charm",
                name="Lucky Charm 🍀",
                description="10% chance of bonus coins!",
                cost=90,
                icon="🍀",
                effect={"type": "boost", "luck_bonus": 0.1},
                category="boost"
            ),
            "study_streak_shield": Perk(
                id="study_streak_shield",
                name="Streak Shield 🛡️",
                description="Protect your streak for one missed day!",
                cost=150,
                icon="🛡️",
                effect={"type": "functional", "streak_protection": 1},
                category="functional"
            )
        }
        
        return perks
    
    def _calculate_level_requirements(self) -> Dict[int, int]:
        """Calculate XP requirements for each level"""
        requirements = {1: 0}  # Level 1 starts at 0 XP
        
        for level in range(2, 101):  # Support up to level 100
            # Exponential growth: level^2 * 50
            requirements[level] = (level - 1) ** 2 * 50
        
        return requirements
    
    def _load_daily_challenges(self) -> List[Dict]:
        """Load or generate daily challenges"""
        # For now, return static challenges
        # In a real implementation, these could be dynamic
        challenges = [
            {
                "id": "daily_quiz",
                "name": "Daily Quiz Challenge",
                "description": "Complete 3 quizzes today",
                "requirement": {"quizzes_today": 3},
                "reward": 50,
                "type": "daily"
            },
            {
                "id": "perfect_attention",
                "name": "Focus Champion",
                "description": "Maintain >80% attention for 20 minutes",
                "requirement": {"attention_time": 20},
                "reward": 40,
                "type": "daily"
            },
            {
                "id": "video_learning",
                "name": "Video Learner",
                "description": "Watch 2 educational videos",
                "requirement": {"videos_today": 2},
                "reward": 30,
                "type": "daily"
            }
        ]
        
        return challenges
    
    def award_coins(self, amount: int, reason: str, multipliers: Dict = None) -> Dict:
        """
        Award coins to student with optional multipliers
        
        Args:
            amount: Base coin amount
            reason: Reason for awarding coins
            multipliers: Optional multipliers to apply
            
        Returns:
            Dictionary with award details
        """
        try:
            if multipliers is None:
                multipliers = {}
            
            # Calculate final amount with multipliers
            final_amount = amount
            applied_multipliers = []
            
            # Apply streak bonus
            if self.current_student.streak_days >= 7:
                streak_bonus = min(self.current_student.streak_days / 7 * 0.1, 0.5)  # Max 50% bonus
                final_amount *= (1 + streak_bonus)
                applied_multipliers.append(f"Streak bonus: +{streak_bonus*100:.0f}%")
            
            # Apply perk multipliers
            if "double_coins" in self.current_student.owned_perks:
                final_amount *= 2
                applied_multipliers.append("Double coins perk: +100%")
            
            # Apply luck bonus
            if "lucky_charm" in self.current_student.owned_perks:
                if random.random() < 0.1:  # 10% chance
                    lucky_bonus = random.randint(10, 50)
                    final_amount += lucky_bonus
                    applied_multipliers.append(f"Lucky charm: +{lucky_bonus} coins!")
            
            # Apply custom multipliers
            for multiplier_name, multiplier_value in multipliers.items():
                if multiplier_name in self.coin_multipliers:
                    final_amount *= multiplier_value
                    applied_multipliers.append(f"{multiplier_name}: +{(multiplier_value-1)*100:.0f}%")
            
            final_amount = int(final_amount)
            
            # Update student profile
            self.current_student.current_coins += final_amount
            self.current_student.total_coins += final_amount
            self.current_student.last_activity = datetime.now()
            
            # Award XP (coins = XP for simplicity)
            self._award_experience(final_amount)
            
            # Check for achievements
            new_achievements = self._check_achievements()
            
            # Save progress
            self._save_student_profiles()
            
            result = {
                "coins_awarded": final_amount,
                "base_amount": amount,
                "current_coins": self.current_student.current_coins,
                "total_coins": self.current_student.total_coins,
                "reason": reason,
                "multipliers_applied": applied_multipliers,
                "new_achievements": new_achievements,
                "level": self.current_student.level,
                "experience_points": self.current_student.experience_points
            }
            
            logger.info(f"Awarded {final_amount} coins for {reason}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to award coins: {e}")
            return {
                "coins_awarded": 0,
                "error": str(e)
            }
    
    def spend_coins(self, amount: int, reason: str) -> bool:
        """
        Spend coins from student account
        
        Args:
            amount: Coins to spend
            reason: Reason for spending
            
        Returns:
            Success status
        """
        try:
            if self.current_student.current_coins >= amount:
                self.current_student.current_coins -= amount
                self.current_student.last_activity = datetime.now()
                self._save_student_profiles()
                
                logger.info(f"Spent {amount} coins for {reason}")
                return True
            else:
                logger.warning(f"Insufficient coins: need {amount}, have {self.current_student.current_coins}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to spend coins: {e}")
            return False
    
    def _award_experience(self, amount: int):
        """Award experience points and check for level up"""
        old_level = self.current_student.level
        self.current_student.experience_points += amount
        
        # Check for level up
        new_level = self._calculate_level(self.current_student.experience_points)
        if new_level > old_level:
            self.current_student.level = new_level
            # Award level up bonus
            level_bonus = new_level * 20
            self.current_student.current_coins += level_bonus
            logger.info(f"Level up! Now level {new_level}, awarded {level_bonus} bonus coins")
    
    def _calculate_level(self, experience: int) -> int:
        """Calculate level based on experience points"""
        for level in range(100, 0, -1):
            if experience >= self.level_requirements.get(level, 0):
                return level
        return 1
    
    def purchase_perk(self, perk_id: str) -> Dict:
        """
        Purchase a perk with coins
        
        Args:
            perk_id: ID of the perk to purchase
            
        Returns:
            Purchase result dictionary
        """
        try:
            if perk_id not in self.perks:
                return {"success": False, "error": "Perk not found"}
            
            perk = self.perks[perk_id]
            
            # Check if already owned
            if perk_id in self.current_student.owned_perks:
                return {"success": False, "error": "Perk already owned"}
            
            # Check if can afford
            if self.current_student.current_coins < perk.cost:
                return {
                    "success": False, 
                    "error": f"Insufficient coins. Need {perk.cost}, have {self.current_student.current_coins}"
                }
            
            # Make purchase
            success = self.spend_coins(perk.cost, f"Purchased {perk.name}")
            if success:
                self.current_student.owned_perks.append(perk_id)
                perk.owned = True
                perk.purchase_date = datetime.now()
                
                result = {
                    "success": True,
                    "perk": perk,
                    "remaining_coins": self.current_student.current_coins,
                    "message": f"Successfully purchased {perk.name}!"
                }
                
                logger.info(f"Purchased perk: {perk.name}")
                return result
            else:
                return {"success": False, "error": "Failed to complete purchase"}
                
        except Exception as e:
            logger.error(f"Failed to purchase perk: {e}")
            return {"success": False, "error": str(e)}
    
    def _check_achievements(self) -> List[Achievement]:
        """Check for newly unlocked achievements"""
        new_achievements = []
        
        for achievement_id, achievement in self.achievements.items():
            if achievement_id in self.current_student.achievements:
                continue  # Already unlocked
            
            if self._check_achievement_requirement(achievement):
                self.current_student.achievements.append(achievement_id)
                achievement.unlocked = True
                achievement.unlock_date = datetime.now()
                
                # Award achievement coins
                self.current_student.current_coins += achievement.reward_coins
                self.current_student.total_coins += achievement.reward_coins
                
                new_achievements.append(achievement)
                logger.info(f"Achievement unlocked: {achievement.name}")
        
        return new_achievements
    
    def _check_achievement_requirement(self, achievement: Achievement) -> bool:
        """Check if achievement requirement is met"""
        requirement = achievement.requirement
        student = self.current_student
        
        try:
            if "quizzes_completed" in requirement:
                return student.total_quizzes >= requirement["quizzes_completed"]
            
            if "perfect_quiz" in requirement:
                # This would need to be tracked separately
                # For now, assume it's met if student has high total coins
                return student.total_coins >= 200
            
            if "streak_days" in requirement:
                return student.streak_days >= requirement["streak_days"]
            
            if "total_coins" in requirement:
                return student.total_coins >= requirement["total_coins"]
            
            if "videos_watched" in requirement:
                return student.total_videos >= requirement["videos_watched"]
            
            if "subject_mastery" in requirement:
                # This would need subject-specific tracking
                # For now, approximate based on total quizzes
                return student.total_quizzes >= 20
            
            if "attention_mastery" in requirement:
                # This would need attention tracking integration
                return student.study_minutes >= requirement["attention_mastery"]
            
            if "early_study_days" in requirement:
                # This would need time-based tracking
                return student.total_quizzes >= 10  # Approximation
            
        except Exception as e:
            logger.error(f"Error checking achievement requirement: {e}")
        
        return False
    
    def update_activity(self, activity_type: str, **kwargs):
        """
        Update student activity and check for streak updates
        
        Args:
            activity_type: Type of activity (quiz, video, study)
            **kwargs: Additional activity data
        """
        try:
            now = datetime.now()
            self.current_student.last_activity = now
            
            # Update activity counters
            if activity_type == "quiz":
                self.current_student.total_quizzes += 1
            elif activity_type == "video":
                self.current_student.total_videos += 1
            elif activity_type == "study":
                study_minutes = kwargs.get("minutes", 0)
                self.current_student.study_minutes += study_minutes
            
            # Update streak
            self._update_streak()
            
            # Check for daily challenges
            self._check_daily_challenges(activity_type, **kwargs)
            
            self._save_student_profiles()
            
        except Exception as e:
            logger.error(f"Failed to update activity: {e}")
    
    def _update_streak(self):
        """Update study streak based on daily activity"""
        now = datetime.now()
        last_activity = self.current_student.last_activity
        
        if last_activity:
            days_diff = (now.date() - last_activity.date()).days
            
            if days_diff == 0:
                # Same day, no change to streak
                pass
            elif days_diff == 1:
                # Next day, increment streak
                self.current_student.streak_days += 1
                if self.current_student.streak_days > self.current_student.longest_streak:
                    self.current_student.longest_streak = self.current_student.streak_days
            else:
                # Missed days, reset streak
                self.current_student.streak_days = 1
        else:
            # First activity
            self.current_student.streak_days = 1
    
    def _check_daily_challenges(self, activity_type: str, **kwargs):
        """Check if daily challenges are completed"""
        # This would need more sophisticated tracking
        # For now, just award bonus coins for certain activities
        
        bonus_coins = 0
        if activity_type == "quiz" and kwargs.get("score", 0) >= 80:
            bonus_coins = 10
        elif activity_type == "video":
            bonus_coins = 5
        
        if bonus_coins > 0:
            self.award_coins(bonus_coins, f"Daily challenge bonus - {activity_type}")
    
    def get_leaderboard(self, metric: str = "total_coins", limit: int = 10) -> List[LeaderboardEntry]:
        """
        Generate leaderboard based on specified metric
        
        Args:
            metric: Metric to rank by (total_coins, level, streak_days, etc.)
            limit: Number of entries to return
            
        Returns:
            List of leaderboard entries
        """
        try:
            # Get all students and sort by metric
            students = list(self.student_profiles.values())
            
            if metric == "total_coins":
                students.sort(key=lambda s: s.total_coins, reverse=True)
            elif metric == "level":
                students.sort(key=lambda s: (s.level, s.experience_points), reverse=True)
            elif metric == "streak_days":
                students.sort(key=lambda s: s.streak_days, reverse=True)
            elif metric == "quizzes":
                students.sort(key=lambda s: s.total_quizzes, reverse=True)
            else:
                students.sort(key=lambda s: s.total_coins, reverse=True)
            
            # Create leaderboard entries
            leaderboard = []
            for i, student in enumerate(students[:limit]):
                score = getattr(student, metric, student.total_coins)
                display_name = f"Student {student.student_id[-4:]}" if len(student.student_id) > 4 else student.student_id
                
                entry = LeaderboardEntry(
                    rank=i + 1,
                    student_id=student.student_id,
                    display_name=display_name,
                    score=score,
                    metric=metric
                )
                leaderboard.append(entry)
            
            return leaderboard
            
        except Exception as e:
            logger.error(f"Failed to generate leaderboard: {e}")
            return []
    
    def get_student_stats(self) -> Dict:
        """Get comprehensive student statistics"""
        student = self.current_student
        
        # Calculate level progress
        current_level_xp = self.level_requirements.get(student.level, 0)
        next_level_xp = self.level_requirements.get(student.level + 1, current_level_xp + 100)
        level_progress = ((student.experience_points - current_level_xp) / 
                         (next_level_xp - current_level_xp)) * 100
        
        # Get achievement progress
        total_achievements = len(self.achievements)
        unlocked_achievements = len(student.achievements)
        achievement_progress = (unlocked_achievements / total_achievements) * 100
        
        # Calculate daily activity
        today = datetime.now().date()
        daily_activity = {
            "quizzes_today": 0,  # Would need daily tracking
            "videos_today": 0,
            "study_time_today": 0
        }
        
        return {
            "student_id": student.student_id,
            "level": student.level,
            "level_progress": round(level_progress, 1),
            "experience_points": student.experience_points,
            "current_coins": student.current_coins,
            "total_coins": student.total_coins,
            "streak_days": student.streak_days,
            "longest_streak": student.longest_streak,
            "total_quizzes": student.total_quizzes,
            "total_videos": student.total_videos,
            "study_minutes": student.study_minutes,
            "achievements": {
                "unlocked": unlocked_achievements,
                "total": total_achievements,
                "progress": round(achievement_progress, 1)
            },
            "perks_owned": len(student.owned_perks),
            "daily_activity": daily_activity,
            "join_date": student.join_date.strftime("%Y-%m-%d"),
            "last_activity": student.last_activity.strftime("%Y-%m-%d %H:%M")
        }
    
    def get_available_perks(self) -> List[Dict]:
        """Get list of available perks for purchase"""
        available_perks = []
        
        for perk_id, perk in self.perks.items():
            perk_data = {
                "id": perk.id,
                "name": perk.name,
                "description": perk.description,
                "cost": perk.cost,
                "icon": perk.icon,
                "category": perk.category,
                "owned": perk_id in self.current_student.owned_perks,
                "can_afford": self.current_student.current_coins >= perk.cost
            }
            available_perks.append(perk_data)
        
        # Sort by category and cost
        available_perks.sort(key=lambda p: (p["category"], p["cost"]))
        return available_perks
    
    def get_achievements_summary(self) -> Dict:
        """Get summary of achievements"""
        unlocked = []
        locked = []
        
        for achievement_id, achievement in self.achievements.items():
            achievement_data = {
                "id": achievement.id,
                "name": achievement.name,
                "description": achievement.description,
                "icon": achievement.icon,
                "reward_coins": achievement.reward_coins,
                "rarity": achievement.rarity,
                "unlocked": achievement_id in self.current_student.achievements
            }
            
            if achievement_data["unlocked"]:
                achievement_data["unlock_date"] = achievement.unlock_date
                unlocked.append(achievement_data)
            else:
                locked.append(achievement_data)
        
        return {
            "unlocked": unlocked,
            "locked": locked,
            "total": len(self.achievements),
            "progress": (len(unlocked) / len(self.achievements)) * 100
        }
    
    def reset_student_data(self, student_id: str = None):
        """Reset student data (for testing or new start)"""
        target_id = student_id or self.current_student.student_id
        
        if target_id in self.student_profiles:
            del self.student_profiles[target_id]
        
        self.current_student = self._get_or_create_student(target_id)
        logger.info(f"Reset data for student: {target_id}")

# Singleton instance for global access
_gamification_engine = None

def get_gamification_engine() -> GamificationEngine:
    """Get global gamification engine instance"""
    global _gamification_engine
    if _gamification_engine is None:
        _gamification_engine = GamificationEngine()
    return _gamification_engine

# Test function
def test_gamification_engine():
    """Test the gamification engine"""
    engine = GamificationEngine()
    
    # Test coin awarding
    result = engine.award_coins(50, "Quiz completion", {"quiz_completion": 1.5})
    print(f"Awarded coins: {result}")
    
    # Test perk purchase
    perks = engine.get_available_perks()
    print(f"Available perks: {len(perks)}")
    
    if perks:
        perk_result = engine.purchase_perk(perks[0]["id"])
        print(f"Purchase result: {perk_result}")
    
    # Test achievements
    engine.update_activity("quiz", score=85)
    achievements = engine.get_achievements_summary()
    print(f"Achievements: {achievements['progress']:.1f}% complete")
    
    # Test leaderboard
    leaderboard = engine.get_leaderboard("total_coins", 5)
    print(f"Leaderboard entries: {len(leaderboard)}")
    
    # Test stats
    stats = engine.get_student_stats()
    print(f"Student stats: Level {stats['level']}, {stats['current_coins']} coins")

if __name__ == "__main__":
    test_gamification_engine()