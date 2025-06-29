"""
Data analysis utilities
"""

from typing import Dict, List, Any, Optional
from collections import Counter
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataAnalyzer:
    """Analyzes YouTube data and provides insights."""
    
    @staticmethod
    def calculate_viral_score(video_data: dict) -> float:
        """Calculate viral potential score for a video."""
        views = video_data.get('view_count', 0)
        likes = video_data.get('like_count', 0)
        comments = video_data.get('comment_count', 0)
        
        if views == 0:
            return 0.0
        
        # Calculate various metrics
        engagement_rate = ((likes + comments) / views) * 100
        like_ratio = (likes / views) * 100 if views > 0 else 0
        comment_ratio = (comments / views) * 100 if views > 0 else 0
        
        # Weighted scoring
        score = 0
        
        # Engagement rate (40% weight)
        if engagement_rate >= 10:
            score += 40
        elif engagement_rate >= 5:
            score += 30
        elif engagement_rate >= 2:
            score += 20
        elif engagement_rate >= 1:
            score += 10
        
        # View count relative scoring (30% weight)
        if views >= 1_000_000:
            score += 30
        elif views >= 100_000:
            score += 25
        elif views >= 10_000:
            score += 20
        elif views >= 1_000:
            score += 10
        
        # Like ratio (20% weight)
        if like_ratio >= 5:
            score += 20
        elif like_ratio >= 2:
            score += 15
        elif like_ratio >= 1:
            score += 10
        elif like_ratio >= 0.5:
            score += 5
        
        # Comment engagement (10% weight)
        if comment_ratio >= 1:
            score += 10
        elif comment_ratio >= 0.5:
            score += 8
        elif comment_ratio >= 0.1:
            score += 5
        
        return min(score, 100.0)
    
    @staticmethod
    def analyze_content_themes(transcripts: List[dict]) -> Dict[str, int]:
        """Analyze content themes from transcripts."""
        if not transcripts:
            return {}
        
        # Psychology and relationship keywords
        theme_keywords = {
            'Psychology': [
                'psychology', 'mind', 'brain', 'mental', 'emotion', 'behavior',
                'cognitive', 'unconscious', 'subconscious', 'therapy', 'anxiety',
                'depression', 'trauma', 'healing', 'mindset'
            ],
            'Relationships': [
                'relationship', 'love', 'dating', 'partner', 'marriage', 'couple',
                'romance', 'attraction', 'chemistry', 'soulmate', 'heartbreak',
                'breakup', 'divorce', 'family', 'friendship'
            ],
            'Self Development': [
                'self', 'improve', 'growth', 'develop', 'success', 'confidence',
                'motivation', 'goal', 'achieve', 'potential', 'mindset',
                'productivity', 'habits', 'discipline'
            ],
            'Communication': [
                'communication', 'talk', 'speak', 'listen', 'conversation',
                'social', 'interaction', 'expression', 'language', 'body language'
            ],
            'Emotions': [
                'emotion', 'feel', 'feeling', 'happy', 'sad', 'angry', 'fear',
                'joy', 'excitement', 'stress', 'calm', 'peace', 'anger'
            ]
        }
        
        theme_counts = {}
        all_text = ""
        
        # Combine all transcript text
        for transcript in transcripts:
            text = transcript.get('full_text', '').lower()
            all_text += text + " "
        
        # Count theme occurrences
        for theme, keywords in theme_keywords.items():
            count = 0
            for keyword in keywords:
                count += all_text.count(keyword.lower())
            if count > 0:
                theme_counts[theme] = count
        
        return theme_counts
    
    @staticmethod
    def analyze_audience_sentiment(comments: List[dict]) -> Dict[str, Any]:
        """Analyze audience sentiment from comments."""
        if not comments:
            return {"sentiment": "neutral", "confidence": 0, "breakdown": {}}
        
        sentiment_keywords = {
            'positive': [
                'love', 'amazing', 'great', 'awesome', 'fantastic', 'excellent',
                'perfect', 'wonderful', 'brilliant', 'outstanding', 'incredible',
                'thank', 'helpful', 'useful', 'inspiring', 'motivating'
            ],
            'negative': [
                'hate', 'terrible', 'awful', 'bad', 'worst', 'boring',
                'stupid', 'waste', 'disappointed', 'disagree', 'wrong'
            ],
            'excited': [
                'excited', 'wow', 'omg', 'amazing', 'mind blown',
                'shocking', 'unbelievable', 'crazy', 'insane'
            ],
            'grateful': [
                'thank', 'grateful', 'appreciate', 'helped', 'changed my life',
                'saved', 'blessing', 'thankful'
            ]
        }
        
        sentiment_scores = {'positive': 0, 'negative': 0, 'excited': 0, 'grateful': 0}
        total_comments = len(comments)
        
        for comment in comments:
            text = comment.get('text', '').lower()
            
            for sentiment, keywords in sentiment_keywords.items():
                for keyword in keywords:
                    if keyword in text:
                        sentiment_scores[sentiment] += 1
                        break  # Count each comment only once per sentiment
        
        # Calculate percentages
        sentiment_breakdown = {}
        for sentiment, count in sentiment_scores.items():
            percentage = (count / total_comments) * 100 if total_comments > 0 else 0
            sentiment_breakdown[sentiment] = {
                'count': count,
                'percentage': percentage
            }
        
        # Determine overall sentiment
        positive_score = sentiment_scores['positive'] + sentiment_scores['excited'] + sentiment_scores['grateful']
        negative_score = sentiment_scores['negative']
        
        if positive_score > negative_score * 2:
            overall_sentiment = "very_positive"
            confidence = min((positive_score / total_comments) * 100, 100)
        elif positive_score > negative_score:
            overall_sentiment = "positive"
            confidence = min(((positive_score - negative_score) / total_comments) * 100, 100)
        elif negative_score > positive_score:
            overall_sentiment = "negative"
            confidence = min(((negative_score - positive_score) / total_comments) * 100, 100)
        else:
            overall_sentiment = "neutral"
            confidence = 50
        
        return {
            "sentiment": overall_sentiment,
            "confidence": confidence,
            "breakdown": sentiment_breakdown,
            "total_analyzed": total_comments
        }
    
    @staticmethod
    def find_top_performing_videos(videos: List[dict], metric: str = "engagement") -> List[dict]:
        """Find top performing videos by specified metric."""
        if not videos:
            return []
        
        def get_sort_key(video):
            if metric == "engagement":
                views = video.get('view_count', 1)
                likes = video.get('like_count', 0)
                comments = video.get('comment_count', 0)
                return ((likes + comments) / views) * 100 if views > 0 else 0
            elif metric == "views":
                return video.get('view_count', 0)
            elif metric == "likes":
                return video.get('like_count', 0)
            elif metric == "comments":
                return video.get('comment_count', 0)
            else:
                return 0
        
        return sorted(videos, key=get_sort_key, reverse=True)
    
    @staticmethod
    def analyze_posting_patterns(videos: List[dict]) -> Dict[str, Any]:
        """Analyze posting patterns and optimal times."""
        if not videos:
            return {}
        
        posting_data = {
            'days_of_week': {},
            'hours_of_day': {},
            'monthly_pattern': {},
            'optimal_times': []
        }
        
        for video in videos:
            published_at = video.get('published_at', '')
            if not published_at:
                continue
                
            try:
                dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                
                # Day of week (0=Monday, 6=Sunday)
                day_name = dt.strftime('%A')
                posting_data['days_of_week'][day_name] = posting_data['days_of_week'].get(day_name, 0) + 1
                
                # Hour of day
                hour = dt.hour
                posting_data['hours_of_day'][hour] = posting_data['hours_of_day'].get(hour, 0) + 1
                
                # Month
                month_name = dt.strftime('%B')
                posting_data['monthly_pattern'][month_name] = posting_data['monthly_pattern'].get(month_name, 0) + 1
                
            except (ValueError, TypeError):
                continue
        
        # Find optimal posting times (most frequent)
        if posting_data['hours_of_day']:
            optimal_hours = sorted(posting_data['hours_of_day'].items(), 
                                 key=lambda x: x[1], reverse=True)[:3]
            posting_data['optimal_times'] = [f"{hour}:00" for hour, _ in optimal_hours]
        
        return posting_data