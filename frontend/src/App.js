import React, { useState, useEffect } from 'react';
import axios from 'axios';

// API Configuration
const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Modern, Beautiful UI Styles
const styles = `
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Fredoka+One:wght@400&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-attachment: fixed;
    min-height: 100vh;
    line-height: 1.6;
    overflow-x: hidden;
}

.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
    position: relative;
}

/* Floating particles animation */
.container::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.1) 1px, transparent 1px),
        radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.1) 1px, transparent 1px),
        radial-gradient(circle at 40% 40%, rgba(255, 255, 255, 0.05) 2px, transparent 2px);
    background-size: 50px 50px, 80px 80px, 120px 120px;
    animation: float 20s ease-in-out infinite;
    pointer-events: none;
    z-index: -1;
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    33% { transform: translateY(-20px) rotate(120deg); }
    66% { transform: translateY(-10px) rotate(240deg); }
}

.main-title {
    font-family: 'Fredoka One', cursive;
    background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #ffeaa7);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 800;
    text-align: center;
    margin: 30px 0;
    animation: gradientFlow 3s ease-in-out infinite;
    text-shadow: 0 4px 8px rgba(0,0,0,0.1);
    letter-spacing: 2px;
}

@keyframes gradientFlow {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* Button Styles */
.big-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 25px;
    font-weight: 600;
    font-size: 18px;
    padding: 18px 35px;
    border: none;
    box-shadow: 
        0 8px 32px rgba(102, 126, 234, 0.3),
        inset 0 1px 0 rgba(255,255,255,0.2);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    cursor: pointer;
    position: relative;
    overflow: hidden;
    margin: 10px;
    min-width: 180px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-family: 'Poppins', sans-serif;
}

.big-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s;
}

.big-button:hover::before {
    left: 100%;
}

.big-button:hover {
    transform: translateY(-4px) scale(1.05);
    box-shadow: 
        0 12px 40px rgba(102, 126, 234, 0.4),
        inset 0 1px 0 rgba(255,255,255,0.3);
}

.big-button:active {
    transform: translateY(-2px) scale(1.02);
}

.success-button {
    background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
    color: white;
    border-radius: 25px;
    font-weight: 600;
    font-size: 18px;
    padding: 18px 35px;
    border: none;
    box-shadow: 
        0 8px 32px rgba(86, 171, 47, 0.3),
        inset 0 1px 0 rgba(255,255,255,0.2);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    cursor: pointer;
    margin: 10px;
    min-width: 180px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.success-button:hover {
    transform: translateY(-4px) scale(1.05);
    box-shadow: 0 12px 40px rgba(86, 171, 47, 0.4);
}

.warning-button {
    background: linear-gradient(135deg, #ff7f50 0%, #ff6b6b 100%);
    color: white;
    border-radius: 25px;
    font-weight: 600;
    font-size: 18px;
    padding: 18px 35px;
    border: none;
    box-shadow: 
        0 8px 32px rgba(255, 107, 107, 0.3),
        inset 0 1px 0 rgba(255,255,255,0.2);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    cursor: pointer;
    margin: 10px;
    min-width: 180px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.warning-button:hover {
    transform: translateY(-4px) scale(1.05);
    box-shadow: 0 12px 40px rgba(255, 107, 107, 0.4);
}

/* Card Styles */
.kid-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 25px;
    padding: 30px;
    margin: 20px 10px;
    box-shadow: 
        0 20px 60px rgba(0,0,0,0.1),
        inset 0 1px 0 rgba(255,255,255,0.8);
    border: 1px solid rgba(255,255,255,0.2);
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
}

.kid-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #667eea, #764ba2);
    border-radius: 25px 25px 0 0;
}

.kid-card:hover {
    transform: translateY(-8px);
    box-shadow: 
        0 30px 80px rgba(0,0,0,0.15),
        inset 0 1px 0 rgba(255,255,255,0.9);
}

.coin-display {
    background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
    color: #8B4513;
    font-size: 28px;
    font-weight: 700;
    padding: 20px 30px;
    border-radius: 50px;
    text-align: center;
    box-shadow: 
        0 10px 30px rgba(247, 151, 30, 0.3),
        inset 0 1px 0 rgba(255,255,255,0.3);
    position: relative;
    overflow: hidden;
    animation: coinGlow 2s ease-in-out infinite alternate;
    font-family: 'Fredoka One', cursive;
    letter-spacing: 2px;
}

@keyframes coinGlow {
    0% { box-shadow: 0 10px 30px rgba(247, 151, 30, 0.3); }
    100% { box-shadow: 0 10px 40px rgba(247, 151, 30, 0.5); }
}

/* Tab Navigation */
.tab-nav {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    color: white;
    font-size: 16px;
    font-weight: 600;
    border-radius: 20px 20px 0 0;
    padding: 15px 25px;
    cursor: pointer;
    transition: all 0.3s ease;
    margin: 0 5px;
    border: 1px solid rgba(255,255,255,0.1);
    position: relative;
    overflow: hidden;
}

.tab-nav::before {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, #667eea, #764ba2);
    transform: scaleX(0);
    transition: transform 0.3s ease;
}

.tab-nav:hover::before {
    transform: scaleX(1);
}

.tab-nav.active {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(15px);
    box-shadow: 0 8px 32px rgba(255,255,255,0.1);
}

.tab-nav.active::before {
    transform: scaleX(1);
}

.quiz-card {
    background: linear-gradient(135deg, rgba(255, 228, 225, 0.9), rgba(255, 240, 245, 0.9));
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 25px;
    margin: 15px 0;
    box-shadow: 0 10px 40px rgba(255, 105, 180, 0.1);
    border-left: 6px solid #ff69b4;
    transition: all 0.3s ease;
    cursor: pointer;
}

.quiz-card:hover {
    transform: translateX(10px);
    box-shadow: 0 15px 50px rgba(255, 105, 180, 0.2);
}

.attention-alert {
    background: linear-gradient(135deg, #ff6b6b, #ee5a24);
    color: white;
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    font-size: 20px;
    font-weight: 600;
    animation: alertPulse 2s infinite;
    box-shadow: 0 15px 50px rgba(255, 107, 107, 0.3);
    border: 2px solid rgba(255,255,255,0.2);
}

@keyframes alertPulse {
    0%, 100% { 
        transform: scale(1);
        box-shadow: 0 15px 50px rgba(255, 107, 107, 0.3);
    }
    50% { 
        transform: scale(1.05);
        box-shadow: 0 20px 60px rgba(255, 107, 107, 0.5);
    }
}

.parent-lock {
    background: linear-gradient(135deg, #8B4513, #A0522D);
    color: white;
    border-radius: 15px;
    padding: 20px;
    font-weight: 600;
    box-shadow: 0 10px 30px rgba(139, 69, 19, 0.3);
    transition: all 0.3s ease;
}

.parent-lock:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 40px rgba(139, 69, 19, 0.4);
}

.video-container {
    border-radius: 25px;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    background: #000;
    height: 450px;
    position: relative;
    border: 3px solid rgba(255,255,255,0.1);
}

.webcam-preview {
    width: 250px;
    height: 180px;
    border-radius: 20px;
    border: 3px solid rgba(102, 126, 234, 0.5);
    background: linear-gradient(135deg, #000 0%, #333 100%);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    font-weight: 600;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    margin: 20px auto;
    transition: all 0.3s ease;
}

.webcam-preview:hover {
    transform: scale(1.05);
    border-color: rgba(102, 126, 234, 0.8);
}

/* Typography */
h1, h2, h3 {
    color: white;
    font-weight: 700;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    margin-bottom: 20px;
    font-family: 'Poppins', sans-serif;
}

h1 { font-size: clamp(2rem, 4vw, 3rem); }
h2 { font-size: clamp(1.5rem, 3vw, 2.5rem); }
h3 { font-size: clamp(1.2rem, 2.5vw, 2rem); }

/* Input Styles */
input, select {
    background: rgba(255, 255, 255, 0.9);
    border: 2px solid rgba(102, 126, 234, 0.3);
    border-radius: 15px;
    padding: 15px 20px;
    font-size: 16px;
    font-weight: 500;
    width: 100%;
    margin: 10px 0;
    transition: all 0.3s ease;
    font-family: 'Poppins', sans-serif;
}

input:focus, select:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
    transform: translateY(-2px);
}

/* Layout Improvements */
.header-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    flex-wrap: wrap;
    gap: 20px;
}

.tab-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 30px;
    justify-content: center;
}

.content-section {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border-radius: 25px;
    padding: 40px;
    margin: 20px 0;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 20px 60px rgba(0,0,0,0.1);
}

.button-group {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
    justify-content: center;
    margin: 20px 0;
}

.chat-container {
    height: 400px;
    overflow-y: auto;
    border: 2px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 20px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    margin: 20px 0;
}

.chat-message {
    margin: 15px 0;
    padding: 15px 20px;
    border-radius: 20px;
    max-width: 80%;
    word-wrap: break-word;
}

.chat-message.user {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    margin-left: auto;
    text-align: right;
}

.chat-message.assistant {
    background: rgba(255,255,255,0.9);
    color: #333;
    margin-right: auto;
}

/* Responsive Design */
@media (max-width: 768px) {
    .container {
        padding: 15px;
    }
    
    .main-title {
        font-size: 2rem;
        margin: 20px 0;
    }
    
    .big-button, .success-button, .warning-button {
        font-size: 16px;
        padding: 15px 25px;
        min-width: 150px;
    }
    
    .coin-display {
        font-size: 20px;
        padding: 15px 20px;
    }
    
    .kid-card {
        padding: 20px;
        margin: 15px 5px;
    }
    
    .content-section {
        padding: 25px;
    }
    
    .tab-nav {
        padding: 12px 20px;
        font-size: 14px;
    }
    
    .header-section {
        flex-direction: column;
        text-align: center;
    }
    
    .tab-container {
        flex-direction: column;
        align-items: center;
    }
    
    .button-group {
        flex-direction: column;
        align-items: center;
    }
    
    .webcam-preview {
        width: 200px;
        height: 150px;
    }
    
    .video-container {
        height: 300px;
    }
}

@media (max-width: 480px) {
    .main-title {
        font-size: 1.5rem;
    }
    
    .big-button, .success-button, .warning-button {
        font-size: 14px;
        padding: 12px 20px;
        min-width: 120px;
    }
    
    .coin-display {
        font-size: 18px;
        padding: 12px 16px;
    }
    
    .content-section {
        padding: 20px;
    }
    
    .kid-card {
        padding: 15px;
    }
}

/* Scrollbar Styling */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.1);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #764ba2, #667eea);
}

/* Loading Animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 0.6s ease-out;
}
`;

