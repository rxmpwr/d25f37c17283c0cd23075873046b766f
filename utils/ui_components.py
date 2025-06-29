"""
Core UI components and widgets
"""

import customtkinter as ctk
from typing import Dict, List, Optional, Tuple, Callable
from tkinter import messagebox


class UIColors:
    """Color constants for consistent theming."""
    PRIMARY = "#2196F3"
    PRIMARY_HOVER = "#1976D2"
    SUCCESS = "#4CAF50"
    SUCCESS_HOVER = "#45A049"
    WARNING = "#FF9800"
    WARNING_HOVER = "#FB8C00"
    ERROR = "#F44336"
    ERROR_HOVER = "#E53935"
    GRAY = "#757575"
    GRAY_HOVER = "#616161"
    LIGHT_GRAY = "#E0E0E0"
    BACKGROUND = "#F5F5F5"
    WHITE = "#FFFFFF"
    TEXT_PRIMARY = "#2B2B2B"
    TEXT_SECONDARY = "#666666"


class UIFonts:
    """Font factory functions for consistent typography."""
    
    @staticmethod
    def get_title():
        """Get title font."""
        return ctk.CTkFont(size=32, weight="bold")
    
    @staticmethod
    def get_heading():
        """Get heading font."""
        return ctk.CTkFont(size=20, weight="bold")
    
    @staticmethod
    def get_subheading():
        """Get subheading font."""
        return ctk.CTkFont(size=16, weight="bold")
    
    @staticmethod
    def get_body():
        """Get body font."""
        return ctk.CTkFont(size=13)
    
    @staticmethod
    def get_small():
        """Get small font."""
        return ctk.CTkFont(size=11)
    
    @staticmethod
    def get_button():
        """Get button font."""
        return ctk.CTkFont(size=14, weight="bold")
    
    @staticmethod
    def get_code():
        """Get code font."""
        return ctk.CTkFont(size=12, family="Consolas")


def create_header_frame(parent: ctk.CTk, title: str, subtitle: str = "") -> ctk.CTkFrame:
    """Create a standardized header frame."""
    header_frame = ctk.CTkFrame(parent, fg_color=UIColors.WHITE, corner_radius=10)
    header_frame.grid_columnconfigure(0, weight=1)
    
    # Title
    title_label = ctk.CTkLabel(
        header_frame,
        text=title,
        font=UIFonts.get_heading(),
        text_color=UIColors.TEXT_PRIMARY
    )
    title_label.grid(row=0, column=0, pady=(15, 5 if subtitle else 15))
    
    # Subtitle if provided
    if subtitle:
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text=subtitle,
            font=UIFonts.get_body(),
            text_color=UIColors.TEXT_SECONDARY
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 15))
    
    return header_frame


def create_action_button(parent: ctk.CTk, text: str, command: Callable, 
                        button_type: str = "primary", width: int = 150, 
                        height: int = 40, **kwargs) -> ctk.CTkButton:
    """Create a standardized action button."""
    color_map = {
        "primary": (UIColors.PRIMARY, UIColors.PRIMARY_HOVER),
        "success": (UIColors.SUCCESS, UIColors.SUCCESS_HOVER),
        "warning": (UIColors.WARNING, UIColors.WARNING_HOVER),
        "error": (UIColors.ERROR, UIColors.ERROR_HOVER),
        "gray": (UIColors.GRAY, UIColors.GRAY_HOVER)
    }
    
    fg_color, hover_color = color_map.get(button_type, color_map["primary"])
    
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        fg_color=fg_color,
        hover_color=hover_color,
        width=width,
        height=height,
        font=UIFonts.get_button(),
        **kwargs
    )


def create_info_card(parent: ctk.CTk, title: str, content: str, 
                    card_type: str = "info") -> ctk.CTkFrame:
    """Create an information card with title and content."""
    color_map = {
        "info": "#E3F2FD",
        "success": "#E8F5E8",
        "warning": "#FFF3E0",
        "error": "#FFEBEE"
    }
    
    bg_color = color_map.get(card_type, color_map["info"])
    
    card = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=10)
    
    # Title
    title_label = ctk.CTkLabel(
        card,
        text=title,
        font=UIFonts.get_subheading(),
        text_color=UIColors.TEXT_PRIMARY
    )
    title_label.pack(pady=(15, 5), padx=15, anchor="w")
    
    # Content
    content_label = ctk.CTkLabel(
        card,
        text=content,
        font=UIFonts.get_body(),
        text_color=UIColors.TEXT_SECONDARY,
        wraplength=500,
        justify="left"
    )
    content_label.pack(pady=(0, 15), padx=15, anchor="w")
    
    return card


def create_metric_display(parent: ctk.CTk, metrics: Dict[str, str]) -> ctk.CTkFrame:
    """Create a metrics display frame."""
    metrics_frame = ctk.CTkFrame(parent, fg_color=UIColors.WHITE, corner_radius=10)
    
    # Grid layout for metrics
    cols = min(len(metrics), 4)  # Max 4 columns
    rows = (len(metrics) + cols - 1) // cols
    
    for i, (label, value) in enumerate(metrics.items()):
        row = i // cols
        col = i % cols
        
        metric_container = ctk.CTkFrame(metrics_frame, fg_color=UIColors.BACKGROUND, corner_radius=8)
        metric_container.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        
        # Value
        value_label = ctk.CTkLabel(
            metric_container,
            text=value,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=UIColors.PRIMARY
        )
        value_label.pack(pady=(10, 5))
        
        # Label
        label_label = ctk.CTkLabel(
            metric_container,
            text=label,
            font=UIFonts.get_small(),
            text_color=UIColors.TEXT_SECONDARY
        )
        label_label.pack(pady=(0, 10))
        
        # Configure column weight
        metrics_frame.grid_columnconfigure(col, weight=1)
    
    return metrics_frame


def show_loading_dialog(parent: ctk.CTk, title: str, message: str, 
                       task_func: Callable, completion_callback: Callable = None,
                       *args, **kwargs):
    """Show a loading dialog while executing a task in background."""
    import threading
    
    dialog = ctk.CTkToplevel(parent)
    dialog.title(title)
    dialog.geometry("400x200")
    dialog.transient(parent)
    dialog.grab_set()
    
    # Center the dialog
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - 200
    y = (dialog.winfo_screenheight() // 2) - 100
    dialog.geometry(f"400x200+{x}+{y}")
    
    # Message label
    message_label = ctk.CTkLabel(
        dialog,
        text=message,
        font=UIFonts.get_body()
    )
    message_label.pack(pady=(30, 20))
    
    # Progress bar
    progress_bar = ctk.CTkProgressBar(dialog, width=300)
    progress_bar.pack(pady=10)
    progress_bar.set(0)
    progress_bar.start()
    
    def run_task():
        try:
            result = task_func(*args, **kwargs)
            dialog.after(0, lambda: _handle_completion(dialog, result, completion_callback))
        except Exception as e:
            dialog.after(0, lambda: _handle_error(dialog, str(e)))
    
    def _handle_completion(dialog, result, callback):
        dialog.destroy()
        if callback:
            callback(result)
    
    def _handle_error(dialog, error_msg):
        dialog.destroy()
        messagebox.showerror("Error", f"Task failed: {error_msg}")
    
    # Start task in background
    thread = threading.Thread(target=run_task, daemon=True)
    thread.start()
    
    return dialog