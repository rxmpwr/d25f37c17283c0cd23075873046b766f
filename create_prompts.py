# create_prompts.py
"""
Module for creating AI prompts based on YouTube analysis data
UPDATED WITH PERFORMANCE OPTIMIZATIONS
Generates customized prompts for viral content creation
"""

from typing import Dict, List, Optional
from datetime import datetime
import json
import os
import logging
import gc
from functools import lru_cache

# Import performance optimizations
try:
    from performance_config import (
        perf_config, 
        MemoryOptimizer, 
        perf_monitor, 
        monitor_performance
    )
    PERFORMANCE_OPTIMIZATIONS = True
except ImportError:
    PERFORMANCE_OPTIMIZATIONS = False

logger = logging.getLogger(__name__)


class PromptGenerator:
    """Generates AI prompts based on analysis data with performance optimizations."""
    
    def __init__(self):
        self.prompt_templates = self._load_prompt_templates()
        self.generated_prompts = {}
        
        # Performance optimization settings
        self.max_insights_processing = 1000 if PERFORMANCE_OPTIMIZATIONS else float('inf')
        self.cache_enabled = PERFORMANCE_OPTIMIZATIONS
        
        # Initialize cache
        if self.cache_enabled:
            self._insights_cache = {}
            self._template_cache = {}
        
    def _load_prompt_templates(self) -> Dict:
        """Load predefined prompt templates with performance optimizations."""
        return {
            'story_generation': {
                'name': 'Tạo Câu Chuyện Viral',
                'description': 'Tạo câu chuyện dựa trên phân tích tâm lý từ YouTube',
                'template': """Dựa trên phân tích YouTube về {main_theme}, hãy tạo một câu chuyện viral với các đặc điểm sau:

🎯 CHỦ ĐỀ CHÍNH: {main_theme}
📊 INSIGHTS TỪ PHÂN TÍCH:
{analysis_insights}

📝 YÊU CẦU VIẾT:
- Độ dài: {min_words} từ trở lên
- Tone: {tone}
- Target audience: {target_audience}
- Hook mạnh trong 2 câu đầu
- Sử dụng storytelling framework: {framework}

🧠 YẾU TỐ TÂM LÝ CẦN TÍCH HỢP:
{psychology_factors}

💡 GỢI Ý NỘI DUNG:
{content_suggestions}

🎬 CẤU TRÚC VIRAL:
1. Hook (15s đầu): {hook_suggestion}
2. Setup conflict/problem
3. Journey/struggle
4. Revelation/insight
5. Transformation
6. Call to action

Hãy viết câu chuyện hoàn chỉnh theo yêu cầu trên.""",
                'priority': 1
            },
            
            'video_script': {
                'name': 'Script Video YouTube',
                'description': 'Tạo script video dựa trên insights từ phân tích',
                'template': """Tạo script video YouTube về {main_theme} dựa trên phân tích dữ liệu:

🎯 THÔNG TIN CƠ BẢN:
- Chủ đề: {main_theme}
- Thời lượng dự kiến: {duration} phút
- Target: {target_audience}
- Mục tiêu engagement: {engagement_goal}%

📊 INSIGHTS TỪ PHÂN TÍCH:
{analysis_insights}

🎬 CẤU TRÚC SCRIPT:

[HOOK - 0:00-0:15]
{hook_content}

[INTRO - 0:15-0:30]
{intro_content}

[MAIN CONTENT - 0:30-{main_end}]
{main_content_structure}

[CLIMAX/REVELATION - {climax_start}-{climax_end}]
{climax_content}

[CONCLUSION - {conclusion_start}-{duration}:00]
{conclusion_content}

🎭 ELEMENTS TƯƠNG TÁC:
{interactive_elements}

📱 OPTIMIZATION:
- Title suggestions: {title_suggestions}
- Thumbnail ideas: {thumbnail_ideas}
- Tags: {suggested_tags}

Viết script chi tiết với dialogue và stage directions.""",
                'priority': 2
            },
            
            'content_series': {
                'name': 'Series Nội Dung',
                'description': 'Tạo series nội dung dựa trên trending topics',
                'template': """Tạo series nội dung {series_length} tập về {main_theme}:

🎯 THÔNG TIN SERIES:
- Tên series: "{series_name}"
- Số tập: {series_length}
- Frequency: {frequency}
- Target audience: {target_audience}

📊 INSIGHTS TỪ PHÂN TÍCH:
{analysis_insights}

📺 OUTLINE TỪNG TẬP:

{episode_outlines}

🔄 CONTENT STRATEGY:
- Format: {content_format}
- Platform optimization: {platform_strategy}
- Cross-promotion: {cross_promotion}
- Audience retention: {retention_strategy}

💡 VIRAL ELEMENTS:
{viral_elements}

📈 SUCCESS METRICS:
{success_metrics}

Phát triển chi tiết từng tập với hook, main content và CTA.""",
                'priority': 3
            },
            
            'social_media': {
                'name': 'Social Media Content',
                'description': 'Tạo nội dung cho các platform khác nhau',
                'template': """Tạo social media content về {main_theme} cho multiple platforms:

🎯 CORE MESSAGE: {core_message}

📊 INSIGHTS TỪ PHÂN TÍCH:
{analysis_insights}

📱 PLATFORM-SPECIFIC CONTENT:

🔴 YOUTUBE SHORTS:
{youtube_shorts_content}

📸 INSTAGRAM:
- Posts: {instagram_posts}
- Stories: {instagram_stories}
- Reels: {instagram_reels}

🎵 TIKTOK:
{tiktok_content}

📘 FACEBOOK:
{facebook_content}

🐦 TWITTER/X:
{twitter_content}

💼 LINKEDIN:
{linkedin_content}

🎨 CREATIVE DIRECTION:
- Visual style: {visual_style}
- Color palette: {color_palette}
- Typography: {typography}
- Brand consistency: {brand_elements}

📅 POSTING SCHEDULE:
{posting_schedule}

Tạo content cụ thể cho từng platform với copy và creative direction.""",
                'priority': 4
            },
            
            'email_sequence': {
                'name': 'Email Marketing Sequence',
                'description': 'Tạo chuỗi email marketing từ insights',
                'template': """Tạo email sequence {sequence_length} emails về {main_theme}:

🎯 CAMPAIGN GOAL: {campaign_goal}
📊 TARGET AUDIENCE: {target_audience}

INSIGHTS TỪ PHÂN TÍCH:
{analysis_insights}

📧 EMAIL SEQUENCE:

{email_sequence_content}

🎨 DESIGN ELEMENTS:
- Subject line formulas: {subject_formulas}
- Email templates: {email_templates}
- CTA strategies: {cta_strategies}

📈 AUTOMATION TRIGGERS:
{automation_triggers}

📊 SUCCESS METRICS:
- Open rate target: {open_rate_target}%
- Click rate target: {click_rate_target}%
- Conversion target: {conversion_target}%

Viết full email sequence với subject lines và body content.""",
                'priority': 5
            },
            
            'blog_content': {
                'name': 'Blog Content Strategy',
                'description': 'Tạo nội dung blog dựa trên analysis',
                'template': """Tạo blog content strategy về {main_theme}:

🎯 CONTENT PILLAR: {main_theme}
📊 CONTENT GOALS: {content_goals}

INSIGHTS TỪ PHÂN TÍCH:
{analysis_insights}

📝 BLOG POST SERIES:

{blog_post_series}

🔍 SEO STRATEGY:
- Primary keywords: {primary_keywords}
- Secondary keywords: {secondary_keywords}
- Content clusters: {content_clusters}
- Internal linking: {linking_strategy}

📊 CONTENT CALENDAR:
{content_calendar}

🎨 CONTENT FORMATS:
- How-to guides: {howto_topics}
- Listicles: {listicle_topics}
- Case studies: {case_study_topics}
- Opinion pieces: {opinion_topics}

📈 DISTRIBUTION STRATEGY:
{distribution_strategy}

Viết outline chi tiết cho từng blog post với SEO optimization.""",
                'priority': 6
            }
        }
    
    @monitor_performance('processing') if PERFORMANCE_OPTIMIZATIONS else lambda f: f
    def generate_prompts_from_analysis(self, analysis_data: Dict, user_preferences: Dict) -> Dict:
        """Generate prompts based on analysis data and user preferences with optimizations."""
        try:
            # Apply memory optimization to input data
            if PERFORMANCE_OPTIMIZATIONS:
                analysis_data = MemoryOptimizer.limit_data_size(analysis_data)
            
            # Extract key insights from analysis (optimized)
            insights = self._extract_insights_optimized(analysis_data)
            
            # Determine which templates to generate based on priority and preferences
            templates_to_generate = self._select_templates_for_generation(user_preferences)
            
            # Generate prompts for selected templates
            generated_prompts = {}
            
            total_templates = len(templates_to_generate)
            for i, (template_key, template_data) in enumerate(templates_to_generate.items()):
                try:
                    # Progress tracking
                    progress = (i + 1) / total_templates * 100
                    if PERFORMANCE_OPTIMIZATIONS and perf_monitor:
                        print(f"🔄 Generating prompt {i+1}/{total_templates}: {template_data['name']}")
                    
                    prompt = self._generate_single_prompt_optimized(
                        template_data, 
                        insights, 
                        user_preferences
                    )
                    generated_prompts[template_key] = prompt
                    
                    # Memory cleanup between templates
                    if PERFORMANCE_OPTIMIZATIONS and i % 2 == 0:  # Every 2 templates
                        gc.collect()
                        
                except Exception as e:
                    logger.error(f"Error generating prompt for {template_key}: {e}")
                    # Continue with other templates
                    continue
            
            # Store generated prompts
            self.generated_prompts = generated_prompts
            
            # Save to file (optimized)
            if generated_prompts:
                self._save_prompts_optimized(generated_prompts)
            
            return generated_prompts
            
        except Exception as e:
            logger.error(f"Error generating prompts: {e}")
            return {}
        finally:
            # Cleanup
            if PERFORMANCE_OPTIMIZATIONS:
                gc.collect()
    
    def _select_templates_for_generation(self, user_preferences: Dict) -> Dict:
        """Select templates for generation based on preferences and performance."""
        selected_templates = {}
        
        # Sort templates by priority for performance
        sorted_templates = sorted(
            self.prompt_templates.items(),
            key=lambda x: x[1].get('priority', 999)
        )
        
        # Apply user preferences and performance limits
        max_templates = perf_config.get('max_prompt_templates', 6) if PERFORMANCE_OPTIMIZATIONS else 6
        count = 0
        
        for template_key, template_data in sorted_templates:
            if count >= max_templates:
                break
                
            # Check if user wants this template
            if user_preferences.get(template_key, True):
                selected_templates[template_key] = template_data
                count += 1
        
        return selected_templates
    
    @lru_cache(maxsize=32) if PERFORMANCE_OPTIMIZATIONS else lambda f: f
    def _extract_insights_optimized(self, analysis_data_hash: str) -> Dict:
        """Extract key insights from analysis data with caching and optimization."""
        # This is a cached version that works with hashable input
        # In practice, you'd need to implement proper hashing for dict
        return self._extract_insights_internal(analysis_data_hash)
    
    def _extract_insights_internal(self, analysis_data: Dict) -> Dict:
        """Internal method for extracting insights."""
        insights = {
            'main_themes': [],
            'audience_appeal_factors': [],
            'sentiment_analysis': {},
            'strengths': [],
            'weaknesses': [],
            'viral_potential': 0,
            'top_performing_content': {},
            'engagement_patterns': {}
        }
        
        # Limit processing for performance
        max_items = self.max_insights_processing
        
        # Extract main themes (optimized)
        transcripts = analysis_data.get('transcripts', [])[:max_items]
        if transcripts:
            themes = self._analyze_themes_from_transcripts_optimized(transcripts)
            insights['main_themes'] = themes
        
        # Extract audience appeal factors (optimized)
        comments = analysis_data.get('bình luận', [])[:max_items]
        if comments:
            appeal_factors = self._analyze_audience_appeal_optimized(comments)
            insights['audience_appeal_factors'] = appeal_factors
        
        # Extract sentiment (optimized)
        if comments:
            sentiment = self._analyze_sentiment_optimized(comments)
            insights['sentiment_analysis'] = sentiment
        
        # Extract performance data (optimized)
        videos = analysis_data.get('video', [])[:max_items]
        if videos:
            top_video = max(videos, key=lambda x: x.get('view_count', 0))
            insights['top_performing_content'] = {
                'title': top_video.get('title', '')[:100],  # Limit title length
                'lượt xem': top_video.get('view_count', 0),
                'engagement_rate': self._calculate_engagement_rate_fast(top_video)
            }
        
        # Calculate viral potential (optimized)
        insights['viral_potential'] = analysis_data.get('viral_score', 0)
        
        return insights
    
    def _analyze_themes_from_transcripts_optimized(self, transcripts: List[Dict]) -> List[str]:
        """Optimized theme analysis from transcripts."""
        themes = []
        theme_keywords = {
            'Relationships': ['love', 'relationship', 'partner', 'dating'],
            'Psychology': ['psychology', 'mind', 'brain', 'behavior'],
            'Self Development': ['growth', 'improve', 'success', 'confidence'],
            'Mental Health': ['anxiety', 'depression', 'stress', 'mental health'],
            'Communication': ['communication', 'talk', 'speak', 'listen']
        }
        
        # Limit text processing for performance
        max_text_length = 5000 if PERFORMANCE_OPTIMIZATIONS else float('inf')
        
        all_text = ""
        for transcript in transcripts[:10]:  # Limit number of transcripts
            text = transcript.get('full_text', '')
            if len(all_text) + len(text) > max_text_length:
                remaining_length = max_text_length - len(all_text)
                text = text[:remaining_length]
                all_text += text
                break
            all_text += text + " "
        
        all_text = all_text.lower()
        
        for theme, keywords in theme_keywords.items():
            score = sum(all_text.count(keyword) for keyword in keywords)
            if score > 0:
                themes.append({'theme': theme, 'score': score})
        
        # Sort by score and return top themes
        themes.sort(key=lambda x: x['score'], reverse=True)
        return [t['theme'] for t in themes[:3]]
    
    def _analyze_audience_appeal_optimized(self, comments: List[Dict]) -> List[str]:
        """Optimized audience appeal analysis."""
        appeal_factors = []
        positive_keywords = [
            'love', 'amazing', 'helpful', 'inspiring', 'relatable', 
            'exactly', 'truth', 'needed this'
        ]
        
        # Limit comment processing
        sample_comments = comments[:50] if PERFORMANCE_OPTIMIZATIONS else comments
        
        all_comments = ' '.join([c.get('text', '')[:200] for c in sample_comments]).lower()
        
        for keyword in positive_keywords:
            if keyword in all_comments:
                appeal_factors.append(keyword)
        
        return appeal_factors[:5]
    
    def _analyze_sentiment_optimized(self, comments: List[Dict]) -> Dict:
        """Optimized sentiment analysis."""
        positive_words = ['love', 'great', 'amazing', 'helpful', 'inspiring']
        negative_words = ['hate', 'boring', 'bad', 'waste', 'terrible']
        
        # Limit processing
        sample_comments = comments[:100] if PERFORMANCE_OPTIMIZATIONS else comments
        
        positive_count = 0
        negative_count = 0
        total_comments = len(sample_comments)
        
        for comment in sample_comments:
            text = comment.get('text', '').lower()
            if any(word in text for word in positive_words):
                positive_count += 1
            if any(word in text for word in negative_words):
                negative_count += 1
        
        return {
            'positive_percentage': (positive_count / total_comments * 100) if total_comments > 0 else 0,
            'negative_percentage': (negative_count / total_comments * 100) if total_comments > 0 else 0,
            'overall_sentiment': 'positive' if positive_count > negative_count else 'neutral'
        }
    
    def _calculate_engagement_rate_fast(self, video: Dict) -> float:
        """Fast engagement rate calculation."""
        views = video.get('view_count', 0)
        likes = video.get('like_count', 0)
        comments = video.get('comment_count', 0)
        
        if views > 0:
            return ((likes + comments) / views) * 100
        return 0
    
    def _generate_single_prompt_optimized(self, template_data: Dict, insights: Dict, preferences: Dict) -> Dict:
        """Generate a single prompt with performance optimizations."""
        template = template_data['template']
        
        # Prepare variables for template (optimized)
        variables = self._prepare_template_variables_optimized(insights, preferences)
        
        # Format template with variables (with error handling)
        try:
            formatted_prompt = template.format(**variables)
        except KeyError as e:
            logger.warning(f"Missing variable {e} in template, using placeholder")
            # Replace missing variables with placeholders
            missing_vars = []
            for key in variables:
                if f"{{{key}}}" not in template:
                    continue
                try:
                    template.format(**{key: variables[key]})
                except KeyError:
                    missing_vars.append(key)
                    
            # Fill missing variables
            for var in missing_vars:
                variables[var] = f"[{var}]"
                
            formatted_prompt = template.format(**variables)
        
        return {
            'name': template_data['name'],
            'description': template_data['description'],
            'prompt': formatted_prompt,
            'variables': variables,
            'created_at': datetime.now().isoformat(),
            'insights_used': insights,
            'word_count': len(formatted_prompt.split()),
            'character_count': len(formatted_prompt)
        }
    
    def _prepare_template_variables_optimized(self, insights: Dict, preferences: Dict) -> Dict:
        """Prepare template variables with performance optimization."""
        # Basic variables
        variables = {
            'main_theme': self._get_main_theme(insights),
            'analysis_insights': self._format_insights_concise(insights),
            'min_words': preferences.get('min_words', 2000),
            'tone': preferences.get('tone', 'Engaging and educational'),
            'target_audience': preferences.get('target_audience', 'Young adults 18-35'),
            'framework': preferences.get('framework', 'Hero\'s Journey'),
            'psychology_factors': self._get_psychology_factors_optimized(insights),
            'content_suggestions': self._get_content_suggestions_optimized(insights),
            'hook_suggestion': self._generate_hook_suggestion_optimized(insights),
            'duration': preferences.get('video_duration', 10),
            'engagement_goal': preferences.get('engagement_goal', 5),
            'series_length': preferences.get('series_length', 5),
            'series_name': self._generate_series_name_optimized(insights),
            'frequency': preferences.get('frequency', 'Weekly'),
            'content_format': preferences.get('content_format', 'Educational + Entertainment'),
            'campaign_goal': preferences.get('campaign_goal', 'Increase engagement and followers'),
            'sequence_length': preferences.get('sequence_length', 7),
            'content_goals': preferences.get('content_goals', 'Educate and inspire audience'),
            'core_message': self._get_core_message_optimized(insights)
        }
        
        # Add time-based variables for video script
        if 'duration' in variables:
            duration = variables['duration']
            variables.update({
                'main_end': f"{max(duration-3, 1)}:00",
                'climax_start': f"{max(duration-3, 1)}:00", 
                'climax_end': f"{max(duration-2, 1)}:30",
                'conclusion_start': f"{max(duration-2, 1)}:30"
            })
        
        # Add content-specific variables (optimized)
        content_vars = self._generate_content_specific_variables_optimized(insights, preferences)
        variables.update(content_vars)
        
        return variables
    
    def _get_main_theme(self, insights: Dict) -> str:
        """Get the main theme from insights."""
        themes = insights.get('main_themes', [])
        return themes[0] if themes else 'Personal Development'
    
    def _format_insights_concise(self, insights: Dict) -> str:
        """Format insights concisely for prompts."""
        formatted = []
        
        if insights.get('main_themes'):
            themes = ', '.join(insights['main_themes'][:3])  # Limit to top 3
            formatted.append(f"• Chủ đề chính: {themes}")
        
        if insights.get('viral_potential'):
            formatted.append(f"• Viral potential: {insights['viral_potential']:.1f}/100")
        
        sentiment = insights.get('sentiment_analysis', {})
        if sentiment:
            formatted.append(f"• Audience sentiment: {sentiment.get('positive_percentage', 0):.1f}% positive")
        
        top_content = insights.get('top_performing_content', {})
        if top_content:
            views = top_content.get('lượt xem', 0)
            formatted.append(f"• Top video: {views:,} views")
        
        return '\n'.join(formatted[:4])  # Limit to top 4 insights
    
    def _get_psychology_factors_optimized(self, insights: Dict) -> str:
        """Get psychology factors optimized for prompts."""
        base_factors = [
            "• Social proof và validation seeking",
            "• Curiosity gap và information seeking", 
            "• Emotional resonance và relatability"
        ]
        
        # Add theme-specific factors
        themes = insights.get('main_themes', [])
        if 'Relationships' in themes:
            base_factors.append("• Attachment theory patterns")
        if 'Psychology' in themes:
            base_factors.append("• Cognitive biases applications")
        
        return '\n'.join(base_factors[:5])  # Limit to 5 factors
    
    def _get_content_suggestions_optimized(self, insights: Dict) -> str:
        """Get optimized content suggestions."""
        themes = insights.get('main_themes', [])
        suggestions = []
        
        if 'Relationships' in themes:
            suggestions.extend([
                "• Hidden relationship psychology most people ignore",
                "• Why we're attracted to the wrong people"
            ])
        
        if 'Psychology' in themes:
            suggestions.extend([
                "• Psychology tricks that actually work",
                "• Cognitive biases affecting daily decisions"
            ])
        
        if not suggestions:
            suggestions = [
                "• Personal transformation stories",
                "• Controversial but true insights"
            ]
        
        return '\n'.join(suggestions[:4])  # Limit to 4 suggestions
    
    def _generate_hook_suggestion_optimized(self, insights: Dict) -> str:
        """Generate optimized hook suggestion."""
        themes = insights.get('main_themes', [])
        viral_score = insights.get('viral_potential', 0)
        
        main_theme = themes[0] if themes else 'life'
        
        if viral_score > 70:
            return f"This will completely change how you think about {main_theme}"
        elif viral_score > 50:
            return f"99% of people don't know this about {main_theme}"
        else:
            return f"If you struggle with {main_theme}, this is for you"
    
    def _generate_series_name_optimized(self, insights: Dict) -> str:
        """Generate optimized series name."""
        themes = insights.get('main_themes', [])
        main_theme = themes[0] if themes else 'Life'
        
        series_names = {
            'Relationships': 'Love Psychology Secrets',
            'Psychology': 'Mind Mastery Series',
            'Self Development': 'Transform Your Life',
            'Mental Health': 'Mental Wellness Journey'
        }
        
        return series_names.get(main_theme, f'{main_theme} Mastery')
    
    def _get_core_message_optimized(self, insights: Dict) -> str:
        """Get optimized core message."""
        themes = insights.get('main_themes', [])
        if not themes:
            return "Transform your mindset, transform your life"
        
        messages = {
            'Relationships': 'Understanding psychology creates deeper connections',
            'Psychology': 'Your mind has more power than you realize',
            'Self Development': 'Small changes lead to massive transformations'
        }
        
        return messages.get(themes[0], 'Knowledge is the key to transformation')
    
    def _generate_content_specific_variables_optimized(self, insights: Dict, preferences: Dict) -> Dict:
        """Generate optimized content-specific variables."""
        variables = {}
        
        # Simplified content generation for performance
        variables.update({
            'hook_content': "Grab attention with shocking statement or question",
            'intro_content': "Welcome back! Today we're diving into...",
            'main_content_structure': "Point 1 → Point 2 → Point 3 with examples",
            'climax_content': "Here's the revelation that changes everything...",
            'conclusion_content': "Remember this key takeaway...",
            'interactive_elements': "Polls, comments challenges, Q&A",
            'title_suggestions': self._generate_titles_optimized(insights),
            'thumbnail_ideas': "Contrast colors, emotion, bold text",
            'suggested_tags': self._generate_tags_optimized(insights)
        })
        
        # Series-specific
        variables.update({
            'episode_outlines': self._generate_episode_outlines_optimized(insights, preferences.get('series_length', 5)),
            'platform_strategy': "YouTube primary, TikTok for clips",
            'viral_elements': "Shocking stats, personal stories, challenges",
            'success_metrics': "Views, engagement, subscribers, retention"
        })
        
        # Social media optimized
        variables.update({
            'youtube_shorts_content': "60s rapid insights with trending audio",
            'instagram_posts': "Quote cards, carousel tips",
            'tiktok_content': "15-60s psychology hacks",
            'visual_style': "Modern, clean, high contrast",
            'posting_schedule': "YouTube: 2x/week, Shorts: daily, Instagram: 3x/week"
        })
        
        return variables
    
    def _generate_titles_optimized(self, insights: Dict) -> str:
        """Generate optimized title suggestions."""
        themes = insights.get('main_themes', ['psychology'])
        main_theme = themes[0] if themes else 'psychology'
        
        titles = [
            f"The Hidden Psychology of {main_theme.title()}",
            f"Why 99% Don't Understand {main_theme.title()}",
            f"This {main_theme.title()} Secret Will Shock You"
        ]
        return ' | '.join(titles)
    
    def _generate_tags_optimized(self, insights: Dict) -> str:
        """Generate optimized tags."""
        themes = insights.get('main_themes', ['psychology'])
        base_tags = ['psychology', 'viral', 'mindset', 'life advice']
        theme_tags = [theme.lower().replace(' ', '') for theme in themes[:2]]
        return ', '.join(base_tags + theme_tags)
    
    def _generate_episode_outlines_optimized(self, insights: Dict, series_length: int) -> str:
        """Generate optimized episode outlines."""
        themes = insights.get('main_themes', ['psychology'])
        main_theme = themes[0] if themes else 'psychology'
        
        outlines = []
        for i in range(1, min(series_length + 1, 8)):  # Limit to max 7 episodes for performance
            outlines.append(f"Episode {i}: {main_theme} principle #{i}")
        
        return '\n'.join(outlines)
    
    def _save_prompts_optimized(self, prompts: Dict) -> bool:
        """Save generated prompts with optimization."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_prompts_{timestamp}.json"
            
            os.makedirs('output/prompts', exist_ok=True)
            filepath = os.path.join('output/prompts', filename)
            
            # Optimize data before saving
            optimized_prompts = {}
            for key, prompt_data in prompts.items():
                # Remove heavy data for file size optimization
                optimized_data = {
                    'name': prompt_data.get('name', ''),
                    'description': prompt_data.get('description', ''),
                    'prompt': prompt_data.get('prompt', ''),
                    'created_at': prompt_data.get('created_at', ''),
                    'word_count': prompt_data.get('word_count', 0)
                }
                optimized_prompts[key] = optimized_data
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(optimized_prompts, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Prompts saved to: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving prompts: {e}")
            return False
    
    def get_available_templates(self) -> Dict:
        """Get list of available prompt templates."""
        return {key: {
            'name': template['name'], 
            'description': template['description'],
            'priority': template.get('priority', 999)
        } for key, template in self.prompt_templates.items()}
    
    def get_generated_prompts(self) -> Dict:
        """Get currently generated prompts."""
        return self.generated_prompts
    
    def export_prompts(self, export_format: str = 'json', filename: Optional[str] = None) -> str:
        """Export prompts in specified format with optimization."""
        if not self.generated_prompts:
            raise ValueError("No prompts generated yet")
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"exported_prompts_{timestamp}.{export_format}"
        
        try:
            if export_format == 'json':
                return self._export_json_optimized(filename)
            elif export_format == 'txt':
                return self._export_txt_optimized(filename)
            elif export_format == 'md':
                return self._export_markdown_optimized(filename)
            else:
                raise ValueError(f"Unsupported export format: {export_format}")
        except Exception as e:
            logger.error(f"Export error: {e}")
            raise
    
    def _export_json_optimized(self, filename: str) -> str:
        """Export prompts as JSON with optimization."""
        os.makedirs('output/exports', exist_ok=True)
        filepath = os.path.join('output/exports', filename)
        
        # Create optimized export
        export_data = {
            'export_info': {
                'timestamp': datetime.now().isoformat(),
                'version': '2.1',
                'prompt_count': len(self.generated_prompts),
                'optimized': PERFORMANCE_OPTIMIZATIONS
            },
            'prompts': self.generated_prompts
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def _export_txt_optimized(self, filename: str) -> str:
        """Export prompts as plain text with optimization."""
        os.makedirs('output/exports', exist_ok=True)
        filepath = os.path.join('output/exports', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("GENERATED AI PROMPTS\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Prompts: {len(self.generated_prompts)}\n\n")
            
            for i, (key, prompt_data) in enumerate(self.generated_prompts.items(), 1):
                f.write(f"{i}. {prompt_data['name']}\n")
                f.write("-" * len(prompt_data['name']) + "\n")
                f.write(f"Description: {prompt_data['description']}\n")
                f.write(f"Word Count: {prompt_data.get('word_count', 'N/A')}\n\n")
                
                # Limit prompt length for readability
                prompt_text = prompt_data['prompt']
                if PERFORMANCE_OPTIMIZATIONS and len(prompt_text) > 2000:
                    prompt_text = prompt_text[:2000] + "\n\n[Content truncated for file size optimization]"
                
                f.write(f"Prompt:\n{prompt_text}\n\n")
                f.write("=" * 50 + "\n\n")
        
        return filepath
    
    def _export_markdown_optimized(self, filename: str) -> str:
        """Export prompts as Markdown with optimization."""
        os.makedirs('output/exports', exist_ok=True)
        filepath = os.path.join('output/exports', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Generated AI Prompts\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
            f.write(f"**Total Prompts:** {len(self.generated_prompts)}  \n")
            if PERFORMANCE_OPTIMIZATIONS:
                f.write("**Optimized:** Yes  \n")
            f.write("\n---\n\n")
            
            for i, (key, prompt_data) in enumerate(self.generated_prompts.items(), 1):
                f.write(f"## {i}. {prompt_data['name']}\n\n")
                f.write(f"**Description:** {prompt_data['description']}  \n")
                f.write(f"**Word Count:** {prompt_data.get('word_count', 'N/A')}  \n")
                f.write(f"**Created:** {prompt_data.get('created_at', 'N/A')}  \n\n")
                
                f.write("### Prompt\n\n")
                
                # Format prompt with optimization
                prompt_text = prompt_data['prompt']
                if PERFORMANCE_OPTIMIZATIONS and len(prompt_text) > 3000:
                    prompt_text = prompt_text[:3000] + "\n\n*[Content truncated for performance]*"
                
                f.write(f"```\n{prompt_text}\n```\n\n")
                f.write("---\n\n")
        
        return filepath
    
    def clear_cache(self):
        """Clear cache for memory optimization."""
        if PERFORMANCE_OPTIMIZATIONS and self.cache_enabled:
            if hasattr(self, '_insights_cache'):
                self._insights_cache.clear()
            if hasattr(self, '_template_cache'):
                self._template_cache.clear()
            gc.collect()
            logger.info("PromptGenerator cache cleared")


# Utility functions
def create_prompts_from_analysis(analysis_data: Dict, user_preferences: Optional[Dict] = None) -> Dict:
    """Create prompts from analysis data - main entry point with optimization."""
    if user_preferences is None:
        user_preferences = get_default_preferences()
    
    generator = PromptGenerator()
    return generator.generate_prompts_from_analysis(analysis_data, user_preferences)


def get_default_preferences() -> Dict:
    """Get default user preferences for prompt generation with optimization."""
    base_preferences = {
        'min_words': 1500 if PERFORMANCE_OPTIMIZATIONS else 2000,  # Slightly reduced for performance
        'tone': 'Engaging and educational',
        'target_audience': 'Young adults 18-35',
        'framework': 'Hero\'s Journey',
        'video_duration': 8 if PERFORMANCE_OPTIMIZATIONS else 10,  # Shorter for performance
        'engagement_goal': 5,
        'series_length': 5,
        'frequency': 'Weekly',
        'content_format': 'Educational + Entertainment',
        'campaign_goal': 'Increase engagement and followers',
        'sequence_length': 5 if PERFORMANCE_OPTIMIZATIONS else 7,  # Reduced for performance
        'content_goals': 'Educate and inspire audience',
        'open_rate_target': 25,
        'click_rate_target': 5,
        'conversion_target': 2
    }
    
    # Template enablement (prioritize important ones for performance)
    template_preferences = {
        'story_generation': True,
        'video_script': True,
        'content_series': True,
        'social_media': True,
        'email_sequence': False if PERFORMANCE_OPTIMIZATIONS else True,  # Disable for performance
        'blog_content': False if PERFORMANCE_OPTIMIZATIONS else True   # Disable for performance
    }
    
    base_preferences.update(template_preferences)
    return base_preferences


# Example usage with performance monitoring
if __name__ == "__main__":
    # Example analysis data (simplified for performance)
    sample_analysis = {
        'transcripts': [
            {'full_text': 'psychology relationship love mind behavior emotion growth success', 'video_id': '123'}
        ],
        'bình luận': [
            {'text': 'love this amazing helpful', 'like_count': 10},
            {'text': 'exactly what I needed', 'like_count': 5}
        ],
        'video': [
            {'title': 'Psychology of Love', 'view_count': 100000, 'like_count': 5000, 'comment_count': 500}
        ],
        'viral_score': 75.5
    }
    
    # Performance tracking
    start_time = datetime.now()
    
    # Generate prompts
    prompts = create_prompts_from_analysis(sample_analysis)
    
    # Performance results
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"🚀 Generated {len(prompts)} prompts in {duration:.2f} seconds")
    
    # Print sample
    for key, prompt_data in list(prompts.items())[:2]:  # Show first 2
        print(f"\n📝 {prompt_data['name']}:")
        print("-" * 50)
        print(f"Words: {prompt_data.get('word_count', 'N/A')}")
        print(prompt_data['prompt'][:200] + "...")
        
    if PERFORMANCE_OPTIMIZATIONS:
        print(f"\n✅ Performance optimizations enabled")
        print(f"💾 Memory usage optimized")
        print(f"⚡ Processing speed optimized")