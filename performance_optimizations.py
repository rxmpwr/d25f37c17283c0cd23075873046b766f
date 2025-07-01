# performance_optimizations.py
"""
Performance optimization solutions for YouTube Analyzer Pro
Fixes UI freezing, slow loading, and memory issues
"""

import threading
import time
import queue
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
import customtkinter as ctk
from typing import Dict, List, Optional, Callable
import json
import weakref
from dataclasses import dataclass
import gc

# ========================================
# 1. ASYNC TASK MANAGER
# ========================================

class AsyncTaskManager:
    """Manages background tasks without blocking UI"""
    
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.active_tasks = {}
        self.task_counter = 0
        
    def run_async(self, func, callback=None, error_callback=None, *args, **kwargs):
        """Run function asynchronously with callbacks"""
        self.task_counter += 1
        task_id = f"task_{self.task_counter}"
        
        def task_wrapper():
            try:
                result = func(*args, **kwargs)
                if callback:
                    # Schedule callback on main thread
                    ctk.CTk().after(0, lambda: callback(result))
                return result
            except Exception as e:
                if error_callback:
                    ctk.CTk().after(0, lambda: error_callback(e))
                else:
                    print(f"Task error: {e}")
                    
        future = self.executor.submit(task_wrapper)
        self.active_tasks[task_id] = future
        return task_id
        
    def cancel_task(self, task_id):
        """Cancel a running task"""
        if task_id in self.active_tasks:
            self.active_tasks[task_id].cancel()
            del self.active_tasks[task_id]

# Global task manager instance
task_manager = AsyncTaskManager()

# ========================================
# 2. PROGRESSIVE DATA LOADER
# ========================================

@dataclass
class DataChunk:
    """Represents a chunk of data for progressive loading"""
    videos: List[Dict]
    comments: List[Dict] 
    transcripts: List[Dict]
    chunk_id: int
    total_chunks: int

class ProgressiveDataLoader:
    """Loads large datasets progressively to avoid UI freezing"""
    
    def __init__(self, chunk_size=50):
        self.chunk_size = chunk_size
        self.loaded_chunks = {}
        self.progress_callback = None
        
    def chunk_data(self, data: Dict) -> List[DataChunk]:
        """Split data into manageable chunks"""
        videos = data.get('video', [])
        comments = data.get('bình luận', [])
        transcripts = data.get('transcripts', [])
        
        total_items = max(len(videos), len(comments), len(transcripts))
        total_chunks = (total_items + self.chunk_size - 1) // self.chunk_size
        
        chunks = []
        for i in range(total_chunks):
            start_idx = i * self.chunk_size
            end_idx = start_idx + self.chunk_size
            
            chunk = DataChunk(
                videos=videos[start_idx:end_idx],
                comments=comments[start_idx:end_idx],
                transcripts=transcripts[start_idx:end_idx],
                chunk_id=i,
                total_chunks=total_chunks
            )
            chunks.append(chunk)
            
        return chunks
        
    def load_progressive(self, data: Dict, display_callback: Callable, 
                        progress_callback: Optional[Callable] = None):
        """Load data progressively with UI updates"""
        self.progress_callback = progress_callback
        chunks = self.chunk_data(data)
        
        def load_chunk(chunk_index):
            if chunk_index >= len(chunks):
                if progress_callback:
                    progress_callback(100, "Complete")
                return
                
            chunk = chunks[chunk_index]
            
            # Update progress
            progress = (chunk_index + 1) / len(chunks) * 100
            if progress_callback:
                progress_callback(progress, f"Loading chunk {chunk_index + 1}/{len(chunks)}")
            
            # Display chunk
            display_callback(chunk)
            
            # Schedule next chunk (prevents UI freeze)
            ctk.CTk().after(100, lambda: load_chunk(chunk_index + 1))
            
        # Start loading
        load_chunk(0)

# ========================================
# 3. OPTIMIZED UI COMPONENTS
# ========================================

