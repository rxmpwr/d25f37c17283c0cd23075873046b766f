# utils/performance_dashboard.py

import customtkinter as ctk
from performance_config import perf_monitor, perf_config

class PerformanceDashboard(ctk.CTkToplevel):
    """Real-time performance monitoring dashboard"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Performance Monitor")
        self.geometry("400x300")
        
        self.setup_ui()
        self.update_dashboard()
        
    def setup_ui(self):
        """Setup dashboard UI"""
        # Memory usage
        self.memory_label = ctk.CTkLabel(self, text="Memory: -- MB")
        self.memory_label.pack(pady=10)
        
        # Performance metrics
        self.metrics_text = ctk.CTkTextbox(self, height=200)
        self.metrics_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Performance presets
        preset_frame = ctk.CTkFrame(self)
        preset_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(preset_frame, text="Performance Preset:").pack(side="left")
        
        self.preset_var = ctk.StringVar(value="balanced")
        preset_menu = ctk.CTkOptionMenu(
            preset_frame,
            variable=self.preset_var,
            values=["conservative", "balanced", "aggressive"],
            command=self.apply_preset
        )
        preset_menu.pack(side="right")
        
    def update_dashboard(self):
        """Update dashboard with current metrics"""
        from performance_config import MemoryOptimizer
        
        # Update memory
        memory_usage = MemoryOptimizer.get_memory_usage_mb()
        self.memory_label.configure(text=f"Memory: {memory_usage:.1f} MB")
        
        # Update metrics
        report = perf_monitor.get_performance_report()
        
        metrics_text = "📊 PERFORMANCE METRICS\n\n"
        for metric, data in report.items():
            metrics_text += f"{metric}:\n"
            metrics_text += f"  Average: {data['average']:.2f}s\n"
            metrics_text += f"  Max: {data['max']:.2f}s\n"
            metrics_text += f"  Count: {data['count']}\n\n"
        
        self.metrics_text.delete("1.0", "end")
        self.metrics_text.insert("1.0", metrics_text)
        
        # Schedule next update
        self.after(5000, self.update_dashboard)  # Update every 5 seconds
        
    def apply_preset(self, preset_name):
        """Apply performance preset"""
        from performance_config import apply_performance_preset
        apply_performance_preset(preset_name)
        
        # Show confirmation
        ctk.CTkLabel(self, text=f"✅ Applied {preset_name} preset", 
                    text_color="green").pack(pady=5)