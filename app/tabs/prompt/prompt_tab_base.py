"""
Base class for Enhanced Prompt Tab Manager
Coordinates all prompt-related functionality
"""

import customtkinter as ctk
from typing import Dict, List, Optional, Callable
from datetime import datetime

# Fix import paths
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# Import các components trong cùng package
from .prompt_ai_analyzer import PromptAIAnalyzer
from .prompt_generator_ui import PromptGeneratorUI
from .prompt_export_manager import PromptExportManager
from .prompt_settings_panel import PromptSettingsPanel
from .prompt_results_panel import PromptResultsPanel

# Import từ utils
try:
    from utils.ui_components import UIColors, UIFonts, create_header_frame
except ImportError:
    print("Warning: Could not import ui_components")
    # Define fallback classes
    class UIColors:
        PRIMARY = "#2196F3"
        SUCCESS = "#4CAF50"
        WARNING = "#FF9800"
        WHITE = "#FFFFFF"
        TEXT_PRIMARY = "#2B2B2B"
        TEXT_SECONDARY = "#666666"
        BACKGROUND = "#F5F5F5"
    
    class UIFonts:
        @staticmethod
        def get_body():
            return ctk.CTkFont(size=13)
        
        @staticmethod
        def get_heading():
            return ctk.CTkFont(size=20, weight="bold")
        
        @staticmethod
        def get_subheading():
            return ctk.CTkFont(size=16, weight="bold")
    
    def create_header_frame(parent, title, subtitle=""):
        frame = ctk.CTkFrame(parent, fg_color=UIColors.WHITE, corner_radius=10)
        ctk.CTkLabel(frame, text=title, font=UIFonts.get_heading()).pack(pady=10)
        if subtitle:
            ctk.CTkLabel(frame, text=subtitle, font=UIFonts.get_body()).pack()
        return frame


