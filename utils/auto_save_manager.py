"""
Auto-save Manager for YouTube Analyzer Pro
Handles automatic saving and loading of analysis data
"""

import json
import os
import shutil
from datetime import datetime
from typing import Dict, Optional
import threading
import time


class AutoSaveManager:
    """Manages auto-saving and recovery of analysis data."""
    
    def __init__(self, save_dir: str = "cache", save_interval: int = 30):
        """
        Initialize auto-save manager.
        
        Args:
            save_dir: Directory to store saved data
            save_interval: Auto-save interval in seconds
        """
        self.save_dir = save_dir
        self.save_interval = save_interval
        self.main_save_file = os.path.join(save_dir, "last_analysis.json")
        self.backup_save_file = os.path.join(save_dir, "last_analysis_backup.json")
        self.temp_save_file = os.path.join(save_dir, "last_analysis_temp.json")
        
        # Create save directory
        os.makedirs(save_dir, exist_ok=True)
        
        # Auto-save thread
        self.auto_save_thread = None
        self.stop_auto_save = threading.Event()
        self.data_to_save = {}
        self.has_changes = False
        
    def start_auto_save(self):
        """Start auto-save background thread."""
        if self.auto_save_thread is None or not self.auto_save_thread.is_alive():
            self.stop_auto_save.clear()
            self.auto_save_thread = threading.Thread(target=self._auto_save_worker)
            self.auto_save_thread.daemon = True
            self.auto_save_thread.start()
            
    def stop_auto_save(self):
        """Stop auto-save background thread."""
        self.stop_auto_save.set()
        if self.auto_save_thread:
            self.auto_save_thread.join()
            
    def _auto_save_worker(self):
        """Background worker for auto-saving."""
        while not self.stop_auto_save.is_set():
            if self.has_changes:
                self.save_data(self.data_to_save)
                self.has_changes = False
            time.sleep(self.save_interval)
            
    def update_data(self, data: Dict):
        """Update data to be saved."""
        self.data_to_save = data
        self.has_changes = True
        
    def save_data(self, data: Dict) -> bool:
        """
        Save data with atomic write and backup.
        
        Args:
            data: Data to save
            
        Returns:
            Success status
        """
        try:
            # Add metadata
            save_data = {
                'data': data,
                'saved_at': datetime.now().isoformat(),
                'version': '1.0'
            }
            
            # Write to temp file first
            with open(self.temp_save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
                
            # Backup current file if exists
            if os.path.exists(self.main_save_file):
                shutil.copy2(self.main_save_file, self.backup_save_file)
                
            # Move temp to main (atomic operation)
            shutil.move(self.temp_save_file, self.main_save_file)
            
            # Clean up old backups (keep only last 5)
            self._cleanup_old_backups()
            
            return True
            
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
            
    def load_data(self) -> Optional[Dict]:
        """
        Load saved data with fallback to backup.
        
        Returns:
            Loaded data or None
        """
        try:
            # Try main file first
            if os.path.exists(self.main_save_file):
                with open(self.main_save_file, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)
                    return save_data.get('data', {})
                    
            # Fallback to backup
            elif os.path.exists(self.backup_save_file):
                print("Main save file not found, loading from backup")
                with open(self.backup_save_file, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)
                    return save_data.get('data', {})
                    
        except Exception as e:
            print(f"Error loading data: {e}")
            
        return None
        
    def get_save_info(self) -> Optional[Dict]:
        """Get information about saved data."""
        try:
            if os.path.exists(self.main_save_file):
                stat = os.stat(self.main_save_file)
                
                with open(self.main_save_file, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)
                    
                return {
                    'file_size': stat.st_size,
                    'modified_time': datetime.fromtimestamp(stat.st_mtime),
                    'saved_at': save_data.get('saved_at'),
                    'version': save_data.get('version'),
                    'has_data': bool(save_data.get('data'))
                }
        except:
            pass
            
        return None
        
    def clear_cache(self) -> bool:
        """Clear all cached data."""
        try:
            files_to_remove = [
                self.main_save_file,
                self.backup_save_file,
                self.temp_save_file
            ]
            
            for file_path in files_to_remove:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    
            return True
            
        except Exception as e:
            print(f"Error clearing cache: {e}")
            return False
            
    def _cleanup_old_backups(self):
        """Clean up old backup files."""
        try:
            # Get all backup files
            backup_pattern = "last_analysis_backup_"
            backups = []
            
            for file in os.listdir(self.save_dir):
                if file.startswith(backup_pattern):
                    file_path = os.path.join(self.save_dir, file)
                    backups.append((file_path, os.path.getmtime(file_path)))
                    
            # Sort by modification time
            backups.sort(key=lambda x: x[1], reverse=True)
            
            # Keep only 5 most recent
            for backup_path, _ in backups[5:]:
                os.remove(backup_path)
                
        except Exception as e:
            print(f"Error cleaning up backups: {e}")
            
    def create_timestamped_backup(self) -> Optional[str]:
        """Create a timestamped backup of current data."""
        try:
            if os.path.exists(self.main_save_file):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"last_analysis_backup_{timestamp}.json"
                backup_path = os.path.join(self.save_dir, backup_name)
                
                shutil.copy2(self.main_save_file, backup_path)
                return backup_path
                
        except Exception as e:
            print(f"Error creating timestamped backup: {e}")
            
        return None