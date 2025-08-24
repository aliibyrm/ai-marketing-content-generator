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

# Custom CSS
st.markdown("""
<style>
    .email-preview {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        font-family: 'Arial', sans-serif;
        line-height: 1.6;
        max-width: 600px;
        color: #000000;
    }
    
    .email-header {
        border-bottom: 2px solid #667eea;
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .subject-line {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
        font-weight: bold;
    }
    
    .email-type-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem;
        cursor: pointer;
        transition: transform 0.2s;
    }
    
    .email-type-card:hover {
        transform: translateY(-2px);
    }
    
    .cta-button {
        background: #667eea;
        color: white;
        padding: 0.8rem 2rem;
        border: none;
        border-radius: 25px;
        font-weight: bold;
        text-decoration: none;
        display: inline-block;
        margin: 1rem 0;
    }
    
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .metric-item {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        color: #000000;
    }
    
    .metric-item h3 {
        color: #000000;
        font-weight: bold;
        margin: 0;
        font-size: 1.5rem;
    }
    
    .metric-item p {
        color: #000000;
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
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
    st.markdown("# 📧 Email Marketing Generator")
    st.markdown("Etkili email kampanyaları için profesyonel içerikler oluşturun!")
    
    # Check API key
    if 'api_key' not in st.session_state or not st.session_state.api_key:
        st.warning("⚠️ Lütfen ana sayfadan OpenAI API anahtarınızı girin.")
        st.stop()
    
    # Initialize generator
    generator = EmailGenerator(
        st.session_state.api_key,
        st.session_state.get('selected_model', 'gpt-3.5-turbo')
    )
    
    # Email Type Selection
    st.markdown("## 📊 Email Türü Seçimi")
    
    email_types = {
        "newsletter": {
            "name": "📰 Newsletter",
            "description": "Düzenli içerik bülteni",
            "purpose": "Bilgilendirme, engagement, brand awareness"
        },
        "promotional": {
            "name": "🎯 Promosyonel",
            "description": "Satış odaklı kampanya emaili",
            "purpose": "Ürün tanıtımı, indirim kampanyaları, satış artışı"
        },
        "welcome": {
            "name": "👋 Hoş Geldin",
            "description": "Yeni üye karşılama emaili",
            "purpose": "Onboarding, ilk izlenim, beklenti yönetimi"
        },
        "followup": {
            "name": "📞 Follow-up",
            "description": "Takip ve hatırlatma emaili",
            "purpose": "Re-engagement, abandoned cart, müşteri geri kazanımı"
        },
        "announcement": {
            "name": "📢 Duyuru",
            "description": "Önemli haberlerin duyurusu",
            "purpose": "Şirket haberleri, ürün lansmanları, güncellemeler"
        },
        "educational": {
            "name": "📚 Eğitici",
            "description": "Bilgi paylaşımı ve eğitim",
            "purpose": "Değer katma, expertise gösterme, trust building"
        }
    }
    
    selected_email_type = st.selectbox(
        "Email Türü:",
        list(email_types.keys()),
        format_func=lambda x: email_types[x]['name']
    )
    
    email_info = email_types[selected_email_type]
    
    # Show email type info
    with st.expander(f"{email_info['name']} Hakkında", expanded=False):
        st.markdown(f"""
        **Açıklama:** {email_info['description']}
        
        **Amaç:** {email_info['purpose']}
        
        **En İyi Uygulamalar:**
        - Kısa ve öz konu başlığı
        - Kişiselleştirme unsurları
        - Açık call-to-action
        - Mobile-friendly tasarım
        - A/B test edilebilir içerik
        """)
    
    # Content Configuration
    st.markdown("## ⚙️ Email İçerik Ayarları")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Subject and Topic
        company_name = st.text_input(
            "Şirket/Marka Adı:",
            placeholder="Örn: TechShop, KahveDünyası",
            help="Email gönderen şirket veya marka adı"
        )
        
        main_topic = st.text_input(
            "Ana Konu/Kampanya:",
            placeholder="Örn: Black Friday indirimleri, Yeni ürün lansmanı",
            help="Email'in ana konusu veya kampanyası"
        )
        
        target_audience = st.selectbox(
            "Hedef Kitle:",
            [
                "Mevcut Müşteriler",
                "Potansiyel Müşteriler", 
                "Premium Üyeler",
                "Yeni Üyeler",
                "Aktif Olmayan Müşteriler",
                "B2B Müşteriler",
                "B2C Müşteriler",
                "Newsletter Aboneleri"
            ]
        )
        
        # Email Goals
        email_goal = st.selectbox(
            "Email Amacı:",
            [
                "Satış Artışı",
                "Brand Awareness", 
                "Müşteri Sadakati",
                "Website Trafiği",
                "Event Katılımı",
                "Uygulama İndirmesi",
                "Survey Tamamlama",
                "Social Media Takip"
            ]
        )
    
    with col2:
        # Tone and Style
        tone = st.selectbox(
            "Email Tonu:",
            ["professional", "friendly", "exciting", "urgent", "informative"],
            format_func=lambda x: {
                "professional": "🎩 Profesyonel",
                "friendly": "😊 Samimi",
                "exciting": "🚀 Heyecanlı", 
                "urgent": "⚡ Acil",
                "informative": "📚 Bilgilendirici"
            }[x]
        )
        
        # Email Elements
        include_personalization = st.checkbox("Kişiselleştirme ekle", value=True)
        include_social_proof = st.checkbox("Sosyal kanıt ekle", value=False)
        include_urgency = st.checkbox("Aciliyet unsuru ekle", value=False)
        include_discount = st.checkbox("İndirim/Teklif ekle", value=selected_email_type == "promotional")
        
        # CTA Settings
        st.markdown("**Call-to-Action Ayarları:**")
        cta_text = st.text_input(
            "CTA Metni:",
            placeholder="Örn: Hemen Satın Al, Daha Fazla Bilgi, Kayıt Ol",
            value="Hemen İncele"
        )
        
        cta_url = st.text_input(
            "CTA Linki (opsiyonel):",
            placeholder="https://example.com/campaign"
        )
    
    # Advanced Settings
    with st.expander("🔧 Gelişmiş Ayarlar"):
        col1, col2 = st.columns(2)
        
        with col1:
            sender_name = st.text_input(
                "Gönderen Adı:",
                placeholder="Örn: Can - TechShop",
                help="Email gönderen kişi/departman adı"
            )
            
            preheader_text = st.text_area(
                "Preheader Text:",
                placeholder="Konu satırını destekleyen kısa açıklama",
                height=60,
                help="Email preview'da görünen kısa açıklama"
            )
        
        with col2:
            email_length = st.select_slider(
                "Email Uzunluğu:",
                options=["Kısa", "Orta", "Uzun"],
                value="Orta"
            )
            
            creativity_level = st.slider(
                "Yaratıcılık Seviyesi:",
                min_value=0.1,
                max_value=1.0,
                value=0.6,
                step=0.1
            )
        
        custom_instructions = st.text_area(
            "Özel Talimatlar:",
            placeholder="Örn: Marka değerlerini vurgula, sürdürülebilirlik temasını kullan",
            height=80
        )
    
    # Generate Email
    if st.button("📧 Email Oluştur", type="primary"):
        if not main_topic:
            st.error("Lütfen ana konu girin!")
            return
            
        if not company_name:
            st.error("Lütfen şirket/marka adı girin!")
            return
        
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
        
        # Generate email
        with st.spinner(f"📧 {email_info['name']} oluşturuluyor..."):
            result = generator.generate_email(**generation_params)
        
        if result['success']:
            email_data = result['email_data']
            
            # Display generated email
            st.markdown("## ✨ Üretilen Email")
            
            # Subject line
            st.markdown(f"""
            <div class="subject-line">
                <strong>Konu:</strong> {email_data.get('subject', 'Email Konusu')}
            </div>
            """, unsafe_allow_html=True)
            
            # Preheader if provided
            if email_data.get('preheader'):
                st.markdown(f"**Preheader:** {email_data['preheader']}")
            
            # Email preview
            st.markdown(f"""
            <div class="email-preview">
                <div class="email-header">
                    <strong>From:</strong> {sender_name or company_name}<br>
                    <strong>To:</strong> {target_audience}<br>
                    <strong>Subject:</strong> {email_data.get('subject', 'Email Konusu')}
                </div>
                
                <div style="white-space: pre-wrap;">
{email_data.get('content', 'Email içeriği')}
                </div>
                
                {f'<a href="{cta_url}" class="cta-button">{cta_text}</a>' if cta_url else f'<div class="cta-button">{cta_text}</div>'}
            </div>
            """, unsafe_allow_html=True)
            
            # Email analysis
            analyzer = ContentAnalyzer()
            content_for_analysis = f"{email_data.get('subject', '')} {email_data.get('content', '')}"
            metrics = analyzer.analyze_content(content_for_analysis)
            
            # Display metrics
            st.markdown("## 📊 Email Analizi")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-item">
                    <h3>{metrics.get('word_count', 0)}</h3>
                    <p>Kelime Sayısı</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                subject_length = len(email_data.get('subject', ''))
                color = "green" if 30 <= subject_length <= 50 else "orange" if subject_length <= 60 else "red"
                st.markdown(f"""
                <div class="metric-item">
                    <h3 style="color: {color}">{subject_length}</h3>
                    <p>Konu Uzunluğu</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                reading_time = max(1, metrics.get('word_count', 0) // 200)
                st.markdown(f"""
                <div class="metric-item">
                    <h3>{reading_time} dk</h3>
                    <p>Okuma Süresi</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                sentiment = metrics.get('sentiment_polarity', 0)
                sentiment_emoji = "😊" if sentiment > 0.1 else "😐" if sentiment > -0.1 else "😔"
                st.markdown(f"""
                <div class="metric-item">
                    <h3>{sentiment_emoji}</h3>
                    <p>Sentiment</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Email Quality Check
            st.markdown("## ✅ Email Kalite Kontrolü")
            
            quality_checks = []
            
            # Subject line checks
            subject = email_data.get('subject', '')
            if 30 <= len(subject) <= 50:
                quality_checks.append("✅ Konu satırı optimal uzunlukta (30-50 karakter)")
            elif len(subject) < 30:
                quality_checks.append("⚠️ Konu satırı biraz kısa (30+ karakter önerilir)")
            else:
                quality_checks.append("⚠️ Konu satırı biraz uzun (50 karakter altı önerilir)")
            
            # Content checks
            word_count = metrics.get('word_count', 0)
            if 50 <= word_count <= 200:
                quality_checks.append("✅ Email uzunluğu optimal (50-200 kelime)")
            elif word_count < 50:
                quality_checks.append("⚠️ Email biraz kısa olabilir")
            else:
                quality_checks.append("⚠️ Email biraz uzun olabilir")
            
            # CTA check
            if cta_text and len(cta_text) <= 25:
                quality_checks.append("✅ CTA metni uygun uzunlukta")
            
            # Personalization check
            if include_personalization:
                quality_checks.append("✅ Kişiselleştirme unsurları eklendi")
            
            for check in quality_checks:
                st.markdown(check)
            
            # Action buttons
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("📋 Kopyala"):
                    full_email = f"Konu: {email_data.get('subject', '')}\n\n{email_data.get('content', '')}"
                    st.success("Email panoya kopyalandı!")
                    # Note: Actual clipboard functionality requires additional setup
            
            with col2:
                # Download as HTML
                html_content = f"""
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>{email_data.get('subject', 'Email')}</title>
                </head>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="border-bottom: 2px solid #667eea; padding-bottom: 10px; margin-bottom: 20px;">
                        <strong>Subject:</strong> {email_data.get('subject', '')}<br>
                        <strong>From:</strong> {sender_name or company_name}
                    </div>
                    <div style="white-space: pre-wrap;">
{email_data.get('content', '')}
                    </div>
                    {f'<a href="{cta_url}" style="background: #667eea; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px;">{cta_text}</a>' if cta_url else f'<div style="background: #667eea; color: white; padding: 10px 20px; border-radius: 5px; display: inline-block; margin-top: 20px;">{cta_text}</div>'}
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
                text_content = f"Konu: {email_data.get('subject', '')}\n\nİçerik:\n{email_data.get('content', '')}\n\nCTA: {cta_text}"
                st.download_button(
                    label="📥 TXT İndir",
                    data=text_content,
                    file_name=f"email_{selected_email_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
            
            with col4:
                if st.button("🔄 Yeniden Üret"):
                    st.rerun()
            
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
            st.error(f"❌ Hata: {result['error']}")
    
    # Tips and best practices
    st.markdown("---")
    st.markdown("## 💡 Email Marketing İpuçları")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### ✅ En İyi Uygulamalar
        - **Kişiselleştirme**: İsim ve tercihler
        - **Mobile Optimize**: %70+ mobile okuma
        - **A/B Testing**: Konu satırı testleri
        - **Segmentasyon**: Hedef kitle grupları
        - **Timing**: Optimal gönderim zamanı
        - **Value First**: Önce değer, sonra satış
        """)
    
    with col2:
        st.markdown("""
        ### 🚫 Kaçınılacaklar
        - Spam trigger kelimeler
        - Çok uzun konu satırları
        - Sadece resim içeriği
        - Belirsiz CTA'lar
        - Aşırı büyük harfler
        - Kişiselleştirme eksikliği
        """)
    
    # Email Performance Benchmarks
    st.markdown("## 📊 Sektör Benchmarkları")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📈 Açılma Oranları**
        - Retail: %18-22
        - B2B: %15-20  
        - Teknoloji: %16-21
        - Finans: %14-19
        """)
    
    with col2:
        st.markdown("""
        **🖱️ Tıklama Oranları**
        - Retail: %2.3-3.2
        - B2B: %2.1-2.8
        - Teknoloji: %2.4-3.1
        - Finans: %1.8-2.5
        """)
    
    with col3:
        st.markdown("""
        **🎯 Optimal Zamanlar**
        - Salı-Çarşamba: En yüksek
        - 10:00-11:00: Sabah peak
        - 14:00-15:00: Öğlen peak
        - Hafta sonu: Düşük
        """)

if __name__ == "__main__":
    main()