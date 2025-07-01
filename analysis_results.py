# analysis_results.py
"""
Module for analyzing Youtube data and formatting results in Vietnamese
UPDATED WITH PERFORMANCE OPTIMIZATIONS
Provides detailed insights for viral content creation
"""

import re
from typing import Dict, List, Tuple
from collections import Counter
import logging

# Import performance optimizations
try:
    from performance_config import perf_config, UIOptimizer, MemoryOptimizer
    PERFORMANCE_OPTIMIZATIONS = True
except ImportError:
    PERFORMANCE_OPTIMIZATIONS = False

logger = logging.getLogger(__name__)


def format_analysis_results(data: Dict) -> str:
    """Format analysis results in Vietnamese with detailed insights and performance optimizations."""
    if not data:
        return "Không có dữ liệu để phân tích"
    
    # Apply performance optimizations if available
    if PERFORMANCE_OPTIMIZATIONS:
        # Limit display items to prevent UI lag
        max_display = perf_config.get('max_display_items', 100)
        data = MemoryOptimizer.limit_data_size(data, max_display)
    
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

    # Phân tích từng khía cạnh với optimizations
    try:
        # Quick insights first (most important for user)
        result_text += generate_quick_insights_optimized(data)
        
        # Core analysis sections (optimized)
        result_text += analyze_content_themes_optimized(data)
        result_text += analyze_us_audience_appeal_optimized(data)
        result_text += analyze_audience_sentiment_optimized(data)
        result_text += analyze_strengths_optimized(data)
        result_text += analyze_weaknesses_optimized(data)
        result_text += suggest_viral_strategies_optimized(data)
        result_text += show_top_videos_details_optimized(data)
        
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
        # Limit additional requirements to prevent overload
        display_reqs = additional_reqs[:5] if PERFORMANCE_OPTIMIZATIONS else additional_reqs
        
        for i, req in enumerate(display_reqs, 1):
            result_text += f"🔍 Yêu cầu {i}: {req['requirement']}\n"
            result_text += f"⏰ Thời gian: {req['timestamp']}\n"
            result_text += f"📊 Kết quả:\n{req['analysis']}\n\n"
            
    return result_text


def generate_quick_insights_optimized(data: Dict) -> str:
    """Generate quick insights without heavy processing - OPTIMIZED VERSION"""
    insights = []
    videos = data.get('video', [])
    
    if not videos:
        return """
💡 INSIGHTS NHANH:
{'='*40}

❓ Cần dữ liệu video để tạo insights chi tiết.
🎯 Hãy thử phân tích với ít nhất 5-10 videos để có kết quả tốt hơn.

"""
    
    # Quick calculations (optimized)
    total_videos = len(videos)
    avg_views = sum(v.get('view_count', 0) for v in videos) / total_videos
    top_video = max(videos, key=lambda x: x.get('view_count', 0))
    
    # Calculate engagement distribution efficiently
    high_engagement = len([v for v in videos if v.get('engagement_rate', 0) > 5])
    good_engagement = len([v for v in videos if 2 <= v.get('engagement_rate', 0) <= 5])
    low_engagement = total_videos - high_engagement - good_engagement
    
    # Performance assessment
    if avg_views > 1000000:
        insights.append("🔥 VIRAL POTENTIAL: Rất cao - Channel đã có viral content")
        insights.append("🎯 Strategy: Scale winning formulas và maintain consistency")
    elif avg_views > 100000:
        insights.append("⭐ VIRAL POTENTIAL: Cao - Đang trên đà phát triển tốt")
        insights.append("📈 Strategy: Optimize top performers và increase frequency")
    elif avg_views > 10000:
        insights.append("📈 VIRAL POTENTIAL: Trung bình - Có cơ hội cải thiện")
        insights.append("🔧 Strategy: A/B test formats và improve thumbnails")
    else:
        insights.append("🎯 VIRAL POTENTIAL: Đang xây dựng - Cần tối ưu strategy")
        insights.append("🚀 Strategy: Focus SEO và consistent posting")
    
    # Top performer insight
    top_views = top_video.get('view_count', 0)
    top_engagement = top_video.get('engagement_rate', 0)
    insights.append(f"🏆 BEST PERFORMER: {top_views:,} views ({top_engagement:.1f}% engagement)")
    
    # Engagement distribution insight
    if high_engagement > total_videos * 0.3:
        insights.append(f"✅ ENGAGEMENT: Excellent - {high_engagement} high-performing videos")
    elif good_engagement > total_videos * 0.5:
        insights.append(f"👍 ENGAGEMENT: Good - Consistent performance pattern")
    else:
        insights.append(f"⚠️ ENGAGEMENT: Needs improvement - Focus on hooks và CTAs")
    
    return f"""
💡 INSIGHTS NHANH:
{'='*40}

{chr(10).join(f'• {insight}' for insight in insights)}

📊 ENGAGEMENT BREAKDOWN:
🔥 High (>5%): {high_engagement} videos
👍 Good (2-5%): {good_engagement} videos  
⚠️ Low (<2%): {low_engagement} videos

"""


