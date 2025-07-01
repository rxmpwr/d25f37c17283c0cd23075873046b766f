# performance_config.py
"""
Complete Performance Configuration and Optimization System for YouTube Analyzer Pro
This file contains all performance optimizations and should be placed in the project root
"""

import json
import os
import time
import threading
import gc
import queue
from typing import Dict, Any, Callable, List, Optional
from collections import deque
from functools import lru_cache, wraps
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

# ========================================
# CONFIGURATION MANAGEMENT
# ========================================

class PerformanceConfig:
    """Performance configuration manager with adaptive settings"""
    
    # Default performance settings
    DEFAULT_SETTINGS = {
        # Data Processing Limits
        "max_videos_per_batch": 20,
        "max_comments_per_video": 50,
        "max_transcript_length": 10000,  # characters
        "batch_processing_size": 100,
        "chunk_size_for_display": 50,
        "max_prompt_templates": 6,
        
        # UI Performance
        "progress_update_throttle": 0.1,  # seconds
        "max_display_items": 100,
        "lazy_load_threshold": 1000,  # items
        "ui_update_frequency": 10,  # fps
        
        # Memory Management  
        "enable_garbage_collection": True,
        "memory_cleanup_interval": 300,  # seconds
        "max_memory_usage_mb": 2048,
        "cache_size_limit": 128,
        
        # API Optimization
        "api_request_delay": 0.5,  # seconds between requests
        "max_concurrent_requests": 3,
        "retry_attempts": 3,
        "timeout_seconds": 30,
        
        # Analysis Optimization
        "enable_smart_caching": True,
        "parallel_processing": True,
        "max_worker_threads": 4,
        "enable_progress_streaming": True,
        
        # Export Optimization
        "max_export_items": 10000,
        "compress_exports": True,
        "stream_large_exports": True
    }
    
    def __init__(self, config_file: str = "config/performance.json"):
        self.config_file = config_file
        self.settings = self.load_settings()
        
    def load_settings(self) -> Dict[str, Any]:
        """Load performance settings from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_settings = json.load(f)
                
                # Merge with defaults
                settings = self.DEFAULT_SETTINGS.copy()
                settings.update(loaded_settings)
                return settings
                
            except Exception as e:
                logger.error(f"Error loading performance config: {e}")
                
        return self.DEFAULT_SETTINGS.copy()
        
    def save_settings(self) -> bool:
        """Save current settings to file"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            
            return True
            
        except Exception as e:
            logger.error(f"Error saving performance config: {e}")
            return False
            
    def get(self, key: str, default=None):
        """Get setting value"""
        return self.settings.get(key, default)
        
    def set(self, key: str, value: Any):
        """Set setting value"""
        self.settings[key] = value
        
    def update_settings(self, new_settings: Dict[str, Any]):
        """Update multiple settings"""
        self.settings.update(new_settings)
        
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = self.DEFAULT_SETTINGS.copy()
        
    def get_optimized_settings_for_dataset_size(self, estimated_videos: int) -> Dict[str, Any]:
        """Get optimized settings based on expected dataset size"""
        if estimated_videos < 50:
            # Small dataset - can handle more
            return {
                "max_videos_per_batch": 50,
                "max_comments_per_video": 100,
                "chunk_size_for_display": 100,
                "max_display_items": 200
            }
        elif estimated_videos < 200:
            # Medium dataset - balanced approach
            return {
                "max_videos_per_batch": 25,
                "max_comments_per_video": 75,
                "chunk_size_for_display": 75,
                "max_display_items": 150
            }
        else:
            # Large dataset - conservative approach
            return {
                "max_videos_per_batch": 10,
                "max_comments_per_video": 30,
                "chunk_size_for_display": 50,
                "max_display_items": 100
            }

# ========================================
# PERFORMANCE MONITORING
# ========================================

