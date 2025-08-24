import streamlit as st
import sys
import os
from pathlib import Path

# Add src to path - daha güvenli yol
current_dir = Path(__file__).parent
project_root = current_dir.parent
src_path = project_root / "src"
config_path = project_root / "config"
sys.path.insert(0, str(src_path))
sys.path.insert(0, str(config_path))

# Artık src olmadan import edebiliriz
from utils.api_handler import APIHandler
from settings import APP_CONFIG
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="AI Marketing Content Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
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
    
    /* Main Header */
    .hero-section {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 3rem 2rem;
        margin-bottom: 3rem;
        text-align: center;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 25px 45px rgba(0, 0, 0, 0.1);
        animation: fadeInUp 1s ease-out;
    }
    
    .hero-section h1 {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: none;
    }
    
    .hero-section p {
        font-size: 1.3rem;
        opacity: 0.9;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Feature Cards */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .feature-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        background: rgba(255, 255, 255, 0.18);
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transform: translateX(-100%);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        100% { transform: translateX(100%); }
    }
    
    .feature-card h4 {
        color: white;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .feature-card p {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1rem;
        line-height: 1.6;
        margin: 0;
    }
    
    /* Metrics Grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.12);
        transition: all 0.3s ease;
        position: relative;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        background: rgba(255, 255, 255, 0.15);
    }
    
    .metric-card h3 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card p {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.95rem;
        margin: 0;
        font-weight: 500;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #7c8df0 0%, #8a5aa8 100%);
    }
    
    /* Info Cards */
    .info-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
    }
    
    .info-card h3 {
        color: white;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .info-card ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .info-card li {
        padding: 0.5rem 0;
        color: rgba(255, 255, 255, 0.8);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .info-card li:last-child {
        border-bottom: none;
    }
    
    .info-card li::before {
        content: '✨';
        margin-right: 0.5rem;
    }
    
    /* Recent History Cards */
    .history-card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(8px);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: all 0.3s ease;
    }
    
    .history-card:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(4px);
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
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-section h1 {
            font-size: 2.5rem;
        }
        
        .hero-section {
            padding: 2rem 1rem;
        }
        
        .features-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .metrics-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
    /* Progress Bar */
    .progress-bar {
        width: 100%;
        height: 4px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 2px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        width: 0%;
        transition: width 0.3s ease;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'generation_history' not in st.session_state:
        st.session_state.generation_history = []
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = "gpt-3.5-turbo"

def load_history():
    """Load generation history from file"""
    try:
        if os.path.exists("data/history.json"):
            with open("data/history.json", "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return []

def save_history():
    """Save generation history to file"""
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/history.json", "w", encoding="utf-8") as f:
            json.dump(st.session_state.generation_history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"History kaydedilemedi: {str(e)}")

def main():
    initialize_session_state()
    
    # Load history on app start
    if not st.session_state.generation_history:
        st.session_state.generation_history = load_history()
    
    # Hero Section
    st.markdown("""
    <div class="hero-section animate-in">
        <h1>🚀 AI Marketing Content Generator</h1>
        <p>Pazarlama içeriklerinizi AI ile saniyeler içinde oluşturun, markanızı güçlendirin!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Ayarlar")
        
        # API Configuration
        with st.expander("🔑 API Ayarları", expanded=True):
            api_key = st.text_input(
                "OpenAI API Key",
                value=st.session_state.api_key,
                type="password",
                help="OpenAI API anahtarınızı girin",
                placeholder="sk-..."
            )
            
            if api_key:
                st.session_state.api_key = api_key
                # Validate API key
                if len(api_key) > 20:
                    st.success("✅ API anahtarı kaydedildi!")
                
            model = st.selectbox(
                "Model Seçimi",
                ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"],
                index=0,
                help="Kullanmak istediğiniz AI modelini seçin"
            )
            st.session_state.selected_model = model
            
            # Model info
            model_info = {
                "gpt-3.5-turbo": "⚡ Hızlı ve ekonomik",
                "gpt-4": "🎯 En yüksek kalite",
                "gpt-4-turbo-preview": "🚀 Gelişmiş özellikler"
            }
            st.info(model_info.get(model, ""))
        
        # Quick Stats
        st.markdown("## 📊 İstatistikler")
        
        total_content = len(st.session_state.generation_history)
        today_count = sum(1 for item in st.session_state.generation_history 
                        if item.get('date', '').startswith(datetime.now().strftime('%Y-%m-%d')))
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{total_content}</h3>
                <p>Toplam İçerik</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{today_count}</h3>
                <p>Bugün Üretilen</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Progress bar for daily usage
        daily_limit = 50  # Example daily limit
        progress_percentage = min((today_count / daily_limit) * 100, 100) if daily_limit > 0 else 0
        
        st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress_percentage}%"></div>
        </div>
        <small style="color: rgba(255,255,255,0.7);">Günlük kullanım: {today_count}/{daily_limit}</small>
        """, unsafe_allow_html=True)
        
        # Clear History
        if st.button("🗑️ Geçmişi Temizle", type="secondary"):
            st.session_state.generation_history = []
            save_history()
            st.success("✅ Geçmiş temizlendi!")
            st.rerun()
    
    # Main Content
    if not st.session_state.api_key:
        st.markdown("""
        <div class="info-card">
            <h3>⚠️ Başlamak için API Anahtarınız Gerekli</h3>
            <p>OpenAI API anahtarınızı yan panelden girerek hemen başlayabilirsiniz!</p>
            <p>💡 API anahtarınızı <a href="https://platform.openai.com/api-keys" target="_blank" style="color: #667eea;">OpenAI Platform</a> üzerinden alabilirsiniz.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Features Grid
    st.markdown("## 🎯 Güçlü Özellikler")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card animate-in" style="animation-delay: 0.1s;">
            <h4>📱 Social Media</h4>
            <p>Instagram, Twitter, LinkedIn ve Facebook için optimize edilmiş içerikler. Hashtag önerileri, emoji kullanımı ve platform-spesifik optimizasyonlar.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card animate-in" style="animation-delay: 0.3s;">
            <h4>🛍️ Ürün Açıklamaları</h4>
            <p>E-ticaret siteleriniz için satış odaklı, SEO uyumlu ve müşteri çeken ürün tanıtım metinleri.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card animate-in" style="animation-delay: 0.2s;">
            <h4>📧 Email Marketing</h4>
            <p>Newsletter, promosyonel emailler, hoş geldin mesajları ve müşteri geri kazanım kampanyaları için etkili email içerikleri.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card animate-in" style="animation-delay: 0.4s;">
            <h4>📝 Blog İçerikleri</h4>
            <p>Okuyucu dostu, bilgilendirici ve arama motorları için optimize edilmiş blog yazıları ve makaleler.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # How to Use Section
    st.markdown("## 🧭 Nasıl Kullanılır?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>🚀 Hızlı Başlangıç</h3>
            <ul>
                <li>Sol panelden API anahtarınızı girin</li>
                <li>İstediğiniz içerik türünü seçin</li>
                <li>Konu ve hedef kitlenizi belirtin</li>
                <li>Generate butonuna tıklayın</li>
                <li>İçeriğinizi indirin veya kopyalayın</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>✨ Pro İpuçları</h3>
            <ul>
                <li>Hedef kitlenizi net tanımlayın</li>
                <li>Marka sesinizi tutarlı kullanın</li>
                <li>A/B test için farklı tonlar deneyin</li>
                <li>Yaratıcılık seviyesini ayarlayın</li>
                <li>Sonuçları geçmişten takip edin</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent History Preview
    if st.session_state.generation_history:
        st.markdown("## 📋 Son Üretilen İçerikler")
        
        # Show last 3 items with better styling
        recent_items = st.session_state.generation_history[-3:]
        
        for i, item in enumerate(reversed(recent_items)):
            with st.expander(
                f"{item.get('type', 'İçerik')} - {item.get('platform', '')} - {item.get('date', 'Tarih yok')[:16]}",
                expanded=False
            ):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown(f"**📊 Tür:** {item.get('type', 'N/A')}")
                    st.markdown(f"**🎯 Platform:** {item.get('platform', 'N/A')}")
                    st.markdown(f"**📝 Konu:** {item.get('topic', 'N/A')}")
                
                with col2:
                    content_preview = item.get('content', '')
                    if len(content_preview) > 150:
                        content_preview = content_preview[:150] + "..."
                    
                    st.markdown("**İçerik Önizleme:**")
                    st.markdown(f"*{content_preview}*")
    
    # Footer Info
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.6); padding: 2rem;">
        <p>🤖 AI Marketing Content Generator v1.0 | Made with ❤️ using Streamlit & OpenAI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Save history on any changes
    save_history()

if __name__ == "__main__":
    main()