"""
Analysis tab manager for displaying YouTube analysis results
"""

import customtkinter as ctk
import time
from typing import Callable, Dict
from tkinter import messagebox, filedialog
import json
from datetime import datetime


class AnalysisTabManager:
    """Manages the analysis results tab."""
    
    def __init__(self, parent, export_json_callback: Callable, 
                 export_csv_callback: Callable, proceed_callback: Callable):
        self.parent = parent
        self.export_json_callback = export_json_callback
        self.export_csv_callback = export_csv_callback
        self.proceed_callback = proceed_callback
        
        # Store data for re-analysis
        self.current_data = None
        self.additional_requirements = []
        
        # Create the tab content
        self.setup_tab()
        
    def setup_tab(self):
        """Setup analysis tab content."""
        # Analysis results tab
        self.tab_frame = ctk.CTkFrame(self.parent, fg_color="#F5F5F5")
        self.tab_frame.grid_rowconfigure(2, weight=1)
        self.tab_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        header_frame = ctk.CTkFrame(self.tab_frame, fg_color="white", corner_radius=10)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            header_frame,
            text="📊 Analysis Results",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=15)
        
        # Progress section
        self.progress_frame = ctk.CTkFrame(self.tab_frame, fg_color="white", corner_radius=10)
        self.progress_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Ready to analyze...",
            font=ctk.CTkFont(size=14)
        )
        self.progress_label.pack(pady=(15, 5))
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, width=600)
        self.progress_bar.pack(pady=(5, 15))
        self.progress_bar.set(0)
        
        # Results display
        results_container = ctk.CTkFrame(self.tab_frame, fg_color="white", corner_radius=10)
        results_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        results_container.grid_rowconfigure(0, weight=1)
        results_container.grid_columnconfigure(0, weight=1)
        
        # Results text box with scrollbar
        self.results_text = ctk.CTkTextbox(
            results_container,
            font=ctk.CTkFont(size=14, family="Times New Roman"),
            wrap="word"
        )
        self.results_text.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Additional Analysis Section
        self.setup_additional_analysis_section()
        
        # Action buttons
        self.setup_action_buttons()

    def setup_additional_analysis_section(self):
        """Setup section for additional analysis requirements."""
        # Additional requirements frame
        additional_frame = ctk.CTkFrame(self.tab_frame, fg_color="white", corner_radius=10)
        additional_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Title
        ctk.CTkLabel(
            additional_frame,
            text="🔍 Phân tích thêm với yêu cầu bổ sung",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10), padx=20, anchor="w")
        
        # Input frame
        input_frame = ctk.CTkFrame(additional_frame, fg_color="#F5F5F5", corner_radius=8)
        input_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Requirements text box
        ctk.CTkLabel(
            input_frame,
            text="Nhập yêu cầu phân tích thêm:",
            font=ctk.CTkFont(size=13)
        ).pack(pady=(10, 5), padx=15, anchor="w")
        
        self.requirements_text = ctk.CTkTextbox(
            input_frame,
            height=80,
            font=ctk.CTkFont(size=13)
        )
        self.requirements_text.pack(fill="x", padx=15, pady=(0, 10))
        
        # Analyze button
        self.reanalyze_btn = ctk.CTkButton(
            additional_frame,
            text="🔄 Phân tích lại với yêu cầu mới",
            command=self.reanalyze_with_requirements,
            width=250,
            height=40,
            state="disabled"
        )
        self.reanalyze_btn.pack(pady=(0, 15))

    def setup_action_buttons(self):
        """Setup action buttons."""
        action_frame = ctk.CTkFrame(self.tab_frame, fg_color="transparent")
        action_frame.pack(pady=(0, 20))
        
        # Export buttons
        self.export_json_btn = ctk.CTkButton(
            action_frame,
            text="📥 Export JSON",
            command=self.export_json_callback,
            width=150,
            state="disabled"
        )
        self.export_json_btn.pack(side="left", padx=5)
        
        self.export_csv_btn = ctk.CTkButton(
            action_frame,
            text="📊 Export CSV",
            command=self.export_csv_callback,
            width=150,
            state="disabled"
        )
        self.export_csv_btn.pack(side="left", padx=5)
        
        # Import button
        self.import_btn = ctk.CTkButton(
            action_frame,
            text="📤 Import Analysis",
            command=self.import_analysis,
            width=150,
            fg_color="#FF9800",
            hover_color="#F57C00"
        )
        self.import_btn.pack(side="left", padx=5)
        
        self.proceed_btn = ctk.CTkButton(
            action_frame,
            text="➡️ Create Prompts",
            command=self.proceed_callback,
            width=150,
            state="disabled"
        )
        self.proceed_btn.pack(side="left", padx=5)

    def update_progress(self, progress_data: Dict):
        """Update analysis progress."""
        status = progress_data.get('status', '')
        message = progress_data.get('message', '')
        progress = progress_data.get('progress', 0)
        
        # Update progress label
        self.progress_label.configure(text=message)
        
        # Update progress bar
        self.progress_bar.set(progress / 100)
        
        # Add status to results text
        if status == 'collecting':
            current_item = progress_data.get('current_channel') or progress_data.get('current_video', '')
            if current_item:
                self.results_text.insert("end", f"Processing: {current_item}\n")
                self.results_text.see("end")

    def on_complete(self, result_data: Dict):
        """Handle analysis completion."""
        status = result_data.get('status', '')
        
        if status == 'success':
            # Store current data
            self.current_data = result_data.get('data', {})
            
            # Update progress
            self.progress_bar.set(1.0)
            self.progress_label.configure(text="Phân tích hoàn thành!")
            
            # Format and display results
            self.display_analysis_results(self.current_data)
            
            # Enable action buttons
            self.export_json_btn.configure(state="normal")
            self.export_csv_btn.configure(state="normal")
            self.proceed_btn.configure(state="normal", text="➡️ Tạo AI Prompts")
            self.reanalyze_btn.configure(state="normal")
            
            # Show success message
            viral_score = result_data.get('viral_score', 0)
            message = f"Phân tích hoàn thành!\n\nĐiểm viral potential: {viral_score:.1f}/100"
            messagebox.showinfo("Thành công", message)
            
        elif status == 'error':
            # Show error
            self.progress_label.configure(text="Phân tích thất bại!")
            error_msg = result_data.get('error', 'Lỗi không xác định')
            self.results_text.insert("end", f"\n\n❌ LỖI: {error_msg}\n")
            messagebox.showerror("Lỗi phân tích", result_data.get('message', 'Phân tích thất bại!'))

    def display_analysis_results(self, data: Dict):
        """Display analysis results with additional requirements if any."""
        try:
            from analysis_results import format_analysis_results
            
            # Add additional requirements to data if any
            if self.additional_requirements:
                data['additional_requirements'] = self.additional_requirements
            
            formatted_results = format_analysis_results(data)
            
            # Add additional analysis section if requirements exist
            if self.additional_requirements:
                formatted_results += self.format_additional_analysis()
            
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", formatted_results)
            
        except ImportError:
            # Fallback to basic display
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", "Analysis completed!\n\n")
            self.results_text.insert("end", json.dumps(data, indent=2))

    def format_additional_analysis(self) -> str:
        """Format additional analysis based on user requirements."""
        if not self.additional_requirements:
            return ""
            
        result = f"""
📋 PHÂN TÍCH BỔ SUNG THEO YÊU CẦU:
{'='*80}

"""
        for i, req in enumerate(self.additional_requirements, 1):
            result += f"\n🔍 Yêu cầu {i}: {req['requirement']}\n"
            result += f"📊 Kết quả phân tích:\n{req['analysis']}\n"
            result += "-" * 50 + "\n"
            
        return result

    def reanalyze_with_requirements(self):
        """Re-analyze data with additional requirements."""
        requirements = self.requirements_text.get("1.0", "end-1c").strip()
        
        if not requirements:
            messagebox.showwarning("Thiếu yêu cầu", "Vui lòng nhập yêu cầu phân tích thêm!")
            return
            
        if not self.current_data:
            messagebox.showerror("Không có dữ liệu", "Không có dữ liệu để phân tích lại!")
            return
            
        # Simulate additional analysis
        self.progress_label.configure(text="Đang phân tích với yêu cầu mới...")
        self.progress_bar.set(0.5)
        
        # Add to requirements list
        additional_analysis = {
            'requirement': requirements,
            'timestamp': datetime.now().isoformat(),
            'analysis': self.generate_additional_analysis(requirements)
        }
        
        self.additional_requirements.append(additional_analysis)
        
        # Update display
        self.display_analysis_results(self.current_data)
        
        # Clear input
        self.requirements_text.delete("1.0", "end")
        
        # Complete
        self.progress_bar.set(1.0)
        self.progress_label.configure(text="Phân tích bổ sung hoàn thành!")
        
        messagebox.showinfo("Hoàn thành", "Đã phân tích thêm theo yêu cầu mới!")

    def generate_additional_analysis(self, requirements: str) -> str:
        """Generate additional analysis based on requirements."""
        # This is a placeholder - in real implementation, this would call AI
        # or perform actual analysis based on the requirements
        
        analysis_templates = {
            'viral': """
- Xu hướng viral: Content về tâm lý và relationships đang có engagement cao nhất
- Yếu tố viral: Tiêu đề có số (5 signs, 3 ways) + emotional triggers
- Timing: Post vào 14:00-16:00 và 20:00-22:00 cho engagement tốt nhất
- Format: Video 8-12 phút có retention rate cao nhất""",
            
            'competitor': """
- So với competitors: Channel này có engagement rate cao hơn trung bình ngành 2.5x
- Điểm mạnh: Content quality và consistency đều nhất
- Cơ hội: Chưa tận dụng YouTube Shorts và live streaming
- Đề xuất: Tạo Shorts từ highlights của long-form videos""",
            
            'pattern': """
- Pattern thành công: Hook mạnh trong 15s đầu + personal story + actionable tips
- Thumbnail pattern: Face closeup + bold text + contrasting colors
- Title formula: [Number] + [Emotional word] + [Benefit] + [Curiosity gap]
- CTA hiệu quả: Question at the end + pin comment với resources"""
        }
        
        # Simple keyword matching
        requirements_lower = requirements.lower()
        
        if 'viral' in requirements_lower or 'xu hướng' in requirements_lower:
            return analysis_templates['viral']
        elif 'competitor' in requirements_lower or 'so sánh' in requirements_lower:
            return analysis_templates['competitor']
        elif 'pattern' in requirements_lower or 'công thức' in requirements_lower:
            return analysis_templates['pattern']
        else:
            return f"""
- Phân tích theo yêu cầu "{requirements}":
- Dữ liệu cho thấy cần tập trung vào: Content quality, consistency, và audience engagement
- Đề xuất: Implement A/B testing cho thumbnails và titles
- Next steps: Monitor metrics trong 30 ngày tới và điều chỉnh strategy"""

    def import_analysis(self):
        """Import previously saved analysis data."""
        filename = filedialog.askopenfilename(
            title="Import Analysis Data",
            filetypes=[
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    imported_data = json.load(f)
                
                # Validate imported data
                if not isinstance(imported_data, dict):
                    raise ValueError("Invalid data format")
                
                # Check if it's analysis data or raw data
                if 'data' in imported_data and 'status' in imported_data:
                    # Full result format
                    self.on_complete(imported_data)
                else:
                    # Just the data portion
                    result = {
                        'status': 'success',
                        'data': imported_data,
                        'viral_score': imported_data.get('viral_score', 75.0)
                    }
                    self.on_complete(result)
                
                messagebox.showinfo(
                    "Import Successful",
                    f"Đã import dữ liệu phân tích từ:\n{os.path.basename(filename)}"
                )
                
            except json.JSONDecodeError:
                messagebox.showerror("Import Error", "File không phải định dạng JSON hợp lệ!")
            except Exception as e:
                messagebox.showerror("Import Error", f"Lỗi khi import: {str(e)}")

    def format_analysis_results(data: Dict) -> str:
        """Format analysis results in Vietnamese with detailed insights."""
        if not data:
            return "Không có dữ liệu để phân tích"
            
        summary = data.get('summary', {})
        
        # ... existing code ...
        
        # Check for additional requirements
        additional_reqs = data.get('additional_requirements', [])
        if additional_reqs:
            result_text += f"""
    📋 PHÂN TÍCH BỔ SUNG THEO YÊU CẦU:
    {'='*80}

    """
            for i, req in enumerate(additional_reqs, 1):
                result_text += f"🔍 Yêu cầu {i}: {req['requirement']}\n"
                result_text += f"⏰ Thời gian: {req['timestamp']}\n"
                result_text += f"📊 Kết quả:\n{req['analysis']}\n\n"
                
        return result_text

    # Tab manager interface
    def show(self):
        """Show the tab."""
        self.tab_frame.grid(row=0, column=0, sticky="nsew")
        
    def hide(self):
        """Hide the tab."""
        self.tab_frame.grid_forget()