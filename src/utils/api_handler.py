import openai
import streamlit as st
from typing import Dict, List, Optional
import json
import time
import logging

class APIHandler:
    """Handle API calls to various AI services"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.client = openai.OpenAI(api_key=api_key)
        
    def generate_content(self, 
                        prompt: str, 
                        max_tokens: int = 1500, 
                        temperature: float = 0.7,
                        system_prompt: str = None) -> Dict:
        """
        Generate content using OpenAI API
        
        Args:
            prompt: User prompt
            max_tokens: Maximum tokens to generate
            temperature: Creativity level (0-1)
            system_prompt: System instructions
            
        Returns:
            Dict with generated content and metadata
        """
        try:
            # Prepare messages
            messages = []
            
            if system_prompt:
                messages.append({
                    "role": "system", 
                    "content": system_prompt
                })
            
            messages.append({
                "role": "user", 
                "content": prompt
            })
            
            # API call with progress indicator
            with st.spinner("AI içerik oluşturuyor..."):
                start_time = time.time()
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                
                end_time = time.time()
            
            # Extract content
            content = response.choices[0].message.content
            
            # Calculate metrics
            generation_time = end_time - start_time
            tokens_used = response.usage.total_tokens
            cost_estimate = self._calculate_cost(tokens_used)
            
            return {
                "success": True,
                "content": content,
                "model": self.model,
                "tokens_used": tokens_used,
                "generation_time": round(generation_time, 2),
                "cost_estimate": cost_estimate,
                "timestamp": time.time()
            }
            
        except openai.AuthenticationError:
            return {
                "success": False,
                "error": "API anahtarı geçersiz. Lütfen doğru API anahtarını girin.",
                "error_type": "authentication"
            }
            
        except openai.RateLimitError:
            return {
                "success": False,
                "error": "Rate limit aşıldı. Lütfen biraz bekleyip tekrar deneyin.",
                "error_type": "rate_limit"
            }
            
        except openai.InsufficientQuotaError:
            return {
                "success": False,
                "error": "API quota yetersiz. Lütfen billing bilgilerinizi kontrol edin.",
                "error_type": "quota"
            }
            
        except Exception as e:
            logging.error(f"API call failed: {str(e)}")
            return {
                "success": False,
                "error": f"Bir hata oluştu: {str(e)}",
                "error_type": "general"
            }
    
    def _calculate_cost(self, tokens: int) -> float:
        """Calculate estimated cost based on model and tokens"""
        # Pricing per 1K tokens (approximate, as of late 2024)
        pricing = {
            "gpt-3.5-turbo": 0.002,
            "gpt-4": 0.03,
            "gpt-4-turbo-preview": 0.01
        }
        
        base_price = pricing.get(self.model, 0.002)
        return round((tokens / 1000) * base_price, 4)
    
    def validate_api_key(self) -> bool:
        """Validate if API key is working"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            return True
        except:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        try:
            models = self.client.models.list()
            gpt_models = [
                model.id for model in models.data 
                if model.id.startswith(('gpt-3.5', 'gpt-4'))
            ]
            return sorted(gpt_models)
        except:
            return ["gpt-3.5-turbo", "gpt-4"]

class ContentAnalyzer:
    """Analyze generated content quality and metrics"""
    
    @staticmethod
    def analyze_content(content: str) -> Dict:
        """Analyze content and return metrics"""
        try:
            from textblob import TextBlob
            
            blob = TextBlob(content)
            
            # Basic metrics
            word_count = len(content.split())
            char_count = len(content)
            sentence_count = len(blob.sentences)
            
            # Readability (simple approximation)
            avg_sentence_length = word_count / max(sentence_count, 1)
            readability_score = max(0, 100 - (avg_sentence_length * 2))
            
            # Sentiment analysis
            sentiment = blob.sentiment
            
            # Extract hashtags and mentions
            words = content.split()
            hashtags = [word for word in words if word.startswith('#')]
            mentions = [word for word in words if word.startswith('@')]
            
            return {
                "word_count": word_count,
                "char_count": char_count,
                "sentence_count": sentence_count,
                "avg_sentence_length": round(avg_sentence_length, 1),
                "readability_score": round(readability_score, 1),
                "sentiment_polarity": round(sentiment.polarity, 2),
                "sentiment_subjectivity": round(sentiment.subjectivity, 2),
                "hashtags": hashtags,
                "mentions": mentions,
                "hashtag_count": len(hashtags),
                "mention_count": len(mentions)
            }
            
        except Exception as e:
            # Fallback basic analysis
            word_count = len(content.split())
            char_count = len(content)
            
            return {
                "word_count": word_count,
                "char_count": char_count,
                "sentence_count": content.count('.') + content.count('!') + content.count('?'),
                "error": f"Advanced analysis failed: {str(e)}"
            }

class PromptOptimizer:
    """Optimize prompts for better results"""
    
    @staticmethod
    def optimize_prompt(base_prompt: str, 
                       content_type: str, 
                       platform: str = None,
                       tone: str = "professional",
                       target_audience: str = None) -> str:
        """
        Optimize prompt based on content type and parameters
        
        Args:
            base_prompt: Base user prompt
            content_type: Type of content (social_media, email, etc.)
            platform: Platform specific requirements
            tone: Desired tone
            target_audience: Target audience description
        
        Returns:
            Optimized prompt string
        """
        
        # Platform-specific optimizations
        platform_specs = {
            "instagram": "Instagram için görsel odaklı, hashtag kullanımlı",
            "twitter": "Twitter için kısa (280 karakter), akılda kalıcı",
            "linkedin": "LinkedIn için profesyonel, iş odaklı",
            "facebook": "Facebook için engaging, community odaklı",
            "email": "Email için konu başlığı ve CTA içeren"
        }
        
        # Tone specifications
        tone_specs = {
            "professional": "profesyonel ve güvenilir",
            "casual": "samimi ve arkadaşça",
            "exciting": "heyecanlı ve enerji dolu",
            "informative": "bilgilendirici ve açıklayıcı",
            "persuasive": "ikna edici ve satış odaklı"
        }
        
        # Build optimized prompt
        optimized_prompt = base_prompt
        
        if platform and platform.lower() in platform_specs:
            optimized_prompt += f"\n\nPlatform özelikleri: {platform_specs[platform.lower()]}"
        
        if tone in tone_specs:
            optimized_prompt += f"\nTon: {tone_specs[tone]}"
        
        if target_audience:
            optimized_prompt += f"\nHedef kitle: {target_audience}"
        
        # Add general optimization instructions
        optimized_prompt += "\n\nLütfen içeriği yaratıcı, özgün ve hedef kitle için uygun olacak şekilde oluşturun."
        
        return optimized_prompt