"""
YouTube Integration Module - Connects UI with YouTube Collector
"""

import threading
from typing import Dict, List, Callable, Optional
from datetime import datetime
import logging

from .youtube_collector import YouTubeCollector, extract_urls_from_text, validate_youtube_url

logger = logging.getLogger(__name__)


class YouTubeAnalysisManager:
    """Manages YouTube data collection and analysis."""
    
    def __init__(self, youtube_keys: List[str], openai_keys: List[str] = None):
        self.youtube_keys = youtube_keys
        self.openai_keys = openai_keys or []
        self.collector = None
        self.is_analyzing = False
        self.current_thread = None
        
        if youtube_keys:
            self.collector = YouTubeCollector(youtube_keys)
        
    def start_analysis(
        self,
        urls: List[str],
        analysis_mode: str = "channel",
        max_videos: int = 20,
        max_comments: int = 50,
        include_transcript: bool = True,
        include_comments: bool = True,
        progress_callback: Callable = None,
        completion_callback: Callable = None
    ):
        """Start YouTube data collection in background thread."""
        
        if self.is_analyzing:
            logger.warning("Analysis already in progress")
            return
            
        if not self.collector:
            logger.error("No YouTube collector initialized")
            if completion_callback:
                completion_callback({
                    'status': 'error',
                    'message': 'YouTube collector not initialized. Check API keys.'
                })
            return
            
        self.is_analyzing = True
        
        # Run analysis in background thread
        self.current_thread = threading.Thread(
            target=self._run_analysis,
            args=(urls, analysis_mode, max_videos, max_comments, 
                  include_transcript, include_comments,
                  progress_callback, completion_callback)
        )
        self.current_thread.daemon = True
        self.current_thread.start()
        
    def _run_analysis(
        self,
        urls: List[str],
        analysis_mode: str,
        max_videos: int,
        max_comments: int,
        include_transcript: bool,
        include_comments: bool,
        progress_callback: Callable,
        completion_callback: Callable
    ):
        """Run the actual analysis."""
        try:
            # Separate channel and video URLs
            channel_urls = []
            video_urls = []
            
            for url in urls:
                is_valid, url_type = validate_youtube_url(url)
                if is_valid:
                    if url_type == "channel":
                        channel_urls.append(url)
                    elif url_type == "video":
                        video_urls.append(url)
                        
            # Progress update
            if progress_callback:
                progress_callback({
                    'status': 'collecting',
                    'message': f'Found {len(channel_urls)} channels and {len(video_urls)} videos',
                    'progress': 10
                })
                
            # Collect data
            all_data = {
                'channels': [],
                'videos': [],
                'transcripts': [],
                'comments': [],
                'collection_date': datetime.now().isoformat()
            }
            
            # Collect channel data
            if channel_urls and analysis_mode == "channel":
                if progress_callback:
                    progress_callback({
                        'status': 'collecting',
                        'message': 'Collecting channel data...',
                        'progress': 20
                    })
                    
                channel_data = self.collector.collect_channel_data(
                    channel_urls=channel_urls,
                    max_videos_per_channel=max_videos,
                    max_comments_per_video=max_comments,
                    include_transcripts=include_transcript,
                    include_comments=include_comments
                )
                
                # Merge data
                all_data['channels'].extend(channel_data.get('channels', []))
                all_data['videos'].extend(channel_data.get('videos', []))
                all_data['transcripts'].extend(channel_data.get('transcripts', []))
                all_data['comments'].extend(channel_data.get('comments', []))
                
            # Collect video data
            if video_urls:
                if progress_callback:
                    progress_callback({
                        'status': 'collecting',
                        'message': 'Collecting video data...',
                        'progress': 50
                    })
                    
                video_data = self.collector.collect_video_data(
                    video_urls=video_urls,
                    max_comments_per_video=max_comments,
                    include_transcripts=include_transcript,
                    include_comments=include_comments
                )
                
                # Merge data
                all_data['videos'].extend(video_data.get('videos', []))
                all_data['transcripts'].extend(video_data.get('transcripts', []))
                all_data['comments'].extend(video_data.get('comments', []))
                
            # Generate summary
            if progress_callback:
                progress_callback({
                    'status': 'analyzing',
                    'message': 'Analyzing collected data...',
                    'progress': 80
                })
                
            all_data['summary'] = self.collector._generate_summary(all_data)
            
            # Calculate viral score
            viral_score = self._calculate_viral_score(all_data)
            
            # Final progress
            if progress_callback:
                progress_callback({
                    'status': 'complete',
                    'message': 'Analysis complete!',
                    'progress': 100
                })
                
            # Send completion callback
            if completion_callback:
                completion_callback({
                    'status': 'success',
                    'data': all_data,
                    'viral_score': viral_score,
                    'message': f'Successfully analyzed {len(all_data["videos"])} videos'
                })
                
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            if completion_callback:
                completion_callback({
                    'status': 'error',
                    'message': str(e),
                    'error': str(e)
                })
                
        finally:
            self.is_analyzing = False
            
    def _calculate_viral_score(self, data: Dict) -> float:
        """Calculate overall viral potential score."""
        videos = data.get('videos', [])
        if not videos:
            return 0.0
            
        total_score = 0
        valid_videos = 0
        
        for video in videos:
            views = video.get('view_count', 0)
            likes = video.get('like_count', 0)
            comments = video.get('comment_count', 0)
            
            if views > 0:
                # Engagement rate
                engagement_rate = ((likes + comments) / views) * 100
                
                # View-based score
                view_score = min(30, views / 1000000 * 30)  # Max 30 points for 1M+ views
                
                # Engagement-based score
                engagement_score = min(50, engagement_rate * 10)  # Max 50 points for 5%+ engagement
                
                # Like ratio score
                like_ratio = (likes / views) * 100
                like_score = min(20, like_ratio * 4)  # Max 20 points for 5%+ like ratio
                
                video_score = view_score + engagement_score + like_score
                total_score += video_score
                valid_videos += 1
                
        if valid_videos > 0:
            return min(100, total_score / valid_videos)
        else:
            return 0.0
            
    def stop_analysis(self):
        """Stop current analysis if running."""
        if self.is_analyzing and self.current_thread:
            # Note: Can't directly stop thread, but can set flag
            self.is_analyzing = False
            logger.info("Analysis stop requested")
            
    def export_data(self, format: str, filename: str) -> str:
        """Export collected data to file."""
        if not hasattr(self, 'last_collected_data'):
            raise ValueError("No data to export")
            
        if format == "json":
            YouTubeDataProcessor.export_to_json(self.last_collected_data, filename)
        elif format == "csv":
            YouTubeDataProcessor.export_to_csv(self.last_collected_data, filename)
        else:
            raise ValueError(f"Unsupported format: {format}")
            
        return filename


class YouTubeDataProcessor:
    """Process YouTube data for export and display."""
    
    @staticmethod
    def export_to_json(data: Dict, filename: str):
        """Export data to JSON file."""
        import json
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    @staticmethod
    def export_to_csv(data: Dict, filename: str):
        """Export video data to CSV file."""
        import csv
        
        videos = data.get('videos', [])
        if not videos:
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