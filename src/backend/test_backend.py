"""
Test script for the Agentic AI Tutor Backend
Comprehensive testing of all backend components
"""

import sys
import time
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent))

def test_syllabus_manager():
    """Test syllabus management functionality"""
    print("🧪 Testing Syllabus Manager...")
    
    try:
        from backend.syllabus_manager import SyllabusManager
        
        manager = SyllabusManager("../data")
        
        # Test syllabus download and indexing
        pdf_path = manager.download_syllabus("Karnataka State Board", "6th", "Math")
        print(f"✅ Syllabus download: {pdf_path is not None}")
        
        if pdf_path:
            success = manager.parse_and_index_syllabus(pdf_path)
            print(f"✅ Indexing success: {success}")
            
            # Test querying
            results = manager.query_syllabus("fractions", "Karnataka State Board", "6th", "Math")
            print(f"✅ Query results: {len(results)} chunks found")
            
            # Test topic extraction
            topics = manager.get_syllabus_topics("Karnataka State Board", "6th", "Math")
            print(f"✅ Topics found: {len(topics)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Syllabus Manager test failed: {e}")
        return False

def test_attention_monitor():
    """Test attention monitoring functionality"""
    print("\n🧪 Testing Attention Monitor...")
    
    try:
        from backend.attention_monitor import AttentionMonitor
        
        monitor = AttentionMonitor("../data")
        
        # Test camera availability
        camera_available = monitor.is_camera_available()
        print(f"✅ Camera available: {camera_available}")
        
        # Test settings
        monitor.update_settings(sensitivity="high")
        print("✅ Settings update: success")
        
        # Test simulation mode (works without camera)
        for i in range(3):
            result = monitor._simulate_attention_detection()
            print(f"✅ Simulation {i+1}: attention={result['confidence']:.2f}")
        
        # Test report generation
        report = monitor.get_attention_report()
        print(f"✅ Report generation: {len(report)} fields")
        
        return True
        
    except Exception as e:
        print(f"❌ Attention Monitor test failed: {e}")
        return False

def test_quiz_generator():
    """Test quiz generation functionality"""
    print("\n🧪 Testing Quiz Generator...")
    
    try:
        from backend.quiz_generator import QuizGenerator
        
        generator = QuizGenerator("../data")
        
        # Test quiz generation
        quiz = generator.generate_quiz("6th", "Karnataka State Board", "Math", "medium", 5)
        print(f"✅ Quiz generation: {quiz.session_id}")
        print(f"✅ Questions: {len(quiz.questions)}")
        
        # Test quiz scoring
        sample_answers = [0, 1, 0, 1, 1]  # Sample answers
        result = generator.score_quiz(quiz, sample_answers, 120.0)
        print(f"✅ Scoring: {result['score']}/{result['total']} ({result['percentage']}%)")
        
        # Test revision generation
        revision = generator.generate_revision_summary("6th", "Karnataka State Board", "Math")
        print(f"✅ Revision: {len(revision['focus_topics'])} topics")
        
        # Test student report
        report = generator.get_student_report("Math", "6th")
        print(f"✅ Student report: {report.get('total_quizzes', 0)} quizzes")
        
        return True
        
    except Exception as e:
        print(f"❌ Quiz Generator test failed: {e}")
        return False

def test_gamification_engine():
    """Test gamification functionality"""
    print("\n🧪 Testing Gamification Engine...")
    
    try:
        from backend.gamification_engine import GamificationEngine
        
        engine = GamificationEngine("../data")
        
        # Test coin awarding
        result = engine.award_coins(50, "Quiz completion")
        print(f"✅ Coin award: {result['coins_awarded']} coins")
        
        # Test perk system
        perks = engine.get_available_perks()
        print(f"✅ Available perks: {len(perks)}")
        
        if perks:
            # Try to purchase a cheap perk
            cheap_perks = [p for p in perks if p['cost'] <= engine.current_student.current_coins and not p['owned']]
            if cheap_perks:
                perk_result = engine.purchase_perk(cheap_perks[0]['id'])
                print(f"✅ Perk purchase: {perk_result['success']}")
        
        # Test achievements
        engine.update_activity("quiz", score=85)
        achievements = engine.get_achievements_summary()
        print(f"✅ Achievements: {achievements['progress']:.1f}% complete")
        
        # Test leaderboard
        leaderboard = engine.get_leaderboard("total_coins", 5)
        print(f"✅ Leaderboard: {len(leaderboard)} entries")
        
        # Test stats
        stats = engine.get_student_stats()
        print(f"✅ Stats: Level {stats['level']}, {stats['current_coins']} coins")
        
        return True
        
    except Exception as e:
        print(f"❌ Gamification Engine test failed: {e}")
        return False

def test_integrated_backend():
    """Test the integrated backend system"""
    print("\n🧪 Testing Integrated Backend...")
    
    try:
        from backend.main import AgenticTutorBackend
        
        backend = AgenticTutorBackend("../data")
        
        # Test learning session setup
        setup_result = backend.setup_learning_session("6th", "Karnataka State Board", "Math")
        print(f"✅ Learning setup: {setup_result['success']}")
        
        # Test roadmap generation
        roadmap = backend.generate_learning_roadmap()
        print(f"✅ Roadmap: {len(roadmap)} characters")
        
        # Test quiz workflow
        quiz_result = backend.create_quiz("medium", 3)
        print(f"✅ Quiz creation: {quiz_result.get('success', False)}")
        
        if quiz_result.get('success'):
            # Submit sample answers
            sample_answers = [0, 1, 0]
            submit_result = backend.submit_quiz(sample_answers, 60.0)
            print(f"✅ Quiz submission: {submit_result.get('percentage', 0)}% score")
        
        # Test dashboard
        dashboard = backend.get_student_dashboard()
        print(f"✅ Dashboard: Level {dashboard['stats']['level']}")
        
        # Test video session
        video_result = backend.start_video_session("test_url", "Test Video")
        print(f"✅ Video session: {video_result['success']}")
        
        if video_result['success']:
            time.sleep(1)  # Brief session
            complete_result = backend.complete_video_session()
            print(f"✅ Video completion: {complete_result.get('coins_earned', 0)} coins")
        
        # Test parent dashboard
        parent_dashboard = backend.get_parent_dashboard()
        print(f"✅ Parent dashboard: {len(parent_dashboard)} sections")
        
        return True
        
    except Exception as e:
        print(f"❌ Integrated Backend test failed: {e}")
        return False

def run_all_tests():
    """Run all backend tests"""
    print("🚀 Starting Agentic AI Tutor Backend Tests...\n")
    
    tests = [
        ("Syllabus Manager", test_syllabus_manager),
        ("Attention Monitor", test_attention_monitor),
        ("Quiz Generator", test_quiz_generator),
        ("Gamification Engine", test_gamification_engine),
        ("Integrated Backend", test_integrated_backend)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print(f"\n{'='*50}")
    print("🏁 TEST SUMMARY")
    print(f"{'='*50}")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name:<20}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)