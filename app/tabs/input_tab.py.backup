"""
Input tab for YouTube URL input and analysis configuration
Enhanced with custom analysis requirements
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import List, Dict, Callable
import re


class InputTabManager:
    def __init__(self, parent_frame: ctk.CTkFrame, analyze_callback: Callable):
        self.parent_frame = parent_frame
        self.analyze_callback = analyze_callback
        
        # Create main container
        self.container = ctk.CTkFrame(parent_frame, fg_color="white")
        
        # Variables
        self.analysis_mode = ctk.StringVar(value="channel")
        self.include_transcript = ctk.BooleanVar(value=True)
        self.include_comments = ctk.BooleanVar(value=True)
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the input tab UI."""
        # Title
        title_label = ctk.CTkLabel(
            self.container,
            text="YouTube URL Input",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#2B2B2B"
        )
        title_label.pack(pady=(20, 10))
        
        # Analysis mode selection
        mode_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        mode_frame.pack(pady=(10, 20))
        
        mode_label = ctk.CTkLabel(
            mode_frame,
            text="Analysis Mode:",
            font=ctk.CTkFont(size=14),
            text_color="#666666"
        )
        mode_label.pack(side="left", padx=(0, 20))
        
        channel_radio = ctk.CTkRadioButton(
            mode_frame,
            text="Channel Analysis",
            variable=self.analysis_mode,
            value="channel",
            font=ctk.CTkFont(size=14),
            text_color="#2B2B2B",
            fg_color="#2196F3",
            hover_color="#1976D2"
        )
        channel_radio.pack(side="left", padx=10)
        
        video_radio = ctk.CTkRadioButton(
            mode_frame,
            text="Video List Analysis",
            variable=self.analysis_mode,
            value="video",
            font=ctk.CTkFont(size=14),
            text_color="#2B2B2B",
            fg_color="#2196F3",
            hover_color="#1976D2"
        )
        video_radio.pack(side="left", padx=10)
        
        # URL input section
        input_frame = ctk.CTkFrame(self.container, fg_color="#F5F5F5", corner_radius=10)
        input_frame.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        
        input_label = ctk.CTkLabel(
            input_frame,
            text="📺 Enter YouTube Channel URLs (analyzes latest videos from each channel):",
            font=ctk.CTkFont(size=14),
            text_color="#666666",
            anchor="w"
        )
        input_label.pack(fill="x", padx=20, pady=(20, 10))
        
        # URL text input
        self.url_text = ctk.CTkTextbox(
            input_frame,
            height=120,
            font=ctk.CTkFont(size=13),
            fg_color="white",
            text_color="#2B2B2B",
            border_width=1,
            border_color="#E0E0E0"
        )
        self.url_text.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Examples
        examples_label = ctk.CTkLabel(
            input_frame,
            text="Examples:\n- https://www.youtube.com/channel/CHANNEL_ID\n- https://www.youtube.com/@username\n- https://www.youtube.com/@channelname\n- https://www.youtube.com/user/username",
            font=ctk.CTkFont(size=11),
            text_color="#999999",
            justify="left",
            anchor="w"
        )
        examples_label.pack(fill="x", padx=20, pady=(0, 20))
        
        # Custom analysis requirements section (NEW)
        requirements_frame = ctk.CTkFrame(self.container, fg_color="#F5F5F5", corner_radius=10)
        requirements_frame.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        
        requirements_label = ctk.CTkLabel(
            requirements_frame,
            text="🎯 Custom Analysis Requirements (Optional):",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#2196F3",
            anchor="w"
        )
        requirements_label.pack(fill="x", padx=20, pady=(20, 10))
        
        requirements_hint = ctk.CTkLabel(
            requirements_frame,
            text="Describe what specific insights you want from the analysis. Leave empty for comprehensive analysis.",
            font=ctk.CTkFont(size=12),
            text_color="#666666",
            anchor="w",
            wraplength=800
        )
        requirements_hint.pack(fill="x", padx=20, pady=(0, 10))
        
        # Custom requirements text input
        self.requirements_text = ctk.CTkTextbox(
            requirements_frame,
            height=100,
            font=ctk.CTkFont(size=13),
            fg_color="white",
            text_color="#2B2B2B",
            border_width=1,
            border_color="#E0E0E0",
            wrap="word"
        )
        self.requirements_text.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Placeholder text
        self.requirements_text.insert("1.0", "E.g., Focus on audience engagement patterns, viral video characteristics, best posting times, content themes that resonate most, etc.")
        self.requirements_text.configure(text_color="#999999")
        
        # Bind events for placeholder
        self.requirements_text.bind("<FocusIn>", self._on_requirements_focus_in)
        self.requirements_text.bind("<FocusOut>", self._on_requirements_focus_out)
        
        # Example prompts
        example_prompts_frame = ctk.CTkFrame(requirements_frame, fg_color="transparent")
        example_prompts_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        example_prompts_label = ctk.CTkLabel(
            example_prompts_frame,
            text="Quick templates:",
            font=ctk.CTkFont(size=11),
            text_color="#666666"
        )
        example_prompts_label.pack(side="left", padx=(0, 10))
        
        # Quick template buttons
        templates = [
            ("Viral Analysis", "Analyze viral potential, engagement patterns, and content strategies that drive high viewership"),
            ("Audience Insights", "Focus on audience demographics, behavior, peak engagement times, and content preferences"),
            ("Content Strategy", "Identify successful content themes, optimal video length, posting frequency, and topic trends"),
            ("Competitor Analysis", "Compare channel performance, content gaps, unique selling points, and growth opportunities")
        ]
        
        for template_name, template_text in templates:
            btn = ctk.CTkButton(
                example_prompts_frame,
                text=template_name,
                command=lambda t=template_text: self._apply_template(t),
                fg_color="#E3F2FD",
                text_color="#2196F3",
                hover_color="#BBDEFB",
                height=25,
                font=ctk.CTkFont(size=11)
            )
            btn.pack(side="left", padx=2)
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=40, pady=(0, 20))
        
        # Clear button
        clear_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Clear All URLs",
            command=self.clear_urls,
            fg_color="#757575",
            hover_color="#616161",
            width=150,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        clear_btn.pack(side="left", padx=(0, 10))
        
        # Validate button
        validate_btn = ctk.CTkButton(
            buttons_frame,
            text="✓ Validate URLs",
            command=self.validate_urls,
            fg_color="#4CAF50",
            hover_color="#45A049",
            width=150,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        validate_btn.pack(side="left", padx=10)
        
        # Load sample button
        sample_btn = ctk.CTkButton(
            buttons_frame,
            text="📋 Load Sample URLs",
            command=self.load_sample_urls,
            fg_color="#FF9800",
            hover_color="#F57C00",
            width=150,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        sample_btn.pack(side="left", padx=10)
        
        # URL count label
        self.url_count_label = ctk.CTkLabel(
            buttons_frame,
            text="0 URLs entered",
            font=ctk.CTkFont(size=12),
            text_color="#666666"
        )
        self.url_count_label.pack(side="right", padx=10)
        
        # Parameters section
        params_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        params_frame.pack(fill="x", padx=40, pady=(0, 20))
        
        # Max videos
        videos_frame = ctk.CTkFrame(params_frame, fg_color="transparent")
        videos_frame.pack(side="left", padx=(0, 30))
        
        videos_label = ctk.CTkLabel(
            videos_frame,
            text="Max videos (per channel):",
            font=ctk.CTkFont(size=13),
            text_color="#666666"
        )
        videos_label.pack(side="left", padx=(0, 10))
        
        self.max_videos_entry = ctk.CTkEntry(
            videos_frame,
            width=60,
            height=30,
            font=ctk.CTkFont(size=13),
            fg_color="white",
            text_color="#2B2B2B",
            border_color="#E0E0E0"
        )
        self.max_videos_entry.pack(side="left")
        self.max_videos_entry.insert(0, "20")
        
        # Max comments
        comments_frame = ctk.CTkFrame(params_frame, fg_color="transparent")
        comments_frame.pack(side="left", padx=30)
        
        comments_label = ctk.CTkLabel(
            comments_frame,
            text="Max comments (per video):",
            font=ctk.CTkFont(size=13),
            text_color="#666666"
        )
        comments_label.pack(side="left", padx=(0, 10))
        
        self.max_comments_entry = ctk.CTkEntry(
            comments_frame,
            width=60,
            height=30,
            font=ctk.CTkFont(size=13),
            fg_color="white",
            text_color="#2B2B2B",
            border_color="#E0E0E0"
        )
        self.max_comments_entry.pack(side="left")
        self.max_comments_entry.insert(0, "50")
        
        # Checkboxes
        checkbox_frame = ctk.CTkFrame(params_frame, fg_color="transparent")
        checkbox_frame.pack(side="right")
        
        self.transcript_checkbox = ctk.CTkCheckBox(
            checkbox_frame,
            text="✓ Include transcript",
            variable=self.include_transcript,
            font=ctk.CTkFont(size=13),
            text_color="#2B2B2B",
            fg_color="#2196F3",
            hover_color="#1976D2",
            checkmark_color="white"
        )
        self.transcript_checkbox.pack(side="left", padx=10)
        
        self.comments_checkbox = ctk.CTkCheckBox(
            checkbox_frame,
            text="✓ Include comments",
            variable=self.include_comments,
            font=ctk.CTkFont(size=13),
            text_color="#2B2B2B",
            fg_color="#2196F3",
            hover_color="#1976D2",
            checkmark_color="white"
        )
        self.comments_checkbox.pack(side="left", padx=10)
        
        # Analyze button
        analyze_btn = ctk.CTkButton(
            self.container,
            text="🔍 Analyze",
            command=self.start_analysis,
            fg_color="#E53935",
            hover_color="#D32F2F",
            height=50,
            font=ctk.CTkFont(size=18, weight="bold"),
            corner_radius=25
        )
        analyze_btn.pack(pady=(10, 30))
        
        # Bind text change event
        self.url_text.bind("<KeyRelease>", self._update_url_count)
    
    def _on_requirements_focus_in(self, event):
        """Handle focus in event for requirements text."""
        if self.requirements_text.get("1.0", "end-1c") == "E.g., Focus on audience engagement patterns, viral video characteristics, best posting times, content themes that resonate most, etc.":
            self.requirements_text.delete("1.0", "end")
            self.requirements_text.configure(text_color="#2B2B2B")
    
    def _on_requirements_focus_out(self, event):
        """Handle focus out event for requirements text."""
        if not self.requirements_text.get("1.0", "end-1c").strip():
            self.requirements_text.insert("1.0", "E.g., Focus on audience engagement patterns, viral video characteristics, best posting times, content themes that resonate most, etc.")
            self.requirements_text.configure(text_color="#999999")
    
    def _apply_template(self, template_text: str):
        """Apply a quick template to requirements."""
        self.requirements_text.delete("1.0", "end")
        self.requirements_text.insert("1.0", template_text)
        self.requirements_text.configure(text_color="#2B2B2B")
    
    def _update_url_count(self, event=None):
        """Update URL count label."""
        text = self.url_text.get("1.0", "end-1c")
        urls = [line.strip() for line in text.split('\n') if line.strip()]
        self.url_count_label.configure(text=f"{len(urls)} URLs entered")
    
    def clear_urls(self):
        """Clear all URLs."""
        self.url_text.delete("1.0", "end")
        self._update_url_count()
    
    def validate_urls(self):
        """Validate entered URLs."""
        urls = self.get_urls()
        
        if not urls:
            messagebox.showwarning("No URLs", "Please enter at least one YouTube URL.")
            return
        
        valid_urls = []
        invalid_urls = []
        
        for url in urls:
            if self._is_valid_youtube_url(url):
                valid_urls.append(url)
            else:
                invalid_urls.append(url)
        
        message = f"Valid URLs: {len(valid_urls)}\n"
        if invalid_urls:
            message += f"Invalid URLs: {len(invalid_urls)}\n\n"
            message += "Invalid URLs:\n" + "\n".join(invalid_urls[:5])
            if len(invalid_urls) > 5:
                message += f"\n... and {len(invalid_urls) - 5} more"
        
        if valid_urls and not invalid_urls:
            messagebox.showinfo("Validation Result", f"All {len(valid_urls)} URLs are valid! ✅")
        else:
            messagebox.showwarning("Validation Result", message)
    
    def load_sample_urls(self):
        """Load sample YouTube URLs."""
        sample_channels = [
            "https://www.youtube.com/@MrBeast",
            "https://www.youtube.com/@PewDiePie",
            "https://www.youtube.com/@tseries",
            "https://www.youtube.com/@SETIndia"
        ]
        
        sample_videos = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://www.youtube.com/watch?v=9bZkp7q19f0",
            "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
            "https://www.youtube.com/watch?v=YQHsXMglC9A"
        ]
        
        if self.analysis_mode.get() == "channel":
            self.url_text.delete("1.0", "end")
            self.url_text.insert("1.0", "\n".join(sample_channels))
        else:
            self.url_text.delete("1.0", "end")
            self.url_text.insert("1.0", "\n".join(sample_videos))
        
        self._update_url_count()
    
    def get_urls(self) -> List[str]:
        """Get list of URLs from text widget."""
        text = self.url_text.get("1.0", "end-1c")
        urls = [line.strip() for line in text.split('\n') if line.strip()]
        return urls
    
    def get_custom_requirements(self) -> str:
        """Get custom analysis requirements."""
        requirements = self.requirements_text.get("1.0", "end-1c").strip()
        # Check if it's the placeholder text
        if requirements == "E.g., Focus on audience engagement patterns, viral video characteristics, best posting times, content themes that resonate most, etc.":
            return ""
        return requirements
    
    def _is_valid_youtube_url(self, url: str) -> bool:
        """Validate YouTube URL."""
        youtube_patterns = [
            r'^https?://(?:www\.)?youtube\.com/channel/[a-zA-Z0-9_-]+',
            r'^https?://(?:www\.)?youtube\.com/c/[a-zA-Z0-9_-]+',
            r'^https?://(?:www\.)?youtube\.com/@[a-zA-Z0-9_-]+',
            r'^https?://(?:www\.)?youtube\.com/user/[a-zA-Z0-9_-]+',
            r'^https?://(?:www\.)?youtube\.com/watch\?v=[a-zA-Z0-9_-]{11}',
            r'^https?://(?:www\.)?youtu\.be/[a-zA-Z0-9_-]{11}'
        ]
        
        return any(re.match(pattern, url) for pattern in youtube_patterns)
    
    def start_analysis(self):
        """Start the analysis process."""
        urls = self.get_urls()
        
        if not urls:
            messagebox.showwarning("No URLs", "Please enter at least one YouTube URL.")
            return
        
        # Validate all URLs
        invalid_urls = [url for url in urls if not self._is_valid_youtube_url(url)]
        if invalid_urls:
            response = messagebox.askyesno(
                "Invalid URLs Found",
                f"Found {len(invalid_urls)} invalid URLs. Continue with valid URLs only?"
            )
            if not response:
                return
            urls = [url for url in urls if self._is_valid_youtube_url(url)]
        
        if not urls:
            messagebox.showerror("No Valid URLs", "No valid YouTube URLs found.")
            return
        
        # Get parameters
        try:
            max_videos = int(self.max_videos_entry.get())
            max_comments = int(self.max_comments_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Parameters", "Max videos and comments must be numbers.")
            return
        
        # Get custom requirements
        custom_requirements = self.get_custom_requirements()
        
        # Prepare analysis configuration
        analysis_config = {
            'urls': urls,
            'mode': self.analysis_mode.get(),
            'max_videos': max_videos,
            'max_comments': max_comments,
            'include_transcript': self.include_transcript.get(),
            'include_comments': self.include_comments.get(),
            'custom_requirements': custom_requirements  # NEW: Pass custom requirements
        }
        
        # Call the analyze callback
        self.analyze_callback(analysis_config)
    
    def show(self):
        """Show the tab."""
        self.container.pack(fill="both", expand=True)
    
    def hide(self):
        """Hide the tab."""
        self.container.pack_forget()