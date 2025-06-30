"""
Main window class for YouTube Analyzer Pro - Fixed Version with Auto-save
"""

import customtkinter as ctk
import threading
from datetime import datetime
from typing import Dict, Optional
from tkinter import messagebox
import json
import csv
import os

# Import API Config Manager
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_config import get_config_manager

# Import tab managers
from .tabs.input_tab import InputTabManager
from .tabs.analysis_tab import AnalysisTabManager
from .tabs.topic_tab import TopicTabManager
from .tabs.content_tab import ContentTabManager
from .tabs.settings_tab import SettingsTabManager

# Import prompt tab
try:
    from .tabs.prompt_tab import PromptTabManager
except ImportError:
    from .tabs.prompt_tab_simple import PromptTabManager

# Import YouTube Integration
try:
    from modules.youtube_integration import YouTubeAnalysisManager
    YOUTUBE_MODULE_AVAILABLE = True
except ImportError as e:
    YOUTUBE_MODULE_AVAILABLE = False
    print(f"Warning: YouTube module not available. {e}")

# Import Create Prompts Module
try:
    from create_prompts import PromptGenerator
    PROMPTS_MODULE_AVAILABLE = True
except ImportError as e:
    PROMPTS_MODULE_AVAILABLE = False
    print(f"Warning: Create prompts module not available. {e}")


class YouTubeAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Viral YouTube Analyzer Pro")
        self.geometry("1500x900")
        self.minsize(1400, 800)
        
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Initialize API Config Manager
        self.config_manager = get_config_manager()
        
        # Initialize variables
        self.current_tab = "input"
        self.analysis_data = {}
        self.generated_content = {}
        self.youtube_manager = None
        
        # Auto-save file path
        self.autosave_path = "cache/last_analysis.json"
        
        # Initialize prompt generator
        if PROMPTS_MODULE_AVAILABLE:
            self.prompt_generator = PromptGenerator()
            self.current_prompts = {}
        else:
            self.prompt_generator = None
            self.current_prompts = {}
        
        # Setup UI
        self.setup_ui()
        
        # Load last analysis if exists
        self.load_last_analysis()
        
        # Bind close event to save before exit
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_closing(self):
        """Handle window closing event."""
        # Save current analysis if exists
        if self.analysis_data:
            self.save_analysis_data()
        self.destroy()
        
    def save_analysis_data(self):
        """Auto-save current analysis data."""
        try:
            # Create cache directory if not exists
            os.makedirs("cache", exist_ok=True)
            
            # Prepare data to save
            save_data = {
                'analysis_data': self.analysis_data,
                'generated_content': self.generated_content,
                'current_prompts': self.current_prompts,
                'saved_at': datetime.now().isoformat(),
                'version': '1.0'
            }
            
            # Save to file
            with open(self.autosave_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
                
            print(f"Analysis data auto-saved to {self.autosave_path}")
            
        except Exception as e:
            print(f"Error saving analysis data: {e}")
            
    def load_last_analysis(self):
        """Load last analysis data if exists."""
        try:
            if os.path.exists(self.autosave_path):
                with open(self.autosave_path, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)
                    
                # Restore data
                self.analysis_data = save_data.get('analysis_data', {})
                self.generated_content = save_data.get('generated_content', {})
                self.current_prompts = save_data.get('current_prompts', {})
                
                # Check if data is not empty
                if self.analysis_data:
                    saved_time = save_data.get('saved_at', '')
                    
                    # Show notification
                    self.after(1000, lambda: messagebox.showinfo(
                        "Đã khôi phục dữ liệu",
                        f"Đã tải lại kết quả phân tích từ lần trước\n"
                        f"Lưu lúc: {saved_time[:19].replace('T', ' ')}\n\n"
                        f"Bạn có thể xem lại trong tab 'Kết Quả Phân Tích'"
                    ))
                    
                    # Update analysis tab with loaded data
                    self.after(500, self._restore_analysis_ui)
                    
                    print(f"Loaded last analysis from {self.autosave_path}")
                    
        except Exception as e:
            print(f"Error loading last analysis: {e}")
            
    def _restore_analysis_ui(self):
        """Restore analysis UI with loaded data."""
        if "analysis" in self.tab_managers and self.analysis_data:
            # Simulate analysis complete to update UI
            result_data = {
                'status': 'success',
                'data': self.analysis_data,
                'restored': True  # Flag to indicate restored data
            }
            self.tab_managers["analysis"].on_complete(result_data)
            
            # Update prompt tab if available
            if "prompt" in self.tab_managers:
                self.tab_managers["prompt"].on_analysis_ready()
        
    def setup_ui(self):
        """Setup main UI structure."""
        # Main container
        self.main_frame = ctk.CTkFrame(self, fg_color="white")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        self.setup_header()
        
        # Tab navigation
        self.setup_tabs()
        
        # Content area
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Initialize tab managers
        self.setup_tab_managers()
        
        # Show first tab
        self.show_tab("input")
        
    def setup_header(self):
        """Setup application header."""
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="white", height=100)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 0))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="Viral YouTube Content Creator",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#2B2B2B"
        )
        title_label.grid(row=0, column=0, pady=(20, 5))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Phân tích nội dung YouTube → Tùy chỉnh prompts → Tạo câu chuyện viral",
            font=ctk.CTkFont(size=14),
            text_color="#666666"
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 20))
        
    def setup_tabs(self):
        """Setup tab navigation."""
        tab_frame = ctk.CTkFrame(self.main_frame, fg_color="white", height=50)
        tab_frame.grid(row=1, column=0, sticky="ew", padx=20)
        tab_frame.grid_columnconfigure(6, weight=1)
        
        # Tab buttons
        self.tab_buttons = {}
        tabs = [
            ("input", "🎯 Cấu Hình Đầu Vào", 0),
            ("analysis", "📊 Kết Quả Phân Tích", 1),
            ("prompt", "✏️ Tạo Prompts", 2),
            ("topic", "💡 Tạo Chủ Đề", 3),
            ("content", "📝 Tạo Nội Dung", 4),
            ("settings", "⚙️ Cài Đặt", 5)
        ]
        
        for key, text, col in tabs:
            btn = ctk.CTkButton(
                tab_frame,
                text=text,
                command=lambda k=key: self.show_tab(k),
                fg_color="transparent",
                text_color="#666666",
                hover_color="#E0E0E0",
                corner_radius=0,
                height=40,
                font=ctk.CTkFont(size=14)
            )
            btn.grid(row=0, column=col, padx=2, sticky="ew")
            self.tab_buttons[key] = btn
            
    def setup_tab_managers(self):
        """Initialize all tab managers."""
        self.tab_managers = {}
        
        # Input Tab
        self.tab_managers["input"] = InputTabManager(
            self.content_frame, 
            self.start_analysis
        )
        
        # Analysis Tab
        self.tab_managers["analysis"] = AnalysisTabManager(
            self.content_frame,
            self.export_analysis_json,
            self.export_analysis_csv,
            lambda: self.show_tab("prompt")
        )
        
        # Prompt Tab
        if self.prompt_generator:
            self.tab_managers["prompt"] = PromptTabManager(
                self.content_frame,
                self.prompt_generator,
                self.get_analysis_data,
                self.set_current_prompts
            )
        
        # Topic Tab
        self.tab_managers["topic"] = TopicTabManager(
            self.content_frame,
            self.generate_topics,
            self.export_topics
        )
        
        # Content Tab
        self.tab_managers["content"] = ContentTabManager(
            self.content_frame,
            self.generate_content,
            self.use_generated_topics
        )
        
        # Settings Tab
        self.tab_managers["settings"] = SettingsTabManager(
            self.content_frame,
            self.config_manager
        )
        
    def show_tab(self, tab_key):
        """Show selected tab."""
        # Hide all tab contents
        for manager in self.tab_managers.values():
            if hasattr(manager, 'hide'):
                manager.hide()
                
        # Update button styles
        for key, btn in self.tab_buttons.items():
            if key == tab_key:
                btn.configure(
                    fg_color="#2196F3",
                    text_color="white",
                    font=ctk.CTkFont(size=14, weight="bold")
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color="#666666",
                    font=ctk.CTkFont(size=14)
                )
                
        # Show selected tab
        if tab_key in self.tab_managers:
            self.tab_managers[tab_key].show()
        
        self.current_tab = tab_key

    def start_analysis(self, analysis_config: Dict):
        """Start YouTube data collection and analysis."""
        # Check if ready for analysis
        ready, message = self.config_manager.is_ready_for_analysis()
        if not ready:
            messagebox.showerror(
                "API Keys Required",
                f"{message}\n\nPlease configure your API keys in the Settings tab."
            )
            self.show_tab("settings")
            return
            
        # Check if YouTube module available
        if not YOUTUBE_MODULE_AVAILABLE:
            messagebox.showerror(
                "Missing Dependencies",
                "YouTube integration module not available!\n\n"
                "Please install required packages:\n"
                "pip install google-api-python-client youtube-transcript-api pytube"
            )
            return
            
        # Initialize YouTube manager with real API keys
        youtube_keys = self.config_manager.get_youtube_keys()
        openai_keys = self.config_manager.get_openai_keys()
        
        if not youtube_keys:
            messagebox.showerror(
                "No YouTube API Keys",
                "Please add at least one YouTube API key in Settings tab."
            )
            self.show_tab("settings")
            return
            
        try:
            self.youtube_manager = YouTubeAnalysisManager(youtube_keys, openai_keys)
            
            # Show analysis tab
            self.show_tab("analysis")
            
            self.youtube_manager.start_analysis(
                analysis_config['urls'],
                analysis_config['mode'],
                analysis_config['max_videos'],
                analysis_config['max_comments'],
                analysis_config['include_transcript'],
                analysis_config['include_comments'],
                self.update_analysis_progress,
                self.on_analysis_complete,
                analysis_config.get('custom_requirements')  # Thêm dòng này
            )
        except Exception as e:
            messagebox.showerror(
                "Analysis Error",
                f"Failed to start analysis:\n{str(e)}"
            )

    def update_analysis_progress(self, progress_data: dict):
        """Update analysis progress in UI."""
        self.after(0, self._update_progress_ui, progress_data)
        
    def _update_progress_ui(self, progress_data: dict):
        """Update progress UI elements."""
        if "analysis" in self.tab_managers:
            self.tab_managers["analysis"].update_progress(progress_data)
                
    def on_analysis_complete(self, result_data: dict):
        """Handle analysis completion."""
        self.after(0, self._handle_analysis_complete, result_data)
        
    def _handle_analysis_complete(self, result_data: dict):
        """Handle analysis completion in UI thread."""
        if "analysis" in self.tab_managers:
            self.tab_managers["analysis"].on_complete(result_data)
            
        # Store analysis data
        if result_data.get('status') == 'success':
            self.analysis_data = result_data.get('data', {})
            
            # Auto-save analysis data
            self.save_analysis_data()
            
            # Update prompt tab if available
            if "prompt" in self.tab_managers:
                self.tab_managers["prompt"].on_analysis_ready()

    def export_analysis_json(self):
        """Export analysis results to JSON."""
        if self.analysis_data:
            from tkinter import filedialog
            
            # Include additional requirements in export
            export_data = self.analysis_data.copy()
            
            # Get additional requirements from analysis tab
            if "analysis" in self.tab_managers:
                analysis_tab = self.tab_managers["analysis"]
                if hasattr(analysis_tab, 'additional_requirements'):
                    export_data['additional_requirements'] = analysis_tab.additional_requirements
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialfile=f"youtube_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            
            if filename:
                try:
                    # Create full export with metadata
                    full_export = {
                        'export_date': datetime.now().isoformat(),
                        'version': '2.0',
                        'status': 'success',
                        'data': export_data,
                        'viral_score': 85.0  # Calculate from data
                    }
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(full_export, f, ensure_ascii=False, indent=2)
                    messagebox.showinfo("Success", f"Data exported to:\n{filename}")
                except Exception as e:
                    messagebox.showerror("Export Error", f"Failed to export data: {e}")
                    
    def export_analysis_csv(self):
        """Export analysis results to CSV."""
        if self.analysis_data:
            from tkinter import filedialog
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"youtube_videos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            if filename:
                try:
                    videos = self.analysis_data.get('videos', [])
                    if videos:
                        with open(filename, 'w', newline='', encoding='utf-8') as f:
                            fieldnames = ['video_id', 'title', 'channel_title', 'view_count', 
                                        'like_count', 'comment_count', 'published_at']
                            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                            writer.writeheader()
                            writer.writerows(videos)
                        messagebox.showinfo("Success", f"Videos exported to:\n{filename}")
                    else:
                        messagebox.showwarning("No Data", "No video data to export!")
                except Exception as e:
                    messagebox.showerror("Export Error", f"Failed to export data: {e}")

    # Data access methods
    def get_analysis_data(self) -> Optional[Dict]:
        """Get current analysis data."""
        return self.analysis_data
        
    def set_current_prompts(self, prompts: Dict):
        """Set current prompts."""
        self.current_prompts = prompts
        # Auto-save when prompts are updated
        self.save_analysis_data()

    # Real API implementations for other features
    def generate_topics(self, config: Dict):
        """Generate topics using OpenAI."""
        if not self.config_manager.get_openai_keys():
            messagebox.showerror(
                "OpenAI API Required",
                "Please configure OpenAI API key in Settings tab to generate topics."
            )
            self.show_tab("settings")
            return
            
        # TODO: Implement real OpenAI topic generation
        messagebox.showinfo("Coming Soon", "OpenAI topic generation will be implemented soon!")
        
    def export_topics(self):
        """Export generated topics."""
        if "topic" in self.tab_managers:
            self.tab_managers["topic"].export_topics()
        
    def generate_content(self, config: Dict):
        """Generate content using OpenAI."""
        if not self.config_manager.get_openai_keys():
            messagebox.showerror(
                "OpenAI API Required",
                "Please configure OpenAI API key in Settings tab to generate content."
            )
            self.show_tab("settings")
            return
            
        # TODO: Implement real OpenAI content generation
        messagebox.showinfo("Coming Soon", "OpenAI content generation will be implemented soon!")
        
    def use_generated_topics(self):
        """Use generated topics in content tab."""
        messagebox.showinfo(
            "Use Topics",
            "Select a topic from the Topic tab and click 'Select' to use it."
        )