class PerformanceMonitor:
    """Monitor application performance and suggest optimizations"""
    
    def __init__(self):
        self.metrics = {
            'api_response_times': deque(maxlen=100),
            'ui_update_times': deque(maxlen=100),
            'memory_usage': deque(maxlen=50),
            'processing_times': deque(maxlen=50)
        }
        self.monitoring_active = False
        self.monitor_thread = None
        
    def start_monitoring(self):
        """Start performance monitoring"""
        if self.monitoring_active:
            return
            
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("Performance monitoring started")
        
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        logger.info("Performance monitoring stopped")
            
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Monitor memory usage
                memory_usage = self._get_memory_usage()
                if memory_usage > 0:
                    self.metrics['memory_usage'].append(memory_usage)
                
                # Check if performance adjustments needed
                self._check_performance_thresholds()
                
                time.sleep(5)  # Monitor every 5 seconds
                
            except Exception as e:
                logger.error(f"Performance monitoring error: {e}")
                
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            import psutil
            import os
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / 1024 / 1024
        except ImportError:
            return 0
        except Exception:
            return 0
            
    def _check_performance_thresholds(self):
        """Check if performance thresholds are exceeded"""
        # Memory threshold check
        if self.metrics['memory_usage']:
            avg_memory = sum(self.metrics['memory_usage']) / len(self.metrics['memory_usage'])
            max_memory = perf_config.get('max_memory_usage_mb', 2048)
            
            if avg_memory > max_memory * 0.8:  # 80% threshold
                self._suggest_memory_optimization()
                
        # API response time check
        if self.metrics['api_response_times']:
            avg_response_time = sum(self.metrics['api_response_times']) / len(self.metrics['api_response_times'])
            
            if avg_response_time > 5.0:  # 5 second threshold
                self._suggest_api_optimization()
                
    def _suggest_memory_optimization(self):
        """Suggest memory optimizations"""
        logger.warning("High memory usage detected")
        logger.info("Suggestions: Reduce batch size, enable GC, limit concurrent operations")
        
    def _suggest_api_optimization(self):
        """Suggest API optimizations"""
        logger.warning("Slow API responses detected")
        logger.info("Suggestions: Increase delays, reduce concurrent requests, check connection")
        
    def record_api_time(self, response_time: float):
        """Record API response time"""
        self.metrics['api_response_times'].append(response_time)
        
    def record_ui_update_time(self, update_time: float):
        """Record UI update time"""
        self.metrics['ui_update_times'].append(update_time)
        
    def record_processing_time(self, processing_time: float):
        """Record data processing time"""
        self.metrics['processing_times'].append(processing_time)
        
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance report"""
        report = {}
        
        for metric_name, values in self.metrics.items():
            if values:
                report[metric_name] = {
                    'average': sum(values) / len(values),
                    'max': max(values),
                    'min': min(values),
                    'count': len(values)
                }
            else:
                report[metric_name] = {'average': 0, 'max': 0, 'min': 0, 'count': 0}
                
        return report

# ========================================
# PERFORMANCE DECORATORS
# ========================================

def monitor_performance(metric_name: str = None):
    """Decorator to monitor function performance"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                elapsed_time = time.time() - start_time
                
                if metric_name == 'api':
                    perf_monitor.record_api_time(elapsed_time)
                elif metric_name == 'ui':
                    perf_monitor.record_ui_update_time(elapsed_time)
                elif metric_name == 'processing':
                    perf_monitor.record_processing_time(elapsed_time)
                    
        return wrapper
    return decorator

def throttle_calls(min_interval: float = 0.1):
    """Decorator to throttle function calls"""
    def decorator(func: Callable):
        last_called = [0]
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            if now - last_called[0] >= min_interval:
                last_called[0] = now
                return func(*args, **kwargs)
                
        return wrapper
    return decorator

# ========================================
# MEMORY MANAGEMENT
# ========================================

