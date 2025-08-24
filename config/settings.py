import os
from typing import Dict, List

# App Configuration
APP_CONFIG = {
    'name': 'AI Marketing Content Generator',
    'version': '1.0.0',
    'description': 'AI-powered marketing content generation tool',
    'author': 'Ali Ibrahim',
    'github': 'https://github.com/aliibyrm/ai-marketing-content-generator'
}

# API Configuration
API_CONFIG = {
    'openai': {
        'default_model': 'gpt-3.5-turbo',
        'available_models': [
            'gpt-3.5-turbo',
            'gpt-4',
            'gpt-4-turbo-preview'
        ],
        'max_tokens': {
            'gpt-3.5-turbo': 4096,
            'gpt-4': 8192,
            'gpt-4-turbo-preview': 128000
        },
        'pricing': {  # Per 1K tokens (approximate)
            'gpt-3.5-turbo': 0.002,
            'gpt-4': 0.03,
            'gpt-4-turbo-preview': 0.01
        }
    }
}

# Platform Configuration
PLATFORM_CONFIG = {
    'instagram': {
        'name': 'Instagram',
        'icon': '📸',
        'color': '#E4405F',
        'char_limit': 2200,
        'optimal_length': '150-300 words',
        'best_practices': [
            'Visual-first content',
            'Use 5-30 hashtags',
            'Story-driven posts',
            'High-quality images',
            'Engaging captions'
        ],
        'content_types': [
            'Photo posts',
            'Carousel posts', 
            'Reels',
            'Stories',
            'IGTV'
        ]
    },
    'twitter': {
        'name': 'Twitter/X',
        'icon': '🐦',
        'color': '#1DA1F2',
        'char_limit': 280,
        'optimal_length': '71-100 characters',
        'best_practices': [
            'Concise messaging',
            'Use trending hashtags',
            'Thread for longer content',
            'Engage in conversations',
            'Share news and insights'
        ],
        'content_types': [
            'Tweets',
            'Threads',
            'Retweets',
            'Quote tweets',
            'Spaces'
        ]
    },
    'linkedin': {
        'name': 'LinkedIn',
        'icon': '💼', 
        'color': '#0A66C2',
        'char_limit': 3000,
        'optimal_length': '150-300 words',
        'best_practices': [
            'Professional tone',
            'Industry insights',
            'Network building',
            'Thought leadership',
            'Value-driven content'
        ],
        'content_types': [
            'Professional updates',
            'Industry articles',
            'Company news',
            'Career insights',
            'Networking posts'
        ]
    },
    'facebook': {
        'name': 'Facebook',
        'icon': '👥',
        'color': '#1877F2', 
        'char_limit': 63206,
        'optimal_length': '40-80 words',
        'best_practices': [
            'Community focus',
            'Shareable content',
            'Ask questions',
            'Use emotions',
            'Local relevance'
        ],
        'content_types': [
            'Status updates',
            'Photo/video posts',
            'Events',
            'Polls',
            'Live videos'
        ]
    }
}

# Content Types Configuration
CONTENT_TYPES = {
    'promotional': {
        'name': '🎯 Promotional',
        'description': 'Product/service promotion',
        'structure': 'Attention + Value proposition + Features + CTA',
        'best_for': ['Product launches', 'Sales campaigns', 'Special offers']
    },
    'educational': {
        'name': '📖 Educational', 
        'description': 'Informative and teaching content',
        'structure': 'Problem + Solution + Steps + Resources',
        'best_for': ['How-to guides', 'Tips & tricks', 'Industry insights']
    },
    'entertaining': {
        'name': '🎭 Entertaining',
        'description': 'Fun and engaging content',
        'structure': 'Hook + Entertainment + Community engagement',
        'best_for': ['Viral content', 'Memes', 'Behind-the-scenes']
    },
    'inspirational': {
        'name': '✨ Inspirational',
        'description': 'Motivational and uplifting',
        'structure': 'Inspiration + Story/example + Motivation + CTA',
        'best_for': ['Success stories', 'Motivation', 'Brand values']
    },
    'behind_scenes': {
        'name': '🎬 Behind the Scenes',
        'description': 'Company culture and processes',
        'structure': 'Curiosity hook + Process + Personal touch',
        'best_for': ['Company culture', 'Process transparency', 'Team highlights']
    },
    'user_generated': {
        'name': '👥 User Generated',
        'description': 'Customer/user content showcase',
        'structure': 'Thank you + Content share + Community celebration',
        'best_for': ['Customer testimonials', 'Reviews', 'Community building']
    },
    'announcement': {
        'name': '📢 Announcement',
        'description': 'News and updates',
        'structure': 'Exciting news + Details + Benefits + Next steps',
        'best_for': ['Product releases', 'Company news', 'Updates']
    },
    'question': {
        'name': '❓ Question/Poll',
        'description': 'Engagement-focused content',
        'structure': 'Question + Context + Options + Community invite',
        'best_for': ['Market research', 'Engagement', 'Community feedback']
    }
}

