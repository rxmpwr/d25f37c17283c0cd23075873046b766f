"""
Utils package with fallback support
"""

# Import với error handling
try:
    from .ui_components import (
        UIColors, UIFonts, create_action_button, 
        create_header_frame, create_metric_display,
        show_loading_dialog
    )
except ImportError:
    # Define minimal fallbacks
    class UIColors:
        PRIMARY = "#2196F3"
        SUCCESS = "#4CAF50"
        WARNING = "#FF9800"
        ERROR = "#F44336"
        GRAY = "#757575"
        WHITE = "#FFFFFF"
        TEXT_PRIMARY = "#2B2B2B"
        TEXT_SECONDARY = "#666666"
        BACKGROUND = "#F5F5F5"
        LIGHT_GRAY = "#E0E0E0"
        
    class UIFonts:
        @staticmethod
        def get_body():
            import customtkinter as ctk
            return ctk.CTkFont(size=13)
            
        @staticmethod
        def get_heading():
            import customtkinter as ctk
            return ctk.CTkFont(size=20, weight="bold")
            
        @staticmethod
        def get_subheading():
            import customtkinter as ctk
            return ctk.CTkFont(size=16, weight="bold")
            
        @staticmethod
        def get_button():
            import customtkinter as ctk
            return ctk.CTkFont(size=14, weight="bold")
            
        @staticmethod
        def get_small():
            import customtkinter as ctk
            return ctk.CTkFont(size=11)
            
        @staticmethod
        def get_code():
            import customtkinter as ctk
            return ctk.CTkFont(size=12, family="Consolas")
    
    def create_action_button(parent, text, command, button_type="primary", **kwargs):
        import customtkinter as ctk
        color_map = {
            "primary": UIColors.PRIMARY,
            "success": UIColors.SUCCESS,
            "warning": UIColors.WARNING,
            "error": UIColors.ERROR,
            "gray": UIColors.GRAY
        }
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            fg_color=color_map.get(button_type, UIColors.PRIMARY),
            **kwargs
        )
        
    def create_header_frame(parent, title, subtitle=""):
        import customtkinter as ctk
        frame = ctk.CTkFrame(parent, fg_color=UIColors.WHITE, corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(
            frame,
            text=title,
            font=UIFonts.get_heading(),
            text_color=UIColors.TEXT_PRIMARY
        )
        title_label.grid(row=0, column=0, pady=(15, 5))
        
        if subtitle:
            subtitle_label = ctk.CTkLabel(
                frame,
                text=subtitle,
                font=UIFonts.get_body(),
                text_color=UIColors.TEXT_SECONDARY
            )
            subtitle_label.grid(row=1, column=0, pady=(0, 15))
            
        return frame
        
    def create_metric_display(parent, metrics):
        import customtkinter as ctk
        frame = ctk.CTkFrame(parent, fg_color=UIColors.WHITE, corner_radius=10)
        
        for i, (label, value) in enumerate(metrics.items()):
            metric_frame = ctk.CTkFrame(frame, fg_color=UIColors.BACKGROUND)
            metric_frame.grid(row=0, column=i, padx=10, pady=10)
            
            value_label = ctk.CTkLabel(
                metric_frame,
                text=value,
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color=UIColors.PRIMARY
            )
            value_label.pack(pady=(10, 5))
            
            label_label = ctk.CTkLabel(
                metric_frame,
                text=label,
                font=UIFonts.get_small(),
                text_color=UIColors.TEXT_SECONDARY
            )
            label_label.pack(pady=(0, 10))
            
        return frame
        
    def show_loading_dialog(parent, title, message, task_func, completion_callback):
        """Simple loading dialog."""
        import threading
        # Execute task directly and call completion
        def run_task():
            try:
                result = task_func()
                parent.after(0, lambda: completion_callback(result))
            except Exception as e:
                from tkinter import messagebox
                parent.after(0, lambda: messagebox.showerror("Error", str(e)))
                
        thread = threading.Thread(target=run_task, daemon=True)
        thread.start()

# Export all
__all__ = [
    'UIColors', 'UIFonts', 'create_action_button',
    'create_header_frame', 'create_metric_display',
    'show_loading_dialog'
]