class MemoryOptimizer:
    """Memory optimization utilities"""
    
    @staticmethod
    def cleanup_large_variables(*variables):
        """Cleanup large variables and force garbage collection"""
        for var in variables:
            if var is None:
                continue
            try:
                if hasattr(var, 'clear'):
                    var.clear()
                elif hasattr(var, '__dict__'):
                    var.__dict__.clear()
            except Exception:
                pass
                
        gc.collect()
        
    @staticmethod
    def limit_data_size(data: dict, max_items_per_category: int = None) -> dict:
        """Limit data size to prevent memory issues"""
        if max_items_per_category is None:
            max_items_per_category = perf_config.get('max_display_items', 100)
            
        if not isinstance(data, dict):
            return data
            
        limited_data = {}
        
        for key, value in data.items():
            if isinstance(value, list) and len(value) > max_items_per_category:
                # Keep most important items (sorted by views if applicable)
                if key == 'video' and value:
                    # Sort by view count and keep top items
                    try:
                        sorted_videos = sorted(value, key=lambda x: x.get('view_count', 0), reverse=True)
                        limited_data[key] = sorted_videos[:max_items_per_category]
                    except Exception:
                        limited_data[key] = value[:max_items_per_category]
                else:
                    # Keep first N items
                    limited_data[key] = value[:max_items_per_category]
            else:
                limited_data[key] = value
                
        return limited_data
        
    @staticmethod
    def get_memory_usage_mb() -> float:
        """Get current memory usage in MB"""
        try:
            import psutil
            import os
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / 1024 / 1024
        except ImportError:
            return 0
        except Exception:
            return 0
            
    @staticmethod
    def check_memory_threshold() -> bool:
        """Check if memory usage is approaching threshold"""
        current_usage = MemoryOptimizer.get_memory_usage_mb()
        max_usage = perf_config.get('max_memory_usage_mb', 2048)
        
        return current_usage > (max_usage * 0.8)  # 80% threshold

# ========================================
# UI OPTIMIZATION
# ========================================

class UIOptimizer:
    """UI optimization utilities"""
    
    @staticmethod
    @throttle_calls(0.1)  # Max 10 updates per second
    def update_progress_throttled(progress_func, *args, **kwargs):
        """Update progress with throttling"""
        try:
            return progress_func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Progress update error: {e}")
            
    @staticmethod
    def optimize_text_widget(text_widget, content: str):
        """Optimize text widget for large content"""
        max_length = perf_config.get('max_transcript_length', 10000)
        
        if len(content) > max_length:
            # Truncate content
            truncated_content = content[:max_length]
            truncated_content += f"\n\n... (Content truncated. Total length: {len(content):,} characters)"
            content = truncated_content
            
        try:
            text_widget.delete("1.0", "end")
            text_widget.insert("1.0", content)
        except Exception as e:
            logger.error(f"Text widget optimization error: {e}")

# ========================================
# ASYNC TASK MANAGEMENT
# ========================================

class AsyncTaskManager:
    """Manages background tasks without blocking UI"""
    
    def __init__(self):
        self.executor = None
        self.active_tasks = {}
        self.task_counter = 0
        
    def _get_executor(self):
        """Get or create thread pool executor"""
        if self.executor is None:
            from concurrent.futures import ThreadPoolExecutor
            max_workers = perf_config.get('max_worker_threads', 4)
            self.executor = ThreadPoolExecutor(max_workers=max_workers)
        return self.executor
        
    def run_async(self, func, callback=None, error_callback=None, *args, **kwargs):
        """Run function asynchronously with callbacks"""
        self.task_counter += 1
        task_id = f"task_{self.task_counter}"
        
        def task_wrapper():
            try:
                result = func(*args, **kwargs)
                if callback:
                    # Schedule callback on main thread
                    try:
                        import customtkinter as ctk
                        ctk.CTk().after(0, lambda: callback(result))
                    except Exception:
                        callback(result)
                return result
            except Exception as e:
                logger.error(f"Async task error: {e}")
                if error_callback:
                    try:
                        import customtkinter as ctk
                        ctk.CTk().after(0, lambda: error_callback(e))
                    except Exception:
                        error_callback(e)
                    
        executor = self._get_executor()
        future = executor.submit(task_wrapper)
        self.active_tasks[task_id] = future
        return task_id
        
    def cancel_task(self, task_id):
        """Cancel a running task"""
        if task_id in self.active_tasks:
            self.active_tasks[task_id].cancel()
            del self.active_tasks[task_id]
            
    def cleanup(self):
        """Cleanup task manager"""
        if self.executor:
            self.executor.shutdown(wait=False)
            self.executor = None