def analyze_content_themes_optimized(data: Dict) -> str:
    """Phân tích chủ đề nội dung qua transcript - OPTIMIZED VERSION."""
    transcripts = data.get('transcripts', [])
    videos = data.get('video', [])
    
    result = f"""
🎯 1. NỘI DUNG CÁC VIDEO ĐỀ CẬP ĐẾN CHỦ ĐỀ GÌ?
{'='*80}

"""
    
    if not transcripts:
        result += "❌ Không có transcript để phân tích chủ đề.\n"
        result += "💡 Gợi ý: Hãy đảm bảo video có phụ đề để phân tích nội dung tốt hơn.\n\n"
        
        # Phân tích qua tiêu đề video thay thế (optimized)
        if videos:
            result += "📋 PHÂN TÍCH QUA TIÊU ĐỀ VIDEO:\n"
            titles = [video.get('title', '') for video in videos[:20]]  # Limit for performance
            title_themes = analyze_titles_for_themes_optimized(titles)
            for theme, count in list(title_themes.items())[:5]:  # Top 5 themes
                result += f"  • {theme}: {count} video\n"
        result += "\n"
        return result
    
    # Optimized theme analysis - limit processing
    sample_transcripts = transcripts[:10] if PERFORMANCE_OPTIMIZATIONS else transcripts
    all_text = ""
    video_themes = {}
    
    for transcript in sample_transcripts:
        text = transcript.get('full_text', '')
        # Limit text length for performance
        if PERFORMANCE_OPTIMIZATIONS and len(text) > 5000:
            text = text[:5000]
        all_text += text + " "
        
        # Phân tích từng video
        video_id = transcript.get('video_id', '')
        if video_id:
            video_themes[video_id] = analyze_text_themes_optimized(text)
    
    # Optimized keyword analysis
    psychology_keywords = {
        '💕 Mối quan hệ & Tình yêu': [
            'relationship', 'love', 'dating', 'partner', 'marriage', 'couple'
        ],
        '🧠 Tâm lý học & Hành vi': [
            'psychology', 'mind', 'brain', 'behavior', 'emotion', 'feeling'
        ],
        '🌟 Phát triển bản thân': [
            'self', 'improve', 'growth', 'success', 'confidence', 'motivation'
        ],
        '🏥 Sức khỏe tinh thần': [
            'anxiety', 'depression', 'stress', 'mental health', 'therapy'
        ],
        '💬 Giao tiếp & Xã hội': [
            'communication', 'talk', 'speak', 'social', 'friends', 'family'
        ]
    }
    
    # Đếm từ khóa (optimized)
    theme_counts = {}
    text_lower = all_text.lower()
    
    for theme, keywords in psychology_keywords.items():
        count = sum(text_lower.count(keyword.lower()) for keyword in keywords)
        if count > 0:
            theme_counts[theme] = count
    
    # Hiển thị kết quả (limited)
    if theme_counts:
        sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        result += "📋 CHỦ ĐỀ CHÍNH ĐƯỢC ĐỀ CẬP:\n\n"
        
        for i, (theme, count) in enumerate(sorted_themes, 1):
            percentage = (count / sum(theme_counts.values())) * 100
            result += f"  {i}. {theme}\n"
            result += f"     📊 Xuất hiện: {count} lần ({percentage:.1f}%)\n"
            
        # Sample video analysis (limited for performance)
        result += "\n📝 SAMPLE VIDEO ANALYSIS:\n"
        sample_videos = videos[:3] if PERFORMANCE_OPTIMIZATIONS else videos[:5]
        
        for i, video in enumerate(sample_videos, 1):
            video_id = video.get('video_id', '')
            title = video.get('title', 'Không có tiêu đề')[:60] + "..."
            result += f"\n🎬 Video {i}: {title}\n"
            
            if video_id in video_themes and video_themes[video_id]:
                top_theme = max(video_themes[video_id].items(), key=lambda x: x[1])
                result += f"   🎯 Chủ đề chính: {top_theme[0]} ({top_theme[1]} lần)\n"
            else:
                result += "   ❓ Chủ đề không xác định\n"
    else:
        result += "❓ Không phát hiện chủ đề tâm lý rõ ràng.\n"
        result += "💡 Có thể cần phân tích với dataset lớn hơn.\n"
    
    result += "\n"
    return result


