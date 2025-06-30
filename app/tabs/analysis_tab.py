"""
Analysis tab for displaying YouTube analysis results with overview section
"""

import customtkinter as ctk
from typing import Dict, Optional, Callable
import json
from datetime import datetime
import threading

class AnalysisTabManager:
    def __init__(self, parent_frame: ctk.CTkFrame, export_json_callback: Callable, 
                 export_csv_callback: Callable, create_prompts_callback: Callable):
        self.parent_frame = parent_frame
        self.export_json_callback = export_json_callback
        self.export_csv_callback = export_csv_callback
        self.create_prompts_callback = create_prompts_callback
        
        # Create main container
        self.container = ctk.CTkFrame(parent_frame, fg_color="white")
        
        # Variables
        self.analysis_data = None
        self.additional_requirements = ""
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the analysis tab UI."""
        # Title
        title_label = ctk.CTkLabel(
            self.container,
            text="📊 Kết Quả Phân Tích",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#2B2B2B"
        )
        title_label.pack(pady=(20, 10))
        
        # Progress section (initially shown)
        self.progress_frame = ctk.CTkFrame(self.container, fg_color="#F5F5F5", corner_radius=10)
        self.progress_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Progress content
        progress_title = ctk.CTkLabel(
            self.progress_frame,
            text="🔄 Đang Phân Tích...",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#2196F3"
        )
        progress_title.pack(pady=(30, 10))
        
        progress_desc = ctk.CTkLabel(
            self.progress_frame,
            text="Đang phân tích dữ liệu YouTube. Quá trình này có thể mất vài phút...",
            font=ctk.CTkFont(size=14),
            text_color="#666666"
        )
        progress_desc.pack(pady=(0, 20))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            width=600,
            height=20,
            progress_color="#2196F3"
        )
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
        
        # Progress details
        self.progress_details_frame = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        self.progress_details_frame.pack(pady=20)
        
        # Progress labels
        self.time_label = ctk.CTkLabel(
            self.progress_details_frame,
            text="⏱️ Thời gian đã qua: 0:00",
            font=ctk.CTkFont(size=13),
            text_color="#666666"
        )
        self.time_label.grid(row=0, column=0, padx=20, pady=5)
        
        self.videos_label = ctk.CTkLabel(
            self.progress_details_frame,
            text="📹 Video đã phân tích: 0",
            font=ctk.CTkFont(size=13),
            text_color="#666666"
        )
        self.videos_label.grid(row=0, column=1, padx=20, pady=5)
        
        self.comments_label = ctk.CTkLabel(
            self.progress_details_frame,
            text="💬 Bình luận đã thu thập: 0",
            font=ctk.CTkFont(size=13),
            text_color="#666666"
        )
        self.comments_label.grid(row=1, column=0, padx=20, pady=5)
        
        self.transcripts_label = ctk.CTkLabel(
            self.progress_details_frame,
            text="📄 Phụ đề đã thu thập: 0",
            font=ctk.CTkFont(size=13),
            text_color="#666666"
        )
        self.transcripts_label.grid(row=1, column=1, padx=20, pady=5)
        
        # Current task
        self.task_label = ctk.CTkLabel(
            self.progress_frame,
            text="🎯 Tác vụ hiện tại: Đang khởi tạo...",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#2196F3"
        )
        self.task_label.pack(pady=(10, 30))
        
        # Results section (initially hidden)
        self.results_frame = ctk.CTkFrame(self.container, fg_color="white")
        
        # Create scrollable frame for results
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.results_frame,
            fg_color="white",
            scrollbar_button_color="#E0E0E0",
            scrollbar_button_hover_color="#CCCCCC"
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
    def show_results(self, analysis_data: Dict):
        """Display analysis results dynamically."""
        # DEBUG: Print data structure
        print(f"DEBUG show_results - analysis_data keys: {analysis_data.keys()}")
        print(f"DEBUG show_results - analysis_type: {analysis_data.get('analysis_type')}")
        
        self.analysis_data = analysis_data
        
        # Hide progress, show results
        self.progress_frame.pack_forget()
        self.results_frame.pack(fill="both", expand=True)
        
        # Clear scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Check if dynamic or structured analysis
        if analysis_data.get('analysis_type') == 'dynamic':
            print("DEBUG: Showing dynamic results")
            self._show_dynamic_results(analysis_data)
        else:
            print("DEBUG: Showing structured results")
            self._show_overview_and_details(analysis_data)
            
    def _show_overview_and_details(self, analysis_data: Dict):
        """Show structured analysis results with overview."""
        print(f"DEBUG _show_overview_and_details - keys: {analysis_data.keys()}")

        # Get actual data from the result
        data = analysis_data.get('data', analysis_data)  # Handle both formats
        
        # 1. OVERVIEW SECTION
        overview_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#E3F2FD", corner_radius=10)
        overview_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        overview_title = ctk.CTkLabel(
            overview_frame,
            text="📊 TỔNG QUAN PHÂN TÍCH",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1565C0"
        )
        overview_title.pack(pady=(20, 15), padx=20)
        
        # Overview content frame
        overview_content = ctk.CTkFrame(overview_frame, fg_color="transparent")
        overview_content.pack(fill="x", padx=30, pady=(0, 20))
        
        # Calculate overview metrics
        videos = data.get('videos', [])
        comments = data.get('comments', [])
        transcripts = data.get('transcripts', [])
        viral_score = analysis_data.get('viral_score', data.get('viral_score', 0))
        
        total_views = sum(v.get('view_count', 0) for v in videos)
        total_likes = sum(v.get('like_count', 0) for v in videos)
        avg_engagement = sum((v.get('like_count', 0) + v.get('comment_count', 0)) / v.get('view_count', 1) * 100 
                           for v in videos if v.get('view_count', 0) > 0) / len(videos) if videos else 0
        
        # Channel info
        channels = data.get('channels', [])
        channel_names = list(set(v.get('channel_title', 'Unknown') for v in videos))[:3]
        channel_text = ", ".join(channel_names)
        if len(channel_names) < len(set(v.get('channel_title') for v in videos)):
            channel_text += "..."
        
        # Create overview items
        overview_items = [
            ("🎬 Kênh phân tích:", channel_text or "N/A"),
            ("📹 Tổng số video:", f"{len(videos):,}"),
            ("👁️ Tổng lượt xem:", f"{total_views:,}"),
            ("❤️ Tổng lượt thích:", f"{total_likes:,}"),
            ("💬 Tổng bình luận thu thập:", f"{len(comments):,}"),
            ("📄 Tổng phụ đề thu thập:", f"{len(transcripts):,}"),
            ("📊 Tỷ lệ tương tác trung bình:", f"{avg_engagement:.2f}%"),
            ("🔥 Điểm Viral:", f"{viral_score:.1f}/100")
        ]
        
        # Display overview in 2 columns
        for i, (label, value) in enumerate(overview_items):
            row = i // 2
            col = i % 2
            
            item_frame = ctk.CTkFrame(overview_content, fg_color="transparent")
            item_frame.grid(row=row, column=col, padx=10, pady=5, sticky="w")
            
            label_widget = ctk.CTkLabel(
                item_frame,
                text=label,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#424242"
            )
            label_widget.pack(side="left", padx=(0, 10))
            
            value_widget = ctk.CTkLabel(
                item_frame,
                text=value,
                font=ctk.CTkFont(size=14),
                text_color="#212121"
            )
            value_widget.pack(side="left")
            
            # Special styling for viral score
            if "Điểm Viral" in label:
                if viral_score >= 70:
                    value_widget.configure(text_color="#4CAF50", font=ctk.CTkFont(size=16, weight="bold"))
                elif viral_score >= 50:
                    value_widget.configure(text_color="#FF9800", font=ctk.CTkFont(size=16, weight="bold"))
                else:
                    value_widget.configure(text_color="#F44336", font=ctk.CTkFont(size=16, weight="bold"))
        
        # Key insights section
        insights_frame = ctk.CTkFrame(overview_frame, fg_color="#FFFFFF", corner_radius=8)
        insights_frame.pack(fill="x", padx=30, pady=(10, 20))
        
        insights_title = ctk.CTkLabel(
            insights_frame,
            text="💡 Key Insights:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#1565C0"
        )
        insights_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        # Generate insights
        insights = self._generate_insights(data)
        for insight in insights[:5]:  # Top 5 insights
            insight_label = ctk.CTkLabel(
                insights_frame,
                text=f"• {insight}",
                font=ctk.CTkFont(size=13),
                text_color="#424242",
                wraplength=700,
                justify="left"
            )
            insight_label.pack(anchor="w", padx=30, pady=3)
        
        # Spacing
        ctk.CTkLabel(insights_frame, text="", height=10).pack()
        
        # 2. Success header
        success_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#E8F5E9", corner_radius=10)
        success_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        success_label = ctk.CTkLabel(
            success_frame,
            text="✅ Phân Tích Hoàn Tất!",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#2E7D32"
        )
        success_label.pack(pady=20)
        
        # 3. Video details section
        if videos:
            videos_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#F5F5F5", corner_radius=10)
            videos_frame.pack(fill="x", padx=20, pady=(0, 20))
            
            videos_title = ctk.CTkLabel(
                videos_frame,
                text="📹 PHÂN TÍCH CHI TIẾT TỪNG VIDEO",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#424242"
            )
            videos_title.pack(pady=(15, 10))
            
            # Display each video
            for i, video in enumerate(videos[:20], 1):  # Limit to 20 videos
                video_frame = ctk.CTkFrame(videos_frame, fg_color="white", corner_radius=8)
                video_frame.pack(fill="x", padx=20, pady=5)
                
                # Video info
                video_info = ctk.CTkFrame(video_frame, fg_color="transparent")
                video_info.pack(fill="x", padx=15, pady=10)
                
                # Title
                title_text = f"📹 Video {i}: {video.get('title', 'N/A')[:80]}..."
                title_label = ctk.CTkLabel(
                    video_info,
                    text=title_text,
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color="#212121",
                    anchor="w"
                )
                title_label.pack(fill="x", pady=(0, 5))
                
                # Metrics
                metrics_text = f"👁️ {video.get('view_count', 0):,} views | "
                metrics_text += f"❤️ {video.get('like_count', 0):,} likes | "
                metrics_text += f"💬 {video.get('comment_count', 0):,} comments"
                
                metrics_label = ctk.CTkLabel(
                    video_info,
                    text=metrics_text,
                    font=ctk.CTkFont(size=12),
                    text_color="#666666"
                )
                metrics_label.pack(anchor="w")
                
                # Engagement rate
                if video.get('view_count', 0) > 0:
                    engagement = ((video.get('like_count', 0) + video.get('comment_count', 0)) / 
                                video.get('view_count', 0) * 100)
                    
                    engagement_label = ctk.CTkLabel(
                        video_info,
                        text=f"📊 Tỷ lệ tương tác: {engagement:.2f}%",
                        font=ctk.CTkFont(size=12),
                        text_color="#2196F3"
                    )
                    engagement_label.pack(anchor="w")
        
                if video.get('tags'):
                    tags_text = f"🏷️ Tags: {', '.join(video.get('tags', [])[:5])}"
                    if len(video.get('tags', [])) > 5:
                        tags_text += f" (+{len(video.get('tags', [])) - 5} more)"
                    
                    tags_label = ctk.CTkLabel(
                        video_info,
                        text=tags_text,
                        font=ctk.CTkFont(size=11),
                        text_color="#757575"
                    )
                    tags_label.pack(anchor="w", pady=(2, 0))

        # 4. Additional requirements section
        req_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#FFF3E0", corner_radius=10)
        req_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        req_title = ctk.CTkLabel(
            req_frame,
            text="🎯 Yêu Cầu Phân Tích Bổ Sung",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#E65100"
        )
        req_title.pack(pady=(15, 10))
        
        self.req_text = ctk.CTkTextbox(
            req_frame,
            height=100,
            font=ctk.CTkFont(size=13),
            fg_color="white",
            text_color="#424242"
        )
        self.req_text.pack(fill="x", padx=20, pady=(0, 20))
        self.req_text.insert("1.0", "Nhập yêu cầu bổ sung cho phân tích AI...")
        
        # 5. Action buttons
        buttons_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        # Export buttons
        export_json_btn = ctk.CTkButton(
            buttons_frame,
            text="📥 Xuất JSON",
            command=self.export_json_callback,
            fg_color="#2196F3",
            hover_color="#1976D2",
            width=150,
            height=40
        )
        export_json_btn.pack(side="left", padx=5)
        
        export_csv_btn = ctk.CTkButton(
            buttons_frame,
            text="📊 Xuất CSV",
            command=self.export_csv_callback,
            fg_color="#4CAF50",
            hover_color="#388E3C",
            width=150,
            height=40
        )
        export_csv_btn.pack(side="left", padx=5)
        
        # Create prompts button
        create_prompts_btn = ctk.CTkButton(
            buttons_frame,
            text="✏️ Tạo Prompts →",
            command=self._on_create_prompts,
            fg_color="#FF6B35",
            hover_color="#E55100",
            width=200,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        create_prompts_btn.pack(side="right", padx=5)

    def _show_dynamic_results(self, analysis_data: Dict):
        """Show dynamic AI analysis results."""
        
        # Raw data summary
        raw_data = analysis_data.get('raw_data', {})
        videos = raw_data.get('videos', [])
        
        summary_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#F5F5F5", corner_radius=10)
        summary_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        summary_title = ctk.CTkLabel(
            summary_frame,
            text="📊 Dữ liệu đã phân tích:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#666666"
        )
        summary_title.pack(pady=(15, 10))
        
        summary_text = f"""• Số video phân tích: {len(videos)}
    - Tổng views: {sum(v.get('view_count', 0) for v in videos):,}
    - Tổng likes: {sum(v.get('like_count', 0) for v in videos):,}
    - Tổng comments thu thập: {len(raw_data.get('comments', []))}
    - Tổng transcripts: {len(raw_data.get('transcripts', []))}
    - Điểm viral: {analysis_data.get('viral_score', 0):.1f}/100"""
        
        summary_label = ctk.CTkLabel(
            summary_frame,
            text=summary_text,
            font=ctk.CTkFont(size=13),
            text_color="#666666",
            justify="left"
        )
        summary_label.pack(padx=20, pady=(0, 15))
        
        # AI Response - Main content
        response_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#FFFFFF", corner_radius=10)
        response_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        response_title = ctk.CTkLabel(
            response_frame,
            text="🎯 Phân tích chi tiết:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#2E7D32"
        )
        response_title.pack(anchor="w", padx=20, pady=(20, 15))
        
        # AI response in a text widget
        response_text = ctk.CTkTextbox(
            response_frame,
            font=ctk.CTkFont(size=14),
            fg_color="#FAFAFA",
            text_color="#212121",
            wrap="word",
            height=400
        )
        response_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Insert AI response
        ai_response = analysis_data.get('ai_response', 'Không có phản hồi từ AI')
        response_text.insert("1.0", ai_response)
        response_text.configure(state="disabled")
        
        # Strategy Box - TỰ ĐỘNG TẠO
        strategy_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#E8F5E9", corner_radius=10)
        strategy_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        strategy_title = ctk.CTkLabel(
            strategy_frame,
            text="🚀 Chiến lược để phát triển kênh Youtube cho bạn",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1B5E20"
        )
        strategy_title.pack(pady=(20, 15))
        
        # Loading indicator
        loading_label = ctk.CTkLabel(
            strategy_frame,
            text="🔄 Đang tạo chiến lược phát triển...",
            font=ctk.CTkFont(size=16),
            text_color="#1976D2"
        )
        loading_label.pack(pady=50)
        
        # Update UI first
        #self.update_idletasks()
        
        # Auto generate strategy in background  
        self._auto_generate_strategy(analysis_data, strategy_frame, loading_label)
    
                
        # Additional requirements section (giữ nguyên)
        additional_req_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#FFF3E0", corner_radius=10)
        additional_req_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        additional_req_title = ctk.CTkLabel(
            additional_req_frame,
            text="🎯 Yêu Cầu Phân Tích Bổ Sung",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#E65100"
        )
        additional_req_title.pack(pady=(15, 10))
        
        self.req_text = ctk.CTkTextbox(
            additional_req_frame,
            height=100,
            font=ctk.CTkFont(size=13),
            fg_color="white",
            text_color="#424242"
        )
        self.req_text.pack(fill="x", padx=20, pady=(0, 20))
        self.req_text.insert("1.0", "Nhập yêu cầu bổ sung cho phân tích AI...")
        
        # Action buttons (giữ nguyên)
        buttons_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        # Export buttons
        export_json_btn = ctk.CTkButton(
            buttons_frame,
            text="📥 Xuất JSON",
            command=self.export_json_callback,
            fg_color="#2196F3",
            hover_color="#1976D2",
            width=150,
            height=40
        )
        export_json_btn.pack(side="left", padx=5)
        
        export_csv_btn = ctk.CTkButton(
            buttons_frame,
            text="📊 Xuất CSV",
            command=self.export_csv_callback,
            fg_color="#4CAF50",
            hover_color="#388E3C",
            width=150,
            height=40
        )
        export_csv_btn.pack(side="left", padx=5)
        
        # Create prompts button
        create_prompts_btn = ctk.CTkButton(
            buttons_frame,
            text="✏️ Tạo Prompts →",
            command=self._on_create_prompts,
            fg_color="#FF6B35",
            hover_color="#E55100",
            width=200,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        create_prompts_btn.pack(side="right", padx=5)

    def _auto_generate_strategy(self, analysis_data: Dict, strategy_frame: ctk.CTkFrame, loading_label: ctk.CTkLabel):
        """Auto generate YouTube growth strategy using AI."""
        # Get AI response from analysis
        ai_analysis = analysis_data.get('ai_response', '')
        
        # Prepare strategy prompt
        strategy_prompt = f"""
    Dựa trên phân tích sau:

    {ai_analysis}

    Hãy giúp tôi xây dựng một chiến lược chi tiết để phát triển kênh YouTube, nhằm:
    - Tối ưu nội dung để thu hút cùng tệp khán giả đó
    - Tạo video hấp dẫn hơn các video viral của đối thủ
    - Tăng trưởng subscribers nhanh hơn
    - Tối ưu SEO tốt hơn
    - Xây dựng cộng đồng trung thành
    - Khai thác các điểm yếu của đối thủ

    Chiến lược hãy chia rõ theo từng mục:

    1. **Nội dung nên sản xuất**
       - Chủ đề hot nên làm
       - Công thức tiêu đề viral
       - Thumbnail thu hút
       - Format video hiệu quả

    2. **Tần suất và lịch đăng**
       - Số video/tuần
       - Giờ đăng tối ưu
       - Lịch content cụ thể

    3. **Chiến lược SEO & mô tả**
       - Keywords nên target
       - Cách viết description
       - Tags hiệu quả

    4. **Chiến lược thu hút và giữ chân khán giả**
       - Hook mạnh trong 5s đầu
       - Cách giữ retention rate cao
       - Call-to-action hiệu quả

    5. **Cách sử dụng Shorts & Trends**
       - Loại content phù hợp Shorts
       - Cách catch trends nhanh
       - Tỷ lệ Shorts/Long-form

    6. **Chiến lược tăng tương tác**
       - Kỹ thuật tăng comments
       - Cách encourage likes & shares
       - Community engagement

    7. **Chiến lược thu hút fan trung thành**
       - Community building
       - Exclusive content
       - Fan interaction

    8. **Lợi thế cạnh tranh có thể xây dựng**
       - USP (Unique Selling Points)
       - Differentiation strategy
       - Brand positioning

    Hãy đưa ra chiến lược CỤ THỂ, KHẢ THI với action items rõ ràng cho từng mục.
    """
        
        try:
            # Call OpenAI API
            from openai import OpenAI
            
            # Get OpenAI client from config
            from api_config import get_openai_keys
            openai_keys = get_openai_keys()
            
            if openai_keys:
                client = OpenAI(api_key=openai_keys[0])
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "Bạn là chuyên gia YouTube growth strategy với 10+ năm kinh nghiệm giúp các kênh phát triển. Hãy đưa ra chiến lược cụ thể, khả thi và có thể action ngay."
                        },
                        {
                            "role": "user",
                            "content": strategy_prompt
                        }
                    ],
                    max_tokens=2500,
                    temperature=0.7
                )
                
                strategy_content = response.choices[0].message.content
                self._strategy_content = strategy_content
                
                # Remove loading label
                loading_label.destroy()
                
                # Create content frame
                strategy_content_frame = ctk.CTkFrame(strategy_frame, fg_color="#FFFFFF", corner_radius=8)
                strategy_content_frame.pack(fill="both", padx=20, pady=(0, 20))
                
                # Display strategy
                strategy_text = ctk.CTkTextbox(
                    strategy_content_frame,
                    font=ctk.CTkFont(size=14),
                    fg_color="#FAFAFA",
                    text_color="#212121",
                    wrap="word",
                    height=500
                )
                strategy_text.pack(fill="both", expand=True, padx=15, pady=15)
                strategy_text.insert("1.0", strategy_content)
                strategy_text.configure(state="disabled")
                
                # Add export button
                export_frame = ctk.CTkFrame(strategy_content_frame, fg_color="transparent")
                export_frame.pack(fill="x", padx=15, pady=(0, 15))
                
                export_strategy_btn = ctk.CTkButton(
                    export_frame,
                    text="📥 Xuất Chiến Lược",
                    command=lambda: self._export_strategy(strategy_content),
                    fg_color="#2196F3",
                    hover_color="#1976D2",
                    width=150,
                    height=35
                )
                export_strategy_btn.pack(side="right")
                
            else:
                # No OpenAI key, show error
                loading_label.configure(
                    text="❌ Không thể tạo chiến lược: Thiếu OpenAI API key",
                    text_color="#F44336"
                )
                
        except Exception as e:
            # Show error
            loading_label.configure(
                text=f"❌ Lỗi: {str(e)}",
                text_color="#F44336"
            )
            print(f"Strategy generation error: {e}")

    def _export_strategy(self, content: str):
        """Export strategy to file."""
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"youtube_strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("🚀 CHIẾN LƯỢC PHÁT TRIỂN KÊNH YOUTUBE\n")
                    f.write("="*50 + "\n\n")
                    f.write(f"Ngày tạo: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
                    f.write(content)
                
                messagebox.showinfo("Thành công", f"Đã xuất chiến lược ra file:\n{filename}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xuất file: {str(e)}")

    def _add_action_buttons(self):
        """Add action buttons at the bottom."""
        buttons_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        # Export buttons
        export_json_btn = ctk.CTkButton(
            buttons_frame,
            text="📥 Xuất JSON",
            command=self.export_json_callback,
            fg_color="#2196F3",
            hover_color="#1976D2",
            width=150,
            height=40
        )
        export_json_btn.pack(side="left", padx=5)
        
        export_csv_btn = ctk.CTkButton(
            buttons_frame,
            text="📊 Xuất CSV",
            command=self.export_csv_callback,
            fg_color="#4CAF50",
            hover_color="#388E3C",
            width=150,
            height=40
        )
        export_csv_btn.pack(side="left", padx=5)
    
    def _generate_insights(self, data: Dict) -> list:
        """Generate key insights from analysis data."""
        insights = []
        videos = data.get('videos', [])
        
        if not videos:
            return ["Không có dữ liệu video để phân tích"]
        
        # Best performing video
        best_video = max(videos, key=lambda x: x.get('view_count', 0))
        if best_video:
            insights.append(f"Video có hiệu suất tốt nhất: '{best_video.get('title', 'N/A')[:50]}...' với {best_video.get('view_count', 0):,} lượt xem")
        
        # Average metrics
        avg_views = sum(v.get('view_count', 0) for v in videos) / len(videos)
        insights.append(f"Trung bình {avg_views:,.0f} lượt xem mỗi video")
        
        # Engagement insights
        high_engagement_videos = [v for v in videos if v.get('view_count', 0) > 0 and 
                                 ((v.get('like_count', 0) + v.get('comment_count', 0)) / v.get('view_count', 0) * 100) > 5]
        if high_engagement_videos:
            insights.append(f"{len(high_engagement_videos)} video có tỷ lệ tương tác cao (>5%)")
        
        # Content themes
        comments = data.get('comments', [])
        if comments:
            insights.append(f"Thu thập được {len(comments)} bình luận để phân tích tâm lý audience")
        
        # Viral potential
        viral_score = data.get('viral_score', 0)
        if viral_score >= 70:
            insights.append("🔥 Nội dung có tiềm năng viral cao!")
        elif viral_score >= 50:
            insights.append("📈 Nội dung có tiềm năng phát triển tốt")
        
        return insights
    
    def _on_create_prompts(self):
        """Handle create prompts button click."""
        # Save additional requirements
        self.additional_requirements = self.req_text.get("1.0", "end-1c").strip()
        if self.additional_requirements == "Nhập yêu cầu bổ sung cho phân tích AI...":
            self.additional_requirements = ""
        
        # Call the callback
        self.create_prompts_callback()
    
    def update_progress(self, progress_data: Dict):
        """Update progress display."""
        # Update progress bar
        if 'progress' in progress_data:
            self.progress_bar.set(progress_data['progress'] / 100)
        
        # Update labels
        if 'time_elapsed' in progress_data:
            self.time_label.configure(text=f"⏱️ Thời gian đã qua: {progress_data['time_elapsed']}")
        
        if 'videos_analyzed' in progress_data:
            self.videos_label.configure(text=f"📹 Video đã phân tích: {progress_data['videos_analyzed']}")
        
        if 'comments_collected' in progress_data:
            self.comments_label.configure(text=f"💬 Bình luận đã thu thập: {progress_data['comments_collected']}")
        
        if 'transcripts_collected' in progress_data:
            self.transcripts_label.configure(text=f"📄 Phụ đề đã thu thập: {progress_data['transcripts_collected']}")
        
        if 'current_task' in progress_data:
            self.task_label.configure(text=f"🎯 Tác vụ hiện tại: {progress_data['current_task']}")
    
    def on_complete(self, result_data: Dict):
        """Handle analysis completion."""
        print(f"DEBUG on_complete - result_data keys: {result_data.keys()}")
        print(f"DEBUG on_complete - status: {result_data.get('status')}")
        print(f"DEBUG on_complete - analysis_type: {result_data.get('analysis_type')}")
        
        if result_data.get('status') == 'success':
            # Pass the WHOLE result_data, not just the 'data' part
            self.show_results(result_data)  # ⬅️ Pass full result
        else:
            # Show error
            self.progress_bar.configure(progress_color="#F44336")
            self.task_label.configure(
                text=f"❌ Lỗi: {result_data.get('error', 'Unknown error')}",
                text_color="#F44336"
            )
    
    def show(self):
        """Show the tab."""
        self.container.pack(fill="both", expand=True)
    
    def hide(self):
        """Hide the tab."""
        self.container.pack_forget()