# ========================================
# APPLICATION INTEGRATION
# ========================================

def apply_performance_optimizations_to_app(app_instance):
    """Apply performance optimizations to existing app instance"""
    try:
        # Start performance monitoring
        perf_monitor.start_monitoring()
        
        # Apply memory optimization
        if hasattr(app_instance, 'analysis_data'):
            app_instance.analysis_data = MemoryOptimizer.limit_data_size(
                getattr(app_instance, 'analysis_data', {})
            )
        
        logger.info("Performance optimizations applied successfully")
        
    except Exception as e:
        logger.error(f"Error applying optimizations: {e}")
    
def get_performance_recommendations(analysis_data: dict) -> List[str]:
    """Get performance recommendations based on data size"""
    recommendations = []
    
    try:
        videos_count = len(analysis_data.get('video', []))
        comments_count = len(analysis_data.get('bình luận', []))
        
        if videos_count > 500:
            recommendations.append("🔄 Large dataset detected - Consider processing in smaller batches")
            recommendations.append("💾 Enable data export for offline analysis")
            
        if comments_count > 10000:
            recommendations.append("💬 High comment volume - Limit comment processing per video")
            recommendations.append("📊 Focus on most engaged comments for analysis")
            
        memory_usage = MemoryOptimizer.get_memory_usage_mb()
        if memory_usage > 1000:  # 1GB
            recommendations.append("🧠 High memory usage - Consider restarting application")
            recommendations.append("🗑️ Clear cache and temporary data")
            
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        
    return recommendations

# ========================================
# CONFIGURATION PRESETS
# ========================================

PERFORMANCE_PRESETS = {
    "conservative": {
        "max_videos_per_batch": 10,
        "max_comments_per_video": 25,
        "chunk_size_for_display": 25,
        "max_display_items": 50,
        "api_request_delay": 1.0,
        "max_concurrent_requests": 2,
        "max_prompt_templates": 3
    },
    
    "balanced": {
        "max_videos_per_batch": 25,
        "max_comments_per_video": 50,
        "chunk_size_for_display": 50,
        "max_display_items": 100,
        "api_request_delay": 0.5,
        "max_concurrent_requests": 3,
        "max_prompt_templates": 6
    },
    
    "aggressive": {
        "max_videos_per_batch": 50,
        "max_comments_per_video": 100,
        "chunk_size_for_display": 100,
        "max_display_items": 200,
        "api_request_delay": 0.3,
        "max_concurrent_requests": 5,
        "max_prompt_templates": 8
    }
}

def apply_performance_preset(preset_name: str):
    """Apply a performance preset"""
    if preset_name in PERFORMANCE_PRESETS:
        perf_config.update_settings(PERFORMANCE_PRESETS[preset_name])
        perf_config.save_settings()
        logger.info(f"Applied '{preset_name}' performance preset")
    else:
        logger.error(f"Unknown preset: {preset_name}")

# ========================================
# STARTUP OPTIMIZATION
# ========================================

def optimize_app_startup():
    """Optimize application startup performance"""
    try:
        # Set optimal performance settings based on system
        memory_usage = MemoryOptimizer.get_memory_usage_mb()
        
        if memory_usage > 0:
            if memory_usage < 500:  # Low memory system
                apply_performance_preset("conservative")
            elif memory_usage < 1500:  # Medium memory system
                apply_performance_preset("balanced")
            else:  # High memory system
                apply_performance_preset("aggressive")
        else:
            # Default to balanced if can't detect memory
            apply_performance_preset("balanced")
            
        logger.info("Application startup optimized based on system resources")
        
    except Exception as e:
        logger.error(f"Error optimizing startup: {e}")

