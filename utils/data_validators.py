"""
Data validation utilities
"""

import re
from typing import Tuple, List, Optional
from urllib.parse import urlparse, parse_qs


class YouTubeURLValidator:
    """Validates and extracts information from YouTube URLs."""
    
    CHANNEL_PATTERNS = [
        r'youtube\.com\/channel\/([a-zA-Z0-9_-]+)',
        r'youtube\.com\/c\/([a-zA-Z0-9_-]+)',
        r'youtube\.com\/@([a-zA-Z0-9_-]+)',
        r'youtube\.com\/user\/([a-zA-Z0-9_-]+)'
    ]
    
    VIDEO_PATTERNS = [
        r'youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})',
        r'youtu\.be\/([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})'
    ]
    
    @classmethod
    def extract_video_id(cls, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL."""
        for pattern in cls.VIDEO_PATTERNS:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        # Try parsing URL parameters
        parsed = urlparse(url)
        if parsed.hostname in ['www.youtube.com', 'youtube.com']:
            query = parse_qs(parsed.query)
            if 'v' in query:
                return query['v'][0]
                
        return None
    
    @classmethod
    def extract_channel_id(cls, url: str) -> Optional[str]:
        """Extract channel identifier from YouTube URL."""
        for pattern in cls.CHANNEL_PATTERNS:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    @classmethod
    def is_valid_youtube_url(cls, url: str) -> bool:
        """Check if URL is a valid YouTube URL."""
        return cls.extract_video_id(url) is not None or cls.extract_channel_id(url) is not None
    
    @classmethod
    def get_url_type(cls, url: str) -> str:
        """Determine if URL is channel or video."""
        if cls.extract_video_id(url):
            return "video"
        elif cls.extract_channel_id(url):
            return "channel"
        else:
            return "unknown"
    
    @classmethod
    def validate_url_list(cls, urls: List[str]) -> Tuple[List[str], List[str], List[str]]:
        """Validate a list of URLs and categorize them."""
        valid_urls = []
        invalid_urls = []
        warnings = []
        
        for url in urls:
            url = url.strip()
            if not url:
                continue
                
            if cls.is_valid_youtube_url(url):
                valid_urls.append(url)
            else:
                invalid_urls.append(url)
                warnings.append(f"Invalid YouTube URL: {url}")
        
        return valid_urls, invalid_urls, warnings


class DataValidator:
    """Validates data integrity and completeness."""
    
    @staticmethod
    def validate_video_data(video: dict) -> Tuple[bool, List[str]]:
        """Validate video data completeness."""
        required_fields = ['video_id', 'title', 'view_count']
        errors = []
        
        for field in required_fields:
            if field not in video or video[field] is None:
                errors.append(f"Missing required field: {field}")
        
        # Validate data types
        if 'view_count' in video:
            try:
                int(video['view_count'])
            except (ValueError, TypeError):
                errors.append("Invalid view_count: must be a number")
        
        if 'published_at' in video and video['published_at']:
            try:
                from datetime import datetime
                datetime.fromisoformat(video['published_at'].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                errors.append("Invalid published_at date format")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_analysis_data(data: dict) -> Tuple[bool, List[str]]:
        """Validate complete analysis data structure."""
        required_sections = ['video', 'summary']
        errors = []
        
        for section in required_sections:
            if section not in data:
                errors.append(f"Missing required section: {section}")
        
        # Validate videos
        if 'video' in data:
            for i, video in enumerate(data['video']):
                is_valid, video_errors = DataValidator.validate_video_data(video)
                if not is_valid:
                    errors.extend([f"Video {i+1}: {error}" for error in video_errors])
        
        # Validate summary
        if 'summary' in data:
            summary = data['summary']
            required_summary_fields = ['total_videos', 'total_views']
            
            for field in required_summary_fields:
                if field not in summary:
                    errors.append(f"Missing summary field: {field}")
        
        return len(errors) == 0, errors


def validate_url(url: str) -> bool:
    """Validate if a string is a valid URL."""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None


def validate_email(email: str) -> bool:
    """Validate if a string is a valid email."""
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return email_pattern.match(email) is not None