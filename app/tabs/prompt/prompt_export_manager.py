"""
Export functionality for generated prompts
"""

import json
import os
from typing import Dict, Optional
from datetime import datetime
from tkinter import filedialog, messagebox

import customtkinter as ctk
from utils.ui_components import UIColors, UIFonts, create_action_button

# Fix import paths
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))


class PromptExportManager:
    """Handles prompt export functionality."""
    
    def auto_save_prompts(self, prompts: Dict) -> None:
        """Auto-save prompts to default location."""
        try:
            os.makedirs("output/prompts", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output/prompts/auto_save_{timestamp}.json"
            
            self._export_json(prompts, filename, include_all=True)
            print(f"Auto-saved prompts to: {filename}")
            
        except Exception as e:
            print(f"Auto-save failed: {e}")
            
    def show_export_dialog(self, parent: ctk.CTk, prompts: Dict) -> None:
        """Show export options dialog."""
        dialog = ExportDialog(parent, prompts, self)
        dialog.show()
        
    def export_prompts(self, prompts: Dict, format: str, 
                      filename: str, options: Dict) -> bool:
        """Export prompts in specified format."""
        try:
            if format == 'json':
                self._export_json(prompts, filename, **options)
            elif format == 'txt':
                self._export_txt(prompts, filename, **options)
            elif format == 'md':
                self._export_markdown(prompts, filename, **options)
            else:
                raise ValueError(f"Unsupported format: {format}")
                
            return True
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
            return False
            
    def _export_json(self, prompts: Dict, filename: str, 
                    include_analytics: bool = True,
                    include_variables: bool = True,
                    include_all: bool = False,
                    **kwargs) -> None:
        """Export prompts to JSON format."""
        export_data = {
            'metadata': {
                'export_date': datetime.now().isoformat(),
                'version': '2.0',
                'total_prompts': len(prompts)
            },
            'prompts': {}
        }
        
        # Calculate overall metrics
        if include_analytics:
            quality_scores = [p.get('quality_score', 50) for p in prompts.values()]
            viral_scores = [p.get('viral_potential', 40) for p in prompts.values()]
            
            export_data['metadata']['avg_quality_score'] = sum(quality_scores) / len(quality_scores)
            export_data['metadata']['avg_viral_potential'] = sum(viral_scores) / len(viral_scores)
            
        # Add prompts
        for key, prompt_data in prompts.items():
            export_entry = {
                'name': prompt_data['name'],
                'description': prompt_data['description'],
                'prompt': prompt_data['prompt'],
                'created_at': prompt_data.get('created_at', datetime.now().isoformat())
            }
            
            if include_analytics:
                export_entry['quality_score'] = prompt_data.get('quality_score', 50)
                export_entry['viral_potential'] = prompt_data.get('viral_potential', 40)
                
            if include_variables and 'variables' in prompt_data:
                export_entry['variables'] = prompt_data['variables']
                
            export_data['prompts'][key] = export_entry
            
        # Write file
        os.makedirs(os.path.dirname(filename), exist_ok=True) if os.path.dirname(filename) else None
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)
            
    def _export_txt(self, prompts: Dict, filename: str, **kwargs) -> None:
        """Export prompts as plain text."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("GENERATED AI PROMPTS\n")
            f.write("=" * 50 + "\n\n")
            
            for key, prompt_data in prompts.items():
                f.write(f"{prompt_data['name']}\n")
                f.write("-" * len(prompt_data['name']) + "\n")
                f.write(f"Description: {prompt_data['description']}\n\n")
                f.write(f"Prompt:\n{prompt_data['prompt']}\n\n")
                f.write("=" * 50 + "\n\n")
                
    def _export_markdown(self, prompts: Dict, filename: str, 
                        include_toc: bool = True, **kwargs) -> None:
        """Export prompts as Markdown."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Generated AI Prompts\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Table of contents
            if include_toc:
                f.write("## Table of Contents\n\n")
                for i, (key, prompt_data) in enumerate(prompts.items(), 1):
                    f.write(f"{i}. [{prompt_data['name']}](#{key})\n")
                f.write("\n---\n\n")
                
            # Prompts
            for key, prompt_data in prompts.items():
                f.write(f"## {prompt_data['name']} {{#{key}}}\n\n")
                f.write(f"**Description:** {prompt_data['description']}\n\n")
                
                if 'quality_score' in prompt_data:
                    f.write(f"**Quality Score:** {prompt_data['quality_score']}% | ")
                    f.write(f"**Viral Potential:** {prompt_data.get('viral_potential', 0)}%\n\n")
                    
                f.write("### Prompt\n\n")
                f.write(f"```\n{prompt_data['prompt']}\n```\n\n")
                f.write("---\n\n")


