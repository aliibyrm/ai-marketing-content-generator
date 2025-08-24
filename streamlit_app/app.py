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

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        color: #000000;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        color: #000000;
    }
    
    .metric-card h3 {
        color: #000000;
        font-weight: bold;
        margin: 0;
        font-size: 1.8rem;
    }
    
    .metric-card p {
        color: #000000;
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-weight: bold;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Genel metin rengi */
    .main .block-container {
        color: #ffffff;
    }
    
    .stMarkdown {
        color: #ffffff;
    }
    
    /* Sadece kartlardaki metinler siyah olsun */
    .feature-card h4,
    .feature-card p {
        color: #000000;
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
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 AI Marketing Content Generator</h1>
        <p>Pazarlama içeriklerinizi AI ile dakikalar içinde oluşturun!</p>
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
                help="OpenAI API anahtarınızı girin"
            )
            
            if api_key:
                st.session_state.api_key = api_key
                
            model = st.selectbox(
                "Model Seçimi",
                ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"],
                index=0,
                help="Kullanmak istediğiniz AI modelini seçin"
            )
            st.session_state.selected_model = model
        
        # Quick Stats
        st.markdown("## 📊 İstatistikler")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>{}</h3>
                <p>Toplam İçerik</p>
            </div>
            """.format(len(st.session_state.generation_history)), unsafe_allow_html=True)
        
        with col2:
            today_count = sum(1 for item in st.session_state.generation_history 
                            if item.get('date', '').startswith(datetime.now().strftime('%Y-%m-%d')))
            st.markdown("""
            <div class="metric-card">
                <h3>{}</h3>
                <p>Bugünkü İçerik</p>
            </div>
            """.format(today_count), unsafe_allow_html=True)
        
        # Clear History
        if st.button("🗑️ Geçmişi Temizle", type="secondary"):
            st.session_state.generation_history = []
            save_history()
            st.success("Geçmiş temizlendi!")
            st.rerun()
    
    # Main Content
    if not st.session_state.api_key:
        st.warning("⚠️ Lütfen önce OpenAI API anahtarınızı yan panelden girin.")
        st.info("💡 API anahtarınızı [OpenAI Platform](https://platform.openai.com/api-keys) üzerinden alabilirsiniz.")
        return
    
    # Feature Cards
    st.markdown("## 🎯 Özellikler")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>📱 Social Media</h4>
            <p>Instagram, Twitter, LinkedIn için içerik</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>📧 Email Marketing</h4>
            <p>Etkili email kampanyaları</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>🛍️ Ürün Açıklamaları</h4>
            <p>Satış odaklı ürün tanıtımları</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <h4>📝 Blog Yazıları</h4>
            <p>SEO uyumlu blog içerikleri</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation Info
    st.markdown("---")
    st.markdown("""
    ## 🧭 Nasıl Kullanılır?
    
    1. **Sol panelden** API anahtarınızı girin
    2. **Yan menüden** istediğiniz içerik türünü seçin
    3. **Gerekli bilgileri** doldurун
    4. **Generate** butonuna tıklayın
    5. **İçeriğinizi** indirin veya kopyalayın
    
    ### 📊 Desteklenen İçerik Türleri:
    - 📱 **Social Media Posts**: Instagram, Twitter, LinkedIn, Facebook
    - 📧 **Email Templates**: Newsletter, Promosyon, Hoş geldin emailları  
    - 🛍️ **Product Descriptions**: E-ticaret için ürün açıklamaları
    - 📝 **Blog Posts**: SEO uyumlu blog yazıları
    """)
    
    # Recent History Preview
    if st.session_state.generation_history:
        st.markdown("## 📋 Son Üretilen İçerikler")
        
        # Show last 3 items
        recent_items = st.session_state.generation_history[-3:]
        
        for item in reversed(recent_items):
            with st.expander(f"{item.get('type', 'Unknown')} - {item.get('date', 'No date')}"):
                st.markdown(f"**Platform/Tür:** {item.get('platform', 'N/A')}")
                st.markdown(f"**Konu:** {item.get('topic', 'N/A')}")
                st.text_area(
                    "İçerik Preview",
                    value=item.get('content', '')[:200] + "..." if len(item.get('content', '')) > 200 else item.get('content', ''),
                    height=100,
                    disabled=True
                )
    
    # Save history on any changes
    save_history()

if __name__ == "__main__":
    main()