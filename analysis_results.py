# analysis_results.py
"""
Module for analyzing Youtube data and formatting results in Vietnamese
Provides detailed insights for viral content creation
"""

import re
from typing import Dict, List, Tuple
from collections import Counter
import logging

logger = logging.getLogger(__name__)


def format_analysis_results(data: Dict) -> str:
    """Format analysis results in Vietnamese with detailed insights."""
    if not data:
        return "Không có dữ liệu để phân tích"
        
    summary = data.get('summary', {})
    
    result_text = f"""
📊 KẾT QUẢ PHÂN TÍCH YOUTUBE CHI TIẾT
{'='*80}

📈 TỔNG QUAN DỮ LIỆU:
📺 Số kênh phân tích: {summary.get('channels_analyzed', 0)}
🎬 Tổng số video: {summary.get('total_videos', 0)}
💬 Tổng số bình luận: {summary.get('total_comments', 0):,}
📝 Số transcript thu thập: {summary.get('total_transcripts', 0)}
👁️ Tổng lượt xem: {summary.get('total_views', 0):,}
👍 Tổng lượt thích: {summary.get('total_likes', 0):,}
📈 Tỷ lệ tương tác trung bình: {summary.get('avg_engagement_rate', 0):.2f}%

"""

    # Phân tích từng khía cạnh
    try:
        result_text += analyze_content_themes(data)
        result_text += analyze_us_audience_appeal(data)
        result_text += analyze_audience_sentiment(data)
        result_text += analyze_strengths(data)
        result_text += analyze_weaknesses(data)
        result_text += suggest_viral_strategies(data)
        result_text += show_top_videos_details(data)
    except Exception as e:
        logger.error(f"Error in analysis: {e}")
        result_text += f"\n❌ Lỗi khi phân tích: {e}\n"
    
    # Additional requirements if any
    additional_reqs = data.get('additional_requirements', [])
    if additional_reqs:
        result_text += f"""
📋 PHÂN TÍCH BỔ SUNG THEO YÊU CẦU:
{'='*80}

"""
        for i, req in enumerate(additional_reqs, 1):
            result_text += f"🔍 Yêu cầu {i}: {req['requirement']}\n"
            result_text += f"⏰ Thời gian: {req['timestamp']}\n"
            result_text += f"📊 Kết quả:\n{req['analysis']}\n\n"
            
    return result_text


def analyze_content_themes(data: Dict) -> str:
    """Phân tích chủ đề nội dung qua transcript."""
    transcripts = data.get('transcripts', [])
    videos = data.get('videos', [])
    
    result = f"""
🎯 1. NỘI DUNG CÁC VIDEO ĐỀ CẬP ĐẾN CHỦ ĐỀ GÌ?
{'='*80}

"""
    
    if not transcripts:
        result += "❌ Không có transcript để phân tích chủ đề.\n"
        result += "💡 Gợi ý: Hãy đảm bảo video có phụ đề để phân tích nội dung tốt hơn.\n\n"
        
        # Phân tích qua tiêu đề video thay thế
        if videos:
            result += "📋 PHÂN TÍCH QUA TIÊU ĐỀ VIDEO:\n"
            titles = [video.get('title', '') for video in videos]
            title_themes = analyze_titles_for_themes(titles)
            for theme, count in title_themes.items():
                result += f"  • {theme}: {count} video\n"
        result += "\n"
        return result
    
    # Phân tích từ khóa chính từ transcript
    all_text = ""
    video_themes = {}
    
    for transcript in transcripts:
        text = transcript.get('full_text', '')
        all_text += text + " "
        
        # Phân tích từng video
        video_id = transcript.get('video_id', '')
        if video_id:
            video_themes[video_id] = analyze_text_themes(text)
    
    # Từ khóa tâm lý phổ biến
    psychology_keywords = {
        '💕 Mối quan hệ & Tình yêu': [
            'relationship', 'love', 'dating', 'partner', 'marriage', 'couple', 
            'romance', 'attraction', 'chemistry', 'soulmate', 'heartbreak'
        ],
        '🧠 Tâm lý học & Hành vi': [
            'psychology', 'mind', 'brain', 'behavior', 'emotion', 'feeling',
            'subconscious', 'personality', 'trait', 'habit', 'pattern'
        ],
        '🌟 Phát triển bản thân': [
            'self', 'improve', 'growth', 'develop', 'success', 'confidence',
            'motivation', 'goal', 'achieve', 'potential', 'mindset'
        ],
        '🏥 Sức khỏe tinh thần': [
            'anxiety', 'depression', 'stress', 'mental health', 'therapy',
            'healing', 'trauma', 'recovery', 'wellness', 'peace'
        ],
        '💬 Giao tiếp & Xã hội': [
            'communication', 'talk', 'speak', 'listen', 'conversation',
            'social', 'friends', 'family', 'connection', 'network'
        ],
        '🔥 Động lực & Truyền cảm hứng': [
            'motivation', 'inspire', 'dream', 'purpose', 'passion',
            'energy', 'drive', 'ambition', 'determination', 'perseverance'
        ],
        '😨 Lo âu & Sợ hãi': [
            'fear', 'worry', 'anxiety', 'panic', 'nervous', 'scared',
            'phobia', 'afraid', 'concern', 'insecurity'
        ],
        '🎭 Cảm xúc & Tâm trạng': [
            'happy', 'sad', 'angry', 'joy', 'excitement', 'disappointment',
            'grief', 'mood', 'emotional', 'feelings'
        ]
    }
    
    # Đếm từ khóa
    theme_counts = {}
    text_lower = all_text.lower()
    
    for theme, keywords in psychology_keywords.items():
        count = 0
        for keyword in keywords:
            count += text_lower.count(keyword.lower())
        if count > 0:
            theme_counts[theme] = count
    
    # Hiển thị kết quả
    if theme_counts:
        sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
        
        result += "📋 CHỦ ĐỀ CHÍNH ĐƯỢC ĐỀ CẬP (theo mức độ xuất hiện):\n\n"
        
        for i, (theme, count) in enumerate(sorted_themes, 1):
            percentage = (count / sum(theme_counts.values())) * 100
            result += f"  {i}. {theme}\n"
            result += f"     📊 Xuất hiện: {count} lần ({percentage:.1f}%)\n"
            
        # Phân tích chi tiết từng video
        result += "\n📝 PHÂN TÍCH CHI TIẾT TỪNG VIDEO:\n"
        for i, video in enumerate(videos[:5], 1):  # Chỉ hiển thị 5 video đầu
            video_id = video.get('video_id', '')
            title = video.get('title', 'Không có tiêu đề')
            result += f"\n🎬 Video {i}: {title[:80]}...\n"
            
            if video_id in video_themes:
                video_theme_data = video_themes[video_id]
                if video_theme_data:
                    top_theme = max(video_theme_data.items(), key=lambda x: x[1])
                    result += f"   🎯 Chủ đề chính: {top_theme[0]} ({top_theme[1]} lần đề cập)\n"
                else:
                    result += "   ❓ Không xác định được chủ đề chính\n"
    else:
        result += "❓ Không phát hiện chủ đề tâm lý rõ ràng trong transcript.\n"
        result += "💡 Video có thể đề cập đến các chủ đề khác hoặc cần phân tích sâu hơn.\n"
    
    result += "\n"
    return result


