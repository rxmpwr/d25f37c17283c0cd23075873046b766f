# Root __init__.py (if needed)
"""
YouTube Analyzer Pro - Complete YouTube Content Analysis Tool

A comprehensive tool for analyzing YouTube content, generating insights,
and creating viral content based on data-driven analysis.
"""

__version__ = "1.0.0"
__description__ = "YouTube Analyzer Pro - Complete YouTube Content Analysis Tool"
__author__ = "YouTube Analyzer Pro Team"
__license__ = "MIT"

# Main application entry point
def main():
    """Main entry point for the application."""
    try:
        from app import YouTubeAnalyzerApp
        import customtkinter as ctk
        
        # Set appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Create and run app
        app = YouTubeAnalyzerApp()
        app.mainloop()
        
    except ImportError as e:
        print(f"Error: Required dependencies not found: {e}")
        print("Please install required packages and try again.")
    except Exception as e:
        print(f"Error starting application: {e}")

if __name__ == "__main__":
    main()