import uuid
import random
from typing import List, Dict, Any
from models import Question, Subject, DifficultyLevel
from .base_module import BaseSubjectModule

class WritingModule(BaseSubjectModule):
    """Writing subject module with grade-specific content"""
    
    def __init__(self):
        super().__init__(Subject.WRITING)
    
    def get_grade_topics(self) -> Dict[int, List[str]]:
        """Writing topics organized by grade level"""
        return {
            1: ["Letter Formation", "Simple Sentences", "Capitals and Periods", "Spelling", "Drawing and Labeling"],
            2: ["Complete Sentences", "Nouns and Verbs", "Question Marks", "Story Writing", "Descriptive Words"],
            3: ["Paragraphs", "Adjectives", "Compound Sentences", "Personal Narratives", "Editing"],
            4: ["Essay Structure", "Complex Sentences", "Punctuation", "Research Writing", "Revision"],
            5: ["Five-Paragraph Essays", "Transitions", "Citing Sources", "Persuasive Writing", "Grammar Rules"],
            6: ["Argumentative Writing", "Literary Analysis", "Advanced Grammar", "Research Papers", "Peer Review"],
            7: ["Creative Writing", "Poetry", "Formal Writing", "MLA Format", "Critical Analysis"],
            8: ["Advanced Essays", "Rhetorical Devices", "Academic Writing", "Independent Research", "Portfolio Development"]
        }
    
    def get_learning_objectives(self, grade_level: int) -> List[str]:
        """Learning objectives for each grade level"""
        objectives = {
            1: ["Write letters correctly", "Write simple sentences", "Use capitals and periods"],
            2: ["Write complete sentences", "Identify nouns and verbs", "Write short stories"],
            3: ["Write organized paragraphs", "Use descriptive language", "Edit their writing"],
            4: ["Write structured essays", "Use complex sentences", "Conduct simple research"],
            5: ["Write five-paragraph essays", "Use transitions effectively", "Write persuasively"],
            6: ["Write argumentative essays", "Analyze literature", "Use advanced grammar"],
            7: ["Write creatively", "Analyze poetry", "Use formal writing style"],
            8: ["Write advanced essays", "Use rhetorical devices", "Conduct independent research"]
        }
        return objectives.get(grade_level, [])
    
    def generate_practice_problems(self, grade_level: int, topic: str, difficulty: DifficultyLevel, count: int = 5) -> List[Question]:
        """Generate writing practice problems"""
        problems = []
        
        for _ in range(count):
            if topic.lower() in ["grammar rules", "nouns and verbs", "adjectives", "advanced grammar"]:
                problem = self._generate_grammar_question(grade_level, difficulty)
            elif topic.lower() in ["punctuation", "capitals and periods", "question marks"]:
                problem = self._generate_punctuation_question(grade_level, difficulty)
            elif topic.lower() in ["complete sentences", "simple sentences", "complex sentences", "compound sentences"]:
                problem = self._generate_sentence_question(grade_level, difficulty)
            elif topic.lower() in ["essay structure", "paragraphs", "five-paragraph essays"]:
                problem = self._generate_structure_question(grade_level, difficulty)
            elif topic.lower() in ["spelling", "descriptive words"]:
                problem = self._generate_spelling_question(grade_level, difficulty)
            elif topic.lower() in ["story writing", "creative writing", "personal narratives"]:
                problem = self._generate_creative_writing_question(grade_level, difficulty)
            else:
                problem = self._generate_general_writing_question(grade_level, topic, difficulty)
            
            problems.append(problem)
        
        return problems
    
    def _generate_grammar_question(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate grammar questions"""
        if grade_level <= 3:
            grammar_questions = [
                {
                    "question": "Which word is a noun in this sentence: 'The dog ran quickly'?",
                    "answer": "dog",
                    "options": ["dog", "ran", "quickly", "the"],
                    "explanation": "A noun is a person, place, or thing. 'Dog' is a thing (animal), so it's a noun."
                },
                {
                    "question": "Which word is a verb in this sentence: 'She sings beautifully'?",
                    "answer": "sings",
                    "options": ["sings", "she", "beautifully", "none"],
                    "explanation": "A verb is an action word. 'Sings' shows what she is doing, so it's a verb."
                },
                {
                    "question": "Which word describes the cat in this sentence: 'The fluffy cat slept'?",
                    "answer": "fluffy",
                    "options": ["fluffy", "cat", "slept", "the"],
                    "explanation": "'Fluffy' is an adjective that describes what the cat looks like."
                }
            ]
        else:
            grammar_questions = [
                {
                    "question": "What type of pronoun is 'themselves' in: 'They taught themselves to swim'?",
                    "answer": "reflexive pronoun",
                    "options": ["reflexive pronoun", "personal pronoun", "possessive pronoun", "demonstrative pronoun"],
                    "explanation": "A reflexive pronoun ends in -self or -selves and refers back to the subject."
                },
                {
                    "question": "What is the subject of this sentence: 'After the storm, the old tree fell down'?",
                    "answer": "the old tree",
                    "options": ["the old tree", "after the storm", "fell down", "the storm"],
                    "explanation": "The subject is who or what the sentence is about. The old tree is what fell down."
                },
                {
                    "question": "Which sentence uses the correct form of the verb?",
                    "answer": "She has written three books.",
                    "options": ["She has written three books.", "She have written three books.", "She has wrote three books.", "She had wrote three books."],
                    "explanation": "The correct past participle of 'write' is 'written', and it pairs with 'has' for present perfect tense."
                }
            ]
        
        q_data = random.choice(grammar_questions)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.WRITING,
            content=q_data["question"],
            correct_answer=q_data["answer"],
            options=q_data["options"],
            difficulty=difficulty,
            explanation=q_data["explanation"],
            hints=[
                "Think about the job each word does in the sentence",
                "Remember the definitions of different parts of speech"
            ]
        )
    
    def _generate_punctuation_question(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate punctuation questions"""
        if grade_level <= 3:
            punct_questions = [
                {
                    "question": "Which sentence is written correctly?",
                    "answer": "My name is Sarah.",
                    "options": ["My name is Sarah.", "my name is sarah", "My name is Sarah", "my Name is Sarah."],
                    "explanation": "Sentences start with a capital letter and end with a period."
                },
                {
                    "question": "What punctuation mark goes at the end of this sentence: 'What is your name'",
                    "answer": "question mark (?)",
                    "options": ["question mark (?)", "period (.)", "exclamation point (!)", "comma (,)"],
                    "explanation": "Questions end with a question mark because they ask something."
                }
            ]
        else:
            punct_questions = [
                {
                    "question": "Which sentence uses commas correctly?",
                    "answer": "I bought apples, oranges, and bananas.",
                    "options": ["I bought apples, oranges, and bananas.", "I bought apples oranges and bananas.", "I bought, apples oranges and bananas.", "I bought apples, oranges and, bananas."],
                    "explanation": "Use commas to separate items in a list, including before 'and' (Oxford comma)."
                },
                {
                    "question": "Where should the apostrophe go in: 'The dogs bone was buried'?",
                    "answer": "dog's (The dog's bone was buried)",
                    "options": ["dog's (The dog's bone was buried)", "dogs' (The dogs' bone was buried)", "bone's (The dogs bone's was buried)", "No apostrophe needed"],
                    "explanation": "Use an apostrophe before 's' to show that one dog owns the bone."
                }
            ]
        
        q_data = random.choice(punct_questions)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.WRITING,
            content=q_data["question"],
            correct_answer=q_data["answer"],
            options=q_data["options"],
            difficulty=difficulty,
            explanation=q_data["explanation"],
            hints=[
                "Think about the rules for each punctuation mark",
                "Read the sentence aloud to hear where pauses should go"
            ]
        )
    
    def _generate_sentence_question(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate sentence structure questions"""
        if grade_level <= 3:
            sentence_questions = [
                {
                    "question": "Which group of words is a complete sentence?",
                    "answer": "The bird flew away.",
                    "options": ["The bird flew away.", "The bird in the tree.", "Flew away quickly.", "Very beautiful bird."],
                    "explanation": "A complete sentence has a subject (the bird) and a verb (flew) and expresses a complete thought."
                },
                {
                    "question": "What is missing from this sentence: 'The cat under the table'?",
                    "answer": "a verb (action word)",
                    "options": ["a verb (action word)", "a noun (naming word)", "a period", "an adjective"],
                    "explanation": "This sentence has a subject (the cat) but no verb to tell us what the cat is doing."
                }
            ]
        else:
            sentence_questions = [
                {
                    "question": "Which sentence is a compound sentence?",
                    "answer": "I wanted to go to the park, but it was raining.",
                    "options": ["I wanted to go to the park, but it was raining.", "Because it was raining, I stayed home.", "I stayed home and read a book.", "The rain stopped, and the sun came out."],
                    "explanation": "A compound sentence joins two complete thoughts with a conjunction like 'but'."
                },
                {
                    "question": "What type of sentence is this: 'Although she was tired, Maria finished her homework'?",
                    "answer": "complex sentence",
                    "options": ["complex sentence", "compound sentence", "simple sentence", "run-on sentence"],
                    "explanation": "A complex sentence has one independent clause and one dependent clause (starting with 'Although')."
                }
            ]
        
        q_data = random.choice(sentence_questions)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.WRITING,
            content=q_data["question"],
            correct_answer=q_data["answer"],
            options=q_data["options"],
            difficulty=difficulty,
            explanation=q_data["explanation"],
            hints=[
                "Look for subjects and verbs in each part",
                "Think about how the parts of the sentence connect"
            ]
        )
    
    def _generate_structure_question(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate questions about writing structure"""
        if grade_level <= 4:
            structure_questions = [
                {
                    "question": "What should come first in a paragraph?",
                    "answer": "topic sentence",
                    "options": ["topic sentence", "conclusion", "details", "transition"],
                    "explanation": "A topic sentence tells the reader what the paragraph will be about."
                },
                {
                    "question": "What is the purpose of a conclusion in a story?",
                    "answer": "to wrap up the story and show how it ends",
                    "options": ["to wrap up the story and show how it ends", "to introduce new characters", "to start the action", "to describe the setting"],
                    "explanation": "A conclusion brings the story to an end and shows what happens to the characters."
                }
            ]
        else:
            structure_questions = [
                {
                    "question": "In a five-paragraph essay, what goes in the first paragraph?",
                    "answer": "introduction with thesis statement",
                    "options": ["introduction with thesis statement", "first body paragraph", "conclusion", "transition paragraph"],
                    "explanation": "The first paragraph introduces the topic and includes a thesis statement that tells the main idea."
                },
                {
                    "question": "What is the purpose of transition words in writing?",
                    "answer": "to connect ideas and help writing flow smoothly",
                    "options": ["to connect ideas and help writing flow smoothly", "to make sentences longer", "to add more details", "to replace punctuation"],
                    "explanation": "Transition words like 'however', 'therefore', and 'in addition' help connect ideas and make writing easier to follow."
                }
            ]
        
        q_data = random.choice(structure_questions)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.WRITING,
            content=q_data["question"],
            correct_answer=q_data["answer"],
            options=q_data["options"],
            difficulty=difficulty,
            explanation=q_data["explanation"],
            hints=[
                "Think about how good writing is organized",
                "Consider what readers need to understand your ideas"
            ]
        )
    
    def _generate_spelling_question(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate spelling questions"""
        if grade_level <= 3:
            spelling_questions = [
                {
                    "question": "Which word is spelled correctly?",
                    "answer": "friend",
                    "options": ["friend", "freind", "frend", "friand"],
                    "explanation": "The correct spelling is 'friend' - remember 'i before e except after c'."
                },
                {
                    "question": "How do you spell the plural of 'cat'?",
                    "answer": "cats",
                    "options": ["cats", "cates", "cat's", "caties"],
                    "explanation": "To make most nouns plural, just add 's'. The plural of cat is cats."
                }
            ]
        else:
            spelling_questions = [
                {
                    "question": "Which word is spelled correctly?",
                    "answer": "necessary",
                    "options": ["necessary", "neccessary", "necesary", "neccesary"],
                    "explanation": "The correct spelling is 'necessary' - one 'c' and two 's' letters."
                },
                {
                    "question": "Which word follows the 'i before e except after c' rule?",
                    "answer": "believe",
                    "options": ["believe", "receive", "weird", "height"],
                    "explanation": "'Believe' follows the rule with 'i before e'. 'Receive' has 'e before i' after 'c'."
                }
            ]
        
        q_data = random.choice(spelling_questions)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.WRITING,
            content=q_data["question"],
            correct_answer=q_data["answer"],
            options=q_data["options"],
            difficulty=difficulty,
            explanation=q_data["explanation"],
            hints=[
                "Sound out the word and think about spelling patterns",
                "Remember common spelling rules and exceptions"
            ]
        )
    
    def _generate_creative_writing_question(self, grade_level: int, difficulty: DifficultyLevel) -> Question:
        """Generate creative writing questions"""
        if grade_level <= 4:
            creative_questions = [
                {
                    "question": "What makes a story interesting to read?",
                    "answer": "characters, setting, and an exciting plot",
                    "options": ["characters, setting, and an exciting plot", "only long sentences", "lots of big words", "many pages"],
                    "explanation": "Good stories have interesting characters, a clear setting, and a plot that keeps readers wanting to know what happens next."
                },
                {
                    "question": "When writing a personal narrative, you should:",
                    "answer": "write about something that happened to you",
                    "options": ["write about something that happened to you", "make up a completely fictional story", "only write about other people", "copy someone else's story"],
                    "explanation": "A personal narrative tells about a real experience from your own life."
                }
            ]
        else:
            creative_questions = [
                {
                    "question": "What is 'show, don't tell' in creative writing?",
                    "answer": "use descriptive details instead of just stating facts",
                    "options": ["use descriptive details instead of just stating facts", "include pictures with your writing", "only write dialogue", "make your writing very short"],
                    "explanation": "Instead of writing 'She was sad,' show it: 'Tears rolled down her cheeks as she stared at the empty room.'"
                },
                {
                    "question": "What is the climax of a story?",
                    "answer": "the most exciting or important moment",
                    "options": ["the most exciting or important moment", "the beginning of the story", "the end of the story", "the setting description"],
                    "explanation": "The climax is the turning point or most intense moment in a story, where the main conflict reaches its peak."
                }
            ]
        
        q_data = random.choice(creative_questions)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.WRITING,
            content=q_data["question"],
            correct_answer=q_data["answer"],
            options=q_data["options"],
            difficulty=difficulty,
            explanation=q_data["explanation"],
            hints=[
                "Think about what makes you want to keep reading a story",
                "Consider the elements that make writing come alive"
            ]
        )
    
    def _generate_general_writing_question(self, grade_level: int, topic: str, difficulty: DifficultyLevel) -> Question:
        """Generate general writing questions"""
        general_questions = [
            {
                "question": "What should you do before you start writing?",
                "answer": "plan your ideas",
                "options": ["plan your ideas", "write as fast as possible", "worry about spelling", "count how many words you need"],
                "explanation": "Planning helps you organize your thoughts and makes your writing clearer and more focused."
            },
            {
                "question": "Why is it important to revise your writing?",
                "answer": "to make your ideas clearer and fix mistakes",
                "options": ["to make your ideas clearer and fix mistakes", "to make it longer", "to use bigger words", "to change the topic"],
                "explanation": "Revising helps you improve your writing by making your ideas clearer, fixing errors, and making sure it makes sense."
            },
            {
                "question": "What is a rough draft?",
                "answer": "your first attempt at writing something",
                "options": ["your first attempt at writing something", "the final version", "a writing assignment", "a type of pencil"],
                "explanation": "A rough draft is your first try at writing something. It doesn't have to be perfect - you can improve it later."
            }
        ]
        
        q_data = random.choice(general_questions)
        
        return Question(
            id=str(uuid.uuid4()),
            subject=Subject.WRITING,
            content=q_data["question"],
            correct_answer=q_data["answer"],
            options=q_data["options"],
            difficulty=difficulty,
            explanation=q_data["explanation"],
            hints=[
                "Think about the writing process from start to finish",
                "Consider what helps make writing better"
            ]
        )