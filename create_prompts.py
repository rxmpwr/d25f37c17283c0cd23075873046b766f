# create_prompts.py
"""
Module for creating AI prompts based on YouTube analysis data
Generates customized prompts for viral content creation
"""

from typing import Dict, List, Optional
from datetime import datetime
import json
import os
import logging

logger = logging.getLogger(__name__)


class PromptGenerator:
    """Generates AI prompts based on analysis data."""
    
    def __init__(self):
        self.prompt_templates = self._load_prompt_templates()
        self.generated_prompts = {}
        
    def _load_prompt_templates(self) -> Dict:
        """Load predefined prompt templates."""
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

Hãy viết câu chuyện hoàn chỉnh theo yêu cầu trên."""
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

Viết script chi tiết với dialogue và stage directions."""
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

Phát triển chi tiết từng tập với hook, main content và CTA."""
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

Tạo content cụ thể cho từng platform với copy và creative direction."""
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

Viết full email sequence với subject lines và body content."""
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

Viết outline chi tiết cho từng blog post với SEO optimization."""
            }
        }
    
    def generate_prompts_from_analysis(self, analysis_data: Dict, user_preferences: Dict) -> Dict:
        """Generate prompts based on analysis data and user preferences."""
        try:
            # Extract key insights from analysis
            insights = self._extract_insights(analysis_data)
            
            # Generate prompts for each template
            generated_prompts = {}
            
            for template_key, template_data in self.prompt_templates.items():
                if user_preferences.get(template_key, True):  # Generate if enabled
                    prompt = self._generate_single_prompt(
                        template_data, 
                        insights, 
                        user_preferences
                    )
                    generated_prompts[template_key] = prompt
            
            # Store generated prompts
            self.generated_prompts = generated_prompts
            
            # Save to file
            self._save_prompts(generated_prompts)
            
            return generated_prompts
            
        except Exception as e:
            logger.error(f"Error generating prompts: {e}")
            return {}
    
    def _extract_insights(self, analysis_data: Dict) -> Dict:
        """Extract key insights from analysis data."""
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
        
        # Extract main themes
        transcripts = analysis_data.get('transcripts', [])
        if transcripts:
            # Analyze themes from transcripts
            themes = self._analyze_themes_from_transcripts(transcripts)
            insights['main_themes'] = themes
        
        # Extract audience appeal factors
        comments = analysis_data.get('comments', [])
        if comments:
            appeal_factors = self._analyze_audience_appeal(comments)
            insights['audience_appeal_factors'] = appeal_factors
        
        # Extract sentiment
        if comments:
            sentiment = self._analyze_sentiment(comments)
            insights['sentiment_analysis'] = sentiment
        
        # Extract performance data
        videos = analysis_data.get('videos', [])
        if videos:
            top_video = max(videos, key=lambda x: x.get('view_count', 0))
            insights['top_performing_content'] = {
                'title': top_video.get('title', ''),
                'views': top_video.get('view_count', 0),
                'engagement_rate': self._calculate_engagement_rate(top_video)
            }
        
        # Calculate viral potential
        insights['viral_potential'] = analysis_data.get('viral_score', 0)
        
        return insights
    
    def _generate_single_prompt(self, template_data: Dict, insights: Dict, preferences: Dict) -> Dict:
        """Generate a single prompt from template and insights."""
        template = template_data['template']
        
        # Prepare variables for template
        variables = {
            'main_theme': self._get_main_theme(insights),
            'analysis_insights': self._format_insights(insights),
            'min_words': preferences.get('min_words', 2000),
            'tone': preferences.get('tone', 'Engaging and educational'),
            'target_audience': preferences.get('target_audience', 'Young adults 18-35'),
            'framework': preferences.get('framework', 'Hero\'s Journey'),
            'psychology_factors': self._get_psychology_factors(insights),
            'content_suggestions': self._get_content_suggestions(insights),
            'hook_suggestion': self._generate_hook_suggestion(insights),
            'duration': preferences.get('video_duration', 10),
            'engagement_goal': preferences.get('engagement_goal', 5),
            'series_length': preferences.get('series_length', 5),
            'series_name': self._generate_series_name(insights),
            'frequency': preferences.get('frequency', 'Weekly'),
            'content_format': preferences.get('content_format', 'Educational + Entertainment'),
            'campaign_goal': preferences.get('campaign_goal', 'Increase engagement and followers'),
            'sequence_length': preferences.get('sequence_length', 7),
            'content_goals': preferences.get('content_goals', 'Educate and inspire audience'),
            'core_message': self._get_core_message(insights)
        }
        
        # Add time-based variables for video script
        if 'duration' in variables:
            duration = variables['duration']
            variables.update({
                'main_end': f"{duration-3}:00",
                'climax_start': f"{duration-3}:00",
                'climax_end': f"{duration-1}:30",
                'conclusion_start': f"{duration-1}:30"
            })
        
        # Add content-specific variables
        variables.update(self._generate_content_specific_variables(insights, preferences))
        
        # Format template with variables
        try:
            formatted_prompt = template.format(**variables)
        except KeyError as e:
            logger.warning(f"Missing variable {e} in template, using placeholder")
            # Replace missing variables with placeholders
            for key in variables:
                template = template.replace(f"{{{key}}}", str(variables.get(key, f"[{key}]")))
            formatted_prompt = template
        
        return {
            'name': template_data['name'],
            'description': template_data['description'],
            'prompt': formatted_prompt,
            'variables': variables,
            'created_at': datetime.now().isoformat(),
            'insights_used': insights
        }
    
    def _analyze_themes_from_transcripts(self, transcripts: List[Dict]) -> List[str]:
        """Analyze main themes from transcripts."""
        themes = []
        theme_keywords = {
            'Relationships': ['love', 'relationship', 'partner', 'dating', 'marriage'],
            'Psychology': ['psychology', 'mind', 'brain', 'behavior', 'emotion'],
            'Self Development': ['growth', 'improve', 'success', 'confidence', 'goal'],
            'Mental Health': ['anxiety', 'depression', 'stress', 'mental health', 'therapy'],
            'Communication': ['communication', 'talk', 'speak', 'listen', 'conversation'],
            'Motivation': ['motivation', 'inspire', 'dream', 'purpose', 'passion']
        }
        
        all_text = ' '.join([t.get('full_text', '') for t in transcripts]).lower()
        
        for theme, keywords in theme_keywords.items():
            score = sum(all_text.count(keyword) for keyword in keywords)
            if score > 0:
                themes.append({'theme': theme, 'score': score})
        
        # Sort by score and return top themes
        themes.sort(key=lambda x: x['score'], reverse=True)
        return [t['theme'] for t in themes[:3]]
    
    def _analyze_audience_appeal(self, comments: List[Dict]) -> List[str]:
        """Analyze what appeals to audience from comments."""
        appeal_factors = []
        positive_keywords = [
            'love', 'amazing', 'helpful', 'inspiring', 'relatable', 
            'exactly', 'truth', 'needed this', 'life changing'
        ]
        
        all_comments = ' '.join([c.get('text', '') for c in comments]).lower()
        
        for keyword in positive_keywords:
            if keyword in all_comments:
                appeal_factors.append(keyword)
        
        return appeal_factors[:5]
    
    def _analyze_sentiment(self, comments: List[Dict]) -> Dict:
        """Analyze sentiment from comments."""
        positive_words = ['love', 'great', 'amazing', 'helpful', 'inspiring']
        negative_words = ['hate', 'boring', 'bad', 'waste', 'terrible']
        
        positive_count = 0
        negative_count = 0
        total_comments = len(comments)
        
        for comment in comments:
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
    
    def _calculate_engagement_rate(self, video: Dict) -> float:
        """Calculate engagement rate for a video."""
        views = video.get('view_count', 0)
        likes = video.get('like_count', 0)
        comments = video.get('comment_count', 0)
        
        if views > 0:
            return ((likes + comments) / views) * 100
        return 0
    
    def _get_main_theme(self, insights: Dict) -> str:
        """Get the main theme from insights."""
        themes = insights.get('main_themes', [])
        return themes[0] if themes else 'Personal Development'
    
    def _format_insights(self, insights: Dict) -> str:
        """Format insights for prompt inclusion."""
        formatted = []
        
        if insights.get('main_themes'):
            formatted.append(f"• Chủ đề chính: {', '.join(insights['main_themes'])}")
        
        if insights.get('viral_potential'):
            formatted.append(f"• Viral potential score: {insights['viral_potential']:.1f}/100")
        
        sentiment = insights.get('sentiment_analysis', {})
        if sentiment:
            formatted.append(f"• Sentiment: {sentiment.get('positive_percentage', 0):.1f}% positive")
        
        top_content = insights.get('top_performing_content', {})
        if top_content:
            formatted.append(f"• Top video: {top_content.get('views', 0):,} views")
        
        return '\n'.join(formatted)
    
    def _get_psychology_factors(self, insights: Dict) -> str:
        """Get psychology factors for prompts."""
        factors = [
            "• Social proof và validation seeking",
            "• Fear of missing out (FOMO)",
            "• Curiosity gap và information seeking",
            "• Personal identity và self-concept",
            "• Emotional resonance và relatability"
        ]
        
        # Add specific factors based on themes
        themes = insights.get('main_themes', [])
        if 'Relationships' in themes:
            factors.append("• Attachment theory và relationship patterns")
        if 'Psychology' in themes:
            factors.append("• Cognitive biases và heuristics")
        
        return '\n'.join(factors)
    
    def _get_content_suggestions(self, insights: Dict) -> str:
        """Get content suggestions based on insights."""
        themes = insights.get('main_themes', [])
        suggestions = []
        
        if 'Relationships' in themes:
            suggestions.extend([
                "• Toxic relationship patterns người ta không nhận ra",
                "• Bí mật tâm lý đằng sau attachment styles",
                "• Tại sao ta attracted to wrong people"
            ])
        
        if 'Psychology' in themes:
            suggestions.extend([
                "• Hidden psychology tricks thao túng tâm lý",
                "• Cognitive biases affect daily decisions",
                "• Subconscious patterns control behavior"
            ])
        
        if not suggestions:
            suggestions = [
                "• Personal transformation stories",
                "• Behind-the-scenes insights",
                "• Controversial but true observations"
            ]
        
        return '\n'.join(suggestions[:5])
    
    def _generate_hook_suggestion(self, insights: Dict) -> str:
        """Generate hook suggestion based on insights."""
        themes = insights.get('main_themes', [])
        viral_score = insights.get('viral_potential', 0)
        
        hooks = [
            "Điều này sẽ thay đổi cách bạn nhìn về {theme}",
            "99% người không biết điều này về {theme}",
            "Nghiên cứu 20 năm tiết lộ sự thật về {theme}",
            "Nếu bạn {behavior}, đây là điều đang xảy ra"
        ]
        
        main_theme = themes[0] if themes else 'life'
        hook_template = hooks[0] if viral_score > 50 else hooks[-1]
        
        return hook_template.format(theme=main_theme, behavior="làm điều này")
    
    def _generate_series_name(self, insights: Dict) -> str:
        """Generate series name based on insights."""
        themes = insights.get('main_themes', [])
        main_theme = themes[0] if themes else 'Life'
        
        series_names = {
            'Relationships': 'The Love Psychology Series',
            'Psychology': 'Mind Secrets Revealed',
            'Self Development': 'Transform Your Life',
            'Mental Health': 'Healing Journey',
            'Communication': 'Connection Mastery',
            'Motivation': 'Unstoppable You'
        }
        
        return series_names.get(main_theme, f'The {main_theme} Chronicles')
    
    def _get_core_message(self, insights: Dict) -> str:
        """Get core message based on insights."""
        themes = insights.get('main_themes', [])
        if not themes:
            return "Transform your mindset, transform your life"
        
        messages = {
            'Relationships': 'Understanding psychology creates deeper connections',
            'Psychology': 'Your mind has more power than you realize',
            'Self Development': 'Small changes lead to massive transformations',
            'Mental Health': 'Healing is possible with the right knowledge',
            'Communication': 'Better communication creates better relationships',
            'Motivation': 'You have unlimited potential within you'
        }
        
        return messages.get(themes[0], 'Knowledge is the key to transformation')
    
    def _generate_content_specific_variables(self, insights: Dict, preferences: Dict) -> Dict:
        """Generate content-specific variables for different prompt types."""
        variables = {}
        
        # Video script specific
        variables.update({
            'hook_content': self._generate_hook_content(insights),
            'intro_content': self._generate_intro_content(insights),
            'main_content_structure': self._generate_main_content_structure(insights),
            'climax_content': self._generate_climax_content(insights),
            'conclusion_content': self._generate_conclusion_content(insights),
            'interactive_elements': self._generate_interactive_elements(insights),
            'title_suggestions': self._generate_title_suggestions(insights),
            'thumbnail_ideas': self._generate_thumbnail_ideas(insights),
            'suggested_tags': self._generate_suggested_tags(insights)
        })
        
        # Series specific
        variables.update({
            'episode_outlines': self._generate_episode_outlines(insights, preferences.get('series_length', 5)),
            'platform_strategy': self._generate_platform_strategy(insights),
            'cross_promotion': self._generate_cross_promotion_strategy(insights),
            'retention_strategy': self._generate_retention_strategy(insights),
            'viral_elements': self._generate_viral_elements(insights),
            'success_metrics': self._generate_success_metrics(insights)
        })
        
        # Social media specific
        variables.update({
            'youtube_shorts_content': self._generate_youtube_shorts(insights),
            'instagram_posts': self._generate_instagram_posts(insights),
            'instagram_stories': self._generate_instagram_stories(insights),
            'instagram_reels': self._generate_instagram_reels(insights),
            'tiktok_content': self._generate_tiktok_content(insights),
            'facebook_content': self._generate_facebook_content(insights),
            'twitter_content': self._generate_twitter_content(insights),
            'linkedin_content': self._generate_linkedin_content(insights),
            'visual_style': self._generate_visual_style(insights),
            'color_palette': self._generate_color_palette(insights),
            'typography': self._generate_typography(insights),
            'brand_elements': self._generate_brand_elements(insights),
            'posting_schedule': self._generate_posting_schedule(insights)
        })
        
        # Email sequence specific
        variables.update({
            'email_sequence_content': self._generate_email_sequence(insights, preferences.get('sequence_length', 7)),
            'subject_formulas': self._generate_subject_formulas(insights),
            'email_templates': self._generate_email_templates(insights),
            'cta_strategies': self._generate_cta_strategies(insights),
            'automation_triggers': self._generate_automation_triggers(insights),
            'open_rate_target': preferences.get('open_rate_target', 25),
            'click_rate_target': preferences.get('click_rate_target', 5),
            'conversion_target': preferences.get('conversion_target', 2)
        })
        
        # Blog content specific
        variables.update({
            'blog_post_series': self._generate_blog_post_series(insights),
            'primary_keywords': self._generate_primary_keywords(insights),
            'secondary_keywords': self._generate_secondary_keywords(insights),
            'content_clusters': self._generate_content_clusters(insights),
            'linking_strategy': self._generate_linking_strategy(insights),
            'content_calendar': self._generate_content_calendar(insights),
            'howto_topics': self._generate_howto_topics(insights),
            'listicle_topics': self._generate_listicle_topics(insights),
            'case_study_topics': self._generate_case_study_topics(insights),
            'opinion_topics': self._generate_opinion_topics(insights),
            'distribution_strategy': self._generate_distribution_strategy(insights)
        })
        
        return variables
    
    def _generate_hook_content(self, insights: Dict) -> str:
        """Generate hook content for video script."""
        main_theme = insights.get('main_themes', ['psychology'])[0].lower()
        
        hooks = {
            'relationships': "Nếu bạn đang struggle với relationships, video này sẽ reveal những psychology patterns mà 99% người không biết...",
            'psychology': "Tôi đã study psychology 10 năm và phát hiện ra điều này sẽ blow your mind...",
            'self development': "Điều tôi sắp share có thể completely change cách bạn approach personal growth...",
            'default': "Điều tôi vừa discover sẽ fundamentally shift cách bạn think về life..."
        }
        
        return hooks.get(main_theme, hooks['default'])
    
    def _generate_intro_content(self, insights: Dict) -> str:
        """Generate intro content."""
        return """Chào mọi người, welcome back to channel!

Hôm nay chúng ta sẽ dive deep into một topic cực kỳ fascinating. Nhưng trước khi start, đừng quên smash that like button và subscribe for more content như này!

Okay, let's get into it..."""
    
    def _generate_main_content_structure(self, insights: Dict) -> str:
        """Generate main content structure."""
        return """Point 1: Context và background (2-3 minutes)
- Explain the basic concept
- Share relevant statistics/research
- Connect to audience's experience

Point 2: Deep dive analysis (3-4 minutes)  
- Break down the psychology behind it
- Use concrete examples
- Address common misconceptions

Point 3: Practical applications (2-3 minutes)
- How to apply this in real life
- Step-by-step actionable advice
- Common mistakes to avoid"""
    
    def _generate_climax_content(self, insights: Dict) -> str:
        """Generate climax content."""
        return """Đây là moment mà everything clicks...

[Pause for dramatic effect]

The real secret is... [reveal the key insight]

This completely changes everything we thought we knew about [topic]."""
    
    def _generate_conclusion_content(self, insights: Dict) -> str:
        """Generate conclusion content."""
        return """Vậy là chúng ta đã explore together một topic thực sự mind-blowing.

Remember: [key takeaway]

Hãy comment bên dưới share experience của bạn, và đừng quên subscribe for more psychology insights!

See you in the next video!"""
    
    # Additional helper methods for other content types...
    def _generate_interactive_elements(self, insights: Dict) -> str:
        return "• Polls in community tab\n• Comment challenges\n• Live Q&A sessions\n• Collaboration với audience"
    
    def _generate_title_suggestions(self, insights: Dict) -> str:
        themes = insights.get('main_themes', ['psychology'])
        main_theme = themes[0] if themes else 'psychology'
        
        suggestions = [
            f"The Hidden Psychology of {main_theme.title()} (Mind-Blowing)",
            f"99% Don't Know This About {main_theme.title()}",
            f"The Dark Truth About {main_theme.title()} Psychology",
            f"This {main_theme.title()} Secret Will Change Your Life"
        ]
        return ' | '.join(suggestions)
    
    def _generate_thumbnail_ideas(self, insights: Dict) -> str:
        return "• Shocked facial expression với bright colors\n• Split screen: before/after\n• Bold text overlay với arrows\n• High contrast background"
    
    def _generate_suggested_tags(self, insights: Dict) -> str:
        themes = insights.get('main_themes', ['psychology'])
        base_tags = ['psychology', 'viral', 'mindset', 'self development', 'life advice']
        theme_tags = [theme.lower().replace(' ', '') for theme in themes]
        return ', '.join(base_tags + theme_tags)
    
    # Placeholder methods for other content generation functions
    def _generate_episode_outlines(self, insights: Dict, series_length: int) -> str:
        outlines = []
        themes = insights.get('main_themes', ['psychology'])
        main_theme = themes[0] if themes else 'psychology'
        
        for i in range(1, series_length + 1):
            outlines.append(f"Episode {i}: [Topic related to {main_theme}]")
        
        return '\n'.join(outlines)
    
    def _generate_platform_strategy(self, insights: Dict) -> str:
        return "YouTube primary, TikTok for viral clips, Instagram for community building"
    
    def _generate_cross_promotion_strategy(self, insights: Dict) -> str:
        return "Cross-promote between platforms, collaborate với other creators, guest appearances"
    
    def _generate_retention_strategy(self, insights: Dict) -> str:
        return "Cliffhangers, consistent upload schedule, community engagement, exclusive content"
    
    def _generate_viral_elements(self, insights: Dict) -> str:
        return "• Shocking statistics\n• Controversial takes\n• Personal stories\n• Interactive challenges"
    
    def _generate_success_metrics(self, insights: Dict) -> str:
        return "• View retention >50%\n• Engagement rate >5%\n• Subscriber growth\n• Comment sentiment"
    
    # Social media content generators
    def _generate_youtube_shorts(self, insights: Dict) -> str:
        return "60-second rapid-fire psychology facts với engaging visuals và trending audio"
    
    def _generate_instagram_posts(self, insights: Dict) -> str:
        return "Quote cards, carousel posts với tips, behind-the-scenes content"
    
    def _generate_instagram_stories(self, insights: Dict) -> str:
        return "Daily polls, Q&A stickers, quick tips, process videos"
    
    def _generate_instagram_reels(self, insights: Dict) -> str:
        return "Trending audio với psychology facts, transformation content"
    
    def _generate_tiktok_content(self, insights: Dict) -> str:
        return "15-60s videos với viral sounds, psychology hacks, đáp criticisms"
    
    def _generate_facebook_content(self, insights: Dict) -> str:
        return "Longer-form posts, community discussions, live streams"
    
    def _generate_twitter_content(self, insights: Dict) -> str:
        return "Thread series, quick insights, engagement với psychology community"
    
    def _generate_linkedin_content(self, insights: Dict) -> str:
        return "Professional insights, career psychology, leadership content"
    
    def _generate_visual_style(self, insights: Dict) -> str:
        return "Modern, clean aesthetic với bold typography và high contrast"
    
    def _generate_color_palette(self, insights: Dict) -> str:
        return "Primary: Deep blue (#1A365D), Accent: Bright orange (#FF6B35), Supporting: Light gray (#F7FAFC)"
    
    def _generate_typography(self, insights: Dict) -> str:
        return "Headers: Bold sans-serif (Poppins), Body: Clean readable (Inter)"
    
    def _generate_brand_elements(self, insights: Dict) -> str:
        return "Consistent logo placement, signature color scheme, recognizable templates"
    
    def _generate_posting_schedule(self, insights: Dict) -> str:
        return """Monday: YouTube video
Tuesday: Instagram post + Stories  
Wednesday: TikTok content
Thursday: Blog post
Friday: YouTube Shorts
Weekend: Community engagement"""
    
    # Email sequence generators
    def _generate_email_sequence(self, insights: Dict, sequence_length: int) -> str:
        emails = []
        for i in range(1, sequence_length + 1):
            emails.append(f"Email {i}: [Subject and content outline]")
        return '\n\n'.join(emails)
    
    def _generate_subject_formulas(self, insights: Dict) -> str:
        return "• Question formula: 'Are you making this [mistake]?'\n• Urgency: 'Only 24 hours left...'\n• Curiosity: 'The secret nobody tells you...'"
    
    def _generate_email_templates(self, insights: Dict) -> str:
        return "Educational template, story-driven template, CTA-focused template"
    
    def _generate_cta_strategies(self, insights: Dict) -> str:
        return "• Single clear CTA per email\n• Action-oriented language\n• Create urgency\n• Provide clear value"
    
    def _generate_automation_triggers(self, insights: Dict) -> str:
        return "Welcome sequence, engagement-based, behavior triggers, re-engagement campaign"
    
    # Blog content generators
    def _generate_blog_post_series(self, insights: Dict) -> str:
        return "5-part series covering fundamentals, advanced concepts, case studies, practical applications, và future trends"
    
    def _generate_primary_keywords(self, insights: Dict) -> str:
        themes = insights.get('main_themes', ['psychology'])
        return f"{themes[0].lower()} tips, {themes[0].lower()} guide, how to {themes[0].lower()}"
    
    def _generate_secondary_keywords(self, insights: Dict) -> str:
        return "mindset, personal development, self improvement, life advice, psychology facts"
    
    def _generate_content_clusters(self, insights: Dict) -> str:
        return "Beginner guides cluster, Advanced techniques cluster, Case studies cluster"
    
    def _generate_linking_strategy(self, insights: Dict) -> str:
        return "Hub page linking to spoke pages, related posts at bottom, contextual internal links"
    
    def _generate_content_calendar(self, insights: Dict) -> str:
        return "Week 1-2: Foundation posts, Week 3-4: Advanced content, Week 5-6: Case studies, Week 7-8: Practical applications"
    
    def _generate_howto_topics(self, insights: Dict) -> str:
        themes = insights.get('main_themes', ['psychology'])
        main_theme = themes[0] if themes else 'psychology'
        return f"How to master {main_theme.lower()}, How to apply {main_theme.lower()} in daily life"
    
    def _generate_listicle_topics(self, insights: Dict) -> str:
        themes = insights.get('main_themes', ['psychology'])
        main_theme = themes[0] if themes else 'psychology'
        return f"10 {main_theme.title()} Facts, 7 Common {main_theme.title()} Mistakes"
    
    def _generate_case_study_topics(self, insights: Dict) -> str:
        return "Success stories, transformation journeys, before/after analyses"
    
    def _generate_opinion_topics(self, insights: Dict) -> str:
        return "Controversial takes, industry predictions, myth-busting articles"
    
    def _generate_distribution_strategy(self, insights: Dict) -> str:
        return "Social media promotion, email newsletter, SEO optimization, guest posting, community sharing"
    
    def _save_prompts(self, prompts: Dict) -> bool:
        """Save generated prompts to file."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_prompts_{timestamp}.json"
            
            os.makedirs('output/prompts', exist_ok=True)
            filepath = os.path.join('output/prompts', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(prompts, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Prompts saved to: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving prompts: {e}")
            return False
    
    def get_available_templates(self) -> Dict:
        """Get list of available prompt templates."""
        return {key: {'name': template['name'], 'description': template['description']} 
                for key, template in self.prompt_templates.items()}
    
    def get_generated_prompts(self) -> Dict:
        """Get currently generated prompts."""
        return self.generated_prompts
    
    def export_prompts(self, export_format: str = 'json', filename: Optional[str] = None) -> str:
        """Export prompts in specified format."""
        if not self.generated_prompts:
            raise ValueError("No prompts generated yet")
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"exported_prompts_{timestamp}.{export_format}"
        
        if export_format == 'json':
            return self._export_json(filename)
        elif export_format == 'txt':
            return self._export_txt(filename)
        elif export_format == 'md':
            return self._export_markdown(filename)
        else:
            raise ValueError(f"Unsupported export format: {export_format}")
    
    def _export_json(self, filename: str) -> str:
        """Export prompts as JSON."""
        os.makedirs('output/exports', exist_ok=True)
        filepath = os.path.join('output/exports', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.generated_prompts, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def _export_txt(self, filename: str) -> str:
        """Export prompts as plain text."""
        os.makedirs('output/exports', exist_ok=True)
        filepath = os.path.join('output/exports', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("GENERATED AI PROMPTS\n")
            f.write("=" * 50 + "\n\n")
            
            for key, prompt_data in self.generated_prompts.items():
                f.write(f"{prompt_data['name']}\n")
                f.write("-" * len(prompt_data['name']) + "\n")
                f.write(f"Description: {prompt_data['description']}\n\n")
                f.write(f"Prompt:\n{prompt_data['prompt']}\n\n")
                f.write("=" * 50 + "\n\n")
        
        return filepath
    
    def _export_markdown(self, filename: str) -> str:
        """Export prompts as Markdown."""
        os.makedirs('output/exports', exist_ok=True)
        filepath = os.path.join('output/exports', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Generated AI Prompts\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for key, prompt_data in self.generated_prompts.items():
                f.write(f"## {prompt_data['name']}\n\n")
                f.write(f"**Description:** {prompt_data['description']}\n\n")
                f.write("### Prompt\n\n")
                f.write(f"```\n{prompt_data['prompt']}\n```\n\n")
                f.write("---\n\n")
        
        return filepath


# Utility functions
def create_prompts_from_analysis(analysis_data: Dict, user_preferences: Optional[Dict] = None) -> Dict:
    """Create prompts from analysis data - main entry point."""
    if user_preferences is None:
        user_preferences = get_default_preferences()
    
    generator = PromptGenerator()
    return generator.generate_prompts_from_analysis(analysis_data, user_preferences)


def get_default_preferences() -> Dict:
    """Get default user preferences for prompt generation."""
    return {
        'min_words': 2000,
        'tone': 'Engaging and educational',
        'target_audience': 'Young adults 18-35',
        'framework': 'Hero\'s Journey',
        'video_duration': 10,
        'engagement_goal': 5,
        'series_length': 5,
        'frequency': 'Weekly',
        'content_format': 'Educational + Entertainment',
        'campaign_goal': 'Increase engagement and followers',
        'sequence_length': 7,
        'content_goals': 'Educate and inspire audience',
        'open_rate_target': 25,
        'click_rate_target': 5,
        'conversion_target': 2,
        # Template enablement
        'story_generation': True,
        'video_script': True,
        'content_series': True,
        'social_media': True,
        'email_sequence': True,
        'blog_content': True
    }


# Example usage
if __name__ == "__main__":
    # Example analysis data
    sample_analysis = {
        'transcripts': [
            {'full_text': 'psychology relationship love mind behavior emotion growth success confidence', 'video_id': '123'}
        ],
        'comments': [
            {'text': 'love this amazing helpful inspiring', 'like_count': 10},
            {'text': 'exactly what I needed relatable truth', 'like_count': 5}
        ],
        'videos': [
            {'title': 'Psychology of Love', 'view_count': 100000, 'like_count': 5000, 'comment_count': 500}
        ],
        'viral_score': 75.5
    }
    
    # Generate prompts
    prompts = create_prompts_from_analysis(sample_analysis)
    
    # Print generated prompts
    for key, prompt_data in prompts.items():
        print(f"\n{prompt_data['name']}:")
        print("-" * 50)
        print(prompt_data['prompt'][:200] + "...")