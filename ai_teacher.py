import openai
import json
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from config import Config
from models import (
    TeachingContext, StudentProfile, StudySession, Question, 
    StudentResponse, Subject, StudyMode, DifficultyLevel
)

logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class AITeacher:
    def __init__(self):
        Config.validate()
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        self.context: Optional[TeachingContext] = None
        
    def initialize_student(self, name: str, grade_level: int, preferred_subjects: List[str]) -> StudentProfile:
        """Initialize a new student profile"""
        subjects = [Subject(subj.strip().lower()) for subj in preferred_subjects if subj.strip().lower() in Subject.__members__.values()]
        
        profile = StudentProfile(
            name=name,
            grade_level=grade_level,
            preferred_subjects=subjects,
            progress={}
        )
        
        self.context = TeachingContext(student=profile)
        logger.info(f"Initialized student profile for {name}, Grade {grade_level}")
        return profile
    
    def start_study_session(self, subject: Subject, mode: StudyMode, difficulty: DifficultyLevel) -> StudySession:
        """Start a new study session"""
        if not self.context:
            raise ValueError("Student profile not initialized")
            
        session = StudySession(
            session_id=str(uuid.uuid4()),
            student_name=self.context.student.name,
            subject=subject,
            mode=mode,
            difficulty=difficulty
        )
        
        self.context.current_session = session
        logger.info(f"Started {mode} session for {subject} at {difficulty} level")
        return session
    
    def generate_question(self, subject: Subject, difficulty: DifficultyLevel, topic: Optional[str] = None) -> Question:
        """Generate a question using AI"""
        grade_level = self.context.student.grade_level if self.context else 5
        
        prompt = f"""
        Generate an educational question for a grade {grade_level} student.
        Subject: {subject.value}
        Difficulty: {difficulty.value}
        Topic: {topic or "general"}
        
        Create a question that is:
        1. Age-appropriate for grade {grade_level}
        2. Educational and engaging
        3. Clear and well-structured
        
        Respond with a JSON object containing:
        - "question": the question text
        - "correct_answer": the correct answer
        - "options": array of 4 multiple choice options (if applicable, null otherwise)
        - "explanation": detailed explanation of the answer
        - "hints": array of 2-3 helpful hints
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            question_data = json.loads(content)
            
            question = Question(
                id=str(uuid.uuid4()),
                subject=subject,
                content=question_data["question"],
                correct_answer=question_data["correct_answer"],
                options=question_data.get("options"),
                difficulty=difficulty,
                explanation=question_data["explanation"],
                hints=question_data.get("hints", [])
            )
            
            return question
            
        except Exception as e:
            logger.error(f"Error generating question: {e}")
            # Fallback question
            return Question(
                id=str(uuid.uuid4()),
                subject=subject,
                content=f"What is 2 + 2?",
                correct_answer="4",
                options=["2", "3", "4", "5"],
                difficulty=difficulty,
                explanation="2 + 2 equals 4 because when you add 2 and 2 together, you get 4.",
                hints=["Think about counting on your fingers", "2 plus 2 is a basic addition problem"]
            )
    
    def evaluate_answer(self, question: Question, student_answer: str) -> StudentResponse:
        """Evaluate a student's answer"""
        is_correct = student_answer.strip().lower() == question.correct_answer.strip().lower()
        
        response = StudentResponse(
            question_id=question.id,
            answer=student_answer,
            is_correct=is_correct
        )
        
        if self.context and self.context.current_session:
            self.context.current_session.responses.append(response)
        
        return response
    
    def provide_feedback(self, question: Question, response: StudentResponse) -> str:
        """Provide personalized feedback on an answer"""
        student_name = self.context.student.name if self.context else "Student"
        
        if response.is_correct:
            feedback_prompt = f"""
            Generate encouraging feedback for {student_name} who answered correctly.
            Question: {question.content}
            Student's answer: {response.answer}
            Correct answer: {question.correct_answer}
            
            Make the feedback:
            1. Positive and encouraging
            2. Brief but meaningful
            3. Age-appropriate for a grade {self.context.student.grade_level if self.context else 5} student
            """
        else:
            feedback_prompt = f"""
            Generate constructive feedback for {student_name} who answered incorrectly.
            Question: {question.content}
            Student's answer: {response.answer}
            Correct answer: {question.correct_answer}
            Explanation: {question.explanation}
            
            Make the feedback:
            1. Supportive and encouraging
            2. Include a hint or learning point
            3. Age-appropriate for a grade {self.context.student.grade_level if self.context else 5} student
            4. Help them understand why their answer was incorrect
            """
        
        try:
            response_obj = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": feedback_prompt}],
                temperature=0.7,
                max_tokens=200
            )
            
            return response_obj.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating feedback: {e}")
            if response.is_correct:
                return f"Great job, {student_name}! That's correct! 🎉"
            else:
                return f"Not quite right, {student_name}. The correct answer is {question.correct_answer}. {question.explanation}"
    
    def have_conversation(self, message: str) -> str:
        """Have a natural conversation with the student"""
        if not self.context:
            return "Hi there! I'm your AI teacher. Let me know your name and grade level to get started!"
        
        student_name = self.context.student.name
        grade_level = self.context.student.grade_level
        
        # Add to conversation history
        self.context.conversation_history.append({"role": "student", "content": message})
        
        # Build context for AI
        conversation_context = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in self.context.conversation_history[-10:]  # Last 10 messages
        ])
        
        prompt = f"""
        You are an AI teacher having a conversation with {student_name}, a grade {grade_level} student.
        
        Your personality:
        - Friendly, patient, and encouraging
        - Educational but fun
        - Age-appropriate for grade {grade_level}
        - Supportive and understanding
        
        Recent conversation:
        {conversation_context}
        
        Student just said: {message}
        
        Respond as their teacher would - be helpful, educational when appropriate, and maintain a positive learning environment.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=300
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Add AI response to history
            self.context.conversation_history.append({"role": "teacher", "content": ai_response})
            
            return ai_response
            
        except Exception as e:
            logger.error(f"Error in conversation: {e}")
            return f"I'm having trouble right now, {student_name}. Could you try asking me again?"
    
    def get_study_suggestions(self) -> List[str]:
        """Get personalized study suggestions"""
        if not self.context:
            return ["Please set up your student profile first!"]
        
        student = self.context.student
        suggestions = []
        
        # Based on preferred subjects
        for subject in student.preferred_subjects:
            suggestions.append(f"Practice {subject.value} problems")
            suggestions.append(f"Take a {subject.value} quiz")
        
        # Based on areas for improvement
        for area in student.areas_for_improvement:
            suggestions.append(f"Review {area} concepts")
        
        # General suggestions
        suggestions.extend([
            "Have a conversation about what you learned today",
            "Try explaining a concept in your own words",
            "Practice with increasing difficulty levels"
        ])
        
        return suggestions[:5]  # Return top 5 suggestions