import streamlit as st
import sys
import os
from pathlib import Path
import json
from datetime import datetime
import emoji

# Add src to path - daha güvenli yol
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from utils.api_handler import APIHandler, ContentAnalyzer, PromptOptimizer
from generators.social_media_generator import SocialMediaGenerator

st.set_page_config(
    page_title="Social Media Content Generator",
    page_icon="📱",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .platform-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem;
        cursor: pointer;
        transition: transform 0.2s;
    }
    
    .platform-card:hover {
        transform: translateY(-2px);
    }
    
    .content-preview {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        font-family: 'Georgia', serif;
        line-height: 1.6;
        color: #000000;
    }
    
    .metrics-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
        color: #000000;
    }
    
    .metrics-card h3 {
        color: #000000;
        font-weight: bold;
        margin: 0;
        font-size: 1.5rem;
    }
    
    .metrics-card p {
        color: #000000;
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
    }
    
    .hashtag {
        color: #1da1f2;
        font-weight: bold;
    }
    
    .mention {
        color: #1da1f2;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def save_to_history(content_data):
    """Save generated content to history"""
    if 'generation_history' not in st.session_state:
        st.session_state.generation_history = []
    
    history_item = {
        'type': 'Social Media',
        'platform': content_data.get('platform', ''),
        'topic': content_data.get('topic', ''),
        'content': content_data.get('content', ''),
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'metrics': content_data.get('metrics', {}),
        'settings': content_data.get('settings', {})
    }
    
    st.session_state.generation_history.append(history_item)
    
    # Keep only last 50 items
    if len(st.session_state.generation_history) > 50:
        st.session_state.generation_history = st.session_state.generation_history[-50:]

def main():
    st.markdown("# 📱 Social Media Content Generator")
    st.markdown("Sosyal medya platformları için etkileyici içerikler oluşturun!")
    
    # Check API key
    if 'api_key' not in st.session_state or not st.session_state.api_key:
        st.warning("⚠️ Lütfen ana sayfadan OpenAI API anahtarınızı girin.")
        st.stop()
    
    # Initialize generator
    generator = SocialMediaGenerator(
        st.session_state.api_key,
        st.session_state.get('selected_model', 'gpt-3.5-turbo')
    )
    
    # Platform Selection
    st.markdown("## 📊 Platform Seçimi")
    
    col1, col2, col3, col4 = st.columns(4)
    
    platform_options = {
        "instagram": {"name": "Instagram", "icon": "📸", "color": "#E4405F"},
        "twitter": {"name": "Twitter/X", "icon": "🐦", "color": "#1DA1F2"},
        "linkedin": {"name": "LinkedIn", "icon": "💼", "color": "#0A66C2"},
        "facebook": {"name": "Facebook", "icon": "👥", "color": "#1877F2"}
    }
    
    selected_platform = st.selectbox(
        "Platform:",
        list(platform_options.keys()),
        format_func=lambda x: f"{platform_options[x]['icon']} {platform_options[x]['name']}"
    )
    
    platform_info = platform_options[selected_platform]
    
    # Platform specific guidelines
    platform_guidelines = {
        "instagram": {
            "char_limit": "2200 karakter",
            "best_practices": "Görsel odaklı, 5-30 hashtag, hikaye anlatımı",
            "optimal_length": "150-300 kelime"
        },
        "twitter": {
            "char_limit": "280 karakter",
            "best_practices": "Kısa ve öz, trending hashtag'ler, engagement odaklı",
            "optimal_length": "71-100 karakter (en iyi engagement)"
        },
        "linkedin": {
            "char_limit": "3000 karakter",
            "best_practices": "Profesyonel ton, değer odaklı, call-to-action",
            "optimal_length": "150-300 kelime"
        },
        "facebook": {
            "char_limit": "63,206 karakter",
            "best_practices": "Community odaklı, soru sorma, emoji kullanımı",
            "optimal_length": "40-80 kelime"
        }
    }
    
    # Show platform info
    with st.expander(f"{platform_info['icon']} {platform_info['name']} Rehberi", expanded=False):
        guidelines = platform_guidelines[selected_platform]
        st.markdown(f"""
        **Karakter Limiti:** {guidelines['char_limit']}
        
        **En İyi Uygulamalar:** {guidelines['best_practices']}
        
        **Optimal Uzunluk:** {guidelines['optimal_length']}
        """)
    
    # Content Configuration
    st.markdown("## ⚙️ İçerik Ayarları")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Topic/Product
        topic = st.text_input(
            "Konu/Ürün/Hizmet:",
            placeholder="Örn: Yeni kahve çeşitlerimiz, Black Friday kampanyası",
            help="Hakkında post oluşturmak istediğiniz konu"
        )
        
        # Target Audience
        target_audience = st.selectbox(
            "Hedef Kitle:",
            [
                "Genel Kitle",
                "18-25 Yaş Gençler", 
                "25-35 Yaş Profesyoneller",
                "35+ Yaş Yetişkinler",
                "Kadın Hedef Kitle",
                "Erkek Hedef Kitle",
                "Ebeveynler",
                "Girişimciler",
                "Teknoloji Meraklıları",
                "Moda Severler"
            ]
        )
        
        # Tone
        tone = st.selectbox(
            "Ton:",
            ["professional", "casual", "exciting", "informative", "persuasive"],
            format_func=lambda x: {
                "professional": "🎩 Profesyonel",
                "casual": "😊 Samimi", 
                "exciting": "🚀 Heyecanlı",
                "informative": "📚 Bilgilendirici",
                "persuasive": "💪 İkna Edici"
            }[x]
        )
    
    with col2:
        # Post Type
        post_type = st.selectbox(
            "Post Türü:",
            [
                "promotional",
                "educational", 
                "entertaining",
                "inspirational",
                "behind_scenes",
                "user_generated",
                "announcement",
                "question"
            ],
            format_func=lambda x: {
                "promotional": "🎯 Tanıtım",
                "educational": "📖 Eğitici",
                "entertaining": "🎭 Eğlenceli", 
                "inspirational": "✨ İlham Verici",
                "behind_scenes": "🎬 Perde Arkası",
                "user_generated": "👥 Kullanıcı İçeriği",
                "announcement": "📢 Duyuru",
                "question": "❓ Soru"
            }[x]
        )
        
        # Include elements
        include_hashtags = st.checkbox("Hashtag'ler dahil et", value=True)
        include_emojis = st.checkbox("Emoji'ler dahil et", value=True)
        include_cta = st.checkbox("Call-to-Action dahil et", value=True)
        
        # Advanced options
        with st.expander("🔧 Gelişmiş Ayarlar"):
            custom_instructions = st.text_area(
                "Özel Talimatlar:",
                placeholder="Örn: Marka değerlerimizi vurgula, yeşil yaşam temasını kullan",
                height=80
            )
            
            creativity_level = st.slider(
                "Yaratıcılık Seviyesi:",
                min_value=0.1,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Düşük = Daha tahmin edilebilir, Yüksek = Daha yaratıcı"
            )
    
    # Generate Content
    if st.button("🚀 İçerik Oluştur", type="primary"):
        if not topic:
            st.error("Lütfen bir konu girin!")
            return
        
        # Prepare generation parameters
        generation_params = {
            'platform': selected_platform,
            'topic': topic,
            'target_audience': target_audience,
            'tone': tone,
            'post_type': post_type,
            'include_hashtags': include_hashtags,
            'include_emojis': include_emojis,
            'include_cta': include_cta,
            'custom_instructions': custom_instructions,
            'creativity_level': creativity_level
        }
        
        # Generate content
        with st.spinner(f"{platform_info['icon']} {platform_info['name']} için içerik oluşturuluyor..."):
            result = generator.generate_post(**generation_params)
        
        if result['success']:
            content = result['content']
            
            # Display generated content
            st.markdown("## ✨ Üretilen İçerik")
            
            # Content preview with platform styling
            st.markdown(f"""
            <div class="content-preview">
                <h4>{platform_info['icon']} {platform_info['name']} Postu</h4>
                <div style="white-space: pre-wrap; font-size: 16px;">
                    {content}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Content analysis
            analyzer = ContentAnalyzer()
            metrics = analyzer.analyze_content(content)
            
            # Display metrics
            st.markdown("## 📊 İçerik Analizi")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metrics-card">
                    <h3>{metrics.get('word_count', 0)}</h3>
                    <p>Kelime</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metrics-card">
                    <h3>{metrics.get('char_count', 0)}</h3>
                    <p>Karakter</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metrics-card">
                    <h3>{metrics.get('hashtag_count', 0)}</h3>
                    <p>Hashtag</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                sentiment = metrics.get('sentiment_polarity', 0)
                sentiment_emoji = "😊" if sentiment > 0.1 else "😐" if sentiment > -0.1 else "😔"
                st.markdown(f"""
                <div class="metrics-card">
                    <h3>{sentiment_emoji}</h3>
                    <p>Sentiment</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Platform specific feedback
            char_count = metrics.get('char_count', 0)
            platform_limits = {
                'twitter': 280,
                'instagram': 2200,
                'linkedin': 3000,
                'facebook': 63206
            }
            
            limit = platform_limits.get(selected_platform, 3000)
            if char_count > limit:
                st.warning(f"⚠️ İçerik {platform_info['name']} karakter limitini ({limit}) aşıyor!")
            else:
                remaining = limit - char_count
                st.success(f"✅ İçerik uygun! {remaining} karakter kaldı.")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📋 Kopyala"):
                    st.write("İçerik panoya kopyalandı!")
                    # Note: Actual clipboard functionality requires additional setup
            
            with col2:
                # Download as text file
                st.download_button(
                    label="📥 İndir (.txt)",
                    data=content,
                    file_name=f"{selected_platform}_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
            
            with col3:
                if st.button("🔄 Yeniden Üret"):
                    st.rerun()
            
            # Save to history
            content_data = {
                'platform': platform_info['name'],
                'topic': topic,
                'content': content,
                'metrics': metrics,
                'settings': generation_params
            }
            save_to_history(content_data)
            
        else:
            st.error(f"❌ Hata: {result['error']}")
    
    # Tips and best practices
    st.markdown("---")
    st.markdown("## 💡 İpuçları")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### ✅ En İyi Uygulamalar
        - **Hedef kitlenizi** tanıyın
        - **Platform özelliklerini** göz önünde bulundurun
        - **Görsel içerik** ekleyin
        - **Engagement** için sorular sorun
        - **Hashtag araştırması** yapın
        """)
    
    with col2:
        st.markdown("""
        ### 🚫 Kaçınılacaklar
        - Çok uzun metinler
        - Alakasız hashtag'ler
        - Aşırı tanıtım
        - Spam benzeri içerik
        - Hedef kitleden uzak dil
        """)

if __name__ == "__main__":
    main()