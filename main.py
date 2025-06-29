"""
Main entry point for YouTube Analyzer Pro
"""

import customtkinter as ctk
import logging
import sys
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Main entry point."""
    # Add current directory to Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Setup folders
    folders = ["config", "output", "output/prompts", "output/exports", "cache"]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    
    # Create default config if needed
    config_file = "config/settings.json"
    if not os.path.exists(config_file):
        import json
        default_config = {
            "api_keys": {
                "youtube": [],
                "openai": [],
                "leonardo": "",
                "google_credentials": [],
                "google_tts": ""
            },
            "generation_settings": {
                "viral_threshold": 70,
                "quality": "Balanced",
                "enable_viral_scoring": True,
                "enable_retry": True,
                "auto_optimize": False
            }
        }
        with open(config_file, "w") as f:
            json.dump(default_config, f, indent=2)
    
    try:
        # Import app
        from app.main_window import YouTubeAnalyzerApp
        
        # Set appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Create and run app
        app = YouTubeAnalyzerApp()
        
        # Check API keys on startup
        from api_config import get_config_manager
        config_manager = get_config_manager()
        ready, message = config_manager.is_ready_for_analysis()
        
        if not ready:
            from tkinter import messagebox
            response = messagebox.askyesno(
                "API Configuration", 
                f"{message}\n\nWould you like to configure API keys now?"
            )
            if response:
                app.show_tab("settings")
        
        # Start the app
        app.mainloop()
        
    except Exception as e:
        logging.error(f"Application error: {e}")
        print(f"Failed to start application: {e}")
        
        # Show error dialog
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Startup Error",
                f"Failed to start YouTube Analyzer Pro:\n\n{str(e)}"
            )
        except:
            pass
        
        sys.exit(1)

if __name__ == "__main__":
    main()