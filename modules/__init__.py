
"""
Core modules for YouTube data collection and integration
"""

# Import core modules
try:
    from .youtube_collector import (
        YouTubeCollector, extract_urls_from_text, validate_youtube_url,
        YouTubeDataProcessor
    )
    
    from .youtube_integration import (
        YouTubeAnalysisManager, YouTubeDataProcessor as IntegrationDataProcessor
    )
    
    COLLECTOR_AVAILABLE = True
    INTEGRATION_AVAILABLE = True
    
except ImportError as e:
    print(f"Warning: YouTube modules could not be imported: {e}")
    COLLECTOR_AVAILABLE = False
    INTEGRATION_AVAILABLE = False

if COLLECTOR_AVAILABLE and INTEGRATION_AVAILABLE:
    __all__ = [
        'YouTubeCollector',
        'YouTubeAnalysisManager', 
        'extract_urls_from_text',
        'validate_youtube_url'
    ]
else:
    __all__ = []