# ========================================
# GLOBAL INSTANCES
# ========================================

# Create global instances
perf_config = PerformanceConfig()
perf_monitor = PerformanceMonitor()
task_manager = AsyncTaskManager()

# ========================================
# CLEANUP ON EXIT
# ========================================

import atexit

def cleanup_on_exit():
    """Cleanup performance monitoring on application exit"""
    try:
        perf_monitor.stop_monitoring()
        task_manager.cleanup()
        logger.info("Performance system cleanup completed")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")

# Register cleanup function
atexit.register(cleanup_on_exit)

# ========================================
# UTILITY FUNCTIONS
# ========================================

def show_loading_dialog(parent, title, message, task_func, callback):
    """Show loading dialog while running task (placeholder for actual implementation)"""
    try:
        # This would be implemented with actual UI framework
        # For now, just run the task
        result = task_func()
        if callback:
            callback(result)
    except Exception as e:
        logger.error(f"Loading dialog error: {e}")
        if callback:
            callback(None)

def get_system_info() -> Dict[str, Any]:
    """Get system information for optimization decisions"""
    info = {
        'memory_mb': MemoryOptimizer.get_memory_usage_mb(),
        'performance_preset': 'balanced',
        'optimizations_enabled': True
    }
    
    try:
        import psutil
        import platform
        
        info.update({
            'cpu_count': psutil.cpu_count(),
            'total_memory_gb': psutil.virtual_memory().total / (1024**3),
            'platform': platform.system(),
            'python_version': platform.python_version()
        })
    except ImportError:
        pass
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        
    return info

# ========================================
# EXPORT FOR INTEGRATION
# ========================================

__all__ = [
    'PerformanceConfig',
    'PerformanceMonitor', 
    'MemoryOptimizer',
    'UIOptimizer',
    'AsyncTaskManager',
    'monitor_performance',
    'throttle_calls',
    'apply_performance_optimizations_to_app',
    'get_performance_recommendations',
    'apply_performance_preset',
    'optimize_app_startup',
    'show_loading_dialog',
    'get_system_info',
    'perf_config',
    'perf_monitor',
    'task_manager'
]

# ========================================
# INITIALIZATION
# ========================================

def initialize_performance_system():
    """Initialize the performance optimization system"""
    try:
        # Auto-optimize on import
        optimize_app_startup()
        
        # Start monitoring
        perf_monitor.start_monitoring()
        
        logger.info("🚀 Performance optimization system initialized")
        logger.info(f"📊 Current settings: {perf_config.get('max_videos_per_batch')} videos/batch")
        logger.info(f"💾 Memory limit: {perf_config.get('max_memory_usage_mb')} MB")
        
        # Log system info
        sys_info = get_system_info()
        logger.info(f"🖥️ System: {sys_info.get('memory_mb', 0):.1f} MB used")
        
    except Exception as e:
        logger.error(f"Error initializing performance system: {e}")

# Auto-initialize when module is imported
initialize_performance_system()

if __name__ == "__main__":
    print("🔧 Performance Configuration Module")
    print("=" * 50)
    print("Available presets:", list(PERFORMANCE_PRESETS.keys()))
    
    sys_info = get_system_info()
    print(f"Current memory usage: {sys_info.get('memory_mb', 0):.1f} MB")
    print(f"Performance preset: {sys_info.get('performance_preset', 'unknown')}")
    
    print("\n📊 Performance Metrics:")
    report = perf_monitor.get_performance_report()
    for metric, data in report.items():
        if data['count'] > 0:
            print(f"  {metric}: {data['average']:.2f}s avg ({data['count']} samples)")
    
    print("\n✅ Performance optimization system ready!")