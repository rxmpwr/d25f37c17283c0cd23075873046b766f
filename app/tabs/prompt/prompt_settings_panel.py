"""
Settings panel widgets for prompt generation
"""

import customtkinter as ctk
from typing import Dict, List, Callable, Optional
import json
import os
from datetime import datetime

from utils.ui_components import UIColors, UIFonts, create_action_button
# Fix import paths
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

class PromptSettingsPanel:
    """Manages prompt generation settings and preferences."""
    
    def __init__(self, parent: ctk.CTkFrame, 
                 initial_preferences: Dict,
                 generate_callback: Callable):
        self.parent = parent
        self.preferences = initial_preferences.copy()
        self.generate_callback = generate_callback
        
        self.template_checkboxes = {}
        self.preference_widgets = {}
        self.generate_button = None
        self.apply_suggestions_btn = None
        
        self.setup_ui()
        
    def setup_ui(self) -> None:
        """Setup settings panel UI."""
        settings_frame = ctk.CTkFrame(
            self.parent, 
            fg_color=UIColors.WHITE, 
            corner_radius=10
        )
        settings_frame.grid(row=0, column=1, sticky="nsew", padx=10)
        settings_frame.grid_rowconfigure(2, weight=1)
        
        # Header
        header_label = ctk.CTkLabel(
            settings_frame,
            text="⚙️ Prompt Configuration",
            font=UIFonts.get_subheading(),
            text_color=UIColors.TEXT_PRIMARY
        )
        header_label.grid(row=0, column=0, pady=(15, 10), padx=15, sticky="w")
        
        # Apply suggestions button
        self.apply_suggestions_btn = create_action_button(
            settings_frame,
            text="✨ Apply AI Suggestions",
            command=lambda: None,  # Will be set by parent
            button_type="success",
            width=200,
            height=35
        )
        self.apply_suggestions_btn.grid(row=1, column=0, pady=5, padx=15)
        self.apply_suggestions_btn.configure(state="disabled")
        
        # Scrollable settings
        settings_scroll = ctk.CTkScrollableFrame(
            settings_frame,
            fg_color="transparent"
        )
        settings_scroll.grid(row=2, column=0, sticky="nsew", padx=15, pady=5)
        settings_scroll.grid_columnconfigure(0, weight=1)
        
        # Template selection
        self._setup_template_selection(settings_scroll)
        
        # Preference sections
        self._setup_audience_preferences(settings_scroll)
        self._setup_content_preferences(settings_scroll)
        self._setup_advanced_preferences(settings_scroll)
        
        # Action buttons
        self._setup_action_buttons(settings_frame)
        
    def _setup_template_selection(self, parent: ctk.CTkFrame) -> None:
        """Setup template selection section."""
        template_section = ctk.CTkFrame(
            parent, 
            fg_color=UIColors.BACKGROUND, 
            corner_radius=8
        )
        template_section.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        templates = {
            'viral_story': {
                'name': '📖 Viral Story Generation',
                'description': 'Hero\'s journey with psychological hooks'
            },
            'video_script': {
                'name': '🎬 Retention-Optimized Script',
                'description': 'Video scripts for maximum watch time'
            },
            'content_series': {
                'name': '📺 7-Episode Content Series',
                'description': 'Multi-part series with cliffhangers'
            },
            'social_viral': {
                'name': '📱 Multi-Platform Viral Package',
                'description': 'Optimized content for all platforms'
            },
            'email_nurture': {
                'name': '📧 7-Email Nurture Sequence',
                'description': 'Progressive email sequence'
            },
            'seo_blog': {
                'name': '📝 SEO Blog Masterpiece',
                'description': 'Search-optimized long-form content'
            }
        }
        
        for i, (key, info) in enumerate(templates.items()):
            self._create_template_checkbox(template_section, i+1, key, info)
            
    def _create_template_checkbox(self, parent: ctk.CTkFrame, row: int, 
                                 key: str, info: Dict) -> None:
        """Create a template checkbox with description."""
        container = ctk.CTkFrame(parent, fg_color="white", corner_radius=6)
        container.grid(row=row, column=0, sticky="ew", padx=15, pady=5)
        
        checkbox = ctk.CTkCheckBox(
            container,
            text=info['name'],
            font=UIFonts.get_body(),
            command=lambda: self._on_template_toggle(key)
        )
        checkbox.grid(row=0, column=0, sticky="w", padx=10, pady=8)
        
        if self.preferences.get(key, True):
            checkbox.select()
            
        self.template_checkboxes[key] = checkbox
        
        # Description
        desc_label = ctk.CTkLabel(
            container,
            text=info['description'],
            font=UIFonts.get_small(),
            text_color=UIColors.TEXT_SECONDARY
        )
        desc_label.grid(row=1, column=0, sticky="w", padx=(35, 10), pady=(0, 8))
        
    def _setup_audience_preferences(self, parent: ctk.CTkFrame) -> None:
        """Setup audience preferences section."""
        section = ctk.CTkFrame(parent, fg_color=UIColors.BACKGROUND, corner_radius=8)
        section.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        header = ctk.CTkLabel(
            section,
            text="👥 Audience Intelligence",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=UIColors.TEXT_PRIMARY
        )
        header.grid(row=0, column=0, columnspan=2, pady=(15, 10), padx=15, sticky="w")
        
        # Preference rows
        self._create_preference_row(
            section, 1, "Primary Audience", "combobox",
            ["Auto-detect from data", "Gen Z (13-24)", "Millennials (25-40)", 
             "Gen X (41-56)", "Custom mix"],
            "primary_audience", "Auto-detect from data"
        )
        
        self._create_preference_row(
            section, 2, "Content Style", "combobox",
            ["Data-driven optimal", "Educational focus", "Entertainment focus", 
             "Inspirational", "Controversial"],
            "content_style", "Data-driven optimal"
        )
        
    def _setup_content_preferences(self, parent: ctk.CTkFrame) -> None:
        """Setup content preferences section."""
        section = ctk.CTkFrame(parent, fg_color=UIColors.BACKGROUND, corner_radius=8)
        section.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        
        header = ctk.CTkLabel(
            section,
            text="📊 Content Optimization",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=UIColors.TEXT_PRIMARY
        )
        header.grid(row=0, column=0, columnspan=2, pady=(15, 10), padx=15, sticky="w")
        
        self._create_preference_row(
            section, 1, "Length Strategy", "combobox",
            ["AI-optimized", "Short-form focus", "Long-form focus", "Mixed"],
            "length_strategy", "AI-optimized"
        )
        
        self._create_preference_row(
            section, 2, "Emotional Tone", "combobox",
            ["Analysis-driven", "Inspiring", "Thought-provoking", "Educational"],
            "emotional_tone", "Analysis-driven"
        )
        
    def _setup_advanced_preferences(self, parent: ctk.CTkFrame) -> None:
        """Setup advanced preferences section."""
        section = ctk.CTkFrame(parent, fg_color=UIColors.BACKGROUND, corner_radius=8)
        section.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        
        header = ctk.CTkLabel(
            section,
            text="🔬 AI Enhancement Settings",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=UIColors.TEXT_PRIMARY
        )
        header.grid(row=0, column=0, columnspan=2, pady=(15, 10), padx=15, sticky="w")
        
        self._create_preference_row(
            section, 1, "AI Creativity", "combobox",
            ["Balanced", "Conservative", "Creative", "Highly innovative"],
            "ai_creativity", "Balanced"
        )
        
        self._create_preference_row(
            section, 2, "Auto-save", "checkbox",
            None, "auto_save", True
        )
        
    def _create_preference_row(self, parent: ctk.CTkFrame, row: int,
                             label_text: str, widget_type: str,
                             options: Optional[List[str]], key: str,
                             default_value) -> None:
        """Create a preference setting row."""
        label = ctk.CTkLabel(
            parent,
            text=f"{label_text}:",
            font=UIFonts.get_body(),
            text_color=UIColors.TEXT_PRIMARY
        )
        label.grid(row=row, column=0, sticky="w", padx=15, pady=8)
        
        if widget_type == "entry":
            widget = ctk.CTkEntry(parent, width=200)
            widget.insert(0, str(default_value))
        elif widget_type == "combobox":
            widget = ctk.CTkComboBox(parent, values=options or [], width=200)
            widget.set(default_value)
        elif widget_type == "checkbox":
            widget = ctk.CTkCheckBox(parent, text="")
            if default_value:
                widget.select()
        else:
            raise ValueError(f"Unsupported widget type: {widget_type}")
            
        widget.grid(row=row, column=1, sticky="w", padx=(10, 15), pady=8)
        self.preference_widgets[key] = widget
        
    def _setup_action_buttons(self, parent: ctk.CTkFrame) -> None:
        """Setup action buttons."""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.grid(row=3, column=0, sticky="ew", padx=15, pady=15)
        
        self.generate_button = create_action_button(
            button_frame,
            text="🚀 Generate Enhanced Prompts",
            command=self.generate_callback,
            button_type="primary",
            width=220,
            height=40
        )
        self.generate_button.pack(side="left", padx=(0, 10))
        self.generate_button.configure(state="disabled")
        
        save_btn = create_action_button(
            button_frame,
            text="💾 Save",
            command=self.save_settings,
            button_type="gray",
            width=80,
            height=40
        )
        save_btn.pack(side="left")
        
    def _on_template_toggle(self, template_key: str) -> None:
        """Handle template checkbox toggle."""
        checkbox = self.template_checkboxes[template_key]
        self.preferences[template_key] = checkbox.get()
        
    def get_current_preferences(self) -> Dict:
        """Get current preferences from UI."""
        # Update from checkboxes
        for key, checkbox in self.template_checkboxes.items():
            self.preferences[key] = checkbox.get()
            
        # Update from other widgets
        for key, widget in self.preference_widgets.items():
            if isinstance(widget, ctk.CTkEntry):
                value = widget.get()
                self.preferences[key] = int(value) if value.isdigit() else value
            elif isinstance(widget, ctk.CTkComboBox):
                self.preferences[key] = widget.get()
            elif isinstance(widget, ctk.CTkCheckBox):
                self.preferences[key] = widget.get()
                
        return self.preferences
        
    def update_from_preferences(self, preferences: Dict) -> None:
        """Update UI from preferences dict."""
        self.preferences = preferences.copy()
        
        # Update checkboxes
        for key, checkbox in self.template_checkboxes.items():
            if key in preferences:
                if preferences[key]:
                    checkbox.select()
                else:
                    checkbox.deselect()
                    
        # Update other widgets
        for key, widget in self.preference_widgets.items():
            if key in preferences:
                value = preferences[key]
                if isinstance(widget, ctk.CTkEntry):
                    widget.delete(0, "end")
                    widget.insert(0, str(value))
                elif isinstance(widget, ctk.CTkComboBox):
                    widget.set(value)
                elif isinstance(widget, ctk.CTkCheckBox):
                    if value:
                        widget.select()
                    else:
                        widget.deselect()
                        
    def enable_generation(self) -> None:
        """Enable generation button."""
        self.generate_button.configure(state="normal")
        
    def enable_apply_suggestions(self) -> None:
        """Enable apply suggestions button."""
        self.apply_suggestions_btn.configure(state="normal")
        
    def save_settings(self) -> None:
        """Save settings to file."""
        try:
            settings_data = {
                'preferences': self.get_current_preferences(),
                'last_updated': datetime.now().isoformat(),
                'version': '2.0'
            }
            
            os.makedirs("config", exist_ok=True)
            with open("config/prompt_settings.json", 'w', encoding='utf-8') as f:
                json.dump(settings_data, f, ensure_ascii=False, indent=2)
                
            from tkinter import messagebox
            messagebox.showinfo("Thành công", "Settings saved successfully!")
            
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Lỗi", f"Failed to save settings: {str(e)}")
            
    def load_settings(self) -> None:
        """Load settings from file."""
        try:
            if os.path.exists("config/prompt_settings.json"):
                with open("config/prompt_settings.json", 'r', encoding='utf-8') as f:
                    settings_data = json.load(f)
                    
                if 'preferences' in settings_data:
                    self.update_from_preferences(settings_data['preferences'])
                    
        except Exception as e:
            print(f"Failed to load settings: {e}")