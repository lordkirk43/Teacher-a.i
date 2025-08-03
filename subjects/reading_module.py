import uuid
import random
from typing import List, Dict, Any
from models import Question, Subject, DifficultyLevel
from .base_module import BaseSubjectModule

class ReadingModule(BaseSubjectModule):
    """Reading subject module with grade-specific content"""
    
    def __init__(self):
        super().__init__(Subject.READING)
    
    def get_grade_topics(self) -> Dict[int, List[str]]:
        """Reading topics organized by grade level"""
        return {
            1: ["Letter Recognition", "Phonics", "Sight Words", "Simple Stories", "Picture Books"],
            2: ["Vowel Sounds", "Consonant Blends", "Short Stories", "Reading Fluency", "Basic Comprehension"],
            3: ["Reading Comprehension", "Main Ideas", "Character Analysis", "Sequence of Events", "Vocabulary Building"],
            4: ["Story Elements", "Compare and Contrast", "Cause and Effect", "Inference", "Context Clues"],
            5: ["Theme Identification", "Author's Purpose", "Text Structure", "Summarizing", "Critical Thinking"],
            6: ["Literary Devices", "Point of View", "Text Analysis", "Research Skills", "Argumentative Reading"],
            7: ["Poetry Analysis", "Drama", "Nonfiction Texts", "Media Literacy", "Advanced Vocabulary"],
            8: ["Classic Literature", "Advanced Comprehension", "Literary Criticism", "Research Projects", "Academic Reading"]
        }
    
    def get_learning_objectives(self, grade_level: int) -> List[str]:
        """Learning objectives for each grade level"""
        objectives = {
            1: ["Recognize all letters", "Sound out simple words", "Read basic sight words"],
            2: ["Read simple sentences fluently", "Understand basic story elements", "Build vocabulary"],
            3: ["Identify main ideas", "Understand character motivations", "Sequence story events"],
            4: ["Make inferences from text", "Compare different texts", "Use context clues"],
            5: ["Identify themes in stories", "Understand author's purpose", "Summarize complex texts"],
            6: ["Analyze literary devices", "Understand different points of view", "Conduct research"],
            7: ["Analyze poetry and drama", "Evaluate media sources", "Build advanced vocabulary"],
            8: ["Analyze classic literature", "Write literary criticism", "Conduct academic research"]
        }
        return objectives.get(grade_level, [])
    
    def generate_practice_problems(self, grade_level: int, topic: str, difficulty: DifficultyLevel, count: int = 5) -> List[Question]:
        """Generate reading practice problems"""
        problems = []
        
        for _ in range(count):
            if topic.lower() in ["phonics", "vowel sounds", "consonant blends"]:
                problem = self._generate_phonics_question(grade_level, difficulty)
            elif topic.lower() in ["sight words", "vocabulary building", "advanced vocabulary"]:
                problem = self._generate_vocabulary_question(grade_level, difficulty)
            elif topic.lower() in ["reading comprehension", "basic comprehension", "advanced comprehension"]:
                problem = self._generate_comprehension_question(grade_level, difficulty)
            elif topic.lower() in ["main ideas", "theme identification"]:
                problem = self._generate_main_idea_question(grade_level, difficulty)
            elif topic.lower() in ["character analysis", "story elements"]:
                problem = self._generate_character_question(grade_level, difficulty)
            elif topic.lower() in ["author's purpose", "point of view"]:
                problem = self._generate_authors_purpose_question(grade_level, difficulty)
            else:
                problem = self._generate_general_reading_question(grade_level, topic, difficulty)
            
            problems.append(problem)
        
        return problems
    
    def _generate_phonics_question(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate phonics and sound-based questions"""
        if grade_level <= 2:
            phonics_data = [
                {
                    "question": "What sound does the letter 'B' make?",
                    "answer": "/b/ as in 'ball'",
                    "options": ["/b/ as in 'ball'", "/d/ as in 'dog'", "/p/ as in 'pig'", "/m/ as in 'mat'"],
                    "explanation": "The letter B makes the /b/ sound, like at the beginning of the word 'ball'."
                },
                {
                    "question": "Which word starts with the same sound as 'cat'?",
                    "answer": "cup",
                    "options": ["cup", "dog", "ball", "sun"],
                    "explanation": "Both 'cat' and 'cup' start with the /k/ sound made by the letter C."
                },
                {
                    "question": "What vowel sound do you hear in the word 'hat'?",
                    "answer": "short a",
                    "options": ["short a", "long a", "short e", "short i"],
                    "explanation": "The word 'hat' has the short 'a' sound in the middle."
                }
            ]
        else:
            phonics_data = [
                {
                    "question": "Which word has a consonant blend at the beginning?",
                    "answer": "stop",
                    "options": ["stop", "cat", "dog", "run"],
                    "explanation": "The word 'stop' begins with the consonant blend 'st' where two consonant sounds are blended together."
                },
                {
                    "question": "What type of syllable is 'make'?",
                    "answer": "silent e syllable",
                    "options": ["silent e syllable", "closed syllable", "open syllable", "r-controlled syllable"],
                    "explanation": "The word 'make' is a silent e syllable where the final 'e' makes the vowel say its name."
                }
            ]
        
        q_data = random.choice(phonics_data)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.READING,
            content=q_data["question"],
            correct_answer=q_data["answer"],
            options=q_data["options"],
            difficulty=difficulty,
            explanation=q_data["explanation"],
            hints=[
                "Say the word out loud and listen to the sounds",
                "Think about what your mouth does when you make each sound"
            ]
        )
    
    def _generate_vocabulary_question(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate vocabulary questions"""
        if grade_level <= 3:
            vocab_data = [
                {
                    "question": "What does the word 'big' mean?",
                    "answer": "large in size",
                    "options": ["large in size", "small in size", "red in color", "very fast"],
                    "explanation": "The word 'big' means large in size, like a big elephant or a big house."
                },
                {
                    "question": "Which word means the opposite of 'hot'?",
                    "answer": "cold",
                    "options": ["cold", "warm", "big", "fast"],
                    "explanation": "Cold is the opposite of hot. When something is not hot, it is cold."
                }
            ]
        else:
            vocab_data = [
                {
                    "question": "What does 'enormous' mean?",
                    "answer": "extremely large",
                    "options": ["extremely large", "very small", "medium sized", "colorful"],
                    "explanation": "'Enormous' means extremely large or huge, much bigger than just 'big'."
                },
                {
                    "question": "If someone is 'cautious', they are:",
                    "answer": "careful and thoughtful",
                    "options": ["careful and thoughtful", "reckless and wild", "happy and excited", "tired and sleepy"],
                    "explanation": "Being cautious means being careful and thinking before you act to avoid danger or mistakes."
                },
                {
                    "question": "What does 'analyze' mean?",
                    "answer": "to examine something carefully",
                    "options": ["to examine something carefully", "to ignore completely", "to run away quickly", "to eat something"],
                    "explanation": "To analyze means to look at something carefully and break it down to understand it better."
                }
            ]
        
        q_data = random.choice(vocab_data)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.READING,
            content=q_data["question"],
            correct_answer=q_data["answer"],
            options=q_data["options"],
            difficulty=difficulty,
            explanation=q_data["explanation"],
            hints=[
                "Think about how the word is used in sentences you've heard",
                "Look for clues in the word itself or similar words you know"
            ]
        )
    
    def _generate_comprehension_question(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate reading comprehension questions"""
        if grade_level <= 3:
            story = "Sam the dog loved to play in the park. Every morning, he would run to the big oak tree and wait for his friend Lucy. Lucy always brought a red ball for them to play with. They would play fetch until it was time for lunch."
            
            questions = [
                {
                    "question": f"Read this story: '{story}' What did Lucy bring to play with?",
                    "answer": "a red ball",
                    "options": ["a red ball", "a blue frisbee", "a yellow stick", "a green rope"],
                    "explanation": "The story says 'Lucy always brought a red ball for them to play with.'"
                },
                {
                    "question": f"Read this story: '{story}' Where did Sam wait for Lucy?",
                    "answer": "by the big oak tree",
                    "options": ["by the big oak tree", "by the pond", "by the playground", "by the gate"],
                    "explanation": "The story says Sam 'would run to the big oak tree and wait for his friend Lucy.'"
                }
            ]
        else:
            story = "The ancient library stood at the center of the small town, its weathered stone walls holding centuries of knowledge. Maria, a curious student, discovered a hidden section behind a moveable bookshelf. Inside, she found manuscripts written in languages she had never seen before, sparking her interest in becoming a linguist."
            
            questions = [
                {
                    "question": f"Read this passage: '{story}' What did Maria discover in the library?",
                    "answer": "a hidden section with old manuscripts",
                    "options": ["a hidden section with old manuscripts", "a secret treasure chest", "a computer room", "a study group"],
                    "explanation": "Maria found a hidden section behind a bookshelf containing manuscripts in unknown languages."
                },
                {
                    "question": f"Read this passage: '{story}' What career did this experience inspire Maria to consider?",
                    "answer": "becoming a linguist",
                    "options": ["becoming a linguist", "becoming a librarian", "becoming a writer", "becoming a teacher"],
                    "explanation": "The passage states that finding manuscripts in unknown languages sparked her interest in becoming a linguist."
                }
            ]
        
        q_data = random.choice(questions)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.READING,
            content=q_data["question"],
            correct_answer=q_data["answer"],
            options=q_data["options"],
            difficulty=difficulty,
            explanation=q_data["explanation"],
            hints=[
                "Read the passage carefully and look for specific details",
                "The answer is usually stated directly in the text"
            ]
        )
    
    def _generate_main_idea_question(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate main idea questions"""
        if grade_level <= 4:
            passage = "Bees are very important insects. They help flowers make seeds by carrying pollen from flower to flower. Without bees, many plants could not reproduce. Bees also make honey, which people enjoy eating. We should protect bees because they help our environment."
            
            question_text = f"Read this passage: '{passage}' What is the main idea?"
            correct_answer = "Bees are important and should be protected"
            options = ["Bees are important and should be protected", "Bees make delicious honey", "Flowers are pretty", "Insects are scary"]
            explanation = "The main idea is that bees are important for the environment and should be protected. All the details support this central idea."
        else:
            passage = "The invention of the printing press in the 15th century revolutionized the spread of information. Before this innovation, books were copied by hand, making them expensive and rare. Johannes Gutenberg's printing press allowed books to be produced quickly and cheaply, leading to increased literacy rates and the rapid spread of ideas across Europe."
            
            question_text = f"Read this passage: '{passage}' What is the main idea?"
            correct_answer = "The printing press revolutionized information sharing"
            options = ["The printing press revolutionized information sharing", "Johannes Gutenberg was a famous inventor", "Books used to be very expensive", "Europe had many new ideas"]
            explanation = "The main idea is that the printing press revolutionized how information was shared, making books cheaper and ideas more accessible."
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.READING,
            content=question_text,
            correct_answer=correct_answer,
            options=options,
            difficulty=difficulty,
            explanation=explanation,
            hints=[
                "Look for the most important point the author is trying to make",
                "The main idea is what the whole passage is about, not just one detail"
            ]
        )
    
    def _generate_character_question(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate character analysis questions"""
        if grade_level <= 4:
            story = "Emma was nervous about her first day at a new school. She packed her backpack three times and checked her schedule over and over. When she got to school, she saw another student sitting alone looking sad. Even though Emma was scared, she walked over and introduced herself. Soon they were both smiling and talking about their favorite books."
            
            questions = [
                {
                    "question": f"Read this story: '{story}' How did Emma feel at the beginning?",
                    "answer": "nervous and scared",
                    "options": ["nervous and scared", "happy and excited", "angry and upset", "bored and tired"],
                    "explanation": "The story says Emma was nervous and scared about her first day at a new school."
                },
                {
                    "question": f"Read this story: '{story}' What does Emma's action show about her character?",
                    "answer": "she is kind and caring",
                    "options": ["she is kind and caring", "she is mean and selfish", "she is lazy and careless", "she is loud and rude"],
                    "explanation": "Even though Emma was scared, she helped another student who looked sad, showing she is kind and caring."
                }
            ]
        else:
            story = "Despite facing numerous obstacles, Dr. Sarah Chen persevered in her research on renewable energy. When her funding was cut, she worked extra hours at a part-time job to continue her experiments. Her colleagues admired her determination, and her breakthrough discovery eventually led to more efficient solar panels."
            
            questions = [
                {
                    "question": f"Read this passage: '{story}' What character trait best describes Dr. Chen?",
                    "answer": "determined and persevering",
                    "options": ["determined and persevering", "lazy and unmotivated", "angry and bitter", "careless and sloppy"],
                    "explanation": "Dr. Chen showed determination by continuing her research despite obstacles and working extra hours when funding was cut."
                }
            ]
        
        q_data = random.choice(questions)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.READING,
            content=q_data["question"],
            correct_answer=q_data["answer"],
            options=q_data["options"],
            difficulty=difficulty,
            explanation=q_data["explanation"],
            hints=[
                "Look at what the character does and says",
                "Think about how the character's actions show their personality"
            ]
        )
    
    def _generate_authors_purpose_question(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate author's purpose questions"""
        passages = [
            {
                "text": "Recycling is one of the easiest ways to help protect our planet. When you recycle paper, plastic, and glass, you reduce waste and save natural resources. Everyone should make recycling a daily habit!",
                "purpose": "to persuade readers to recycle",
                "options": ["to persuade readers to recycle", "to entertain with a funny story", "to inform about different materials", "to describe a recycling plant"],
                "explanation": "The author is trying to convince readers that they should recycle by explaining the benefits and urging action."
            },
            {
                "text": "The water cycle begins when the sun heats water in oceans, lakes, and rivers. This causes evaporation, turning liquid water into water vapor. The water vapor rises into the atmosphere, where it cools and condenses into clouds.",
                "purpose": "to inform about the water cycle",
                "options": ["to inform about the water cycle", "to persuade people to save water", "to entertain with a story", "to describe a specific lake"],
                "explanation": "The author is providing factual information about how the water cycle works, which is informative writing."
            }
        ]
        
        passage_data = random.choice(passages)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.READING,
            content=f"Read this passage: '{passage_data['text']}' What is the author's purpose?",
            correct_answer=passage_data["purpose"],
            options=passage_data["options"],
            difficulty=difficulty,
            explanation=passage_data["explanation"],
            hints=[
                "Ask yourself: Is the author trying to teach, convince, or entertain?",
                "Look for clue words like 'should', 'must' (persuade) or facts and explanations (inform)"
            ]
        )
    
    def _generate_general_reading_question(self, grade_level: int, topic: str, difficulty: DifficultyLevel) -> Question:
        """Generate general reading questions"""
        questions = [
            {
                "question": "What is a synonym for 'happy'?",
                "answer": "joyful",
                "options": ["joyful", "sad", "angry", "tired"],
                "explanation": "A synonym is a word that means the same thing. 'Joyful' means the same as 'happy'."
            },
            {
                "question": "In a story, what is the 'setting'?",
                "answer": "when and where the story takes place",
                "options": ["when and where the story takes place", "the main character", "the problem in the story", "the ending"],
                "explanation": "The setting is when (time) and where (place) a story happens."
            },
            {
                "question": "What is an antonym for 'big'?",
                "answer": "small",
                "options": ["small", "large", "huge", "giant"],
                "explanation": "An antonym is a word that means the opposite. 'Small' is the opposite of 'big'."
            }
        ]
        
        q_data = random.choice(questions)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.READING,
            content=q_data["question"],
            correct_answer=q_data["answer"],
            options=q_data["options"],
            difficulty=difficulty,
            explanation=q_data["explanation"],
            hints=[
                "Think about what you've learned about reading and stories",
                "Use context clues and your knowledge of word relationships"
            ]
        )