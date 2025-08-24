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

# Modern CSS with glassmorphism and animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(-45deg, #667eea, #764ba2, #667eea, #f093fb);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Header */
    .page-header {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .page-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Platform Selection Cards */
    .platform-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .platform-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 2px solid transparent;
        position: relative;
        overflow: hidden;
    }
    
    .platform-card.selected {
        border: 2px solid rgba(255, 255, 255, 0.4);
        background: rgba(255, 255, 255, 0.15);
        transform: scale(1.05);
    }
    
    .platform-card:hover {
        transform: translateY(-4px) scale(1.02);
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
    }
    
    .platform-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s;
    }
    
    .platform-card:hover::before {
        left: 100%;
    }
    
    .platform-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .platform-name {
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0;
    }
    
    /* Form Sections */
    .form-section {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
    }
    
    .form-section h3 {
        color: white;
        font-weight: 600;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Content Preview */
    .content-preview {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        color: #333;
        position: relative;
        overflow: hidden;
    }
    
    .content-preview::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
    }
    
    .platform-preview-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(0,0,0,0.1);
    }
    
    .platform-preview-header h4 {
        margin: 0;
        color: #333;
        font-weight: 600;
    }
    
    .content-text {
        font-size: 1.1rem;
        line-height: 1.7;
        color: #444;
        white-space: pre-wrap;
        margin-bottom: 1.5rem;
    }
    
    .hashtag {
        color: #1da1f2;
        font-weight: 600;
    }
    
    .emoji {
        font-size: 1.2em;
    }
    
    /* Metrics Cards */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.15);
        transition: all 0.3s ease;
        color: white;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        background: rgba(255, 255, 255, 0.18);
    }
    
    .metric-card h3 {
        font-size: 2rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        color: white;
    }
    
    .metric-card p {
        font-size: 0.9rem;
        margin: 0;
        opacity: 0.9;
        color: white;
    }
    
    /* Action Buttons */
    .action-buttons {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .action-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    
    .action-button.secondary {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Platform Guidelines */
    .guidelines-card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(8px);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: white;
    }
    
    .guidelines-card strong {
        color: #f093fb;
    }
    
    /* Tips Section */
    .tips-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .tip-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
    }
    
    .tip-card h3 {
        color: white;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .tip-card ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .tip-card li {
        padding: 0.5rem 0;
        color: rgba(255, 255, 255, 0.8);
        position: relative;
        padding-left: 1.5rem;
    }
    
    .tip-card li::before {
        content: '✨';
        position: absolute;
        left: 0;
        top: 0.5rem;
    }
    
    /* Loading Animation */
    .loading-animation {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Character Limit Indicator */
    .char-limit {
        margin-top: 1rem;
        padding: 0.5rem;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .char-limit.good {
        background: rgba(40, 167, 69, 0.2);
        color: #28a745;
        border: 1px solid rgba(40, 167, 69, 0.3);
    }
    
    .char-limit.warning {
        background: rgba(255, 193, 7, 0.2);
        color: #ffc107;
        border: 1px solid rgba(255, 193, 7, 0.3);
    }
    
    .char-limit.danger {
        background: rgba(220, 53, 69, 0.2);
        color: #dc3545;
        border: 1px solid rgba(220, 53, 69, 0.3);
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .platform-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .metrics-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .action-buttons {
            flex-direction: column;
        }
        
        .tips-grid {
            grid-template-columns: 1fr;
        }
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
    # Header
    st.markdown("""
    <div class="page-header animate-in">
        <h1>📱 Social Media Content Generator</h1>
        <p>Sosyal medya platformları için viral potansiyeli yüksek içerikler oluşturun!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API key
    if 'api_key' not in st.session_state or not st.session_state.api_key:
        st.markdown("""
        <div class="form-section">
            <h3>⚠️ API Anahtarı Gerekli</h3>
            <p>Lütfen ana sayfadan OpenAI API anahtarınızı girin.</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()
    
    # Initialize generator
    generator = SocialMediaGenerator(
        st.session_state.api_key,
        st.session_state.get('selected_model', 'gpt-3.5-turbo')
    )
    
    # Platform Selection
    st.markdown("""
    <div class="form-section animate-in">
        <h3>📊 Platform Seçimi</h3>
    </div>
    """, unsafe_allow_html=True)
    
    platform_options = {
        "instagram": {"name": "Instagram", "icon": "📸", "color": "#E4405F"},
        "twitter": {"name": "Twitter/X", "icon": "🐦", "color": "#1DA1F2"},
        "linkedin": {"name": "LinkedIn", "icon": "💼", "color": "#0A66C2"},
        "facebook": {"name": "Facebook", "icon": "👥", "color": "#1877F2"}
    }
    
    # Create platform selection with custom styling
    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]
    
    selected_platform = st.selectbox(
        "Platform seçin:",
        list(platform_options.keys()),
        format_func=lambda x: f"{platform_options[x]['icon']} {platform_options[x]['name']}",
        key="platform_select"
    )
    
    platform_info = platform_options[selected_platform]
    
    # Platform specific guidelines
    platform_guidelines = {
        "instagram": {
            "char_limit": "2,200 karakter",
            "best_practices": "Görsel odaklı içerik, 5-30 hashtag, hikaye anlatımı, yüksek kalite görseller",
            "optimal_length": "150-300 kelime",
            "engagement_tips": "Story kullanın, UGC paylaşın, influencer işbirlikleri yapın"
        },
        "twitter": {
            "char_limit": "280 karakter",
            "best_practices": "Kısa ve öz mesajlar, trending hashtag'ler, thread'ler, güncel konular",
            "optimal_length": "71-100 karakter (en yüksek engagement)",
            "engagement_tips": "Retweet'leri teşvik edin, sorular sorun, viral konulara dahil olun"
        },
        "linkedin": {
            "char_limit": "3,000 karakter",
            "best_practices": "Profesyonel ton, sektör insights'ı, thought leadership, network building",
            "optimal_length": "150-300 kelime",
            "engagement_tips": "Uzman görüşleri paylaşın, case study'ler sunun, mesleki başarıları vurgulayın"
        },
        "facebook": {
            "char_limit": "63,206 karakter",
            "best_practices": "Community odaklı içerik, soru sorma, emoji kullanımı, yerel relevans",
            "optimal_length": "40-80 kelime",
            "engagement_tips": "Grup paylaşımları yapın, live video kullanın, etkinlik oluşturun"
        }
    }
    
    # Show platform guidelines
    with st.expander(f"{platform_info['icon']} {platform_info['name']} Rehberi ve İpuçları", expanded=False):
        guidelines = platform_guidelines[selected_platform]
        st.markdown(f"""
        <div class="guidelines-card">
            <p><strong>📏 Karakter Limiti:</strong> {guidelines['char_limit']}</p>
            <p><strong>✅ En İyi Uygulamalar:</strong> {guidelines['best_practices']}</p>
            <p><strong>📊 Optimal Uzunluk:</strong> {guidelines['optimal_length']}</p>
            <p><strong>🚀 Engagement İpuçları:</strong> {guidelines['engagement_tips']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Content Configuration
    st.markdown("""
    <div class="form-section animate-in" style="animation-delay: 0.2s;">
        <h3>⚙️ İçerik Ayarları</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Topic/Product
        topic = st.text_input(
            "🎯 Konu/Ürün/Hizmet:",
            placeholder="Örn: Yeni kahve çeşitlerimiz, Black Friday kampanyası, sürdürülebilirlik",
            help="Hakkında post oluşturmak istediğiniz ana konu"
        )
        
        # Target Audience
        target_audience = st.selectbox(
            "👥 Hedef Kitle:",
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
            "🎭 Ton ve Stil:",
            ["professional", "casual", "exciting", "informative", "persuasive"],
            format_func=lambda x: {
                "professional": "🎩 Profesyonel",
                "casual": "😊 Samimi & Dostça", 
                "exciting": "🚀 Heyecan Verici",
                "informative": "📚 Bilgilendirici",
                "persuasive": "💪 İkna Edici"
            }[x]
        )
    
    with col2:
        # Post Type
        post_type = st.selectbox(
            "📝 Post Türü:",
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
                "promotional": "🎯 Tanıtım & Satış",
                "educational": "📖 Eğitici & Bilgilendirici",
                "entertaining": "🎭 Eğlenceli & Viral", 
                "inspirational": "✨ İlham Verici",
                "behind_scenes": "🎬 Perde Arkası",
                "user_generated": "👥 Kullanıcı İçeriği",
                "announcement": "📢 Duyuru & Haber",
                "question": "❓ Soru & Anket"
            }[x]
        )
        
        # Include elements with better styling
        st.markdown("**🔧 Dahil Edilecek Unsurlar:**")
        
        col_a, col_b = st.columns(2)
        with col_a:
            include_hashtags = st.checkbox("# Hashtag'ler", value=True)
            include_emojis = st.checkbox("😀 Emoji'ler", value=True)
        
        with col_b:
            include_cta = st.checkbox("📢 Call-to-Action", value=True)
            auto_optimize = st.checkbox("🤖 Otomatik Optimizasyon", value=True)
    
    # Advanced options
    with st.expander("🔧 Gelişmiş Ayarlar & Özelleştirme", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            custom_instructions = st.text_area(
                "📋 Özel Talimatlar:",
                placeholder="Örn: Marka değerlerimizi vurgula, yeşil yaşam temasını kullan, genç dili kullan",
                height=100,
                help="AI'ya özel talimatlar verebilirsiniz"
            )
            
            brand_voice = st.selectbox(
                "🎤 Marka Sesi:",
                ["Standart", "Lüks & Premium", "Genç & Modern", "Güvenilir & Klasik", "İnovatif & Teknolojik"],
                help="Markanızın genel karakterini yansıtan ses tonu"
            )
        
        with col2:
            creativity_level = st.slider(
                "🎨 Yaratıcılık Seviyesi:",
                min_value=0.1,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Düşük = Daha güvenli ve tahmin edilebilir, Yüksek = Daha yaratıcı ve risk alıcı"
            )
            
            content_length = st.select_slider(
                "📏 İçerik Uzunluğu Tercihi:",
                options=["Kısa", "Orta", "Uzun"],
                value="Orta",
                help="Platform limitlerini göz önünde bulundurarak içerik uzunluğu"
            )
    
    # Generate Content Button
    if st.button("🚀 İçerik Oluştur", type="primary", key="generate_btn"):
        if not topic:
            st.error("❌ Lütfen bir konu girin!")
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
        
        # Add brand voice to custom instructions
        if brand_voice != "Standart":
            brand_voice_instructions = {
                "Lüks & Premium": "Lüks, elit ve premium bir marka sesi kullan",
                "Genç & Modern": "Genç, modern ve trendy bir dil kullan", 
                "Güvenilir & Klasik": "Güvenilir, klasik ve saygın bir ton kullan",
                "İnovatif & Teknolojik": "İnovatif, teknolojik ve gelecek odaklı bir yaklaşım kullan"
            }
            generation_params['custom_instructions'] += f" {brand_voice_instructions.get(brand_voice, '')}"
        
        # Generate content with progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with st.spinner():
            status_text.text(f"🔄 {platform_info['icon']} {platform_info['name']} için içerik oluşturuluyor...")
            progress_bar.progress(25)
            
            result = generator.generate_post(**generation_params)
            progress_bar.progress(75)
            
            if result['success']:
                progress_bar.progress(100)
                status_text.text("✅ İçerik başarıyla oluşturuldu!")
                
                content = result['content']
                
                # Display generated content with beautiful styling
                st.markdown("""
                <div class="content-preview animate-in">
                    <div class="platform-preview-header">
                        <span style="font-size: 2rem;">{}</span>
                        <h4>{} Postu</h4>
                        <span style="background: {}; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">LIVE</span>
                    </div>
                    <div class="content-text">{}</div>
                </div>
                """.format(
                    platform_info['icon'], 
                    platform_info['name'],
                    platform_info['color'],
                    content.replace('\n', '<br>')
                ), unsafe_allow_html=True)
                
                # Content analysis
                analyzer = ContentAnalyzer()
                metrics = analyzer.analyze_content(content)
                
                # Display metrics with beautiful cards
                st.markdown("## 📊 İçerik Analizi ve Performans Tahmini")
                
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>{metrics.get('word_count', 0)}</h3>
                        <p>💬 Kelime Sayısı</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>{metrics.get('char_count', 0)}</h3>
                        <p>📏 Karakter</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>{metrics.get('hashtag_count', 0)}</h3>
                        <p># Hashtag</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    reading_time = max(1, metrics.get('word_count', 0) // 200)  # Approx reading time
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>{reading_time}s</h3>
                        <p>⏱️ Okuma Süresi</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col5:
                    sentiment = metrics.get('sentiment_polarity', 0)
                    if sentiment > 0.3:
                        sentiment_score, sentiment_emoji = "Pozitif", "😊"
                    elif sentiment > -0.1:
                        sentiment_score, sentiment_emoji = "Nötr", "😐"
                    else:
                        sentiment_score, sentiment_emoji = "Negatif", "😔"
                    
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>{sentiment_emoji}</h3>
                        <p>💭 {sentiment_score}</p>
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
                remaining = limit - char_count
                
                if char_count > limit:
                    limit_class = "danger"
                    limit_message = f"⚠️ İçerik {platform_info['name']} karakter limitini ({limit:,}) aşıyor! {char_count - limit} karakter fazla."
                elif remaining < 50:
                    limit_class = "warning"
                    limit_message = f"⚡ Limit yaklaşıyor! {remaining} karakter kaldı."
                else:
                    limit_class = "good"
                    limit_message = f"✅ İçerik uygun! {remaining:,} karakter kaldı."
                
                st.markdown(f'<div class="char-limit {limit_class}">{limit_message}</div>', unsafe_allow_html=True)
                
                # Action buttons with modern styling
                st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
                
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    if st.button("📋 Kopyala", key="copy_btn"):
                        # Here you would implement clipboard functionality
                        st.success("✅ İçerik kopyalandı!")
                
                with col2:
                    # Download as text file
                    st.download_button(
                        label="📥 TXT İndir",
                        data=content,
                        file_name=f"{selected_platform}_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                
                with col3:
                    # Download as JSON with metadata
                    content_json = {
                        "platform": platform_info['name'],
                        "content": content,
                        "metrics": metrics,
                        "settings": generation_params,
                        "generated_at": datetime.now().isoformat()
                    }
                    st.download_button(
                        label="📊 JSON İndir",
                        data=json.dumps(content_json, ensure_ascii=False, indent=2),
                        file_name=f"{selected_platform}_post_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                
                with col4:
                    if st.button("🔄 Yeniden Üret", key="regenerate_btn"):
                        st.rerun()
                
                with col5:
                    if st.button("✨ Optimize Et", key="optimize_btn"):
                        st.info("🚀 İçerik optimizasyon özelliği yakında geliyor!")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
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
                progress_bar.progress(0)
                status_text.text("")
                st.error(f"❌ Hata: {result['error']}")
    
    # Tips and best practices with modern cards
    st.markdown("---")
    st.markdown("## 💡 Pro İpuçları ve En İyi Uygulamalar")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="tip-card animate-in" style="animation-delay: 0.1s;">
            <h3>✅ En İyi Uygulamalar</h3>
            <ul>
                <li><strong>Hedef kitlenizi</strong> net olarak tanımlayın</li>
                <li><strong>Platform özelliklerini</strong> göz önünde bulundurun</li>
                <li><strong>Görsel içerik</strong> planınızı yapın</li>
                <li><strong>Engagement</strong> için sorular sorun</li>
                <li><strong>Hashtag araştırması</strong> yapın</li>
                <li><strong>Posting zamanını</strong> optimize edin</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="tip-card animate-in" style="animation-delay: 0.3s;">
            <h3>📈 Engagement Artırma</h3>
            <ul>
                <li><strong>Story-telling</strong> tekniklerini kullanın</li>
                <li><strong>User-generated content</strong> teşvik edin</li>
                <li><strong>Trending konulara</strong> dahil olun</li>
                <li><strong>Cross-platform</strong> paylaşım yapın</li>
                <li><strong>Community building</strong> odaklı yaklaşım</li>
                <li><strong>Analitikleri</strong> düzenli takip edin</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tip-card animate-in" style="animation-delay: 0.2s;">
            <h3>🚫 Kaçınılacaklar</h3>
            <ul>
                <li>Çok uzun ve karmaşık metinler</li>
                <li>Alakasız veya spam hashtag'ler</li>
                <li>Aşırı tanıtım odaklı içerik</li>
                <li>Tutarsız marka sesi kullanımı</li>
                <li>Hedef kitle dışı dil ve ton</li>
                <li>Düşük kaliteli görsel kullanımı</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="tip-card animate-in" style="animation-delay: 0.4s;">
            <h3>🎯 Platform Özel İpuçları</h3>
            <ul>
                <li><strong>Instagram:</strong> Stories ve Reels kullanın</li>
                <li><strong>Twitter:</strong> Thread'ler oluşturun</li>
                <li><strong>LinkedIn:</strong> Industry insights paylaşın</li>
                <li><strong>Facebook:</strong> Community grupları kullanın</li>
                <li><strong>Tüm platformlar:</strong> Tutarlı branding</li>
                <li><strong>A/B testing</strong> yapmayı unutmayın</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()