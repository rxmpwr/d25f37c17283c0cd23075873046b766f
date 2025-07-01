# utils/memory_manager.py

import gc
import time
import threading
from performance_config import perf_config, MemoryOptimizer

class AutoMemoryManager:
    """Automatic memory management for the application"""
    
    def __init__(self):
        self.cleanup_thread = None
        self.running = False
        
    def start_auto_cleanup(self):
        """Start automatic memory cleanup"""
        if self.running:
            return
            
        self.running = True
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.cleanup_thread.start()
        
    def stop_auto_cleanup(self):
        """Stop automatic memory cleanup"""
        self.running = False
        
    def _cleanup_loop(self):
        """Main cleanup loop"""
        cleanup_interval = perf_config.get('memory_cleanup_interval', 300)  # 5 minutes
        
        while self.running:
            time.sleep(cleanup_interval)
            
            if MemoryOptimizer.check_memory_threshold():
                print("🧹 Running automatic memory cleanup...")
                gc.collect()
                
                memory_after = MemoryOptimizer.get_memory_usage_mb()
                print(f"💾 Memory usage after cleanup: {memory_after:.1f} MB")

# Global memory manager
auto_memory_manager = AutoMemoryManager()

# Start on import
auto_memory_manager.start_auto_cleanup()