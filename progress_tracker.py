import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import logging

from models import Subject, DifficultyLevel, StudySession, StudentResponse, StudentProfile

logger = logging.getLogger(__name__)

@dataclass
class TopicProgress:
    """Track progress for a specific topic"""
    topic: str
    subject: Subject
    attempts: int = 0
    correct_answers: int = 0
    last_practiced: Optional[datetime] = None
    current_difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    mastery_level: float = 0.0  # 0.0 to 1.0
    needs_review: bool = False

@dataclass
class SessionSummary:
    """Summary of a study session"""
    session_id: str
    subject: Subject
    mode: str
    score: float
    questions_answered: int
    time_spent: float  # in minutes
    topics_covered: List[str]
    difficulty_level: DifficultyLevel
    date: datetime

class ProgressTracker:
    """Tracks student progress and adapts difficulty"""
    
    def __init__(self, student_name: str):
        self.student_name = student_name
        self.progress_file = f"progress_{student_name.lower().replace(' ', '_')}.json"
        self.topic_progress: Dict[str, TopicProgress] = {}
        self.session_history: List[SessionSummary] = []
        self.achievements: List[str] = []
        self.load_progress()
    
    def load_progress(self):
        """Load progress from file"""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r') as f:
                    data = json.load(f)
                
                # Load topic progress
                for topic_key, topic_data in data.get('topics', {}).items():
                    topic_progress = TopicProgress(
                        topic=topic_data['topic'],
                        subject=Subject(topic_data['subject']),
                        attempts=topic_data['attempts'],
                        correct_answers=topic_data['correct_answers'],
                        last_practiced=datetime.fromisoformat(topic_data['last_practiced']) if topic_data.get('last_practiced') else None,
                        current_difficulty=DifficultyLevel(topic_data['current_difficulty']),
                        mastery_level=topic_data['mastery_level'],
                        needs_review=topic_data.get('needs_review', False)
                    )
                    self.topic_progress[topic_key] = topic_progress
                
                # Load session history
                for session_data in data.get('sessions', []):
                    session = SessionSummary(
                        session_id=session_data['session_id'],
                        subject=Subject(session_data['subject']),
                        mode=session_data['mode'],
                        score=session_data['score'],
                        questions_answered=session_data['questions_answered'],
                        time_spent=session_data['time_spent'],
                        topics_covered=session_data['topics_covered'],
                        difficulty_level=DifficultyLevel(session_data['difficulty_level']),
                        date=datetime.fromisoformat(session_data['date'])
                    )
                    self.session_history.append(session)
                
                self.achievements = data.get('achievements', [])
                
                logger.info(f"Loaded progress for {self.student_name}")
                
            except Exception as e:
                logger.error(f"Error loading progress: {e}")
                self._initialize_default_progress()
        else:
            self._initialize_default_progress()
    
    def _initialize_default_progress(self):
        """Initialize default progress for new student"""
        logger.info(f"Initializing new progress for {self.student_name}")
        self.topic_progress = {}
        self.session_history = []
        self.achievements = []
    
    def save_progress(self):
        """Save progress to file"""
        try:
            data = {
                'student_name': self.student_name,
                'topics': {},
                'sessions': [],
                'achievements': self.achievements,
                'last_updated': datetime.now().isoformat()
            }
            
            # Save topic progress
            for topic_key, topic_progress in self.topic_progress.items():
                data['topics'][topic_key] = {
                    'topic': topic_progress.topic,
                    'subject': topic_progress.subject.value,
                    'attempts': topic_progress.attempts,
                    'correct_answers': topic_progress.correct_answers,
                    'last_practiced': topic_progress.last_practiced.isoformat() if topic_progress.last_practiced else None,
                    'current_difficulty': topic_progress.current_difficulty.value,
                    'mastery_level': topic_progress.mastery_level,
                    'needs_review': topic_progress.needs_review
                }
            
            # Save session history (keep last 50 sessions)
            recent_sessions = self.session_history[-50:]
            for session in recent_sessions:
                data['sessions'].append({
                    'session_id': session.session_id,
                    'subject': session.subject.value,
                    'mode': session.mode,
                    'score': session.score,
                    'questions_answered': session.questions_answered,
                    'time_spent': session.time_spent,
                    'topics_covered': session.topics_covered,
                    'difficulty_level': session.difficulty_level.value,
                    'date': session.date.isoformat()
                })
            
            with open(self.progress_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Saved progress for {self.student_name}")
            
        except Exception as e:
            logger.error(f"Error saving progress: {e}")
    
    def record_session(self, session: StudySession):
        """Record a completed study session"""
        if not session.end_time:
            session.end_time = datetime.now()
        
        # Calculate time spent
        time_spent = (session.end_time - session.start_time).total_seconds() / 60  # minutes
        
        # Get topics covered
        topics_covered = list(set([q.content.split()[0] for q in session.questions if session.questions]))  # Simplified topic extraction
        
        # Create session summary
        session_summary = SessionSummary(
            session_id=session.session_id,
            subject=session.subject,
            mode=session.mode.value,
            score=session.score or 0.0,
            questions_answered=len(session.responses),
            time_spent=time_spent,
            topics_covered=topics_covered,
            difficulty_level=session.difficulty,
            date=session.start_time
        )
        
        self.session_history.append(session_summary)
        
        # Update topic progress
        self._update_topic_progress(session)
        
        # Check for achievements
        self._check_achievements(session_summary)
        
        # Save progress
        self.save_progress()
        
        logger.info(f"Recorded session {session.session_id} for {self.student_name}")
    
    def _update_topic_progress(self, session: StudySession):
        """Update progress for topics covered in the session"""
        if not session.questions or not session.responses:
            return
        
        # Group responses by topic (simplified)
        topic_responses = {}
        for i, question in enumerate(session.questions):
            if i < len(session.responses):
                # Extract topic from question (this is a simplified approach)
                topic = self._extract_topic_from_question(question.content)
                topic_key = f"{session.subject.value}_{topic}"
                
                if topic_key not in topic_responses:
                    topic_responses[topic_key] = {'correct': 0, 'total': 0, 'topic': topic}
                
                topic_responses[topic_key]['total'] += 1
                if session.responses[i].is_correct:
                    topic_responses[topic_key]['correct'] += 1
        
        # Update topic progress
        for topic_key, data in topic_responses.items():
            if topic_key not in self.topic_progress:
                self.topic_progress[topic_key] = TopicProgress(
                    topic=data['topic'],
                    subject=session.subject,
                    current_difficulty=session.difficulty
                )
            
            progress = self.topic_progress[topic_key]
            progress.attempts += data['total']
            progress.correct_answers += data['correct']
            progress.last_practiced = datetime.now()
            
            # Calculate mastery level (percentage correct with recency weighting)
            accuracy = progress.correct_answers / progress.attempts if progress.attempts > 0 else 0
            progress.mastery_level = min(accuracy * 1.2, 1.0)  # Slight boost for recent practice
            
            # Determine if needs review (low accuracy or not practiced recently)
            if accuracy < 0.6 or (progress.last_practiced and 
                                  (datetime.now() - progress.last_practiced).days > 7):
                progress.needs_review = True
            else:
                progress.needs_review = False
            
            # Adjust difficulty based on performance
            self._adjust_difficulty(progress, accuracy)
    
    def _extract_topic_from_question(self, question_content: str) -> str:
        """Extract topic from question content (simplified approach)"""
        # This is a basic implementation - in a real system, you'd want more sophisticated topic extraction
        content_lower = question_content.lower()
        
        # Math topics
        if any(word in content_lower for word in ['add', 'addition', '+', 'plus']):
            return 'addition'
        elif any(word in content_lower for word in ['subtract', 'subtraction', '-', 'minus']):
            return 'subtraction'
        elif any(word in content_lower for word in ['multiply', 'multiplication', '×', 'times']):
            return 'multiplication'
        elif any(word in content_lower for word in ['divide', 'division', '÷']):
            return 'division'
        elif any(word in content_lower for word in ['fraction', 'fractions']):
            return 'fractions'
        
        # Science topics
        elif any(word in content_lower for word in ['animal', 'animals']):
            return 'animals'
        elif any(word in content_lower for word in ['plant', 'plants']):
            return 'plants'
        elif any(word in content_lower for word in ['weather', 'rain', 'sun']):
            return 'weather'
        elif any(word in content_lower for word in ['space', 'planet', 'solar']):
            return 'space'
        
        # Reading topics
        elif any(word in content_lower for word in ['read', 'story', 'character']):
            return 'reading_comprehension'
        elif any(word in content_lower for word in ['word', 'vocabulary']):
            return 'vocabulary'
        
        # Writing topics
        elif any(word in content_lower for word in ['sentence', 'grammar']):
            return 'grammar'
        elif any(word in content_lower for word in ['spell', 'spelling']):
            return 'spelling'
        
        return 'general'
    
    def _adjust_difficulty(self, progress: TopicProgress, recent_accuracy: float):
        """Adjust difficulty based on performance"""
        if recent_accuracy >= 0.8 and progress.attempts >= 3:
            # Student is doing well, increase difficulty
            if progress.current_difficulty == DifficultyLevel.BEGINNER:
                progress.current_difficulty = DifficultyLevel.INTERMEDIATE
            elif progress.current_difficulty == DifficultyLevel.INTERMEDIATE:
                progress.current_difficulty = DifficultyLevel.ADVANCED
        elif recent_accuracy < 0.5 and progress.attempts >= 3:
            # Student is struggling, decrease difficulty
            if progress.current_difficulty == DifficultyLevel.ADVANCED:
                progress.current_difficulty = DifficultyLevel.INTERMEDIATE
            elif progress.current_difficulty == DifficultyLevel.INTERMEDIATE:
                progress.current_difficulty = DifficultyLevel.BEGINNER
    
    def _check_achievements(self, session: SessionSummary):
        """Check for new achievements"""
        new_achievements = []
        
        # First session achievement
        if len(self.session_history) == 1:
            new_achievements.append("🌟 Welcome! You completed your first session!")
        
        # Perfect score achievement
        if session.score == 100:
            new_achievements.append("🎯 Perfect Score! You got 100% on a quiz!")
        
        # Streak achievements
        recent_sessions = self.session_history[-5:]
        if len(recent_sessions) >= 3 and all(s.score >= 80 for s in recent_sessions):
            achievement = "🔥 On Fire! Three great sessions in a row!"
            if achievement not in self.achievements:
                new_achievements.append(achievement)
        
        # Subject mastery
        subject_sessions = [s for s in self.session_history if s.subject == session.subject]
        if len(subject_sessions) >= 5:
            avg_score = sum(s.score for s in subject_sessions[-5:]) / 5
            if avg_score >= 85:
                achievement = f"🏆 {session.subject.value.title()} Expert! High performance across multiple sessions!"
                if achievement not in self.achievements:
                    new_achievements.append(achievement)
        
        # Consistency achievement
        if len(self.session_history) >= 7:
            recent_dates = [s.date.date() for s in self.session_history[-7:]]
            unique_dates = set(recent_dates)
            if len(unique_dates) >= 5:  # Practiced on at least 5 different days
                achievement = "📅 Consistent Learner! You've been practicing regularly!"
                if achievement not in self.achievements:
                    new_achievements.append(achievement)
        
        # Add new achievements
        self.achievements.extend(new_achievements)
        
        if new_achievements:
            logger.info(f"New achievements for {self.student_name}: {new_achievements}")
    
    def get_recommended_difficulty(self, subject: Subject, topic: str = None) -> DifficultyLevel:
        """Get recommended difficulty for a subject/topic"""
        if topic:
            topic_key = f"{subject.value}_{topic}"
            if topic_key in self.topic_progress:
                return self.topic_progress[topic_key].current_difficulty
        
        # Look at recent performance in this subject
        subject_sessions = [s for s in self.session_history[-10:] if s.subject == subject]
        if subject_sessions:
            avg_score = sum(s.score for s in subject_sessions) / len(subject_sessions)
            if avg_score >= 85:
                return DifficultyLevel.ADVANCED
            elif avg_score >= 70:
                return DifficultyLevel.INTERMEDIATE
            else:
                return DifficultyLevel.BEGINNER
        
        return DifficultyLevel.INTERMEDIATE  # Default
    
    def get_topics_needing_review(self, subject: Subject = None) -> List[TopicProgress]:
        """Get topics that need review"""
        topics = []
        for topic_progress in self.topic_progress.values():
            if subject and topic_progress.subject != subject:
                continue
            
            if topic_progress.needs_review or topic_progress.mastery_level < 0.6:
                topics.append(topic_progress)
        
        # Sort by most urgent (lowest mastery level and oldest practice)
        topics.sort(key=lambda t: (t.mastery_level, t.last_practiced or datetime.min))
        return topics
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """Get a comprehensive progress summary"""
        total_sessions = len(self.session_history)
        if total_sessions == 0:
            return {
                "total_sessions": 0,
                "message": "No sessions completed yet. Let's start learning!"
            }
        
        # Calculate overall statistics
        avg_score = sum(s.score for s in self.session_history) / total_sessions
        total_time = sum(s.time_spent for s in self.session_history)
        total_questions = sum(s.questions_answered for s in self.session_history)
        
        # Subject breakdown
        subject_stats = {}
        for subject in Subject:
            subject_sessions = [s for s in self.session_history if s.subject == subject]
            if subject_sessions:
                subject_stats[subject.value] = {
                    "sessions": len(subject_sessions),
                    "avg_score": sum(s.score for s in subject_sessions) / len(subject_sessions),
                    "last_practiced": max(s.date for s in subject_sessions).strftime("%Y-%m-%d")
                }
        
        # Recent performance trend
        recent_sessions = self.session_history[-5:]
        trend = "stable"
        if len(recent_sessions) >= 3:
            early_avg = sum(s.score for s in recent_sessions[:2]) / 2
            late_avg = sum(s.score for s in recent_sessions[-2:]) / 2
            if late_avg > early_avg + 10:
                trend = "improving"
            elif late_avg < early_avg - 10:
                trend = "declining"
        
        # Topics mastered
        mastered_topics = [
            t for t in self.topic_progress.values() 
            if t.mastery_level >= 0.8 and t.attempts >= 3
        ]
        
        return {
            "total_sessions": total_sessions,
            "avg_score": round(avg_score, 1),
            "total_time_minutes": round(total_time, 1),
            "total_questions_answered": total_questions,
            "subject_stats": subject_stats,
            "trend": trend,
            "mastered_topics": len(mastered_topics),
            "topics_need_review": len(self.get_topics_needing_review()),
            "achievements": len(self.achievements),
            "recent_achievements": self.achievements[-3:] if len(self.achievements) >= 3 else self.achievements
        }
    
    def get_study_recommendations(self) -> List[str]:
        """Get personalized study recommendations"""
        recommendations = []
        
        # Check for topics needing review
        review_topics = self.get_topics_needing_review()
        if review_topics:
            top_review = review_topics[0]
            recommendations.append(f"📚 Review {top_review.topic} in {top_review.subject.value} - you haven't practiced this recently")
        
        # Check for subjects not practiced recently
        recent_subjects = set(s.subject for s in self.session_history[-5:])
        all_subjects = set(Subject)
        neglected_subjects = all_subjects - recent_subjects
        if neglected_subjects:
            subject = next(iter(neglected_subjects))
            recommendations.append(f"🎯 Try some {subject.value} practice - it's been a while!")
        
        # Suggest increasing difficulty for mastered topics
        mastered_topics = [
            t for t in self.topic_progress.values() 
            if t.mastery_level >= 0.8 and t.current_difficulty != DifficultyLevel.ADVANCED
        ]
        if mastered_topics:
            topic = mastered_topics[0]
            recommendations.append(f"🚀 Challenge yourself with harder {topic.topic} problems - you're doing great!")
        
        # Suggest consistency if irregular practice
        if len(self.session_history) >= 3:
            recent_dates = [s.date.date() for s in self.session_history[-7:]]
            days_since_last = (datetime.now().date() - max(recent_dates)).days
            if days_since_last >= 2:
                recommendations.append("⏰ Try to practice a little bit each day for better learning!")
        
        # Default recommendations if none specific
        if not recommendations:
            recommendations = [
                "🌟 Take a quiz to test your knowledge",
                "💡 Try explanation mode to learn new concepts",
                "🎮 Practice mode gives you immediate feedback",
                "💬 Chat with me about anything you're curious about!"
            ]
        
        return recommendations[:3]  # Return top 3 recommendations