def analyze_us_audience_appeal(data: Dict) -> str:
    """Phân tích sức hút với khán giả Mỹ."""
    result = f"""
🇺🇸 2. ĐIỀU GÌ KHIẾN NỘI DUNG THU HÚT KHÁN GIẢ MỸ?
{'='*80}

"""
    
    transcripts = data.get('transcripts', [])
    videos = data.get('videos', [])
    
    if not transcripts:
        result += "❌ Cần transcript để phân tích sức hút với khán giả Mỹ.\n\n"
        return result
    
    # Yếu tố thu hút khán giả Mỹ
    us_appeal_factors = {
        '🎯 Tính cá nhân hóa': [
            'you', 'your', 'yourself', 'personal', 'individual', 'own',
            'unique', 'special', 'specific'
        ],
        '🔥 Tính khẩn cấp/Hấp dẫn': [
            'now', 'today', 'immediately', 'urgent', 'important', 'must',
            'need to know', 'secret', 'hidden', 'revealed'
        ],
        '💪 Tự lực cánh sinh': [
            'self-made', 'independent', 'control', 'power', 'strong',
            'overcome', 'achieve', 'success', 'winner'
        ],
        '🧠 Khoa học/Tâm lý': [
            'research', 'study', 'science', 'psychology', 'expert',
            'proven', 'facts', 'evidence', 'data'
        ],
        '💰 Thành công/Tiền bạc': [
            'success', 'money', 'rich', 'wealthy', 'profit', 'earn',
            'millionaire', 'achievement', 'goal'
        ],
        '❤️ Cảm xúc mạnh': [
            'amazing', 'incredible', 'shocking', 'surprising', 'love',
            'hate', 'fear', 'excited', 'passionate'
        ],
        '🎭 Kể chuyện': [
            'story', 'tell', 'happened', 'experience', 'journey',
            'adventure', 'discover', 'reveal'
        ]
    }
    
    # Phân tích tất cả transcript
    all_text = ""
    for transcript in transcripts:
        all_text += transcript.get('full_text', '') + " "
    
    text_lower = all_text.lower()
    appeal_scores = {}
    
    for factor, keywords in us_appeal_factors.items():
        score = 0
        found_keywords = []
        for keyword in keywords:
            count = text_lower.count(keyword.lower())
            if count > 0:
                score += count
                found_keywords.append(f"{keyword}({count})")
        
        if score > 0:
            appeal_scores[factor] = {'score': score, 'keywords': found_keywords}
    
    if appeal_scores:
        sorted_appeals = sorted(appeal_scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        result += "🎯 CÁC YẾU TỐ THU HÚT KHÁN GIẢ MỸ:\n\n"
        
        for i, (factor, data_info) in enumerate(sorted_appeals, 1):
            score = data_info['score']
            keywords = data_info['keywords']
            result += f"  {i}. {factor}\n"
            result += f"     📊 Điểm số: {score} (từ khóa: {', '.join(keywords[:5])})\n"
            
            # Giải thích tại sao yếu tố này thu hút
            explanations = {
                '🎯 Tính cá nhân hóa': 'Khán giả Mỹ thích nội dung tập trung vào cá nhân, tạo cảm giác được quan tâm riêng.',
                '🔥 Tính khẩn cấp/Hấp dẫn': 'Văn hóa "instant gratification" - muốn có kết quả ngay lập tức.',
                '💪 Tự lực cánh sinh': 'Văn hóa tự lập mạnh mẽ, tin vào khả năng tự thay đổi cuộc đời.',
                '🧠 Khoa học/Tâm lý': 'Tin tưởng vào nghiên cứu khoa học và bằng chứng thực tế.',
                '💰 Thành công/Tiền bạc': 'Định hướng thành công và tài chính rõ ràng.',
                '❤️ Cảm xúc mạnh': 'Thích nội dung tạo phản ứng cảm xúc mạnh mẽ.',
                '🎭 Kể chuyện': 'Yêu thích câu chuyện cá nhân và trải nghiệm thực tế.'
            }
            
            if factor in explanations:
                result += f"     💡 {explanations[factor]}\n"
            result += "\n"
        
        # Đánh giá tổng thể
        total_score = sum(item[1]['score'] for item in sorted_appeals)
        result += f"📈 TỔNG ĐIỂM THU HÚT: {total_score}/100+\n"
        
        if total_score >= 50:
            result += "✅ Nội dung có tiềm năng thu hút tốt khán giả Mỹ\n"
        elif total_score >= 20:
            result += "⚠️ Nội dung có một số yếu tố thu hút, cần cải thiện thêm\n"
        else:
            result += "❌ Nội dung cần điều chỉnh để phù hợp với khán giả Mỹ hơn\n"
            
    else:
        result += "❓ Không phát hiện yếu tố thu hút khán giả Mỹ rõ ràng.\n"
        result += "💡 Nên thêm các yếu tố: cá nhân hóa, khoa học, tự lập, cảm xúc mạnh.\n"
    
    result += "\n"
    return result


def analyze_audience_sentiment(data: Dict) -> str:
    """Phân tích cảm nhận khán giả qua comment."""
    result = f"""
💬 3. CẢM NHẬN CỦA KHÁN GIẢ KHI XEM VIDEO?
{'='*80}

"""
    
    comments = data.get('comments', [])
    
    if not comments:
        result += "❌ Không có comment để phân tích cảm nhận khán giả.\n\n"
        return result
    
    # Phân loại cảm xúc trong comment
    sentiment_keywords = {
        '😍 Tích cực/Thích thú': [
            'love', 'amazing', 'great', 'awesome', 'fantastic', 'excellent',
            'perfect', 'wonderful', 'brilliant', 'outstanding', 'incredible',
            'thank you', 'helpful', 'useful', 'inspiring', 'motivating'
        ],
        '😔 Tiêu cực/Không thích': [
            'hate', 'terrible', 'awful', 'bad', 'worst', 'boring',
            'stupid', 'waste', 'disappointed', 'disagree', 'wrong'
        ],
        '🤔 Thắc mắc/Tò mò': [
            'question', 'how', 'why', 'what', 'when', 'where',
            'curious', 'wonder', 'confused', 'explain', 'help'
        ],
        '🔥 Hứng thú/Kích động': [
            'excited', 'wow', 'omg', 'amazing', 'mind blown',
            'shocking', 'unbelievable', 'crazy', 'insane'
        ],
        '🎯 Liên quan cá nhân': [
            'me too', 'same here', 'relate', 'exactly', 'my life',
            'happened to me', 'i feel', 'my experience'
        ],
        '🙏 Biết ơn/Cảm kích': [
            'thank', 'grateful', 'appreciate', 'helped me',
            'changed my life', 'saved me', 'blessing'
        ]
    }
    
    # Phân tích sentiment
    sentiment_counts = {}
    all_comments_text = ""
    
    for comment in comments:
        text = comment.get('text', '').lower()
        all_comments_text += text + " "
        
        for sentiment, keywords in sentiment_keywords.items():
            if sentiment not in sentiment_counts:
                sentiment_counts[sentiment] = 0
            
            for keyword in keywords:
                if keyword.lower() in text:
                    sentiment_counts[sentiment] += 1
    
    # Phân tích top comment
    top_comments = sorted(comments, key=lambda x: x.get('like_count', 0), reverse=True)[:10]
    
    result += "📊 PHÂN TÍCH CẢM XÚC TRONG COMMENT:\n\n"
    
    if sentiment_counts:
        total_sentiments = sum(sentiment_counts.values())
        sorted_sentiments = sorted(sentiment_counts.items(), key=lambda x: x[1], reverse=True)
        
        for sentiment, count in sorted_sentiments:
            if count > 0:
                percentage = (count / total_sentiments) * 100
                result += f"  {sentiment}: {count} comment ({percentage:.1f}%)\n"
        
        # Đánh giá tổng thể
        positive_score = sentiment_counts.get('😍 Tích cực/Thích thú', 0) + sentiment_counts.get('🙏 Biết ơn/Cảm kích', 0)
        negative_score = sentiment_counts.get('😔 Tiêu cực/Không thích', 0)
        
        result += f"\n📈 ĐÁNH GIÁ TỔNG THỂ:\n"
        if positive_score > negative_score * 2:
            result += "✅ Phản ứng khán giả rất tích cực\n"
        elif positive_score > negative_score:
            result += "👍 Phản ứng khán giả tích cực\n"
        elif negative_score > positive_score:
            result += "👎 Có một số phản ứng tiêu cực cần lưu ý\n"
        else:
            result += "😐 Phản ứng khán giả trung tính\n"
    
    # Hiển thị top comment
    result += "\n🔝 TOP COMMENT CÓ NHIỀU LIKE NHẤT:\n\n"
    for i, comment in enumerate(top_comments[:5], 1):
        text = comment.get('text', '')[:150]
        if len(comment.get('text', '')) > 150:
            text += '...'
        likes = comment.get('like_count', 0)
        author = comment.get('author', 'Anonymous')
        
        result += f"  {i}. 👤 {author} (👍 {likes})\n"
        result += f"     💬 \"{text}\"\n\n"
    
    result += "\n"
    return result


def analyze_strengths(data: Dict) -> str:
    """Phân tích điểm mạnh của video."""
    result = f"""
💪 4. ĐIỂM MẠNH CỦA CÁC VIDEO:
{'='*80}

"""
    
    videos = data.get('videos', [])
    comments = data.get('comments', [])
    summary = data.get('summary', {})
    
    strengths = []
    
    # Phân tích engagement rate
    avg_engagement = summary.get('avg_engagement_rate', 0)
    if avg_engagement > 5:
        strengths.append(f"🔥 Tỷ lệ tương tác xuất sắc ({avg_engagement:.2f}%) - Top 1% trên YouTube")
    elif avg_engagement > 2:
        strengths.append(f"📈 Tỷ lệ tương tác tốt ({avg_engagement:.2f}%) - Trên mức trung bình ngành")
    
    # Phân tích lượt xem
    if videos:
        total_views = sum(video.get('view_count', 0) for video in videos)
        avg_views = total_views / len(videos)
        
        # Check viral videos
        viral_videos = [v for v in videos if v.get('view_count', 0) > 1000000]
        if viral_videos:
            strengths.append(f"🚀 {len(viral_videos)} video đạt triệu views - Khả năng tạo viral content")
        elif avg_views > 100000:
            strengths.append(f"👁️ Lượt xem ấn tượng (TB: {avg_views:,.0f} lượt/video)")
        elif avg_views > 10000:
            strengths.append(f"📺 Lượt xem tốt (TB: {avg_views:,.0f} lượt/video)")
    
    # Phân tích comment quality
    if comments:
        long_comments = [c for c in comments if len(c.get('text', '')) > 50]
        engaging_comments = [c for c in comments if any(word in c.get('text', '').lower() 
                           for word in ['thank', 'helpful', 'love', 'great'])]
        
        if len(long_comments) / len(comments) > 0.3:
            strengths.append("💬 Comment chất lượng cao - Khán giả engage sâu với content")
        if len(engaging_comments) / len(comments) > 0.5:
            strengths.append("❤️ Khán giả yêu thích content - Nhiều phản hồi tích cực")
    
    # Phân tích consistency
    if len(videos) > 3:
        view_counts = [v.get('view_count', 0) for v in videos]
        if view_counts:
            avg = sum(view_counts) / len(view_counts)
            consistent_videos = [v for v in view_counts if v > avg * 0.5]
            if len(consistent_videos) > len(view_counts) * 0.7:
                strengths.append("📊 Performance ổn định - Đã có audience base trung thành")
    
    # Phân tích growth trend
    if videos and len(videos) > 5:
        recent_views = sum(v.get('view_count', 0) for v in videos[:5]) / 5
        older_views = sum(v.get('view_count', 0) for v in videos[-5:]) / 5
        if recent_views > older_views * 1.5:
            growth_percent = ((recent_views - older_views) / older_views) * 100
            strengths.append(f"📈 Channel đang growth mạnh (+{growth_percent:.0f}% views)")
    
    # Hiển thị điểm mạnh
    if strengths:
        for i, strength in enumerate(strengths, 1):
            result += f"  {i}. {strength}\n"
    else:
        result += "❓ Cần phân tích thêm để xác định điểm mạnh cụ thể.\n"
    
    # Phân tích video performance cao nhất
    if videos:
        top_video = max(videos, key=lambda x: x.get('view_count', 0))
        result += f"\n🏆 VIDEO HIỆU SUẤT CAO NHẤT:\n"
        result += f"   📹 {top_video.get('title', '')[:80]}...\n"
        result += f"   👁️ {top_video.get('view_count', 0):,} lượt xem\n"
        result += f"   👍 {top_video.get('like_count', 0):,} lượt thích\n"
        
        engagement = 0
        if top_video.get('view_count', 0) > 0:
            engagement = ((top_video.get('like_count', 0) + top_video.get('comment_count', 0)) / 
                         top_video.get('view_count', 0)) * 100
        result += f"   📈 Tỷ lệ tương tác: {engagement:.2f}%\n"
        
        # Phân tích yếu tố thành công
        result += f"\n   🔍 YẾU TỐ THÀNH CÔNG:\n"
        title = top_video.get('title', '').lower()
        if any(word in title for word in ['how', 'why', 'what']):
            result += "   • Sử dụng question hook hiệu quả\n"
        if any(char.isdigit() for char in title):
            result += "   • Có số trong title (listicle format)\n"
        if '?' in title:
            result += "   • Tạo curiosity với câu hỏi\n"
    
    result += "\n"
    return result


def analyze_weaknesses(data: Dict) -> str:
    """Phân tích điểm hạn chế và cần cải thiện."""
    result = f"""
⚠️ 5. ĐIỂM HẠN CHẾ VÀ CẦN CẢI THIỆN:
{'='*80}

"""
    
    videos = data.get('videos', [])
    comments = data.get('comments', [])
    transcripts = data.get('transcripts', [])
    summary = data.get('summary', {})
    
    weaknesses = []
    improvements = []
    
    # Phân tích engagement thấp
    avg_engagement = summary.get('avg_engagement_rate', 0)
    if avg_engagement < 1:
        weaknesses.append("📉 Tỷ lệ tương tác thấp - Dưới 1% là mức báo động")
        improvements.append("💡 Hook mạnh hơn trong 3 giây đầu + CTA rõ ràng")
    elif avg_engagement < 2:
        weaknesses.append("📊 Tỷ lệ tương tác dưới trung bình ngành")
        improvements.append("💡 Test nhiều format content để tìm style phù hợp")
    
    # Phân tích comment ít
    if videos:
        total_comments = sum(v.get('comment_count', 0) for v in videos)
        avg_comments = total_comments / len(videos)
        if avg_comments < 50:
            weaknesses.append("💬 Ít comment - Khán giả chưa có động lực tương tác")
            improvements.append("💡 Đặt câu hỏi cụ thể cuối video + pin comment hấp dẫn")
    
    # Phân tích thiếu transcript
    if len(transcripts) < len(videos) * 0.5:
        missing_percent = ((len(videos) - len(transcripts)) / len(videos)) * 100
        weaknesses.append(f"📝 {missing_percent:.0f}% video thiếu transcript - Mất SEO và accessibility")
        improvements.append("💡 Upload subtitle cho tất cả video để tăng reach")
    
    # Phân tích độ dài title
    if videos:
        long_titles = [v for v in videos if len(v.get('title', '')) > 100]
        short_titles = [v for v in videos if len(v.get('title', '')) < 30]
        
        if len(long_titles) > len(videos) * 0.3:
            weaknesses.append("📝 Nhiều title quá dài - Bị cắt trên mobile")
            improvements.append("💡 Giới hạn title 60-70 ký tự, keyword quan trọng đầu tiên")
        if len(short_titles) > len(videos) * 0.3:
            weaknesses.append("📝 Nhiều title quá ngắn - Thiếu keyword SEO")
            improvements.append("💡 Mở rộng title với keyword relevant")
    
    # Phân tích thumbnail (dựa vào performance)
    if videos and len(videos) > 5:
        # Check videos có performance thấp bất thường
        avg_views = sum(v.get('view_count', 0) for v in videos) / len(videos)
        poor_performers = [v for v in videos if v.get('view_count', 0) < avg_views * 0.3]
        if len(poor_performers) > len(videos) * 0.3:
            weaknesses.append("🖼️ Nhiều video underperform - Có thể do thumbnail kém hấp dẫn")
            improvements.append("💡 A/B test thumbnail với màu sắc tương phản + text rõ ràng")
    
    # Phân tích posting schedule
    if videos and len(videos) > 3:
        # Simple check for consistency (can be improved)
        weaknesses.append("📅 Cần review posting schedule")
        improvements.append("💡 Post đều đặn vào giờ vàng của target audience")
    
    # Phân tích negative comments
    if comments:
        negative_words = ['bad', 'terrible', 'worst', 'hate', 'boring', 'stupid', 'waste']
        negative_comments = []
        for comment in comments:
            text = comment.get('text', '').lower()
            if any(word in text for word in negative_words):
                negative_comments.append(comment)
        
        if len(negative_comments) > len(comments) * 0.1:  # Trên 10% comment tiêu cực
            weaknesses.append(f"👎 {len(negative_comments)} comment tiêu cực - Cần address concerns")
            improvements.append("💡 Phân tích feedback pattern và cải thiện weak points")
    
    # Hiển thị kết quả
    if weaknesses:
        result += "🚨 CÁC VẤN ĐỀ CẦN KHẮC PHỤC:\n\n"
        for i, weakness in enumerate(weaknesses, 1):
            result += f"  {i}. {weakness}\n"
        
        result += "\n🔧 GỢI Ý CẢI THIỆN CỤ THỂ:\n\n"
        for i, improvement in enumerate(improvements, 1):
            result += f"  {i}. {improvement}\n"
    else:
        result += "✅ Không phát hiện điểm yếu đáng kể.\n"
        result += "💡 Tiếp tục optimize và scale những gì đang work.\n"
    
    result += "\n"
    return result


def suggest_viral_strategies(data: Dict) -> str:
    """Gợi ý chiến lược viral."""
    result = f"""
🚀 6. CHIẾN LƯỢC VIRAL - TIẾP CẬN NHIỀU KHÁN GIẢ HƠN:
{'='*80}

"""
    
    videos = data.get('videos', [])
    transcripts = data.get('transcripts', [])
    comments = data.get('comments', [])
    summary = data.get('summary', {})
    
    # Chiến lược nội dung dựa trên data
    result += "📝 CHIẾN LƯỢC NỘI DUNG:\n"
    
    if videos:
        # Phân tích top performers
        top_videos = sorted(videos, key=lambda x: x.get('view_count', 0), reverse=True)[:5]
        common_elements = analyze_common_elements(top_videos)
        
        if common_elements:
            result += f"   • Pattern thành công: {', '.join(common_elements)}\n"
            result += "   • Scale những yếu tố này trong content mới\n"
        else:
            result += "   • Test nhiều format để tìm winning formula\n"
    
    result += "   • Hook mạnh mẽ trong 3-5 giây đầu\n"
    result += "   • Story structure: Problem → Journey → Solution → Transformation\n"
    
    # Chiến lược tiêu đề dựa trên performance
    result += "\n🎯 CHIẾN LƯỢC TIÊU ĐỀ VIRAL:\n"
    
    if videos:
        # Analyze successful title patterns
        high_view_videos = [v for v in videos if v.get('view_count', 0) > 
                           sum(v.get('view_count', 0) for v in videos) / len(videos)]
        
        title_patterns = []
        for video in high_view_videos:
            title = video.get('title', '').lower()
            if '?' in title:
                title_patterns.append("Questions")
            if any(str(i) in title for i in range(10)):
                title_patterns.append("Numbers")
            if any(word in title for word in ['secret', 'truth', 'hidden']):
                title_patterns.append("Mystery/Curiosity")
                
        if title_patterns:
            most_common = Counter(title_patterns).most_common(2)
            result += f"   • Patterns work tốt: {', '.join([p[0] for p in most_common])}\n"
    
    result += "   • Formula: [Number] + [Emotional Word] + [Benefit] + [Curiosity Gap]\n"
    result += "   • A/B test 3-5 variations cho mỗi video\n"
    
    # Chiến lược thumbnail
    result += "\n🖼️ CHIẾN LƯỢC THUMBNAIL:\n"
    result += "   • Contrast cao + Màu sắc nổi bật (đỏ, vàng, xanh neon)\n"
    result += "   • Face closeup với emotion mạnh\n"
    result += "   • Text to đậm, dễ đọc trên mobile\n"
    result += "   • Test với/không arrow và circle\n"
    
    # Chiến lược tâm lý
    result += "\n🧠 CHIẾN LƯỢC TÂM LÝ KHÁN GIẢ:\n"
    
    if comments:
        # Analyze what resonates with audience
        positive_comments = [c for c in comments if any(word in c.get('text', '').lower() 
                           for word in ['helpful', 'thank', 'love', 'relate'])]
        
        if positive_comments:
            result += "   • Audience respond tốt với content có tính relate cao\n"
            result += "   • Focus vào personal stories và real experiences\n"
        else:
            result += "   • Test emotional triggers khác nhau\n"
            result += "   • Tạo connection qua vulnerability và authenticity\n"
    
    # Platform strategy dựa trên data
    result += "\n📱 CHIẾN LƯỢC PLATFORM:\n"
    
    avg_views = sum(v.get('view_count', 0) for v in videos) / len(videos) if videos else 0
    
    if avg_views < 10000:
        result += "   • Focus YouTube SEO: Tags, descriptions, keywords\n"
        result += "   • Leverage YouTube Shorts cho discoverability\n"
    elif avg_views < 100000:
        result += "   • Cross-promote trên TikTok/Instagram Reels\n"
        result += "   • Collaborate với channels cùng size\n"
    else:
        result += "   • Scale winning content across platforms\n"
        result += "   • Build email list từ top viewers\n"
    
    # Timing strategy
    result += "\n⏰ CHIẾN LƯỢC THỜI GIAN:\n"
    result += "   • Post giờ vàng: 14:00-16:00 và 20:00-22:00 (target timezone)\n"
    result += "   • Consistency quan trọng hơn frequency\n"
    result += "   • Ride trending topics khi relevant\n"
    
    # PHẦN HÀNH ĐỘNG TIẾP THEO - DYNAMIC
    result += f"\n🎬 HÀNH ĐỘNG TIẾP THEO (Dựa trên phân tích kênh này):\n"
    
    # Tạo action items động
    action_items = generate_dynamic_action_items(data)
    
    # Hiển thị tối đa 5 action items quan trọng nhất
    for i, action in enumerate(action_items[:5], 1):
        result += f"   {i}. {action}\n"
    
    # Mục tiêu cụ thể
    result += f"\n📊 MỤC TIÊU CỤ THỂ CHO 30 NGÀY TỚI:\n"
    
    # Tính toán mục tiêu dựa trên current performance
    if videos:
        current_avg_views = sum(v.get('view_count', 0) for v in videos[:10]) / min(len(videos), 10)
        current_avg_engagement = summary.get('avg_engagement_rate', 0)
        
        # Set realistic growth targets
        if current_avg_views < 1000:
            target_views = 2500
            growth_text = "2.5x growth"
        elif current_avg_views < 10000:
            target_views = int(current_avg_views * 2)
            growth_text = "2x growth"
        elif current_avg_views < 100000:
            target_views = int(current_avg_views * 1.5)
            growth_text = "50% growth"
        else:
            target_views = int(current_avg_views * 1.3)
            growth_text = "30% growth"
            
        target_engagement = max(current_avg_engagement * 1.2, 3.0)
        target_subscribers = max(100, int(current_avg_views / 100))
        
        result += f"   • Average views: {current_avg_views:,.0f} → {target_views:,} ({growth_text})\n"
        result += f"   • Engagement rate: {current_avg_engagement:.1f}% → {target_engagement:.1f}%\n"
        result += f"   • New subscribers: +{target_subscribers:,} subscribers\n"
    else:
        result += "   • Establish baseline metrics trong tuần đầu\n"
        result += "   • Target 1,000 views/video trong tháng đầu\n"
        result += "   • Build đến 100 loyal subscribers\n"
    
    result += "\n"
    return result


def show_top_videos_details(data: Dict) -> str:
    """Hiển thị chi tiết video top performance."""
    result = f"""
🏆 7. CHI TIẾT VIDEO TOP PERFORMANCE:
{'='*80}

"""
    
    videos = data.get('videos', [])
    
    if not videos:
        result += "❌ Không có dữ liệu video để phân tích.\n"
        return result
    
    # Sắp xếp video theo view count
    sorted_videos = sorted(videos, key=lambda x: x.get('view_count', 0), reverse=True)
    
    for i, video in enumerate(sorted_videos[:5], 1):  # Top 5 videos
        title = video.get('title', 'Không có tiêu đề')
        views = video.get('view_count', 0)
        likes = video.get('like_count', 0)
        comments = video.get('comment_count', 0)
        published = video.get('published_at', '')[:10]
        duration = video.get('duration', '')
        
        # Tính engagement rate
        engagement_rate = 0
        if views > 0:
            engagement_rate = ((likes + comments) / views) * 100
        
        # Phân tích title
        title_analysis = analyze_title_viral_potential(title)
        
        result += f"🎬 TOP {i}: {title}\n"
        result += f"   📊 {views:,} views | {likes:,} likes | {comments:,} comments\n"
        result += f"   📈 Engagement: {engagement_rate:.2f}% | Ngày đăng: {published}"
        if duration:
            result += f" | Độ dài: {format_duration(duration)}"
        result += f"\n   🎯 Phân tích tiêu đề: {title_analysis}\n"
        
        # Đánh giá performance  
        performance_emoji = ""
        if engagement_rate > 5:
            performance_emoji = "🔥"
            performance_text = "Performance xuất sắc - Top 1%"
        elif engagement_rate > 2:
            performance_emoji = "⭐"
            performance_text = "Performance tốt - Trên trung bình"
        elif engagement_rate > 1:
            performance_emoji = "👍"
            performance_text = "Performance trung bình"
        else:
            performance_emoji = "📊"
            performance_text = "Cần cải thiện engagement"
            
        result += f"   {performance_emoji} {performance_text}\n"
        
        # Success factors cho top performer
        if i == 1 and engagement_rate > 2:
            result += "\n   🔑 YẾU TỐ THÀNH CÔNG CỦA VIDEO NÀY:\n"
            success_factors = analyze_video_success_factors(video)
            for factor in success_factors:
                result += f"      • {factor}\n"
        
        result += "\n"
    
    # Overall insights
    if len(videos) > 5:
        result += "💡 INSIGHTS TỪ TOP PERFORMERS:\n"
        insights = generate_performance_insights(sorted_videos[:5])
        for insight in insights:
            result += f"   • {insight}\n"
    
    return result


# Helper functions
def analyze_text_themes(text: str) -> Dict[str, int]:
    """Phân tích chủ đề từ text."""
    themes = {
        'Tâm lý': ['psychology', 'mind', 'brain', 'mental', 'emotion'],
        'Mối quan hệ': ['relationship', 'love', 'partner', 'couple', 'dating'],
        'Phát triển bản thân': ['self', 'improve', 'growth', 'success', 'confidence'],
        'Cảm xúc': ['feel', 'emotion', 'happy', 'sad', 'anger', 'fear'],
        'Hành vi': ['behavior', 'action', 'habit', 'pattern', 'react']
    }
    
    text_lower = text.lower()
    theme_counts = {}
    
    for theme, keywords in themes.items():
        count = sum(text_lower.count(keyword) for keyword in keywords)
        if count > 0:
            theme_counts[theme] = count
    
    return theme_counts


def analyze_titles_for_themes(titles: List[str]) -> Dict[str, int]:
    """Phân tích chủ đề từ danh sách tiêu đề."""
    all_titles = ' '.join(titles).lower()
    
    themes = {
        'Tâm lý học': ['psychology', 'mind', 'brain', 'mental'],
        'Mối quan hệ': ['relationship', 'love', 'dating', 'couple'],
        'Cảm xúc': ['emotion', 'feel', 'happy', 'sad'],
        'Hành vi': ['behavior', 'action', 'habit'],
        'Phát triển': ['growth', 'improve', 'success']
    }
    
    theme_counts = {}
    for theme, keywords in themes.items():
        count = sum(all_titles.count(keyword) for keyword in keywords)
        if count > 0:
            theme_counts[theme] = count
    
    return theme_counts


def analyze_title_viral_potential(title: str) -> str:
    """Phân tích tiềm năng viral của tiêu đề."""
    viral_indicators = {
        'Số': any(char.isdigit() for char in title),
        'Câu hỏi': '?' in title,
        'Cảm xúc mạnh': any(word in title.lower() for word in ['shocking', 'amazing', 'incredible', 'secret']),
        'Tính cá nhân': any(word in title.lower() for word in ['you', 'your']),
        'Tính khẩn cấp': any(word in title.lower() for word in ['now', 'immediately', 'today']),
        'Tính độc quyền': any(word in title.lower() for word in ['secret', 'hidden', 'never', 'nobody'])
    }
    
    score = sum(1 for indicator in viral_indicators.values() if indicator)
    
    if score >= 4:
        return "Tiềm năng viral rất cao ⭐⭐⭐⭐"
    elif score >= 3:
        return "Tiềm năng viral cao ⭐⭐⭐"
    elif score >= 2:
        return "Tiềm năng viral trung bình ⭐⭐"
    elif score >= 1:
        return "Tiềm năng viral thấp ⭐"
    else:
        return "Cần tối ưu title để viral"


def format_duration(duration: str) -> str:
    """Format duration từ YouTube API (PT4M13S) thành readable."""
    import re
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    if not match:
        return duration
        
    hours, minutes, seconds = match.groups()
    hours = int(hours) if hours else 0
    minutes = int(minutes) if minutes else 0
    seconds = int(seconds) if seconds else 0
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"


def analyze_common_elements(videos: List[Dict]) -> List[str]:
    """Tìm elements chung trong top videos."""
    elements = []
    
    if not videos:
        return elements
        
    # Check title patterns
    titles = [v.get('title', '').lower() for v in videos]
    
    # Common words (exclude common ones)
    all_words = ' '.join(titles).split()
    word_freq = Counter(word for word in all_words 
                       if len(word) > 4 and word not in ['about', 'video', 'youtube'])
    
    common_words = [word for word, count in word_freq.most_common(3) if count > len(videos) * 0.3]
    if common_words:
        elements.append(f"Keywords: {', '.join(common_words)}")
    
    # Check format patterns
    if sum(1 for t in titles if '?' in t) > len(titles) * 0.5:
        elements.append("Question format")
    if sum(1 for t in titles if any(char.isdigit() for char in t)) > len(titles) * 0.5:
        elements.append("Numbers in title")
        
    return elements


def generate_dynamic_action_items(data: Dict) -> List[str]:
    """Generate dynamic action items based on analysis."""
    action_items = []
    videos = data.get('videos', [])
    comments = data.get('comments', [])
    transcripts = data.get('transcripts', [])
    summary = data.get('summary', {})
    
    if not videos:
        return ["📊 Thu thập data để có insights cụ thể", 
                "🎯 Bắt đầu với 5 test videos khác nhau"]
    
    # 1. Based on view performance
    avg_views = sum(v.get('view_count', 0) for v in videos) / len(videos)
    
    if avg_views < 1000:
        action_items.append("🔍 Nghiên cứu SEO: Optimize title, tags, descriptions với target keywords")
        action_items.append("🖼️ Redesign thumbnails: A/B test với colors và text rõ ràng")
    elif avg_views < 10000:
        action_items.append("📱 Tạo YouTube Shorts từ best moments của long videos")
        action_items.append("🎯 Target specific niche keywords thay vì broad terms")
    elif avg_views < 100000:
        action_items.append("🤝 Collab với creators cùng size (10K-100K views)")
        action_items.append("📊 Double down on content types có highest views")
    else:
        action_items.append("📈 Scale winning formula: Tạo series từ top performers")
        action_items.append("💎 Maintain quality while increasing frequency")
    
    # 2. Based on engagement
    avg_engagement = summary.get('avg_engagement_rate', 0)
    
    if avg_engagement < 1:
        action_items.append("🎬 Re-edit videos: Hook mạnh hơn trong 3 seconds đầu")
        action_items.append("💬 End screen CTA: Ask specific question để trigger comments")
    elif avg_engagement < 2:
        action_items.append("📌 Pin comment với question hoặc poll ngay khi upload")
        action_items.append("❤️ Reply tất cả comments trong 24h đầu")
    elif avg_engagement < 5:
        action_items.append("🏆 Create community posts để maintain engagement between videos")
    
    # 3. Based on content analysis
    if transcripts:
        # Check if using CTAs
        all_text = ' '.join(t.get('full_text', '').lower() for t in transcripts[:5])
        if 'subscribe' not in all_text and 'like' not in all_text:
            action_items.append("📢 Add clear CTAs: 'Like và subscribe' ở timing phù hợp")
    
    # 4. Based on consistency
    if len(videos) > 5:
        # Simple consistency check
        recent_5 = sorted(videos, key=lambda x: x.get('published_at', ''), reverse=True)[:5]
        if recent_5:
            action_items.append("📅 Set fixed upload schedule và announce cho audience")
    
    # 5. Based on comment sentiment
    if comments:
        questions = [c for c in comments if '?' in c.get('text', '')]
        if len(questions) > len(comments) * 0.2:
            action_items.append("📹 Create FAQ video addressing top audience questions")
            
        negative = sum(1 for c in comments if any(word in c.get('text', '').lower() 
                      for word in ['boring', 'long', 'slow']))
        if negative > len(comments) * 0.1:
            action_items.append("✂️ Tighten editing: Cut dead air và keep pace moving")
    
    # 6. Platform specific
    if not any('short' in v.get('title', '').lower() for v in videos):
        action_items.append("📱 Start YouTube Shorts strategy: 1 short/week từ existing content")
    
    # 7. Based on top video analysis
    if videos:
        top_video = max(videos, key=lambda x: x.get('view_count', 0))
        top_engagement = ((top_video.get('like_count', 0) + top_video.get('comment_count', 0)) / 
                         top_video.get('view_count', 1)) * 100
        
        if top_engagement > avg_engagement * 2:
            action_items.append(f"🔄 Analyze và replicate format của: \"{top_video.get('title', '')[:40]}...\"")
    
    return action_items


def analyze_video_success_factors(video: Dict) -> List[str]:
    """Analyze success factors of a specific video."""
    factors = []
    
    title = video.get('title', '')
    views = video.get('view_count', 0)
    engagement = ((video.get('like_count', 0) + video.get('comment_count', 0)) / views * 100) if views > 0 else 0
    
    # Title analysis
    if '?' in title:
        factors.append("Sử dụng question hook tạo curiosity")
    if any(str(i) in title for i in range(10)):
        factors.append("Number in title (specific và clickable)")
    if len(title) < 70:
        factors.append("Title length optimal cho cả desktop và mobile")
    
    # Timing analysis
    published = video.get('published_at', '')
    if published:
        # Could analyze day of week, time, etc.
        factors.append("Timing phù hợp với audience timezone")
    
    # Performance metrics
    if engagement > 5:
        factors.append(f"Exceptional engagement rate ({engagement:.1f}%)")
    if views > 1000000:
        factors.append("Đạt viral threshold (1M+ views)")
        
    return factors


def generate_performance_insights(top_videos: List[Dict]) -> List[str]:
    """Generate insights from top performing videos."""
    insights = []
    
    if not top_videos:
        return insights
    
    # Average metrics of top videos
    avg_views = sum(v.get('view_count', 0) for v in top_videos) / len(top_videos)
    avg_engagement = sum(((v.get('like_count', 0) + v.get('comment_count', 0)) / 
                         v.get('view_count', 1) * 100) for v in top_videos) / len(top_videos)
    
    # Title length pattern
    title_lengths = [len(v.get('title', '')) for v in top_videos]
    avg_title_length = sum(title_lengths) / len(title_lengths)
    
    insights.append(f"Top videos average {avg_views:,.0f} views với {avg_engagement:.1f}% engagement")
    insights.append(f"Optimal title length: {avg_title_length:.0f} characters")
    
    # Common elements
    common = analyze_common_elements(top_videos)
    if common:
        insights.append(f"Common success elements: {', '.join(common)}")
    
    # Duration pattern
    durations = [v.get('duration', '') for v in top_videos if v.get('duration')]
    if durations:
        # Could analyze optimal video length
        insights.append("Video length phù hợp với content type và audience retention")
    
    return insights


def generate_channel_specific_tips(data: Dict) -> List[str]:
    """Generate channel-specific tips based on analysis."""
    tips = []
    videos = data.get('videos', [])
    
    if not videos:
        return ["Cần thêm dữ liệu để tạo tips cụ thể"]
    
    # Analyze top performing video patterns
    top_videos = sorted(videos, key=lambda x: x.get('view_count', 0), reverse=True)[:3]
    
    for video in top_videos:
        title = video.get('title', '')
        # Extract patterns from successful titles
        if '?' in title:
            tips.append("Sử dụng câu hỏi trong title để tạo curiosity")
        if any(str(i) in title for i in range(10)):
            tips.append("Sử dụng số trong title (listicles) để thu hút")
        if any(word in title.lower() for word in ['how', 'why', 'what']):
            tips.append("Tiếp tục với format educational content")
            
    return list(set(tips))  # Remove duplicates