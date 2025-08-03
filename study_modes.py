from typing import List, Dict, Any, Optional
import random
from datetime import datetime
import logging

from models import (
    StudyMode, Subject, DifficultyLevel, Question, StudentResponse,
    StudySession, TeachingContext
)
from ai_teacher import AITeacher
from subjects import MathModule, ScienceModule, ReadingModule, WritingModule

logger = logging.getLogger(__name__)

class StudyModeManager:
    """Manages different study modes and their interactions"""
    
    def __init__(self, ai_teacher: AITeacher):
        self.ai_teacher = ai_teacher
        self.subject_modules = {
            Subject.MATH: MathModule(),
            Subject.SCIENCE: ScienceModule(),
            Subject.READING: ReadingModule(),
            Subject.WRITING: WritingModule()
        }
    
    def start_mode(self, mode: StudyMode, subject: Subject, difficulty: DifficultyLevel) -> Dict[str, Any]:
        """Start a specific study mode"""
        if mode == StudyMode.QUIZ:
            return self._start_quiz_mode(subject, difficulty)
        elif mode == StudyMode.PRACTICE:
            return self._start_practice_mode(subject, difficulty)
        elif mode == StudyMode.EXPLANATION:
            return self._start_explanation_mode(subject, difficulty)
        elif mode == StudyMode.REVIEW:
            return self._start_review_mode(subject, difficulty)
        elif mode == StudyMode.CONVERSATION:
            return self._start_conversation_mode()
        else:
            return {"error": "Unknown study mode"}
    
    def _start_quiz_mode(self, subject: Subject, difficulty: DifficultyLevel) -> Dict[str, Any]:
        """Start quiz mode with multiple choice questions"""
        session = self.ai_teacher.start_study_session(subject, StudyMode.QUIZ, difficulty)
        
        # Generate 5-10 questions for the quiz
        num_questions = random.randint(5, 10)
        questions = []
        
        if subject in self.subject_modules:
            # Get topics for the student's grade level
            module = self.subject_modules[subject]
            grade_level = self.ai_teacher.context.student.grade_level
            topics = module.get_topics_for_grade(grade_level)
            
            for _ in range(num_questions):
                topic = random.choice(topics) if topics else "general"
                try:
                    # Try to use subject module first
                    practice_problems = module.generate_practice_problems(
                        grade_level, topic, difficulty, 1
                    )
                    if practice_problems:
                        questions.extend(practice_problems)
                    else:
                        # Fallback to AI generation
                        question = self.ai_teacher.generate_question(subject, difficulty, topic)
                        questions.append(question)
                except Exception as e:
                    logger.warning(f"Error generating question from module: {e}")
                    # Fallback to AI generation
                    question = self.ai_teacher.generate_question(subject, difficulty, topic)
                    questions.append(question)
        else:
            # Use AI teacher for subjects without specific modules
            for _ in range(num_questions):
                question = self.ai_teacher.generate_question(subject, difficulty)
                questions.append(question)
        
        session.questions = questions
        
        return {
            "mode": "quiz",
            "session_id": session.session_id,
            "total_questions": len(questions),
            "current_question": 0,
            "question": questions[0].dict() if questions else None,
            "instructions": f"Welcome to your {subject.value} quiz! Answer each question to the best of your ability. You'll get feedback after each answer."
        }
    
    def _start_practice_mode(self, subject: Subject, difficulty: DifficultyLevel) -> Dict[str, Any]:
        """Start practice mode with immediate feedback"""
        session = self.ai_teacher.start_study_session(subject, StudyMode.PRACTICE, difficulty)
        
        # Generate one question to start
        question = None
        if subject in self.subject_modules:
            module = self.subject_modules[subject]
            grade_level = self.ai_teacher.context.student.grade_level
            topics = module.get_topics_for_grade(grade_level)
            
            if topics:
                topic = random.choice(topics)
                try:
                    practice_problems = module.generate_practice_problems(
                        grade_level, topic, difficulty, 1
                    )
                    if practice_problems:
                        question = practice_problems[0]
                except Exception as e:
                    logger.warning(f"Error generating practice problem: {e}")
        
        if not question:
            question = self.ai_teacher.generate_question(subject, difficulty)
        
        session.questions = [question]
        
        return {
            "mode": "practice",
            "session_id": session.session_id,
            "question": question.dict(),
            "instructions": f"Practice time! I'll give you {subject.value} problems one at a time. Take your time and I'll help you learn from each answer."
        }
    
    def _start_explanation_mode(self, subject: Subject, difficulty: DifficultyLevel) -> Dict[str, Any]:
        """Start explanation mode for learning concepts"""
        session = self.ai_teacher.start_study_session(subject, StudyMode.EXPLANATION, difficulty)
        
        # Get a topic to explain
        topic = "general concepts"
        if subject in self.subject_modules:
            module = self.subject_modules[subject]
            grade_level = self.ai_teacher.context.student.grade_level
            topics = module.get_topics_for_grade(grade_level)
            if topics:
                topic = random.choice(topics)
        
        # Generate an explanation
        student_name = self.ai_teacher.context.student.name
        grade_level = self.ai_teacher.context.student.grade_level
        
        explanation_prompt = f"""
        You are teaching {student_name}, a grade {grade_level} student, about {topic} in {subject.value}.
        
        Provide a clear, engaging explanation that:
        1. Is age-appropriate for grade {grade_level}
        2. Uses examples they can relate to
        3. Breaks down complex ideas into simple parts
        4. Is encouraging and positive
        5. Invites questions
        
        Make it interactive by asking them what they'd like to know more about.
        """
        
        try:
            response = self.ai_teacher.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": explanation_prompt}],
                temperature=0.7,
                max_tokens=500
            )
            explanation = response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            explanation = f"Let's learn about {topic} in {subject.value}! This is an important topic that will help you understand how things work. What would you like to know about {topic}?"
        
        return {
            "mode": "explanation",
            "session_id": session.session_id,
            "topic": topic,
            "explanation": explanation,
            "instructions": "I'm here to explain concepts and answer your questions. Feel free to ask me anything about this topic!"
        }
    
    def _start_review_mode(self, subject: Subject, difficulty: DifficultyLevel) -> Dict[str, Any]:
        """Start review mode to go over previous topics"""
        session = self.ai_teacher.start_study_session(subject, StudyMode.REVIEW, difficulty)
        
        # Get topics for review
        review_topics = []
        if subject in self.subject_modules:
            module = self.subject_modules[subject]
            grade_level = self.ai_teacher.context.student.grade_level
            topics = module.get_topics_for_grade(grade_level)
            review_topics = topics[:3] if topics else ["basic concepts"]
        
        student_name = self.ai_teacher.context.student.name
        
        review_summary = f"""
        Hi {student_name}! Let's review some important {subject.value} topics:
        
        """
        
        for i, topic in enumerate(review_topics, 1):
            review_summary += f"{i}. {topic}\n"
        
        review_summary += f"""
        
        Which topic would you like to review first? I can:
        - Explain the concept again
        - Give you practice problems
        - Answer any questions you have
        - Show you examples
        
        Just let me know what would help you most!
        """
        
        return {
            "mode": "review",
            "session_id": session.session_id,
            "topics": review_topics,
            "summary": review_summary,
            "instructions": "Review mode helps you go over topics you've learned before. Choose what you'd like to focus on!"
        }
    
    def _start_conversation_mode(self) -> Dict[str, Any]:
        """Start free conversation mode"""
        student_name = self.ai_teacher.context.student.name if self.ai_teacher.context else "Student"
        
        welcome_message = f"""
        Hi {student_name}! I'm here to chat and help you learn. You can:
        
        - Ask me questions about any subject
        - Tell me what you're working on in school
        - Share what you're curious about
        - Ask for help with homework
        - Just have a friendly conversation!
        
        What's on your mind today?
        """
        
        return {
            "mode": "conversation",
            "message": welcome_message,
            "instructions": "Feel free to ask me anything or just chat! I'm here to help you learn and explore your curiosity."
        }
    
    def handle_answer(self, session_id: str, answer: str, question_id: Optional[str] = None) -> Dict[str, Any]:
        """Handle a student's answer in any mode"""
        if not self.ai_teacher.context or not self.ai_teacher.context.current_session:
            return {"error": "No active session"}
        
        session = self.ai_teacher.context.current_session
        
        if session.session_id != session_id:
            return {"error": "Session ID mismatch"}
        
        if session.mode == StudyMode.CONVERSATION:
            return self._handle_conversation(answer)
        elif session.mode in [StudyMode.QUIZ, StudyMode.PRACTICE]:
            return self._handle_question_answer(answer, question_id)
        elif session.mode == StudyMode.EXPLANATION:
            return self._handle_explanation_question(answer)
        elif session.mode == StudyMode.REVIEW:
            return self._handle_review_request(answer)
        else:
            return {"error": "Unknown session mode"}
    
    def _handle_conversation(self, message: str) -> Dict[str, Any]:
        """Handle conversation mode messages"""
        response = self.ai_teacher.have_conversation(message)
        
        return {
            "response": response,
            "suggestions": [
                "Can you help me with math?",
                "Tell me about science",
                "What should I read?",
                "How can I improve my writing?"
            ]
        }
    
    def _handle_question_answer(self, answer: str, question_id: Optional[str]) -> Dict[str, Any]:
        """Handle answers to quiz/practice questions"""
        session = self.ai_teacher.context.current_session
        
        # Find the current question
        current_question = None
        question_index = len(session.responses)
        
        if question_index < len(session.questions):
            current_question = session.questions[question_index]
        
        if not current_question:
            return {"error": "No current question found"}
        
        # Evaluate the answer
        response = self.ai_teacher.evaluate_answer(current_question, answer)
        feedback = self.ai_teacher.provide_feedback(current_question, response)
        
        # Check if there are more questions
        next_question = None
        is_complete = False
        
        if session.mode == StudyMode.QUIZ:
            # In quiz mode, move to next question or complete
            if question_index + 1 < len(session.questions):
                next_question = session.questions[question_index + 1]
            else:
                is_complete = True
        elif session.mode == StudyMode.PRACTICE:
            # In practice mode, generate a new question
            try:
                subject = session.subject
                difficulty = session.difficulty
                
                if subject in self.subject_modules:
                    module = self.subject_modules[subject]
                    grade_level = self.ai_teacher.context.student.grade_level
                    topics = module.get_topics_for_grade(grade_level)
                    
                    if topics:
                        topic = random.choice(topics)
                        practice_problems = module.generate_practice_problems(
                            grade_level, topic, difficulty, 1
                        )
                        if practice_problems:
                            next_question = practice_problems[0]
                
                if not next_question:
                    next_question = self.ai_teacher.generate_question(subject, difficulty)
                
                session.questions.append(next_question)
                
            except Exception as e:
                logger.error(f"Error generating next question: {e}")
                next_question = self.ai_teacher.generate_question(session.subject, session.difficulty)
                session.questions.append(next_question)
        
        result = {
            "correct": response.is_correct,
            "feedback": feedback,
            "explanation": current_question.explanation,
            "is_complete": is_complete
        }
        
        if next_question:
            result["next_question"] = next_question.dict()
        
        if is_complete:
            # Calculate final score for quiz
            correct_answers = sum(1 for r in session.responses if r.is_correct)
            total_questions = len(session.questions)
            score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
            session.score = score
            session.end_time = datetime.now()
            
            result["final_score"] = score
            result["total_correct"] = correct_answers
            result["total_questions"] = total_questions
            result["completion_message"] = self._generate_completion_message(score)
        
        return result
    
    def _handle_explanation_question(self, question: str) -> Dict[str, Any]:
        """Handle questions in explanation mode"""
        session = self.ai_teacher.context.current_session
        topic = getattr(session, 'topic', session.subject.value)
        
        # Generate a detailed explanation
        student_name = self.ai_teacher.context.student.name
        grade_level = self.ai_teacher.context.student.grade_level
        
        explanation_prompt = f"""
        {student_name}, a grade {grade_level} student, is learning about {topic} and asked: "{question}"
        
        Provide a helpful, age-appropriate answer that:
        1. Directly addresses their question
        2. Uses examples they can understand
        3. Is encouraging and supportive
        4. Invites follow-up questions
        5. Connects to what they're learning
        """
        
        try:
            response = self.ai_teacher.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": explanation_prompt}],
                temperature=0.7,
                max_tokens=400
            )
            explanation = response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            explanation = f"That's a great question about {topic}! Let me think about the best way to explain this to you..."
        
        return {
            "explanation": explanation,
            "suggestions": [
                "Can you give me an example?",
                "Why is this important?",
                "How does this connect to other things I know?",
                "Can we try a practice problem?"
            ]
        }
    
    def _handle_review_request(self, request: str) -> Dict[str, Any]:
        """Handle requests in review mode"""
        session = self.ai_teacher.context.current_session
        
        # Parse the request and provide appropriate review content
        response = self.ai_teacher.have_conversation(f"I'd like to review: {request}")
        
        return {
            "response": response,
            "options": [
                "Practice problems",
                "Explanation",
                "Examples",
                "Different topic"
            ]
        }
    
    def _generate_completion_message(self, score: float) -> str:
        """Generate an encouraging completion message"""
        student_name = self.ai_teacher.context.student.name
        
        if score >= 90:
            return f"Excellent work, {student_name}! You scored {score:.0f}%! You really understand this material! 🌟"
        elif score >= 80:
            return f"Great job, {student_name}! You scored {score:.0f}%! You're doing really well! 👏"
        elif score >= 70:
            return f"Good work, {student_name}! You scored {score:.0f}%! Keep practicing and you'll get even better! 💪"
        elif score >= 60:
            return f"Nice effort, {student_name}! You scored {score:.0f}%! Let's review some concepts and try again! 📚"
        else:
            return f"You're learning, {student_name}! You scored {score:.0f}%. Don't worry - everyone learns at their own pace. Let's practice more! 🌱"
    
    def get_study_suggestions(self) -> List[str]:
        """Get personalized study suggestions"""
        if not self.ai_teacher.context:
            return ["Set up your profile to get personalized suggestions!"]
        
        suggestions = self.ai_teacher.get_study_suggestions()
        
        # Add mode-specific suggestions
        mode_suggestions = [
            "Take a quiz to test your knowledge",
            "Practice problems with immediate feedback",
            "Ask for explanations of difficult concepts",
            "Review topics you've learned before",
            "Have a conversation about what interests you"
        ]
        
        return suggestions + mode_suggestions