class VirtualScrollableFrame(ctk.CTkScrollableFrame):
    """Virtual scrolling frame for large datasets"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.items = []
        self.visible_items = {}
        self.item_height = 100
        self.viewport_start = 0
        self.viewport_size = 10
        
    def set_items(self, items: List[Dict]):
        """Set items with virtual scrolling"""
        self.items = items
        self.update_viewport()
        
    def update_viewport(self):
        """Update visible items in viewport"""
        # Clear existing widgets
        for widget in self.visible_items.values():
            if hasattr(widget, 'destroy'):
                widget.destroy()
        self.visible_items.clear()
        
        # Calculate visible range
        start = max(0, self.viewport_start)
        end = min(len(self.items), start + self.viewport_size)
        
        # Create widgets for visible items only
        for i in range(start, end):
            item = self.items[i]
            widget = self.create_item_widget(item, i)
            self.visible_items[i] = widget
            
    def create_item_widget(self, item: Dict, index: int):
        """Create widget for individual item - override in subclass"""
        frame = ctk.CTkFrame(self)
        frame.grid(row=index, column=0, sticky="ew", pady=2)
        
        label = ctk.CTkLabel(frame, text=str(item))
        label.pack(pady=5)
        
        return frame

class OptimizedResultsPanel(ctk.CTkFrame):
    """Optimized results display with virtual scrolling and lazy loading"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.setup_ui()
        self.data_loader = ProgressiveDataLoader(chunk_size=20)
        self.displayed_chunks = 0
        
    def setup_ui(self):
        """Setup optimized UI structure"""
        # Progress indicator
        self.progress_frame = ctk.CTkFrame(self)
        self.progress_frame.pack(fill="x", padx=10, pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(side="left", fill="x", expand=True, padx=5)
        
        self.status_label = ctk.CTkLabel(self.progress_frame, text="Sẵn sàng")
        self.status_label.pack(side="right", padx=5)
        
        # Scrollable content area with virtual scrolling
        self.content_area = VirtualScrollableFrame(self)
        self.content_area.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Load more button
        self.load_more_btn = ctk.CTkButton(
            self, text="Load More Results", command=self.load_more_data
        )
        self.load_more_btn.pack(pady=5)
        self.load_more_btn.pack_forget()  # Initially hidden
        
    def display_results_optimized(self, data: Dict):
        """Display results with progressive loading"""
        self.clear_display()
        self.displayed_chunks = 0
        
        # Start progressive loading
        self.data_loader.load_progressive(
            data, 
            self.display_chunk,
            self.update_progress
        )
        
    def display_chunk(self, chunk: DataChunk):
        """Display a single chunk of data"""
        # Create summary widget for this chunk
        chunk_frame = ctk.CTkFrame(self.content_area)
        chunk_frame.grid(row=self.displayed_chunks, column=0, sticky="ew", pady=2)
        
        # Videos summary
        if chunk.videos:
            videos_label = ctk.CTkLabel(
                chunk_frame, 
                text=f"📹 Videos {chunk.chunk_id * self.data_loader.chunk_size + 1}-"
                     f"{chunk.chunk_id * self.data_loader.chunk_size + len(chunk.videos)}"
            )
            videos_label.pack(anchor="w", padx=10, pady=2)
            
            # Show only summary for performance
            for i, video in enumerate(chunk.videos[:3]):  # Show max 3 per chunk
                video_summary = self.create_video_summary(video)
                video_summary.pack(fill="x", padx=20, pady=1)
                
        self.displayed_chunks += 1
        
        # Show load more button if there are more chunks
        if chunk.chunk_id < chunk.total_chunks - 1:
            self.load_more_btn.pack(pady=5)
        else:
            self.load_more_btn.pack_forget()
            
    def create_video_summary(self, video: Dict) -> ctk.CTkFrame:
        """Create lightweight video summary widget"""
        frame = ctk.CTkFrame(self.content_area)
        
        # Title (truncated)
        title = video.get('title', 'No title')[:60] + "..." if len(video.get('title', '')) > 60 else video.get('title', 'No title')
        title_label = ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(weight="bold"))
        title_label.pack(anchor="w", padx=5, pady=2)
        
        # Stats in one line
        views = video.get('view_count', 0)
        likes = video.get('like_count', 0)
        comments = video.get('comment_count', 0)
        stats_text = f"👁️ {views:,} | 👍 {likes:,} | 💬 {comments:,}"
        
        stats_label = ctk.CTkLabel(frame, text=stats_text, text_color="gray")
        stats_label.pack(anchor="w", padx=5)
        
        return frame
        
    def update_progress(self, progress: float, status: str):
        """Update loading progress"""
        self.progress_bar.set(progress / 100)
        self.status_label.configure(text=status)
        
        if progress >= 100:
            # Hide progress bar when complete
            self.progress_frame.pack_forget()
            
    def load_more_data(self):
        """Load more data chunks"""
        # This would trigger loading next batch
        pass
        
    def clear_display(self):
        """Clear all displayed content efficiently"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
        self.progress_frame.pack(fill="x", padx=10, pady=5)
        self.progress_bar.set(0)

# ========================================
# 4. MEMORY EFFICIENT DATA PROCESSOR
# ========================================

class MemoryEfficientProcessor:
    """Process large datasets without memory overflow"""
    
    def __init__(self):
        self.cache = {}
        self.cache_size_limit = 100  # MB
        
    @lru_cache(maxsize=32)
    def process_text_analysis(self, text_hash: str, text: str) -> Dict:
        """Cache expensive text analysis operations"""
        # Simulate expensive text processing
        words = text.lower().split()
        return {
            'word_count': len(words),
            'keywords': self.extract_keywords(words),
            'sentiment': self.analyze_sentiment_fast(words)
        }
        
    def extract_keywords(self, words: List[str]) -> List[str]:
        """Fast keyword extraction"""
        # Simple keyword extraction (can be improved)
        keyword_candidates = [w for w in words if len(w) > 4]
        return list(set(keyword_candidates))[:10]  # Top 10 unique keywords
        
    def analyze_sentiment_fast(self, words: List[str]) -> str:
        """Fast sentiment analysis"""
        positive_words = set(['good', 'great', 'amazing', 'love', 'excellent', 'awesome'])
        negative_words = set(['bad', 'terrible', 'hate', 'awful', 'boring', 'worst'])
        
        pos_count = sum(1 for w in words if w in positive_words)
        neg_count = sum(1 for w in words if w in negative_words)
        
        if pos_count > neg_count:
            return 'positive'
        elif neg_count > pos_count:
            return 'negative'
        return 'neutral'
        
    def process_batch(self, items: List[Dict], processor_func: Callable) -> List[Dict]:
        """Process items in batches to prevent memory overflow"""
        batch_size = 50
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_results = [processor_func(item) for item in batch]
            results.extend(batch_results)
            
            # Force garbage collection after each batch
            gc.collect()
            
        return results

# ========================================
# 5. OPTIMIZED YOUTUBE INTEGRATION
# ========================================

class OptimizedYouTubeAnalysisManager:
    """Optimized version of YouTube analysis with better performance"""
    
    def __init__(self, youtube_api_keys: List[str], openai_api_keys: List[str] = None):
        self.youtube_api_keys = youtube_api_keys
        self.openai_api_keys = openai_api_keys or []
        self.task_manager = AsyncTaskManager()
        self.data_processor = MemoryEfficientProcessor()
        self.progress_queue = queue.Queue()
        
    def start_analysis_optimized(self, urls: List[str], mode: str = 'channel', 
                                max_videos: int = 20, max_comments: int = 50,
                                progress_callback: Optional[Callable] = None,
                                complete_callback: Optional[Callable] = None):
        """Start optimized analysis with better progress tracking"""
        
        def analysis_task():
            try:
                # Phase 1: Data Collection (40% of progress)
                self.update_progress(5, "Initializing data collection...", progress_callback)
                
                collected_data = self.collect_data_batch(urls, mode, max_videos, max_comments, progress_callback)
                
                # Phase 2: Processing (40% of progress) 
                self.update_progress(45, "Processing collected data...", progress_callback)
                
                processed_data = self.process_data_efficient(collected_data, progress_callback)
                
                # Phase 3: Analysis (20% of progress)
                self.update_progress(85, "Running AI analysis...", progress_callback)
                
                final_result = self.run_analysis_efficient(processed_data, progress_callback)
                
                self.update_progress(100, "Analysis complete!", progress_callback)
                
                return final_result
                
            except Exception as e:
                if progress_callback:
                    progress_callback({'error': str(e)})
                raise
                
        # Run analysis asynchronously
        task_id = self.task_manager.run_async(
            analysis_task,
            callback=complete_callback,
            error_callback=lambda e: print(f"Analysis error: {e}")
        )
        
        return task_id
        
    def collect_data_batch(self, urls: List[str], mode: str, max_videos: int, 
                          max_comments: int, progress_callback: Optional[Callable]) -> Dict:
        """Collect data in batches to avoid API rate limits"""
        all_data = {'video': [], 'bình luận': [], 'transcripts': []}
        
        total_urls = len(urls)
        for i, url in enumerate(urls):
            # Update progress for each URL
            url_progress = 5 + (35 * (i + 1) / total_urls)  # 5-40% range
            self.update_progress(url_progress, f"Processing URL {i+1}/{total_urls}...", progress_callback)
            
            # Collect data for this URL (implement actual collection logic)
            url_data = self.collect_single_url_data(url, mode, max_videos, max_comments)
            
            # Merge data
            all_data['video'].extend(url_data.get('video', []))
            all_data['bình luận'].extend(url_data.get('bình luận', []))
            all_data['transcripts'].extend(url_data.get('transcripts', []))
            
            # Small delay to avoid rate limiting
            time.sleep(0.1)
            
        return all_data
        
    def collect_single_url_data(self, url: str, mode: str, max_videos: int, max_comments: int) -> Dict:
        """Collect data from single URL - implement actual logic here"""
        # Placeholder - implement actual YouTube API calls
        return {
            'video': [{'title': f'Video from {url}', 'view_count': 1000}],
            'bình luận': [{'text': 'Sample comment', 'like_count': 5}],
            'transcripts': [{'full_text': 'Sample transcript', 'video_id': '123'}]
        }
        
    def process_data_efficient(self, data: Dict, progress_callback: Optional[Callable]) -> Dict:
        """Process data efficiently in batches"""
        videos = data.get('video', [])
        comments = data.get('bình luận', [])
        transcripts = data.get('transcripts', [])
        
        # Process videos in batches
        self.update_progress(50, "Processing videos...", progress_callback)
        processed_videos = self.data_processor.process_batch(videos, self.process_single_video)
        
        # Process comments in batches  
        self.update_progress(65, "Processing comments...", progress_callback)
        processed_comments = self.data_processor.process_batch(comments, self.process_single_comment)
        
        # Process transcripts in batches
        self.update_progress(80, "Processing transcripts...", progress_callback)
        processed_transcripts = self.data_processor.process_batch(transcripts, self.process_single_transcript)
        
        return {
            'video': processed_videos,
            'bình luận': processed_comments, 
            'transcripts': processed_transcripts,
            'summary': self.generate_summary(processed_videos, processed_comments, processed_transcripts)
        }
        
    def process_single_video(self, video: Dict) -> Dict:
        """Process single video efficiently"""
        # Add computed fields
        video['engagement_rate'] = self.calculate_engagement_rate(video)
        video['viral_score'] = self.calculate_viral_score_fast(video)
        return video
        
    def process_single_comment(self, comment: Dict) -> Dict:
        """Process single comment efficiently"""
        text = comment.get('text', '')
        text_hash = str(hash(text))
        
        # Use cached analysis if available
        analysis = self.data_processor.process_text_analysis(text_hash, text)
        comment.update(analysis)
        return comment
        
    def process_single_transcript(self, transcript: Dict) -> Dict:
        """Process single transcript efficiently"""
        text = transcript.get('full_text', '')
        if text:
            text_hash = str(hash(text))
            analysis = self.data_processor.process_text_analysis(text_hash, text)
            transcript.update(analysis)
        return transcript
        
    def calculate_engagement_rate(self, video: Dict) -> float:
        """Fast engagement rate calculation"""
        views = video.get('view_count', 0)
        likes = video.get('like_count', 0)
        comments = video.get('comment_count', 0)
        
        if views > 0:
            return ((likes + comments) / views) * 100
        return 0
        
    def calculate_viral_score_fast(self, video: Dict) -> float:
        """Fast viral score calculation"""
        engagement = self.calculate_engagement_rate(video)
        views = video.get('view_count', 0)
        
        # Simple viral score formula
        score = 0
        if views > 1000000:
            score += 40
        elif views > 100000:
            score += 25
        elif views > 10000:
            score += 15
            
        score += min(engagement * 10, 40)  # Engagement can contribute max 40 points
        
        return min(score, 100)
        
    def generate_summary(self, videos: List[Dict], comments: List[Dict], transcripts: List[Dict]) -> Dict:
        """Generate summary statistics efficiently"""
        return {
            'total_videos': len(videos),
            'total_comments': len(comments),
            'total_transcripts': len(transcripts),
            'avg_views': sum(v.get('view_count', 0) for v in videos) / len(videos) if videos else 0,
            'avg_engagement_rate': sum(v.get('engagement_rate', 0) for v in videos) / len(videos) if videos else 0
        }
        
    def run_analysis_efficient(self, data: Dict, progress_callback: Optional[Callable]) -> Dict:
        """Run final analysis efficiently"""
        self.update_progress(90, "Generating insights...", progress_callback)
        
        # Generate insights efficiently
        insights = {
            'viral_potential': self.calculate_overall_viral_potential(data),
            'top_themes': self.extract_top_themes(data),
            'audience_sentiment': self.analyze_overall_sentiment(data)
        }
        
        return {
            'status': 'success',
            'data': data,
            'insights': insights,
            'timestamp': time.time()
        }
        
    def calculate_overall_viral_potential(self, data: Dict) -> float:
        """Calculate overall viral potential efficiently"""
        videos = data.get('video', [])
        if not videos:
            return 0
            
        avg_viral_score = sum(v.get('viral_score', 0) for v in videos) / len(videos)
        return avg_viral_score
        
    def extract_top_themes(self, data: Dict) -> List[str]:
        """Extract top themes efficiently"""
        # Simplified theme extraction
        transcripts = data.get('transcripts', [])
        all_keywords = []
        
        for transcript in transcripts:
            keywords = transcript.get('keywords', [])
            all_keywords.extend(keywords)
            
        # Count and return top themes
        from collections import Counter
        theme_counts = Counter(all_keywords)
        return [theme for theme, count in theme_counts.most_common(5)]
        
    def analyze_overall_sentiment(self, data: Dict) -> str:
        """Analyze overall sentiment efficiently"""
        comments = data.get('bình luận', [])
        if not comments:
            return 'neutral'
            
        sentiments = [c.get('sentiment', 'neutral') for c in comments]
        positive_count = sentiments.count('positive')
        negative_count = sentiments.count('negative')
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        return 'neutral'
        
    def update_progress(self, progress: float, status: str, callback: Optional[Callable]):
        """Update progress safely"""
        if callback:
            try:
                callback({
                    'progress': progress,
                    'status': status,
                    'timestamp': time.time()
                })
            except Exception as e:
                print(f"Progress callback error: {e}")

# ========================================
# 6. USAGE EXAMPLE
# ========================================

def optimize_existing_analysis_tab():
    """Example of how to optimize existing analysis tab"""
    
    class OptimizedAnalysisTabManager:
        def __init__(self, parent_frame):
            self.parent_frame = parent_frame
            self.results_panel = OptimizedResultsPanel(parent_frame)
            self.youtube_manager = None
            
        def start_optimized_analysis(self, config: Dict):
            """Start analysis with optimizations"""
            # Create optimized YouTube manager
            self.youtube_manager = OptimizedYouTubeAnalysisManager(
                config.get('youtube_keys', []),
                config.get('openai_keys', [])
            )
            
            # Start analysis with progress tracking
            task_id = self.youtube_manager.start_analysis_optimized(
                urls=config['urls'],
                mode=config['mode'],
                max_videos=config['max_videos'],
                max_comments=config['max_comments'],
                progress_callback=self.on_progress_update,
                complete_callback=self.on_analysis_complete
            )
            
            return task_id
            
        def on_progress_update(self, progress_data: Dict):
            """Handle progress updates on main thread"""
            def update_ui():
                progress = progress_data.get('progress', 0)
                status = progress_data.get('status', 'Đang xử lý...')
                
                # Update progress in UI
                self.results_panel.update_progress(progress, status)
                
            # Schedule UI update on main thread
            self.parent_frame.after(0, update_ui)
            
        def on_analysis_complete(self, result_data: Dict):
            """Handle analysis completion"""
            def update_ui():
                if result_data.get('status') == 'success':
                    # Display results with progressive loading
                    self.results_panel.display_results_optimized(result_data['data'])
                else:
                    # Handle error
                    error_msg = result_data.get('error', 'Unknown error')
                    print(f"Analysis failed: {error_msg}")
                    
            # Schedule UI update on main thread  
            self.parent_frame.after(0, update_ui)

# Example usage
if __name__ == "__main__":
    print("🚀 Performance Optimization Solutions Ready!")
    print("Key improvements:")
    print("1. Async task management - prevents UI freezing")
    print("2. Progressive data loading - handles large datasets") 
    print("3. Virtual scrolling - efficient UI rendering")
    print("4. Memory efficient processing - prevents crashes")
    print("5. Optimized YouTube analysis - faster processing")
    print("6. Better progress tracking - improved UX")