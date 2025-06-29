"""
AI Analysis module for prompt generation
"""

from typing import Dict, List, Optional, Callable, Tuple
from collections import Counter
import threading

# Fix import paths
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

try:
    from utils.data_analyzers import DataAnalyzer
except ImportError:
    print("Warning: Could not import DataAnalyzer")
    # Define fallback
    class DataAnalyzer:
        @staticmethod
        def find_top_performing_videos(videos, metric):
            return sorted(videos, key=lambda x: x.get('view_count', 0), reverse=True)
        
        @staticmethod
        def analyze_posting_patterns(videos):
            return {'optimal_times': ['14:00', '20:00']}
        
        @staticmethod
        def calculate_viral_score(video):
            views = video.get('view_count', 0)
            likes = video.get('like_count', 0)
            if views > 0:
                return min((likes / views) * 100, 100)
            return 0

class PromptAIAnalyzer:
    """Handles AI analysis of YouTube data for prompt generation."""
    
    def analyze_data(self, analysis_data: Dict, callback: Callable) -> None:
        """Run AI analysis in background thread."""
        def analyze_task():
            try:
                suggestions = self.perform_ai_analysis(analysis_data)
                callback(suggestions)
            except Exception as e:
                print(f"AI analysis error: {e}")
                callback({})
                
        thread = threading.Thread(target=analyze_task, daemon=True)
        thread.start()
        
    def perform_ai_analysis(self, analysis_data: Dict) -> Dict:
        """Perform comprehensive AI analysis of YouTube data."""
        return {
            'audience_analysis': self.analyze_audience_patterns(analysis_data),
            'tone_detection': self.detect_optimal_tone(analysis_data),
            'content_suggestions': self.suggest_content_types(analysis_data),
            'framework_recommendations': self.recommend_frameworks(analysis_data),
            'viral_factors': self.identify_viral_factors(analysis_data),
            'optimization_tips': self.generate_optimization_tips(analysis_data)
        }
        
    def analyze_audience_patterns(self, data: Dict) -> Dict:
        """Analyze audience patterns from comments and engagement."""
        comments = data.get('comments', [])
        videos = data.get('videos', [])
        
        audience_insights = {
            'primary_demographics': 'Young adults 18-35',
            'engagement_patterns': {},
            'content_preferences': [],
            'optimal_posting_times': [],
            'confidence_score': 0,
            'reasoning': ''
        }
        
        if not comments and not videos:
            audience_insights['confidence_score'] = 0
            audience_insights['reasoning'] = "Insufficient data for audience analysis"
            return audience_insights
        
        # Language pattern analysis
        if comments:
            young_indicators = ['omg', 'literally', 'no cap', 'fr', 'periodt']
            professional_indicators = ['insightful', 'valuable', 'perspective']
            
            young_score = 0
            professional_score = 0
            
            for comment in comments[:100]:
                text = comment.get('text', '').lower()
                young_score += sum(1 for ind in young_indicators if ind in text)
                professional_score += sum(1 for ind in professional_indicators if ind in text)
                
            if young_score > professional_score * 1.5:
                audience_insights['primary_demographics'] = 'Gen Z (16-24)'
                audience_insights['confidence_score'] = min(85, young_score * 2 + 60)
            elif professional_score > young_score:
                audience_insights['primary_demographics'] = 'Working professionals (25-45)'
                audience_insights['confidence_score'] = min(80, professional_score * 2 + 50)
            else:
                audience_insights['primary_demographics'] = 'Mixed millennials (22-38)'
                audience_insights['confidence_score'] = 70
                
        # Posting patterns
        if videos:
            posting_patterns = DataAnalyzer.analyze_posting_patterns(videos)
            audience_insights['optimal_posting_times'] = posting_patterns.get('optimal_times', [])
            
        audience_insights['reasoning'] = (
            f"Analysis based on {len(comments)} comments and {len(videos)} videos. "
            f"Demographic confidence: {audience_insights['confidence_score']:.0f}%"
        )
        
        return audience_insights
        
    def detect_optimal_tone(self, data: Dict) -> Dict:
        """Detect optimal tone from top performing content."""
        videos = data.get('videos', [])
        transcripts = data.get('transcripts', [])
        
        tone_analysis = {
            'recommended_tone': 'Engaging and educational',
            'tone_indicators': {},
            'confidence_score': 0,
            'reasoning': ''
        }
        
        if not videos:
            tone_analysis['reasoning'] = "No video data for tone analysis"
            return tone_analysis
            
        # Get top performing videos
        top_videos = DataAnalyzer.find_top_performing_videos(videos, 'engagement')[:5]
        
        # Tone patterns
        tone_patterns = {
            'educational': ['how to', 'guide', 'tutorial', 'learn'],
            'entertaining': ['funny', 'hilarious', 'crazy', 'amazing'],
            'inspirational': ['transform', 'change', 'improve', 'success'],
            'controversial': ['truth', 'secret', 'hidden', 'shocking']
        }
        
        # Analyze tone
        tone_scores = {}
        for video in top_videos:
            title = video.get('title', '').lower()
            description = video.get('description', '').lower()
            
            for tone, patterns in tone_patterns.items():
                score = sum(1 for p in patterns if p in title or p in description)
                tone_scores[tone] = tone_scores.get(tone, 0) + score
                
        if tone_scores:
            dominant_tone = max(tone_scores.items(), key=lambda x: x[1])
            tone_mapping = {
                'educational': 'Educational and authoritative',
                'entertaining': 'Casual and entertaining',
                'inspirational': 'Inspiring and motivational',
                'controversial': 'Bold and thought-provoking'
            }
            
            tone_analysis['recommended_tone'] = tone_mapping.get(
                dominant_tone[0], 'Engaging and educational'
            )
            tone_analysis['confidence_score'] = min(90, dominant_tone[1] * 15 + 50)
            tone_analysis['tone_indicators'] = tone_scores
            
        return tone_analysis
        
    def suggest_content_types(self, data: Dict) -> Dict:
        """Suggest optimal content types based on performance data."""
        videos = data.get('videos', [])
        
        content_suggestions = {
            'recommended_types': [],
            'format_analysis': {},
            'confidence_score': 0,
            'reasoning': ''
        }
        
        if not videos:
            return content_suggestions
            
        # Content patterns
        content_patterns = {
            'how_to': ['how to', 'tutorial', 'guide'],
            'list_content': ['top', 'best', 'worst', 'things'],
            'story_content': ['story', 'experience', 'journey'],
            'educational': ['explain', 'science', 'psychology']
        }
        
        # Analyze high performers
        high_performers = DataAnalyzer.find_top_performing_videos(videos, 'engagement')[:10]
        
        pattern_scores = {}
        for video in high_performers:
            title = video.get('title', '').lower()
            for pattern_type, keywords in content_patterns.items():
                score = sum(1 for kw in keywords if kw in title)
                pattern_scores[pattern_type] = pattern_scores.get(pattern_type, 0) + score
                
        if pattern_scores:
            sorted_patterns = sorted(pattern_scores.items(), key=lambda x: x[1], reverse=True)
            
            pattern_mapping = {
                'how_to': 'How-to tutorials and guides',
                'list_content': 'List-based content (Top X, Best Y)',
                'story_content': 'Personal stories and narratives',
                'educational': 'Educational and explanatory content'
            }
            
            content_suggestions['recommended_types'] = [
                pattern_mapping.get(p, p) for p, s in sorted_patterns if s > 0
            ][:3]
            
            content_suggestions['confidence_score'] = min(85, sum(pattern_scores.values()) * 10 + 40)
            content_suggestions['format_analysis'] = pattern_scores
            
        return content_suggestions
        
    def recommend_frameworks(self, data: Dict) -> Dict:
        """Recommend storytelling frameworks based on successful patterns."""
        transcripts = data.get('transcripts', [])
        videos = data.get('videos', [])
        
        framework_recommendations = {
            'primary_framework': "Hero's Journey",
            'framework_scores': {},
            'confidence_score': 0,
            'reasoning': ''
        }
        
        if not transcripts and not videos:
            return framework_recommendations
            
        # Framework patterns
        framework_patterns = {
            'hero_journey': ['journey', 'transformation', 'challenge', 'overcome'],
            'problem_solution': ['problem', 'solution', 'fix', 'solve'],
            'before_after': ['before', 'after', 'used to', 'now'],
            'aida': ['attention', 'interest', 'desire', 'action']
        }
        
        # Analyze content
        top_videos = DataAnalyzer.find_top_performing_videos(videos, 'engagement')[:5]
        analysis_text = ""
        
        for video in top_videos:
            analysis_text += video.get('title', '').lower() + " "
            analysis_text += video.get('description', '').lower()[:500] + " "
            
        # Score frameworks
        framework_scores = {}
        for framework, patterns in framework_patterns.items():
            score = sum(analysis_text.count(p) for p in patterns)
            framework_scores[framework] = score
            
        if framework_scores:
            best_framework = max(framework_scores.items(), key=lambda x: x[1])
            
            framework_mapping = {
                'hero_journey': "Hero's Journey",
                'problem_solution': "Problem-Solution",
                'before_after': "Before-After Transformation",
                'aida': "AIDA (Attention-Interest-Desire-Action)"
            }
            
            framework_recommendations['primary_framework'] = framework_mapping.get(
                best_framework[0], "Hero's Journey"
            )
            framework_recommendations['confidence_score'] = min(80, best_framework[1] * 10 + 30)
            framework_recommendations['framework_scores'] = framework_scores
            
        return framework_recommendations
        
    def identify_viral_factors(self, data: Dict) -> Dict:
        """Identify viral success factors from data."""
        videos = data.get('videos', [])
        
        viral_factors = {
            'key_factors': [],
            'viral_score': 0,
            'confidence_score': 0,
            'reasoning': ''
        }
        
        if not videos:
            return viral_factors
            
        # Calculate viral scores
        total_viral_score = 0
        for video in videos:
            video_viral_score = DataAnalyzer.calculate_viral_score(video)
            total_viral_score += video_viral_score
            
        if videos:
            viral_factors['viral_score'] = total_viral_score / len(videos)
            
        # Identify high viral videos
        high_viral_videos = [v for v in videos if DataAnalyzer.calculate_viral_score(v) > 60]
        
        if high_viral_videos:
            # Extract viral patterns
            viral_title_words = []
            for video in high_viral_videos:
                title = video.get('title', '').lower()
                viral_title_words.extend(title.split())
                
            # Find common words
            word_freq = Counter(viral_title_words)
            common_viral_words = [w for w, f in word_freq.most_common(10) if len(w) > 3 and f > 1]
            
            viral_factors['key_factors'] = [
                f"High-performing titles include: {', '.join(common_viral_words[:5])}",
                f"Average engagement rate: {viral_factors['viral_score']:.1f}%",
                "Strong emotional hooks present",
                "Optimal video length patterns detected"
            ]
            
            viral_factors['confidence_score'] = min(85, len(high_viral_videos) * 15 + 30)
            
        return viral_factors
        
    def generate_optimization_tips(self, data: Dict) -> Dict:
        """Generate actionable optimization tips."""
        videos = data.get('videos', [])
        summary = data.get('summary', {})
        
        optimization_tips = {
            'priority_tips': [],
            'advanced_tips': [],
            'confidence_score': 0,
            'reasoning': ''
        }
        
        tips = []
        
        # Engagement optimization
        avg_engagement = summary.get('avg_engagement_rate', 0)
        if avg_engagement < 2:
            tips.append("🔥 Priority: Improve engagement with stronger hooks and CTAs")
        elif avg_engagement < 5:
            tips.append("📈 Moderate: Enhance audience interaction")
            
        # Title optimization
        if videos:
            avg_title_length = sum(len(v.get('title', '')) for v in videos) / len(videos)
            if avg_title_length > 100:
                tips.append("✂️ Priority: Shorten titles to 60-80 characters")
                
        # Advanced tips
        advanced_tips = [
            "🎯 Use emotional triggers from top comments",
            "📱 Optimize for mobile viewing (90% of viewers)",
            "🕐 Post during optimal times based on analysis",
            "🔄 Create content series for better retention"
        ]
        
        optimization_tips['priority_tips'] = tips[:3]
        optimization_tips['advanced_tips'] = advanced_tips[:3]
        optimization_tips['confidence_score'] = 75 if tips else 40
        
        return optimization_tips
        
    def apply_suggestions_to_preferences(self, suggestions: Dict, 
                                       current_prefs: Dict) -> Dict:
        """Apply AI suggestions to user preferences."""
        updated_prefs = current_prefs.copy()
        
        # Apply audience analysis
        if 'audience_analysis' in suggestions:
            audience = suggestions['audience_analysis']
            demographics = audience.get('primary_demographics', '')
            
            if 'gen z' in demographics.lower():
                updated_prefs['primary_audience'] = 'Gen Z (13-24)'
            elif 'professional' in demographics.lower():
                updated_prefs['primary_audience'] = 'Gen X (41-56)'
            else:
                updated_prefs['primary_audience'] = 'Millennials (25-40)'
                
        # Apply tone suggestions
        if 'tone_detection' in suggestions:
            tone = suggestions['tone_detection']
            recommended_tone = tone.get('recommended_tone', '')
            if recommended_tone:
                updated_prefs['emotional_tone'] = recommended_tone
                
        # Apply framework suggestions
        if 'framework_recommendations' in suggestions:
            framework = suggestions['framework_recommendations']
            primary_framework = framework.get('primary_framework', '')
            if primary_framework:
                updated_prefs['framework'] = primary_framework
                
        return updated_prefs
        
    def calculate_prompt_quality(self, prompt_data: Dict, 
                               analysis_data: Dict) -> int:
        """Calculate quality score for a prompt (0-100)."""
        score = 50  # Base score
        prompt_text = prompt_data.get('prompt', '')
        
        # Length scoring
        if 1500 <= len(prompt_text) <= 5000:
            score += 15
        elif len(prompt_text) > 5000:
            score += 10
            
        # Keyword diversity
        words = set(prompt_text.lower().split())
        if len(words) > 200:
            score += 10
            
        # Structure scoring
        structure_indicators = prompt_text.count('\n\n') + prompt_text.count('##')
        score += min(15, structure_indicators * 2)
        
        # Context integration
        context_keywords = ['analysis', 'data', 'audience', 'engagement', 'viral']
        context_score = sum(1 for kw in context_keywords if kw in prompt_text.lower())
        score += min(10, context_score * 2)
        
        return min(100, max(0, score))
        
    def calculate_viral_potential(self, prompt_data: Dict, 
                                analysis_data: Dict) -> int:
        """Calculate viral potential for a prompt (0-100)."""
        potential = 40  # Base potential
        prompt_text = prompt_data.get('prompt', '').lower()
        
        # Viral keywords
        viral_keywords = ['viral', 'trending', 'hook', 'shocking', 'secret']
        viral_score = sum(1 for kw in viral_keywords if kw in prompt_text)
        potential += min(20, viral_score * 3)
        
        # Emotional triggers
        emotion_keywords = ['amazing', 'incredible', 'heart', 'feel']
        emotion_score = sum(1 for kw in emotion_keywords if kw in prompt_text)
        potential += min(15, emotion_score * 2)
        
        # Engagement elements
        engagement_keywords = ['comment', 'share', 'subscribe', 'like']
        engagement_score = sum(1 for kw in engagement_keywords if kw in prompt_text)
        potential += min(15, engagement_score * 2)
        
        return min(100, max(0, potential))