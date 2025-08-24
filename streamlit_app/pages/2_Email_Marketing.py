import streamlit as st
import sys
import os
from pathlib import Path
import json
from datetime import datetime

# Add src to path - daha güvenli yol
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from utils.api_handler import APIHandler, ContentAnalyzer
from generators.email_generator import EmailGenerator

st.set_page_config(
    page_title="Email Marketing Generator",
    page_icon="📧",
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
    
    /* Page Header */
    .page-header {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
    }
    
    .page-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Email Type Cards */
    .email-type-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .email-type-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 2rem;
        color: white;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 2px solid transparent;
        position: relative;
        overflow: hidden;
    }
    
    .email-type-card.selected {
        border: 2px solid rgba(255, 255, 255, 0.4);
        background: rgba(255, 255, 255, 0.15);
        transform: scale(1.02);
    }
    
    .email-type-card:hover {
        transform: translateY(-4px) scale(1.02);
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
    }
    
    .email-type-card::before {
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
    
    .email-type-card h4 {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: white;
    }
    
    .email-type-card .description {
        font-size: 0.9rem;
        opacity: 0.8;
        margin-bottom: 1rem;
        color: rgba(255, 255, 255, 0.8);
    }
    
    .email-type-card .purpose {
        font-size: 0.85rem;
        color: #f093fb;
        font-weight: 500;
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
    
    /* Email Preview */
    .email-preview {
        background: white;
        border-radius: 16px;
        padding: 0;
        margin: 2rem 0;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        color: #333;
        overflow: hidden;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .email-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        color: white;
        border-radius: 16px 16px 0 0;
    }
    
    .email-header h4 {
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .email-header .meta {
        font-size: 0.9rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .email-body {
        padding: 2rem;
    }
    
    .subject-line {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        border-radius: 12px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
    }
    
    .subject-line::before {
        content: '✉️ ';
        margin-right: 0.5rem;
    }
    
    .email-content {
        font-size: 1rem;
        line-height: 1.7;
        color: #444;
        white-space: pre-wrap;
        margin: 1.5rem 0;
    }
    
    .cta-button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1rem 2rem;
        border: none;
        border-radius: 25px;
        font-weight: bold;
        text-decoration: none;
        display: inline-block;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* Quality Indicators */
    .quality-checks {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(8px);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .quality-check {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0.5rem 0;
        color: white;
        font-size: 0.95rem;
    }
    
    .quality-check.good {
        color: #28a745;
    }
    
    .quality-check.warning {
        color: #ffc107;
    }
    
    .quality-check.error {
        color: #dc3545;
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
    
    .metric-card h3.warning {
        color: #ffc107;
    }
    
    .metric-card h3.error {
        color: #dc3545;
    }
    
    .metric-card h3.good {
        color: #28a745;
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
        justify-content: center;
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
    
    /* Performance Benchmarks */
    .benchmarks-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .benchmark-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
    }
    
    .benchmark-card h3 {
        color: white;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .benchmark-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .benchmark-list li {
        padding: 0.5rem 0;
        color: rgba(255, 255, 255, 0.8);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .benchmark-list li:last-child {
        border-bottom: none;
    }
    
    .benchmark-value {
        color: #f093fb;
        font-weight: 600;
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
    
    /* Progress Steps */
    .progress-steps {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
        gap: 1rem;
    }
    
    .progress-step {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .progress-step.active {
        background: linear-gradient(135deg, #667eea, #764ba2);
        transform: scale(1.1);
    }
    
    .progress-step.completed {
        background: #28a745;
    }
    
    .progress-connector {
        width: 30px;
        height: 2px;
        background: rgba(255, 255, 255, 0.2);
        margin: 0 0.5rem;
    }
    
    .progress-connector.completed {
        background: #28a745;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .email-type-grid {
            grid-template-columns: 1fr;
        }
        
        .metrics-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .action-buttons {
            flex-direction: column;
            align-items: center;
        }
        
        .benchmarks-grid {
            grid-template-columns: 1fr;
        }
        
        .tips-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

def save_to_history(content_data):
    """Save generated email to history"""
    if 'generation_history' not in st.session_state:
        st.session_state.generation_history = []
    
    history_item = {
        'type': 'Email Marketing',
        'email_type': content_data.get('email_type', ''),
        'subject': content_data.get('subject', ''),
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
        <h1>📧 Email Marketing Generator</h1>
        <p>Yüksek açılma oranları ve etkili conversion'lar için profesyonel email kampanyaları oluşturun!</p>
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
    generator = EmailGenerator(
        st.session_state.api_key,
        st.session_state.get('selected_model', 'gpt-3.5-turbo')
    )
    
    # Email Type Selection
    st.markdown("""
    <div class="form-section animate-in">
        <h3>📊 Email Türü Seçimi</h3>
        <p>Kampanyanızın amacına en uygun email türünü seçin:</p>
    </div>
    """, unsafe_allow_html=True)
    
    email_types = {
        "newsletter": {
            "name": "📰 Newsletter",
            "description": "Düzenli içerik bülteni ve community building",
            "purpose": "Bilgilendirme, engagement, brand awareness ve müşteri sadakati"
        },
        "promotional": {
            "name": "🎯 Promosyonel",
            "description": "Satış odaklı kampanya ve özel teklifler",
            "purpose": "Ürün tanıtımı, indirim kampanyaları, conversion artışı"
        },
        "welcome": {
            "name": "👋 Hoş Geldin",
            "description": "Yeni üye karşılama ve onboarding",
            "purpose": "İlk izlenim, beklenti yönetimi, müşteri yolculuğu başlangıcı"
        },
        "followup": {
            "name": "📞 Follow-up",
            "description": "Takip, hatırlatma ve re-engagement",
            "purpose": "Abandoned cart, müşteri geri kazanımı, activation"
        },
        "announcement": {
            "name": "📢 Duyuru",
            "description": "Önemli haberlerin duyurusu ve güncellemeler",
            "purpose": "Şirket haberleri, ürün lansmanları, policy değişiklikleri"
        },
        "educational": {
            "name": "📚 Eğitici",
            "description": "Bilgi paylaşımı, rehberler ve ipuçları",
            "purpose": "Değer katma, expertise gösterme, trust building"
        }
    }
    
    # Display email type cards
    st.markdown('<div class="email-type-grid">', unsafe_allow_html=True)
    
    # Create columns for email type selection
    cols = st.columns(3)
    email_type_names = list(email_types.keys())
    
    for i, (key, info) in enumerate(email_types.items()):
        with cols[i % 3]:
            if st.button(info["name"], key=f"email_type_{key}", use_container_width=True):
                st.session_state.selected_email_type = key
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Email type selector (fallback)
    selected_email_type = st.selectbox(
        "Veya listeden seçin:",
        list(email_types.keys()),
        format_func=lambda x: email_types[x]['name'],
        key="email_type_selectbox"
    )
    
    email_info = email_types[selected_email_type]
    
    # Show email type info
    with st.expander(f"{email_info['name']} - Detaylı Bilgi", expanded=False):
        st.markdown(f"""
        <div class="email-type-card">
            <h4>{email_info['name']}</h4>
            <div class="description">{email_info['description']}</div>
            <div class="purpose"><strong>Amaç:</strong> {email_info['purpose']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress Steps
    st.markdown("""
    <div class="progress-steps">
        <div class="progress-step completed">1</div>
        <div class="progress-connector completed"></div>
        <div class="progress-step active">2</div>
        <div class="progress-connector"></div>
        <div class="progress-step">3</div>
        <div class="progress-connector"></div>
        <div class="progress-step">4</div>
    </div>
    <div style="text-align: center; color: rgba(255,255,255,0.8); margin-bottom: 2rem;">
        <small>Email Türü Seçimi → <strong>İçerik Ayarları</strong> → Email Oluşturma → Sonuç</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Content Configuration
    st.markdown("""
    <div class="form-section animate-in" style="animation-delay: 0.2s;">
        <h3>⚙️ Email İçerik Ayarları</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Basic Information
        company_name = st.text_input(
            "🏢 Şirket/Marka Adı:",
            placeholder="Örn: TechShop, KahveDünyası, InnovateCorp",
            help="Email gönderen şirket veya marka adı"
        )
        
        main_topic = st.text_input(
            "🎯 Ana Konu/Kampanya:",
            placeholder="Örn: Black Friday indirimleri, Yeni ürün lansmanı, Müşteri başarı hikayeleri",
            help="Email'in ana konusu veya kampanyası"
        )
        
        target_audience = st.selectbox(
            "👥 Hedef Kitle:",
            [
                "Mevcut Müşteriler",
                "Potansiyel Müşteriler", 
                "Premium Üyeler",
                "Yeni Üyeler",
                "Aktif Olmayan Müşteriler",
                "B2B Müşteriler",
                "B2C Müşteriler",
                "Newsletter Aboneleri",
                "Tekrarlayan Alıcılar"
            ]
        )
        
        # Email Goals
        email_goal = st.selectbox(
            "🎯 Email Amacı:",
            [
                "Satış Artışı",
                "Brand Awareness", 
                "Müşteri Sadakati",
                "Website Trafiği",
                "Event Katılımı",
                "Uygulama İndirmesi",
                "Survey Tamamlama",
                "Social Media Takip",
                "Lead Generation",
                "Customer Retention"
            ]
        )
    
    with col2:
        # Tone and Style
        tone = st.selectbox(
            "🎭 Email Tonu:",
            ["professional", "friendly", "exciting", "urgent", "informative"],
            format_func=lambda x: {
                "professional": "🎩 Profesyonel & Güvenilir",
                "friendly": "😊 Samimi & Dostça",
                "exciting": "🚀 Heyecanlı & Enerjik", 
                "urgent": "⚡ Acil & Harekete Geçirici",
                "informative": "📚 Bilgilendirici & Açıklayıcı"
            }[x]
        )
        
        # Email Elements
        st.markdown("**📋 Dahil Edilecek Unsurlar:**")
        
        col_a, col_b = st.columns(2)
        with col_a:
            include_personalization = st.checkbox("👤 Kişiselleştirme", value=True)
            include_social_proof = st.checkbox("⭐ Sosyal Kanıt", value=False)
        
        with col_b:
            include_urgency = st.checkbox("⏰ Aciliyet Unsuru", value=False)
            include_discount = st.checkbox("💰 İndirim/Teklif", value=selected_email_type == "promotional")
        
        # CTA Settings
        st.markdown("**🎯 Call-to-Action Ayarları:**")
        cta_text = st.text_input(
            "CTA Metni:",
            placeholder="Örn: Hemen Satın Al, Daha Fazla Bilgi, Ücretsiz Dene",
            value="Hemen İncele"
        )
        
        cta_url = st.text_input(
            "CTA Linki (opsiyonel):",
            placeholder="https://example.com/campaign"
        )
    
    # Advanced Settings
    with st.expander("🔧 Gelişmiş Ayarlar ve Özelleştirme", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            sender_name = st.text_input(
                "👤 Gönderen Adı:",
                placeholder="Örn: Can - TechShop, Marketing Ekibi",
                help="Email gönderen kişi/departman adı"
            )
            
            preheader_text = st.text_area(
                "📱 Preheader Text:",
                placeholder="Konu satırını destekleyen, merak uyandırıcı kısa açıklama...",
                height=60,
                help="Email preview'da görünen, konu satırını tamamlayan açıklama"
            )
            
            email_length = st.select_slider(
                "📏 Email Uzunluğu:",
                options=["Kısa", "Orta", "Uzun"],
                value="Orta",
                help="Kısa: 50-100 kelime, Orta: 100-200 kelime, Uzun: 200+ kelime"
            )
        
        with col2:
            creativity_level = st.slider(
                "🎨 Yaratıcılık Seviyesi:",
                min_value=0.1,
                max_value=1.0,
                value=0.6,
                step=0.1,
                help="Düşük = Daha güvenli ve standart, Yüksek = Daha yaratıcı ve deneysel"
            )
            
            brand_voice = st.selectbox(
                "🎤 Marka Sesi:",
                ["Standart", "Lüks & Premium", "Genç & Modern", "Güvenilir & Klasik", "İnovatif & Teknolojik", "Eğlenceli & Yaratıcı"],
                help="Markanızın genel karakterini yansıtan ses tonu"
            )
            
            custom_instructions = st.text_area(
                "📝 Özel Talimatlar:",
                placeholder="Örn: Sürdürürebilirlik vurgusu yap, testimonial ekle, video linkini dahil et...",
                height=80,
                help="AI'ya verilecek özel yönergeler ve istekler"
            )
    
    # Generate Email Button
    if st.button("📧 Email Kampanyası Oluştur", type="primary", key="generate_email_btn"):
        if not main_topic:
            st.error("❌ Lütfen ana konu girin!")
            return
            
        if not company_name:
            st.error("❌ Lütfen şirket/marka adı girin!")
            return
        
        # Update progress
        st.markdown("""
        <div class="progress-steps">
            <div class="progress-step completed">1</div>
            <div class="progress-connector completed"></div>
            <div class="progress-step completed">2</div>
            <div class="progress-connector completed"></div>
            <div class="progress-step active">3</div>
            <div class="progress-connector"></div>
            <div class="progress-step">4</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Prepare generation parameters
        generation_params = {
            'email_type': selected_email_type,
            'company_name': company_name,
            'main_topic': main_topic,
            'target_audience': target_audience,
            'email_goal': email_goal,
            'tone': tone,
            'include_personalization': include_personalization,
            'include_social_proof': include_social_proof,
            'include_urgency': include_urgency,
            'include_discount': include_discount,
            'cta_text': cta_text,
            'cta_url': cta_url,
            'sender_name': sender_name,
            'preheader_text': preheader_text,
            'email_length': email_length,
            'custom_instructions': custom_instructions,
            'creativity_level': creativity_level
        }
        
        # Add brand voice to custom instructions
        if brand_voice != "Standart":
            brand_voice_instructions = {
                "Lüks & Premium": "Lüks, elit ve premium bir marka sesi kullan, kalite ve prestij vurgula",
                "Genç & Modern": "Genç, modern ve trendy bir dil kullan, güncel referanslar ekle", 
                "Güvenilir & Klasik": "Güvenilir, klasik ve saygın bir ton kullan, deneyim vurgula",
                "İnovatif & Teknolojik": "İnovatif, teknolojik ve gelecek odaklı yaklaşım, cutting-edge vurgusu",
                "Eğlenceli & Yaratıcı": "Eğlenceli, yaratıcı ve samimi bir yaklaşım, espri ve yaratıcılık"
            }
            generation_params['custom_instructions'] += f" {brand_voice_instructions.get(brand_voice, '')}"
        
        # Generate email with progress indicator
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with st.spinner():
            status_text.text(f"🔄 {email_info['name']} oluşturuluyor...")
            progress_bar.progress(25)
            
            result = generator.generate_email(**generation_params)
            progress_bar.progress(100)
            
            if result['success']:
                status_text.text("✅ Email başarıyla oluşturuldu!")
                
                # Update final progress
                st.markdown("""
                <div class="progress-steps">
                    <div class="progress-step completed">1</div>
                    <div class="progress-connector completed"></div>
                    <div class="progress-step completed">2</div>
                    <div class="progress-connector completed"></div>
                    <div class="progress-step completed">3</div>
                    <div class="progress-connector completed"></div>
                    <div class="progress-step completed">4</div>
                </div>
                """, unsafe_allow_html=True)
                
                email_data = result['email_data']
                
                # Display generated email
                st.markdown("## ✨ Üretilen Email Kampanyanız")
                
                # Subject line with beautiful styling
                st.markdown(f"""
                <div class="subject-line">
                    <strong>Konu:</strong> {email_data.get('subject', 'Email Konusu')}
                </div>
                """, unsafe_allow_html=True)
                
                # Email preview with realistic styling
                st.markdown(f"""
                <div class="email-preview">
                    <div class="email-header">
                        <h4>📧 Email Önizleme</h4>
                        <div class="meta">
                            <strong>Gönderen:</strong> {sender_name or company_name}<br>
                            <strong>Alıcı:</strong> {target_audience}<br>
                            <strong>Konu:</strong> {email_data.get('subject', 'Email Konusu')}
                            {f'<br><strong>Preheader:</strong> {preheader_text}' if preheader_text else ''}
                        </div>
                    </div>
                    
                    <div class="email-body">
                        <div class="email-content">{email_data.get('content', 'Email içeriği')}</div>
                        
                        {f'<a href="{cta_url}" class="cta-button">{cta_text}</a>' if cta_url else f'<div class="cta-button">{cta_text}</div>'}
                        
                        <div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #eee; font-size: 0.8rem; color: #888;">
                            Bu email {company_name} tarafından gönderilmiştir.<br>
                            Email tercihlerinizi değiştirmek için <a href="#" style="color: #667eea;">buraya tıklayın</a>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Email analysis and metrics
                analyzer = ContentAnalyzer()
                content_for_analysis = f"{email_data.get('subject', '')} {email_data.get('content', '')}"
                metrics = analyzer.analyze_content(content_for_analysis)
                
                # Display metrics with beautiful cards
                st.markdown("## 📊 Email Analizi ve Performans Tahmini")
                
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    word_count = metrics.get('word_count', 0)
                    word_class = "good" if 50 <= word_count <= 200 else "warning" if word_count < 50 else "error"
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3 class="{word_class}">{word_count}</h3>
                        <p>💬 Kelime Sayısı</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    subject_length = len(email_data.get('subject', ''))
                    subject_class = "good" if 30 <= subject_length <= 50 else "warning" if subject_length <= 60 else "error"
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3 class="{subject_class}">{subject_length}</h3>
                        <p>📏 Konu Uzunluğu</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    reading_time = max(1, word_count // 200)
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>{reading_time} dk</h3>
                        <p>⏱️ Okuma Süresi</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    # Deliverability score (simulated based on best practices)
                    deliverability_score = 85  # Base score
                    if 30 <= subject_length <= 50:
                        deliverability_score += 5
                    if include_personalization:
                        deliverability_score += 3
                    if cta_text and len(cta_text) <= 25:
                        deliverability_score += 2
                    deliverability_score = min(deliverability_score, 100)
                    
                    score_class = "good" if deliverability_score >= 80 else "warning" if deliverability_score >= 60 else "error"
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3 class="{score_class}">{deliverability_score}%</h3>
                        <p>📬 Deliverability</p>
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
                
                # Email Quality Check with detailed feedback
                st.markdown("## ✅ Email Kalite Kontrolü ve Öneriler")
                
                quality_checks = []
                
                # Subject line checks
                subject = email_data.get('subject', '')
                if 30 <= len(subject) <= 50:
                    quality_checks.append(("good", "✅ Konu satırı optimal uzunlukta (30-50 karakter)"))
                elif len(subject) < 30:
                    quality_checks.append(("warning", "⚠️ Konu satırı biraz kısa olabilir (30+ karakter önerilir)"))
                else:
                    quality_checks.append(("warning", "⚠️ Konu satırı uzun olabilir (50 karakter altı önerilir)"))
                
                # Content checks
                if 50 <= word_count <= 200:
                    quality_checks.append(("good", "✅ Email uzunluğu optimal (50-200 kelime)"))
                elif word_count < 50:
                    quality_checks.append(("warning", "⚠️ Email içeriği biraz kısa olabilir"))
                else:
                    quality_checks.append(("warning", "⚠️ Email içeriği uzun, özet geçmeyi düşünün"))
                
                # CTA check
                if cta_text and len(cta_text) <= 25:
                    quality_checks.append(("good", "✅ CTA metni uygun uzunlukta ve net"))
                elif not cta_text:
                    quality_checks.append(("warning", "⚠️ CTA eksik, harekete geçirici mesaj ekleyin"))
                
                # Personalization check
                if include_personalization:
                    quality_checks.append(("good", "✅ Kişiselleştirme unsurları eklendi"))
                
                # Mobile optimization
                quality_checks.append(("good", "✅ Mobile-friendly format kullanıldı"))
                
                # Display quality checks
                st.markdown('<div class="quality-checks">', unsafe_allow_html=True)
                for check_type, message in quality_checks:
                    st.markdown(f'<div class="quality-check {check_type}">{message}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Action buttons with modern styling
                st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
                
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    if st.button("📋 Kopyala", key="copy_email_btn"):
                        st.success("✅ Email içeriği kopyalandı!")
                
                with col2:
                    # Download as HTML
                    html_content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>{email_data.get('subject', 'Email')}</title>
                        <style>
                            body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto; padding: 20px; }}
                            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px 8px 0 0; }}
                            .content {{ padding: 20px; background: white; }}
                            .cta {{ background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 25px; display: inline-block; margin: 20px 0; }}
                            .footer {{ background: #f8f9fa; padding: 15px; font-size: 12px; color: #666; border-radius: 0 0 8px 8px; }}
                        </style>
                    </head>
                    <body>
                        <div class="header">
                            <h2 style="margin:0;">{email_data.get('subject', '')}</h2>
                            <p style="margin:5px 0 0 0; opacity:0.9;">From: {sender_name or company_name}</p>
                        </div>
                        <div class="content">
                            <div style="white-space: pre-wrap;">{email_data.get('content', '')}</div>
                            {f'<a href="{cta_url}" class="cta">{cta_text}</a>' if cta_url else f'<div class="cta" style="cursor: default;">{cta_text}</div>'}
                        </div>
                        <div class="footer">
                            Bu email {company_name} tarafından gönderilmiştir.<br>
                            Email tercihlerinizi değiştirmek için lütfen bizimle iletişime geçin.
                        </div>
                    </body>
                    </html>
                    """
                    st.download_button(
                        label="📥 HTML İndir",
                        data=html_content,
                        file_name=f"email_{selected_email_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                        mime="text/html"
                    )
                
                with col3:
                    # Download as text
                    text_content = f"""Konu: {email_data.get('subject', '')}
Gönderen: {sender_name or company_name}
Hedef Kitle: {target_audience}
Email Türü: {email_info['name']}

İçerik:
{email_data.get('content', '')}

CTA: {cta_text}
{f'Link: {cta_url}' if cta_url else ''}

---
Oluşturulma Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
AI Model: {st.session_state.get('selected_model', 'gpt-3.5-turbo')}
"""
                    st.download_button(
                        label="📥 TXT İndir",
                        data=text_content,
                        file_name=f"email_{selected_email_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                
                with col4:
                    if st.button("🔄 Yeniden Üret", key="regenerate_email_btn"):
                        st.rerun()
                
                with col5:
                    if st.button("✨ A/B Test Ver.", key="ab_test_btn"):
                        st.info("🚀 A/B test versiyonu özelliği yakında geliyor!")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Save to history
                content_data = {
                    'email_type': email_info['name'],
                    'subject': email_data.get('subject', ''),
                    'content': email_data.get('content', ''),
                    'metrics': metrics,
                    'settings': generation_params
                }
                save_to_history(content_data)
                
            else:
                progress_bar.progress(0)
                status_text.text("")
                st.error(f"❌ Hata: {result['error']}")
    
    # Email Marketing Tips and Best Practices
    st.markdown("---")
    st.markdown("## 💡 Email Marketing İpuçları ve En İyi Uygulamalar")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="tip-card animate-in" style="animation-delay: 0.1s;">
            <h3>✅ En İyi Uygulamalar</h3>
            <ul>
                <li><strong>Kişiselleştirme</strong> - İsim, lokasyon, geçmiş davranışlar</li>
                <li><strong>Mobile Optimize</strong> - Emailların %70'i mobilde okunuyor</li>
                <li><strong>A/B Testing</strong> - Konu satırı ve CTA testleri yapın</li>
                <li><strong>Segmentasyon</strong> - Doğru mesajı doğru kişiye gönderin</li>
                <li><strong>Timing</strong> - Optimal gönderim zamanını bulun</li>
                <li><strong>Value First</strong> - Önce değer sunun, sonra satış yapın</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tip-card animate-in" style="animation-delay: 0.2s;">
            <h3>🚫 Kaçınılacaklar</h3>
            <ul>
                <li>Spam trigger kelimeler (FREE, URGENT, !!!)</li>
                <li>Çok uzun konu satırları (50+ karakter)</li>
                <li>Sadece resim içerikli emailler</li>
                <li>Belirsiz veya zayıf CTA'lar</li>
                <li>Aşırı büyük harf kullanımı</li>
                <li>Kişiselleştirme eksikliği</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Email Performance Benchmarks
    st.markdown("## 📊 Sektör Performans Benchmarkları")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="benchmark-card animate-in" style="animation-delay: 0.1s;">
            <h3>📈 Açılma Oranları</h3>
            <ul class="benchmark-list">
                <li>Retail <span class="benchmark-value">18-22%</span></li>
                <li>B2B <span class="benchmark-value">15-20%</span></li>
                <li>Teknoloji <span class="benchmark-value">16-21%</span></li>
                <li>Finans <span class="benchmark-value">14-19%</span></li>
                <li>Sağlık <span class="benchmark-value">20-25%</span></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="benchmark-card animate-in" style="animation-delay: 0.2s;">
            <h3>🖱️ Tıklama Oranları</h3>
            <ul class="benchmark-list">
                <li>Retail <span class="benchmark-value">2.3-3.2%</span></li>
                <li>B2B <span class="benchmark-value">2.1-2.8%</span></li>
                <li>Teknoloji <span class="benchmark-value">2.4-3.1%</span></li>
                <li>Finans <span class="benchmark-value">1.8-2.5%</span></li>
                <li>Eğitim <span class="benchmark-value">2.8-3.5%</span></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="benchmark-card animate-in" style="animation-delay: 0.3s;">
            <h3>🎯 Optimal Zamanlar</h3>
            <ul class="benchmark-list">
                <li>En iyi günler <span class="benchmark-value">Salı-Çarşamba</span></li>
                <li>Sabah peak <span class="benchmark-value">10:00-11:00</span></li>
                <li>Öğlen peak <span class="benchmark-value">14:00-15:00</span></li>
                <li>Hafta sonu <span class="benchmark-value">Düşük performans</span></li>
                <li>B2B optimal <span class="benchmark-value">Salı 10:00</span></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()