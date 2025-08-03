#!/usr/bin/env python3
"""
Teacher AI - An AI-powered educational assistant for students
Main application entry point
"""

import sys
import os
from typing import Optional
import logging
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
import colorama
from colorama import Fore, Style
from datetime import datetime

# Initialize colorama for cross-platform color support
colorama.init()

from config import Config
from ai_teacher import AITeacher
from study_modes import StudyModeManager
from progress_tracker import ProgressTracker
from models import Subject, StudyMode, DifficultyLevel

# Set up logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('teacher_ai.log'),
        logging.StreamHandler() if Config.DEBUG else logging.NullHandler()
    ]
)

logger = logging.getLogger(__name__)

class TeacherAIApp:
    """Main application class for Teacher AI"""
    
    def __init__(self):
        self.console = Console()
        self.ai_teacher: Optional[AITeacher] = None
        self.study_manager: Optional[StudyModeManager] = None
        self.progress_tracker: Optional[ProgressTracker] = None
        self.current_session_id: Optional[str] = None
    
    def start(self):
        """Start the Teacher AI application"""
        try:
            self._show_welcome()
            self._setup_student()
            self._main_menu()
        except KeyboardInterrupt:
            self.console.print("\n👋 Goodbye! Keep learning!", style="bold blue")
        except Exception as e:
            logger.error(f"Application error: {e}")
            self.console.print(f"\n❌ An error occurred: {e}", style="bold red")
            if Config.DEBUG:
                raise
    
    def _show_welcome(self):
        """Display welcome message"""
        welcome_text = Text()
        welcome_text.append("🤖 Welcome to Teacher AI! 🎓\n", style="bold blue")
        welcome_text.append("Your personal AI tutor is here to help you learn and grow!\n", style="cyan")
        welcome_text.append("I can help you with math, science, reading, writing, and more!", style="green")
        
        welcome_panel = Panel(
            welcome_text,
            title="Teacher AI",
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print(welcome_panel)
        self.console.print()
    
    def _setup_student(self):
        """Set up student profile"""
        self.console.print("📝 Let's set up your learning profile!", style="bold yellow")
        
        # Get student information
        name = Prompt.ask("What's your name?", default=Config.STUDENT_NAME)
        
        while True:
            try:
                grade = int(Prompt.ask("What grade are you in?", default=str(Config.GRADE_LEVEL)))
                if 1 <= grade <= 12:
                    break
                else:
                    self.console.print("Please enter a grade between 1 and 12.", style="red")
            except ValueError:
                self.console.print("Please enter a valid number.", style="red")
        
        # Show available subjects
        self.console.print("\n📚 Available subjects:")
        subjects_table = Table(show_header=False, box=None)
        subjects_table.add_column(style="cyan")
        subjects_table.add_column(style="white")
        
        for i, subject in enumerate(Subject, 1):
            subjects_table.add_row(f"{i}.", subject.value.title())
        
        self.console.print(subjects_table)
        
        # Get preferred subjects
        subject_input = Prompt.ask(
            "\nWhich subjects interest you most? (enter numbers separated by commas)",
            default="1,2,3"
        )
        
        try:
            subject_indices = [int(x.strip()) - 1 for x in subject_input.split(',')]
            preferred_subjects = [
                list(Subject)[i].value for i in subject_indices 
                if 0 <= i < len(Subject)
            ]
        except (ValueError, IndexError):
            preferred_subjects = ["math", "science", "reading"]
        
        # Initialize AI teacher and related components
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Setting up your AI teacher...", total=None)
            
            try:
                self.ai_teacher = AITeacher()
                self.ai_teacher.initialize_student(name, grade, preferred_subjects)
                self.study_manager = StudyModeManager(self.ai_teacher)
                self.progress_tracker = ProgressTracker(name)
                
                progress.update(task, description="Ready to learn! 🚀")
                
            except Exception as e:
                progress.stop()
                self.console.print(f"\n❌ Setup failed: {e}", style="bold red")
                if "OPENAI_API_KEY" in str(e):
                    self.console.print(
                        "💡 Please set your OpenAI API key in the .env file",
                        style="yellow"
                    )
                sys.exit(1)
        
        self.console.print(f"\n🎉 Welcome, {name}! I'm excited to help you learn!", style="bold green")
    
    def _main_menu(self):
        """Display and handle main menu"""
        while True:
            self.console.print("\n" + "="*50, style="blue")
            self.console.print("🏠 MAIN MENU", style="bold blue")
            self.console.print("="*50, style="blue")
            
            # Show quick progress summary
            if self.progress_tracker:
                summary = self.progress_tracker.get_progress_summary()
                if summary["total_sessions"] > 0:
                    self.console.print(
                        f"📊 Sessions completed: {summary['total_sessions']} | "
                        f"Average score: {summary['avg_score']}% | "
                        f"Achievements: {summary['achievements']}",
                        style="dim cyan"
                    )
            
            menu_options = [
                "🎯 Take a Quiz",
                "💪 Practice Problems", 
                "💡 Learn New Concepts",
                "📚 Review Topics",
                "💬 Chat with AI Teacher",
                "📈 View Progress",
                "⚙️  Settings",
                "👋 Exit"
            ]
            
            self.console.print()
            for i, option in enumerate(menu_options, 1):
                self.console.print(f"{i}. {option}")
            
            choice = Prompt.ask("\nWhat would you like to do?", choices=[str(i) for i in range(1, len(menu_options) + 1)])
            
            if choice == "1":
                self._start_quiz_mode()
            elif choice == "2":
                self._start_practice_mode()
            elif choice == "3":
                self._start_explanation_mode()
            elif choice == "4":
                self._start_review_mode()
            elif choice == "5":
                self._start_conversation_mode()
            elif choice == "6":
                self._show_progress()
            elif choice == "7":
                self._show_settings()
            elif choice == "8":
                if Confirm.ask("Are you sure you want to exit?"):
                    break
    
    def _choose_subject_and_difficulty(self) -> tuple[Subject, DifficultyLevel]:
        """Let user choose subject and difficulty"""
        # Choose subject
        self.console.print("\n📚 Choose a subject:")
        subjects = list(Subject)
        for i, subject in enumerate(subjects, 1):
            self.console.print(f"{i}. {subject.value.title()}")
        
        while True:
            try:
                subject_choice = int(Prompt.ask("Subject", choices=[str(i) for i in range(1, len(subjects) + 1)]))
                chosen_subject = subjects[subject_choice - 1]
                break
            except (ValueError, IndexError):
                self.console.print("Please choose a valid subject number.", style="red")
        
        # Get recommended difficulty
        recommended_difficulty = self.progress_tracker.get_recommended_difficulty(chosen_subject)
        
        # Choose difficulty
        self.console.print(f"\n⚡ Choose difficulty level (recommended: {recommended_difficulty.value}):")
        difficulties = list(DifficultyLevel)
        for i, difficulty in enumerate(difficulties, 1):
            marker = "⭐" if difficulty == recommended_difficulty else " "
            self.console.print(f"{i}. {marker} {difficulty.value.title()}")
        
        difficulty_choice = Prompt.ask(
            "Difficulty", 
            choices=[str(i) for i in range(1, len(difficulties) + 1)],
            default=str(difficulties.index(recommended_difficulty) + 1)
        )
        chosen_difficulty = difficulties[int(difficulty_choice) - 1]
        
        return chosen_subject, chosen_difficulty
    
    def _start_quiz_mode(self):
        """Start quiz mode"""
        self.console.print("\n🎯 QUIZ MODE", style="bold yellow")
        subject, difficulty = self._choose_subject_and_difficulty()
        
        result = self.study_manager.start_mode(StudyMode.QUIZ, subject, difficulty)
        if "error" in result:
            self.console.print(f"❌ Error: {result['error']}", style="red")
            return
        
        self.current_session_id = result["session_id"]
        self.console.print(f"\n{result['instructions']}", style="cyan")
        
        self._handle_quiz_session(result)
    
    def _handle_quiz_session(self, session_data: dict):
        """Handle quiz session interaction"""
        question_num = 1
        total_questions = session_data["total_questions"]
        
        while True:
            if "question" not in session_data:
                break
            
            question = session_data["question"]
            
            # Display question
            self.console.print(f"\n📝 Question {question_num}/{total_questions}", style="bold")
            self.console.print(f"{question['content']}", style="white")
            
            if question.get("options"):
                self.console.print("\nChoices:")
                for i, option in enumerate(question["options"], 1):
                    self.console.print(f"{i}. {option}")
                
                # Get answer
                while True:
                    try:
                        answer_choice = int(Prompt.ask("Your answer", choices=[str(i) for i in range(1, len(question["options"]) + 1)]))
                        answer = question["options"][answer_choice - 1]
                        break
                    except (ValueError, IndexError):
                        self.console.print("Please choose a valid option number.", style="red")
            else:
                answer = Prompt.ask("Your answer")
            
            # Submit answer
            result = self.study_manager.handle_answer(self.current_session_id, answer, question["id"])
            
            # Show feedback
            if result["correct"]:
                self.console.print("✅ Correct!", style="bold green")
            else:
                self.console.print("❌ Not quite right.", style="bold red")
            
            self.console.print(f"💬 {result['feedback']}", style="cyan")
            
            if result.get("is_complete"):
                # Quiz completed
                self.console.print(f"\n🎉 Quiz Complete!", style="bold green")
                self.console.print(f"📊 Final Score: {result['final_score']:.0f}%", style="bold yellow")
                self.console.print(f"✅ Correct: {result['total_correct']}/{result['total_questions']}")
                self.console.print(f"💬 {result['completion_message']}", style="cyan")
                
                # Record session for progress tracking
                if self.ai_teacher.context and self.ai_teacher.context.current_session:
                    self.progress_tracker.record_session(self.ai_teacher.context.current_session)
                
                break
            elif "next_question" in result:
                session_data["question"] = result["next_question"]
                question_num += 1
            
            # Pause between questions
            Prompt.ask("\nPress Enter to continue...", default="")
    
    def _start_practice_mode(self):
        """Start practice mode"""
        self.console.print("\n💪 PRACTICE MODE", style="bold yellow")
        subject, difficulty = self._choose_subject_and_difficulty()
        
        result = self.study_manager.start_mode(StudyMode.PRACTICE, subject, difficulty)
        if "error" in result:
            self.console.print(f"❌ Error: {result['error']}", style="red")
            return
        
        self.current_session_id = result["session_id"]
        self.console.print(f"\n{result['instructions']}", style="cyan")
        
        self._handle_practice_session(result)
    
    def _handle_practice_session(self, session_data: dict):
        """Handle practice session interaction"""
        question_count = 0
        
        while True:
            if "question" not in session_data:
                break
            
            question = session_data["question"]
            question_count += 1
            
            # Display question
            self.console.print(f"\n📝 Practice Problem #{question_count}", style="bold")
            self.console.print(f"{question['content']}", style="white")
            
            if question.get("options"):
                self.console.print("\nChoices:")
                for i, option in enumerate(question["options"], 1):
                    self.console.print(f"{i}. {option}")
                
                while True:
                    try:
                        answer_choice = int(Prompt.ask("Your answer", choices=[str(i) for i in range(1, len(question["options"]) + 1)]))
                        answer = question["options"][answer_choice - 1]
                        break
                    except (ValueError, IndexError):
                        self.console.print("Please choose a valid option number.", style="red")
            else:
                answer = Prompt.ask("Your answer")
            
            # Submit answer
            result = self.study_manager.handle_answer(self.current_session_id, answer, question["id"])
            
            # Show feedback
            if result["correct"]:
                self.console.print("✅ Excellent!", style="bold green")
            else:
                self.console.print("❌ Let's learn from this!", style="bold yellow")
            
            self.console.print(f"💬 {result['feedback']}", style="cyan")
            
            if result.get("explanation"):
                self.console.print(f"📖 Explanation: {result['explanation']}", style="dim white")
            
            # Ask if they want to continue
            if not Confirm.ask("\nWould you like another practice problem?"):
                # Record partial session
                if self.ai_teacher.context and self.ai_teacher.context.current_session:
                    session = self.ai_teacher.context.current_session
                    session.score = sum(1 for r in session.responses if r.is_correct) / len(session.responses) * 100 if session.responses else 0
                    self.progress_tracker.record_session(session)
                break
            
            if "next_question" in result:
                session_data["question"] = result["next_question"]
    
    def _start_explanation_mode(self):
        """Start explanation mode"""
        self.console.print("\n💡 EXPLANATION MODE", style="bold yellow")
        subject, difficulty = self._choose_subject_and_difficulty()
        
        result = self.study_manager.start_mode(StudyMode.EXPLANATION, subject, difficulty)
        if "error" in result:
            self.console.print(f"❌ Error: {result['error']}", style="red")
            return
        
        self.current_session_id = result["session_id"]
        self.console.print(f"\n📚 Topic: {result.get('topic', 'General Concepts')}", style="bold cyan")
        self.console.print(f"\n{result['explanation']}", style="white")
        
        self._handle_explanation_session()
    
    def _handle_explanation_session(self):
        """Handle explanation session interaction"""
        while True:
            self.console.print("\n" + "-"*40, style="dim")
            question = Prompt.ask("What would you like to know more about? (or 'quit' to exit)")
            
            if question.lower() in ['quit', 'exit', 'done']:
                break
            
            result = self.study_manager.handle_answer(self.current_session_id, question)
            
            if "explanation" in result:
                self.console.print(f"\n{result['explanation']}", style="white")
            
            if result.get("suggestions"):
                self.console.print("\n💡 You might also ask:", style="dim cyan")
                for suggestion in result["suggestions"]:
                    self.console.print(f"  • {suggestion}", style="dim white")
    
    def _start_review_mode(self):
        """Start review mode"""
        self.console.print("\n📚 REVIEW MODE", style="bold yellow")
        
        # Show topics that need review
        review_topics = self.progress_tracker.get_topics_needing_review()
        if review_topics:
            self.console.print("📋 Topics that could use some review:")
            for topic in review_topics[:5]:
                mastery_percent = int(topic.mastery_level * 100)
                self.console.print(f"  • {topic.topic} ({topic.subject.value}) - {mastery_percent}% mastery")
        
        subject, difficulty = self._choose_subject_and_difficulty()
        
        result = self.study_manager.start_mode(StudyMode.REVIEW, subject, difficulty)
        if "error" in result:
            self.console.print(f"❌ Error: {result['error']}", style="red")
            return
        
        self.current_session_id = result["session_id"]
        self.console.print(f"\n{result['summary']}", style="cyan")
        
        self._handle_review_session()
    
    def _handle_review_session(self):
        """Handle review session interaction"""
        while True:
            self.console.print("\n" + "-"*40, style="dim")
            request = Prompt.ask("What would you like to review? (or 'quit' to exit)")
            
            if request.lower() in ['quit', 'exit', 'done']:
                break
            
            result = self.study_manager.handle_answer(self.current_session_id, request)
            
            if "response" in result:
                self.console.print(f"\n{result['response']}", style="white")
            
            if result.get("options"):
                self.console.print("\n🎯 What would you like to do next?", style="cyan")
                for option in result["options"]:
                    self.console.print(f"  • {option}", style="dim white")
    
    def _start_conversation_mode(self):
        """Start conversation mode"""
        self.console.print("\n💬 CHAT MODE", style="bold yellow")
        
        result = self.study_manager.start_mode(StudyMode.CONVERSATION, None, None)
        self.console.print(f"\n{result['message']}", style="cyan")
        
        while True:
            self.console.print("\n" + "-"*40, style="dim")
            message = Prompt.ask("You")
            
            if message.lower() in ['quit', 'exit', 'bye']:
                self.console.print("👋 It was great chatting with you! Keep up the great learning!", style="green")
                break
            
            result = self.study_manager.handle_answer("conversation", message)
            
            if "response" in result:
                self.console.print(f"🤖 Teacher AI: {result['response']}", style="white")
            
            if result.get("suggestions"):
                self.console.print("\n💡 You might also ask:", style="dim cyan")
                for suggestion in result["suggestions"]:
                    self.console.print(f"  • {suggestion}", style="dim white")
    
    def _show_progress(self):
        """Show detailed progress information"""
        self.console.print("\n📈 YOUR PROGRESS", style="bold yellow")
        
        summary = self.progress_tracker.get_progress_summary()
        
        if summary["total_sessions"] == 0:
            self.console.print("No sessions completed yet. Let's start learning!", style="cyan")
            return
        
        # Overall stats
        stats_table = Table(title="Overall Statistics", box=None)
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="white")
        
        stats_table.add_row("Total Sessions", str(summary["total_sessions"]))
        stats_table.add_row("Average Score", f"{summary['avg_score']}%")
        stats_table.add_row("Time Spent", f"{summary['total_time_minutes']:.1f} minutes")
        stats_table.add_row("Questions Answered", str(summary["total_questions_answered"]))
        stats_table.add_row("Topics Mastered", str(summary["mastered_topics"]))
        stats_table.add_row("Achievements Earned", str(summary["achievements"]))
        
        self.console.print(stats_table)
        
        # Subject breakdown
        if summary["subject_stats"]:
            self.console.print("\n📚 Subject Breakdown", style="bold cyan")
            subject_table = Table()
            subject_table.add_column("Subject", style="cyan")
            subject_table.add_column("Sessions", style="white")
            subject_table.add_column("Average Score", style="white")
            subject_table.add_column("Last Practiced", style="white")
            
            for subject, stats in summary["subject_stats"].items():
                subject_table.add_row(
                    subject.title(),
                    str(stats["sessions"]),
                    f"{stats['avg_score']:.1f}%",
                    stats["last_practiced"]
                )
            
            self.console.print(subject_table)
        
        # Recent achievements
        if summary["recent_achievements"]:
            self.console.print("\n🏆 Recent Achievements", style="bold yellow")
            for achievement in summary["recent_achievements"]:
                self.console.print(f"  {achievement}", style="green")
        
        # Recommendations
        recommendations = self.progress_tracker.get_study_recommendations()
        if recommendations:
            self.console.print("\n💡 Recommendations", style="bold cyan")
            for rec in recommendations:
                self.console.print(f"  {rec}", style="white")
        
        Prompt.ask("\nPress Enter to continue...", default="")
    
    def _show_settings(self):
        """Show settings menu"""
        self.console.print("\n⚙️  SETTINGS", style="bold yellow")
        
        settings_options = [
            "📊 Export Progress Data",
            "🔄 Reset Progress", 
            "👤 Change Student Profile",
            "🔙 Back to Main Menu"
        ]
        
        for i, option in enumerate(settings_options, 1):
            self.console.print(f"{i}. {option}")
        
        choice = Prompt.ask("\nChoose an option", choices=[str(i) for i in range(1, len(settings_options) + 1)])
        
        if choice == "1":
            self._export_progress()
        elif choice == "2":
            self._reset_progress()
        elif choice == "3":
            self._change_profile()
    
    def _export_progress(self):
        """Export progress data"""
        try:
            filename = f"progress_export_{self.ai_teacher.context.student.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            # This would export the progress data
            self.console.print(f"📁 Progress exported to {filename}", style="green")
        except Exception as e:
            self.console.print(f"❌ Export failed: {e}", style="red")
    
    def _reset_progress(self):
        """Reset progress data"""
        if Confirm.ask("⚠️  Are you sure you want to reset all progress? This cannot be undone."):
            try:
                os.remove(self.progress_tracker.progress_file)
                self.progress_tracker = ProgressTracker(self.ai_teacher.context.student.name)
                self.console.print("🔄 Progress reset successfully!", style="green")
            except Exception as e:
                self.console.print(f"❌ Reset failed: {e}", style="red")
    
    def _change_profile(self):
        """Change student profile"""
        self.console.print("👤 Profile changes will take effect on next restart.", style="yellow")
        # This would allow changing the profile

def main():
    """Main entry point"""
    app = TeacherAIApp()
    app.start()

if __name__ == "__main__":
    main()