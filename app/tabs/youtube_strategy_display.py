# youtube_strategy_display.py
"""
YouTube Strategy Display - Hiển thị chiến lược phát triển kênh YouTube
"""

import customtkinter as ctk
from tkinter import messagebox
import json
from datetime import datetime


class YouTubeStrategyDisplay:
    """Class để hiển thị chiến lược phát triển kênh YouTube."""
    
    @staticmethod
    def get_full_strategy_content():
        """Trả về nội dung chiến lược đầy đủ."""
        return {
            "title": "🚀 Chiến lược để phát triển kênh Youtube cho bạn",
            "sections": [
                {
                    "title": "**1. Tối ưu nội dung video:**",
                    "items": [
                        "- **Thumbnail hấp dẫn:** Sử dụng màu sắc nổi bật, khuôn mặt có cảm xúc mạnh, text overlay rõ ràng và tạo tò mò.",
                        "- **Title viral:** Sử dụng con số cụ thể, từ khóa mạnh như 'Bí mật', 'Sốc', 'Không ngờ', đặt câu hỏi kích thích tò mò."
                    ]
                },
                {
                    "title": "**2. Chiến lược SEO Youtube:**",
                    "items": [
                        "- **Keyword research:** Sử dụng YouTube Search Suggest, Google Trends, và TubeBuddy để tìm từ khóa có search volume cao.",
                        "- **Cách viết description:** Viết mô tả chi tiết, hấp dẫn và chứa từ khóa chính, giúp cải thiện khả năng tìm kiếm và Click-through Rate (CTR).",
                        "- **Tags hiệu quả:** Sử dụng tags liên quan, hợp lý và phân ảnh nội dung video để tăng khả năng xuất hiện trên YouTube Search."
                    ]
                },
                {
                    "title": "**3. Visual Branding (Nhận diện thương hiệu):**",
                    "items": [
                        "- **Màu sắc chủ đạo:** Chọn 2-3 màu chính phù hợp với personality của kênh (VD: xanh dương cho công nghệ, cam cho năng lượng).",
                        "- **Font chữ chuẩn:** Sử dụng 1-2 font dễ đọc trên thumbnail (Sans-serif như Arial, Helvetica cho hiện đại, hoặc bold fonts cho impact).",
                        "- **Layout thumbnail template:** Tạo 3-4 mẫu layout cố định (face + text, split screen, before/after) để khán giả dễ nhận diện.",
                        "- **Logo/Watermark:** Đặt logo nhỏ góc phải dưới, opacity 70% để không che nội dung nhưng vẫn brand recognition.",
                        "- **Color grading:** Áp dụng LUT/filter nhất quán cho tất cả video tạo visual signature riêng.",
                        "- **Intro/Outro:** Intro max 3-5 giây với animation logo, outro 10-15 giây với end screen elements."
                    ]
                },
                {
                    "title": "**4. Chiến lược thu hút và giữ chân khán giả:**",
                    "items": [
                        "- **Hook mạnh trong 5s đầu:** Bắt đầu video bằng câu hỏi hoặc tình huống gây tò mò, thu hút người xem từ đầu.",
                        "- **Cách giữ retention rate cao:** Đảm bảo nội dung hấp dẫn, tương tác với khán giả, và giữ chân họ bằng việc cung cấp thông tin giá trị liên tục.",
                        "- **Call-to-action hiệu quả:** Sử dụng các CTAs như 'Subscribe for more insights', 'Leave a comment with your thoughts', 'Share with someone who needs this' để khuyến khích hành động từ khán giả."
                    ]
                },
                {
                    "title": "**5. Cách sử dụng Shorts & Trends:**",
                    "items": [
                        "- **Loại content phù hợp Shorts:** Tạo shorts từ những đoạn nổi bật trong video dài, hoặc tập trung vào những chủ đề ngắn gọn, gây chú ý.",
                        "- **Cách catch trends nhanh:** Theo dõi xu hướng và sự kiện nóng hổi để tạo nội dung phản ảnh và tham gia vào các trends.",
                        "- **Tỷ lệ Shorts/Long-form:** Thử nghiệm với tỷ lệ Shorts và Long-form để xem xét phản hồi từ khán giả và hiệu quả trên kênh."
                    ]
                },
                {
                    "title": "**6. Process nghiên cứu & chọn chủ đề:**",
                    "items": [
                        "- **Weekly Research Process:** Mỗi thứ 2 dành 2h cho keyword research với TubeBuddy/VidIQ + YouTube Analytics.",
                        "- **Content Mining từ Comments:** Review top 50 comments mỗi tuần, tìm câu hỏi lặp lại → tạo video response.",
                        "- **Trending Topic Monitoring:** Set Google Alerts cho niche keywords, check YouTube Trending daily, follow 5-10 channels cùng niche.",
                        "- **Topic Validation Checklist:** Search volume >1000/tháng? Competition score <70? Relevant với audience? Có unique angle?",
                        "- **Content Calendar Planning:** Plan 1 tháng ahead với 40% evergreen + 40% trending + 20% experimental content."
                    ]
                },
                {
                    "title": "**7. Chiến lược tăng tương tác:**",
                    "items": [
                        "- **Kỹ thuật tăng comments:** Khuyến khích khán giả bình luận bằng cách đặt câu hỏi, trả lời các câu hỏi, và tương tác tích cực với bình luận.",
                        "- **Cách encourage likes & shares:** Yêu cầu khán giả like nếu họ thấy video hữu ích, và chia sẻ nếu họ nghĩ nội dung có thể giúp người khác.",
                        "- **Community engagement:** Tham gia vào cộng đồng, tương tác với fan trên các nền tảng khác như Facebook, Instagram để xây dựng mối quan hệ tốt với khán giả."
                    ]
                },
                {
                    "title": "**8. Script & Storytelling Framework:**",
                    "items": [
                        "- **Hook Formula (5s đầu):** 'Bạn có biết [shocking fact]?' hoặc 'Hôm nay tôi sẽ reveal [benefit] chỉ trong [time]'",
                        "- **Story Structure:** Problem (30s) → Agitation (1min) → Solution (3-5min) → Transformation (1min) → CTA (30s)",
                        "- **Script Template:** Conversational tone với 'bạn/mình', short sentences, personal anecdotes mỗi 2-3 phút.",
                        "- **Transition Phrases:** 'Nhưng đó chưa phải tất cả...', 'Điều thú vị là...', 'Và đây mới là phần quan trọng nhất...'",
                        "- **Cliffhangers:** Teaser ở đầu video, mini-hooks mỗi 2 phút, end screen teasing next video."
                    ]
                },
                {
                    "title": "**9. KPIs và Mục tiêu cụ thể:**",
                    "items": [
                        "- **Subscriber Growth:** Target +500-1000 subs/tháng trong 3 tháng đầu, +2000/tháng sau 6 tháng.",
                        "- **View Metrics:** Average View Duration >50% cho 10-min videos, >40% cho 15-min videos.",
                        "- **CTR Target:** Thumbnail CTR >8% trong 48h đầu, overall CTR >5%.",
                        "- **Engagement Rate:** (Likes + Comments) / Views >6%, Comment rate >0.5%.",
                        "- **Watch Time:** 4000 hours trong 90 ngày đầu, sau đó +2000 hours/tháng.",
                        "- **Revenue Goals:** RPM $2-5 cho niche giáo dục, CPM $4-8 cho entertainment."
                    ]
                },
                {
                    "title": "**10. Chiến lược thu hút fan trung thành:**",
                    "items": [
                        "- **Community building:** Tạo ra không gian giao lưu, thảo luận cho cộng đồng khán giả, có thể qua livestreams, Q&A sessions, hoặc Facebook Groups.",
                        "- **Exclusive content:** Cung cấp nội dung độc quyền cho fan trung thành, như behind-the-scenes, sneak peeks, hoặc bài giảng ngắn."
                    ]
                },
                {
                    "title": "**11. Timeline triển khai 3-6 tháng:**",
                    "items": [
                        "- **Tháng 1 (Foundation):** Test 3-4 content formats, establish visual branding, setup analytics tracking.",
                        "- **Tuần 1-2:** Research phase - analyze top 20 competitors, identify content gaps, create channel art/logo.",
                        "- **Tuần 3-4:** Production sprint - create 8 videos (4 different formats), A/B test thumbnails.",
                        "- **Tháng 2 (Optimization):** Double down on best performing format, refine SEO strategy, start community building.",
                        "- **Tuần 5-6:** Analyze metrics, identify winning format (highest retention + CTR), optimize based on data.",
                        "- **Tuần 7-8:** Scale production of winning format, implement viewer feedback, test Shorts strategy.",
                        "- **Tháng 3-4 (Growth):** Increase posting frequency, collaborate với creators, launch email list.",
                        "- **Tháng 5-6 (Monetization):** Diversify revenue streams, launch products/services, explore sponsorships.",
                        "- **Milestones:** M1: 1K subs, M3: 10K subs + 4K watch hours, M6: 25K subs + monetization enabled."
                    ]
                }
            ]
        }
    
    @staticmethod
    def create_strategy_display(parent_frame):
        """Tạo widget hiển thị chiến lược."""
        # Main container
        container = ctk.CTkFrame(parent_frame, fg_color="white")
        
        # Header
        header_frame = ctk.CTkFrame(container, fg_color="white")
        header_frame.pack(fill="x", padx=40, pady=(30, 20))
        
        strategy_content = YouTubeStrategyDisplay.get_full_strategy_content()
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text=strategy_content["title"],
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#2B2B2B"
        )
        title_label.pack()
        
        # Scrollable content
        content_frame = ctk.CTkScrollableFrame(
            container,
            fg_color="#F8FFF8",
            scrollbar_button_color="#E0E0E0",
            corner_radius=15
        )
        content_frame.pack(fill="both", expand=True, padx=40, pady=(0, 30))
        
        # Display sections
        for section in strategy_content["sections"]:
            # Section title
            section_title = ctk.CTkLabel(
                content_frame,
                text=section["title"],
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#2B2B2B",
                anchor="w"
            )
            section_title.pack(fill="x", padx=30, pady=(20, 10))
            
            # Section items
            for item in section["items"]:
                item_label = ctk.CTkLabel(
                    content_frame,
                    text=item,
                    font=ctk.CTkFont(size=13),
                    text_color="#444444",
                    anchor="w",
                    justify="left",
                    wraplength=900
                )
                item_label.pack(fill="x", padx=(50, 30), pady=3)
        
        # Export button
        export_frame = ctk.CTkFrame(container, fg_color="white")
        export_frame.pack(fill="x", padx=40, pady=(20, 30))
        
        export_btn = ctk.CTkButton(
            export_frame,
            text="📥 Xuất Chiến Lược",
            command=lambda: YouTubeStrategyDisplay.export_strategy(strategy_content),
            fg_color="#2196F3",
            hover_color="#1976D2",
            height=45,
            width=200
        )
        export_btn.pack()
        
        return container
    
    @staticmethod
    def export_strategy(strategy_content):
        """Export chiến lược ra file."""
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("Markdown files", "*.md"),
                ("All files", "*.*")
            ],
            initialfile=f"youtube_strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(strategy_content["title"] + "\n")
                    f.write("=" * 60 + "\n\n")
                    
                    for section in strategy_content["sections"]:
                        f.write(section["title"] + "\n")
                        for item in section["items"]:
                            f.write(item + "\n")
                        f.write("\n")
                
                messagebox.showinfo("Thành công", f"Đã xuất chiến lược ra file:\n{filename}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xuất file: {str(e)}")


# Tab Manager cho Strategy
class StrategyTabManager:
    """Tab manager để hiển thị chiến lược YouTube."""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.container = YouTubeStrategyDisplay.create_strategy_display(parent_frame)
        
    def show(self):
        """Show the tab."""
        self.container.pack(fill="both", expand=True)
        
    def hide(self):
        """Hide the tab."""
        self.container.pack_forget()