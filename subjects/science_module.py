import uuid
import random
from typing import List, Dict, Any
from models import Question, Subject, DifficultyLevel
from .base_module import BaseSubjectModule

class ScienceModule(BaseSubjectModule):
    """Science subject module with grade-specific content"""
    
    def __init__(self):
        super().__init__(Subject.SCIENCE)
    
    def get_grade_topics(self) -> Dict[int, List[str]]:
        """Science topics organized by grade level"""
        return {
            1: ["Animals", "Plants", "Weather", "Seasons", "Our Bodies"],
            2: ["Life Cycles", "Habitats", "Materials", "Day and Night", "Healthy Living"],
            3: ["Ecosystems", "States of Matter", "Simple Machines", "Earth's Surface", "Plant Growth"],
            4: ["Food Chains", "Rocks and Minerals", "Energy", "Water Cycle", "Animal Adaptations"],
            5: ["Solar System", "Human Body Systems", "Chemical vs Physical Changes", "Electricity", "Ecosystems Balance"],
            6: ["Cell Structure", "Genetics", "Earth's Layers", "Forces and Motion", "Climate vs Weather"],
            7: ["Photosynthesis", "Periodic Table", "Plate Tectonics", "Simple Chemistry", "Evolution"],
            8: ["Chemical Reactions", "Physics Laws", "Genetics and DNA", "Environmental Science", "Space Exploration"]
        }
    
    def get_learning_objectives(self, grade_level: int) -> List[str]:
        """Learning objectives for each grade level"""
        objectives = {
            1: ["Identify basic animal needs", "Recognize plant parts", "Describe weather patterns"],
            2: ["Understand animal life cycles", "Compare different habitats", "Identify material properties"],
            3: ["Explain simple ecosystems", "Describe states of matter", "Identify simple machines"],
            4: ["Trace energy through food chains", "Classify rocks and minerals", "Explain the water cycle"],
            5: ["Describe the solar system", "Identify body systems", "Distinguish physical and chemical changes"],
            6: ["Understand cell structure", "Explain basic genetics", "Describe Earth's layers"],
            7: ["Explain photosynthesis", "Use the periodic table", "Understand plate tectonics"],
            8: ["Balance chemical equations", "Apply physics laws", "Understand DNA structure"]
        }
        return objectives.get(grade_level, [])
    
    def generate_practice_problems(self, grade_level: int, topic: str, difficulty: DifficultyLevel, count: int = 5) -> List[Question]:
        """Generate science practice problems"""
        problems = []
        
        for _ in range(count):
            if topic.lower() in ["animals", "animal adaptations"]:
                problem = self._generate_animal_question(grade_level, difficulty)
            elif topic.lower() in ["plants", "plant growth", "photosynthesis"]:
                problem = self._generate_plant_question(grade_level, difficulty)
            elif topic.lower() in ["weather", "climate vs weather"]:
                problem = self._generate_weather_question(grade_level, difficulty)
            elif topic.lower() in ["states of matter", "chemical vs physical changes"]:
                problem = self._generate_matter_question(grade_level, difficulty)
            elif topic.lower() in ["solar system", "space exploration"]:
                problem = self._generate_space_question(grade_level, difficulty)
            elif topic.lower() in ["human body systems", "our bodies"]:
                problem = self._generate_body_question(grade_level, difficulty)
            else:
                problem = self._generate_general_science_question(grade_level, topic, difficulty)
            
            problems.append(problem)
        
        return problems
    
    def _generate_animal_question(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate animal-related questions"""
        if grade_level <= 3:
            animals_data = {
                "dog": {"habitat": "homes with humans", "food": "meat and dog food", "baby": "puppy"},
                "cat": {"habitat": "homes with humans", "food": "meat and cat food", "baby": "kitten"},
                "bird": {"habitat": "trees and sky", "food": "seeds and worms", "baby": "chick"},
                "fish": {"habitat": "water", "food": "small plants and animals", "baby": "fry"}
            }
        else:
            animals_data = {
                "lion": {"habitat": "grasslands", "food": "meat (carnivore)", "adaptation": "sharp teeth and claws"},
                "elephant": {"habitat": "savannas", "food": "plants (herbivore)", "adaptation": "large ears for cooling"},
                "polar bear": {"habitat": "arctic ice", "food": "seals and fish", "adaptation": "thick fur for warmth"},
                "giraffe": {"habitat": "african savannas", "food": "leaves from tall trees", "adaptation": "long neck"}
            }
        
        animal = random.choice(list(animals_data.keys()))
        data = animals_data[animal]
        
        if grade_level <= 3:
            question_types = ["habitat", "food", "baby"]
            q_type = random.choice(question_types)
            
            if q_type == "habitat":
                question_text = f"Where do {animal}s usually live?"
                correct_answer = data["habitat"]
                wrong_answers = ["in the ocean", "underground", "in space"]
            elif q_type == "food":
                question_text = f"What do {animal}s eat?"
                correct_answer = data["food"]
                wrong_answers = ["rocks", "plastic", "nothing"]
            else:  # baby
                question_text = f"What is a baby {animal} called?"
                correct_answer = data["baby"]
                wrong_answers = ["cub", "calf", "joey"]
        else:
            question_text = f"What adaptation helps a {animal} survive in its environment?"
            correct_answer = data["adaptation"]
            wrong_answers = ["webbed feet", "gills for breathing", "ability to fly"]
        
        # Remove correct answer from wrong answers if it exists
        wrong_answers = [ans for ans in wrong_answers if ans != correct_answer]
        options = [correct_answer] + wrong_answers[:3]
        random.shuffle(options)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.SCIENCE,
            content=question_text,
            correct_answer=correct_answer,
            options=options,
            difficulty=difficulty,
            explanation=f"{animal.title()}s have adapted to their environment. {correct_answer}.",
            hints=[
                f"Think about where {animal}s live and what they need to survive",
                "Consider how the animal's body helps it in its environment"
            ]
        )
    
    def _generate_plant_question(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate plant-related questions"""
        if grade_level <= 3:
            questions = [
                {
                    "question": "What do plants need to grow?",
                    "answer": "sunlight, water, and air",
                    "options": ["sunlight, water, and air", "only water", "only sunlight", "candy and soda"],
                    "explanation": "Plants need sunlight for energy, water for nutrients, and air (carbon dioxide) to make food."
                },
                {
                    "question": "What part of the plant takes in water?",
                    "answer": "roots",
                    "options": ["roots", "leaves", "flowers", "stem"],
                    "explanation": "Roots grow underground and absorb water and nutrients from the soil."
                }
            ]
        else:
            questions = [
                {
                    "question": "What process do plants use to make their own food?",
                    "answer": "photosynthesis",
                    "options": ["photosynthesis", "respiration", "digestion", "reproduction"],
                    "explanation": "Photosynthesis is the process where plants use sunlight, water, and carbon dioxide to make glucose (food)."
                },
                {
                    "question": "What gas do plants take in during photosynthesis?",
                    "answer": "carbon dioxide",
                    "options": ["carbon dioxide", "oxygen", "nitrogen", "hydrogen"],
                    "explanation": "Plants take in carbon dioxide from the air and release oxygen during photosynthesis."
                }
            ]
        
        q_data = random.choice(questions)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.SCIENCE,
            content=q_data["question"],
            correct_answer=q_data["answer"],
            options=q_data["options"],
            difficulty=difficulty,
            explanation=q_data["explanation"],
            hints=[
                "Think about what plants need from their environment",
                "Consider the different parts of a plant and their functions"
            ]
        )
    
    def _generate_weather_question(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate weather-related questions"""
        if grade_level <= 3:
            questions = [
                {
                    "question": "What causes rain?",
                    "answer": "water evaporating and then condensing in clouds",
                    "options": ["water evaporating and then condensing in clouds", "clouds getting angry", "the sun being sad", "wind blowing hard"],
                    "explanation": "Rain forms when water evaporates, rises into the sky, forms clouds, and then falls back down."
                },
                {
                    "question": "Which season comes after winter?",
                    "answer": "spring",
                    "options": ["spring", "summer", "fall", "winter again"],
                    "explanation": "Spring comes after winter, when plants start to grow and weather gets warmer."
                }
            ]
        else:
            questions = [
                {
                    "question": "What is the difference between weather and climate?",
                    "answer": "weather is daily conditions, climate is long-term patterns",
                    "options": ["weather is daily conditions, climate is long-term patterns", "they are the same thing", "weather is hot, climate is cold", "climate changes daily"],
                    "explanation": "Weather describes daily atmospheric conditions, while climate describes long-term weather patterns over many years."
                },
                {
                    "question": "What causes different seasons on Earth?",
                    "answer": "Earth's tilt as it orbits the sun",
                    "options": ["Earth's tilt as it orbits the sun", "the moon's phases", "distance from the sun", "the sun getting hotter and cooler"],
                    "explanation": "Earth's seasons are caused by the planet's tilt, which affects how much sunlight different areas receive."
                }
            ]
        
        q_data = random.choice(questions)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.SCIENCE,
            content=q_data["question"],
            correct_answer=q_data["answer"],
            options=q_data["options"],
            difficulty=difficulty,
            explanation=q_data["explanation"],
            hints=[
                "Think about what you observe in the sky and environment",
                "Consider how the Earth and sun interact"
            ]
        )
    
    def _generate_matter_question(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate questions about states of matter"""
        if grade_level <= 4:
            questions = [
                {
                    "question": "What are the three main states of matter?",
                    "answer": "solid, liquid, and gas",
                    "options": ["solid, liquid, and gas", "hot, cold, and warm", "big, medium, and small", "hard, soft, and smooth"],
                    "explanation": "The three main states of matter are solid (like ice), liquid (like water), and gas (like steam)."
                },
                {
                    "question": "What happens to water when it freezes?",
                    "answer": "it becomes ice (solid)",
                    "options": ["it becomes ice (solid)", "it becomes steam", "it disappears", "it becomes heavier"],
                    "explanation": "When water freezes at 0°C (32°F), it changes from a liquid to a solid state called ice."
                }
            ]
        else:
            questions = [
                {
                    "question": "What is a physical change?",
                    "answer": "a change that doesn't create a new substance",
                    "options": ["a change that doesn't create a new substance", "a change that creates a new substance", "a change in color only", "a change in temperature only"],
                    "explanation": "A physical change alters the form or appearance of matter but doesn't create a new substance, like melting ice."
                },
                {
                    "question": "What is a chemical change?",
                    "answer": "a change that creates a new substance",
                    "options": ["a change that creates a new substance", "a change in shape only", "a change in size only", "a change in location only"],
                    "explanation": "A chemical change creates a new substance with different properties, like burning wood to make ash."
                }
            ]
        
        q_data = random.choice(questions)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.SCIENCE,
            content=q_data["question"],
            correct_answer=q_data["answer"],
            options=q_data["options"],
            difficulty=difficulty,
            explanation=q_data["explanation"],
            hints=[
                "Think about how matter can change form",
                "Consider examples from everyday life"
            ]
        )
    
    def _generate_space_question(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate space-related questions"""
        questions = [
            {
                "question": "What is the closest star to Earth?",
                "answer": "the Sun",
                "options": ["the Sun", "the Moon", "Mars", "Jupiter"],
                "explanation": "The Sun is the closest star to Earth and provides light and heat for our planet."
            },
            {
                "question": "How many planets are in our solar system?",
                "answer": "8",
                "options": ["8", "7", "9", "10"],
                "explanation": "There are 8 planets in our solar system: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune."
            },
            {
                "question": "What causes day and night on Earth?",
                "answer": "Earth rotating on its axis",
                "options": ["Earth rotating on its axis", "the Moon moving", "the Sun moving", "clouds covering the Sun"],
                "explanation": "Day and night are caused by Earth spinning (rotating) on its axis, so different parts face the Sun."
            }
        ]
        
        q_data = random.choice(questions)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.SCIENCE,
            content=q_data["question"],
            correct_answer=q_data["answer"],
            options=q_data["options"],
            difficulty=difficulty,
            explanation=q_data["explanation"],
            hints=[
                "Think about what you can see in the sky",
                "Consider how Earth moves in space"
            ]
        )
    
    def _generate_body_question(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate human body questions"""
        if grade_level <= 3:
            questions = [
                {
                    "question": "What does your heart do?",
                    "answer": "pumps blood through your body",
                    "options": ["pumps blood through your body", "helps you think", "helps you see", "helps you hear"],
                    "explanation": "Your heart is a muscle that pumps blood to carry oxygen and nutrients throughout your body."
                },
                {
                    "question": "What do your lungs help you do?",
                    "answer": "breathe",
                    "options": ["breathe", "digest food", "see colors", "hear sounds"],
                    "explanation": "Your lungs help you breathe by taking in oxygen from the air and removing carbon dioxide."
                }
            ]
        else:
            questions = [
                {
                    "question": "What system in your body fights off germs?",
                    "answer": "immune system",
                    "options": ["immune system", "digestive system", "respiratory system", "nervous system"],
                    "explanation": "The immune system protects your body from germs, viruses, and other harmful substances."
                },
                {
                    "question": "What connects your muscles to your bones?",
                    "answer": "tendons",
                    "options": ["tendons", "ligaments", "cartilage", "joints"],
                    "explanation": "Tendons are strong, flexible tissues that connect muscles to bones, allowing movement."
                }
            ]
        
        q_data = random.choice(questions)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.SCIENCE,
            content=q_data["question"],
            correct_answer=q_data["answer"],
            options=q_data["options"],
            difficulty=difficulty,
            explanation=q_data["explanation"],
            hints=[
                "Think about how your body works",
                "Consider what each body part or system does"
            ]
        )
    
    def _generate_general_science_question(self, grade_level: int, topic: str, difficulty: DifficultyLevel) -> Question:
        """Generate general science questions for various topics"""
        general_questions = [
            {
                "question": "What tool would you use to measure temperature?",
                "answer": "thermometer",
                "options": ["thermometer", "ruler", "scale", "clock"],
                "explanation": "A thermometer is used to measure how hot or cold something is."
            },
            {
                "question": "What is the scientific method?",
                "answer": "a way to test ideas and answer questions",
                "options": ["a way to test ideas and answer questions", "a type of math", "a kind of machine", "a science book"],
                "explanation": "The scientific method is a process scientists use to study the world and answer questions through observation and experiments."
            }
        ]
        
        q_data = random.choice(general_questions)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.SCIENCE,
            content=q_data["question"],
            correct_answer=q_data["answer"],
            options=q_data["options"],
            difficulty=difficulty,
            explanation=q_data["explanation"],
            hints=[
                "Think about tools and methods scientists use",
                "Consider how we learn about the world around us"
            ]
        )