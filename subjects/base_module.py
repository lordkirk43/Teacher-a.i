from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from models import Question, Subject, DifficultyLevel

class BaseSubjectModule(ABC):
    """Base class for all subject-specific teaching modules"""
    
    def __init__(self, subject: Subject):
        self.subject = subject
        self.topics = self.get_grade_topics()
    
    @abstractmethod
    def get_grade_topics(self) -> Dict[int, List[str]]:
        """Return topics organized by grade level"""
        pass
    
    @abstractmethod
    def generate_practice_problems(self, grade_level: int, topic: str, difficulty: DifficultyLevel, count: int = 5) -> List[Question]:
        """Generate practice problems for a specific topic"""
        pass
    
    @abstractmethod
    def get_learning_objectives(self, grade_level: int) -> List[str]:
        """Get learning objectives for a grade level"""
        pass
    
    def get_topics_for_grade(self, grade_level: int) -> List[str]:
        """Get topics appropriate for a specific grade level"""
        return self.topics.get(grade_level, [])
    
    def get_difficulty_progression(self, topic: str) -> List[str]:
        """Get the natural difficulty progression for a topic"""
        return [
            f"Basic {topic} concepts",
            f"Intermediate {topic} problems", 
            f"Advanced {topic} applications"
        ]
    
    def create_explanation(self, topic: str, grade_level: int) -> str:
        """Create an age-appropriate explanation of a topic"""
        return f"Let me explain {topic} in a way that's perfect for grade {grade_level}!"
    
    def suggest_next_topics(self, current_topic: str, grade_level: int) -> List[str]:
        """Suggest related topics to study next"""
        topics = self.get_topics_for_grade(grade_level)
        try:
            current_index = topics.index(current_topic)
            # Return next 2-3 topics
            return topics[current_index + 1:current_index + 4]
        except ValueError:
            # If current topic not found, return first few topics
            return topics[:3]