class EnhancedPromptTabManager:
    """Enhanced prompt generation with AI smart suggestions."""
    
    def __init__(self, parent_frame: ctk.CTkFrame, 
                 prompt_generator,
                 get_analysis_data_callback: Callable,
                 set_prompts_callback: Callable):
        self.parent_frame = parent_frame
        self.prompt_generator = prompt_generator
        self.get_analysis_data = get_analysis_data_callback
        self.set_prompts = set_prompts_callback
        
        # Initialize components
        self.ai_analyzer = PromptAIAnalyzer()
        self.export_manager = PromptExportManager()
        
        # Tab frame
        self.tab_frame: Optional[ctk.CTkFrame] = None
        self.is_visible = False
        
        # Current state
        self.current_prompts: Dict = {}
        self.user_preferences: Dict = self._load_default_preferences()
        self.ai_suggestions: Dict = {}
        self.analysis_ready = False
        self.analysis_data: Optional[Dict] = None
        
        # UI components
        self.settings_panel: Optional[PromptSettingsPanel] = None
        self.results_panel: Optional[PromptResultsPanel] = None
        self.generator_ui: Optional[PromptGeneratorUI] = None
        
        # Setup UI
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self) -> None:
        """Setup the enhanced prompt tab interface."""
        # Main tab frame
        self.tab_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        
        # Configure grid
        self.tab_frame.grid_rowconfigure(1, weight=1)
        self.tab_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        self._setup_header()
        
        # Main content with 3 columns
        self._setup_main_content()
        
        # Initially hidden
        self.hide()
        
    def _setup_header(self) -> None:
        """Setup enhanced header section."""
        header = create_header_frame(
            self.tab_frame,
            "🧠 AI-Powered Prompt Generation",
            "Intelligent prompt creation with data-driven suggestions and optimization"
        )
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 0))
        
        # Add status label
        self.status_label = ctk.CTkLabel(
            header,
            text="⚠️ Waiting for analysis data...",
            font=UIFonts.get_body(),
            text_color=UIColors.WARNING
        )
        self.status_label.grid(row=2, column=0, pady=10, sticky="w")
        
    def _setup_main_content(self) -> None:
        """Setup main 3-column layout."""
        main_container = ctk.CTkFrame(self.tab_frame, fg_color="transparent")
        main_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1, minsize=350)
        main_container.grid_columnconfigure(1, weight=1, minsize=350)
        main_container.grid_columnconfigure(2, weight=2, minsize=500)
        
        # Initialize UI components
        self.generator_ui = PromptGeneratorUI(
            main_container,
            self.ai_analyzer,
            self.run_ai_analysis,
            self.apply_ai_suggestions
        )
        
        self.settings_panel = PromptSettingsPanel(
            main_container,
            self.user_preferences,
            self.generate_enhanced_prompts
        )
        
        self.results_panel = PromptResultsPanel(
            main_container,
            self.export_manager,
            self.copy_prompt_to_clipboard
        )
        
    def run_ai_analysis(self) -> None:
        """Run AI analysis on YouTube data."""
        if not self.analysis_ready:
            from tkinter import messagebox
            messagebox.showwarning("No Data", "Please complete YouTube analysis first.")
            return
            
        analysis_data = self.get_analysis_data()
        if not analysis_data:
            from tkinter import messagebox
            messagebox.showerror("Error", "No analysis data available.")
            return
            
        # Delegate to AI analyzer
        self.ai_analyzer.analyze_data(
            analysis_data,
            self._on_ai_analysis_complete
        )
        
    def _on_ai_analysis_complete(self, suggestions: Dict) -> None:
        """Handle AI analysis completion."""
        self.ai_suggestions = suggestions
        self.generator_ui.display_suggestions(suggestions)
        self.settings_panel.enable_apply_suggestions()
        
    def apply_ai_suggestions(self) -> None:
        """Apply AI suggestions to settings."""
        if not self.ai_suggestions:
            from tkinter import messagebox
            messagebox.showwarning("No Suggestions", "Run AI analysis first.")
            return
            
        # Update preferences from AI suggestions
        updated_prefs = self.ai_analyzer.apply_suggestions_to_preferences(
            self.ai_suggestions,
            self.user_preferences
        )
        
        self.user_preferences.update(updated_prefs)
        self.settings_panel.update_from_preferences(self.user_preferences)
        
        from tkinter import messagebox
        messagebox.showinfo("Applied", "AI suggestions have been applied!")
        
    def generate_enhanced_prompts(self) -> None:
        """Generate enhanced prompts with AI intelligence."""
        if not self.analysis_ready:
            from tkinter import messagebox
            messagebox.showwarning("No Data", "Please complete YouTube analysis first.")
            return
            
        # Get current preferences from settings panel
        self.user_preferences = self.settings_panel.get_current_preferences()
        
        # Include AI suggestions
        if self.ai_suggestions:
            self.user_preferences['ai_suggestions'] = self.ai_suggestions
            
        # Generate prompts
        analysis_data = self.get_analysis_data()
        
        def generate_task():
            prompts = self.prompt_generator.generate_prompts_from_analysis(
                analysis_data,
                self.user_preferences
            )
            
            # Add quality scoring
            for key, prompt_data in prompts.items():
                prompt_data['quality_score'] = self.ai_analyzer.calculate_prompt_quality(
                    prompt_data, analysis_data
                )
                prompt_data['viral_potential'] = self.ai_analyzer.calculate_viral_potential(
                    prompt_data, analysis_data
                )
                
            return prompts
            
        # Show loading and generate
        from utils.ui_components import show_loading_dialog
        show_loading_dialog(
            self.tab_frame,
            "Generating Enhanced Prompts",
            "Creating AI-optimized prompts...",
            generate_task,
            self._on_prompts_generated
        )
        
    def _on_prompts_generated(self, prompts: Dict) -> None:
        """Handle prompts generation completion."""
        self.current_prompts = prompts
        self.set_prompts(prompts)
        self.results_panel.display_prompts(prompts)
        
        # Auto-save if enabled
        if self.user_preferences.get('auto_save', True):
            self.export_manager.auto_save_prompts(prompts)
            
    def copy_prompt_to_clipboard(self, prompt_text: str) -> None:
        """Copy prompt text to clipboard."""
        try:
            self.tab_frame.clipboard_clear()
            self.tab_frame.clipboard_append(prompt_text)
            
            from tkinter import messagebox
            word_count = len(prompt_text.split())
            messagebox.showinfo(
                "Copied!",
                f"Prompt copied to clipboard!\n\nStats: {word_count:,} words"
            )
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Failed to copy: {str(e)}")
            
    def on_analysis_ready(self) -> None:
        """Called when analysis data is ready."""
        self.analysis_ready = True
        self.analysis_data = self.get_analysis_data()
        
        self.status_label.configure(
            text="✅ Analysis data ready - Run AI analysis for suggestions",
            text_color=UIColors.SUCCESS
        )
        
        self.generator_ui.enable_analysis()
        self.settings_panel.enable_generation()
        
    def save_settings(self) -> None:
        """Save current settings."""
        self.settings_panel.save_settings()
        
    def load_settings(self) -> None:
        """Load saved settings."""
        self.settings_panel.load_settings()
        
    def _load_default_preferences(self) -> Dict:
        """Load default preferences."""
        return {
            'viral_story': True,
            'video_script': True,
            'content_series': True,
            'social_viral': True,
            'email_nurture': True,
            'seo_blog': True,
            'primary_audience': 'Auto-detect from data',
            'content_style': 'Data-driven optimal',
            'engagement_target': 'Maximum viral potential',
            'length_strategy': 'AI-optimized',
            'emotional_tone': 'Analysis-driven',
            'complexity_level': 'Adaptive',
            'cta_style': 'High-conversion optimized',
            'ai_creativity': 'Balanced',
            'data_influence': 'Heavy data-driven',
            'include_trends': True,
            'personalization': 'Maximum',
            'auto_save': True,
            'framework': "Hero's Journey",
            'min_words': 2000,
            'video_duration': 10,
            'series_length': 7
        }
        
    def show(self) -> None:
        """Show the enhanced tab."""
        self.tab_frame.grid(row=0, column=0, sticky="nsew")
        self.is_visible = True
        
    def hide(self) -> None:
        """Hide the enhanced tab."""
        self.tab_frame.grid_remove()
        self.is_visible = False


# Alias for backward compatibility
PromptTabManager = EnhancedPromptTabManager