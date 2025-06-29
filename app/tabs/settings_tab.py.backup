"""
Settings tab manager for API keys and configuration
"""

import customtkinter as ctk
from tkinter import StringVar, filedialog, messagebox
from typing import Callable
import threading
import os


class SettingsTabManager:
    """Manages the settings tab for API configuration."""
    
    def __init__(self, parent, config_manager):
        self.parent = parent
        self.config_manager = config_manager
        
        # Initialize entry lists
        self.openai_entries = []
        self.youtube_entries = []
        self.google_entries = []
        
        # Initialize variables
        self.viral_threshold = None
        self.quality_var = StringVar(value="Balanced")
        
        # Create the tab content
        self.setup_tab()
        
        # Load existing keys
        self.load_saved_keys()
        
    def setup_tab(self):
        """Setup settings tab content."""
        # Settings tab
        self.tab_frame = ctk.CTkScrollableFrame(self.parent, fg_color="#F5F5F5")
        
        # Setup all sections
        self.setup_openai_section()
        self.setup_youtube_section()
        self.setup_google_section()
        self.setup_leonardo_section()
        self.setup_generation_settings()
        self.setup_action_buttons()
        
    def setup_openai_section(self):
        """Setup OpenAI API keys section."""
        # OpenAI Settings
        openai_frame = ctk.CTkFrame(self.tab_frame, fg_color="white", corner_radius=10)
        openai_frame.pack(fill="x", padx=20, pady=20)
        
        # OpenAI header with status
        openai_header_frame = ctk.CTkFrame(openai_frame, fg_color="transparent")
        openai_header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            openai_header_frame,
            text="🤖 OpenAI API Keys",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left")
        
        self.openai_status_label = ctk.CTkLabel(
            openai_header_frame,
            text="● 0 keys configured",
            font=ctk.CTkFont(size=12),
            text_color="#F44336"
        )
        self.openai_status_label.pack(side="right", padx=10)
        
        # OpenAI key entries container
        self.openai_entries_frame = ctk.CTkFrame(openai_frame, fg_color="transparent")
        self.openai_entries_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Add key button
        add_openai_btn = ctk.CTkButton(
            openai_frame,
            text="➕ Add OpenAI Key",
            command=self.add_openai_key,
            fg_color="#4CAF50",
            width=150
        )
        add_openai_btn.pack(pady=(10, 20))
        
    def setup_youtube_section(self):
        """Setup YouTube API keys section."""
        # YouTube Settings
        youtube_frame = ctk.CTkFrame(self.tab_frame, fg_color="white", corner_radius=10)
        youtube_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # YouTube header with status
        youtube_header_frame = ctk.CTkFrame(youtube_frame, fg_color="transparent")
        youtube_header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            youtube_header_frame,
            text="📺 YouTube API Keys",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left")
        
        self.youtube_status_label = ctk.CTkLabel(
            youtube_header_frame,
            text="● 0 keys configured",
            font=ctk.CTkFont(size=12),
            text_color="#F44336"
        )
        self.youtube_status_label.pack(side="right", padx=10)
        
        # YouTube key entries container
        self.youtube_entries_frame = ctk.CTkFrame(youtube_frame, fg_color="transparent")
        self.youtube_entries_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Add key button
        add_youtube_btn = ctk.CTkButton(
            youtube_frame,
            text="➕ Add YouTube Key",
            command=self.add_youtube_key,
            fg_color="#FF0000",
            width=150
        )
        add_youtube_btn.pack(pady=(10, 20))
        
    def setup_google_section(self):
        """Setup Google Service Account section."""
        # Google Service Account
        google_frame = ctk.CTkFrame(self.tab_frame, fg_color="white", corner_radius=10)
        google_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Google header with status
        google_header_frame = ctk.CTkFrame(google_frame, fg_color="transparent")
        google_header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            google_header_frame,
            text="📊 Google Service Accounts (for Sheets export)",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left")
        
        self.google_status_label = ctk.CTkLabel(
            google_header_frame,
            text="● Not configured",
            font=ctk.CTkFont(size=12),
            text_color="#F44336"
        )
        self.google_status_label.pack(side="right", padx=10)
        
        # Google credentials container
        self.google_entries_frame = ctk.CTkFrame(google_frame, fg_color="transparent")
        self.google_entries_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Add credential button
        add_google_btn = ctk.CTkButton(
            google_frame,
            text="➕ Add Service Account Credentials",
            command=self.add_google_credential,
            fg_color="#1A73E8",
            width=200
        )
        add_google_btn.pack(pady=(10, 20))
        
    def setup_leonardo_section(self):
        """Setup Leonardo AI section."""
        # Leonardo AI Settings
        leonardo_frame = ctk.CTkFrame(self.tab_frame, fg_color="white", corner_radius=10)
        leonardo_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Leonardo header with status
        leonardo_header_frame = ctk.CTkFrame(leonardo_frame, fg_color="transparent")
        leonardo_header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            leonardo_header_frame,
            text="🎨 Leonardo AI",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left")
        
        self.leonardo_status_label = ctk.CTkLabel(
            leonardo_header_frame,
            text="● Not configured",
            font=ctk.CTkFont(size=12),
            text_color="#F44336"
        )
        self.leonardo_status_label.pack(side="right", padx=10)
        
        # Leonardo key entry
        leonardo_entry_frame = ctk.CTkFrame(leonardo_frame, fg_color="transparent")
        leonardo_entry_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        self.leonardo_entry = ctk.CTkEntry(
            leonardo_entry_frame,
            placeholder_text="Enter Leonardo AI API key",
            show="*",
            width=400
        )
        self.leonardo_entry.pack(side="left", padx=(0, 10))
        
        # Test button for Leonardo
        test_leonardo_btn = ctk.CTkButton(
            leonardo_entry_frame,
            text="Test",
            command=self.test_leonardo_api,
            width=80
        )
        test_leonardo_btn.pack(side="left")
        
    def setup_generation_settings(self):
        """Setup generation settings section."""
        # Generation Settings
        gen_frame = ctk.CTkFrame(self.tab_frame, fg_color="white", corner_radius=10)
        gen_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            gen_frame,
            text="⚙️ Generation Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=(20, 15), sticky="w")
        
        # API Status Check Button
        api_status_btn = ctk.CTkButton(
            gen_frame,
            text="🔍 Check All API Status",
            command=self.check_all_api_status,
            fg_color="#2196F3",
            hover_color="#1976D2",
            width=180,
            height=40
        )
        api_status_btn.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        # Test all APIs button
        test_all_btn = ctk.CTkButton(
            gen_frame,
            text="🧪 Test All APIs",
            command=self.test_all_apis,
            fg_color="#9C27B0",
            hover_color="#7B1FA2",
            width=180,
            height=40
        )
        test_all_btn.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        
        # Viral Score Threshold
        ctk.CTkLabel(gen_frame, text="Viral Score Threshold:").grid(
            row=2, column=0, padx=20, pady=10, sticky="w"
        )
        self.viral_threshold = ctk.CTkSlider(
            gen_frame,
            from_=0,
            to=100,
            number_of_steps=100,
            width=300
        )
        self.viral_threshold.grid(row=2, column=1, padx=20, pady=10)
        self.viral_threshold.set(70)
        
        self.threshold_label = ctk.CTkLabel(gen_frame, text="70%")
        self.threshold_label.grid(row=2, column=2, padx=10, pady=10)
        self.viral_threshold.configure(command=self.update_threshold_label)
        
        # Quality settings
        quality_options = ["Balanced", "Quality", "Speed"]
        ctk.CTkLabel(gen_frame, text="Quality:").grid(
            row=3, column=0, padx=20, pady=10, sticky="w"
        )
        for i, option in enumerate(quality_options):
            radio = ctk.CTkRadioButton(
                gen_frame,
                text=option,
                variable=self.quality_var,
                value=option
            )
            radio.grid(row=3, column=i+1, padx=10, pady=10)
            
        # Enable features
        self.enable_viral_scoring = ctk.CTkCheckBox(
            gen_frame,
            text="✓ Enable Viral Scoring"
        )
        self.enable_viral_scoring.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.enable_viral_scoring.select()
        
        self.enable_low_score_retry = ctk.CTkCheckBox(
            gen_frame,
            text="✓ Enable Retry for Low Scores"
        )
        self.enable_low_score_retry.grid(row=4, column=1, padx=20, pady=10, sticky="w")
        self.enable_low_score_retry.select()
        
        self.auto_optimize = ctk.CTkCheckBox(
            gen_frame,
            text="✓ Auto-optimize Prompts Based on Performance"
        )
        self.auto_optimize.grid(row=5, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="w")
        
    def setup_action_buttons(self):
        """Setup action buttons."""
        # Save Settings button
        save_frame = ctk.CTkFrame(self.tab_frame, fg_color="transparent")
        save_frame.pack(pady=20)
        
        save_btn = ctk.CTkButton(
            save_frame,
            text="💾 Save Settings",
            command=self.save_all_settings,
            fg_color="#4CAF50",
            hover_color="#45A049",
            width=200,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        save_btn.pack(side="left", padx=10)
        
        clear_btn = ctk.CTkButton(
            save_frame,
            text="🗑️ Clear All Keys",
            command=self.clear_all_keys,
            fg_color="#F44336",
            hover_color="#E53935",
            width=200,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        clear_btn.pack(side="left", padx=10)

    # API Key Management Methods
    def add_openai_key(self):
        """Add OpenAI API key entry."""
        entry_frame = ctk.CTkFrame(self.openai_entries_frame, fg_color="transparent")
        entry_frame.pack(fill="x", pady=5)
        
        entry = ctk.CTkEntry(
            entry_frame,
            placeholder_text="Enter OpenAI API key",
            show="*",
            width=400
        )
        entry.pack(side="left", padx=(0, 10))
        
        test_btn = ctk.CTkButton(
            entry_frame,
            text="Test",
            command=lambda: self.test_openai_key(entry),
            width=80
        )
        test_btn.pack(side="left", padx=(0, 10))
        
        remove_btn = ctk.CTkButton(
            entry_frame,
            text="❌ Remove",
            command=lambda: self.remove_key_entry(entry_frame, self.openai_entries),
            fg_color="#F44336",
            width=100
        )
        remove_btn.pack(side="left")
        
        self.openai_entries.append((entry_frame, entry))
        self.update_api_status_labels()
        
    def add_youtube_key(self):
        """Add YouTube API key entry."""
        entry_frame = ctk.CTkFrame(self.youtube_entries_frame, fg_color="transparent")
        entry_frame.pack(fill="x", pady=5)
        
        entry = ctk.CTkEntry(
            entry_frame,
            placeholder_text="Enter YouTube API key",
            show="*",
            width=400
        )
        entry.pack(side="left", padx=(0, 10))
        
        test_btn = ctk.CTkButton(
            entry_frame,
            text="Test",
            command=lambda: self.test_youtube_key(entry),
            width=80
        )
        test_btn.pack(side="left", padx=(0, 10))
        
        remove_btn = ctk.CTkButton(
            entry_frame,
            text="❌ Remove",
            command=lambda: self.remove_key_entry(entry_frame, self.youtube_entries),
            fg_color="#F44336",
            width=100
        )
        remove_btn.pack(side="left")
        
        self.youtube_entries.append((entry_frame, entry))
        self.update_api_status_labels()
        
    def add_google_credential(self):
        """Add Google Service Account credential."""
        entry_frame = ctk.CTkFrame(self.google_entries_frame, fg_color="transparent")
        entry_frame.pack(fill="x", pady=5)
        
        file_label = ctk.CTkLabel(
            entry_frame,
            text="No file selected",
            fg_color="#E0E0E0",
            corner_radius=5,
            width=300
        )
        file_label.pack(side="left", padx=(0, 10))
        
        browse_btn = ctk.CTkButton(
            entry_frame,
            text="📁 Browse",
            command=lambda: self.browse_credential_file(file_label),
            width=100
        )
        browse_btn.pack(side="left", padx=(0, 10))
        
        test_btn = ctk.CTkButton(
            entry_frame,
            text="Test",
            command=lambda: self.test_google_credential(file_label),
            width=80
        )
        test_btn.pack(side="left", padx=(0, 10))
        
        remove_btn = ctk.CTkButton(
            entry_frame,
            text="❌ Remove",
            command=lambda: self.remove_key_entry(entry_frame, self.google_entries),
            fg_color="#F44336",
            width=100
        )
        remove_btn.pack(side="left")
        
        self.google_entries.append((entry_frame, file_label))
        self.update_api_status_labels()
        
    def remove_key_entry(self, frame, entries_list):
        """Remove an API key entry."""
        frame.destroy()
        entries_list[:] = [(f, e) for f, e in entries_list if f != frame]
        self.update_api_status_labels()
        
    def update_api_status_labels(self):
        """Update status labels for all APIs."""
        # OpenAI status
        openai_count = len(self.openai_entries)
        if openai_count > 0:
            self.openai_status_label.configure(
                text=f"● {openai_count} keys configured",
                text_color="#4CAF50"
            )
        else:
            self.openai_status_label.configure(
                text="● 0 keys configured",
                text_color="#F44336"
            )
            
        # YouTube status
        youtube_count = len(self.youtube_entries)
        if youtube_count > 0:
            self.youtube_status_label.configure(
                text=f"● {youtube_count} keys configured",
                text_color="#4CAF50"
            )
        else:
            self.youtube_status_label.configure(
                text="● 0 keys configured",
                text_color="#F44336"
            )
            
        # Google status
        google_count = len(self.google_entries)
        if google_count > 0:
            self.google_status_label.configure(
                text=f"● {google_count} accounts configured",
                text_color="#4CAF50"
            )
        else:
            self.google_status_label.configure(
                text="● Not configured",
                text_color="#F44336"
            )
            
        # Leonardo status
        if self.leonardo_entry.get():
            self.leonardo_status_label.configure(
                text="● Configured",
                text_color="#4CAF50"
            )
        else:
            self.leonardo_status_label.configure(
                text="● Not configured",
                text_color="#F44336"
            )

    # Testing Methods
    def test_openai_key(self, entry_widget):
        """Test OpenAI API key."""
        key = entry_widget.get()
        if not key:
            messagebox.showwarning("Warning", "Please enter an API key")
            return
            
        # Use config manager to test
        is_valid, message = self.config_manager.test_openai_api(key)
        
        if is_valid:
            messagebox.showinfo("Test Result", message)
            # Update in config
            if key not in self.config_manager.api_config.openai_keys:
                self.config_manager.add_openai_key(key)
        else:
            messagebox.showerror("Test Failed", message)
        
    def test_youtube_key(self, entry_widget):
        """Test YouTube API key."""
        key = entry_widget.get()
        if not key:
            messagebox.showwarning("Warning", "Please enter an API key")
            return
            
        # Use config manager to test
        is_valid, message = self.config_manager.test_youtube_api(key)
        
        if is_valid:
            messagebox.showinfo("Test Result", message)
            # Update in config
            if key not in self.config_manager.api_config.youtube_keys:
                self.config_manager.add_youtube_key(key)
        else:
            messagebox.showerror("Test Failed", message)
        
    def test_google_credential(self, file_label):
        """Test Google Service Account credential."""
        if not hasattr(file_label, 'file_path'):
            messagebox.showwarning("Warning", "Please select a credential file")
            return
            
        # Use config manager to test
        is_valid, message = self.config_manager.test_google_credentials(file_label.file_path)
        
        if is_valid:
            messagebox.showinfo("Test Result", message)
        else:
            messagebox.showerror("Test Failed", message)
        
    def test_leonardo_api(self):
        """Test Leonardo AI API key."""
        key = self.leonardo_entry.get()
        if not key:
            messagebox.showwarning("Warning", "Please enter Leonardo AI API key")
            return
            
        # Use config manager to test
        is_valid, message = self.config_manager.test_leonardo_api(key)
        
        if is_valid:
            messagebox.showinfo("Test Result", message)
            self.config_manager.api_config.leonardo_key = key
            self.config_manager.save_config()
            self.update_api_status_labels()
        else:
            messagebox.showerror("Test Failed", message)

    def check_all_api_status(self):
        """Check status of all configured APIs using config manager."""
        status = self.config_manager.get_api_status()
        
        status_report = []
        
        # YouTube status
        yt = status['youtube']
        status_report.append(f"YouTube API: {yt['configured']} keys configured, {yt['valid']} valid")
        for key_info in yt['keys']:
            status_report.append(f"  - {key_info['key']}: {key_info['message']}")
            
        # OpenAI status
        openai = status['openai']
        status_report.append(f"\nOpenAI API: {openai['configured']} keys configured, {openai['valid']} valid")
        for key_info in openai['keys']:
            status_report.append(f"  - {key_info['key']}: {key_info['message']}")
            
        # Leonardo status
        leo = status['leonardo']
        if leo['configured']:
            status_report.append(f"\nLeonardo AI: {leo.get('message', 'Configured')}")
            
        # Google status
        google = status['google']
        status_report.append(f"\nGoogle Sheets: {google['configured']} accounts configured, {google['valid']} valid")
        for cred_info in google['credentials']:
            status_report.append(f"  - {cred_info['file']}: {cred_info['message']}")
            
        # Overall readiness
        ready, msg = self.config_manager.is_ready_for_analysis()
        status_report.append(f"\n{'='*40}")
        status_report.append(msg)
        
        messagebox.showinfo("API Status Report", "\n".join(status_report))
        
    def test_all_apis(self):
        """Test all configured APIs."""
        # Show progress dialog
        progress_window = ctk.CTkToplevel(self.tab_frame)
        progress_window.title("Testing APIs...")
        progress_window.geometry("400x200")
        progress_window.transient(self.tab_frame)
        progress_window.grab_set()
        
        progress_label = ctk.CTkLabel(
            progress_window,
            text="Testing all configured APIs...",
            font=ctk.CTkFont(size=14)
        )
        progress_label.pack(pady=20)
        
        progress_bar = ctk.CTkProgressBar(progress_window, width=300)
        progress_bar.pack(pady=10)
        progress_bar.set(0)
        
        status_text = ctk.CTkLabel(progress_window, text="")
        status_text.pack(pady=10)
        
        def run_tests():
            # Test all APIs
            status = self.config_manager.get_api_status()
            
            # Calculate progress
            total_tests = (len(status['youtube']['keys']) + 
                          len(status['openai']['keys']) + 
                          (1 if status['leonardo']['configured'] else 0) +
                          len(status['google']['credentials']))
            
            if total_tests == 0:
                progress_window.destroy()
                messagebox.showwarning("No APIs", "No API keys configured to test")
                return
                
            # The actual status is already computed by get_api_status()
            # Just show the results
            progress_bar.set(1.0)
            status_text.configure(text="Tests completed!")
            
            # Close progress window
            progress_window.after(1000, progress_window.destroy)
            
            # Show results
            self.tab_frame.after(1100, self.check_all_api_status)
            
        # Run tests in thread
        thread = threading.Thread(target=run_tests)
        thread.daemon = True
        thread.start()

    # File Management
    def browse_credential_file(self, label):
        """Browse for credential file."""
        filename = filedialog.askopenfilename(
            title="Select Google Service Account JSON",
            filetypes=[("JSON files", "*.json")]
        )
        if filename:
            label.configure(text=os.path.basename(filename))
            label.file_path = filename
            self.update_api_status_labels()
            
    def update_threshold_label(self, value):
        """Update threshold label."""
        self.threshold_label.configure(text=f"{int(value)}%")

    # Settings Management
    def save_all_settings(self):
        """Save all settings using config manager."""
        try:
            # Update config manager with current UI values
            config = self.config_manager.api_config
            
            # Collect OpenAI keys
            config.openai_keys = [entry.get() for _, entry in self.openai_entries if entry.get()]
            
            # Collect YouTube keys
            config.youtube_keys = [entry.get() for _, entry in self.youtube_entries if entry.get()]
            
            # Leonardo key
            config.leonardo_key = self.leonardo_entry.get()
            
            # Google credentials
            config.google_credentials = []
            for _, label in self.google_entries:
                if hasattr(label, 'file_path'):
                    config.google_credentials.append(label.file_path)
            
            # Update generation settings
            settings = self.config_manager.generation_settings
            settings.viral_threshold = int(self.viral_threshold.get())
            settings.quality = self.quality_var.get()
            settings.enable_viral_scoring = self.enable_viral_scoring.get()
            settings.enable_retry = self.enable_low_score_retry.get()
            settings.auto_optimize = self.auto_optimize.get()
            
            # Save to file
            if self.config_manager.save_config():
                messagebox.showinfo("Success", "Settings saved successfully!")
            else:
                messagebox.showerror("Error", "Failed to save settings")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
            
    def clear_all_keys(self):
        """Clear all API keys after confirmation."""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all API keys?"):
            # Clear UI elements
            for frame, _ in self.openai_entries:
                frame.destroy()
            self.openai_entries.clear()
            
            for frame, _ in self.youtube_entries:
                frame.destroy()
            self.youtube_entries.clear()
            
            for frame, _ in self.google_entries:
                frame.destroy()
            self.google_entries.clear()
            
            self.leonardo_entry.delete(0, 'end')
            
            # Clear in config manager
            self.config_manager.clear_all_keys()
            
            # Update status labels
            self.update_api_status_labels()
            
            messagebox.showinfo("Success", "All API keys cleared!")
            
    def load_saved_keys(self):
        """Load saved API keys from config file."""
        # Keys are automatically loaded by config_manager
        # Just refresh the UI
        config = self.config_manager.api_config
        
        # Load OpenAI keys
        for key in config.openai_keys:
            if key:
                self.add_openai_key()
                _, entry = self.openai_entries[-1]
                entry.insert(0, key)
                
        # Load YouTube keys
        for key in config.youtube_keys:
            if key:
                self.add_youtube_key()
                _, entry = self.youtube_entries[-1]
                entry.insert(0, key)
                
        # Load Leonardo key
        if config.leonardo_key:
            self.leonardo_entry.insert(0, config.leonardo_key)
            
        # Load Google credentials
        for cred_file in config.google_credentials:
            if cred_file and os.path.exists(cred_file):
                self.add_google_credential()
                _, label = self.google_entries[-1]
                label.configure(text=os.path.basename(cred_file))
                label.file_path = cred_file
                
        self.update_api_status_labels()

    # Tab manager interface
    def show(self):
        """Show the tab."""
        self.tab_frame.grid(row=0, column=0, sticky="nsew")
        
    def hide(self):
        """Hide the tab."""
        self.tab_frame.grid_forget()