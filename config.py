import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Student Configuration
    STUDENT_NAME = os.getenv("STUDENT_NAME", "Student")
    GRADE_LEVEL = int(os.getenv("GRADE_LEVEL", "5"))
    PREFERRED_SUBJECTS = os.getenv("PREFERRED_SUBJECTS", "math,science,reading").split(",")
    
    # System Configuration
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Teaching Configuration
    MAX_QUESTIONS_PER_SESSION = 10
    DIFFICULTY_LEVELS = ["beginner", "intermediate", "advanced"]
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required. Please set it in your .env file.")
        return True