from generators.base_generator import BaseGenerator
from utils.api_handler import PromptOptimizer
from prompts.social_media_prompts import SocialMediaPrompts

class SocialMediaGenerator(BaseGenerator):
    """Generate social media content for various platforms"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        super().__init__(api_key, model)
        self.prompts = SocialMediaPrompts()
    
    def generate_content(self, **kwargs) -> dict:
        """
        Generate content based on parameters (abstract method implementation)
        
        Returns:
            Dict containing generated content and metadata
        """
        # Default to generate_post if no specific method is called
        return self.generate_post(**kwargs)
    
    def generate_post(self,
                     platform: str,
                     topic: str,
                     target_audience: str = "Genel Kitle",
                     tone: str = "professional",
                     post_type: str = "promotional",
                     include_hashtags: bool = True,
                     include_emojis: bool = True,
                     include_cta: bool = True,
                     custom_instructions: str = "",
                     creativity_level: float = 0.7) -> dict:
        """
        Generate a social media post
        
        Args:
            platform: Social media platform (instagram, twitter, linkedin, facebook)
            topic: Main topic or subject
            target_audience: Target audience description
            tone: Content tone
            post_type: Type of post
            include_hashtags: Include hashtags
            include_emojis: Include emojis
            include_cta: Include call-to-action
            custom_instructions: Additional instructions
            creativity_level: AI creativity level (0-1)
        
        Returns:
            Dict with generated content and metadata
        """
        
        # Get platform-specific prompt
        base_prompt = self.prompts.get_platform_prompt(
            platform=platform,
            post_type=post_type,
            topic=topic,
            target_audience=target_audience
        )
        
        # Add optional elements
        optional_elements = []
        if include_hashtags:
            optional_elements.append("relevant hashtags")
        if include_emojis:
            optional_elements.append("appropriate emojis")
        if include_cta:
            optional_elements.append("call-to-action")
        
        if optional_elements:
            base_prompt += f"\n\nDahil et: {', '.join(optional_elements)}"
        
        # Add custom instructions
        if custom_instructions:
            base_prompt += f"\n\nEk talimatlar: {custom_instructions}"
        
        # Get system prompt
        system_prompt = self.prompts.get_system_prompt(platform, tone)
        
        # Optimize prompt
        optimized_prompt = PromptOptimizer.optimize_prompt(
            base_prompt=base_prompt,
            content_type="social_media",
            platform=platform,
            tone=tone,
            target_audience=target_audience
        )
        
        # Generate content
        result = self.api_handler.generate_content(
            prompt=optimized_prompt,
            system_prompt=system_prompt,
            max_tokens=self._get_max_tokens(platform),
            temperature=creativity_level
        )
        
        if result['success']:
            # Post-process content
            processed_content = self._post_process_content(
                result['content'], 
                platform, 
                include_hashtags,
                include_emojis
            )
            result['content'] = processed_content
        
        return result
    
    def generate_content_series(self,
                              platform: str,
                              theme: str,
                              post_count: int = 5,
                              **kwargs) -> dict:
        """
        Generate a series of related social media posts
        
        Args:
            platform: Social media platform
            theme: Overall theme for the series
            post_count: Number of posts to generate
            **kwargs: Additional arguments for individual posts
        
        Returns:
            Dict with generated content series
        """
        
        series_prompt = self.prompts.get_series_prompt(
            platform=platform,
            theme=theme,
            post_count=post_count
        )
        
        system_prompt = self.prompts.get_system_prompt(
            platform, 
            kwargs.get('tone', 'professional')
        )
        
        result = self.api_handler.generate_content(
            prompt=series_prompt,
            system_prompt=system_prompt,
            max_tokens=self._get_max_tokens(platform) * post_count,
            temperature=kwargs.get('creativity_level', 0.7)
        )
        
        if result['success']:
            # Split content into individual posts
            content = result['content']
            posts = self._split_series_content(content, post_count)
            result['posts'] = posts
            result['series_count'] = len(posts)
        
        return result
    
    def generate_hashtags(self,
                         topic: str,
                         platform: str = "instagram",
                         count: int = 10,
                         mix_popular_niche: bool = True) -> dict:
        """
        Generate relevant hashtags for a topic
        
        Args:
            topic: Main topic
            platform: Platform for hashtags
            count: Number of hashtags to generate
            mix_popular_niche: Mix popular and niche hashtags
        
        Returns:
            Dict with generated hashtags
        """
        
        hashtag_prompt = self.prompts.get_hashtag_prompt(
            topic=topic,
            platform=platform,
            count=count,
            mix_popular_niche=mix_popular_niche
        )
        
        result = self.api_handler.generate_content(
            prompt=hashtag_prompt,
            max_tokens=300,
            temperature=0.5
        )
        
        if result['success']:
            hashtags = self._extract_hashtags(result['content'])
            result['hashtags'] = hashtags
            result['hashtag_count'] = len(hashtags)
        
        return result
    
    def _get_max_tokens(self, platform: str) -> int:
        """Get appropriate max tokens for platform"""
        token_limits = {
            'twitter': 100,
            'instagram': 800,
            'linkedin': 1000,
            'facebook': 800
        }
        return token_limits.get(platform, 800)
    
    def _post_process_content(self, 
                            content: str, 
                            platform: str,
                            include_hashtags: bool,
                            include_emojis: bool) -> str:
        """Post-process generated content"""
        
        # Clean up content
        content = content.strip()
        
        # Platform-specific character limits
        char_limits = {
            'twitter': 280,
            'instagram': 2200,
            'linkedin': 3000,
            'facebook': 63206
        }
        
        limit = char_limits.get(platform)
        if limit and len(content) > limit:
            # Truncate while preserving hashtags
            if include_hashtags and '#' in content:
                text_part = content.split('#')[0].strip()
                hashtag_part = '#' + '#'.join(content.split('#')[1:])
                
                # Truncate text part if needed
                available_chars = limit - len(hashtag_part) - 5  # buffer
                if len(text_part) > available_chars:
                    text_part = text_part[:available_chars].rsplit(' ', 1)[0] + '...'
                
                content = f"{text_part}\n\n{hashtag_part}"
            else:
                content = content[:limit-3] + '...'
        
        return content
    
    def _split_series_content(self, content: str, expected_count: int) -> list:
        """Split series content into individual posts"""
        
        # Try different splitting patterns
        separators = ['\n\n---\n\n', '\n\n**Post', '\n\n1.', '\n\n2.']
        
        posts = []
        for separator in separators:
            if separator in content:
                posts = [post.strip() for post in content.split(separator) if post.strip()]
                break
        
        # Fallback: split by double newlines
        if not posts:
            posts = [post.strip() for post in content.split('\n\n') if post.strip()]
        
        # Ensure we have the expected number of posts
        if len(posts) < expected_count:
            posts.extend(['[Additional content needed]'] * (expected_count - len(posts)))
        elif len(posts) > expected_count:
            posts = posts[:expected_count]
        
        return posts
    
    def _extract_hashtags(self, content: str) -> list:
        """Extract hashtags from generated content"""
        import re
        
        # Find hashtags using regex
        hashtag_pattern = r'#[A-Za-z0-9_]+'
        hashtags = re.findall(hashtag_pattern, content)
        
        # Remove duplicates while preserving order
        unique_hashtags = []
        for hashtag in hashtags:
            if hashtag not in unique_hashtags:
                unique_hashtags.append(hashtag)
        
        return unique_hashtags