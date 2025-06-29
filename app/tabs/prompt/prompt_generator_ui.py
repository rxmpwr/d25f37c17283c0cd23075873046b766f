"""
UI components for AI suggestions and analysis display
"""

import customtkinter as ctk
from typing import Dict, Callable

# Fix import paths
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# Safe imports with fallbacks
try:
    from utils.ui_components import UIColors, UIFonts, create_action_button
except ImportError:
    # Define fallbacks
    class UIColors:
        PRIMARY = "#2196F3"
        SUCCESS = "#4CAF50"
        WARNING = "#FF9800"
        ERROR = "#F44336"
        WHITE = "#FFFFFF"
        TEXT_PRIMARY = "#2B2B2B"
        TEXT_SECONDARY = "#666666"
        BACKGROUND = "#F5F5F5"
        LIGHT_GRAY = "#E0E0E0"
    
    class UIFonts:
        @staticmethod
        def get_body():
            return ctk.CTkFont(size=13)
        @staticmethod
        def get_subheading():
            return ctk.CTkFont(size=16, weight="bold")
    
    def create_action_button(parent, text, command, button_type="primary", **kwargs):
        color_map = {
            "primary": UIColors.PRIMARY,
            "success": UIColors.SUCCESS,
            "warning": UIColors.WARNING,
            "error": UIColors.ERROR
        }
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            fg_color=color_map.get(button_type, UIColors.PRIMARY),
            **kwargs
        )


class PromptGeneratorUI:
    """Handles AI suggestions UI and user interactions."""
    
    def __init__(self, parent: ctk.CTkFrame, 
                 ai_analyzer,
                 run_analysis_callback: Callable,
                 apply_suggestions_callback: Callable):
        self.parent = parent
        self.ai_analyzer = ai_analyzer
        self.run_analysis = run_analysis_callback
        self.apply_suggestions = apply_suggestions_callback
        
        self.suggestions_frame = None
        self.analyze_button = None
        
        self.setup_ui()
        
    def setup_ui(self) -> None:
        """Setup AI suggestions panel."""
        suggestions_frame = ctk.CTkFrame(
            self.parent, 
            fg_color=UIColors.WHITE, 
            corner_radius=10
        )
        suggestions_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        suggestions_frame.grid_rowconfigure(2, weight=1)
        suggestions_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        header_label = ctk.CTkLabel(
            suggestions_frame,
            text="🔍 AI Smart Suggestions",
            font=UIFonts.get_subheading(),
            text_color=UIColors.TEXT_PRIMARY
        )
        header_label.grid(row=0, column=0, pady=(15, 10), padx=15, sticky="w")
        
        # Analyze button
        self.analyze_button = create_action_button(
            suggestions_frame,
            text="🧠 Analyze & Suggest",
            command=self.run_analysis,
            button_type="primary",
            width=200,
            height=40
        )
        self.analyze_button.grid(row=1, column=0, pady=10, padx=15)
        self.analyze_button.configure(state="disabled")
        
        # Suggestions content
        self.suggestions_scroll = ctk.CTkScrollableFrame(
            suggestions_frame,
            fg_color="transparent",
            scrollbar_fg_color=UIColors.LIGHT_GRAY
        )
        self.suggestions_scroll.grid(row=2, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.suggestions_scroll.grid_columnconfigure(0, weight=1)
        
        # Initial placeholder
        self._show_placeholder()
        
    def _show_placeholder(self) -> None:
        """Show placeholder when no suggestions available."""
        placeholder = ctk.CTkFrame(
            self.suggestions_scroll, 
            fg_color=UIColors.BACKGROUND, 
            corner_radius=8
        )
        placeholder.grid(row=0, column=0, sticky="ew", pady=10)
        
        placeholder_label = ctk.CTkLabel(
            placeholder,
            text="🤖 AI Waiting for Analysis\n\nComplete YouTube analysis\nand click 'Analyze & Suggest'",
            font=UIFonts.get_body(),
            text_color=UIColors.TEXT_SECONDARY,
            justify="center"
        )
        placeholder_label.pack(pady=20)
        
    def enable_analysis(self) -> None:
        """Enable analysis button when data is ready."""
        self.analyze_button.configure(state="normal")
        
    def display_suggestions(self, suggestions: Dict) -> None:
        """Display AI suggestions in UI."""
        # Clear existing
        for widget in self.suggestions_scroll.winfo_children():
            widget.destroy()
            
        # Display each suggestion category
        row = 0
        
        if 'audience_analysis' in suggestions:
            self._create_suggestion_card(
                row, "👥 Audience Intelligence",
                suggestions['audience_analysis']
            )
            row += 1
            
        if 'tone_detection' in suggestions:
            self._create_suggestion_card(
                row, "🎵 Optimal Tone",
                suggestions['tone_detection']
            )
            row += 1
            
        if 'content_suggestions' in suggestions:
            self._create_suggestion_card(
                row, "📋 Content Types",
                suggestions['content_suggestions']
            )
            row += 1
            
        if 'viral_factors' in suggestions:
            self._create_suggestion_card(
                row, "🚀 Viral Potential",
                suggestions['viral_factors']
            )
            row += 1
            
    def _create_suggestion_card(self, row: int, title: str, data: Dict) -> None:
        """Create a suggestion card."""
        card = ctk.CTkFrame(
            self.suggestions_scroll, 
            fg_color=UIColors.WHITE, 
            corner_radius=8
        )
        card.grid(row=row, column=0, sticky="ew", pady=8)
        card.grid_columnconfigure(0, weight=1)
        
        # Header with confidence
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))
        header_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=UIColors.TEXT_PRIMARY
        )
        title_label.grid(row=0, column=0, sticky="w")
        
        # Confidence score
        confidence = data.get('confidence_score', 0)
        confidence_color = (UIColors.SUCCESS if confidence > 70 else 
                          UIColors.WARNING if confidence > 40 else 
                          UIColors.ERROR)
        
        confidence_label = ctk.CTkLabel(
            header_frame,
            text=f"{confidence:.0f}% confident",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=confidence_color
        )
        confidence_label.grid(row=0, column=1, sticky="e")
        
        # Content based on data type
        self._add_card_content(card, data)
        
    def _add_card_content(self, card: ctk.CTkFrame, data: Dict) -> None:
        """Add content to suggestion card based on data type."""
        content_text = ""
        
        if 'primary_demographics' in data:
            content_text = f"Primary: {data['primary_demographics']}"
        elif 'recommended_tone' in data:
            content_text = data['recommended_tone']
        elif 'recommended_types' in data:
            types = data['recommended_types']
            content_text = ', '.join(types[:2]) if types else 'No recommendations'
        elif 'viral_score' in data:
            content_text = f"Score: {data['viral_score']:.1f}/100"
            
        # Add reasoning if available
        if data.get('reasoning'):
            content_text += f"\n{data['reasoning'][:100]}..."
            
        content_label = ctk.CTkLabel(
            card,
            text=content_text,
            font=UIFonts.get_body(),
            text_color=UIColors.TEXT_SECONDARY,
            wraplength=300,
            justify="left"
        )
        content_label.grid(row=1, column=0, sticky="ew", padx=15, pady=(5, 15))