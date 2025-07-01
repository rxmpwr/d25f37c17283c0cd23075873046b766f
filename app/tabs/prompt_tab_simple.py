"""
Simple Prompt Tab Manager for fallback when enhanced version has issues
"""

import customtkinter as ctk
from typing import Dict, Optional, Callable
from tkinter import messagebox
import json
from datetime import datetime

class PromptTabManager:
    """Simple prompt generation tab."""
    
    def __init__(self, parent_frame: ctk.CTkFrame, 
                 prompt_generator,
                 get_analysis_data_callback: Callable,
                 set_prompts_callback: Callable):
        self.parent_frame = parent_frame
        self.prompt_generator = prompt_generator
        self.get_analysis_data = get_analysis_data_callback
        self.set_prompts = set_prompts_callback
        
        # State
        self.analysis_ready = False
        self.current_prompts = {}
        
        # Create tab
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the prompt tab interface."""
        # Main tab frame
        self.tab_frame = ctk.CTkFrame(self.parent_frame, fg_color="#F5F5F5")
        self.tab_frame.grid_rowconfigure(1, weight=1)
        self.tab_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        header_frame = ctk.CTkFrame(self.tab_frame, fg_color="white", corner_radius=10)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        ctk.CTkLabel(
            header_frame,
            text="🧠 AI-Powered Prompt Generation",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            header_frame,
            text="Generate optimized prompts based on YouTube analysis data",
            font=ctk.CTkFont(size=14),
            text_color="#666666"
        ).pack(pady=(0, 10))
        
        # Status
        self.status_label = ctk.CTkLabel(
            header_frame,
            text="⚠️ Waiting for analysis data...",
            font=ctk.CTkFont(size=14),
            text_color="#FF9800"
        )
        self.status_label.pack(pady=(0, 15))
        
        # Content area
        content_frame = ctk.CTkFrame(self.tab_frame, fg_color="white", corner_radius=10)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Settings
        settings_frame = ctk.CTkFrame(content_frame, fg_color="#F5F5F5", corner_radius=8)
        settings_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            settings_frame,
            text="⚙️ Prompt Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        # Template checkboxes
        self.template_vars = {}
        templates = [
            ("story_generation", "📖 Viral Story"),
            ("video_script", "🎬 Video Script"),
            ("content_series", "📺 Content Series"),
            ("social_media", "📱 Social Media"),
            ("email_sequence", "📧 Email Sequence"),
            ("blog_content", "📝 Blog Content")
        ]
        
        checkbox_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        checkbox_frame.pack(pady=10)
        
        for key, label in templates:
            var = ctk.BooleanVar(value=True)
            self.template_vars[key] = var
            
            checkbox = ctk.CTkCheckBox(
                checkbox_frame,
                text=label,
                variable=var,
                font=ctk.CTkFont(size=13)
            )
            checkbox.pack(anchor="w", pady=2, padx=20)
        
        # Generate button
        self.generate_btn = ctk.CTkButton(
            settings_frame,
            text="🚀 Generate Prompts",
            command=self.generate_prompts,
            width=200,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold"),
            state="disabled"
        )
        self.generate_btn.pack(pady=20)
        
        # Results
        results_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        results_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            results_frame,
            text="📝 Generated Prompts",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(0, 10))
        
        # Results textbox
        self.results_text = ctk.CTkTextbox(
            results_frame,
            font=ctk.CTkFont(size=13),
            wrap="word"
        )
        self.results_text.pack(fill="both", expand=True)
        
        # Export buttons
        export_frame = ctk.CTkFrame(results_frame, fg_color="transparent")
        export_frame.pack(pady=10)
        
        self.export_btn = ctk.CTkButton(
            export_frame,
            text="📥 Export",
            command=self.export_prompts,
            width=100,
            height=35,
            state="disabled"
        )
        self.export_btn.pack(side="left", padx=5)
        
        self.copy_btn = ctk.CTkButton(
            export_frame,
            text="📋 Copy",
            command=self.copy_prompts,
            width=100,
            height=35,
            state="disabled"
        )
        self.copy_btn.pack(side="left", padx=5)
        
        # Initially hidden
        self.hide()
        
    def on_analysis_ready(self):
        """Called when analysis data is ready."""
        self.analysis_ready = True
        self.status_label.configure(
            text="✅ Analysis data ready - You can now generate prompts!",
            text_color="#4CAF50"
        )
        self.generate_btn.configure(state="normal")
        
    def generate_prompts(self):
        """Generate prompts from analysis data."""
        if not self.analysis_ready:
            messagebox.showwarning("Không có dữ liệu", "Please complete YouTube analysis first!")
            return
            
        analysis_data = self.get_analysis_data()
        if not analysis_data:
            messagebox.showerror("Lỗi", "No analysis data available!")
            return
            
        try:
            # Show loading
            self.generate_btn.configure(text="🔄 Generating...", state="disabled")
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", "Generating AI-powered prompts...\n\nPlease wait...")
            
            # Update UI
            self.tab_frame.update()
            
            # Get preferences
            preferences = self._get_preferences()
            
            # Generate prompts
            if self.prompt_generator:
                prompts = self.prompt_generator.generate_prompts_from_analysis(
                    analysis_data, 
                    preferences
                )
            else:
                # Fallback demo prompts
                prompts = self._generate_demo_prompts(analysis_data, preferences)
            
            # Display results
            self.display_prompts(prompts)
            
            # Store prompts
            self.current_prompts = prompts
            self.set_prompts(prompts)
            
            # Enable export
            self.export_btn.configure(state="normal")
            self.copy_btn.configure(state="normal")
            
            # Reset button
            self.generate_btn.configure(text="🚀 Generate Prompts", state="normal")
            
            messagebox.showinfo("Thành Công", f"Generated {len(prompts)} prompts successfully!")
            
        except Exception as e:
            self.generate_btn.configure(text="🚀 Generate Prompts", state="normal")
            messagebox.showerror("Lỗi", f"Failed to generate prompts: {str(e)}")
            
    def _get_preferences(self):
        """Get current preferences."""
        prefs = {
            'min_words': 2000,
            'tone': 'Engaging and educational',
            'target_audience': 'Young adults 18-35',
            'framework': "Hero's Journey",
            'video_duration': 10,
            'series_length': 5,
            'frequency': 'Weekly',
            'content_format': 'Educational + Entertainment',
            'campaign_goal': 'Increase engagement and followers',
            'sequence_length': 7,
            'content_goals': 'Educate and inspire audience'
        }
        
        # Add template selections
        for key, var in self.template_vars.items():
            prefs[key] = var.get()
            
        return prefs
        
    def _generate_demo_prompts(self, analysis_data: Dict, preferences: Dict) -> Dict:
        """Generate demo prompts when generator not available."""
        prompts = {}
        
        if preferences.get('story_generation', True):
            prompts['story_generation'] = {
                'name': '📖 Viral Story Generation',
                'description': 'Create engaging stories based on YouTube insights',
                'prompt': """Create a viral story about relationships and psychology based on these insights:

