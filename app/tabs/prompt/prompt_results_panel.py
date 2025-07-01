"""
Results panel for displaying generated prompts
"""

import customtkinter as ctk
from typing import Dict, List, Callable
from tkinter import messagebox

# Fix import paths
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# Safe imports with fallbacks
try:
    from utils.ui_components import UIColors, UIFonts, create_action_button, create_metric_display
except ImportError:
    # Define fallbacks
    class UIColors:
        PRIMARY = "#2196F3"
        SUCCESS = "#4CAF50"
        WARNING = "#FF9800"
        ERROR = "#F44336"
        GRAY = "#757575"
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
        @staticmethod
        def get_small():
            return ctk.CTkFont(size=11)
        @staticmethod
        def get_code():
            return ctk.CTkFont(size=12, family="Consolas")
    
    def create_action_button(parent, text, command, button_type="primary", **kwargs):
        color_map = {
            "primary": UIColors.PRIMARY,
            "success": UIColors.SUCCESS,
            "warning": UIColors.WARNING,
            "error": UIColors.ERROR,
            "gray": UIColors.GRAY
        }
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            fg_color=color_map.get(button_type, UIColors.PRIMARY),
            **kwargs
        )
    
    def create_metric_display(parent, metrics):
        frame = ctk.CTkFrame(parent, fg_color=UIColors.WHITE, corner_radius=10)
        for i, (label, value) in enumerate(metrics.items()):
            metric_frame = ctk.CTkFrame(frame, fg_color=UIColors.BACKGROUND)
            metric_frame.grid(row=0, column=i, padx=10, pady=10)
            
            value_label = ctk.CTkLabel(
                metric_frame,
                text=value,
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color=UIColors.PRIMARY
            )
            value_label.pack(pady=(10, 5))
            
            label_label = ctk.CTkLabel(
                metric_frame,
                text=label,
                font=UIFonts.get_small(),
                text_color=UIColors.TEXT_SECONDARY
            )
            label_label.pack(pady=(0, 10))
        return frame