class ExportDialog:
    """Export options dialog."""
    
    def __init__(self, parent: ctk.CTk, prompts: Dict, export_manager):
        self.parent = parent
        self.prompts = prompts
        self.export_manager = export_manager
        self.result = None
        
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Export Prompts")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._center_dialog()
        self._setup_ui()
        
    def _center_dialog(self) -> None:
        """Center dialog on screen."""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - 250
        y = (self.dialog.winfo_screenheight() // 2) - 200
        self.dialog.geometry(f"500x400+{x}+{y}")
        
    def _setup_ui(self) -> None:
        """Setup dialog UI."""
        # Title
        title_label = ctk.CTkLabel(
            self.dialog,
            text="📤 Export Enhanced Prompts",
            font=UIFonts.get_subheading()
        )
        title_label.pack(pady=(20, 10))
        
        # Stats
        stats_frame = ctk.CTkFrame(self.dialog, fg_color=UIColors.BACKGROUND)
        stats_frame.pack(pady=10, padx=20, fill="x")
        
        quality_scores = [p.get('quality_score', 50) for p in self.prompts.values()]
        viral_scores = [p.get('viral_potential', 40) for p in self.prompts.values()]
        
        stats_text = (f"📊 {len(self.prompts)} prompts • "
                     f"Avg Quality: {sum(quality_scores)/len(quality_scores):.0f}% • "
                     f"Avg Viral: {sum(viral_scores)/len(viral_scores):.0f}%")
        
        stats_label = ctk.CTkLabel(stats_frame, text=stats_text, font=UIFonts.get_body())
        stats_label.pack(pady=10)
        
        # Format selection
        format_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        format_frame.pack(pady=10, fill="x", padx=20)
        
        format_label = ctk.CTkLabel(format_frame, text="Export Format:", font=UIFonts.get_body())
        format_label.pack(anchor="w")
        
        self.format_var = ctk.StringVar(value="json")
        
        formats = [
            ("json", "JSON (with analytics & metadata)"),
            ("txt", "Plain Text"),
            ("md", "Markdown")
        ]
        
        for value, text in formats:
            radio = ctk.CTkRadioButton(
                format_frame,
                text=text,
                variable=self.format_var,
                value=value,
                font=UIFonts.get_body()
            )
            radio.pack(anchor="w", pady=3)
            
        # Options
        options_frame = ctk.CTkFrame(self.dialog, fg_color=UIColors.BACKGROUND)
        options_frame.pack(pady=20, padx=20, fill="x")
        
        options_label = ctk.CTkLabel(options_frame, text="Include:", font=UIFonts.get_body())
        options_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.include_analytics = ctk.CTkCheckBox(
            options_frame,
            text="Quality & Viral Analytics",
            font=UIFonts.get_body()
        )
        self.include_analytics.pack(anchor="w", padx=10, pady=2)
        self.include_analytics.select()
        
        self.include_variables = ctk.CTkCheckBox(
            options_frame,
            text="Template Variables",
            font=UIFonts.get_body()
        )
        self.include_variables.pack(anchor="w", padx=10, pady=(2, 10))
        
        # Buttons
        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        button_frame.pack(pady=20)
        
        export_btn = create_action_button(
            button_frame,
            text="📤 Export",
            command=self._on_export,
            button_type="success"
        )
        export_btn.pack(side="left", padx=10)
        
        cancel_btn = create_action_button(
            button_frame,
            text="Cancel",
            command=self._on_cancel,
            button_type="gray"
        )
        cancel_btn.pack(side="left", padx=10)
        
    def _on_export(self) -> None:
        """Handle export button."""
        format = self.format_var.get()
        
        # Get filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"ai_enhanced_prompts_{timestamp}.{format}"
        
        filename = filedialog.asksaveasfilename(
            defaultextension=f".{format}",
            filetypes=[(f"{format.upper()} files", f"*.{format}"), ("All files", "*.*")],
            initialfile=default_filename
        )
        
        if filename:
            options = {
                'include_analytics': self.include_analytics.get(),
                'include_variables': self.include_variables.get()
            }
            
            success = self.export_manager.export_prompts(
                self.prompts, format, filename, options
            )
            
            if success:
                messagebox.showinfo("Success", f"Prompts exported to:\n{filename}")
                self.dialog.destroy()
                
    def _on_cancel(self) -> None:
        """Handle cancel button."""
        self.dialog.destroy()
        
    def show(self) -> None:
        """Show dialog and wait."""
        self.dialog.wait_window()