Main Theme: Psychology of Relationships
Target Audience: Young adults 18-35
Tone: Engaging and educational

Requirements:
- Hook readers in the first paragraph
- Use storytelling techniques from top-performing videos
- Include psychological insights
- Create emotional connection
- End with a powerful call-to-action

Write a complete story of at least 2000 words.""",
                'created_at': datetime.now().isoformat()
            }
            
        if preferences.get('video_script', True):
            prompts['video_script'] = {
                'name': '🎬 YouTube Video Script',
                'description': 'Script optimized for retention and engagement',
                'prompt': """Create a 10-minute YouTube video script about relationship psychology.

Structure:
- Hook (0-15 seconds): Grab attention immediately
- Introduction (15-45 seconds): Set up the topic
- Main Content (45 seconds - 8 minutes): Core value delivery
- Climax (8-9 minutes): Key revelation or insight
- Conclusion (9-10 minutes): Summary and CTA

Include:
- Engaging transitions
- Visual cues
- Audience interaction prompts
- Clear value proposition""",
                'created_at': datetime.now().isoformat()
            }
            
        return prompts
        
    def display_prompts(self, prompts: Dict):
        """Display generated prompts."""
        self.results_text.delete("1.0", "end")
        
        result_text = "🎯 AI-GENERATED PROMPTS\n" + "="*60 + "\n\n"
        
        for i, (key, prompt_data) in enumerate(prompts.items(), 1):
            result_text += f"#{i}. {prompt_data['name']}\n"
            result_text += "-"*60 + "\n"
            result_text += f"📋 Description: {prompt_data['description']}\n\n"
            result_text += f"💡 Prompt:\n{prompt_data['prompt']}\n\n"
            result_text += "="*60 + "\n\n"
            
        self.results_text.insert("1.0", result_text)
        
    def export_prompts(self):
        """Export prompts to file."""
        if not self.current_prompts:
            messagebox.showwarning("Không có dữ liệu", "No prompts to export!")
            return
            
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"ai_prompts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.current_prompts, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Thành Công", f"Prompts exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Failed to export: {str(e)}")
                
    def copy_prompts(self):
        """Copy prompts to clipboard."""
        if not self.current_prompts:
            messagebox.showwarning("Không có dữ liệu", "No prompts to copy!")
            return
            
        try:
            all_text = self.results_text.get("1.0", "end-1c")
            self.tab_frame.clipboard_clear()
            self.tab_frame.clipboard_append(all_text)
            messagebox.showinfo("Thành công", "Prompts copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Failed to copy: {str(e)}")
        
    # Tab manager interface
    def show(self):
        """Show the tab."""
        self.tab_frame.grid(row=0, column=0, sticky="nsew")
        
    def hide(self):
        """Hide the tab."""
        self.tab_frame.grid_forget()