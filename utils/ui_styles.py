"""
UI styling utilities and theme management
"""

import customtkinter as ctk
from typing import Dict


class ThemeManager:
    """Manages application themes."""
    
    THEMES = {
        "light": {
            "bg_color": "#FFFFFF",
            "fg_color": "#F5F5F5",
            "text_color": "#2B2B2B",
            "button_color": "#2196F3"
        },
        "dark": {
            "bg_color": "#2B2B2B",
            "fg_color": "#3C3C3C",
            "text_color": "#FFFFFF",
            "button_color": "#1976D2"
        }
    }
    
    @classmethod
    def apply_theme(cls, theme_name: str) -> None:
        """Apply a theme to the application."""
        if theme_name in cls.THEMES:
            ctk.set_appearance_mode(theme_name)
    
    @classmethod
    def get_theme_colors(cls, theme_name: str) -> Dict[str, str]:
        """Get colors for a specific theme."""
        return cls.THEMES.get(theme_name, cls.THEMES["light"])


def apply_hover_effect(widget, hover_color: str = None) -> None:
    """Apply hover effect to a widget."""
    if hover_color is None:
        hover_color = "#E0E0E0"
        
    # Only apply to widgets that support fg_color
    if hasattr(widget, 'cget') and hasattr(widget, 'configure'):
        try:
            original_color = widget.cget("fg_color")
        except:
            return  # Widget doesn't support fg_color
        
        def on_enter(event):
            try:
                widget.configure(fg_color=hover_color)
            except:
                pass
        
        def on_leave(event):
            try:
                widget.configure(fg_color=original_color)
            except:
                pass
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)


def create_tooltip(widget, text: str) -> None:
    """Create a tooltip for a widget."""
    def show_tooltip(event):
        tooltip = ctk.CTkToplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        
        label = ctk.CTkLabel(
            tooltip,
            text=text,
            font=ctk.CTkFont(size=11),
            fg_color="#2B2B2B",
            text_color="#FFFFFF",
            corner_radius=5
        )
        label.pack(padx=5, pady=3)
        
        def hide_tooltip():
            tooltip.destroy()
        
        tooltip.after(3000, hide_tooltip)  # Auto-hide after 3 seconds
        widget.tooltip = tooltip  # Keep reference
    
    def hide_tooltip(event):
        if hasattr(widget, 'tooltip'):
            try:
                widget.tooltip.destroy()
            except:
                pass
    
    widget.bind("<Enter>", show_tooltip)
    widget.bind("<Leave>", hide_tooltip)