# Tone Configuration
TONE_CONFIG = {
    'professional': {
        'name': '🎩 Professional',
        'description': 'Formal, trustworthy, expert',
        'keywords': ['expertise', 'reliability', 'quality', 'professional'],
        'avoid': ['slang', 'excessive emoji', 'casual language']
    },
    'casual': {
        'name': '😊 Casual',
        'description': 'Friendly, approachable, conversational',
        'keywords': ['friendly', 'conversational', 'relatable', 'easy-going'],
        'avoid': ['overly formal', 'jargon', 'stiff language']
    },
    'exciting': {
        'name': '🚀 Exciting',
        'description': 'Energetic, enthusiastic, motivational',
        'keywords': ['amazing', 'incredible', 'exciting', 'awesome'],
        'avoid': ['boring', 'passive', 'understated']
    },
    'informative': {
        'name': '📚 Informative',
        'description': 'Educational, clear, fact-based',
        'keywords': ['learn', 'discover', 'understand', 'knowledge'],
        'avoid': ['opinion-heavy', 'promotional', 'emotional']
    },
    'persuasive': {
        'name': '💪 Persuasive',
        'description': 'Convincing, action-oriented, sales-focused',
        'keywords': ['proven', 'guaranteed', 'results', 'transform'],
        'avoid': ['hesitant', 'uncertain', 'weak CTAs']
    }
}

# Target Audience Configuration
TARGET_AUDIENCES = {
    'general': {
        'name': 'Genel Kitle',
        'age_range': '18-65',
        'characteristics': 'Broad appeal, diverse interests',
        'content_style': 'Universal, accessible language'
    },
    'young_adults': {
        'name': '18-25 Yaş Gençler',
        'age_range': '18-25', 
        'characteristics': 'Tech-savvy, social media native, trend-conscious',
        'content_style': 'Trendy, visual, quick consumption'
    },
    'professionals': {
        'name': '25-35 Yaş Profesyoneller',
        'age_range': '25-35',
        'characteristics': 'Career-focused, time-conscious, value-driven',
        'content_style': 'Professional, efficient, actionable'
    },
    'mature_adults': {
        'name': '35+ Yaş Yetişkinler',
        'age_range': '35+',
        'characteristics': 'Experienced, quality-focused, family-oriented',
        'content_style': 'Detailed, trustworthy, relationship-building'
    },
    'female_audience': {
        'name': 'Kadın Hedef Kitle',
        'age_range': 'All ages',
        'characteristics': 'Diverse interests, community-oriented, detail-focused',
        'content_style': 'Inclusive, community-building, authentic'
    },
    'male_audience': {
        'name': 'Erkek Hedef Kitle', 
        'age_range': 'All ages',
        'characteristics': 'Direct communication, solution-focused, achievement-oriented',
        'content_style': 'Direct, results-focused, practical'
    },
    'parents': {
        'name': 'Ebeveynler',
        'age_range': '25-50',
        'characteristics': 'Family-focused, time-limited, value-conscious',
        'content_style': 'Family-friendly, practical, time-saving'
    },
    'entrepreneurs': {
        'name': 'Girişimciler',
        'age_range': '25-55',
        'characteristics': 'Innovation-focused, risk-taking, growth-minded',
        'content_style': 'Inspirational, strategic, growth-oriented'
    },
    'tech_enthusiasts': {
        'name': 'Teknoloji Meraklıları',
        'age_range': '18-45',
        'characteristics': 'Early adopters, detail-oriented, tech-savvy',
        'content_style': 'Technical, innovative, feature-focused'
    },
    'fashion_lovers': {
        'name': 'Moda Severler',
        'age_range': '16-40',
        'characteristics': 'Style-conscious, trend-following, visual-oriented',
        'content_style': 'Visual, trendy, aspirational'
    }
}

