"""
Topic tab manager for generating viral topic ideas
"""

import customtkinter as ctk
from tkinter import StringVar, messagebox, filedialog
from typing import Callable, Dict, List
from datetime import datetime
import json
import threading


class TopicTabManager:
    """Manages the topic generation tab."""
    
    def __init__(self, parent, generate_callback: Callable, export_callback: Callable):
        self.parent = parent
        self.generate_callback = generate_callback
        self.export_callback = export_callback
        
        # Initialize variables
        self.num_topics_var = StringVar(value="10")
        self.generated_topics = []
        
        # Create the tab content
        self.setup_tab()
        
    def setup_tab(self):
        """Setup topic generation tab content."""
        # Topic generation tab
        self.tab_frame = ctk.CTkFrame(self.parent, fg_color="#F5F5F5")
        self.tab_frame.grid_rowconfigure(3, weight=1)
        self.tab_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        self.setup_header()
        
        # Settings
        self.setup_settings()
        
        # Generate button
        self.setup_generate_button()
        
        # Results area
        self.setup_results_area()
        
        # Export button
        self.setup_export_section()
        
    def setup_header(self):
        """Setup header section."""
        header_frame = ctk.CTkFrame(self.tab_frame, fg_color="white", corner_radius=10)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        header_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            header_frame,
            text="💡 Generate Viral Topics",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, pady=(15, 5))
        
        ctk.CTkLabel(
            header_frame,
            text="Generate viral topic ideas based on analysis results.",
            font=ctk.CTkFont(size=14),
            text_color="#666666"
        ).grid(row=1, column=0, pady=(0, 15))
        
    def setup_settings(self):
        """Setup topic generation settings."""
        settings_frame = ctk.CTkFrame(self.tab_frame, fg_color="white", corner_radius=10)
        settings_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        settings_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            settings_frame,
            text="⚙️ Topic Generation Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 15), sticky="w")
        
        # Number of topics
        ctk.CTkLabel(settings_frame, text="Number of Topics:").grid(
            row=1, column=0, padx=20, pady=10, sticky="w"
        )
        num_topics_entry = ctk.CTkEntry(
            settings_frame,
            textvariable=self.num_topics_var,
            width=200
        )
        num_topics_entry.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        
        # Topic focus
        ctk.CTkLabel(settings_frame, text="Topic Focus:").grid(
            row=2, column=0, padx=20, pady=10, sticky="w"
        )
        self.topic_focus = ctk.CTkComboBox(
            settings_frame,
            values=[
                "Psychology & Relationships", 
                "Technology & Innovation", 
                "Health & Wellness", 
                "Education & Learning", 
                "Entertainment & Humor",
                "Business & Finance",
                "Lifestyle & Personal Growth",
                "Science & Discovery"
            ],
            width=300
        )
        self.topic_focus.grid(row=2, column=1, padx=20, pady=10, sticky="w")
        self.topic_focus.set("Psychology & Relationships")
        
        # Content type
        ctk.CTkLabel(settings_frame, text="Content Type:").grid(
            row=3, column=0, padx=20, pady=10, sticky="w"
        )
        self.content_type = ctk.CTkComboBox(
            settings_frame,
            values=[
                "Video Content",
                "Blog Posts", 
                "Social Media Posts",
                "Podcast Episodes",
                "Email Newsletter",
                "Course Content"
            ],
            width=300
        )
        self.content_type.grid(row=3, column=1, padx=20, pady=10, sticky="w")
        self.content_type.set("Video Content")
        
        # Target audience
        ctk.CTkLabel(settings_frame, text="Target Audience:").grid(
            row=4, column=0, padx=20, pady=10, sticky="w"
        )
        self.target_audience = ctk.CTkComboBox(
            settings_frame,
            values=[
                "Gen Z (18-24)",
                "Millennials (25-40)", 
                "Gen X (41-56)",
                "All Adults",
                "Professionals",
                "Students",
                "Parents"
            ],
            width=300
        )
        self.target_audience.grid(row=4, column=1, padx=20, pady=(10, 20), sticky="w")
        self.target_audience.set("Millennials (25-40)")
        
    def setup_generate_button(self):
        """Setup generate button."""
        self.generate_topics_btn = ctk.CTkButton(
            self.tab_frame,
            text="🔥 Generate Viral Topics",
            command=self.generate_topics,
            height=50,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#FF6B35",
            hover_color="#E85D25"
        )
        self.generate_topics_btn.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        
    def setup_results_area(self):
        """Setup results display area."""
        # Results container
        results_container = ctk.CTkFrame(self.tab_frame, fg_color="white", corner_radius=10)
        results_container.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))
        results_container.grid_rowconfigure(1, weight=1)
        results_container.grid_columnconfigure(0, weight=1)
        
        # Results header
        ctk.CTkLabel(
            results_container,
            text="📋 Generated Topics",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Scrollable frame for topics
        self.topics_results_frame = ctk.CTkScrollableFrame(
            results_container,
            fg_color="#F8F9FA",
            corner_radius=10
        )
        self.topics_results_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
    def setup_export_section(self):
        """Setup export section."""
        export_frame = ctk.CTkFrame(self.tab_frame, fg_color="transparent")
        export_frame.grid(row=4, column=0, pady=(0, 20))
        
        self.export_topics_btn = ctk.CTkButton(
            export_frame,
            text="📥 Export Topics",
            command=self.export_topics,
            fg_color="#2196F3",
            width=150,
            height=40,
            state="disabled"
        )
        self.export_topics_btn.pack(side="left", padx=10)
        
        self.copy_all_btn = ctk.CTkButton(
            export_frame,
            text="📋 Copy All",
            command=self.copy_all_topics,
            fg_color="#4CAF50",
            width=150,
            height=40,
            state="disabled"
        )
        self.copy_all_btn.pack(side="left", padx=10)
        
        self.clear_topics_btn = ctk.CTkButton(
            export_frame,
            text="🗑️ Clear Topics",
            command=self.clear_topics,
            fg_color="#757575",
            width=150,
            height=40,
            state="disabled"
        )
        self.clear_topics_btn.pack(side="left", padx=10)

    def generate_topics(self):
        """Generate viral topics."""
        # Update button state
        self.generate_topics_btn.configure(state="disabled", text="🔄 Generating...")
        
        # Get settings
        num_topics = int(self.num_topics_var.get())
        focus = self.topic_focus.get()
        content_type = self.content_type.get()
        audience = self.target_audience.get()
        
        def generate_in_background():
            try:
                # Generate topics based on focus area
                topics = self.create_topics_based_on_focus(focus, content_type, audience, num_topics)
                
                # Update UI in main thread
                self.tab_frame.after(0, self._update_topics_display, topics)
                
            except Exception as e:
                self.tab_frame.after(0, self._show_generation_error, str(e))
        
        # Run in background thread
        thread = threading.Thread(target=generate_in_background, daemon=True)
        thread.start()

        try:
            self.generate_callback({'demo': True})
        except:
            # Use built-in demo generation
            self._generate_demo_topics()

    def _generate_demo_topics(self):
        """Generate demo topics khi callback fails."""
        # Update button state
        self.generate_topics_btn.configure(state="disabled", text="🔄 Generating...")
        
        # Get settings
        num_topics = int(self.num_topics_var.get())
        focus = self.topic_focus.get()
        content_type = self.content_type.get()
        audience = self.target_audience.get()
        
        # Generate demo topics
        import time
        time.sleep(1)  # Simulate processing
        
        topics = self.create_topics_based_on_focus(focus, content_type, audience, num_topics)
        
        # Update display
        self.tab_frame.after(0, self._update_topics_display, topics)        
        
    def create_topics_based_on_focus(self, focus: str, content_type: str, audience: str, num_topics: int) -> List[Dict]:
        """Create topics based on selected focus area."""
        # Topic templates by focus area
        topic_templates = {
            "Psychology & Relationships": [
                "The Hidden Psychology Behind Why We {action}",
                "5 Toxic {relationship_type} Patterns You Don't Realize You're In",
                "Why Your Brain Craves {emotion} (And How to Break Free)",
                "The Science of {psychological_concept}: What Really Happens to Your {body_part}",
                "Attachment Styles: The Secret Code to All Your {relationship_area}",
                "{number} Signs You're Dating a {personality_type}",
                "Why We {behavior} When We're {emotional_state}",
                "The Psychology of {daily_activity}: What It Reveals About You",
                "How to Read People Like a Book: {number} Body Language Secrets",
                "The Dark Side of {positive_trait}: When It Becomes Toxic"
            ],
            "Technology & Innovation": [
                "The Future of {tech_field}: What's Coming in {year}",
                "{number} AI Tools That Will Change {industry} Forever",
                "Why {tech_company} Is Winning the {tech_battle}",
                "The Hidden Dangers of {popular_tech}",
                "How {emerging_tech} Will Transform {daily_activity}",
                "{number} Tech Trends Everyone Will Be Talking About",
                "The Rise and Fall of {tech_product}: What Went Wrong",
                "Why {tech_concept} Is the Next Big Thing",
                "The Real Cost of {digital_service}: Is It Worth It?",
                "How to Protect Yourself from {tech_threat}"
            ],
            "Health & Wellness": [
                "The {number}-Minute Morning Routine That Changed My Life",
                "Why {popular_diet} Doesn't Work (And What Does)",
                "The Secret to {health_goal} That Doctors Don't Tell You",
                "{number} Foods That Are Secretly Destroying Your {body_system}",
                "The Science-Backed Way to {wellness_activity}",
                "Why Everyone Is Talking About {wellness_trend}",
                "The Hidden Connection Between {activity} and {health_outcome}",
                "How to {health_action} Without {common_struggle}",
                "{number} Myths About {health_topic} That Need to Die",
                "The Real Reason You Can't {health_goal}"
            ]
        }
        
        # Variables for topic generation
        variables = {
            "action": ["ghost people", "self-sabotage", "procrastinate", "avoid commitment", "overthink everything"],
            "relationship_type": ["relationship", "friendship", "workplace", "family", "dating"],
            "emotion": ["drama", "validation", "chaos", "attention", "conflict"],
            "psychological_concept": ["heartbreak", "rejection", "attachment", "trauma", "anxiety"],
            "body_part": ["brain", "heart", "body", "mind", "nervous system"],
            "relationship_area": ["relationships", "connections", "interactions", "bonds", "communications"],
            "number": ["3", "5", "7", "10", "12"],
            "personality_type": ["narcissist", "empath", "introvert", "people-pleaser", "perfectionist"],
            "behavior": ["lie", "cheat", "withdraw", "lash out", "shut down"],
            "emotional_state": ["stressed", "angry", "hurt", "scared", "overwhelmed"],
            "daily_activity": ["social media", "shopping", "eating", "working", "sleeping"],
            "positive_trait": ["kindness", "ambition", "perfectionism", "loyalty", "independence"],
            "tech_field": ["AI", "blockchain", "VR", "quantum computing", "robotics"],
            "year": ["2025", "2026", "2030"],
            "tech_company": ["Apple", "Google", "Meta", "OpenAI", "Tesla"],
            "tech_battle": ["AI race", "metaverse war", "streaming wars", "smartphone battle"],
            "popular_tech": ["social media", "smartphones", "AI chatbots", "smart homes"],
            "emerging_tech": ["AI", "VR", "blockchain", "IoT", "5G"],
            "industry": ["healthcare", "education", "finance", "entertainment", "retail"],
            "tech_product": ["Google Glass", "Facebook Portal", "Clubhouse", "NFTs"],
            "tech_concept": ["quantum computing", "neural interfaces", "digital twins", "edge computing"],
            "digital_service": ["Netflix", "social media", "cloud storage", "online shopping"],
            "tech_threat": ["AI bias", "data breaches", "deepfakes", "cyber attacks"],
            "health_goal": ["lose weight", "sleep better", "reduce stress", "boost energy"],
            "wellness_activity": ["meditate", "exercise", "eat healthy", "sleep better"],
            "wellness_trend": ["intermittent fasting", "cold therapy", "breathwork", "mindfulness"],
            "health_outcome": ["longevity", "happiness", "productivity", "immunity"],
            "health_action": ["lose weight", "build muscle", "reduce anxiety", "improve focus"],
            "common_struggle": ["giving up", "feeling hungry", "losing motivation", "getting overwhelmed"],
            "health_topic": ["calories", "carbs", "supplements", "exercise", "sleep"]
        }
        
        import random
        
        # Get templates for the focus area
        templates = topic_templates.get(focus, topic_templates["Psychology & Relationships"])
        
        # Generate topics
        generated_topics = []
        
        for i in range(num_topics):
            # Select random template
            template = random.choice(templates)
            
            # Replace variables in template
            topic = template
            for var, options in variables.items():
                if f"{{{var}}}" in topic:
                    topic = topic.replace(f"{{{var}}}", random.choice(options))
            
            # Create topic data
            topic_data = {
                "id": i + 1,
                "title": topic,
                "focus": focus,
                "content_type": content_type,
                "target_audience": audience,
                "viral_score": random.randint(70, 95),  # Simulated viral potential
                "created_at": datetime.now().isoformat(),
                "keywords": self.extract_keywords_from_topic(topic),
                "engagement_prediction": random.choice(["High", "Very High", "Extremely High"])
            }
            
            generated_topics.append(topic_data)
        
        return generated_topics

    def extract_keywords_from_topic(self, topic: str) -> List[str]:
        """Extract keywords from topic for SEO."""
        # Simple keyword extraction
        keywords = []
        
        # Common viral keywords
        viral_words = ["secret", "hidden", "why", "how", "science", "psychology", "signs", "toxic", "myths"]
        
        topic_lower = topic.lower()
        for word in viral_words:
            if word in topic_lower:
                keywords.append(word)
        
        # Add topic-specific keywords
        if "relationship" in topic_lower:
            keywords.extend(["relationships", "dating", "love"])
        if "psychology" in topic_lower:
            keywords.extend(["psychology", "mental health", "behavior"])
        if "brain" in topic_lower:
            keywords.extend(["neuroscience", "cognitive", "mindset"])
            
        return keywords[:5]  # Limit to 5 keywords

    def _update_topics_display(self, topics: List[Dict]):
        """Update topics display with generated topics."""
        # Store topics
        self.generated_topics = topics
        
        # Clear previous results
        for widget in self.topics_results_frame.winfo_children():
            widget.destroy()
        
        # Display topics
        for topic in topics:
            self._create_topic_card(topic)
        
        # Enable export buttons
        self.export_topics_btn.configure(state="normal")
        self.copy_all_btn.configure(state="normal")
        self.clear_topics_btn.configure(state="normal")
        
        # Reset generate button
        self.generate_topics_btn.configure(state="normal", text="🔥 Generate Viral Topics")
        
        messagebox.showinfo("Success", f"Generated {len(topics)} viral topics!")

    def _create_topic_card(self, topic: Dict):
        """Create a card for displaying topic."""
        card = ctk.CTkFrame(self.topics_results_frame, fg_color="white", corner_radius=10)
        card.pack(fill="x", padx=10, pady=10)
        
        # Header with topic number and viral score
        header_frame = ctk.CTkFrame(card, fg_color="#E8F5E8", corner_radius=8)
        header_frame.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(
            header_frame,
            text=f"#{topic['id']}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#2196F3"
        ).pack(side="left", padx=15, pady=10)
        
        # Viral score
        score_color = "#4CAF50" if topic['viral_score'] >= 85 else "#FF9800" if topic['viral_score'] >= 75 else "#F44336"
        ctk.CTkLabel(
            header_frame,
            text=f"🔥 {topic['viral_score']}% Viral Potential",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=score_color
        ).pack(side="right", padx=15, pady=10)
        
        # Topic title
        title_label = ctk.CTkLabel(
            card,
            text=topic['title'],
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=600,
            justify="left"
        )
        title_label.pack(anchor="w", padx=15, pady=(0, 10))
        
        # Metadata
        meta_frame = ctk.CTkFrame(card, fg_color="#F5F5F5", corner_radius=5)
        meta_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        meta_text = f"📊 {topic['content_type']} | 🎯 {topic['target_audience']} | 📈 {topic['engagement_prediction']} Engagement"
        if topic['keywords']:
            meta_text += f" | 🏷️ {', '.join(topic['keywords'][:3])}"
            
        ctk.CTkLabel(
            meta_frame,
            text=meta_text,
            font=ctk.CTkFont(size=11),
            text_color="#666666"
        ).pack(padx=10, pady=8)
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(card, fg_color="transparent")
        buttons_frame.pack(pady=(0, 15))
        
        select_btn = ctk.CTkButton(
            buttons_frame,
            text="📌 Select",
            command=lambda: self.select_topic(topic),
            width=100,
            height=30,
            fg_color="#2196F3"
        )
        select_btn.pack(side="left", padx=5)
        
        copy_btn = ctk.CTkButton(
            buttons_frame,
            text="📋 Copy",
            command=lambda: self.copy_topic(topic),
            width=100,
            height=30,
            fg_color="#4CAF50"
        )
        copy_btn.pack(side="left", padx=5)
        
        edit_btn = ctk.CTkButton(
            buttons_frame,
            text="✏️ Edit",
            command=lambda: self.edit_topic(topic),
            width=100,
            height=30,
            fg_color="#FF9800"
        )
        edit_btn.pack(side="left", padx=5)

    def _show_generation_error(self, error_message: str):
        """Show error message for topic generation."""
        self.generate_topics_btn.configure(state="normal", text="🔥 Generate Viral Topics")
        messagebox.showerror("Error", f"Failed to generate topics: {error_message}")

    def select_topic(self, topic: Dict):
        """Select topic and move to content tab."""
        # Store selected topic in clipboard for content tab
        self.tab_frame.clipboard_clear()
        self.tab_frame.clipboard_append(topic['title'])
        
        messagebox.showinfo("Topic Selected", f"Selected: {topic['title'][:50]}...\nTopic copied to clipboard!")

    def copy_topic(self, topic: Dict):
        """Copy topic to clipboard."""
        self.tab_frame.clipboard_clear()
        self.tab_frame.clipboard_append(topic['title'])
        messagebox.showinfo("Copied", "Topic copied to clipboard!")

    def edit_topic(self, topic: Dict):
        """Edit topic title."""
        # Create edit dialog
        edit_window = ctk.CTkToplevel(self.tab_frame)
        edit_window.title("Edit Topic")
        edit_window.geometry("600x300")
        edit_window.transient(self.tab_frame)
        edit_window.grab_set()
        
        # Edit form
        ctk.CTkLabel(
            edit_window,
            text="Edit Topic:",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(20, 10))
        
        edit_textbox = ctk.CTkTextbox(edit_window, height=100, width=500)
        edit_textbox.pack(pady=10, padx=20)
        edit_textbox.insert("1.0", topic['title'])
        
        # Buttons
        button_frame = ctk.CTkFrame(edit_window, fg_color="transparent")
        button_frame.pack(pady=20)
        
        def save_edit():
            new_title = edit_textbox.get("1.0", "end-1c")
            topic['title'] = new_title
            edit_window.destroy()
            # Refresh display
            self._update_topics_display(self.generated_topics)
            messagebox.showinfo("Saved", "Topic updated successfully!")
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Save",
            command=save_edit,
            fg_color="#4CAF50"
        )
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="❌ Cancel",
            command=edit_window.destroy,
            fg_color="#757575"
        )
        cancel_btn.pack(side="left", padx=10)

    def export_topics(self):
        """Export generated topics to file."""
        if not self.generated_topics:
            messagebox.showwarning("No Topics", "No topics to export!")
            return
        
        # Ask for filename
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[
                ("JSON files", "*.json"),
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ],
            initialfile=f"viral_topics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(self.generated_topics, f, ensure_ascii=False, indent=2)
                elif filename.endswith('.txt'):
                    with open(filename, 'w', encoding='utf-8') as f:
                        for i, topic in enumerate(self.generated_topics, 1):
                            f.write(f"{i}. {topic['title']}\n")
                elif filename.endswith('.csv'):
                    import csv
                    with open(filename, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(['ID', 'Title', 'Focus', 'Content Type', 'Target Audience', 'Viral Score'])
                        for topic in self.generated_topics:
                            writer.writerow([
                                topic['id'], topic['title'], topic['focus'], 
                                topic['content_type'], topic['target_audience'], topic['viral_score']
                            ])
                
                messagebox.showinfo("Success", f"Topics exported to: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export topics: {e}")

    def copy_all_topics(self):
        """Copy all topics to clipboard."""
        if not self.generated_topics:
            messagebox.showwarning("No Topics", "No topics to copy!")
            return
        
        topics_text = "\n".join([f"{i}. {topic['title']}" for i, topic in enumerate(self.generated_topics, 1)])
        
        self.tab_frame.clipboard_clear()
        self.tab_frame.clipboard_append(topics_text)
        
        messagebox.showinfo("Copied", f"All {len(self.generated_topics)} topics copied to clipboard!")

    def clear_topics(self):
        """Clear all generated topics."""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all topics?"):
            # Clear topics
            self.generated_topics = []
            
            # Clear display
            for widget in self.topics_results_frame.winfo_children():
                widget.destroy()
            
            # Disable export buttons
            self.export_topics_btn.configure(state="disabled")
            self.copy_all_btn.configure(state="disabled")
            self.clear_topics_btn.configure(state="disabled")
            
            messagebox.showinfo("Cleared", "All topics cleared!")

    # Tab manager interface
    def show(self):
        """Show the tab."""
        self.tab_frame.grid(row=0, column=0, sticky="nsew")
        
    def hide(self):
        """Hide the tab."""
        self.tab_frame.grid_forget()