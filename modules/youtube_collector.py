# modules/youtube_collector.py

import os
import re
import json
import time
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import pytube
from urllib.parse import urlparse, parse_qs

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class YouTubeCollector:
    """Collect data from YouTube including video info, transcripts, and comments."""
    
    def __init__(self, api_keys: List[str]):
        """Initialize with list of YouTube API keys for rotation."""
        self.api_keys = api_keys
        self.current_key_index = 0
        self.youtube_service = None
        self._initialize_service()
        
    def _initialize_service(self):
        """Initialize YouTube API service with current API key."""
        if not self.api_keys:
            raise ValueError("No YouTube API keys provided")
            
        try:
            self.youtube_service = build(
                'youtube', 
                'v3', 
                developerKey=self.api_keys[self.current_key_index]
            )
        except Exception as e:
            logger.error(f"Failed to initialize YouTube service: {e}")
            raise
            
    def _rotate_api_key(self):
        """Rotate to next API key when quota exceeded."""
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        self._initialize_service()
        logger.info(f"Rotated to API key index: {self.current_key_index}")
        
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL."""
        # Handle different YouTube URL formats
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:embed\/)([0-9A-Za-z_-]{11})',
            r'(?:watch\?v=)([0-9A-Za-z_-]{11})',
            r'(?:youtu.be\/)([0-9A-Za-z_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
                
        # Try parsing URL
        parsed = urlparse(url)
        if parsed.hostname in ['www.youtube.com', 'youtube.com']:
            query = parse_qs(parsed.query)
            if 'v' in query:
                return query['v'][0]
                
        return None
        
    def extract_channel_id(self, url: str) -> Optional[str]:
        """Extract channel ID from YouTube URL."""
        # Handle different channel URL formats
        patterns = [
            r'youtube\.com\/channel\/([a-zA-Z0-9_-]+)',
            r'youtube\.com\/c\/([a-zA-Z0-9_-]+)',
            r'youtube\.com\/@([a-zA-Z0-9_-]+)',
            r'youtube\.com\/user\/([a-zA-Z0-9_-]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                identifier = match.group(1)
                # If it's a username or handle, need to get channel ID
                if pattern.endswith('user\/([a-zA-Z0-9_-]+)') or pattern.endswith('@([a-zA-Z0-9_-]+)'):
                    return self._get_channel_id_from_username(identifier)
                return identifier
                
        return None
        
    def _get_channel_id_from_username(self, username: str) -> Optional[str]:
        """Get channel ID from username or handle."""
        try:
            # Remove @ if present
            username = username.lstrip('@')
            
            # Search for channel
            request = self.youtube_service.search().list(
                part="snippet",
                q=username,
                type="channel",
                maxResults=1
            )
            response = request.execute()
            
            if response['items']:
                return response['items'][0]['snippet']['channelId']
                
        except HttpError as e:
            if e.resp.status == 403:
                logger.warning("API quota exceeded, rotating key...")
                self._rotate_api_key()
                return self._get_channel_id_from_username(username)
            logger.error(f"Error getting channel ID: {e}")
            
        return None
        
    def get_channel_videos(self, channel_id: str, max_videos: int = 20) -> List[Dict]:
        """Get latest videos from a channel."""
        videos = []
        
        try:
            # Get channel's uploads playlist
            request = self.youtube_service.channels().list(
                part="contentDetails",
                id=channel_id
            )
            response = request.execute()
            
            if not response['items']:
                logger.warning(f"Channel not found: {channel_id}")
                return videos
                
            uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Get videos from uploads playlist
            next_page_token = None
            
            while len(videos) < max_videos:
                try:
                    request = self.youtube_service.playlistItems().list(
                        part="snippet",
                        playlistId=uploads_playlist_id,
                        maxResults=min(50, max_videos - len(videos)),
                        pageToken=next_page_token
                    )
                    response = request.execute()
                    
                    # Log để debug
                    logger.info(f"Fetched {len(response['items'])} videos, total so far: {len(videos)}")
                    
                    if not response['items']:
                        logger.info("No more videos available")
                        break
                    
                    for item in response['items']:
                        if len(videos) >= max_videos:
                            break
                            
                        video_data = {
                            'video_id': item['snippet']['resourceId']['videoId'],
                            'title': item['snippet']['title'],
                            'description': item['snippet']['description'],
                            'published_at': item['snippet']['publishedAt'],
                            'channel_id': item['snippet']['channelId'],
                            'channel_title': item['snippet']['channelTitle'],
                            'thumbnail_url': item['snippet']['thumbnails'].get('high', {}).get('url', '')
                        }
                        videos.append(video_data)
                        
                    next_page_token = response.get('nextPageToken')
                    if not next_page_token:
                        logger.info("No more pages available")
                        break
                        
                except HttpError as e:
                    logger.error(f"Error in pagination: {e}")
                    if e.resp.status == 403:
                        logger.warning("API quota exceeded during video fetch")
                        break
                        
        except HttpError as e:
            if e.resp.status == 403:
                logger.warning("API quota exceeded, rotating key...")
                self._rotate_api_key()
                return self.get_channel_videos(channel_id, max_videos)
            logger.error(f"Error getting channel videos: {e}")
        
        logger.info(f"Total videos collected: {len(videos)} (requested: {max_videos})")
        return videos[:max_videos]
        
    def get_video_details(self, video_id: str) -> Optional[Dict]:
        """Get detailed information about a video."""
        try:
            request = self.youtube_service.videos().list(
                part="snippet,statistics,contentDetails",
                id=video_id
            )
            response = request.execute()
            
            if not response['items']:
                logger.warning(f"Video not found: {video_id}")
                return None
                
            item = response['items'][0]
            
            # Parse duration - KIỂM TRA KEY TỒN TẠI
            duration = item['contentDetails'].get('duration', 'PT0S')  # Default nếu không có
            
            video_details = {
                'video_id': video_id,
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'channel_id': item['snippet']['channelId'],
                'channel_title': item['snippet']['channelTitle'],
                'published_at': item['snippet']['publishedAt'],
                'duration': duration,
                'view_count': int(item['statistics'].get('viewCount', 0)),
                'like_count': int(item['statistics'].get('likeCount', 0)),
                'comment_count': int(item['statistics'].get('commentCount', 0)),
                'tags': item['snippet'].get('tags', []),
                'category_id': item['snippet'].get('categoryId', ''),
                'thumbnail_url': item['snippet']['thumbnails'].get('maxres', {}).get('url') or 
                               item['snippet']['thumbnails'].get('high', {}).get('url', '')
            }
            
            return video_details
            
        except HttpError as e:
            if e.resp.status == 403:
                logger.warning("API quota exceeded, rotating key...")
                self._rotate_api_key()
                return self.get_video_details(video_id)
            logger.error(f"Error getting video details: {e}")
            return None
            
        except Exception as e:
            logger.error(f"Unexpected error getting video details: {e}")
            return None
        
    def get_video_transcript(self, video_id: str, languages: List[str] = ['en']) -> Optional[Dict]:
        """Get transcript for a video."""
        try:
            # Try to get transcript in preferred languages
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            transcript = None
            
            # Try manual transcripts first
            try:
                transcript = transcript_list.find_manually_created_transcript(languages)
            except:
                # Fall back to auto-generated
                try:
                    transcript = transcript_list.find_generated_transcript(languages)
                except:
                    # Try any available transcript
                    try:
                        available_transcripts = list(transcript_list)
                        if available_transcripts:
                            transcript = available_transcripts[0]
                    except:
                        pass
                        
            if not transcript:
                logger.warning(f"No transcript found for video {video_id}")
                return None
                        
            # Fetch the actual transcript
            transcript_data = transcript.fetch()
            
            # Format transcript - FIX: Handle the transcript data properly
            if isinstance(transcript_data, list):
                # Normal case: list of transcript entries
                full_text = ' '.join([entry.get('text', '') for entry in transcript_data])
                segments = transcript_data
            else:
                # Handle other cases
                full_text = str(transcript_data)
                segments = []
            
            return {
                'video_id': video_id,
                'language': getattr(transcript, 'language', 'unknown'),
                'language_code': getattr(transcript, 'language_code', 'unknown'),
                'is_generated': getattr(transcript, 'is_generated', True),
                'full_text': full_text,
                'segments': segments
            }
            
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            logger.warning(f"No transcript available for video {video_id}: {e}")
        except Exception as e:
            logger.error(f"Error getting transcript for video {video_id}: {e}")
            
        return None
        
    def get_video_comments(self, video_id: str, max_comments: int = 100) -> List[Dict]:
        """Get comments for a video."""
        comments = []
        
        try:
            next_page_token = None
            while len(comments) < max_comments:
                request = self.youtube_service.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=min(100, max_comments - len(comments)),
                    order="relevance",
                    pageToken=next_page_token
                )
                response = request.execute()
                
                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']
                    comment_data = {
                        'comment_id': item['id'],
                        'video_id': video_id,
                        'text': comment['textDisplay'],
                        'author': comment['authorDisplayName'],
                        'author_channel_id': comment['authorChannelId']['value'],
                        'like_count': comment['likeCount'],
                        'published_at': comment['publishedAt'],
                        'updated_at': comment['updatedAt']
                    }
                    comments.append(comment_data)
                    
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
                    
        except HttpError as e:
            if e.resp.status == 403:
                if "commentsDisabled" in str(e):
                    logger.warning(f"Comments disabled for video {video_id}")
                else:
                    logger.warning("API quota exceeded, rotating key...")
                    self._rotate_api_key()
                    return self.get_video_comments(video_id, max_comments)
            else:
                logger.error(f"Error getting comments for video {video_id}: {e}")
                
        return comments[:max_comments]
        
    def collect_channel_data(
        self, 
        channel_urls: List[str], 
        max_videos_per_channel: int = 20,
        max_comments_per_video: int = 50,
        include_transcripts: bool = True,
        include_comments: bool = True
    ) -> Dict:
        """Collect comprehensive data from multiple channels."""
        all_data = {
            'channels': [],
            'video': [],
            'transcripts': [],
            'bình luận': [],
            'collection_date': datetime.now().isoformat()
        }
        
        for channel_url in channel_urls:
            logger.info(f"Processing channel: {channel_url}")
            
            # Extract channel ID
            channel_id = self.extract_channel_id(channel_url)
            if not channel_id:
                logger.warning(f"Could not extract channel ID from: {channel_url}")
                continue
                
            # Get channel analytics first
            channel_analytics = self.get_channel_analytics(channel_id)
            if channel_analytics:
                channel_analytics['url'] = channel_url
                all_data['channels'].append(channel_analytics)
                
            # Get channel videos
            videos = self.get_channel_videos(channel_id, max_videos_per_channel)
            logger.info(f"Found {len(videos)} videos for channel {channel_id}")
            
            # Process each video
            for i, video in enumerate(videos):
                video_id = video['video_id']
                logger.info(f"Processing video {i+1}/{len(videos)}: {video_id} - {video['title']}")
                
                # Get detailed video info
                video_details = self.get_video_details(video_id)
                if video_details:
                    all_data['video'].append(video_details)
                    
                # Get transcript if requested
                if include_transcripts:
                    transcript = self.get_video_transcript(video_id)
                    if transcript:
                        all_data['transcripts'].append(transcript)
                        
                # Get comments if requested
                if include_comments:
                    comments = self.get_video_comments(video_id, max_comments_per_video)
                    all_data['bình luận'].extend(comments)
                    
                # Small delay to avoid rate limiting
                time.sleep(0.5)
                
        # Add summary statistics
        all_data['summary'] = self._generate_summary(all_data)
                
        return all_data
        
    def collect_video_data(
        self,
        video_urls: List[str],
        max_comments_per_video: int = 50,
        include_transcripts: bool = True,
        include_comments: bool = True
    ) -> Dict:
        """Collect comprehensive data from specific videos."""
        all_data = {
            'video': [],
            'transcripts': [],
            'bình luận': [],
            'collection_date': datetime.now().isoformat()
        }
        
        for video_url in video_urls:
            logger.info(f"Processing video: {video_url}")
            
            # Extract video ID
            video_id = self.extract_video_id(video_url)
            if not video_id:
                logger.warning(f"Could not extract video ID from: {video_url}")
                continue
                
            # Get detailed video info
            video_details = self.get_video_details(video_id)
            if video_details:
                all_data['video'].append(video_details)
                
            # Get transcript if requested
            if include_transcripts:
                transcript = self.get_video_transcript(video_id)
                if transcript:
                    all_data['transcripts'].append(transcript)
                    
            # Get comments if requested
            if include_comments:
                comments = self.get_video_comments(video_id, max_comments_per_video)
                all_data['bình luận'].extend(comments)
                
            # Small delay to avoid rate limiting
            time.sleep(0.5)
            
        return all_data
        
    def save_collected_data(self, data: Dict, output_file: str):
        """Save collected data to JSON file."""
        try:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Data saved to: {output_file}")
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            
    def get_channel_analytics(self, channel_id: str) -> Dict:
        """Get analytics summary for a channel."""
        try:
            # Get channel statistics
            request = self.youtube_service.channels().list(
                part="statistics,snippet",
                id=channel_id
            )
            response = request.execute()
            
            if not response['items']:
                return {}
                
            item = response['items'][0]
            
            analytics = {
                'channel_id': channel_id,
                'channel_title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'published_at': item['snippet']['publishedAt'],
                'subscriber_count': int(item['statistics'].get('subscriberCount', 0)),
                'view_count': int(item['statistics'].get('viewCount', 0)),
                'video_count': int(item['statistics'].get('videoCount', 0)),
                'country': item['snippet'].get('country', 'Unknown')
            }
            
            return analytics
            
        except HttpError as e:
            if e.resp.status == 403:
                logger.warning("API quota exceeded, rotating key...")
                self._rotate_api_key()
                return self.get_channel_analytics(channel_id)
            logger.error(f"Error getting channel analytics: {e}")
            
        return {}
        
    def search_videos(
        self,
        query: str,
        max_results: int = 50,
        order: str = "relevance",
        published_after: Optional[str] = None
    ) -> List[Dict]:
        """Search for videos based on query."""
        videos = []
        
        try:
            search_params = {
                'part': 'snippet',
                'q': query,
                'type': 'video',
                'maxResults': min(50, max_results),
                'order': order
            }
            
            if published_after:
                search_params['publishedAfter'] = published_after
                
            next_page_token = None
            while len(videos) < max_results:
                if next_page_token:
                    search_params['pageToken'] = next_page_token
                    
                request = self.youtube_service.search().list(**search_params)
                response = request.execute()
                
                for item in response['items']:
                    video_data = {
                        'video_id': item['id']['videoId'],
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'channel_id': item['snippet']['channelId'],
                        'channel_title': item['snippet']['channelTitle'],
                        'published_at': item['snippet']['publishedAt'],
                        'thumbnail_url': item['snippet']['thumbnails']['high']['url']
                    }
                    videos.append(video_data)
                    
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
                    
        except HttpError as e:
            if e.resp.status == 403:
                logger.warning("API quota exceeded, rotating key...")
                self._rotate_api_key()
                return self.search_videos(query, max_results, order, published_after)
            logger.error(f"Error searching videos: {e}")
            
        return videos[:max_results]
        
    def get_trending_videos(self, region_code: str = 'US', category_id: Optional[str] = None) -> List[Dict]:
        """Get trending videos for a specific region."""
        videos = []
        
        try:
            params = {
                'part': 'snippet,statistics',
                'chart': 'mostPopular',
                'regionCode': region_code,
                'maxResults': 50
            }
            
            if category_id:
                params['videoCategoryId'] = category_id
                
            request = self.youtube_service.videos().list(**params)
            response = request.execute()
            
            for item in response['items']:
                video_data = {
                    'video_id': item['id'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'channel_id': item['snippet']['channelId'],
                    'channel_title': item['snippet']['channelTitle'],
                    'published_at': item['snippet']['publishedAt'],
                    'view_count': int(item['statistics'].get('viewCount', 0)),
                    'like_count': int(item['statistics'].get('likeCount', 0)),
                    'comment_count': int(item['statistics'].get('commentCount', 0)),
                    'category_id': item['snippet'].get('categoryId', ''),
                    'tags': item['snippet'].get('tags', [])
                }
                videos.append(video_data)
                
        except HttpError as e:
            if e.resp.status == 403:
                logger.warning("API quota exceeded, rotating key...")
                self._rotate_api_key()
                return self.get_trending_videos(region_code, category_id)
            logger.error(f"Error getting trending videos: {e}")
            
        return videos

    def _generate_summary(self, data: Dict) -> Dict:
        """Generate summary statistics for collected data."""
        summary = {
            'channels_analyzed': len(data.get('channels', [])),
            'total_videos': len(data.get('video', [])),
            'total_comments': len(data.get('bình luận', [])),
            'total_transcripts': len(data.get('transcripts', [])),
            'total_views': sum(video.get('view_count', 0) for video in data.get('video', [])),
            'total_likes': sum(video.get('like_count', 0) for video in data.get('video', [])),
            'avg_engagement_rate': 0,
            'top_categories': {},
            'date_range': {'start': 'N/A', 'end': 'N/A'}
        }
        
        # Calculate average engagement rate
        videos = data.get('video', [])
        if videos:
            total_engagement = 0
            valid_videos = 0
            
            for video in videos:
                views = video.get('view_count', 0)
                likes = video.get('like_count', 0)
                comments = video.get('comment_count', 0)
                
                if views > 0:
                    engagement_rate = ((likes + comments) / views) * 100
                    total_engagement += engagement_rate
                    valid_videos += 1
                    
            if valid_videos > 0:
                summary['avg_engagement_rate'] = total_engagement / valid_videos
                
            # Get date range
            dates = [video.get('published_at', '') for video in videos if video.get('published_at')]
            if dates:
                dates.sort()
                summary['date_range'] = {
                    'start': dates[0][:10] if dates[0] else 'N/A',
                    'end': dates[-1][:10] if dates[-1] else 'N/A'
                }
                
            # Count categories
            categories = {}
            for video in videos:
                category = video.get('category_id', 'Unknown')
                categories[category] = categories.get(category, 0) + 1
            summary['top_categories'] = dict(sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5])
            
        return summary


# Utility functions for standalone usage
def extract_urls_from_text(text: str) -> Tuple[List[str], List[str]]:
    """Extract YouTube channel and video URLs from text."""
    channel_urls = []
    video_urls = []
    
    # Patterns for different URL types
    channel_patterns = [
        r'(https?://(?:www\.)?youtube\.com/channel/[a-zA-Z0-9_-]+)',
        r'(https?://(?:www\.)?youtube\.com/c/[a-zA-Z0-9_-]+)',
        r'(https?://(?:www\.)?youtube\.com/@[a-zA-Z0-9_-]+)',
        r'(https?://(?:www\.)?youtube\.com/user/[a-zA-Z0-9_-]+)'
    ]
    
    video_patterns = [
        r'(https?://(?:www\.)?youtube\.com/watch\?v=[a-zA-Z0-9_-]+)',
        r'(https?://(?:www\.)?youtu\.be/[a-zA-Z0-9_-]+)'
    ]
    
    # Extract channel URLs
    for pattern in channel_patterns:
        matches = re.findall(pattern, text)
        channel_urls.extend(matches)
        
    # Extract video URLs
    for pattern in video_patterns:
        matches = re.findall(pattern, text)
        video_urls.extend(matches)
        
    # Remove duplicates while preserving order
    channel_urls = list(dict.fromkeys(channel_urls))
    video_urls = list(dict.fromkeys(video_urls))
    
    return channel_urls, video_urls


def validate_youtube_url(url: str) -> Tuple[bool, str]:
    """Validate YouTube URL and return type."""
    url = url.strip()
    
    # Check if it's a valid YouTube domain
    youtube_domains = ['youtube.com', 'www.youtube.com', 'youtu.be', 'm.youtube.com']
    parsed = urlparse(url)
    
    if parsed.hostname not in youtube_domains:
        return False, "invalid"
        
    # Check URL patterns
    if any(pattern in url for pattern in ['/channel/', '/c/', '/@', '/user/']):
        return True, "channel"
    elif '/watch?v=' in url or 'youtu.be/' in url:
        return True, "video"
    else:
        return False, "invalid"


class YouTubeDataProcessor:
    """Process and format YouTube data for analysis."""
    
    @staticmethod
    def format_for_display(data: Dict) -> Dict:
        """Format collected data for UI display."""
        display_data = {
            'summary': data.get('summary', {}),
            'channels': [],
            'top_videos': [],
            'recent_comments': [],
            'transcript_preview': ''
        }
        
        # Format channels
        for channel in data.get('channels', []):
            display_data['channels'].append({
                'title': channel.get('channel_title', 'Unknown'),
                'subscribers': f"{channel.get('subscriber_count', 0):,}",
                'total_views': f"{channel.get('view_count', 0):,}",
                'video_count': channel.get('video_count', 0)
            })
            
        # Get top videos by views
        videos = sorted(data.get('video', []), key=lambda x: x.get('view_count', 0), reverse=True)
        for video in videos[:10]:
            display_data['top_videos'].append({
                'title': video.get('title', ''),
                'lượt xem': f"{video.get('view_count', 0):,}",
                'lượt thích': f"{video.get('like_count', 0):,}",
                'engagement_rate': f"{((video.get('like_count', 0) + video.get('comment_count', 0)) / video.get('view_count', 1) * 100):.2f}%",
                'published': video.get('published_at', '')[:10]
            })
            
        # Get recent comments
        comments = sorted(data.get('bình luận', []), key=lambda x: x.get('like_count', 0), reverse=True)
        for comment in comments[:20]:
            display_data['recent_comments'].append({
                'text': comment.get('text', '')[:200] + '...' if len(comment.get('text', '')) > 200 else comment.get('text', ''),
                'lượt thích': comment.get('like_count', 0),
                'author': comment.get('author', 'Anonymous')
            })
            
        return display_data
        
    @staticmethod
    def export_to_json(data: Dict, filename: str):
        """Export data to JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Data exported to {filename}")
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            
    @staticmethod
    def export_to_csv(data: Dict, filename: str):
        """Export video data to CSV file."""
        try:
            import csv
            
            videos = data.get('video', [])
            if not videos:
                logger.warning("No video data to export")
                return
                
            fieldnames = [
                'video_id', 'title', 'channel_title', 'published_at',
                'view_count', 'like_count', 'comment_count', 'duration',
                'engagement_rate', 'category_id'
            ]
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for video in videos:
                    views = video.get('view_count', 1)
                    likes = video.get('like_count', 0)
                    comments = video.get('comment_count', 0)
                    engagement_rate = ((likes + comments) / views) * 100 if views > 0 else 0
                    
                    row = {
                        'video_id': video.get('video_id', ''),
                        'title': video.get('title', ''),
                        'channel_title': video.get('channel_title', ''),
                        'published_at': video.get('published_at', ''),
                        'view_count': video.get('view_count', 0),
                        'like_count': video.get('like_count', 0),
                        'comment_count': video.get('comment_count', 0),
                        'duration': video.get('duration', ''),
                        'engagement_rate': f"{engagement_rate:.2f}",
                        'category_id': video.get('category_id', '')
                    }
                    writer.writerow(row)
                    
            logger.info(f"Video data exported to {filename}")
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")


# Example usage
if __name__ == "__main__":
    # Example API keys (replace with actual keys)
    api_keys = ["YOUR_API_KEY_1", "YOUR_API_KEY_2"]
    
    # Initialize collector
    collector = YouTubeCollector(api_keys)
    
    # Example: Collect data from channels
    channel_urls = [
        "https://www.youtube.com/@MrBeast",
        "https://www.youtube.com/@PewDiePie"
    ]
    
    channel_data = collector.collect_channel_data(
        channel_urls=channel_urls,
        max_videos_per_channel=10,
        max_comments_per_video=50,
        include_transcripts=True,
        include_comments=True
    )
    
    # Save data
    collector.save_collected_data(channel_data, "output/channel_data.json")
    
    # Example: Collect data from specific videos
    video_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=9bZkp7q19f0"
    ]
    
    video_data = collector.collect_video_data(
        video_urls=video_urls,
        max_comments_per_video=100,
        include_transcripts=True,
        include_comments=True
    )
    
    # Save data
    collector.save_collected_data(video_data, "output/video_data.json")