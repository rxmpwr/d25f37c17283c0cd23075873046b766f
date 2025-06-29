"""
Prompt tab manager with fallback support
"""

try:
    # Try to import enhanced version
    from .prompt.prompt_tab_base import EnhancedPromptTabManager as PromptTabManager
except ImportError:
    # Fallback to simple version
    from .prompt_tab_simple import PromptTabManager

__all__ = ['PromptTabManager']