def analyze_us_audience_appeal_optimized(data: Dict) -> str:
    """Phân tích sức hút với khán giả Mỹ - OPTIMIZED VERSION."""
    result = f"""
🇺🇸 2. ĐIỀU GÌ KHIẾN NỘI DUNG THU HÚT KHÁN GIẢ MỸ?
{'='*80}

"""
    
    transcripts = data.get('transcripts', [])
    
    if not transcripts:
        result += "❌ Cần transcript để phân tích sức hút với khán giả Mỹ.\n\n"
        return result
    
    # Optimized appeal factors (reduced set for performance)
    us_appeal_factors = {
        '🎯 Tính cá nhân hóa': ['you', 'your', 'yourself', 'personal'],
        '🔥 Tính khẩn cấp': ['now', 'today', 'secret', 'hidden', 'revealed'],
        '💪 Tự lực cánh sinh': ['self-made', 'control', 'power', 'strong'],
        '🧠 Khoa học/Research': ['research', 'study', 'science', 'proven'],
        '❤️ Cảm xúc mạnh': ['amazing', 'incredible', 'shocking', 'love']
    }
    
    # Limit transcripts for performance
    sample_transcripts = transcripts[:5] if PERFORMANCE_OPTIMIZATIONS else transcripts
    
    # Phân tích transcript (optimized)
    all_text = ""
    for transcript in sample_transcripts:
        text = transcript.get('full_text', '')
        # Limit text length
        if len(text) > 3000:
            text = text[:3000]
        all_text += text + " "
    
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
            appeal_scores[factor] = {'score': score, 'keywords': found_keywords[:3]}  # Limit keywords shown
    
    if appeal_scores:
        sorted_appeals = sorted(appeal_scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        result += "🎯 CÁC YẾU TỐ THU HÚT KHÁN GIẢ MỸ:\n\n"
        
        for i, (factor, data_info) in enumerate(sorted_appeals, 1):
            score = data_info['score']
            keywords = data_info['keywords']
            result += f"  {i}. {factor}\n"
            result += f"     📊 Điểm số: {score} (từ: {', '.join(keywords)})\n"
        
        # Đánh giá tổng thể
        total_score = sum(item[1]['score'] for item in sorted_appeals)
        result += f"\n📈 TỔNG ĐIỂM THU HÚT: {total_score}\n"
        
        if total_score >= 50:
            result += "✅ Nội dung có tiềm năng thu hút tốt khán giả Mỹ\n"
        elif total_score >= 20:
            result += "⚠️ Nội dung có potential, cần optimize thêm\n"
        else:
            result += "❌ Cần điều chỉnh để phù hợp khán giả Mỹ hơn\n"
            
    else:
        result += "❓ Chưa phát hiện yếu tố thu hút khán giả Mỹ rõ ràng.\n"
        result += "💡 Gợi ý: Thêm personal stories, urgency, scientific backing.\n"
    
    result += "\n"
    return result


def analyze_audience_sentiment_optimized(data: Dict) -> str:
    """Phân tích cảm nhận khán giả qua comment - OPTIMIZED VERSION."""
    result = f"""
💬 3. CẢM NHẬN CỦA KHÁN GIẢ KHI XEM VIDEO?
{'='*80}

"""
    
    comments = data.get('bình luận', [])
    
    if not comments:
        result += "❌ Không có comment để phân tích cảm nhận khán giả.\n\n"
        return result
    
    # Limit comments for performance
    sample_comments = comments[:100] if PERFORMANCE_OPTIMIZATIONS else comments
    
    # Simplified sentiment keywords
    sentiment_keywords = {
        '😍 Tích cực': ['love', 'amazing', 'great', 'awesome', 'thank', 'helpful'],
        '😔 Tiêu cực': ['hate', 'terrible', 'bad', 'boring', 'stupid', 'waste'],
        '🤔 Thắc mắc': ['question', 'how', 'why', 'what', 'explain'],
        '🎯 Liên quan': ['me too', 'same', 'relate', 'exactly', 'my life']
    }
    
    # Phân tích sentiment (optimized)
    sentiment_counts = {}
    positive_comments = []
    
    for comment in sample_comments:
        text = comment.get('text', '').lower()
        
        for sentiment, keywords in sentiment_keywords.items():
            if sentiment not in sentiment_counts:
                sentiment_counts[sentiment] = 0
            
            if any(keyword in text for keyword in keywords):
                sentiment_counts[sentiment] += 1
                
                # Collect positive examples
                if sentiment == '😍 Tích cực' and len(positive_comments) < 3:
                    positive_comments.append(comment)
    
    # Hiển thị phân tích
    result += "📊 PHÂN TÍCH CẢM XÚC:\n\n"
    
    if sentiment_counts:
        total_sentiments = sum(sentiment_counts.values())
        
        for sentiment, count in sentiment_counts.items():
            if count > 0:
                percentage = (count / total_sentiments) * 100
                result += f"  {sentiment}: {count} comment ({percentage:.1f}%)\n"
        
        # Đánh giá tổng thể
        positive_score = sentiment_counts.get('😍 Tích cực', 0)
        negative_score = sentiment_counts.get('😔 Tiêu cực', 0)
        
        result += f"\n📈 ĐÁNH GIÁ:\n"
        if positive_score > negative_score * 2:
            result += "✅ Phản ứng khán giả rất tích cực\n"
        elif positive_score > negative_score:
            result += "👍 Phản ứng khán giả tích cực\n"
        else:
            result += "⚠️ Cần cải thiện để có phản ứng tích cực hơn\n"
    
    # Hiển thị top comment (limited)
    if positive_comments:
        result += "\n🔝 SAMPLE POSITIVE COMMENTS:\n\n"
        for i, comment in enumerate(positive_comments, 1):
            text = comment.get('text', '')[:100] + "..." if len(comment.get('text', '')) > 100 else comment.get('text', '')
            likes = comment.get('like_count', 0)
            
            result += f"  {i}. \"{text}\" ({likes} likes)\n"
    
    result += "\n"
    return result


def analyze_strengths_optimized(data: Dict) -> str:
    """Phân tích điểm mạnh - OPTIMIZED VERSION."""
    result = f"""
💪 4. ĐIỂM MẠNH CỦA CÁC VIDEO:
{'='*80}

"""
    
    videos = data.get('video', [])
    summary = data.get('summary', {})
    
    strengths = []
    
    # Quick strength analysis
    avg_engagement = summary.get('avg_engagement_rate', 0)
    total_videos = len(videos)
    
    if avg_engagement > 5:
        strengths.append(f"🔥 Engagement xuất sắc ({avg_engagement:.2f}%) - Top tier performance")
    elif avg_engagement > 2:
        strengths.append(f"📈 Engagement tốt ({avg_engagement:.2f}%) - Trên mức TB")
    
    # Views analysis (optimized)
    if videos:
        avg_views = summary.get('avg_views', 0)
        viral_videos = [v for v in videos if v.get('view_count', 0) > 1000000]
        
        if viral_videos:
            strengths.append(f"🚀 {len(viral_videos)} video viral (1M+ views)")
        elif avg_views > 100000:
            strengths.append(f"👁️ Views ấn tượng (TB: {avg_views:,.0f}/video)")
        elif avg_views > 10000:
            strengths.append(f"📺 Performance ổn định (TB: {avg_views:,.0f}/video)")
    
    # Consistency check (simplified)
    if total_videos > 5:
        high_performers = len([v for v in videos if v.get('engagement_rate', 0) > avg_engagement])
        consistency_rate = (high_performers / total_videos) * 100
        
        if consistency_rate > 50:
            strengths.append(f"📊 Consistency tốt ({consistency_rate:.0f}% videos above average)")
    
    # Top performer analysis
    if videos:
        top_video = max(videos, key=lambda x: x.get('view_count', 0))
        top_views = top_video.get('view_count', 0)
        top_engagement = top_video.get('engagement_rate', 0)
        
        if top_views > 500000 or top_engagement > 5:
            strengths.append(f"🏆 Best performer: {top_views:,} views, {top_engagement:.1f}% engagement")
    
    # Display strengths
    if strengths:
        for i, strength in enumerate(strengths, 1):
            result += f"  {i}. {strength}\n"
    else:
        result += "❓ Cần dataset lớn hơn để xác định điểm mạnh.\n"
    
    # Quick recommendations
    result += f"\n🎯 LEVERAGE POINTS:\n"
    if avg_engagement > 3:
        result += "• Scale successful content formats\n"
        result += "• Maintain posting consistency\n"
    else:
        result += "• Focus on improving engagement first\n"
        result += "• Analyze top performers for patterns\n"
    
    result += "\n"
    return result


def analyze_weaknesses_optimized(data: Dict) -> str:
    """Phân tích điểm yếu - OPTIMIZED VERSION."""
    result = f"""
⚠️ 5. ĐIỂM HẠN CHẾ VÀ CẦN CẢI THIỆN:
{'='*80}

"""
    
    videos = data.get('video', [])
    summary = data.get('summary', {})
    
    weaknesses = []
    improvements = []
    
    # Quick weakness analysis
    avg_engagement = summary.get('avg_engagement_rate', 0)
    total_videos = len(videos)
    
    if avg_engagement < 1:
        weaknesses.append("📉 Engagement thấp (<1%) - Cần cải thiện urgent")
        improvements.append("💡 Focus hook mạnh + clear CTAs")
    elif avg_engagement < 2:
        weaknesses.append("📊 Engagement dưới TB ngành (<2%)")
        improvements.append("💡 A/B test thumbnails + titles")
    
    # Performance distribution analysis
    if videos:
        low_performers = len([v for v in videos if v.get('engagement_rate', 0) < 1])
        if low_performers > total_videos * 0.3:
            weaknesses.append(f"⚠️ {low_performers} videos có engagement thấp")
            improvements.append("💡 Analyze low performers để tránh lặp lại")
    
    # Content gaps (simplified)
    transcripts = data.get('transcripts', [])
    if len(transcripts) < len(videos) * 0.5:
        missing_percent = ((len(videos) - len(transcripts)) / len(videos)) * 100
        weaknesses.append(f"📝 {missing_percent:.0f}% videos thiếu subtitles")
        improvements.append("💡 Add subtitles để improve accessibility + SEO")
    
    # Comment engagement
    comments = data.get('bình luận', [])
    if videos and comments:
        avg_comments_per_video = len(comments) / len(videos)
        if avg_comments_per_video < 10:
            weaknesses.append("💬 Ít comment - Khán giả chưa engage sâu")
            improvements.append("💡 End videos với specific questions")
    
    # Display results
    if weaknesses:
        result += "🚨 CÁC ĐIỂM CẦN CẢI THIỆN:\n\n"
        for i, weakness in enumerate(weaknesses, 1):
            result += f"  {i}. {weakness}\n"
        
        result += "\n🔧 HÀNH ĐỘNG ƯU TIÊN:\n\n"
        for i, improvement in enumerate(improvements, 1):
            result += f"  {i}. {improvement}\n"
    else:
        result += "✅ Không phát hiện điểm yếu đáng kể.\n"
        result += "💡 Focus vào scaling những gì đang work.\n"
    
    result += "\n"
    return result


def suggest_viral_strategies_optimized(data: Dict) -> str:
    """Gợi ý chiến lược viral - OPTIMIZED VERSION."""
    result = f"""
🚀 6. CHIẾN LƯỢC VIRAL - SCALE CONTENT HIỆU QUẢ:
{'='*80}

"""
    
    videos = data.get('video', [])
    summary = data.get('summary', {})
    
    if not videos:
        result += "❓ Cần data để tạo strategy cụ thể.\n\n"
        return result
    
    # Quick strategy based on current performance
    avg_views = summary.get('avg_views', 0)
    avg_engagement = summary.get('avg_engagement_rate', 0)
    
    result += "📝 STRATEGY DỰA TRÊN PERFORMANCE HIỆN TẠI:\n\n"
    
    # Content strategy based on data
    if avg_views > 100000:
        result += "🎯 HIGH PERFORMER STRATEGY:\n"
        result += "• Analyze top 3 videos để tìm success patterns\n"
        result += "• Scale winning formats với variations\n"
        result += "• Increase posting frequency\n"
        result += "• Cross-promote lên multiple platforms\n\n"
    elif avg_views > 10000:
        result += "📈 GROWTH STRATEGY:\n"
        result += "• Optimize thumbnails với A/B testing\n"
        result += "• Improve titles với emotional triggers\n"
        result += "• Focus SEO với trending keywords\n"
        result += "• Create YouTube Shorts cho discovery\n\n"
    else:
        result += "🎯 FOUNDATION STRATEGY:\n"
        result += "• Establish consistent posting schedule\n"
        result += "• Focus basic SEO optimization\n"
        result += "• Build audience với engaging hooks\n"
        result += "• Study competitor successful content\n\n"
    
    # Engagement optimization
    result += "💡 ENGAGEMENT OPTIMIZATION:\n"
    if avg_engagement > 3:
        result += "• Maintain current engagement tactics\n"
        result += "• Test longer content formats\n"
    else:
        result += "• Strengthen hooks trong 3-5 giây đầu\n"
        result += "• Add clear CTAs throughout video\n"
        result += "• Pin engaging comments để trigger responses\n"
    
    # Quick win tactics
    result += "\n⚡ QUICK WIN TACTICS:\n"
    result += "• Create 3 Shorts from best moments của top video\n"
    result += "• Update old video titles với current trends\n"
    result += "• Engage với tất cả comments trong 24h đầu\n"
    result += "• Cross-promote trên social media platforms\n"
    
    # Performance targets
    current_avg = int(avg_views)
    if current_avg > 0:
        target_views = min(current_avg * 2, current_avg + 50000)  # Realistic targets
        target_engagement = min(avg_engagement * 1.5, avg_engagement + 2)
        target_subscribers = max(100, int(current_avg/100))
        
        result += f"\n📊 TARGET CHO 30 NGÀY TỚI:\n"
        result += f"• Avg views: {current_avg:,} → {target_views:,}\n"
        result += f"• Engagement: {avg_engagement:.1f}% → {target_engagement:.1f}%\n"
        result += f"• New subscribers: +{target_subscribers:,}\n"
    
    result += "\n"
    return result


def show_top_videos_details_optimized(data: Dict) -> str:
    """Hiển thị chi tiết top videos - OPTIMIZED VERSION."""
    result = f"""
🏆 7. TOP VIDEOS PERFORMANCE:
{'='*80}

"""
    
    videos = data.get('video', [])
    
    if not videos:
        result += "❌ Không có video data để phân tích.\n"
        return result
    
    # Limit to top 3 for performance
    display_count = 3 if PERFORMANCE_OPTIMIZATIONS else 5
    top_videos = sorted(videos, key=lambda x: x.get('view_count', 0), reverse=True)[:display_count]
    
    for i, video in enumerate(top_videos, 1):
        title = video.get('title', 'No title')
        # Truncate long titles
        if len(title) > 60:
            title = title[:57] + "..."
            
        views = video.get('view_count', 0)
        likes = video.get('like_count', 0)
        comments = video.get('comment_count', 0)
        engagement = video.get('engagement_rate', 0)
        published = video.get('published_at', '')[:10]
        
        result += f"🎬 TOP {i}: {title}\n"
        result += f"   📊 {views:,} views | {likes:,} likes | {comments:,} comments\n"
        result += f"   📈 {engagement:.2f}% engagement"
        
        if published:
            result += f" | 📅 {published}"
        result += "\n"
        
        # Performance assessment
        if engagement > 5:
            result += "   🔥 Exceptional performance\n"
        elif engagement > 2:
            result += "   ⭐ Above average performance\n"
        else:
            result += "   📊 Standard performance\n"
        
        # Quick success factors for top video only
        if i == 1 and engagement > 2:
            result += "   🔑 Success factors:\n"
            factors = analyze_video_success_factors_optimized(video)
            for factor in factors[:3]:  # Limit factors shown
                result += f"      • {factor}\n"
        
        result += "\n"
    
    # Overall insights (simplified)
    if len(videos) > display_count:
        remaining = len(videos) - display_count
        result += f"💡 ... and {remaining} more videos analyzed\n"
        
        # Quick pattern analysis
        avg_top_engagement = sum(v.get('engagement_rate', 0) for v in top_videos) / len(top_videos)
        result += f"📈 Top performers average: {avg_top_engagement:.1f}% engagement\n"
    
    return result


# Helper functions (optimized versions)
def analyze_text_themes_optimized(text: str) -> Dict[str, int]:
    """Phân tích chủ đề từ text - OPTIMIZED."""
    # Simplified themes for performance
    themes = {
        'Tâm lý': ['psychology', 'mind', 'mental'],
        'Quan hệ': ['relationship', 'love', 'partner'],
        'Phát triển': ['improve', 'growth', 'success'],
        'Cảm xúc': ['emotion', 'feel', 'happy']
    }
    
    text_lower = text.lower()
    theme_counts = {}
    
    for theme, keywords in themes.items():
        count = sum(text_lower.count(keyword) for keyword in keywords)
        if count > 0:
            theme_counts[theme] = count
    
    return theme_counts


def analyze_titles_for_themes_optimized(titles: List[str]) -> Dict[str, int]:
    """Phân tích chủ đề từ titles - OPTIMIZED."""
    all_titles = ' '.join(titles).lower()
    
    themes = {
        'Psychology': ['psychology', 'mind', 'mental'],
        'Relationships': ['relationship', 'love', 'dating'],
        'Self-help': ['improve', 'success', 'tips'],
        'Lifestyle': ['life', 'daily', 'routine']
    }
    
    theme_counts = {}
    for theme, keywords in themes.items():
        count = sum(all_titles.count(keyword) for keyword in keywords)
        if count > 0:
            theme_counts[theme] = count
    
    return theme_counts


def analyze_video_success_factors_optimized(video: Dict) -> List[str]:
    """Analyze success factors - OPTIMIZED."""
    factors = []
    
    title = video.get('title', '')
    views = video.get('view_count', 0)
    engagement = video.get('engagement_rate', 0)
    
    # Quick factor analysis
    if '?' in title:
        factors.append("Question hook creates curiosity")
    if any(str(i) in title for i in range(10)):
        factors.append("Numbers in title (specific content)")
    if engagement > 5:
        factors.append(f"High engagement rate ({engagement:.1f}%)")
    if views > 1000000:
        factors.append("Viral reach (1M+ views)")
    
    return factors


# Performance monitoring decorator
def monitor_analysis_performance(func):
    """Decorator to monitor analysis performance"""
    def wrapper(*args, **kwargs):
        if PERFORMANCE_OPTIMIZATIONS:
            import time
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                elapsed = time.time() - start_time
                if elapsed > 2.0:  # Log slow operations
                    logger.warning(f"Slow analysis operation: {func.__name__} took {elapsed:.2f}s")
        else:
            return func(*args, **kwargs)
    return wrapper


# Apply monitoring to main function
format_analysis_results = monitor_analysis_performance(format_analysis_results)


# Additional utility functions for the original implementation
def analyze_content_themes(data: Dict) -> str:
    """Original function for backward compatibility"""
    return analyze_content_themes_optimized(data)


def analyze_us_audience_appeal(data: Dict) -> str:
    """Original function for backward compatibility"""
    return analyze_us_audience_appeal_optimized(data)


def analyze_audience_sentiment(data: Dict) -> str:
    """Original function for backward compatibility"""
    return analyze_audience_sentiment_optimized(data)


def analyze_strengths(data: Dict) -> str:
    """Original function for backward compatibility"""
    return analyze_strengths_optimized(data)


def analyze_weaknesses(data: Dict) -> str:
    """Original function for backward compatibility"""
    return analyze_weaknesses_optimized(data)


def suggest_viral_strategies(data: Dict) -> str:
    """Original function for backward compatibility"""
    return suggest_viral_strategies_optimized(data)


def show_top_videos_details(data: Dict) -> str:
    """Original function for backward compatibility"""
    return show_top_videos_details_optimized(data)


def generate_dynamic_action_items(data: Dict) -> List[str]:
    """Generate dynamic action items based on analysis."""
    action_items = []
    videos = data.get('video', [])
    comments = data.get('bình luận', [])
    transcripts = data.get('transcripts', [])
    summary = data.get('summary', {})
    
    if not videos:
        return ["📊 Thu thập data để có insights cụ thể", 
                "🎯 Bắt đầu với 5 test videos khác nhau"]
    
    # 1. Based on view performance
    avg_views = summary.get('avg_views', 0)
    
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
        
        avg_engagement = summary.get('avg_engagement_rate', 0)
        if top_engagement > avg_engagement * 2:
            action_items.append(f"🔄 Analyze và replicate format của: \"{top_video.get('title', '')[:40]}...\"")
    
    return action_items[:8]  # Limit to 8 action items


def generate_channel_specific_tips(data: Dict) -> List[str]:
    """Generate channel-specific tips based on analysis."""
    tips = []
    videos = data.get('video', [])
    
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