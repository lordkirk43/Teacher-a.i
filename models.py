from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class StudyMode(str, Enum):
    QUIZ = "quiz"
    PRACTICE = "practice"
    EXPLANATION = "explanation"
    REVIEW = "review"
    CONVERSATION = "conversation"

class Subject(str, Enum):
    MATH = "math"
    SCIENCE = "science"
    READING = "reading"
    WRITING = "writing"
    HISTORY = "history"
    GEOGRAPHY = "geography"

class Question(BaseModel):
    id: str
    subject: Subject
    content: str
    correct_answer: str
    options: Optional[List[str]] = None
    difficulty: DifficultyLevel
    explanation: str
    hints: List[str] = []

class StudentResponse(BaseModel):
    question_id: str
    answer: str
    is_correct: bool
    time_taken: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class StudySession(BaseModel):
    session_id: str
    student_name: str
    subject: Subject
    mode: StudyMode
    difficulty: DifficultyLevel
    questions: List[Question] = []
    responses: List[StudentResponse] = []
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    score: Optional[float] = None

class StudentProfile(BaseModel):
    name: str
    grade_level: int
    preferred_subjects: List[Subject]
    strengths: List[str] = []
    areas_for_improvement: List[str] = []
    learning_style: Optional[str] = None
    progress: Dict[str, Any] = {}

class TeachingContext(BaseModel):
    student: StudentProfile
    current_session: Optional[StudySession] = None
    conversation_history: List[Dict[str, str]] = []
    last_topic: Optional[str] = None
    current_difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE