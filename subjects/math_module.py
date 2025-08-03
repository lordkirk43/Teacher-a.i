import uuid
import random
from typing import List, Dict, Any
from models import Question, Subject, DifficultyLevel
from .base_module import BaseSubjectModule

class MathModule(BaseSubjectModule):
    """Math subject module with grade-specific content"""
    
    def __init__(self):
        super().__init__(Subject.MATH)
    
    def get_grade_topics(self) -> Dict[int, List[str]]:
        """Math topics organized by grade level"""
        return {
            1: ["Counting", "Addition", "Subtraction", "Shapes", "Patterns"],
            2: ["Place Value", "Two-digit Addition", "Two-digit Subtraction", "Time", "Money"],
            3: ["Multiplication", "Division", "Fractions", "Measurement", "Data and Graphs"],
            4: ["Multi-digit Multiplication", "Long Division", "Decimals", "Geometry", "Area and Perimeter"],
            5: ["Fractions Operations", "Decimals Operations", "Volume", "Coordinate Plane", "Order of Operations"],
            6: ["Ratios", "Proportions", "Percentages", "Integers", "Basic Algebra"],
            7: ["Algebraic Expressions", "Equations", "Inequalities", "Geometry Formulas", "Probability"],
            8: ["Linear Equations", "Systems of Equations", "Functions", "Pythagorean Theorem", "Statistics"]
        }
    
    def get_learning_objectives(self, grade_level: int) -> List[str]:
        """Learning objectives for each grade level"""
        objectives = {
            1: ["Count to 100", "Add and subtract within 20", "Identify basic shapes"],
            2: ["Understand place value to 100", "Add and subtract within 100", "Tell time"],
            3: ["Multiply and divide within 100", "Understand fractions", "Solve word problems"],
            4: ["Multiply multi-digit numbers", "Add and subtract fractions", "Find area and perimeter"],
            5: ["Perform operations with decimals", "Add and subtract fractions", "Understand volume"],
            6: ["Solve ratio and proportion problems", "Work with percentages", "Understand integers"],
            7: ["Solve algebraic equations", "Work with geometric formulas", "Calculate probability"],
            8: ["Solve linear equations", "Work with functions", "Apply Pythagorean theorem"]
        }
        return objectives.get(grade_level, [])
    
    def generate_practice_problems(self, grade_level: int, topic: str, difficulty: DifficultyLevel, count: int = 5) -> List[Question]:
        """Generate math practice problems"""
        problems = []
        
        for _ in range(count):
            if topic.lower() == "addition":
                problem = self._generate_addition_problem(grade_level, difficulty)
            elif topic.lower() == "subtraction":
                problem = self._generate_subtraction_problem(grade_level, difficulty)
            elif topic.lower() == "multiplication":
                problem = self._generate_multiplication_problem(grade_level, difficulty)
            elif topic.lower() == "division":
                problem = self._generate_division_problem(grade_level, difficulty)
            elif topic.lower() == "fractions":
                problem = self._generate_fraction_problem(grade_level, difficulty)
            else:
                problem = self._generate_word_problem(grade_level, topic, difficulty)
            
            problems.append(problem)
        
        return problems
    
    def _generate_addition_problem(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate addition problems based on grade and difficulty"""
        if grade_level <= 2:
            if difficulty == DifficultyLevel.BEGINNER:
                a, b = random.randint(1, 5), random.randint(1, 5)
            elif difficulty == DifficultyLevel.INTERMEDIATE:
                a, b = random.randint(1, 10), random.randint(1, 10)
            else:
                a, b = random.randint(10, 20), random.randint(1, 10)
        else:
            if difficulty == DifficultyLevel.BEGINNER:
                a, b = random.randint(10, 50), random.randint(10, 50)
            elif difficulty == DifficultyLevel.INTERMEDIATE:
                a, b = random.randint(50, 200), random.randint(50, 200)
            else:
                a, b = random.randint(200, 1000), random.randint(200, 1000)
        
        answer = a + b
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.MATH,
            content=f"What is {a} + {b}?",
            correct_answer=str(answer),
            options=[str(answer), str(answer + 1), str(answer - 1), str(answer + 2)],
            difficulty=difficulty,
            explanation=f"{a} + {b} = {answer}. When we add {a} and {b}, we get {answer}.",
            hints=[
                f"Try counting up from {a}",
                f"You can break down {b} into smaller numbers to make it easier"
            ]
        )
    
    def _generate_subtraction_problem(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate subtraction problems"""
        if grade_level <= 2:
            if difficulty == DifficultyLevel.BEGINNER:
                a, b = random.randint(5, 10), random.randint(1, 5)
            else:
                a, b = random.randint(10, 20), random.randint(1, 10)
        else:
            if difficulty == DifficultyLevel.BEGINNER:
                a, b = random.randint(20, 100), random.randint(10, 50)
            else:
                a, b = random.randint(100, 500), random.randint(50, 200)
        
        # Ensure a > b for positive results
        if b > a:
            a, b = b, a
        
        answer = a - b
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.MATH,
            content=f"What is {a} - {b}?",
            correct_answer=str(answer),
            options=[str(answer), str(answer + 1), str(answer - 1), str(answer + 2)],
            difficulty=difficulty,
            explanation=f"{a} - {b} = {answer}. When we subtract {b} from {a}, we get {answer}.",
            hints=[
                f"Try counting backwards from {a}",
                f"Think: what number plus {b} equals {a}?"
            ]
        )
    
    def _generate_multiplication_problem(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate multiplication problems"""
        if grade_level <= 3:
            if difficulty == DifficultyLevel.BEGINNER:
                a, b = random.randint(1, 5), random.randint(1, 5)
            else:
                a, b = random.randint(1, 10), random.randint(1, 10)
        else:
            if difficulty == DifficultyLevel.BEGINNER:
                a, b = random.randint(1, 12), random.randint(1, 12)
            else:
                a, b = random.randint(10, 25), random.randint(2, 12)
        
        answer = a * b
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.MATH,
            content=f"What is {a} × {b}?",
            correct_answer=str(answer),
            options=[str(answer), str(answer + a), str(answer - a), str(answer + b)],
            difficulty=difficulty,
            explanation=f"{a} × {b} = {answer}. This means {a} groups of {b}, or {b} added {a} times.",
            hints=[
                f"Try adding {b} to itself {a} times",
                f"Remember your times tables!"
            ]
        )
    
    def _generate_division_problem(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate division problems"""
        # Generate division by creating multiplication first
        if grade_level <= 4:
            if difficulty == DifficultyLevel.BEGINNER:
                divisor = random.randint(2, 5)
                quotient = random.randint(2, 10)
            else:
                divisor = random.randint(2, 10)
                quotient = random.randint(2, 12)
        else:
            if difficulty == DifficultyLevel.BEGINNER:
                divisor = random.randint(2, 12)
                quotient = random.randint(2, 20)
            else:
                divisor = random.randint(10, 25)
                quotient = random.randint(5, 30)
        
        dividend = divisor * quotient
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.MATH,
            content=f"What is {dividend} ÷ {divisor}?",
            correct_answer=str(quotient),
            options=[str(quotient), str(quotient + 1), str(quotient - 1), str(quotient + 2)],
            difficulty=difficulty,
            explanation=f"{dividend} ÷ {divisor} = {quotient}. This means {dividend} divided into {divisor} equal groups gives us {quotient} in each group.",
            hints=[
                f"Think: {divisor} times what number equals {dividend}?",
                f"Try using multiplication to check your answer"
            ]
        )
    
    def _generate_fraction_problem(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate fraction problems"""
        if difficulty == DifficultyLevel.BEGINNER:
            numerator = random.randint(1, 4)
            denominator = random.randint(numerator + 1, 8)
        else:
            numerator = random.randint(1, 10)
            denominator = random.randint(numerator + 1, 20)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.MATH,
            content=f"What fraction represents {numerator} out of {denominator} equal parts?",
            correct_answer=f"{numerator}/{denominator}",
            options=[f"{numerator}/{denominator}", f"{denominator}/{numerator}", f"{numerator}/{numerator}", f"{denominator}/{denominator}"],
            difficulty=difficulty,
            explanation=f"When we have {numerator} parts out of {denominator} total equal parts, we write it as {numerator}/{denominator}.",
            hints=[
                "The top number shows how many parts we have",
                "The bottom number shows how many total parts there are"
            ]
        )
    
    def _generate_word_problem(self, grade_level: int, topic: str, difficulty: DifficultyLevel) -> Question:
        """Generate word problems for various topics"""
        scenarios = [
            "Sarah has {a} apples. She gives away {b} apples. How many apples does she have left?",
            "There are {a} students in the class. Each student has {b} pencils. How many pencils are there in total?",
            "A box contains {a} cookies. If {b} cookies are eaten, how many cookies remain?",
            "Tom collects {a} stickers each day for {b} days. How many stickers does he collect in total?"
        ]
        
        scenario = random.choice(scenarios)
        
        if "gives away" in scenario or "eaten" in scenario:
            # Subtraction problem
            a = random.randint(10, 50)
            b = random.randint(1, a)
            answer = a - b
            operation = "subtraction"
        else:
            # Multiplication problem
            a = random.randint(2, 12)
            b = random.randint(2, 10)
            answer = a * b
            operation = "multiplication"
        
        problem_text = scenario.format(a=a, b=b)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.MATH,
            content=problem_text,
            correct_answer=str(answer),
            options=[str(answer), str(answer + 1), str(answer - 1), str(answer + 5)],
            difficulty=difficulty,
            explanation=f"This is a {operation} problem. The answer is {answer}.",
            hints=[
                "Read the problem carefully and identify what operation to use",
                f"Look for key words that suggest {operation}"
            ]
        )