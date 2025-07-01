"""
Main window class for YouTube Analyzer Pro - UPDATED WITH PERFORMANCE OPTIMIZATIONS
"""

import customtkinter as ctk
import threading
from datetime import datetime
from typing import Dict, Optional
from tkinter import messagebox
import json
import csv
import gc
import time

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

# Import performance optimizations
try:
    from performance_config import (
        perf_config, 
        perf_monitor, 
        MemoryOptimizer, 
        apply_performance_optimizations_to_app,
        get_performance_recommendations,
        optimize_app_startup
    )
    PERFORMANCE_OPTIMIZATIONS = True
except ImportError:
    PERFORMANCE_OPTIMIZATIONS = False
    print("Warning: Performance optimizations not available")


class YouTubeAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Viral Youtube Content Creator")
        self.geometry("1500x900")
        self.minsize(1400, 800)
        
        # Performance optimization - apply early
        if PERFORMANCE_OPTIMIZATIONS:
            optimize_app_startup()
            apply_performance_optimizations_to_app(self)
            perf_monitor.start_monitoring()
        
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
        
        # Performance tracking
        self.last_memory_check = time.time()
        self.analysis_start_time = None
        
        # Initialize prompt generator
        if PROMPTS_MODULE_AVAILABLE:
            self.prompt_generator = PromptGenerator()
            self.current_prompts = {}
        else:
            self.prompt_generator = None
            self.current_prompts = {}
        
        # Setup UI
        self.setup_ui()
        
        # Performance monitoring setup
        if PERFORMANCE_OPTIMIZATIONS:
            self.setup_performance_monitoring()
        
    def setup_performance_monitoring(self):
        """Setup performance monitoring for the application"""
        # Schedule periodic memory checks
        self.after(30000, self.check_memory_usage)  # Every 30 seconds
        
        # Setup performance recommendations
        self.performance_recommendations = []
        
    def check_memory_usage(self):
        """Check memory usage and perform cleanup if needed"""
        if not PERFORMANCE_OPTIMIZATIONS:
            self.after(30000, self.check_memory_usage)
            return
            
        current_time = time.time()
        if current_time - self.last_memory_check > 30:  # Check every 30 seconds
            memory_usage = MemoryOptimizer.get_memory_usage_mb()
            
            if memory_usage > 0:
                print(f"🧠 Memory usage: {memory_usage:.1f} MB")
                
                # If memory usage is high, suggest cleanup
                if MemoryOptimizer.check_memory_threshold():
                    self.suggest_memory_cleanup()
                    
            self.last_memory_check = current_time
            
        # Schedule next check
        self.after(30000, self.check_memory_usage)
        
    def suggest_memory_cleanup(self):
        """Suggest memory cleanup to user"""
        if hasattr(self, '_cleanup_suggested'):
            return  # Don't spam suggestions
            
        self._cleanup_suggested = True
        
        response = messagebox.askyesno(
            "Memory Usage High",
            "Memory usage is high. Would you like to clear cache and optimize performance?\n\n"
            "This will clear analysis data but improve performance."
        )
        
        if response:
            self.cleanup_memory()
        
        # Reset suggestion flag after 5 minutes
        self.after(300000, lambda: delattr(self, '_cleanup_suggested'))
        
    def cleanup_memory(self):
        """Cleanup memory and optimize performance"""
        try:
            # Clear analysis data
            MemoryOptimizer.cleanup_large_variables(self.analysis_data, self.generated_content)
            self.analysis_data = {}
            self.generated_content = {}
            
            # Clear tab manager caches
            for tab_manager in self.tab_managers.values():
                if hasattr(tab_manager, 'clear_cache'):
                    tab_manager.clear_cache()
                    
            # Force garbage collection
            gc.collect()
            
            # Show result
            new_memory = MemoryOptimizer.get_memory_usage_mb()
            if new_memory > 0:
                messagebox.showinfo(
                    "Memory Cleanup Complete",
                    f"Memory usage reduced to {new_memory:.1f} MB\n\n"
                    "Performance should be improved."
                )
            else:
                messagebox.showinfo("Memory Cleanup Complete", "Memory optimization completed.")
                
        except Exception as e:
            messagebox.showerror("Cleanup Error", f"Error during cleanup: {e}")
        
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
        """Setup application header with performance info."""
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="white", height=100)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 0))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="Phần Mềm Phân Tích YouTube Viral Pro",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#2B2B2B"
        )
        title_label.grid(row=0, column=0, pady=(20, 5))
        
        # Subtitle with performance info
        subtitle_text = "Analyze YouTube content → Customize prompts → Generate viral stories)"
        if PERFORMANCE_OPTIMIZATIONS:
            subtitle_text += " (Performance Optimized)"
            
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text=subtitle_text,
            font=ctk.CTkFont(size=14),
            text_color="#666666"
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 5))
        
        # Performance status (if available)
        if PERFORMANCE_OPTIMIZATIONS:
            self.performance_status_label = ctk.CTkLabel(
                header_frame,
                text="🚀 Performance mode: Active",
                font=ctk.CTkFont(size=11),
                text_color="#4CAF50"
            )
            self.performance_status_label.grid(row=2, column=0, pady=(0, 15))
        
    def setup_tabs(self):
        """Setup tab navigation."""
        tab_frame = ctk.CTkFrame(self.main_frame, fg_color="white", height=50)
        tab_frame.grid(row=1, column=0, sticky="ew", padx=20)
        tab_frame.grid_columnconfigure(7, weight=1)  # Added column for performance tab
        
        # Tab buttons
        self.tab_buttons = {}
        tabs = [
            ("input", "🎯 Input Configuration", 0),
            ("analysis", "📊 Analysis Result", 1),
            ("prompt", "✏️ Create Prompts", 2),
            ("topic", "💡 Generate Topic", 3),
            ("content", "📝 Generate Content", 4),
            ("settings", "⚙️ Settings", 5)
        ]
        
        # Add performance tab if optimizations available
        if PERFORMANCE_OPTIMIZATIONS:
            tabs.append(("performance", "📈 Performance", 6))
        
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
        
        # Analysis Tab (with performance optimizations)
        self.tab_managers["analysis"] = AnalysisTabManager(
            self.content_frame,
            self.export_analysis_json,
            self.export_analysis_csv,
            lambda: self.show_tab("prompt")
        )
        
        # Apply performance optimizations to analysis tab
        if PERFORMANCE_OPTIMIZATIONS and hasattr(self.tab_managers["analysis"], 'apply_optimizations'):
            self.tab_managers["analysis"].apply_optimizations()
        
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
        
        # Settings Tab (with performance settings)
        self.tab_managers["settings"] = SettingsTabManager(
            self.content_frame,
            self.config_manager
        )
        
        # Performance Tab (if optimizations available)
        if PERFORMANCE_OPTIMIZATIONS:
            self.tab_managers["performance"] = self.create_performance_tab()
        
    def create_performance_tab(self):
        """Create performance monitoring tab"""
        class PerformanceTabManager:
            def __init__(self, parent_frame, main_app):
                self.parent_frame = parent_frame
                self.main_app = main_app
                self.tab_frame = None
                self.is_visible = False
                self.setup_ui()
                
            def setup_ui(self):
                """Setup performance tab UI"""
                self.tab_frame = ctk.CTkFrame(self.parent_frame, fg_color="white")
                
                # Performance metrics
                metrics_frame = ctk.CTkFrame(self.tab_frame)
                metrics_frame.pack(fill="x", padx=20, pady=10)
                
                ctk.CTkLabel(
                    metrics_frame, 
                    text="📊 Performance Metrics",
                    font=ctk.CTkFont(size=18, weight="bold")
                ).pack(pady=10)
                
                # Memory usage
                self.memory_label = ctk.CTkLabel(metrics_frame, text="Memory: -- MB")
                self.memory_label.pack(pady=5)
                
                # Performance settings
                settings_frame = ctk.CTkFrame(self.tab_frame)
                settings_frame.pack(fill="x", padx=20, pady=10)
                
                ctk.CTkLabel(
                    settings_frame,
                    text="⚙️ Performance Settings",
                    font=ctk.CTkFont(size=18, weight="bold")
                ).pack(pady=10)
                
                # Preset selection
                preset_frame = ctk.CTkFrame(settings_frame)
                preset_frame.pack(fill="x", padx=10, pady=5)
                
                ctk.CTkLabel(preset_frame, text="Performance Preset:").pack(side="left", padx=5)
                
                self.preset_var = ctk.StringVar(value="balanced")
                preset_menu = ctk.CTkOptionMenu(
                    preset_frame,
                    variable=self.preset_var,
                    values=["conservative", "balanced", "aggressive"],
                    command=self.apply_preset
                )
                preset_menu.pack(side="right", padx=5)
                
                # Manual cleanup button
                cleanup_btn = ctk.CTkButton(
                    settings_frame,
                    text="🧹 Clear Cache & Optimize Memory",
                    command=self.main_app.cleanup_memory
                )
                cleanup_btn.pack(pady=10)
                
                # Performance report
                self.report_text = ctk.CTkTextbox(self.tab_frame, height=300)
                self.report_text.pack(fill="both", expand=True, padx=20, pady=10)
                
                self.hide()
                
            def apply_preset(self, preset_name):
                """Apply performance preset"""
                from performance_config import apply_performance_preset
                apply_performance_preset(preset_name)
                
                messagebox.showinfo(
                    "Performance Preset Applied",
                    f"Applied '{preset_name}' performance preset.\n\n"
                    "Settings will take effect for new analysis operations."
                )
                
            def show(self):
                """Show performance tab"""
                self.tab_frame.pack(fill="both", expand=True)
                self.is_visible = True
                self.update_metrics()
                
            def hide(self):
                """Hide performance tab"""
                self.tab_frame.pack_forget()
                self.is_visible = False
                
            def update_metrics(self):
                """Update performance metrics"""
                if not self.is_visible:
                    return
                    
                # Update memory usage
                memory_usage = MemoryOptimizer.get_memory_usage_mb()
                if memory_usage > 0:
                    self.memory_label.configure(text=f"Memory: {memory_usage:.1f} MB")
                
                # Update performance report
                report = perf_monitor.get_performance_report()
                
                report_text = "📊 PERFORMANCE REPORT\n\n"
                
                for metric, data in report.items():
                    if data['count'] > 0:
                        report_text += f"{metric.replace('_', ' ').title()}:\n"
                        report_text += f"  Average: {data['average']:.2f}s\n"
                        report_text += f"  Max: {data['max']:.2f}s\n"
                        report_text += f"  Count: {data['count']}\n\n"
                
                # Add recommendations
                if hasattr(self.main_app, 'analysis_data') and self.main_app.analysis_data:
                    recommendations = get_performance_recommendations(self.main_app.analysis_data)
                    if recommendations:
                        report_text += "💡 RECOMMENDATIONS:\n\n"
                        for rec in recommendations:
                            report_text += f"• {rec}\n"
                
                self.report_text.delete("1.0", "end")
                self.report_text.insert("1.0", report_text)
                
                # Schedule next update
                if self.is_visible:
                    self.main_app.after(5000, self.update_metrics)
        
        return PerformanceTabManager(self.content_frame, self)
        
    def show_tab(self, tab_key):
        """Show selected tab with performance optimization."""
        # Performance tracking
        if PERFORMANCE_OPTIMIZATIONS:
            start_time = time.time()
        
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
        
        # Performance tracking
        if PERFORMANCE_OPTIMIZATIONS:
            elapsed = time.time() - start_time
            if elapsed > 0.5:  # Log slow tab switches
                print(f"⚠️ Slow tab switch to {tab_key}: {elapsed:.2f}s")

    def start_analysis(self, analysis_config: Dict):
        """Start YouTube data collection and analysis with performance optimizations."""
        # Performance pre-check
        if PERFORMANCE_OPTIMIZATIONS:
            # Check memory before starting
            if MemoryOptimizer.check_memory_threshold():
                response = messagebox.askyesno(
                    "High Memory Usage",
                    "Memory usage is high. Clear cache before starting analysis?\n\n"
                    "This will improve performance but clear existing data."
                )
                if response:
                    self.cleanup_memory()
                elif not messagebox.askyesno(
                    "Continue Anyway?",
                    "Continue with high memory usage? This may cause performance issues."
                ):
                    return
            
            # Apply optimized settings based on expected dataset size
            estimated_videos = analysis_config.get('max_videos', 20) * len(analysis_config.get('urls', []))
            optimized_settings = perf_config.get_optimized_settings_for_dataset_size(estimated_videos)
            
            # Show optimization info
            if estimated_videos > 100:
                messagebox.showinfo(
                    "Large Dataset Detected",
                    f"Estimated {estimated_videos} videos will be processed.\n\n"
                    "Performance optimizations have been applied:\n"
                    f"• Batch size: {optimized_settings.get('max_videos_per_batch', 20)}\n"
                    f"• Comments per video: {optimized_settings.get('max_comments_per_video', 50)}\n\n"
                    "Processing may take longer but will be more stable."
                )
        
        # Check if ready for analysis
        ready, message = self.config_manager.is_ready_for_analysis()
        if not ready:
            messagebox.showerror(
                "Cần API Keys",
                f"{message}\n\nPlease configure your API keys in the Settings tab."
            )
            self.show_tab("settings")
            return
            
        # Check if YouTube module available
        if not YOUTUBE_MODULE_AVAILABLE:
            messagebox.showerror(
                "Thiếu Dependencies",
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
                "Không Có YouTube API Keys",
                "Vui lòng thêm ít nhất một YouTube API key trong tab Cài Đặt."
            )
            self.show_tab("settings")
            return
            
        try:
            # Store analysis start time for performance tracking
            self.analysis_start_time = time.time()
            
            self.youtube_manager = YouTubeAnalysisManager(youtube_keys, openai_keys)
            
            # Show analysis tab
            self.show_tab("analysis")
            
            # Start real analysis with performance optimizations
            self.youtube_manager.start_analysis(
                analysis_config['urls'],
                analysis_config['mode'],
                analysis_config['max_videos'],
                analysis_config['max_comments'],
                analysis_config['include_transcript'],
                analysis_config['include_comments'],
                self.update_analysis_progress,
                self.on_analysis_complete
            )
            
        except Exception as e:
            messagebox.showerror(
                "Lỗi Phân Tích",
                f"Failed to start analysis:\n{str(e)}"
            )

    def update_analysis_progress(self, progress_data: dict):
        """Update analysis progress in UI with optimization."""
        self.after(0, self._update_progress_ui, progress_data)
        
    def _update_progress_ui(self, progress_data: dict):
        """Update progress UI elements with throttling."""
        if "analysis" in self.tab_managers:
            # Performance optimization - throttle updates
            if PERFORMANCE_OPTIMIZATIONS:
                current_time = time.time()
                if not hasattr(self, '_last_progress_update'):
                    self._last_progress_update = 0
                    
                # Limit updates to prevent UI lag
                if current_time - self._last_progress_update < 0.1:  # 100ms throttle
                    return
                    
                self._last_progress_update = current_time
            
            self.tab_managers["analysis"].update_progress(progress_data)
                
    def on_analysis_complete(self, result_data: dict):
        """Handle analysis completion with performance tracking."""
        self.after(0, self._handle_analysis_complete, result_data)
        
    def _handle_analysis_complete(self, result_data: dict):
        """Handle analysis completion in UI thread with optimization."""
        if "analysis" in self.tab_managers:
            self.tab_managers["analysis"].on_complete(result_data)
            
        # Store analysis data with optimization
        if result_data.get('status') == 'success':
            raw_data = result_data.get('data', {})
            
            # Apply memory optimization before storing
            if PERFORMANCE_OPTIMIZATIONS:
                self.analysis_data = MemoryOptimizer.limit_data_size(raw_data)
                
                # Show performance info
                if self.analysis_start_time:
                    elapsed = time.time() - self.analysis_start_time
                    memory_usage = MemoryOptimizer.get_memory_usage_mb()
                    
                    print(f"✅ Analysis completed in {elapsed:.1f}s")
                    if memory_usage > 0:
                        print(f"💾 Memory usage: {memory_usage:.1f} MB")
                    
                    # Show recommendations if needed
                    recommendations = get_performance_recommendations(self.analysis_data)
                    if recommendations:
                        self.performance_recommendations = recommendations
                        
                        # Show top recommendation
                        messagebox.showinfo(
                            "Performance Tip",
                            f"Analysis complete!\n\n"
                            f"💡 Tip: {recommendations[0]}\n\n"
                            f"Check Performance tab for more recommendations."
                        )
            else:
                self.analysis_data = raw_data
            
            # Update prompt tab if available
            if "prompt" in self.tab_managers:
                self.tab_managers["prompt"].on_analysis_ready()

    def export_analysis_json(self):
        """Export analysis results to JSON with optimization."""
        if not self.analysis_data:
            messagebox.showwarning("No Data", "No analysis data to export.")
            return
            
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
                    'version': '2.1',  # Updated version
                    'status': 'success',
                    'data': export_data,
                    'viral_score': self.analysis_data.get('viral_score', 0)
                }
                
                # Add performance info if available
                if PERFORMANCE_OPTIMIZATIONS:
                    full_export['performance_info'] = {
                        'optimizations_applied': True,
                        'export_time': datetime.now().isoformat(),
                        'data_size_limited': True if MemoryOptimizer.check_memory_threshold() else False
                    }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(full_export, f, ensure_ascii=False, indent=2)
                    
                messagebox.showinfo("Export Success", f"Data exported to:\n{filename}")
                
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export data: {e}")
                    
    def export_analysis_csv(self):
        """Export analysis results to CSV with optimization."""
        if not self.analysis_data:
            messagebox.showwarning("No Data", "No analysis data to export.")
            return
            
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"youtube_videos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if filename:
            try:
                videos = self.analysis_data.get('video', [])
                if videos:
                    # Limit export size for performance
                    if PERFORMANCE_OPTIMIZATIONS:
                        max_export = perf_config.get('max_export_items', 10000)
                        if len(videos) > max_export:
                            videos = videos[:max_export]
                            messagebox.showinfo(
                                "Large Dataset",
                                f"Exporting first {max_export} videos for performance.\n"
                                f"Total videos: {len(self.analysis_data.get('video', []))}"
                            )
                    
                    with open(filename, 'w', newline='', encoding='utf-8') as f:
                        fieldnames = ['video_id', 'title', 'channel_title', 'view_count', 
                                    'like_count', 'comment_count', 'published_at', 'engagement_rate', 'viral_score']
                        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                        writer.writeheader()
                        writer.writerows(videos)
                        
                    messagebox.showinfo("Export Success", f"Videos exported to:\n{filename}")
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
            "Select a topic from the Topic tab and click 'Chọn' to use it."
        )
        
    def on_closing(self):
        """Handle application closing with cleanup."""
        try:
            # Performance cleanup
            if PERFORMANCE_OPTIMIZATIONS:
                perf_monitor.stop_monitoring()
                MemoryOptimizer.cleanup_large_variables(
                    self.analysis_data, 
                    self.generated_content, 
                    self.current_prompts
                )
                gc.collect()
                
            # Stop any running analysis
            if self.youtube_manager and hasattr(self.youtube_manager, 'stop_analysis'):
                self.youtube_manager.stop_analysis()
                
        except Exception as e:
            print(f"Error during cleanup: {e}")
        finally:
            self.destroy()
            
    def protocol(self, protocol, func):
        """Override protocol to handle window closing."""
        if protocol == "WM_DELETE_WINDOW":
            super().protocol(protocol, self.on_closing)
        else:
            super().protocol(protocol, func)


# Ensure proper cleanup on close
if __name__ == "__main__":
    app = YouTubeAnalyzerApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()