# Generation Settings
GENERATION_SETTINGS = {
    'default_max_tokens': 1500,
    'default_temperature': 0.7,
    'max_retries': 3,
    'timeout_seconds': 30,
    'history_limit': 100,
    'export_formats': ['txt', 'json', 'csv', 'pdf'],
    'supported_languages': ['tr', 'en'],
    'default_language': 'tr'
}

# File Paths
PATHS = {
    'data_dir': 'data',
    'exports_dir': 'data/exports',
    'templates_dir': 'data/templates',
    'history_file': 'data/history.json',
    'settings_file': 'data/user_settings.json',
    'logs_dir': 'logs'
}

# UI Configuration
UI_CONFIG = {
    'primary_color': '#667eea',
    'secondary_color': '#764ba2',
    'success_color': '#28a745',
    'warning_color': '#ffc107',
    'error_color': '#dc3545',
    'info_color': '#17a2b8',
    'sidebar_width': 300,
    'max_content_width': 1200
}

# Feature Flags
FEATURES = {
    'social_media_generator': True,
    'email_marketing_generator': True,
    'product_description_generator': True,
    'blog_post_generator': True,
    'analytics_dashboard': True,
    'export_functionality': True,
    'history_tracking': True,
    'multi_language_support': False,  # Future feature
    'ai_model_comparison': False,     # Future feature
    'collaboration_features': False  # Future feature
}

# Environment Variables
def get_env_config():
    """Get configuration from environment variables"""
    return {
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY'),
        'debug_mode': os.getenv('DEBUG', 'False').lower() == 'true',
        'log_level': os.getenv('LOG_LEVEL', 'INFO'),
        'environment': os.getenv('ENVIRONMENT', 'development')
    }

# Validation Rules
VALIDATION_RULES = {
    'min_topic_length': 3,
    'max_topic_length': 200,
    'min_custom_instructions_length': 0,
    'max_custom_instructions_length': 1000,
    'max_hashtags_count': 30,
    'min_content_length': 10,
    'max_content_length': 10000
}

# Error Messages
ERROR_MESSAGES = {
    'api_key_missing': 'API anahtarı eksik. Lütfen ayarlardan API anahtarınızı girin.',
    'api_key_invalid': 'API anahtarı geçersiz. Lütfen doğru API anahtarını girin.',
    'rate_limit_exceeded': 'Rate limit aşıldı. Lütfen biraz bekleyip tekrar deneyin.',
    'quota_exceeded': 'API quota yetersiz. Lütfen billing bilgilerinizi kontrol edin.',
    'topic_too_short': f'Konu en az {VALIDATION_RULES["min_topic_length"]} karakter olmalıdır.',
    'topic_too_long': f'Konu en fazla {VALIDATION_RULES["max_topic_length"]} karakter olabilir.',
    'generation_failed': 'İçerik oluşturulurken bir hata oluştu. Lütfen tekrar deneyin.',
    'export_failed': 'İçerik dışa aktarılırken bir hata oluştu.',
    'history_load_failed': 'Geçmiş yüklenirken bir hata oluştu.'
}

# Success Messages
SUCCESS_MESSAGES = {
    'content_generated': '✅ İçerik başarıyla oluşturuldu!',
    'content_exported': '✅ İçerik başarıyla dışa aktarıldı!',
    'settings_saved': '✅ Ayarlar kaydedildi!',
    'history_cleared': '✅ Geçmiş temizlendi!',
    'api_key_validated': '✅ API anahtarı doğrulandı!'
}