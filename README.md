# Teacher AI 🤖🎓

An intelligent AI-powered educational assistant designed to help students learn and grow through personalized tutoring, adaptive difficulty, and engaging study modes.

## Features ✨

### 🎯 **Multiple Study Modes**
- **Quiz Mode**: Test knowledge with auto-generated questions
- **Practice Mode**: Continuous practice with immediate feedback
- **Explanation Mode**: Interactive concept learning and Q&A
- **Review Mode**: Revisit previously learned topics
- **Conversation Mode**: Free-form chat with the AI teacher

### 📚 **Subject Coverage**
- **Mathematics**: Addition, subtraction, multiplication, division, fractions, algebra, geometry
- **Science**: Animals, plants, weather, space, human body, physics, chemistry
- **Reading**: Phonics, vocabulary, comprehension, main ideas, character analysis
- **Writing**: Grammar, punctuation, sentence structure, essays, creative writing

### 🎮 **Adaptive Learning**
- **Personalized Difficulty**: AI adjusts question difficulty based on performance
- **Progress Tracking**: Detailed analytics on learning progress and mastery
- **Achievement System**: Motivational badges and milestones
- **Smart Recommendations**: Personalized study suggestions

### 📊 **Progress Analytics**
- Track performance across subjects and topics
- View learning trends and improvements
- Identify areas needing review
- Export progress data

## Quick Start 🚀

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd teacher-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   STUDENT_NAME=Your Son's Name
   GRADE_LEVEL=5
   PREFERRED_SUBJECTS=math,science,reading
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## Usage Guide 📖

### First Time Setup
1. Enter your child's name and grade level
2. Select preferred subjects
3. The AI teacher will initialize and create a personalized learning profile

### Study Modes

#### 🎯 Quiz Mode
- Take structured quizzes with 5-10 questions
- Get immediate feedback on each answer
- Receive a final score and completion message
- Questions adapt to your grade level and performance

#### 💪 Practice Mode
- Work through problems one at a time
- Get detailed explanations for each answer
- Continue practicing as long as you want
- Perfect for building confidence in specific topics

#### 💡 Explanation Mode
- Learn new concepts through interactive explanations
- Ask follow-up questions about any topic
- Get age-appropriate explanations with examples
- Great for understanding "why" behind concepts

#### 📚 Review Mode
- Revisit topics you've studied before
- Focus on areas that need improvement
- Get personalized recommendations for what to review
- Strengthen your foundation in key concepts

#### 💬 Conversation Mode
- Chat freely with your AI teacher
- Ask questions about homework
- Explore topics you're curious about
- Get help with specific problems

### Progress Tracking
- View detailed statistics on your learning journey
- See which topics you've mastered
- Get recommendations for what to study next
- Track your improvement over time

## Architecture 🏗️

```
teacher-ai/
├── main.py                 # Main application entry point
├── config.py              # Configuration management
├── models.py              # Data models and structures
├── ai_teacher.py          # Core AI teacher logic
├── study_modes.py         # Study mode implementations
├── progress_tracker.py    # Progress tracking and analytics
├── subjects/              # Subject-specific modules
│   ├── __init__.py
│   ├── base_module.py     # Base class for subjects
│   ├── math_module.py     # Math problems and topics
│   ├── science_module.py  # Science questions
│   ├── reading_module.py  # Reading comprehension
│   └── writing_module.py  # Writing and grammar
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

### Key Components

- **AITeacher**: Core AI agent that handles conversations and question generation
- **StudyModeManager**: Manages different study modes and their interactions
- **ProgressTracker**: Tracks learning progress and provides analytics
- **Subject Modules**: Generate grade-appropriate questions for each subject

## Configuration ⚙️

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `STUDENT_NAME`: Default student name
- `GRADE_LEVEL`: Default grade level (1-12)
- `PREFERRED_SUBJECTS`: Comma-separated list of preferred subjects
- `DEBUG`: Enable debug mode (True/False)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, WARNING, ERROR)

### Customization
- Modify `config.py` to adjust default settings
- Add new subjects by creating modules in the `subjects/` directory
- Extend study modes by modifying `study_modes.py`

## Educational Philosophy 🎓

Teacher AI is built on proven educational principles:

### **Adaptive Learning**
- Questions adjust to the student's skill level
- Difficulty increases as mastery improves
- Struggling students get additional support

### **Immediate Feedback**
- Students learn from mistakes right away
- Positive reinforcement for correct answers
- Explanations help build understanding

### **Personalized Learning**
- Content adapts to individual progress
- Recommendations based on learning patterns
- Multiple subjects and difficulty levels

### **Engagement & Motivation**
- Achievement system with badges and milestones
- Encouraging, age-appropriate feedback
- Variety in question types and study modes

## Grade Level Coverage 📊

### Elementary (Grades 1-5)
- **Math**: Basic arithmetic, word problems, fractions, geometry basics
- **Science**: Animals, plants, weather, simple machines, human body
- **Reading**: Phonics, sight words, comprehension, vocabulary
- **Writing**: Letters, sentences, paragraphs, basic grammar

### Middle School (Grades 6-8)
- **Math**: Advanced arithmetic, pre-algebra, geometry, statistics
- **Science**: Earth science, life science, physical science, scientific method
- **Reading**: Literary analysis, advanced vocabulary, research skills
- **Writing**: Essays, research papers, advanced grammar, creative writing

## Contributing 🤝

We welcome contributions! Here are some ways you can help:

1. **Add New Subjects**: Create modules for history, geography, foreign languages
2. **Improve Question Generation**: Enhance the AI's ability to create varied questions
3. **Add Study Modes**: Implement new ways for students to learn
4. **Enhance UI**: Improve the command-line interface or add a web interface
5. **Better Analytics**: Add more detailed progress tracking and insights

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Troubleshooting 🔧

### Common Issues

**"OPENAI_API_KEY is required" error**
- Make sure you've set your OpenAI API key in the `.env` file
- Verify the key is correct and has sufficient credits

**Module import errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're using Python 3.8 or higher

**Progress not saving**
- Check file permissions in the project directory
- Look for error messages in the `teacher_ai.log` file

**Questions seem too easy/hard**
- The system adapts over time - try completing a few sessions
- You can manually select difficulty levels in each study mode

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Support 💬

If you encounter issues or have questions:
1. Check the troubleshooting section above
2. Look through existing GitHub issues
3. Create a new issue with detailed information about your problem

## Roadmap 🗺️

Future enhancements planned:
- [ ] Web-based interface
- [ ] Mobile app
- [ ] Voice interaction
- [ ] Multiplayer study sessions
- [ ] Teacher dashboard for parents/educators
- [ ] Integration with school curricula
- [ ] Offline mode
- [ ] Multi-language support

---

**Happy Learning! 🎉**

Teacher AI is designed to make learning fun, engaging, and effective. Whether your child needs help with homework, wants to get ahead, or just loves to learn, Teacher AI is here to help them succeed!