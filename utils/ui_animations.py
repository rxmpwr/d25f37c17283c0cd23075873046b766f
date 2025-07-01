"""
UI animation utilities
"""

import customtkinter as ctk
from typing import Optional


class AnimationHelper:
    """Helper class for UI animations."""
    
    @staticmethod
    def fade_in(widget, duration: int = 500, 
                start_alpha: float = 0.0, end_alpha: float = 1.0) -> None:
        """Fade in animation for widget."""
        steps = 20
        step_duration = duration // steps
        alpha_step = (end_alpha - start_alpha) / steps
        
        def animate_step(current_step: int = 0):
            if current_step <= steps:
                # Note: CustomTkinter doesn't support true transparency
                # This is a placeholder for the animation concept
                widget.configure(state="normal")
                
                if current_step < steps:
                    widget.after(step_duration, lambda: animate_step(current_step + 1))
        
        animate_step()
    
    @staticmethod
    def slide_in(widget, direction: str = "left", 
                 duration: int = 500, distance: int = 100) -> None:
        """Slide in animation for widget."""
        # Get current position
        widget.update_idletasks()
        start_x = widget.winfo_x()
        start_y = widget.winfo_y()
        
        # Calculate starting position based on direction
        if direction == "left":
            widget.place(x=start_x - distance, y=start_y)
            target_x = start_x
            target_y = start_y
        elif direction == "right":
            widget.place(x=start_x + distance, y=start_y)
            target_x = start_x
            target_y = start_y
        elif direction == "top":
            widget.place(x=start_x, y=start_y - distance)
            target_x = start_x
            target_y = start_y
        else:  # bottom
            widget.place(x=start_x, y=start_y + distance)
            target_x = start_x
            target_y = start_y
        
        # Animate
        steps = 20
        step_duration = duration // steps
        x_step = (target_x - widget.winfo_x()) / steps
        y_step = (target_y - widget.winfo_y()) / steps
        
        def animate_step(current_step: int = 0):
            if current_step <= steps:
                current_x = widget.winfo_x() + x_step
                current_y = widget.winfo_y() + y_step
                widget.place(x=int(current_x), y=int(current_y))
                
                if current_step < steps:
                    widget.after(step_duration, lambda: animate_step(current_step + 1))
        
        animate_step()
    
    @staticmethod
    def pulse_button(button: ctk.CTkButton, color: str = None, 
                     duration: int = 200, pulses: int = 1) -> None:
        """Pulse animation for button."""
        if color is None:
            color = "#1976D2"
            
        original_color = button.cget("fg_color")
        
        def pulse_cycle(remaining_pulses: int):
            if remaining_pulses > 0:
                button.configure(fg_color=color)
                button.after(duration // 2, lambda: button.configure(fg_color=original_color))
                button.after(duration, lambda: pulse_cycle(remaining_pulses - 1))
        
        pulse_cycle(pulses)
    
    @staticmethod
    def shake(widget, distance: int = 10, 
              duration: int = 500, shakes: int = 3) -> None:
        """Shake animation for widget (e.g., on error)."""
        widget.update_idletasks()
        original_x = widget.winfo_x()
        
        shake_duration = duration // (shakes * 4)
        
        def shake_cycle(remaining_shakes: int, direction: int = 1):
            if remaining_shakes > 0:
                # Move right
                widget.place(x=original_x + (distance * direction))
                widget.after(shake_duration, lambda: widget.place(x=original_x))
                
                # Schedule next shake
                widget.after(shake_duration * 2, 
                           lambda: shake_cycle(remaining_shakes - 1, -direction))
            else:
                # Ensure widget returns to original position
                widget.place(x=original_x)
        
        shake_cycle(shakes)