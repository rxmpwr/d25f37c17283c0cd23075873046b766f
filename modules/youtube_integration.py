"""
YouTube Integration Module - Manages YouTube data collection and AI analysis
FIXED VERSION with proper error handling
"""

import threading
import time
from typing import List, Dict, Optional, Callable
from datetime import datetime
import logging
import json

# Import YouTube collector
from modules.youtube_collector import YouTubeCollector

# Import OpenAI for analysis
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI not available. Install with: pip install openai")

logger = logging.getLogger(__name__)


class YouTubeAnalysisManager:
    """Manages YouTube analysis workflow with AI integration."""
    
    def __init__(self, youtube_api_keys: List[str], openai_api_keys: List[str] = None):
        """Initialize with API keys."""
        self.youtube_api_keys = youtube_api_keys
        self.openai_api_keys = openai_api_keys or []
        
        # Initialize YouTube collector
        self.collector = YouTubeCollector(youtube_api_keys)
        
        # Initialize OpenAI client if available
        self.openai_client = None
        if OPENAI_AVAILABLE and self.openai_api_keys:
            try:
                self.openai_client = OpenAI(api_key=self.openai_api_keys[0])
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
        
        # Progress tracking
        self.progress_callback = None
        self.complete_callback = None
        self.start_time = None
        self.is_analyzing = False
        
    def start_analysis(self, urls: List[str], mode: str = 'channel', 
                      max_videos: int = 20, max_comments: int = 50,
                      include_transcript: bool = True, include_comments: bool = True,
                      progress_callback: Optional[Callable] = None,
                      complete_callback: Optional[Callable] = None,
                      custom_requirements: str = None):
        """Start YouTube analysis in background thread."""
        
        self.progress_callback = progress_callback
        self.complete_callback = complete_callback
        self.is_analyzing = True
        self.start_time = time.time()
        
        # Run analysis in background thread
        analysis_thread = threading.Thread(
            target=self._perform_analysis,
            args=(urls, mode, max_videos, max_comments, 
                  include_transcript, include_comments, custom_requirements)
        )
        analysis_thread.daemon = True
        analysis_thread.start()
        
    def _perform_analysis(self, urls: List[str], mode: str, max_videos: int, 
                         max_comments: int, include_transcript: bool, 
                         include_comments: bool, custom_requirements: str):
        """Perform the actual analysis - FIXED VERSION."""
        try:
            print(f"\n{'='*60}")
            print(f"🔍 YOUTUBE ANALYSIS DEBUG START")
            print(f"{'='*60}")
            print(f"📊 Input parameters:")
            print(f"   URLs: {urls}")
            print(f"   Mode: {mode}")
            print(f"   Max videos: {max_videos}")
            print(f"   Max comments: {max_comments}")
            print(f"   Include transcript: {include_transcript}")
            print(f"   Include comments: {include_comments}")
            print(f"   Custom requirements: {bool(custom_requirements)}")
            print(f"   API keys available: {len(self.youtube_api_keys)}")
            print(f"   Collector initialized: {self.collector is not None}")

            # Initialize progress
            self._update_progress("Đang khởi tạo...", 0)
            
            # Initialize data container - FIX: Define all_data early
            all_data = {
                'channels': [],
                'video': [],
                'transcripts': [],
                'bình luận': [],
                'collection_date': datetime.now().isoformat()
            }
            
            # Separate URLs by type
            channel_urls = []
            video_urls = []
            
            for url in urls:
                print(f"📊 Processing URL: {url}")
                if mode == 'channel':
                    channel_urls.append(url)
                else:
                    video_urls.append(url)
            
            print(f"📊 URL separation:")
            print(f"   Channel URLs: {channel_urls}")
            print(f"   Video URLs: {video_urls}")
            
            # Process based on mode
            if mode == 'channel' and channel_urls:
                self._update_progress("Thu thập dữ liệu kênh...", 10)
                print(f"🎬 Starting channel data collection...")
                
                try:
                    collected_data = self.collector.collect_channel_data(
                        channel_urls=channel_urls,
                        max_videos_per_channel=max_videos,
                        max_comments_per_video=max_comments,
                        include_transcripts=include_transcript,
                        include_comments=include_comments
                    )
                    
                    # Update all_data with collected data
                    all_data.update(collected_data)
                    
                    print(f"✅ Channel collection completed:")
                    print(f"   Channels: {len(all_data.get('channels', []))}")
                    print(f"   Videos: {len(all_data.get('video', []))}")
                    print(f"   Comments: {len(all_data.get('bình luận', []))}")
                    print(f"   Transcripts: {len(all_data.get('transcripts', []))}")
                    
                except Exception as e:
                    print(f"❌ Error in channel collection: {e}")
                    logger.error(f"Error in channel collection: {e}")
                    # Continue with empty data
                    
            elif video_urls:
                self._update_progress("Thu thập dữ liệu video...", 10)
                print(f"📹 Starting video data collection...")
                
                try:
                    collected_data = self.collector.collect_video_data(
                        video_urls=video_urls,
                        max_comments_per_video=max_comments,
                        include_transcripts=include_transcript,
                        include_comments=include_comments
                    )
                    
                    # Update all_data with collected data
                    all_data.update(collected_data)
                    
                    print(f"✅ Video collection completed:")
                    print(f"   Videos: {len(all_data.get('video', []))}")
                    print(f"   Comments: {len(all_data.get('bình luận', []))}")
                    print(f"   Transcripts: {len(all_data.get('transcripts', []))}")
                    
                except Exception as e:
                    print(f"❌ Error in video collection: {e}")
                    logger.error(f"Error in video collection: {e}")
                    # Continue with empty data
                    
            else:
                print(f"❌ ERROR: No valid URLs to process!")
                print(f"   Mode: {mode}")
                print(f"   Channel URLs: {channel_urls}")
                print(f"   Video URLs: {video_urls}")
                
                # Return empty result
                analysis_result = {
                    'status': 'error',
                    'error': 'No valid URLs provided',
                    'data': all_data,
                    'viral_score': 0
                }
                self._on_complete(analysis_result)
                return
            
            # Update progress during collection
            total_items = len(all_data.get('video', []))
            print(f"📈 Processing {total_items} collected videos...")
            
            for i, video in enumerate(all_data.get('video', [])):
                progress = 10 + (70 * (i + 1) / max(total_items, 1))
                self._update_progress(
                    f"Đang xử lý video {i+1}/{total_items}...", 
                    progress,
                    videos_analyzed=i+1,
                    comments_collected=len(all_data.get('bình luận', [])),
                    transcripts_collected=len(all_data.get('transcripts', []))
                )
            
            # Analyze with AI if custom requirements provided
            self._update_progress("Đang phân tích với AI...", 85)
            
            if custom_requirements and self.openai_client:
                print(f"🤖 Starting AI analysis...")
                analysis_result = self.analyze_with_ai(all_data, custom_requirements)
                print(f"✅ AI analysis completed")
            else:
                print(f"📊 Starting structured analysis...")
                viral_score = self._calculate_viral_score(all_data)
                analysis_result = {
                    'status': 'success',
                    'analysis_type': 'structured',
                    'data': all_data,
                    'viral_score': viral_score
                }
                print(f"✅ Structured analysis completed, viral score: {viral_score}")
            
            print(f"🎯 Final analysis result:")
            print(f"   Status: {analysis_result.get('status')}")
            print(f"   Type: {analysis_result.get('analysis_type', 'N/A')}")
            print(f"   Viral score: {analysis_result.get('viral_score', 'N/A')}")
            print(f"   Data keys: {list(analysis_result.get('data', {}).keys())}")
            print(f"   Videos in result: {len(analysis_result.get('data', {}).get('video', []))}")
            
            # Complete
            self._update_progress("Hoàn tất!", 100)
            time.sleep(0.5)
            
            print(f"🔄 Calling completion callback...")
            self._on_complete(analysis_result)
            print(f"✅ Analysis process completed!")
            print(f"{'='*60}")
            
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            print(f"\n❌ CRITICAL ERROR in analysis:")
            print(f"   Error: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Make sure we have all_data defined even in error case
            if 'all_data' not in locals():
                all_data = {
                    'channels': [],
                    'video': [],
                    'transcripts': [],
                    'bình luận': [],
                    'collection_date': datetime.now().isoformat()
                }
            
            self._on_complete({
                'status': 'error',
                'error': str(e),
                'data': all_data
            })
        finally:
            self.is_analyzing = False
    
    def analyze_with_ai(self, youtube_data: Dict, custom_requirements: str) -> Dict:
        """Analyze YouTube data with AI based on custom requirements."""
        try:
            # Check if OpenAI client is available
            if not self.openai_client:
                logger.warning("OpenAI client not initialized")
                return {
                    'status': 'error',
                    'error': 'OpenAI API không được cấu hình',
                    'data': youtube_data,
                    'viral_score': self._calculate_viral_score(youtube_data)
                }
            
            # Prepare data summary for ChatGPT
            data_summary = self._prepare_data_summary(youtube_data)
            
            # Create dynamic prompt based on user requirements
            messages = [
                {
                    "role": "system",
                    "content": """Bạn là chuyên gia phân tích YouTube content với khả năng:
- Phân tích xu hướng và patterns trong content
- Hiểu tâm lý audience và engagement
- Đưa ra insights sâu sắc về chiến lược content
- Provide actionable recommendations

Hãy phân tích chi tiết theo yêu cầu của người dùng, sử dụng dữ liệu được cung cấp."""
                },
                {
                    "role": "user", 
                    "content": f"""
Dữ liệu YouTube đã thu thập:
{data_summary}

YÊU CẦU PHÂN TÍCH CỤ THỂ:
{custom_requirements}

Hãy phân tích chi tiết theo yêu cầu trên. Format câu trả lời rõ ràng với:
- Các insights chính
- Số liệu minh họa cụ thể
- Recommendations khả thi
- Kết luận tổng quan
"""
                }
            ]
            
            # Call ChatGPT
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",  # or "gpt-4" if available
                messages=messages,
                max_tokens=2500,
                temperature=0.7
            )
            
            # Get raw response
            ai_analysis = response.choices[0].message.content
            
            # Calculate viral score based on data
            viral_score = self._calculate_viral_score(youtube_data)
            
            # Return dynamic result
            return {
                'status': 'success',
                'analysis_type': 'dynamic',
                'user_requirements': custom_requirements,
                'ai_response': ai_analysis,
                'raw_data': youtube_data,
                'data': youtube_data,  # Also include in 'data' key for consistency
                'viral_score': viral_score,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"AI analysis error: {e}")
            return {
                'status': 'error',
                'error': f'Lỗi phân tích AI: {str(e)}',
                'analysis_type': 'dynamic',
                'data': youtube_data,
                'viral_score': self._calculate_viral_score(youtube_data)
            }
    
    def _prepare_data_summary(self, youtube_data: Dict) -> str:
        """Prepare concise data summary for AI analysis."""
        summary = []
        
        # Channel info
        channels = youtube_data.get('channels', [])
        if channels:
            summary.append("=== THÔNG TIN KÊNH ===")
            for channel in channels:
                summary.append(f"\nKênh: {channel.get('channel_title', 'N/A')}")
                summary.append(f"- Subscribers: {channel.get('subscriber_count', 0):,}")
                summary.append(f"- Tổng views: {channel.get('view_count', 0):,}")
                summary.append(f"- Tổng videos: {channel.get('video_count', 0):,}")
                summary.append(f"- Quốc gia: {channel.get('country', 'Unknown')}")
        
        # Videos analysis
        videos = youtube_data.get('video', [])
        if videos:
            summary.append(f"\n\n=== PHÂN TÍCH {len(videos)} VIDEO ===")
            
            # Overall stats
            total_views = sum(v.get('view_count', 0) for v in videos)
            total_likes = sum(v.get('like_count', 0) for v in videos)
            total_comments = sum(v.get('comment_count', 0) for v in videos)
            avg_views = total_views / len(videos) if videos else 0
            avg_engagement = sum(
                ((v.get('like_count', 0) + v.get('comment_count', 0)) / v.get('view_count', 1) * 100)
                for v in videos if v.get('view_count', 0) > 0
            ) / len(videos) if videos else 0
            
            summary.append(f"\nTổng quan:")
            summary.append(f"- Tổng views: {total_views:,}")
            summary.append(f"- Tổng likes: {total_likes:,}")
            summary.append(f"- Tổng comments: {total_comments:,}")
            summary.append(f"- Trung bình views/video: {avg_views:,.0f}")
            summary.append(f"- Engagement rate trung bình: {avg_engagement:.2f}%")
            
            # Top videos by views
            summary.append("\n\nTOP VIDEO THEO VIEWS:")
            sorted_videos = sorted(videos, key=lambda x: x.get('view_count', 0), reverse=True)
            
            for i, video in enumerate(sorted_videos[:5], 1):
                summary.append(f"\n{i}. {video.get('title', 'N/A')}")
                summary.append(f"   Views: {video.get('view_count', 0):,}")
                summary.append(f"   Likes: {video.get('like_count', 0):,}")
                summary.append(f"   Comments: {video.get('comment_count', 0):,}")
                
                # Engagement metrics
                views = video.get('view_count', 0)
                if views > 0:
                    engagement = ((video.get('like_count', 0) + video.get('comment_count', 0)) / views * 100)
                    like_ratio = (video.get('like_count', 0) / views * 100)
                    summary.append(f"   Engagement: {engagement:.2f}% | Like ratio: {like_ratio:.2f}%")
                
                # Duration
                duration = video.get('duration', 'N/A')
                summary.append(f"   Duration: {duration}")
        
        # Comments analysis
        comments = youtube_data.get('bình luận', [])
        if comments:
            summary.append(f"\n\n=== PHÂN TÍCH {len(comments)} COMMENTS ===")
            
            # Sentiment indicators
            positive_words = ['love', 'great', 'amazing', 'best', 'awesome', 'excellent']
            negative_words = ['hate', 'bad', 'worst', 'terrible', 'awful']
            
            positive_count = sum(1 for c in comments 
                               if any(word in c.get('text', '').lower() for word in positive_words))
            negative_count = sum(1 for c in comments 
                               if any(word in c.get('text', '').lower() for word in negative_words))
            
            summary.append(f"\nSentiment phân tích sơ bộ:")
            summary.append(f"- Positive comments: {positive_count} ({positive_count/len(comments)*100:.1f}%)")
            summary.append(f"- Negative comments: {negative_count} ({negative_count/len(comments)*100:.1f}%)")
            
            # Top comments
            summary.append("\n\nTOP COMMENTS (theo likes):")
            top_comments = sorted(comments, key=lambda x: x.get('like_count', 0), reverse=True)[:5]
            
            for i, comment in enumerate(top_comments, 1):
                comment_text = comment.get('text', '')[:100]
                likes = comment.get('like_count', 0)
                summary.append(f"\n{i}. \"{comment_text}...\"")
                summary.append(f"   Likes: {likes}")
        
        # Transcripts summary
        transcripts = youtube_data.get('transcripts', [])
        if transcripts:
            summary.append(f"\n\n=== TRANSCRIPTS: {len(transcripts)} videos có phụ đề ===")
            
            # Language distribution
            languages = {}
            for t in transcripts:
                lang = t.get('language', 'unknown')
                languages[lang] = languages.get(lang, 0) + 1
            
            summary.append("\nNgôn ngữ phụ đề:")
            for lang, count in languages.items():
                summary.append(f"- {lang}: {count} videos")
        
        return '\n'.join(summary)
    
    def _calculate_viral_score(self, data: Dict) -> float:
        """Calculate viral potential score based on various metrics."""
        score = 0
        weights = {
            'lượt xem': 0.3,
            'tương tác': 0.3,
            'growth': 0.2,
            'consistency': 0.1,
            'sentiment': 0.1
        }
        
        videos = data.get('video', [])
        if not videos:
            return 0
        
        # Views score (normalized by channel average)
        total_views = sum(v.get('view_count', 0) for v in videos)
        avg_views = total_views / len(videos) if videos else 0
        
        if avg_views > 1000000:
            views_score = 100
        elif avg_views > 500000:
            views_score = 80
        elif avg_views > 100000:
            views_score = 60
        elif avg_views > 50000:
            views_score = 40
        else:
            views_score = 20
        
        # Engagement score
        engagement_rates = []
        for video in videos:
            views = video.get('view_count', 0)
            if views > 0:
                engagement = ((video.get('like_count', 0) + video.get('comment_count', 0)) / views * 100)
                engagement_rates.append(engagement)
        
        avg_engagement = sum(engagement_rates) / len(engagement_rates) if engagement_rates else 0
        engagement_score = min(avg_engagement * 10, 100)  # Cap at 100
        
        # Growth score (compare recent vs older videos)
        if len(videos) >= 5:
            recent_videos = sorted(videos, key=lambda x: x.get('published_at', ''), reverse=True)[:5]
            older_videos = sorted(videos, key=lambda x: x.get('published_at', ''), reverse=True)[5:10]
            
            if older_videos:
                recent_avg = sum(v.get('view_count', 0) for v in recent_videos) / len(recent_videos)
                older_avg = sum(v.get('view_count', 0) for v in older_videos) / len(older_videos)
                
                if older_avg > 0:
                    growth_rate = ((recent_avg - older_avg) / older_avg) * 100
                    growth_score = min(max(growth_rate + 50, 0), 100)
                else:
                    growth_score = 50
            else:
                growth_score = 50
        else:
            growth_score = 50
        
        # Consistency score (regular uploads)
        consistency_score = 70  # Default
        
        # Sentiment score from comments
        comments = data.get('bình luận', [])
        if comments:
            positive_indicators = ['love', 'great', 'amazing', 'best', 'helpful', 'thank']
            positive_count = sum(1 for c in comments 
                               if any(indicator in c.get('text', '').lower() 
                                     for indicator in positive_indicators))
            sentiment_score = min((positive_count / len(comments)) * 200, 100)
        else:
            sentiment_score = 50
        
        # Calculate weighted score
        score = (
            weights['lượt xem'] * views_score +
            weights['tương tác'] * engagement_score +
            weights['growth'] * growth_score +
            weights['consistency'] * consistency_score +
            weights['sentiment'] * sentiment_score
        )
        
        return round(score, 1)
    
    def _update_progress(self, task: str, progress: float, **kwargs):
        """Update analysis progress."""
        if self.progress_callback:
            elapsed = time.time() - self.start_time if self.start_time else 0
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            
            progress_data = {
                'current_task': task,
                'progress': progress,
                'time_elapsed': f"{minutes}:{seconds:02d}",
                **kwargs
            }
            
            self.progress_callback(progress_data)
    
    def _on_complete(self, result: Dict):
        """Handle analysis completion."""
        self.is_analyzing = False
        
        print(f"\n🏁 COMPLETION CALLBACK TRIGGERED")
        print(f"📊 Result summary:")
        print(f"   Keys: {list(result.keys())}")
        print(f"   Status: {result.get('status')}")
        
        if result.get('status') == 'success':
            data = result.get('data', {})
            print(f"   ✅ Success! Data contains:")
            print(f"      Videos: {len(data.get('video', []))}")
            print(f"      Comments: {len(data.get('bình luận', []))}")
            print(f"      Transcripts: {len(data.get('transcripts', []))}")
            print(f"      Viral score: {result.get('viral_score')}")
            
            # Sample a video title to verify data quality
            videos = data.get('video', [])
            if videos:
                print(f"      Sample video: {videos[0].get('title', 'No title')[:50]}...")
        else:
            print(f"   ❌ Error: {result.get('error')}")
        
        if self.complete_callback:
            print(f"🔄 Executing complete_callback...")
            try:
                self.complete_callback(result)
                print(f"✅ Complete callback executed successfully")
            except Exception as e:
                print(f"❌ Error in complete callback: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"❌ WARNING: No complete_callback set!")
        
        print(f"🏁 Completion callback finished\n")
    
    def stop_analysis(self):
        """Stop ongoing analysis."""
        self.is_analyzing = False
        logger.info("Analysis stopped by user")