"""
Input tab for YouTube URL input and analysis configuration
Enhanced with custom analysis requirements - FIXED VERSION
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
        self.analysis_mode = ctk.StringVar(value="video")  # Changed to video as default
        self.include_transcript = ctk.BooleanVar(value=True)
        self.include_comments = ctk.BooleanVar(value=True)
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the input tab UI."""
        # Title
        title_label = ctk.CTkLabel(
            self.container,
            text="Nhập URL Youtube",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#2B2B2B"
        )
        title_label.pack(pady=(20, 10))
        
        # Analysis mode selection
        mode_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        mode_frame.pack(pady=(10, 20))
        
        mode_label = ctk.CTkLabel(
            mode_frame,
            text="Chế độ phân tích:",
            font=ctk.CTkFont(size=14),
            text_color="#666666"
        )
        mode_label.pack(side="left", padx=(0, 20))
        
        channel_radio = ctk.CTkRadioButton(
            mode_frame,
            text="Phân tích kênh",
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
            text="Phân tích danh sách video",
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
            text="📺 Nhập URL video YouTube:",
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
        
        # Pre-fill with sample URL
        self.url_text.insert("1.0", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        
        # Examples
        examples_label = ctk.CTkLabel(
            input_frame,
            text="Examples:\n- https://www.youtube.com/watch?v=VIDEO_ID (for videos)\n- https://www.youtube.com/@channelname (for channels)\n- https://www.youtube.com/channel/CHANNEL_ID (for channels)",
            font=ctk.CTkFont(size=11),
            text_color="#999999",
            justify="left",
            anchor="w"
        )
        examples_label.pack(fill="x", padx=20, pady=(0, 20))
        
        # Custom analysis requirements section (OPTIONAL)
        requirements_frame = ctk.CTkFrame(self.container, fg_color="#F5F5F5", corner_radius=10)
        requirements_frame.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        
        requirements_label = ctk.CTkLabel(
            requirements_frame,
            text="🎯 Yêu Cầu Phân Tích (Tùy chọn):",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#2196F3",
            anchor="w"
        )
        requirements_label.pack(fill="x", padx=20, pady=(20, 10))
        
        requirements_hint = ctk.CTkLabel(
            requirements_frame,
            text="Mô tả những insights cụ thể bạn muốn từ phân tích. Để trống cho phân tích tự động.",
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
        
        # Insert placeholder text
        self.requirements_text.insert("1.0", "Để trống cho phân tích tự động hoặc mô tả yêu cầu cụ thể...")
        self.requirements_text.configure(text_color="#999999")
        
        # Bind events for placeholder
        self.requirements_text.bind("<FocusIn>", self._on_requirements_focus_in)
        self.requirements_text.bind("<FocusOut>", self._on_requirements_focus_out)
        
        # Example prompts
        example_prompts_frame = ctk.CTkFrame(requirements_frame, fg_color="transparent")
        example_prompts_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        example_prompts_label = ctk.CTkLabel(
            example_prompts_frame,
            text="Mẫu nhanh:",
            font=ctk.CTkFont(size=11),
            text_color="#666666"
        )
        example_prompts_label.pack(side="left", padx=(0, 10))

        # Define template questions as class attribute
        self.template_questions = {
            "Phân Tích Viral": """Phân tích tại sao video này viral:
- Những yếu tố nào làm video này thu hút lượng view cao?
- Tiêu đề, thumbnail, nội dung có gì đặc biệt?
- Thời điểm đăng có ảnh hưởng không?
- Audience reaction như thế nào?""",
            
            "Insights Khán Giả": """Phân tích khán giả:
- Đối tượng khán giả chính là ai?
- Họ quan tâm điều gì nhất?
- Phản hồi trong comments như thế nào?
- Có insights gì về behavior của audience?""",
            
            "Chiến Lược Nội Dung": """Phân tích chiến lược nội dung:
- Video này fit vào content strategy nào?
- Format và style có gì nổi bật?
- Có thể học hỏi gì cho content tương tự?
- Điểm mạnh và cơ hội cải thiện?""",
            
            "Phân Tích Đối Thủ": """So sánh với competitors:
- Video này khác gì so với competitors cùng niche?
- Unique selling points là gì?
- Có gap nào có thể khai thác?
- Lesson learned để differentiate?"""
        }

        # Track selected templates
        self.selected_templates = set()

        # Create checkboxes for templates
        for template_name in self.template_questions.keys():
            template_var = ctk.BooleanVar()
            
            checkbox = ctk.CTkCheckBox(
                example_prompts_frame,
                text=template_name,
                variable=template_var,
                command=lambda name=template_name, var=template_var: self._toggle_template(name, var),
                fg_color="#2196F3",
                hover_color="#1976D2",
                checkmark_color="white",
                font=ctk.CTkFont(size=11)
            )
            checkbox.pack(side="left", padx=5)
            
            # Store reference to checkbox variable
            setattr(self, f"template_{template_name.replace(' ', '_')}_var", template_var)
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=40, pady=(0, 20))
        
        # Clear button
        clear_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Xóa Tất Cả URLs",
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
            text="✓ Kiểm Tra URLs",
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
            text="📋 Tải URLs Mẫu",
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
            text="1 URL entered",
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
            text="Số video tối đa (mỗi kênh):",
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
            text="Số bình luận tối đa (mỗi video):",
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
            text="✓ Bao gồm phụ đề",
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
            text="✓ Bao gồm bình luận",
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
            text="🔍 Phân Tích",
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

    def _toggle_template(self, template_name: str, var: ctk.BooleanVar):
        """Handle template checkbox toggle."""
        if var.get():
            # Add template
            self.selected_templates.add(template_name)
        else:
            # Remove template
            self.selected_templates.discard(template_name)
        
        # Update requirements text
        self._update_requirements_from_templates()

    def _update_requirements_from_templates(self):
        """Update requirements text based on selected templates."""
        # Clear current text
        self.requirements_text.delete("1.0", "end")
        
        if not self.selected_templates:
            # No templates selected, show placeholder
            self.requirements_text.insert("1.0", "Để trống cho phân tích tự động hoặc mô tả yêu cầu cụ thể...")
            self.requirements_text.configure(text_color="#999999")
        else:
            # Combine questions from selected templates
            all_questions = []
            
            # Add header
            all_questions.append("Hãy phân tích video YouTube này theo các yêu cầu sau:\n")
            
            # Add questions from each selected template
            for template_name in ["Phân Tích Viral", "Insights Khán Giả", "Chiến Lược Nội Dung", "Phân Tích Đối Thủ"]:
                if template_name in self.selected_templates:
                    all_questions.append(f"\n** {template_name} **")
                    all_questions.append(self.template_questions[template_name])
            
            # Insert combined text
            combined_text = "\n".join(all_questions)
            self.requirements_text.insert("1.0", combined_text)
            self.requirements_text.configure(text_color="#2B2B2B")
   
    def _on_requirements_focus_in(self, event):
        """Handle focus in event for requirements text."""
        current_text = self.requirements_text.get("1.0", "end-1c")
        # Check if it's placeholder text
        if current_text in [
            "Để trống cho phân tích tự động hoặc mô tả yêu cầu cụ thể...",
            "Mô tả những insights cụ thể bạn muốn từ phân tích. Để trống cho phân tích toàn diện."
        ]:
            self.requirements_text.delete("1.0", "end")
            self.requirements_text.configure(text_color="#2B2B2B")

    def _on_requirements_focus_out(self, event):
        """Handle focus out event for requirements text."""
        if not self.requirements_text.get("1.0", "end-1c").strip():
            self.requirements_text.insert("1.0", "Để trống cho phân tích tự động hoặc mô tả yêu cầu cụ thể...")
            self.requirements_text.configure(text_color="#999999")
    
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
            messagebox.showwarning("Không có URLs", "Vui lòng nhập ít nhất một URL Youtube.")
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
            messagebox.showinfo("Kết Quả Kiểm Tra", f"All {len(valid_urls)} URLs are valid! ✅")
        else:
            messagebox.showwarning("Kết Quả Kiểm Tra", message)
    
    def load_sample_urls(self):
        """Load sample YouTube URLs."""
        sample_channels = [
            "https://www.youtube.com/@MrBeast",
            "https://www.youtube.com/@PewDiePie",
            "https://www.youtube.com/@tseries"
        ]
        
        sample_videos = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://www.youtube.com/watch?v=9bZkp7q19f0",
            "https://www.youtube.com/watch?v=kJQP7kiw5Fk"
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
        print(f"DEBUG: Raw requirements: '{requirements}'")
        
        # Check if it's the placeholder text
        placeholder_texts = [
            "Để trống cho phân tích tự động hoặc mô tả yêu cầu cụ thể...",
            "Mô tả những insights cụ thể bạn muốn từ phân tích. Để trống cho phân tích toàn diện."
        ]
        
        if requirements in placeholder_texts:
            print("DEBUG: Requirements is placeholder - returning empty")
            return ""
        
        print(f"DEBUG: Returning requirements: '{requirements}'")
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
        """Start the analysis process - FIXED VERSION."""
        print("DEBUG: start_analysis called")
        
        urls = self.get_urls()
        print(f"DEBUG: URLs found: {urls}")
        
        if not urls:
            messagebox.showwarning("Không có URLs", "Vui lòng nhập ít nhất một URL YouTube.")
            return
        
        # Get custom requirements - MAKE IT OPTIONAL
        custom_requirements = self.get_custom_requirements()
        print(f"DEBUG: Custom requirements: '{custom_requirements}'")
        
        # Validate all URLs
        print("DEBUG: Validating URLs...")
        invalid_urls = [url for url in urls if not self._is_valid_youtube_url(url)]
        print(f"DEBUG: Invalid URLs: {invalid_urls}")
        
        if invalid_urls:
            response = messagebox.askyesno(
                "Tìm thấy URLs không hợp lệ",
                f"Tìm thấy {len(invalid_urls)} URLs không hợp lệ. Tiếp tục với URLs hợp lệ?"
            )
            if not response:
                return
            urls = [url for url in urls if self._is_valid_youtube_url(url)]
        
        if not urls:
            messagebox.showerror("Không có URLs hợp lệ", "Không tìm thấy URLs YouTube hợp lệ.")
            return
        
        # Get parameters
        print("DEBUG: Getting parameters...")
        try:
            max_videos = int(self.max_videos_entry.get())
            max_comments = int(self.max_comments_entry.get())
            print(f"DEBUG: max_videos={max_videos}, max_comments={max_comments}")
        except ValueError:
            messagebox.showerror("Tham số không hợp lệ", "Số video và bình luận tối đa phải là số.")
            return
        
        # Prepare analysis configuration
        print("DEBUG: Preparing analysis config...")
        analysis_config = {
            'urls': urls,
            'mode': self.analysis_mode.get(),
            'max_videos': max_videos,
            'max_comments': max_comments,
            'include_transcript': self.include_transcript.get(),
            'include_comments': self.include_comments.get(),
            'custom_requirements': custom_requirements  # Can be empty - that's OK!
        }
        
        print(f"DEBUG: Analysis config: {analysis_config}")
        
        # Call the analyze callback
        print("DEBUG: Calling analyze_callback...")
        try:
            self.analyze_callback(analysis_config)
            print("DEBUG: analyze_callback completed successfully")
        except Exception as e:
            print(f"DEBUG: Error in analyze_callback: {e}")
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi bắt đầu phân tích: {e}")
        
    def show(self):
        """Show the tab."""
        self.container.pack(fill="both", expand=True)
    
    def hide(self):
        """Hide the tab."""
        self.container.pack_forget()
