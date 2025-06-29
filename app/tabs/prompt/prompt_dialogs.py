"""
Dialog windows for prompt editing and configuration
"""

import customtkinter as ctk
from typing import Dict, Optional

from utils.ui_components import UIColors, UIFonts, create_action_button
# Fix import paths
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

class PromptEditorDialog:
    """Dialog for editing prompts with advanced features."""
    
    def __init__(self, parent: ctk.CTk, prompt_data: Dict):
        self.parent = parent
        self.prompt_data = prompt_data
        self.result = None
        
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title(f"Edit: {prompt_data['name']}")
        self.dialog.geometry("900x700")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._center_dialog()
        self._setup_ui()
        
    def _center_dialog(self) -> None:
        """Center dialog on screen."""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - 450
        y = (self.dialog.winfo_screenheight() // 2) - 350
        self.dialog.geometry(f"900x700+{x}+{y}")
        
    def _setup_ui(self) -> None:
        """Setup editor UI."""
        # Header
        header = ctk.CTkLabel(
            self.dialog,
            text=f"✏️ Editing: {self.prompt_data['name']}",
            font=UIFonts.get_subheading()
        )
        header.pack(pady=(20, 10))
        
        # Editor frame
        editor_frame = ctk.CTkFrame(self.dialog)
        editor_frame.pack(fill="both", expand=True, padx=20, pady=10)
        editor_frame.grid_rowconfigure(1, weight=1)
        editor_frame.grid_columnconfigure(0, weight=1)
        
        # Toolbar
        toolbar = ctk.CTkFrame(editor_frame, fg_color=UIColors.LIGHT_GRAY, height=50)
        toolbar.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        self.word_count_label = ctk.CTkLabel(
            toolbar, 
            text="Words: 0", 
            font=UIFonts.get_small()
        )
        self.word_count_label.pack(side="left", padx=10, pady=10)
        
        # Text editor
        self.text_editor = ctk.CTkTextbox(
            editor_frame,
            font=UIFonts.get_code(),
            wrap="word"
        )
        self.text_editor.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.text_editor.insert("1.0", self.prompt_data['prompt'])
        
        # Bind events
        self.text_editor.bind('<KeyRelease>', self._update_word_count)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        button_frame.pack(pady=20)
        
        save_btn = create_action_button(
            button_frame,
            text="💾 Save Changes",
            command=self._on_save,
            button_type="success"
        )
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = create_action_button(
            button_frame,
            text="❌ Cancel",
            command=self._on_cancel,
            button_type="gray"
        )
        cancel_btn.pack(side="left", padx=10)
        
        # Initial word count
        self._update_word_count()
        
    def _update_word_count(self, event=None) -> None:
        """Update word count display."""
        content = self.text_editor.get("1.0", "end-1c")
        word_count = len(content.split())
        self.word_count_label.configure(text=f"Words: {word_count:,}")
        
    def _on_save(self) -> None:
        """Handle save button."""
        self.result = self.text_editor.get("1.0", "end-1c")
        self.dialog.destroy()
        
    def _on_cancel(self) -> None:
        """Handle cancel button."""
        self.result = None
        self.dialog.destroy()
        
    def get_result(self) -> Optional[str]:
        """Get editor result."""
        self.dialog.wait_window()
        return self.result