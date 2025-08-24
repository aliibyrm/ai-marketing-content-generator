from abc import ABC, abstractmethod
from utils.api_handler import APIHandler
from typing import Dict, List, Optional

class BaseGenerator(ABC):
    """Base class for all content generators"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Initialize the base generator
        
        Args:
            api_key: OpenAI API key
            model: AI model to use
        """
        self.api_key = api_key
        self.model = model
        self.api_handler = APIHandler(api_key, model)
    
    @abstractmethod
    def generate_content(self, **kwargs) -> Dict:
        """
        Generate content based on parameters
        
        Returns:
            Dict containing generated content and metadata
        """
        pass
    
    def validate_inputs(self, required_fields: List[str], inputs: Dict) -> bool:
        """
        Validate that required inputs are provided
        
        Args:
            required_fields: List of required field names
            inputs: Dictionary of input values
        
        Returns:
            True if all required fields are present and non-empty
        """
        for field in required_fields:
            if field not in inputs or not inputs[field]:
                return False
        return True
    
    def sanitize_input(self, text: str) -> str:
        """
        Sanitize input text to prevent issues
        
        Args:
            text: Input text to sanitize
        
        Returns:
            Sanitized text
        """
        if not text:
            return ""
        
        # Basic sanitization
        text = text.strip()
        
        # Remove excessive whitespace
        import re
        text = re.sub(r'\s+', ' ', text)
        
        # Limit length to prevent excessive token usage
        if len(text) > 5000:
            text = text[:5000] + "..."
        
        return text
    
    def format_output(self, content: str, format_type: str = "plain") -> str:
        """
        Format output content based on type
        
        Args:
            content: Generated content
            format_type: Output format (plain, html, markdown)
        
        Returns:
            Formatted content
        """
        if format_type == "html":
            # Convert newlines to HTML breaks
            content = content.replace('\n', '<br>')
            # Add basic HTML structure
            content = f"<div class='generated-content'>{content}</div>"
        
        elif format_type == "markdown":
            # Ensure proper markdown formatting
            if not content.startswith('#'):
                content = f"# Generated Content\n\n{content}"
        
        return content
    
    def estimate_generation_time(self, prompt_length: int, max_tokens: int) -> float:
        """
        Estimate generation time based on input parameters
        
        Args:
            prompt_length: Length of input prompt in characters
            max_tokens: Maximum tokens to generate
        
        Returns:
            Estimated time in seconds
        """
        # Rough estimation formula
        base_time = 2.0  # Base processing time
        prompt_factor = prompt_length / 1000 * 0.5  # Time per 1000 chars
        token_factor = max_tokens / 100 * 0.3  # Time per 100 tokens
        
        return base_time + prompt_factor + token_factor
    
    def get_usage_stats(self) -> Dict:
        """
        Get usage statistics for the generator
        
        Returns:
            Dictionary with usage stats
        """
        # This would typically connect to a database or file
        # For now, return dummy stats
        return {
            "total_generations": 0,
            "total_tokens_used": 0,
            "average_generation_time": 0,
            "favorite_tone": "professional",
            "most_used_platform": "instagram"
        }
    
    def export_content(self, content: str, filename: str, format_type: str = "txt") -> bool:
        """
        Export generated content to file
        
        Args:
            content: Content to export
            filename: Output filename
            format_type: File format (txt, html, md, json)
        
        Returns:
            True if export successful, False otherwise
        """
        try:
            import os
            
            # Ensure exports directory exists
            os.makedirs("data/exports", exist_ok=True)
            
            filepath = f"data/exports/{filename}.{format_type}"
            
            if format_type == "json":
                import json
                export_data = {
                    "content": content,
                    "generated_at": self._get_timestamp(),
                    "model": self.model,
                    "generator_type": self.__class__.__name__
                }
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            return True
            
        except Exception as e:
            print(f"Export failed: {str(e)}")
            return False
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _clean_content(self, content: str) -> str:
        """Clean and normalize generated content"""
        if not content:
            return ""
        
        # Remove extra whitespace
        import re
        content = re.sub(r'\n\s*\n', '\n\n', content)  # Multiple newlines to double
        content = re.sub(r' +', ' ', content)  # Multiple spaces to single
        
        # Remove markdown artifacts if not intended
        content = content.replace('**', '')
        content = content.replace('##', '')
        
        # Trim
        content = content.strip()
        
        return content
    
    def get_content_suggestions(self, topic: str) -> List[str]:
        """
        Get content suggestions based on topic
        
        Args:
            topic: Main topic
        
        Returns:
            List of content suggestions
        """
        suggestions = [
            f"Educational content about {topic}",
            f"Behind-the-scenes look at {topic}",
            f"Tips and tricks related to {topic}",
            f"User testimonials about {topic}",
            f"Industry trends in {topic}",
            f"Common misconceptions about {topic}",
            f"Future of {topic}",
            f"Beginner's guide to {topic}"
        ]
        
        return suggestions[:5]  # Return top 5 suggestions