class PromptResultsPanel:
    """Manages prompt results display and interactions."""
    
    def __init__(self, parent: ctk.CTkFrame,
                 export_manager,
                 copy_callback: Callable):
        self.parent = parent
        self.export_manager = export_manager
        self.copy_callback = copy_callback
        
        self.current_prompts = {}
        self.prompt_tabs = {}
        self.prompt_contents = {}
        self.active_tab = None
        
        self.setup_ui()
        
    def setup_ui(self) -> None:
        """Setup results panel UI."""
        results_frame = ctk.CTkFrame(
            self.parent,
            fg_color=UIColors.WHITE,
            corner_radius=10
        )
        results_frame.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        results_frame.grid_rowconfigure(1, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        self._setup_header(results_frame)
        
        # Prompt display area
        self._setup_prompt_display(results_frame)
        
    def _setup_header(self, parent: ctk.CTkFrame) -> None:
        """Setup results header."""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 0))
        header.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(
            header,
            text="📝 Generated Prompts & Analytics",
            font=UIFonts.get_subheading(),
            text_color=UIColors.TEXT_PRIMARY
        )
        title_label.grid(row=0, column=0, sticky="w")
        
        # Metrics row
        metrics_frame = ctk.CTkFrame(header, fg_color="transparent")
        metrics_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        metrics_frame.grid_columnconfigure(2, weight=1)
        
        self.quality_label = ctk.CTkLabel(
            metrics_frame,
            text="Quality Score: --",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=UIColors.PRIMARY
        )
        self.quality_label.grid(row=0, column=0, sticky="w")
        
        self.viral_label = ctk.CTkLabel(
            metrics_frame,
            text="Viral Potential: --",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=UIColors.SUCCESS
        )
        self.viral_label.grid(row=0, column=1, sticky="w", padx=(20, 0))
        
        self.export_button = create_action_button(
            metrics_frame,
            text="📤 Export Suite",
            command=self._export_prompts,
            button_type="success",
            width=120,
            height=35
        )
        self.export_button.grid(row=0, column=3, sticky="e")
        self.export_button.configure(state="disabled")
        
    def _setup_prompt_display(self, parent: ctk.CTkFrame) -> None:
        """Setup prompt display area."""
        self.display_frame = ctk.CTkFrame(
            parent,
            fg_color=UIColors.BACKGROUND,
            corner_radius=8
        )
        self.display_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.display_frame.grid_rowconfigure(1, weight=1)
        self.display_frame.grid_columnconfigure(0, weight=1)
        
        # Tab buttons
        self.tabs_frame = ctk.CTkFrame(
            self.display_frame,
            fg_color=UIColors.WHITE,
            corner_radius=6
        )
        self.tabs_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        # Content area
        self.content_frame = ctk.CTkFrame(
            self.display_frame,
            fg_color="transparent"
        )
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Show placeholder
        self._show_placeholder()
        
    def _show_placeholder(self) -> None:
        """Show placeholder when no prompts."""
        placeholder = ctk.CTkFrame(
            self.content_frame,
            fg_color=UIColors.WHITE,
            corner_radius=8
        )
        placeholder.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        placeholder_label = ctk.CTkLabel(
            placeholder,
            text="🎯 AI-Enhanced Prompt Generation\n\nGenerated prompts will appear here",
            font=UIFonts.get_body(),
            text_color=UIColors.TEXT_SECONDARY,
            justify="center"
        )
        placeholder_label.pack(pady=50)
        
    def display_prompts(self, prompts: Dict) -> None:
        """Display generated prompts."""
        self.current_prompts = prompts
        
        # Clear existing
        for widget in self.tabs_frame.winfo_children():
            widget.destroy()
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        if not prompts:
            self._show_placeholder()
            return
            
        # Create tab buttons
        self.prompt_tabs = {}
        for i, (key, prompt_data) in enumerate(prompts.items()):
            quality = prompt_data.get('quality_score', 50)
            
            btn = ctk.CTkButton(
                self.tabs_frame,
                text=f"{prompt_data['name']} ({quality}%)",
                command=lambda k=key: self._show_prompt_tab(k),
                fg_color="transparent",
                text_color=self._get_quality_color(quality),
                hover_color=UIColors.LIGHT_GRAY,
                corner_radius=5,
                height=40,
                width=180
            )
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.prompt_tabs[key] = btn
            
        # Create content areas
        self.prompt_contents = {}
        for key, prompt_data in prompts.items():
            content = self._create_prompt_content(prompt_data)
            self.prompt_contents[key] = content
            
        # Show first tab
        if prompts:
            first_key = list(prompts.keys())[0]
            self._show_prompt_tab(first_key)
            
        # Update metrics
        self._update_metrics(prompts)
        
        # Enable export
        self.export_button.configure(state="normal")
        
    def _create_prompt_content(self, prompt_data: Dict) -> ctk.CTkFrame:
        """Create content frame for a prompt."""
        content = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)
        
        # Scrollable textbox
        textbox = ctk.CTkTextbox(
            content,
            font=UIFonts.get_code(),
            wrap="word"
        )
        textbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        textbox.insert("1.0", prompt_data['prompt'])
        textbox.configure(state="disabled")
        
        # Action buttons
        button_frame = ctk.CTkFrame(content, fg_color="transparent")
        button_frame.grid(row=1, column=0, pady=10)
        
        copy_btn = create_action_button(
            button_frame,
            text="📋 Copy",
            command=lambda: self.copy_callback(prompt_data['prompt']),
            button_type="primary",
            width=100,
            height=35
        )
        copy_btn.pack(side="left", padx=5)
        
        # Add analytics if available
        if 'quality_score' in prompt_data:
            analytics = {
                'Chất lượng': f"{prompt_data['quality_score']}%",
                'Viral': f"{prompt_data.get('viral_potential', 0)}%",
                'Words': str(len(prompt_data['prompt'].split()))
            }
            
            metrics_display = create_metric_display(content, analytics)
            metrics_display.grid(row=2, column=0, pady=(0, 10))
            
        return content
        
    def _show_prompt_tab(self, tab_key: str) -> None:
        """Show specific prompt tab."""
        # Update button styles
        for key, btn in self.prompt_tabs.items():
            if key == tab_key:
                btn.configure(
                    fg_color=UIColors.PRIMARY,
                    text_color=UIColors.WHITE
                )
            else:
                quality = self.current_prompts[key].get('quality_score', 50)
                btn.configure(
                    fg_color="transparent",
                    text_color=self._get_quality_color(quality)
                )
                
        # Hide all contents
        for content in self.prompt_contents.values():
            content.grid_remove()
            
        # Show selected
        if tab_key in self.prompt_contents:
            self.prompt_contents[tab_key].grid(row=0, column=0, sticky="nsew")
            
        self.active_tab = tab_key
        
    def _get_quality_color(self, quality: int) -> str:
        """Get color based on quality score."""
        if quality > 80:
            return UIColors.SUCCESS
        elif quality > 60:
            return UIColors.WARNING
        else:
            return UIColors.GRAY
            
    def _update_metrics(self, prompts: Dict) -> None:
        """Update overall metrics display."""
        if not prompts:
            return
            
        # Calculate averages
        quality_scores = [p.get('quality_score', 50) for p in prompts.values()]
        viral_scores = [p.get('viral_potential', 40) for p in prompts.values()]
        
        avg_quality = sum(quality_scores) / len(quality_scores)
        avg_viral = sum(viral_scores) / len(viral_scores)
        
        # Update labels
        self.quality_label.configure(text=f"Avg Quality: {avg_quality:.0f}%")
        self.viral_label.configure(text=f"Avg Viral: {avg_viral:.0f}%")
        
        # Update colors
        self.quality_label.configure(text_color=self._get_quality_color(avg_quality))
        self.viral_label.configure(text_color=self._get_quality_color(avg_viral))
        
    def _export_prompts(self) -> None:
        """Export prompts using export manager."""
        if not self.current_prompts:
            messagebox.showwarning("No Prompts", "No prompts to export.")
            return
            
        # Show export dialog
        self.export_manager.show_export_dialog(
            self.parent,
            self.current_prompts
        )