const App = () => {
  // Game State
  const [gameState, setGameState] = useState({
    coins: 100,
    total_coins_earned: 100,
    streak_days: 0,
    quizzes_completed: 0,
    videos_watched: 0,
    current_level: 1,
    unlocked_perks: [],
    daily_progress: { videos: 0, quizzes: 0, study_time: 0 },
    attention_score: 100,
    parent_authenticated: false,
  });

  // App States
  const [currentScreen, setCurrentScreen] = useState('welcome');
  const [quizQuestions, setQuizQuestions] = useState([]);
  const [quizAnswers, setQuizAnswers] = useState([]);
  const [currentVideo, setCurrentVideo] = useState({});
  const [userGrade, setUserGrade] = useState('');
  const [userBoard, setUserBoard] = useState('');
  const [userSubject, setUserSubject] = useState('');
  const [activeTab, setActiveTab] = useState('home');
  const [chatHistory, setChatHistory] = useState([]);
  const [chatMessage, setChatMessage] = useState('');
  const [learningPlan, setLearningPlan] = useState('Click to generate your plan!');
  const [attentionAlert, setAttentionAlert] = useState('');
  const [socraticQuestion, setSocraticQuestion] = useState('');
  const [videoTitle, setVideoTitle] = useState('');
  const [videoPlayerHtml, setVideoPlayerHtml] = useState('');
  const [quizIntro, setQuizIntro] = useState('');
  const [quizContainerVisible, setQuizContainerVisible] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [answerOptions, setAnswerOptions] = useState(['', '', '', '']);
  const [quizProgress, setQuizProgress] = useState('');
  const [quizResults, setQuizResults] = useState('');
  const [perkResult, setPerkResult] = useState('');
  const [parentPin, setParentPin] = useState('');
  const [parentStatus, setParentStatus] = useState('');
  const [selectionStatus, setSelectionStatus] = useState('');
  const [videoCompletionMsg, setVideoCompletionMsg] = useState('');
  const [attentionStatus, setAttentionStatus] = useState('');
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  
  // Loading States
  const [loading, setLoading] = useState({
    roadmap: false,
    chat: false,
    quiz: false,
    video: false,
    parent: false,
    perk: false,
  });

  // Error States
  const [errors, setErrors] = useState({
    api: '',
    general: '',
  });

  // Sample Data (from original)
  const SAMPLE_VIDEOS = {
    Math: [
      { title: 'Fun with Fractions! 🥧', duration: '15:30', url: 'https://www.youtube.com/embed/dQw4w9WgXcQ' },
      // ... other videos
    ],
    // ... other subjects
  };

  const PERKS_SHOP = [
    { name: 'Golden Star Badge ⭐', cost: 50, description: 'Show everyone you\'re a star student!' },
    // ... other perks
  ];

  // API Functions
  const addCoins = (amount) => {
    setGameState((prev) => ({
      ...prev,
      coins: prev.coins + amount,
      total_coins_earned: prev.total_coins_earned + amount,
    }));
  };

  const spendCoins = (amount) => {
    if (gameState.coins >= amount) {
      setGameState((prev) => ({ ...prev, coins: prev.coins - amount }));
      return true;
    }
    return false;
  };

  const verifyParentPin = async (pin) => {
    setLoading(prev => ({ ...prev, parent: true }));
    try {
      const response = await api.post('/verify_parent', { pin });
      if (response.data.success) {
        setGameState((prev) => ({ ...prev, parent_authenticated: true }));
        setParentStatus('✅ Parent access granted!');
      } else {
        setParentStatus('❌ Wrong PIN. Try again!');
      }
    } catch (error) {
      console.error('Parent verification error:', error);
      setParentStatus('❌ Error verifying PIN. Please try again.');
    } finally {
      setLoading(prev => ({ ...prev, parent: false }));
    }
  };

  const logoutParent = async () => {
    try {
      await api.post('/logout_parent');
      setGameState((prev) => ({ ...prev, parent_authenticated: false }));
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const getVideoForSubject = async (subject) => {
    setLoading(prev => ({ ...prev, video: true }));
    try {
      const response = await api.get(`/get_video_for_subject?subject=${subject}`);
      return response.data;
    } catch (error) {
      console.error('Get video error:', error);
      return SAMPLE_VIDEOS[subject]?.[0] || { title: 'Sample Video', url: 'https://www.youtube.com/embed/dQw4w9WgXcQ' };
    } finally {
      setLoading(prev => ({ ...prev, video: false }));
    }
  };

  const simulateAttentionCheck = async () => {
    try {
      const response = await api.get('/simulate_attention_check');
      const { attention_level, needs_check, socratic_question } = response.data || {};
      
      setGameState((prev) => ({ ...prev, attention_score: attention_level || 100 }));
      
      if (needs_check && socratic_question) {
        setSocraticQuestion(socratic_question);
        setAttentionAlert(`🚨 Focus Check! 🚨\n\n${socratic_question}`);
        return true;
      }
      return false;
    } catch (error) {
      console.error('Attention check error:', error);
      return false;
    }
  };

  const completeVideoWatching = async (subject) => {
    try {
      const response = await api.post('/complete_video_watching', { subject });
      const { coins_earned } = response.data;
      
      addCoins(coins_earned);
      setGameState((prev) => ({
        ...prev,
        videos_watched: prev.videos_watched + 1,
        daily_progress: { ...prev.daily_progress, videos: prev.daily_progress.videos + 1 },
      }));
      setVideoCompletionMsg(`🎉 Great job! You earned ${coins_earned} coins for watching the video! 🎉`);
    } catch (error) {
      console.error('Complete video error:', error);
      setVideoCompletionMsg('🎉 Great job! Video completed!');
    }
  };

  const generateQuiz = async (subject, grade) => {
    setLoading(prev => ({ ...prev, quiz: true }));
    try {
      const response = await api.post('/generate_quiz', { 
        subject,
        grade: grade || userGrade
      });
      return response.data.questions;
    } catch (error) {
      console.error('Generate quiz error:', error);
      // Fallback mock data
      return [
        { question: 'What is 2+2?', options: ['3', '4', '5', '6'], correct: 1 },
        { question: 'What is the capital of France?', options: ['London', 'Berlin', 'Paris', 'Madrid'], correct: 2 },
      ];
    } finally {
      setLoading(prev => ({ ...prev, quiz: false }));
    }
  };

  const calculateQuizScore = async (answers, questions) => {
    try {
      const correctAnswers = questions.map(q => q.correct);
      const response = await api.post('/calculate_quiz_score', { 
        answers,
        correct_answers: correctAnswers
      });
      
      const { score, percentage, coins_earned, message } = response.data;
      
      addCoins(coins_earned);
      setGameState((prev) => ({
        ...prev,
        quizzes_completed: prev.quizzes_completed + 1,
        daily_progress: { ...prev.daily_progress, quizzes: prev.daily_progress.quizzes + 1 },
      }));
      
      return { score, percentage, coins: coins_earned, message };
    } catch (error) {
      console.error('Calculate quiz score error:', error);
      // Fallback calculation
      const correctAnswers = questions.map(q => q.correct);
      const correct = answers.reduce((acc, a, i) => acc + (a === correctAnswers[i] ? 1 : 0), 0);
      const total = questions.length;
      const percentage = (correct / total) * 100;
      const coins = percentage >= 80 ? 50 : 10;
      return { score: `${correct}/${total}`, percentage, coins, message: 'Keep practicing!' };
    }
  };

  const getCoinDisplay = () => `🪙 ${gameState.coins} Coins`;

  const buyPerk = async (perkIndex) => {
    setLoading(prev => ({ ...prev, perk: true }));
    try {
      const response = await api.post('/buy_perk', { perk_index: perkIndex });
      
      if (response.data.success) {
        const perk = PERKS_SHOP[perkIndex];
        setGameState((prev) => ({ 
          ...prev, 
          coins: prev.coins - perk.cost,
          unlocked_perks: [...prev.unlocked_perks, perk.name] 
        }));
        setPerkResult(`🎉 You bought ${perk.name}! Enjoy your new perk!`);
      } else {
        setPerkResult(response.data.message || '❌ Unable to purchase perk!');
      }
    } catch (error) {
      console.error('Buy perk error:', error);
      setPerkResult('❌ Error purchasing perk. Please try again.');
    } finally {
      setLoading(prev => ({ ...prev, perk: false }));
    }
  };

  const getLeaderboard = async () => {
    try {
      const response = await api.get('/leaderboard');
      return response.data.leaderboard;
    } catch (error) {
      console.error('Leaderboard error:', error);
      return `
    🏆 Your Progress 🏆
    - 🪙 Total Coins Earned: ${gameState.total_coins_earned}
    - 🎯 Quizzes Completed: ${gameState.quizzes_completed}
    - 📺 Videos Watched: ${gameState.videos_watched}
      `;
    }
  };

  const getParentDashboard = async () => {
    try {
      const response = await api.get('/parent_dashboard');
      return response.data.dashboard;
    } catch (error) {
      console.error('Parent dashboard error:', error);
      if (!gameState.parent_authenticated) return '🔒 Please log in as parent first!';
      return '👨‍👩‍👧‍👦 Parent Dashboard - Error loading data';
    }
  };

  const generateLearningRoadmap = async () => {
    setLoading(prev => ({ ...prev, roadmap: true }));
    try {
      const response = await api.post('/generate_roadmap', {
        grade: userGrade,
        board: userBoard,
        subject: userSubject
      });
      
      setLearningPlan(response.data.roadmap);
    } catch (error) {
      console.error('Generate roadmap error:', error);
      setLearningPlan('❌ Unable to generate roadmap. Please ensure you have selected your grade, board, and subject, and that the backend is running.');
    } finally {
      setLoading(prev => ({ ...prev, roadmap: false }));
    }
  };

  const chatWithTutor = async (message) => {
    if (!message.trim()) return;
    
    setLoading(prev => ({ ...prev, chat: true }));
    
    // Add user message immediately
    const newChatHistory = [...chatHistory, { role: 'user', content: message }];
    setChatHistory(newChatHistory);
    setChatMessage('');
    
    try {
      const response = await api.post('/chat_with_tutor', {
        message,
        subject: userSubject || 'General',
        grade: userGrade || '10th'
      });
      
      const botResponse = response.data?.response || 'Sorry, I didn\'t get a response from the AI.';
      setChatHistory([...newChatHistory, { role: 'assistant', content: botResponse }]);
    } catch (error) {
      console.error('Chat error:', error);
      let errorMessage = '❌ Sorry, I\'m having trouble connecting right now.';
      
      if (error.response?.status === 403) {
        errorMessage = '❌ API Authentication failed. Please check your EURIAI API key.';
      } else if (error.response?.status === 503) {
        errorMessage = '❌ AI Tutor service is currently unavailable. Please try again later.';
      } else if (!error.response) {
        errorMessage = '❌ Cannot connect to backend. Please make sure the backend is running.';
      }
      
      setChatHistory([...newChatHistory, { 
        role: 'assistant', 
        content: errorMessage
      }]);
    } finally {
      setLoading(prev => ({ ...prev, chat: false }));
    }
  };

  // Event Handlers
  const switchToSelection = () => setCurrentScreen('selection');

  const handleParentLogin = async () => {
    await verifyParentPin(parentPin);
  };

  const setupLearning = () => {
    if (userGrade && userBoard && userSubject) {
      setSelectionStatus('✅ Great! Let\'s start learning!');
      setCurrentScreen('main');
    } else {
      setSelectionStatus('❌ Please select all options!');
    }
  };

  const loadVideoForSubject = async () => {
    const video = await getVideoForSubject(userSubject);
    setVideoTitle(`Now Playing: ${video.title}`);
    setVideoPlayerHtml(`<iframe width="100%" height="100%" src="${video.url}" frameborder="0" allowfullscreen></iframe>`);
    setCurrentVideo(video);
  };

  const checkAttention = async () => {
    const needsCheck = await simulateAttentionCheck();
    if (needsCheck) {
      setAttentionStatus('⚠️ Pay attention!');
    } else {
      setAttentionStatus('✅ Excellent focus!');
      setAttentionAlert('');
      setSocraticQuestion('');
    }
  };

  const handleSocraticAnswer = (answer) => {
    if (answer) {
      setAttentionAlert('');
      setSocraticQuestion('');
      setAttentionStatus('👏 Great answer!');
    }
  };

  const startQuizSession = async () => {
    const questions = await generateQuiz(userSubject, userGrade);
    setQuizQuestions(questions);
    setQuizAnswers(new Array(questions.length).fill(-1)); // Initialize with -1 for unanswered
    setQuizContainerVisible(true);
    setCurrentQuestionIndex(0);
    setCurrentQuestion(`Question 1: ${questions[0].question}`);
    setAnswerOptions(questions[0].options);
    setQuizProgress(`Progress: 0/${questions.length}`);
  };

  const handleQuizAnswer = (answerIndex) => {
    const newAnswers = [...quizAnswers];
    newAnswers[currentQuestionIndex] = answerIndex;
    setQuizAnswers(newAnswers);
    
    // Move to next question or show submit button
    if (currentQuestionIndex < quizQuestions.length - 1) {
      const nextIndex = currentQuestionIndex + 1;
      setCurrentQuestionIndex(nextIndex);
      setCurrentQuestion(`Question ${nextIndex + 1}: ${quizQuestions[nextIndex].question}`);
      setAnswerOptions(quizQuestions[nextIndex].options);
      setQuizProgress(`Progress: ${nextIndex}/${quizQuestions.length}`);
    } else {
      setQuizProgress(`Progress: ${quizQuestions.length}/${quizQuestions.length} - Ready to submit!`);
    }
  };

  const submitQuizFinal = async () => {
    const result = await calculateQuizScore(quizAnswers, quizQuestions);
    setQuizResults(`Quiz Complete! Score: ${result.score} (${result.percentage}%) Coins: ${result.coins} - ${result.message}`);
    setQuizContainerVisible(false);
  };

  // Render
  return (
    <div className="container fade-in">
      <style>{styles}</style>
      {currentScreen === 'welcome' && (
        <div className="content-section">
          <h1 className="main-title">🚀 Agentic AI Tutor - Your After-School Adventure! 🚀</h1>
          <p style={{ fontSize: '22px', color: 'white', textAlign: 'center', marginBottom: '40px', fontWeight: '500' }}>
            Welcome to the most fun way to learn! 🌟✨
          </p>
          <div className="button-group">
            <button className="big-button" onClick={switchToSelection}>
              🎮 Start as Guest - Let's Learn!
            </button>
          </div>
          <div className="kid-card" style={{ maxWidth: '500px', margin: '40px auto' }}>
            <h3 style={{ color: '#667eea', marginBottom: '20px' }}>👨‍👩‍👧‍👦 Parent Login</h3>
            <input
              type="password"
              placeholder="Enter PIN (default: 1234)"
              value={parentPin}
              onChange={(e) => setParentPin(e.target.value)}
              style={{ marginBottom: '20px' }}
            />
            <div className="button-group">
              <button 
                className="parent-lock" 
                onClick={handleParentLogin}
                disabled={loading.parent}
              >
                {loading.parent ? '🔄 Verifying...' : '🔓 Parent Login'}
              </button>
            </div>
            {parentStatus && (
              <p style={{ textAlign: 'center', marginTop: '15px', fontWeight: '600', color: '#667eea' }}>
                {parentStatus}
              </p>
            )}
          </div>
        </div>
      )}

      {currentScreen === 'selection' && (
        <div className="content-section">
          <h2 style={{ textAlign: 'center', marginBottom: '40px' }}>📚 Let's Set Up Your Learning Adventure! 📚</h2>
          <div style={{ maxWidth: '600px', margin: '0 auto' }}>
            <div className="kid-card">
              <select value={userGrade} onChange={(e) => setUserGrade(e.target.value)}>
                <option value="">🎓 What grade are you in?</option>
                <option>5th Grade</option>
                <option>6th Grade</option>
                <option>7th Grade</option>
                <option>8th Grade</option>
                <option>9th Grade</option>
                <option>10th Grade</option>
              </select>
            </div>
            <div className="kid-card">
              <select value={userBoard} onChange={(e) => setUserBoard(e.target.value)}>
                <option value="">📖 Which board do you follow?</option>
                <option>Karnataka State Board</option>
                <option>CBSE</option>
                <option>ICSE</option>
                <option>IGCSE</option>
                <option>IB</option>
              </select>
            </div>
            <div className="kid-card">
              <select value={userSubject} onChange={(e) => setUserSubject(e.target.value)}>
                <option value="">🔬 What subject shall we explore?</option>
                <option>Math</option>
                <option>Science</option>
                <option>English</option>
                <option>Social Studies</option>
                <option>Physics</option>
                <option>Chemistry</option>
                <option>Biology</option>
              </select>
            </div>
            <div className="button-group">
              <button className="big-button" onClick={setupLearning}>
                🌟 Begin My Learning Journey!
              </button>
            </div>
            {selectionStatus && (
              <div style={{ textAlign: 'center', marginTop: '20px', fontSize: '18px', fontWeight: '600', color: 'white' }}>
                {selectionStatus}
              </div>
            )}
          </div>
        </div>
      )}

      {currentScreen === 'main' && (
        <div>
          <div className="header-section">
            <div className="coin-display">{getCoinDisplay()}</div>
            <button className="warning-button" onClick={() => setCurrentScreen('welcome')}>
              🏠 Back to Home
            </button>
          </div>
          <div className="tab-container">
            <button className={`tab-nav ${activeTab === 'home' ? 'active' : ''}`} onClick={() => setActiveTab('home')}>
              🏠 Dashboard
            </button>
            <button className={`tab-nav ${activeTab === 'video' ? 'active' : ''}`} onClick={() => setActiveTab('video')}>
              📺 Watch & Learn
            </button>
            <button className={`tab-nav ${activeTab === 'quiz' ? 'active' : ''}`} onClick={() => setActiveTab('quiz')}>
              🎯 Quiz Time
            </button>
            <button className={`tab-nav ${activeTab === 'rewards' ? 'active' : ''}`} onClick={() => setActiveTab('rewards')}>
              🏆 Rewards & Shop
            </button>
            <button className={`tab-nav ${activeTab === 'chat' ? 'active' : ''}`} onClick={() => setActiveTab('chat')}>
              💬 AI Tutor Chat
            </button>
            <button className={`tab-nav ${activeTab === 'parent' ? 'active' : ''}`} onClick={() => setActiveTab('parent')}>
              👨‍👩‍👧‍👦 Parent Zone
            </button>
          </div>

          {activeTab === 'home' && (
            <div className="content-section">
              <h3 style={{ textAlign: 'center', marginBottom: '30px' }}>🌟 Welcome to Your Learning Dashboard! 🌟</h3>
              
              <div className="kid-card">
                <h4 style={{ color: '#667eea', marginBottom: '20px' }}>📊 Your Daily Progress</h4>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '20px', marginBottom: '20px' }}>
                  <div style={{ textAlign: 'center', padding: '15px', background: 'rgba(102, 126, 234, 0.1)', borderRadius: '15px' }}>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#667eea' }}>{gameState.videos_watched}</div>
                    <div style={{ fontSize: '14px', color: '#666' }}>Videos Watched</div>
                  </div>
                  <div style={{ textAlign: 'center', padding: '15px', background: 'rgba(86, 171, 47, 0.1)', borderRadius: '15px' }}>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#56ab2f' }}>{gameState.quizzes_completed}</div>
                    <div style={{ fontSize: '14px', color: '#666' }}>Quizzes Completed</div>
                  </div>
                  <div style={{ textAlign: 'center', padding: '15px', background: 'rgba(247, 151, 30, 0.1)', borderRadius: '15px' }}>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#f7971e' }}>{gameState.streak_days}</div>
                    <div style={{ fontSize: '14px', color: '#666' }}>Day Streak</div>
                  </div>
                </div>
              </div>

              <div className="button-group">
                <button 
                  className="success-button" 
                  onClick={generateLearningRoadmap}
                  disabled={loading.roadmap}
                >
                  {loading.roadmap ? '🔄 Generating Plan...' : '🎯 Create My Learning Plan!'}
                </button>
              </div>
              
              {learningPlan !== 'Click to generate your plan!' && (
                <div className="kid-card">
                  <h4 style={{ color: '#667eea', marginBottom: '15px' }}>📋 Your Learning Plan</h4>
                  <p style={{ fontSize: '16px', lineHeight: '1.6', color: '#555' }}>{learningPlan}</p>
                </div>
              )}
            </div>
          )}

          {activeTab === 'video' && (
            <div className="content-section">
              <h3 style={{ textAlign: 'center', marginBottom: '30px' }}>🎬 Educational Videos</h3>
              
              {videoTitle && (
                <div className="kid-card" style={{ textAlign: 'center', marginBottom: '30px' }}>
                  <h4 style={{ color: '#667eea', marginBottom: '10px' }}>{videoTitle}</h4>
                </div>
              )}
              
              <div className="video-container" dangerouslySetInnerHTML={{ __html: videoPlayerHtml }} />
              
              <div className="button-group" style={{ marginTop: '30px' }}>
                <button 
                  className="big-button" 
                  onClick={loadVideoForSubject}
                  disabled={loading.video}
                >
                  {loading.video ? '🔄 Loading Video...' : `📺 Load Video for ${userSubject}`}
                </button>
                <button className="success-button" onClick={() => completeVideoWatching(userSubject)}>
                  ✅ I Finished Watching!
                </button>
              </div>
              
              {videoCompletionMsg && (
                <div className="kid-card" style={{ textAlign: 'center', background: 'linear-gradient(135deg, rgba(86, 171, 47, 0.1), rgba(168, 230, 207, 0.1))' }}>
                  <p style={{ fontSize: '18px', fontWeight: '600', color: '#56ab2f', margin: '0' }}>{videoCompletionMsg}</p>
                </div>
              )}
              
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '20px', marginTop: '30px' }}>
                <div className="webcam-preview">📹 Attention Monitor (Simulated)</div>
                <button className="warning-button" onClick={checkAttention}>🔍 Check My Focus</button>
                
                {attentionStatus && (
                  <div style={{ textAlign: 'center', fontSize: '16px', fontWeight: '600', color: 'white' }}>
                    {attentionStatus}
                  </div>
                )}
              </div>
              
              {attentionAlert && <div className="attention-alert">{attentionAlert}</div>}
              
              {socraticQuestion && (
                <div className="kid-card">
                  <h4 style={{ color: '#667eea', marginBottom: '20px' }}>💭 Quick Question:</h4>
                  <input 
                    placeholder="Type your answer here..." 
                    onChange={(e) => handleSocraticAnswer(e.target.value)}
                    style={{ marginBottom: '20px' }}
                  />
                  <div className="button-group">
                    <button className="warning-button">💡 Submit Answer</button>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'quiz' && (
            <div className="content-section">
              <h3 style={{ textAlign: 'center', marginBottom: '30px' }}>🧠 Test Your Knowledge</h3>
              
              <div className="kid-card" style={{ textAlign: 'center' }}>
                <h4 style={{ color: '#667eea', marginBottom: '20px' }}>Ready to challenge yourself?</h4>
                <p style={{ fontSize: '16px', color: '#666', marginBottom: '30px' }}>
                  Test what you've learned with our interactive quiz for {userSubject}! 🎯
                </p>
                <div className="button-group">
                  <button 
                    className="big-button" 
                    onClick={startQuizSession}
                    disabled={loading.quiz}
                  >
                    {loading.quiz ? '🔄 Creating Quiz...' : `🚀 Start ${userSubject} Quiz!`}
                  </button>
                </div>
              </div>
              
              {quizContainerVisible && (
                <div className="kid-card">
                  <h4 style={{ color: '#667eea', marginBottom: '20px' }}>{currentQuestion}</h4>
                  <div style={{ display: 'grid', gap: '15px', marginBottom: '20px' }}>
                    {answerOptions.map((opt, i) => (
                      <button 
                        key={i} 
                        className="quiz-card" 
                        onClick={() => handleQuizAnswer(i)}
                        style={{ 
                          backgroundColor: quizAnswers[currentQuestionIndex] === i ? 'rgba(102, 126, 234, 0.2)' : undefined 
                        }}
                      >
                        <span style={{ fontWeight: '600', color: '#667eea', marginRight: '10px' }}>{String.fromCharCode(65 + i)}.</span>
                        {opt}
                      </button>
                    ))}
                  </div>
                  <div style={{ textAlign: 'center', marginBottom: '20px' }}>
                    <p style={{ fontSize: '16px', fontWeight: '600', color: '#667eea' }}>{quizProgress}</p>
                  </div>
                  {currentQuestionIndex >= quizQuestions.length - 1 && quizAnswers[currentQuestionIndex] !== -1 && (
                    <div className="button-group">
                      <button className="success-button" onClick={submitQuizFinal}>
                        📝 Submit Quiz
                      </button>
                    </div>
                  )}
                </div>
              )}
              
              {quizResults && (
                <div className="kid-card" style={{ textAlign: 'center', background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1))' }}>
                  <h4 style={{ color: '#667eea', marginBottom: '15px' }}>🎉 Quiz Results!</h4>
                  <p style={{ fontSize: '18px', fontWeight: '600', color: '#667eea' }}>{quizResults}</p>
                </div>
              )}
            </div>
          )}

          {activeTab === 'rewards' && (
            <div className="content-section">
              <h3 style={{ textAlign: 'center', marginBottom: '30px' }}>🎁 Your Amazing Rewards</h3>
              
              <div className="kid-card">
                <h4 style={{ color: '#667eea', marginBottom: '20px' }}>🏆 Your Progress</h4>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
                  <div style={{ textAlign: 'center', padding: '20px', background: 'linear-gradient(135deg, rgba(247, 151, 30, 0.1), rgba(255, 210, 0, 0.1))', borderRadius: '15px' }}>
                    <div style={{ fontSize: '32px', marginBottom: '10px' }}>🪙</div>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#f7971e' }}>{gameState.total_coins_earned}</div>
                    <div style={{ fontSize: '14px', color: '#666' }}>Total Coins Earned</div>
                  </div>
                  <div style={{ textAlign: 'center', padding: '20px', background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1))', borderRadius: '15px' }}>
                    <div style={{ fontSize: '32px', marginBottom: '10px' }}>🎯</div>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#667eea' }}>{gameState.quizzes_completed}</div>
                    <div style={{ fontSize: '14px', color: '#666' }}>Quizzes Completed</div>
                  </div>
                  <div style={{ textAlign: 'center', padding: '20px', background: 'linear-gradient(135deg, rgba(86, 171, 47, 0.1), rgba(168, 230, 207, 0.1))', borderRadius: '15px' }}>
                    <div style={{ fontSize: '32px', marginBottom: '10px' }}>📺</div>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#56ab2f' }}>{gameState.videos_watched}</div>
                    <div style={{ fontSize: '14px', color: '#666' }}>Videos Watched</div>
                  </div>
                </div>
              </div>
              
              <div className="kid-card">
                <h4 style={{ color: '#667eea', marginBottom: '20px' }}>🛍️ Awesome Perk Shop</h4>
                <div style={{ display: 'grid', gap: '20px', marginBottom: '30px' }}>
                  {PERKS_SHOP.map((perk, i) => (
                    <div key={i} className="quiz-card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderLeft: '6px solid #f7971e' }}>
                      <div>
                        <div style={{ fontSize: '18px', fontWeight: '600', color: '#667eea', marginBottom: '8px' }}>{perk.name}</div>
                        <div style={{ fontSize: '14px', color: '#666', marginBottom: '10px' }}>{perk.description}</div>
                        <div style={{ fontSize: '16px', fontWeight: '600', color: '#f7971e' }}>💰 {perk.cost} coins</div>
                      </div>
                      <button 
                        className="warning-button" 
                        onClick={() => buyPerk(i)}
                        disabled={loading.perk}
                        style={{ minWidth: '120px', padding: '10px 20px' }}
                      >
                        {loading.perk ? '🔄 Buying...' : '💳 Buy Now'}
                      </button>
                    </div>
                  ))}
                </div>
                
                {perkResult && (
                  <div style={{ textAlign: 'center', padding: '15px', background: 'rgba(102, 126, 234, 0.1)', borderRadius: '15px' }}>
                    <p style={{ fontSize: '16px', fontWeight: '600', color: '#667eea', margin: '0' }}>{perkResult}</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'chat' && (
            <div className="content-section">
              <h3 style={{ textAlign: 'center', marginBottom: '30px' }}>🤖 Chat with Your AI Tutor</h3>
              
              <div className="kid-card">
                <h4 style={{ color: '#667eea', marginBottom: '20px' }}>💬 Conversation</h4>
                <div className="chat-container">
                  {chatHistory.length === 0 ? (
                    <div style={{ textAlign: 'center', color: '#999', fontStyle: 'italic', marginTop: '50px' }}>
                      👋 Hi there! I'm your AI tutor. Ask me anything about {userSubject}!
                    </div>
                  ) : (
                    chatHistory.map((msg, i) => (
                      <div key={i} className={`chat-message ${msg.role}`}>
                        <strong style={{ marginBottom: '5px', display: 'block' }}>
                          {msg.role === 'user' ? '👤 You' : '🤖 AI Tutor'}:
                        </strong>
                        {msg.content}
                      </div>
                    ))
                  )}
                </div>
                
                <div style={{ display: 'flex', gap: '15px', marginTop: '20px' }}>
                  <input
                    value={chatMessage}
                    onChange={(e) => setChatMessage(e.target.value)}
                    placeholder={`Ask me about ${userSubject}... 🤔`}
                    style={{ flex: '1' }}
                    onKeyPress={(e) => e.key === 'Enter' && chatWithTutor(chatMessage)}
                  />
                  <button 
                    className="big-button" 
                    onClick={() => chatWithTutor(chatMessage)}
                    disabled={!chatMessage.trim() || loading.chat}
                    style={{ minWidth: '120px' }}
                  >
                    {loading.chat ? '🔄 Sending...' : '📤 Send'}
                  </button>
                </div>
                
                <div className="button-group" style={{ marginTop: '20px' }}>
                  <button className="warning-button" onClick={() => setChatHistory([])}>
                    🧹 Clear Chat
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'parent' && (
            <div className="content-section">
              <h3 style={{ textAlign: 'center', marginBottom: '30px' }}>👨‍👩‍👧‍👦 Parent Dashboard</h3>
              
              {gameState.parent_authenticated ? (
                <div>
                  <div className="kid-card">
                    <h4 style={{ color: '#667eea', marginBottom: '20px' }}>📊 Child's Learning Summary</h4>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginBottom: '20px' }}>
                      <div style={{ textAlign: 'center', padding: '20px', background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1))', borderRadius: '15px' }}>
                        <div style={{ fontSize: '32px', marginBottom: '10px' }}>🎯</div>
                        <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#667eea' }}>{gameState.quizzes_completed}</div>
                        <div style={{ fontSize: '14px', color: '#666' }}>Quizzes Completed</div>
                      </div>
                      <div style={{ textAlign: 'center', padding: '20px', background: 'linear-gradient(135deg, rgba(86, 171, 47, 0.1), rgba(168, 230, 207, 0.1))', borderRadius: '15px' }}>
                        <div style={{ fontSize: '32px', marginBottom: '10px' }}>📺</div>
                        <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#56ab2f' }}>{gameState.videos_watched}</div>
                        <div style={{ fontSize: '14px', color: '#666' }}>Videos Watched</div>
                      </div>
                      <div style={{ textAlign: 'center', padding: '20px', background: 'linear-gradient(135deg, rgba(247, 151, 30, 0.1), rgba(255, 210, 0, 0.1))', borderRadius: '15px' }}>
                        <div style={{ fontSize: '32px', marginBottom: '10px' }}>🔥</div>
                        <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#f7971e' }}>{gameState.streak_days}</div>
                        <div style={{ fontSize: '14px', color: '#666' }}>Day Streak</div>
                      </div>
                      <div style={{ textAlign: 'center', padding: '20px', background: 'linear-gradient(135deg, rgba(255, 107, 107, 0.1), rgba(238, 90, 36, 0.1))', borderRadius: '15px' }}>
                        <div style={{ fontSize: '32px', marginBottom: '10px' }}>👁️</div>
                        <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#ff6b6b' }}>{gameState.attention_score}%</div>
                        <div style={{ fontSize: '14px', color: '#666' }}>Attention Score</div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="kid-card">
                    <h4 style={{ color: '#667eea', marginBottom: '20px' }}>🎓 Current Learning</h4>
                    <div style={{ display: 'grid', gap: '15px' }}>
                      <div style={{ padding: '15px', background: 'rgba(102, 126, 234, 0.05)', borderRadius: '10px', border: '2px solid rgba(102, 126, 234, 0.1)' }}>
                        <strong style={{ color: '#667eea' }}>Grade:</strong> {userGrade || 'Not selected'}
                      </div>
                      <div style={{ padding: '15px', background: 'rgba(102, 126, 234, 0.05)', borderRadius: '10px', border: '2px solid rgba(102, 126, 234, 0.1)' }}>
                        <strong style={{ color: '#667eea' }}>Board:</strong> {userBoard || 'Not selected'}
                      </div>
                      <div style={{ padding: '15px', background: 'rgba(102, 126, 234, 0.05)', borderRadius: '10px', border: '2px solid rgba(102, 126, 234, 0.1)' }}>
                        <strong style={{ color: '#667eea' }}>Subject:</strong> {userSubject || 'Not selected'}
                      </div>
                    </div>
                  </div>
                  
                  <div className="button-group">
                    <button className="warning-button" onClick={logoutParent}>
                      🚪 Logout Parent
                    </button>
                  </div>
                </div>
              ) : (
                <div className="kid-card" style={{ textAlign: 'center' }}>
                  <h4 style={{ color: '#667eea', marginBottom: '20px' }}>🔒 Access Restricted</h4>
                  <p style={{ fontSize: '16px', color: '#666', marginBottom: '20px' }}>
                    Please authenticate as a parent to view the dashboard.
                  </p>
                  <p style={{ fontSize: '14px', color: '#999' }}>
                    Go back to the welcome screen to enter your PIN.
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default App;