"""
Analysis tab for displaying comprehensive YouTube analysis results
Complete Vietnamese version - Hoàn toàn bằng tiếng Việt
"""

import customtkinter as ctk
from typing import Dict, Optional, Callable
import json
from datetime import datetime
import threading
from tkinter import messagebox, filedialog
import os
import glob

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
        # Title with animation
        
        subtitle_label = ctk.CTkLabel(
            self.container,
            text="Phân tích thời gian thực nội dung YouTube với insights viral (Tối ưu hiệu suất)",
            font=ctk.CTkFont(size=14),
            text_color="#666666"
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Progress section (initially shown)
        self.progress_frame = ctk.CTkFrame(self.container, fg_color="#F8F9FA", corner_radius=12)
        self.progress_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Progress content with better styling
        progress_title = ctk.CTkLabel(
            self.progress_frame,
            text="🔄 Đang Phân Tích Dữ Liệu YouTube...",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#2196F3"
        )
        progress_title.pack(pady=(40, 15))
        
        progress_desc = ctk.CTkLabel(
            self.progress_frame,
            text="Đang xử lý video YouTube, bình luận, phụ đề và tạo AI insights...",
            font=ctk.CTkFont(size=15),
            text_color="#555555",
            wraplength=600
        )
        progress_desc.pack(pady=(0, 25))
        
        # Enhanced progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            width=700,
            height=24,
            progress_color="#4CAF50",
            corner_radius=12
        )
        self.progress_bar.pack(pady=15)
        self.progress_bar.set(0)
        
        # Progress details in grid
        self.progress_details_frame = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        self.progress_details_frame.pack(pady=25)
        
        # Progress labels with icons
        self.time_label = ctk.CTkLabel(
            self.progress_details_frame,
            text="⏱️ Thời gian đã qua: 0:00",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#424242"
        )
        self.time_label.grid(row=0, column=0, padx=25, pady=8)
        
        self.videos_label = ctk.CTkLabel(
            self.progress_details_frame,
            text="📹 Video đã phân tích: 0",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#424242"
        )
        self.videos_label.grid(row=0, column=1, padx=25, pady=8)
        
        self.comments_label = ctk.CTkLabel(
            self.progress_details_frame,
            text="💬 Bình luận đã thu thập: 0",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#424242"
        )
        self.comments_label.grid(row=1, column=0, padx=25, pady=8)
        
        self.transcripts_label = ctk.CTkLabel(
            self.progress_details_frame,
            text="📄 Phụ đề đã trích xuất: 0",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#424242"
        )
        self.transcripts_label.grid(row=1, column=1, padx=25, pady=8)
        
        # Current task with better styling
        self.task_label = ctk.CTkLabel(
            self.progress_frame,
            text="🎯 Tác vụ hiện tại: Đang khởi tạo...",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1976D2"
        )
        self.task_label.pack(pady=(20, 40))
        
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
        """Display comprehensive analysis results."""
        print(f"DEBUG show_results - analysis_data keys: {analysis_data.keys()}")
        print(f"DEBUG show_results - analysis_type: {analysis_data.get('analysis_type')}")
        
        self.analysis_data = analysis_data
        
        # Auto-save results to JSON file
        self._auto_save_results(analysis_data)
        
        # Hide progress, show results
        self.progress_frame.pack_forget()
        self.results_frame.pack(fill="both", expand=True)
        
        # Clear scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Create comprehensive results display
        self._create_comprehensive_results(analysis_data)
            
    def _auto_save_results(self, analysis_data: Dict):
        """Auto-save analysis results to JSON file."""
        try:
            # Create output directory if not exists
            os.makedirs("output/analysis", exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output/analysis/youtube_analysis_{timestamp}.json"
            
            # Prepare data for saving
            save_data = {
                'saved_at': datetime.now().isoformat(),
                'analysis_results': analysis_data,
                'app_version': '2.0',
                'file_type': 'youtube_analysis'
            }
            
            # Save to file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Analysis results auto-saved to: {filename}")
            
            # Show notification in UI
            self._show_save_notification(filename)
            
        except Exception as e:
            print(f"❌ Error auto-saving results: {e}")
    
    def _show_save_notification(self, filename: str):
        """Show save notification in UI."""
        # Add a small notification at the top of results
        notification_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#E8F5E9", corner_radius=8)
        notification_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        notification_label = ctk.CTkLabel(
            notification_frame,
            text=f"💾 Kết quả đã tự động lưu vào: {os.path.basename(filename)}",
            font=ctk.CTkFont(size=12),
            text_color="#2E7D32"
        )
        notification_label.pack(pady=8)
        
    def _create_comprehensive_results(self, analysis_data: Dict):
        """Create comprehensive results display with all sections."""
        
        # Get data - handle both structured and dynamic analysis
        if analysis_data.get('analysis_type') == 'dynamic':
            raw_data = analysis_data.get('raw_data', {})
            ai_response = analysis_data.get('ai_response', '')
        else:
            raw_data = analysis_data.get('data', analysis_data)
            ai_response = None
        
        videos = raw_data.get('video', [])
        comments = raw_data.get('bình luận', [])
        transcripts = raw_data.get('transcripts', [])
        channels = raw_data.get('channels', [])
        viral_score = analysis_data.get('viral_score', raw_data.get('viral_score', 0))
        
        # 1. SUCCESS HEADER
        self._create_success_header(viral_score)
        
        # 2. EXECUTIVE SUMMARY
        self._create_executive_summary(videos, comments, transcripts, viral_score, channels)
        
        # 3. KEY PERFORMANCE METRICS
        self._create_performance_metrics(videos, comments)
        
        # 4. TOP PERFORMING CONTENT
        self._create_top_content_section(videos)
        
        # 5. AUDIENCE INSIGHTS
        self._create_audience_insights(comments, videos)
        
        # 6. CONTENT ANALYSIS
        self._create_content_analysis(transcripts, videos)
        
        # 7. AI INSIGHTS (if available)
        if ai_response:
            self._create_ai_insights_section(ai_response)
            
        # 8. VIRAL POTENTIAL ANALYSIS
        self._create_viral_analysis(viral_score, videos)
        
        # 9. STRENGTHS & OPPORTUNITIES
        self._create_strengths_opportunities(videos, comments, viral_score)
        
        # 10. ACTIONABLE RECOMMENDATIONS
        self._create_recommendations(videos, comments, viral_score)
        
        # 11. DETAILED VIDEO BREAKDOWN
        self._create_detailed_breakdown(videos, comments, transcripts)
        
        # 12. ADDITIONAL REQUIREMENTS
        self._create_additional_requirements()
        
        # 13. ACTION BUTTONS (Modified)
        self._create_action_buttons()
        
    def _create_success_header(self, viral_score: float):
        """Create success header with viral score."""
        header_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#E8F5E9", corner_radius=15)
        header_frame.pack(fill="x", padx=20, pady=(0, 25))
        
        # Success icon and title
        success_title = ctk.CTkLabel(
            header_frame,
            text="✅ Phân Tích Hoàn Tất!",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#2E7D32"
        )
        success_title.pack(pady=(20, 10))
        
        # Viral score display
        if viral_score >= 70:
            score_color = "#4CAF50"
            score_emoji = "🔥"
            score_text = "Tiềm Năng Viral Cao!"
        elif viral_score >= 50:
            score_color = "#FF9800"
            score_emoji = "📈"
            score_text = "Tiềm Năng Tăng Trưởng Tốt"
        else:
            score_color = "#F44336"
            score_emoji = "💡"
            score_text = "Cơ Hội Cải Thiện"
        
        score_frame = ctk.CTkFrame(header_frame, fg_color="white", corner_radius=10)
        score_frame.pack(padx=30, pady=(0, 20))
        
        score_label = ctk.CTkLabel(
            score_frame,
            text=f"{score_emoji} Điểm Viral: {viral_score:.1f}/100",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=score_color
        )
        score_label.pack(pady=15)
        
        score_desc = ctk.CTkLabel(
            score_frame,
            text=score_text,
            font=ctk.CTkFont(size=14),
            text_color="#666666"
        )
        score_desc.pack(pady=(0, 15))
        
    def _create_executive_summary(self, videos: list, comments: list, transcripts: list, viral_score: float, channels: list):
        """Create executive summary section."""
        summary_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#F3E5F5", corner_radius=15)
        summary_frame.pack(fill="x", padx=20, pady=(0, 25))
        
        summary_title = ctk.CTkLabel(
            summary_frame,
            text="📊 TÓM TẮT ĐIỀU HÀNH",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#7B1FA2"
        )
        summary_title.pack(pady=(20, 15))
        
        # Summary stats in grid
        stats_frame = ctk.CTkFrame(summary_frame, fg_color="white", corner_radius=10)
        stats_frame.pack(fill="x", padx=25, pady=(0, 20))
        
        # Calculate summary metrics
        total_views = sum(v.get('view_count', 0) for v in videos)
        total_likes = sum(v.get('like_count', 0) for v in videos)
        total_video_comments = sum(v.get('comment_count', 0) for v in videos)
        avg_views = total_views / len(videos) if videos else 0
        avg_engagement = sum((v.get('like_count', 0) + v.get('comment_count', 0)) / v.get('view_count', 1) * 100 
                           for v in videos if v.get('view_count', 0) > 0) / len(videos) if videos else 0
        
        # Channel info
        channel_names = list(set(v.get('channel_title', 'Không rõ') for v in videos if v.get('channel_title')))
        channels_text = ", ".join(channel_names[:3])
        if len(channel_names) > 3:
            channels_text += f" và {len(channel_names) - 3} kênh khác"
        
        summary_stats = [
            ("🎬 Kênh Đã Phân Tích", channels_text or "Không có"),
            ("📹 Tổng Số Video", f"{len(videos):,}"),
            ("👁️ Tổng Lượt Xem", f"{total_views:,}"),
            ("❤️ Tổng Lượt Thích", f"{total_likes:,}"),
            ("💬 Bình Luận Đã Thu Thập", f"{len(comments):,}"),
            ("📄 Phụ Đề Đã Trích Xuất", f"{len(transcripts):,}"),
            ("📊 Trung Bình Lượt Xem/Video", f"{avg_views:,.0f}"),
            ("🎯 Tỷ Lệ Tương Tác Trung Bình", f"{avg_engagement:.2f}%"),
        ]
        
        # Display in 2x4 grid
        for i, (label, value) in enumerate(summary_stats):
            row = i // 2
            col = i % 2
            
            stat_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
            stat_frame.grid(row=row, column=col, padx=20, pady=10, sticky="w")
            
            label_widget = ctk.CTkLabel(
                stat_frame,
                text=label + ":",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#424242"
            )
            label_widget.pack(side="left", padx=(0, 10))
            
            value_widget = ctk.CTkLabel(
                stat_frame,
                text=value,
                font=ctk.CTkFont(size=14),
                text_color="#1976D2"
            )
            value_widget.pack(side="left")
        
    def _create_performance_metrics(self, videos: list, comments: list):
        """Create performance metrics section."""
        metrics_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#E3F2FD", corner_radius=15)
        metrics_frame.pack(fill="x", padx=20, pady=(0, 25))
        
        metrics_title = ctk.CTkLabel(
            metrics_frame,
            text="📈 CHỈ SỐ HIỆU SUẤT CHÍNH",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1565C0"
        )
        metrics_title.pack(pady=(20, 15))
        
        if not videos:
            no_data_label = ctk.CTkLabel(
                metrics_frame,
                text="Không có dữ liệu video để tính toán chỉ số",
                font=ctk.CTkFont(size=14),
                text_color="#666666"
            )
            no_data_label.pack(pady=20)
            return
        
        # Calculate advanced metrics
        view_counts = [v.get('view_count', 0) for v in videos]
        engagement_rates = []
        
        for video in videos:
            views = video.get('view_count', 0)
            if views > 0:
                engagement = ((video.get('like_count', 0) + video.get('comment_count', 0)) / views) * 100
                engagement_rates.append(engagement)
        
        # Metrics calculations
        max_views = max(view_counts) if view_counts else 0
        min_views = min(view_counts) if view_counts else 0
        median_views = sorted(view_counts)[len(view_counts)//2] if view_counts else 0
        avg_engagement = sum(engagement_rates) / len(engagement_rates) if engagement_rates else 0
        max_engagement = max(engagement_rates) if engagement_rates else 0
        
        # High performers
        high_performers = [v for v in videos if v.get('view_count', 0) > median_views * 1.5]
        viral_videos = [v for v in videos if v.get('view_count', 0) > max_views * 0.8]
        
        metrics_content = ctk.CTkFrame(metrics_frame, fg_color="white", corner_radius=10)
        metrics_content.pack(fill="x", padx=25, pady=(0, 20))
        
        metrics_data = [
            ("📊 Phân Phối Hiệu Suất", ""),
            ("   • Lượt Xem Cao Nhất", f"{max_views:,}"),
            ("   • Lượt Xem Trung Vị", f"{median_views:,}"),
            ("   • Lượt Xem Thấp Nhất", f"{min_views:,}"),
            ("", ""),
            ("🎯 Phân Tích Tương Tác", ""),
            ("   • Tương Tác Trung Bình", f"{avg_engagement:.2f}%"),
            ("   • Tương Tác Đỉnh", f"{max_engagement:.2f}%"),
            ("   • Video Hiệu Suất Cao", f"{len(high_performers)} video"),
            ("   • Ứng Viên Viral", f"{len(viral_videos)} video"),
        ]
        
        for label, value in metrics_data:
            if not label:  # Spacer
                ctk.CTkLabel(metrics_content, text="", height=5).pack()
                continue
                
            metric_frame = ctk.CTkFrame(metrics_content, fg_color="transparent")
            metric_frame.pack(fill="x", padx=20, pady=3)
            
            if not value:  # Section header
                header_label = ctk.CTkLabel(
                    metric_frame,
                    text=label,
                    font=ctk.CTkFont(size=15, weight="bold"),
                    text_color="#1565C0"
                )
                header_label.pack(anchor="w")
            else:
                metric_label = ctk.CTkLabel(
                    metric_frame,
                    text=f"{label}: {value}",
                    font=ctk.CTkFont(size=13),
                    text_color="#424242"
                )
                metric_label.pack(anchor="w")
        
    def _create_top_content_section(self, videos: list):
        """Create top performing content section."""
        top_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#FFF3E0", corner_radius=15)
        top_frame.pack(fill="x", padx=20, pady=(0, 25))
        
        top_title = ctk.CTkLabel(
            top_frame,
            text="🏆 NỘI DUNG HIỆU SUẤT CAO NHẤT",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#E65100"
        )
        top_title.pack(pady=(20, 15))
        
        if not videos:
            return
        
        # Sort videos by views
        sorted_videos = sorted(videos, key=lambda x: x.get('view_count', 0), reverse=True)
        top_videos = sorted_videos[:5]  # Show top 5
        
        for i, video in enumerate(top_videos, 1):
            video_frame = ctk.CTkFrame(top_frame, fg_color="white", corner_radius=10)
            video_frame.pack(fill="x", padx=25, pady=8)
            
            # Video header
            header_frame = ctk.CTkFrame(video_frame, fg_color="transparent")
            header_frame.pack(fill="x", padx=15, pady=(10, 5))
            
            rank_label = ctk.CTkLabel(
                header_frame,
                text=f"#{i}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#FF6B35",
                width=40
            )
            rank_label.pack(side="left")
            
            title_label = ctk.CTkLabel(
                header_frame,
                text=video.get('title', 'Không có')[:80] + ("..." if len(video.get('title', '')) > 80 else ""),
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#212121",
                anchor="w"
            )
            title_label.pack(side="left", fill="x", expand=True, padx=(10, 0))
            
            # Metrics
            metrics_frame = ctk.CTkFrame(video_frame, fg_color="transparent")
            metrics_frame.pack(fill="x", padx=15, pady=(0, 10))
            
            views = video.get('view_count', 0)
            likes = video.get('like_count', 0)
            comments = video.get('comment_count', 0)
            engagement = ((likes + comments) / views * 100) if views > 0 else 0
            
            metrics_text = f"👁️ {views:,} lượt xem  •  ❤️ {likes:,} thích  •  💬 {comments:,} bình luận  •  📊 {engagement:.2f}% tương tác"
            
            metrics_label = ctk.CTkLabel(
                metrics_frame,
                text=metrics_text,
                font=ctk.CTkFont(size=12),
                text_color="#666666"
            )
            metrics_label.pack(anchor="w", padx=35)
    
    def _create_audience_insights(self, comments: list, videos: list):
        """Create audience insights section."""
        audience_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#E8F5E9", corner_radius=15)
        audience_frame.pack(fill="x", padx=20, pady=(0, 25))
        
        audience_title = ctk.CTkLabel(
            audience_frame,
            text="👥 INSIGHTS KHÁN GIẢ",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#2E7D32"
        )
        audience_title.pack(pady=(20, 15))
        
        insights_content = ctk.CTkFrame(audience_frame, fg_color="white", corner_radius=10)
        insights_content.pack(fill="x", padx=25, pady=(0, 20))
        
        if not comments:
            no_comments_label = ctk.CTkLabel(
                insights_content,
                text="Không có bình luận để phân tích khán giả",
                font=ctk.CTkFont(size=14),
                text_color="#666666"
            )
            no_comments_label.pack(pady=20)
            return
        
        # Sentiment analysis - Vietnamese keywords
        positive_keywords = ['thích', 'tuyệt vời', 'hay', 'tốt', 'xuất sắc', 'cảm ơn', 'love', 'great', 'amazing', 'awesome', 'helpful', 'thank', 'best', 'perfect']
        negative_keywords = ['ghét', 'tệ', 'dở', 'chán', 'không hay', 'hate', 'bad', 'terrible', 'worst', 'boring', 'useless']
        
        positive_count = sum(1 for c in comments if any(word in c.get('text', '').lower() for word in positive_keywords))
        negative_count = sum(1 for c in comments if any(word in c.get('text', '').lower() for word in negative_keywords))
        
        total_comments = len(comments)
        positive_pct = (positive_count / total_comments * 100) if total_comments > 0 else 0
        negative_pct = (negative_count / total_comments * 100) if total_comments > 0 else 0
        
        # Top comments by likes
        top_comments = sorted(comments, key=lambda x: x.get('like_count', 0), reverse=True)[:3]
        
        audience_insights = [
            ("📊 Phân Tích Cảm Xúc", ""),
            ("   • Bình Luận Tích Cực", f"{positive_count} ({positive_pct:.1f}%)"),
            ("   • Bình Luận Tiêu Cực", f"{negative_count} ({negative_pct:.1f}%)"),
            ("", ""),
            ("💬 Bình Luận Hàng Đầu Theo Tương Tác", ""),
        ]
        
        # Add insights to UI
        for label, value in audience_insights:
            if not label:
                ctk.CTkLabel(insights_content, text="", height=5).pack()
                continue
                
            insight_frame = ctk.CTkFrame(insights_content, fg_color="transparent")
            insight_frame.pack(fill="x", padx=20, pady=3)
            
            if not value:
                header_label = ctk.CTkLabel(
                    insight_frame,
                    text=label,
                    font=ctk.CTkFont(size=15, weight="bold"),
                    text_color="#2E7D32"
                )
                header_label.pack(anchor="w")
            else:
                insight_label = ctk.CTkLabel(
                    insight_frame,
                    text=f"{label}: {value}",
                    font=ctk.CTkFont(size=13),
                    text_color="#424242"
                )
                insight_label.pack(anchor="w")
        
        # Show top comments
        for i, comment in enumerate(top_comments, 1):
            comment_frame = ctk.CTkFrame(insights_content, fg_color="#F5F5F5", corner_radius=8)
            comment_frame.pack(fill="x", padx=20, pady=5)
            
            comment_text = comment.get('text', '')[:100] + ("..." if len(comment.get('text', '')) > 100 else "")
            comment_likes = comment.get('like_count', 0)
            
            comment_label = ctk.CTkLabel(
                comment_frame,
                text=f"{i}. \"{comment_text}\" ({comment_likes} thích)",
                font=ctk.CTkFont(size=12),
                text_color="#333333",
                wraplength=600,
                justify="left"
            )
            comment_label.pack(padx=15, pady=8, anchor="w")
    
    def _create_content_analysis(self, transcripts: list, videos: list):
        """Create content analysis section."""
        content_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#F3E5F5", corner_radius=15)
        content_frame.pack(fill="x", padx=20, pady=(0, 25))
        
        content_title = ctk.CTkLabel(
            content_frame,
            text="📝 PHÂN TÍCH NỘI DUNG",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#7B1FA2"
        )
        content_title.pack(pady=(20, 15))
        
        analysis_content = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=10)
        analysis_content.pack(fill="x", padx=25, pady=(0, 20))
        
        if not transcripts and not videos:
            no_content_label = ctk.CTkLabel(
                analysis_content,
                text="Không có dữ liệu nội dung để phân tích",
                font=ctk.CTkFont(size=14),
                text_color="#666666"
            )
            no_content_label.pack(pady=20)
            return
        
        # Duration analysis
        durations = []
        for video in videos:
            duration_str = video.get('duration', '')
            if duration_str and ':' in duration_str:
                try:
                    if duration_str.count(':') == 1:  # MM:SS
                        minutes, seconds = map(int, duration_str.split(':'))
                        total_seconds = minutes * 60 + seconds
                    else:  # HH:MM:SS or PT format
                        if duration_str.startswith('PT'):
                            # Skip PT format parsing for now
                            continue
                        parts = list(map(int, duration_str.split(':')))
                        total_seconds = parts[0] * 3600 + parts[1] * 60 + parts[2]
                    durations.append(total_seconds)
                except:
                    pass
        
        # Language analysis from transcripts
        languages = {}
        total_transcript_words = 0
        
        for transcript in transcripts:
            lang = transcript.get('language', 'không rõ')
            languages[lang] = languages.get(lang, 0) + 1
            
            text = transcript.get('full_text', '')
            word_count = len(text.split()) if text else 0
            total_transcript_words += word_count
        
        # Content insights
        avg_duration = sum(durations) / len(durations) if durations else 0
        avg_duration_min = avg_duration / 60
        
        content_insights = [
            ("⏱️ Phân Tích Thời Lượng", ""),
            ("   • Thời Lượng Trung Bình", f"{avg_duration_min:.1f} phút"),
            ("   • Tổng Video Có Thời Lượng", f"{len(durations)}"),
            ("", ""),
            ("🗣️ Phân Tích Ngôn Ngữ & Phụ Đề", ""),
            ("   • Video Có Phụ Đề", f"{len(transcripts)}"),
            ("   • Tổng Từ Đã Phân Tích", f"{total_transcript_words:,}"),
        ]
        
        # Display content insights
        for label, value in content_insights:
            if not label:
                ctk.CTkLabel(analysis_content, text="", height=5).pack()
                continue
                
            insight_frame = ctk.CTkFrame(analysis_content, fg_color="transparent")
            insight_frame.pack(fill="x", padx=20, pady=3)
            
            if not value:
                header_label = ctk.CTkLabel(
                    insight_frame,
                    text=label,
                    font=ctk.CTkFont(size=15, weight="bold"),
                    text_color="#7B1FA2"
                )
                header_label.pack(anchor="w")
            else:
                insight_label = ctk.CTkLabel(
                    insight_frame,
                    text=f"{label}: {value}",
                    font=ctk.CTkFont(size=13),
                    text_color="#424242"
                )
                insight_label.pack(anchor="w")
    
    def _create_ai_insights_section(self, ai_response: str):
        """Create AI insights section for dynamic analysis."""
        ai_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#E1F5FE", corner_radius=15)
        ai_frame.pack(fill="x", padx=20, pady=(0, 25))
        
        ai_title = ctk.CTkLabel(
            ai_frame,
            text="🤖 AI INSIGHTS & PHÂN TÍCH",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#0277BD"
        )
        ai_title.pack(pady=(20, 15))
        
        # AI response display
        ai_text_frame = ctk.CTkFrame(ai_frame, fg_color="white", corner_radius=10)
        ai_text_frame.pack(fill="x", padx=25, pady=(0, 20))
        
        ai_textbox = ctk.CTkTextbox(
            ai_text_frame,
            height=300,
            font=ctk.CTkFont(size=14),
            fg_color="#FAFAFA",
            text_color="#212121",
            wrap="word"
        )
        ai_textbox.pack(fill="both", expand=True, padx=15, pady=15)
        ai_textbox.insert("1.0", ai_response)
        ai_textbox.configure(state="disabled")
    
    def _create_viral_analysis(self, viral_score: float, videos: list):
        """Create viral potential analysis section."""
        viral_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#FFF8E1", corner_radius=15)
        viral_frame.pack(fill="x", padx=20, pady=(0, 25))
        
        viral_title = ctk.CTkLabel(
            viral_frame,
            text="🔥 PHÂN TÍCH TIỀM NĂNG VIRAL",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#F57F17"
        )
        viral_title.pack(pady=(20, 15))
        
        viral_content = ctk.CTkFrame(viral_frame, fg_color="white", corner_radius=10)
        viral_content.pack(fill="x", padx=25, pady=(0, 20))
        
        # Viral score breakdown
        score_breakdown = self._calculate_viral_breakdown(viral_score, videos)
        
        viral_insights = [
            ("📊 Điểm Viral Tổng Thể", f"{viral_score:.1f}/100"),
            ("", ""),
            ("🎯 Phân Tích Điểm Số", ""),
            ("   • Chất Lượng Nội Dung", f"{score_breakdown['content']:.1f}/25"),
            ("   • Tỷ Lệ Tương Tác", f"{score_breakdown['tương tác']:.1f}/25"),
            ("   • Tiềm Năng Tăng Trưởng", f"{score_breakdown['growth']:.1f}/25"),
            ("   • Sức Hấp Dẫn Khán Giả", f"{score_breakdown['appeal']:.1f}/25"),
        ]
        
        # Display viral insights
        for label, value in viral_insights:
            if not label:
                ctk.CTkLabel(viral_content, text="", height=5).pack()
                continue
                
            insight_frame = ctk.CTkFrame(viral_content, fg_color="transparent")
            insight_frame.pack(fill="x", padx=20, pady=3)
            
            if not value:
                header_label = ctk.CTkLabel(
                    insight_frame,
                    text=label,
                    font=ctk.CTkFont(size=15, weight="bold"),
                    text_color="#F57F17"
                )
                header_label.pack(anchor="w")
            else:
                insight_label = ctk.CTkLabel(
                    insight_frame,
                    text=f"{label}: {value}",
                    font=ctk.CTkFont(size=13),
                    text_color="#424242"
                )
                insight_label.pack(anchor="w")
    
    def _calculate_viral_breakdown(self, viral_score: float, videos: list) -> dict:
        """Calculate breakdown of viral score components."""
        # Simple breakdown - in real implementation, this would use the actual algorithm
        content_score = min(viral_score * 0.3, 25)
        engagement_score = min(viral_score * 0.25, 25)
        growth_score = min(viral_score * 0.25, 25)
        appeal_score = min(viral_score * 0.2, 25)
        
        return {
            'content': content_score,
            'tương tác': engagement_score,
            'growth': growth_score,
            'appeal': appeal_score
        }
    
    def _create_strengths_opportunities(self, videos: list, comments: list, viral_score: float):
        """Create strengths and opportunities section."""
        so_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#E8EAF6", corner_radius=15)
        so_frame.pack(fill="x", padx=20, pady=(0, 25))
        
        so_title = ctk.CTkLabel(
            so_frame,
            text="⚡ ĐIỂM MẠNH & CƠ HỘI",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#3F51B5"
        )
        so_title.pack(pady=(20, 15))
        
        # Create two columns
        columns_frame = ctk.CTkFrame(so_frame, fg_color="transparent")
        columns_frame.pack(fill="x", padx=25, pady=(0, 20))
        
        # Strengths column
        strengths_frame = ctk.CTkFrame(columns_frame, fg_color="#E8F5E9", corner_radius=10)
        strengths_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        strengths_title = ctk.CTkLabel(
            strengths_frame,
            text="💪 ĐIỂM MẠNH",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#2E7D32"
        )
        strengths_title.pack(pady=(15, 10))
        
        # Calculate strengths
        strengths = self._identify_strengths(videos, comments, viral_score)
        for strength in strengths:
            strength_label = ctk.CTkLabel(
                strengths_frame,
                text=f"✅ {strength}",
                font=ctk.CTkFont(size=13),
                text_color="#424242",
                wraplength=250,
                justify="left"
            )
            strength_label.pack(anchor="w", padx=15, pady=3)
        
        ctk.CTkLabel(strengths_frame, text="", height=10).pack()
        
        # Opportunities column
        opportunities_frame = ctk.CTkFrame(columns_frame, fg_color="#FFF3E0", corner_radius=10)
        opportunities_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        opportunities_title = ctk.CTkLabel(
            opportunities_frame,
            text="🎯 CƠ HỘI",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#E65100"
        )
        opportunities_title.pack(pady=(15, 10))
        
        # Calculate opportunities
        opportunities = self._identify_opportunities(videos, comments, viral_score)
        for opportunity in opportunities:
            opportunity_label = ctk.CTkLabel(
                opportunities_frame,
                text=f"🔸 {opportunity}",
                font=ctk.CTkFont(size=13),
                text_color="#424242",
                wraplength=250,
                justify="left"
            )
            opportunity_label.pack(anchor="w", padx=15, pady=3)
        
        ctk.CTkLabel(opportunities_frame, text="", height=10).pack()
    
    def _identify_strengths(self, videos: list, comments: list, viral_score: float) -> list:
        """Identify content strengths."""
        strengths = []
        
        if not videos:
            return ["Cần dữ liệu video để phân tích"]
        
        # Calculate metrics
        avg_views = sum(v.get('view_count', 0) for v in videos) / len(videos)
        high_engagement_videos = [v for v in videos if v.get('view_count', 0) > 0 and 
                                 ((v.get('like_count', 0) + v.get('comment_count', 0)) / v.get('view_count', 0) * 100) > 3]
        
        if viral_score >= 70:
            strengths.append("Nội dung có tiềm năng viral cao")
        if avg_views > 10000:
            strengths.append("Hiệu suất lượt xem mạnh")
        if len(high_engagement_videos) > len(videos) * 0.3:
            strengths.append("Tương tác khán giả tốt")
        if len(comments) > len(videos) * 10:
            strengths.append("Tương tác cộng đồng tích cực")
        if len(videos) >= 10:
            strengths.append("Tạo nội dung nhất quán")
        
        # Add more based on data
        positive_sentiment = sum(1 for c in comments if any(word in c.get('text', '').lower() 
                               for word in ['thích', 'tuyệt', 'hay', 'tốt', 'love', 'great', 'amazing']))
        if positive_sentiment > len(comments) * 0.2:
            strengths.append("Cảm xúc khán giả tích cực")
        
        if not strengths:
            strengths = ["Đang xây dựng nền tảng nội dung", "Thu thập insights khán giả", "Học hỏi động lực nền tảng"]
        
        return strengths[:6]  # Max 6 strengths
    
    def _identify_opportunities(self, videos: list, comments: list, viral_score: float) -> list:
        """Identify improvement opportunities."""
        opportunities = []
        
        if not videos:
            return ["Thu thập thêm dữ liệu video để phân tích"]
        
        # Calculate metrics for opportunities
        avg_views = sum(v.get('view_count', 0) for v in videos) / len(videos)
        avg_engagement = sum((v.get('like_count', 0) + v.get('comment_count', 0)) / v.get('view_count', 1) * 100 
                           for v in videos if v.get('view_count', 0) > 0) / len(videos) if videos else 0
        
        if viral_score < 50:
            opportunities.append("Cải thiện tiềm năng viral nội dung")
        if avg_engagement < 2:
            opportunities.append("Tăng tương tác khán giả")
        if avg_views < 5000:
            opportunities.append("Tối ưu để tăng độ phủ")
        if len(comments) < len(videos) * 5:
            opportunities.append("Xây dựng cộng đồng mạnh hơn")
        
        if not opportunities:
            opportunities = ["Mở rộng đa dạng nội dung", "Tối ưu lịch đăng bài", "Cải thiện thumbnail và tiêu đề"]
        
        return opportunities[:6]  # Max 6 opportunities
    
    def _create_recommendations(self, videos: list, comments: list, viral_score: float):
        """Create actionable recommendations section."""
        rec_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#F1F8E9", corner_radius=15)
        rec_frame.pack(fill="x", padx=20, pady=(0, 25))
        
        rec_title = ctk.CTkLabel(
            rec_frame,
            text="🎯 KHUYẾN NGHỊ CÓ THỂ THỰC HIỆN",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#33691E"
        )
        rec_title.pack(pady=(20, 15))
        
        rec_content = ctk.CTkFrame(rec_frame, fg_color="white", corner_radius=10)
        rec_content.pack(fill="x", padx=25, pady=(0, 20))
        
        # Generate recommendations based on analysis
        recommendations = self._generate_recommendations(videos, comments, viral_score)
        
        for i, (category, rec_list) in enumerate(recommendations.items(), 1):
            # Category header
            cat_frame = ctk.CTkFrame(rec_content, fg_color="transparent")
            cat_frame.pack(fill="x", padx=20, pady=(15 if i > 1 else 10, 5))
            
            cat_label = ctk.CTkLabel(
                cat_frame,
                text=f"{i}. {category}",
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color="#33691E"
            )
            cat_label.pack(anchor="w")
            
            # Recommendations
            for rec in rec_list:
                rec_frame_item = ctk.CTkFrame(rec_content, fg_color="transparent")
                rec_frame_item.pack(fill="x", padx=40, pady=2)
                
                rec_label = ctk.CTkLabel(
                    rec_frame_item,
                    text=f"• {rec}",
                    font=ctk.CTkFont(size=13),
                    text_color="#424242",
                    wraplength=600,
                    justify="left"
                )
                rec_label.pack(anchor="w")
        
        ctk.CTkLabel(rec_content, text="", height=10).pack()
    
    def _generate_recommendations(self, videos: list, comments: list, viral_score: float) -> dict:
        """Generate actionable recommendations."""
        recommendations = {}
        
        # Content optimization
        content_recs = []
        if viral_score < 60:
            content_recs.extend([
                "Phân tích video hiệu suất cao để xác định yếu tố thành công",
                "Tạo thumbnail hấp dẫn hơn với màu sắc sáng và text rõ ràng",
                "Cải thiện hook video - làm cho 15 giây đầu thú vị hơn"
            ])
        
        recommendations["Tối Ưu Nội Dung"] = content_recs[:3]
        
        # Audience engagement
        engagement_recs = [
            "Phản hồi bình luận trong vài giờ đầu sau khi đăng",
            "Tạo bài đăng cộng đồng để duy trì tương tác giữa các video",
            "Sử dụng poll và câu hỏi trong tab cộng đồng"
        ]
        
        recommendations["Tương Tác Khán Giả"] = engagement_recs[:3]
        
        # Growth strategy
        growth_recs = [
            "Tối ưu lịch đăng dựa trên hoạt động khán giả",
            "Tạo YouTube Shorts để tăng khả năng được phát hiện",
            "Hợp tác với creator cùng lĩnh vực"
        ]
        
        recommendations["Chiến Lược Tăng Trưởng"] = growth_recs[:3]
        
        return recommendations
    
    def _create_detailed_breakdown(self, videos: list, comments: list, transcripts: list):
        """Create detailed video breakdown section."""
        breakdown_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#FAFAFA", corner_radius=15)
        breakdown_frame.pack(fill="x", padx=20, pady=(0, 25))
        
        breakdown_title = ctk.CTkLabel(
            breakdown_frame,
            text="📋 PHÂN TÍCH CHI TIẾT VIDEO",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#424242"
        )
        breakdown_title.pack(pady=(20, 15))
        
        if not videos:
            no_videos_label = ctk.CTkLabel(
                breakdown_frame,
                text="Không có video để phân tích chi tiết",
                font=ctk.CTkFont(size=14),
                text_color="#666666"
            )
            no_videos_label.pack(pady=20)
            return
        
        # Show pagination info
        total_videos = len(videos)
        show_count = min(10, total_videos)  # Show top 10
        
        pagination_label = ctk.CTkLabel(
            breakdown_frame,
            text=f"Hiển thị top {show_count} trên {total_videos} video (Tối ưu hiệu suất)",
            font=ctk.CTkFont(size=13),
            text_color="#666666"
        )
        pagination_label.pack(pady=(0, 15))
        
        # Video breakdown list
        breakdown_content = ctk.CTkFrame(breakdown_frame, fg_color="white", corner_radius=10)
        breakdown_content.pack(fill="x", padx=25, pady=(0, 20))
        
        # Sort by views and show top videos
        sorted_videos = sorted(videos, key=lambda x: x.get('view_count', 0), reverse=True)
        
        for i, video in enumerate(sorted_videos[:show_count], 1):
            self._create_video_breakdown_item(breakdown_content, i, video, comments, transcripts)
        
        # Show more button if needed
        if total_videos > show_count:
            more_label = ctk.CTkLabel(
                breakdown_frame,
                text=f"🔽 {total_videos - show_count} video khác có trong file phân tích đã lưu",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#2196F3"
            )
            more_label.pack(pady=(0, 20))
    
    def _create_video_breakdown_item(self, parent: ctk.CTkFrame, index: int, video: dict, 
                                   comments: list, transcripts: list):
        """Create individual video breakdown item."""
        video_frame = ctk.CTkFrame(parent, fg_color="#F8F9FA", corner_radius=8)
        video_frame.pack(fill="x", padx=15, pady=8)
        
        # Video header
        header_frame = ctk.CTkFrame(video_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(12, 8))
        
        # Index and title
        index_label = ctk.CTkLabel(
            header_frame,
            text=f"#{index}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FF6B35",
            width=35
        )
        index_label.pack(side="left")
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=video.get('title', 'Không có')[:70] + ("..." if len(video.get('title', '')) > 70 else ""),
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#212121",
            anchor="w"
        )
        title_label.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        # Metrics row
        metrics_frame = ctk.CTkFrame(video_frame, fg_color="transparent")
        metrics_frame.pack(fill="x", padx=15, pady=(0, 12))
        
        views = video.get('view_count', 0)
        likes = video.get('like_count', 0)
        video_comments = video.get('comment_count', 0)
        engagement = ((likes + video_comments) / views * 100) if views > 0 else 0
        
        metrics_text = f"👁️ {views:,}  •  ❤️ {likes:,}  •  💬 {video_comments:,}  •  📊 {engagement:.2f}%"
        
        metrics_label = ctk.CTkLabel(
            metrics_frame,
            text=metrics_text,
            font=ctk.CTkFont(size=12),
            text_color="#666666"
        )
        metrics_label.pack(anchor="w", padx=45)
    
    def _create_additional_requirements(self):
        """Create additional requirements section."""
        req_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#FFF3E0", corner_radius=15)
        req_frame.pack(fill="x", padx=20, pady=(0, 25))
        
        req_title = ctk.CTkLabel(
            req_frame,
            text="🎯 Yêu Cầu Phân Tích Bổ Sung",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#E65100"
        )
        req_title.pack(pady=(20, 15))
        
        req_desc = ctk.CTkLabel(
            req_frame,
            text="Thêm yêu cầu cụ thể cho phân tích AI hoặc insights tùy chỉnh bạn cần:",
            font=ctk.CTkFont(size=14),
            text_color="#666666"
        )
        req_desc.pack(padx=25, pady=(0, 10))
        
        self.req_text = ctk.CTkTextbox(
            req_frame,
            height=120,
            font=ctk.CTkFont(size=13),
            fg_color="white",
            text_color="#424242",
            border_width=2,
            border_color="#E0E0E0"
        )
        self.req_text.pack(fill="x", padx=25, pady=(0, 25))
        self.req_text.insert("1.0", "Nhập yêu cầu bổ sung cho phân tích AI...")
    
    def _create_action_buttons(self):
        """Create action buttons section - Vietnamese version."""
        buttons_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 30))
        
        # Left side - Load Previous Results button
        load_btn = ctk.CTkButton(
            buttons_frame,
            text="📁 Tải Kết Quả Cũ",
            command=self._load_previous_results,
            fg_color="#9C27B0",
            hover_color="#7B1FA2",
            width=200,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        load_btn.pack(side="left")
        
        # Right side - Create prompts button
        create_prompts_btn = ctk.CTkButton(
            buttons_frame,
            text="✏️ Tạo AI Prompts →",
            command=self._on_create_prompts,
            fg_color="#FF6B35",
            hover_color="#E55100",
            width=220,
            height=55,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=12
        )
        create_prompts_btn.pack(side="right")
    
    def _load_previous_results(self):
        """Load and display previous analysis results."""
        try:
            # Check if output/analysis directory exists
            analysis_dir = "output/analysis"
            if not os.path.exists(analysis_dir):
                messagebox.showinfo(
                    "Không Có Kết Quả Cũ", 
                    "Không tìm thấy kết quả phân tích cũ.\nChạy phân tích trước để lưu kết quả."
                )
                return
            
            # Get all JSON files in analysis directory
            json_files = glob.glob(os.path.join(analysis_dir, "youtube_analysis_*.json"))
            
            if not json_files:
                messagebox.showinfo(
                    "Không Có Kết Quả Cũ", 
                    "Không tìm thấy kết quả phân tích cũ.\nChạy phân tích trước để lưu kết quả."
                )
                return
            
            # Sort by modification time (newest first)
            json_files.sort(key=os.path.getmtime, reverse=True)
            
            # Create selection dialog
            self._show_file_selection_dialog(json_files)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải kết quả cũ: {str(e)}")
    
    def _show_file_selection_dialog(self, json_files: list):
        """Show dialog to select which previous result to load."""
        # Create popup window
        popup = ctk.CTkToplevel(self.container)
        popup.title("Tải Kết Quả Cũ")
        popup.geometry("600x400")
        popup.transient(self.container.winfo_toplevel())
        popup.grab_set()
        
        # Center the popup
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (600 // 2)
        y = (popup.winfo_screenheight() // 2) - (400 // 2)
        popup.geometry(f"600x400+{x}+{y}")
        
        # Title
        title_label = ctk.CTkLabel(
            popup,
            text="📁 Chọn Kết Quả Phân Tích Cũ",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#1565C0"
        )
        title_label.pack(pady=(20, 15))
        
        # Description
        desc_label = ctk.CTkLabel(
            popup,
            text="Chọn một kết quả phân tích để xem:",
            font=ctk.CTkFont(size=14),
            text_color="#666666"
        )
        desc_label.pack(pady=(0, 20))
        
        # Scrollable frame for file list
        files_frame = ctk.CTkScrollableFrame(popup, fg_color="white")
        files_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Variable to store selected file
        selected_file = ctk.StringVar()
        
        # Create radio buttons for each file
        for i, file_path in enumerate(json_files[:20]):  # Limit to 20 most recent
            try:
                # Extract timestamp from filename
                filename = os.path.basename(file_path)
                timestamp_str = filename.replace("youtube_analysis_", "").replace(".json", "")
                
                # Parse timestamp
                timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                display_time = timestamp.strftime("%d/%m/%Y %H:%M:%S")
                
                # Get file size
                file_size = os.path.getsize(file_path)
                size_kb = file_size / 1024
                
                # Create radio button
                radio_frame = ctk.CTkFrame(files_frame, fg_color="#F5F5F5", corner_radius=8)
                radio_frame.pack(fill="x", pady=5)
                
                radio_btn = ctk.CTkRadioButton(
                    radio_frame,
                    text=f"Phân tích từ {display_time} ({size_kb:.1f} KB)",
                    variable=selected_file,
                    value=file_path,
                    font=ctk.CTkFont(size=13),
                    text_color="#424242"
                )
                radio_btn.pack(anchor="w", padx=15, pady=10)
                
                # Select first item by default
                if i == 0:
                    selected_file.set(file_path)
                    
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
                continue
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(popup, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Hủy",
            command=popup.destroy,
            fg_color="#757575",
            hover_color="#616161",
            width=100,
            height=35
        )
        cancel_btn.pack(side="left")
        
        # Load button
        load_btn = ctk.CTkButton(
            buttons_frame,
            text="Tải Đã Chọn",
            command=lambda: self._load_selected_file(selected_file.get(), popup),
            fg_color="#2196F3",
            hover_color="#1976D2",
            width=120,
            height=35
        )
        load_btn.pack(side="right")
    
    def _load_selected_file(self, file_path: str, popup):
        """Load the selected analysis file."""
        try:
            if not file_path:
                messagebox.showwarning("Không Có Lựa Chọn", "Vui lòng chọn file để tải.")
                return
            
            # Load JSON file
            with open(file_path, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
            
            # Extract analysis results
            analysis_results = saved_data.get('analysis_results', saved_data)
            
            # Close popup
            popup.destroy()
            
            # Display the loaded results
            self.show_results(analysis_results)
            
            # Show success message
            filename = os.path.basename(file_path)
            messagebox.showinfo(
                "Thành Công", 
                f"Đã tải thành công kết quả phân tích từ:\n{filename}"
            )
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải file phân tích: {str(e)}")
    
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
            self.transcripts_label.configure(text=f"📄 Phụ đề đã trích xuất: {progress_data['transcripts_collected']}")
        
        if 'current_task' in progress_data:
            self.task_label.configure(text=f"🎯 Tác vụ hiện tại: {progress_data['current_task']}")
    
    def on_complete(self, result_data: Dict):
        """Handle analysis completion."""
        print(f"DEBUG on_complete - result_data keys: {result_data.keys()}")
        print(f"DEBUG on_complete - status: {result_data.get('status')}")
        
        if result_data.get('status') == 'success':
            self.show_results(result_data)
        else:
            # Show error
            self.progress_bar.configure(progress_color="#F44336")
            self.task_label.configure(
                text=f"❌ Lỗi: {result_data.get('error', 'Lỗi không xác định')}",
                text_color="#F44336"
            )
    
    def show(self):
        """Show the tab."""
        self.container.pack(fill="both", expand=True)
    
    def hide(self):
        """Hide the tab."""
        self.container.pack_forget()