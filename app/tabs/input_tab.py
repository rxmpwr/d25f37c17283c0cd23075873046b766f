"""
Input tab for YouTube URL input and analysis configuration
Enhanced with custom analysis requirements
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import List, Dict, Callable
import re
import os
from datetime import datetime


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
        # BỎ TITLE - Bắt đầu trực tiếp với Analysis mode
        
        # Analysis mode selection
        mode_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        mode_frame.pack(pady=(20, 20))
       
        
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
            text="📺 Nhập URL kênh Youtube (phân tích video mới nhất từ mỗi kênh):",
            font=ctk.CTkFont(size=14),
            text_color="#666666",
            anchor="w"
        )
        input_label.pack(fill="x", padx=20, pady=(20, 10))
        
        # URL text input với placeholder
        self.url_text = ctk.CTkTextbox(
            input_frame,
            height=120,
            font=ctk.CTkFont(size=13),
            fg_color="white",
            text_color="#999999",  # Màu xám cho placeholder
            border_width=1,
            border_color="#E0E0E0"
        )
        self.url_text.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Thêm placeholder text
        self.url_placeholder = "Examples:\n- https://www.youtube.com/channel/CHANNEL_ID\n- https://www.youtube.com/@username\n- https://www.youtube.com/@channelname\n- https://www.youtube.com/user/username"
        self.url_text.insert("1.0", self.url_placeholder)
        
        # Bind events cho URL placeholder
        self.url_text.bind("<FocusIn>", self._on_url_focus_in)
        self.url_text.bind("<FocusOut>", self._on_url_focus_out)
        
        # Custom analysis requirements section
        requirements_frame = ctk.CTkFrame(self.container, fg_color="#F5F5F5", corner_radius=10)
        requirements_frame.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        
        requirements_label = ctk.CTkLabel(
            requirements_frame,
            text="🎯 Yêu Cầu Phân Tích:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#2196F3",
            anchor="w"
        )
        requirements_label.pack(fill="x", padx=20, pady=(20, 10))
        
        requirements_hint = ctk.CTkLabel(
            requirements_frame,
            text="Mô tả những insights cụ thể bạn muốn từ phân tích.",
            font=ctk.CTkFont(size=12),
            text_color="#666666",
            anchor="w",
            wraplength=800
        )
        requirements_hint.pack(fill="x", padx=20, pady=(0, 10))
        
        # Custom requirements text input với placeholder
        self.requirements_text = ctk.CTkTextbox(
            requirements_frame,
            height=100,
            font=ctk.CTkFont(size=13),
            fg_color="white",
            text_color="#999999",  # Màu xám cho placeholder
            border_width=1,
            border_color="#E0E0E0",
            wrap="word"
        )
        self.requirements_text.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Thêm placeholder cho requirements
        self.requirements_placeholder = "Mô tả những insights cụ thể bạn muốn từ phân tích. Để trống cho phân tích toàn diện."
        self.requirements_text.insert("1.0", self.requirements_placeholder)
       
        # Bind events for placeholder
        self.requirements_text.bind("<FocusIn>", self._on_requirements_focus_in)
        self.requirements_text.bind("<FocusOut>", self._on_requirements_focus_out)
        
        # Example prompts - Mẫu nhanh
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
            "Viral Analysis": """
        - Những video nào có lượt xem vượt trội so với trung bình?
        - Video nào tăng view nhanh nhất trong 24h hoặc 7 ngày đầu?
        - Những yếu tố nào lặp lại trong các video viral (chủ đề, tiêu đề, thumbnail, độ dài, hook đầu video)?
        - Có trend nào được kênh tận dụng hiệu quả không?
        - Có đặc điểm gì trong cách dùng video, giọng nói, hoặc âm nhạc giúp video viral không?
        - Họ có định dạng series hoặc công thức nội dung đặc biệt nào giúp tăng khả năng viral không?
        - Tỷ lệ giữ chân người xem (retention rate) trong các video viral như thế nào?""",
            
            "Audience Insights": """
        - Đối tượng khán giả chính của kênh là ai (độ tuổi, giới tính, sở thích)?
        - Khán giả thường bình luận về điều gì nhiều nhất?
        - Có những pain points hoặc nhu cầu nào của khán giả được nhắc đến nhiều?
        - Thời điểm nào khán giả tương tác nhiều nhất?
        - Khán giả thích loại content nào nhất từ kênh này?
        - Có sự khác biệt nào về audience giữa các loại video khác nhau không?""",
            
            "Content Strategy": """
        - Kênh đang follow chiến lược content nào?
        - Tần suất đăng video như thế nào?
        - Có sự nhất quán về chủ đề, style, format không?
        - Họ có sử dụng content pillars (các trụ cột nội dung chính) không?
        - Cách họ cân bằng giữa evergreen content và trending content?
        - Có chiến lược cross-promotion hoặc content series không?
        - Điểm mạnh và điểm yếu trong content strategy hiện tại?""",
            
            "Competitor Analysis": """
        - So với các kênh cùng niche, kênh này có gì nổi bật?
        - Những video nào perform tốt hơn competitors?
        - Có gap nào trong content mà competitors chưa khai thác?
        - Tốc độ tăng trưởng so với competitors như thế nào?
        - Unique selling points của kênh là gì?
        - Có cơ hội nào để differentiate với competitors?"""
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
        analyze_btn.pack(pady=(10, 20))
        
        # Auto-save buttons frame (THÊM MỚI)
        autosave_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        autosave_frame.pack(fill="x", padx=40, pady=(0, 30))

        # Clear cache button
        self.clear_cache_btn = ctk.CTkButton(
            autosave_frame,
            text="🗑️ Xóa Dữ Liệu Cũ",
            command=self.clear_cache,
            fg_color="#FF5252",
            hover_color="#D32F2F",
            width=200,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.clear_cache_btn.pack(side="left", padx=(0, 10))

        # Load last analysis button
        self.load_last_btn = ctk.CTkButton(
            autosave_frame,
            text="📂 Tải Lại Kết Quả Cũ",
            command=self.load_last_analysis,
            fg_color="#4CAF50",
            hover_color="#388E3C",
            width=200,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.load_last_btn.pack(side="left", padx=10)

        # Cache info label
        self.cache_info_label = ctk.CTkLabel(
            autosave_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#666666"
        )
        self.cache_info_label.pack(side="left", padx=20)

        # Check cache status on init
        self.check_cache_status()
        
        # Bind text change event
        self.url_text.bind("<KeyRelease>", self._update_url_count)

    def _on_url_focus_in(self, event):
        """Handle focus in event for URL text."""
        current_text = self.url_text.get("1.0", "end-1c").strip()
        if current_text == self.url_placeholder.strip():
            self.url_text.delete("1.0", "end")
            self.url_text.configure(text_color="#2B2B2B")  # Màu đen cho text thật

    def _on_url_focus_out(self, event):
        """Handle focus out event for URL text."""
        current_text = self.url_text.get("1.0", "end-1c").strip()
        if not current_text:
            self.url_text.insert("1.0", self.url_placeholder)
            self.url_text.configure(text_color="#999999")  # Màu xám cho placeholder
        self._update_url_count()  # Cập nhật số URLs

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
            self.requirements_text.insert("1.0", self.requirements_placeholder)
            self.requirements_text.configure(text_color="#999999")
        else:
            # Combine questions from selected templates
            all_questions = []
            
            # Add header
            all_questions.append("Hãy phân tích các video trên kênh YouTube này để xác định các yếu tố khiến một video trở nên lan truyền mạnh mẽ (viral). Trả lời các câu hỏi sau:\n")
            
            # Add questions from each selected template
            for template_name in ["Viral Analysis", "Audience Insights", "Content Strategy", "Competitor Analysis"]:
                if template_name in self.selected_templates:
                    all_questions.append(f"\n** {template_name} **")
                    all_questions.append(self.template_questions[template_name])
            
            # Insert combined text
            combined_text = "\n".join(all_questions)
            self.requirements_text.insert("1.0", combined_text)
            self.requirements_text.configure(text_color="#2B2B2B")
   
    def _on_requirements_focus_in(self, event):
        """Handle focus in event for requirements text."""
        current_text = self.requirements_text.get("1.0", "end-1c").strip()
        if current_text == self.requirements_placeholder.strip():
            self.requirements_text.delete("1.0", "end")
            self.requirements_text.configure(text_color="#2B2B2B")

    def _on_requirements_focus_out(self, event):
        """Handle focus out event for requirements text."""
        current_text = self.requirements_text.get("1.0", "end-1c").strip()
        if not current_text and not self.selected_templates:
            self.requirements_text.insert("1.0", self.requirements_placeholder)
            self.requirements_text.configure(text_color="#999999")
    
    def _apply_template(self, template_text: str):
        """Apply a quick template to requirements."""
        self.requirements_text.delete("1.0", "end")
        self.requirements_text.insert("1.0", template_text)
        self.requirements_text.configure(text_color="#2B2B2B")
    
    def _update_url_count(self, event=None):
        """Update URL count label."""
        text = self.url_text.get("1.0", "end-1c").strip()
        
        # Kiểm tra nếu vẫn là placeholder
        if text == self.url_placeholder.strip():
            self.url_count_label.configure(text="0 URLs entered")
            return
            
        urls = [line.strip() for line in text.split('\n') if line.strip() and line.strip().startswith('http')]
        self.url_count_label.configure(text=f"{len(urls)} URLs entered")
    
    def clear_urls(self):
        """Clear all URLs."""
        self.url_text.delete("1.0", "end")
        self.url_text.insert("1.0", self.url_placeholder)
        self.url_text.configure(text_color="#999999")
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
            self.url_text.configure(text_color="#2B2B2B")
        else:
            self.url_text.delete("1.0", "end")
            self.url_text.insert("1.0", "\n".join(sample_videos))
            self.url_text.configure(text_color="#2B2B2B")
        
        self._update_url_count()
    
    def get_urls(self) -> List[str]:
        """Get list of URLs from text widget."""
        text = self.url_text.get("1.0", "end-1c").strip()
        
        # Kiểm tra nếu vẫn là placeholder
        if text == self.url_placeholder.strip():
            return []
        
        urls = [line.strip() for line in text.split('\n') if line.strip() and line.strip().startswith('http')]
        return urls
    
    def get_custom_requirements(self) -> str:
        """Get custom analysis requirements."""
        requirements = self.requirements_text.get("1.0", "end-1c").strip()
        
        # Kiểm tra nếu vẫn là placeholder
        if requirements == self.requirements_placeholder.strip():
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
        print("DEBUG: start_analysis called")
        
        urls = self.get_urls()
        print(f"DEBUG: URLs found: {urls}")
        
        if not urls:
            messagebox.showwarning("Không có URLs", "Vui lòng nhập ít nhất một URL YouTube.")
            return
        
        # Get custom requirements
        custom_requirements = self.get_custom_requirements()
        print(f"DEBUG: Requirements: {custom_requirements}")
        
        if not custom_requirements:
            messagebox.showwarning(
                "Yêu cầu phân tích bắt buộc", 
                "Vui lòng nhập yêu cầu phân tích cụ thể!"
            )
            return
        
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
            'custom_requirements': custom_requirements
        }
        
        print(f"DEBUG: Analysis config: {analysis_config}")
        
        # Call the analyze callback
        print("DEBUG: Calling analyze_callback...")
        self.analyze_callback(analysis_config)
        print("DEBUG: analyze_callback completed")
    
    def clear_cache(self):
        """Clear cached analysis data."""
        try:
            cache_path = "cache/last_analysis.json"
            if os.path.exists(cache_path):
                # Ask for confirmation
                result = messagebox.askyesno(
                    "Xác nhận xóa",
                    "Bạn có chắc muốn xóa dữ liệu phân tích đã lưu?\n"
                    "Hành động này không thể hoàn tác."
                )
                
                if result:
                    os.remove(cache_path)
                    messagebox.showinfo(
                        "Thành công",
                        "Đã xóa dữ liệu phân tích cũ."
                    )
                    self.check_cache_status()
            else:
                messagebox.showinfo(
                    "Thông báo",
                    "Không có dữ liệu cũ để xóa."
                )
        except Exception as e:
            messagebox.showerror(
                "Lỗi",
                f"Không thể xóa dữ liệu: {str(e)}"
            )

    def load_last_analysis(self):
        """Load last analysis from cache."""
        try:
            # Get reference to main app through parent hierarchy
            app = self.parent_frame.master.master  # Navigate to main window
            
            # Check if cache exists
            if os.path.exists("cache/last_analysis.json"):
                app.load_last_analysis()
                app.show_tab("analysis")
            else:
                messagebox.showinfo(
                    "Không có dữ liệu",
                    "Không tìm thấy kết quả phân tích nào được lưu."
                )
        except Exception as e:
            messagebox.showerror(
                "Lỗi",
                f"Không thể tải dữ liệu: {str(e)}"
            )

    def check_cache_status(self):
        """Check if cache exists and update button states."""
        cache_exists = os.path.exists("cache/last_analysis.json")
        
        if cache_exists:
            self.clear_cache_btn.configure(state="normal")
            self.load_last_btn.configure(state="normal")
            
            # Show cache info
            try:
                cache_stat = os.stat("cache/last_analysis.json")
                cache_time = datetime.fromtimestamp(cache_stat.st_mtime)
                cache_size = cache_stat.st_size / 1024  # KB
                
                self.cache_info_label.configure(
                    text=f"💾 Dữ liệu đã lưu: {cache_time.strftime('%d/%m/%Y %H:%M')} ({cache_size:.1f} KB)"
                )
            except:
                pass
        else:
            self.clear_cache_btn.configure(state="disabled")
            self.load_last_btn.configure(state="disabled")
            self.cache_info_label.configure(text="")
    
    def show(self):
        """Show the tab."""
        self.container.pack(fill="both", expand=True)
    
    def hide(self):
        """Hide the tab."""
        self.container.pack_forget()