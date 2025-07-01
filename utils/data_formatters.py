"""
Data formatting utilities
"""

from typing import Union
from datetime import datetime
import re


class DataFormatter:
    """Formats data for display and export."""
    
    @staticmethod
    def format_number(number: Union[int, float], format_type: str = "default") -> str:
        """Format numbers with appropriate units."""
        if not isinstance(number, (int, float)) or number < 0:
            return "0"
            
        if format_type == "lượt xem" or format_type == "subscribers":
            if number >= 1_000_000_000:
                return f"{number / 1_000_000_000:.1f}B"
            elif number >= 1_000_000:
                return f"{number / 1_000_000:.1f}M"
            elif number >= 1_000:
                return f"{number / 1_000:.1f}K"
            else:
                return str(int(number))
        elif format_type == "percentage":
            return f"{number:.2f}%"
        elif format_type == "currency":
            return f"${number:,.2f}"
        else:
            return f"{number:,}"
    
    @staticmethod
    def format_duration(duration_str: str) -> str:
        """Format ISO 8601 duration to readable format."""
        if not duration_str:
            return "Unknown"
            
        # Parse ISO 8601 duration (PT4M13S format)
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
        if not match:
            return duration_str
            
        hours, minutes, seconds = match.groups()
        hours = int(hours) if hours else 0
        minutes = int(minutes) if minutes else 0
        seconds = int(seconds) if seconds else 0
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    
    @staticmethod
    def format_date(date_str: str, format_type: str = "short") -> str:
        """Format ISO date string to readable format."""
        if not date_str:
            return "Unknown"
            
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            
            if format_type == "short":
                return dt.strftime("%Y-%m-%d")
            elif format_type == "long":
                return dt.strftime("%B %d, %Y")
            elif format_type == "relative":
                now = datetime.now(dt.tzinfo)
                diff = now - dt
                
                if diff.days > 365:
                    return f"{diff.days // 365} year{'s' if diff.days // 365 > 1 else ''} ago"
                elif diff.days > 30:
                    return f"{diff.days // 30} month{'s' if diff.days // 30 > 1 else ''} ago"
                elif diff.days > 0:
                    return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
                elif diff.seconds > 3600:
                    hours = diff.seconds // 3600
                    return f"{hours} hour{'s' if hours > 1 else ''} ago"
                elif diff.seconds > 60:
                    minutes = diff.seconds // 60
                    return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
                else:
                    return "Just now"
            else:
                return dt.strftime("%Y-%m-%d %H:%M")
                
        except (ValueError, TypeError):
            return date_str
    
    @staticmethod
    def format_engagement_rate(likes: int, comments: int, views: int) -> str:
        """Calculate and format engagement rate."""
        if views == 0:
            return "0.00%"
        
        engagement = ((likes + comments) / views) * 100
        return f"{engagement:.2f}%"
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
        """Truncate text to specified length."""
        if not text or len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix


class TextProcessor:
    """Processes and cleans text data."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text data."""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\:\;]', '', text)
        
        return text
    
    @staticmethod
    def extract_keywords(text: str, min_length: int = 3) -> list:
        """Extract keywords from text."""
        if not text:
            return []
        
        # Common stop words
        stop_words = {
            'the', 'a', 'an', 'và', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'trên', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
        }
        
        # Extract words
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        keywords = [word for word in words 
                   if len(word) >= min_length and word not in stop_words]
        
        # Count frequency and return top keywords
        from collections import Counter
        word_count = Counter(keywords)
        return [word for word, count in word_count.most_common(20)]
    
    @staticmethod
    def summarize_text(text: str, max_sentences: int = 3) -> str:
        """Create a simple summary of text."""
        if not text:
            return ""
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= max_sentences:
            return text
        
        # Return first few sentences as summary
        return '. '.join(sentences[:max_sentences]) + '.'
    
    @staticmethod
    def detect_language(text: str) -> str:
        """Simple language detection."""
        if not text:
            return "unknown"
        
        # Simple heuristic based on common words
        english_words = ['the', 'và', 'is', 'in', 'to', 'trên', 'a', 'that', 'it', 'with']
        vietnamese_words = ['và', 'là', 'có', 'được', 'này', 'của', 'cho', 'một', 'trong', 'không']
        
        text_lower = text.lower()
        
        english_count = sum(1 for word in english_words if word in text_lower)
        vietnamese_count = sum(1 for word in vietnamese_words if word in text_lower)
        
        if english_count > vietnamese_count:
            return "english"
        elif vietnamese_count > 0:
            return "vietnamese"
        else:
            return "unknown"


def format_number(number: Union[int, float]) -> str:
    """Format number with commas."""
    return f"{number:,}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format percentage with specified decimal places."""
    return f"{value:.{decimals}f}%"


def safe_get(dictionary: dict, key: str, default=None, type_cast=None):
    """Safely get value from dictionary with optional type casting."""
    value = dictionary.get(key, default)
    
    if type_cast and value is not None:
        try:
            return type_cast(value)
        except (ValueError, TypeError):
            return default
    
    return value