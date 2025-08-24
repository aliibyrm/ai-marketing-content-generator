class EmailPrompts:
    """Email marketing content generation prompts"""
    
    def get_system_prompt(self, email_type: str, tone: str = "professional") -> str:
        """Get system prompt for email generation"""
        
        email_type_specs = {
            "newsletter": {
                "purpose": "Düzenli bilgilendirme ve engagement",
                "structure": "Kişisel selamlama + değerli içerik + community building + CTA",
                "key_elements": "Value-first content, brand personality, consistency"
            },
            "promotional": {
                "purpose": "Satış artışı ve conversion",
                "structure": "Dikkat çekici açılış + değer propositionu + urgency + güçlü CTA",
                "key_elements": "Clear benefits, social proof, limited time offers"
            },
            "welcome": {
                "purpose": "Onboarding ve ilk izlenim",
                "structure": "Sıcak karşılama + beklenti yönetimi + next steps + destek bilgileri",
                "key_elements": "Warm welcome, clear expectations, helpful resources"
            },
            "followup": {
                "purpose": "Re-engagement ve conversion",
                "structure": "Hatırlatma + değer hatırlatması + yeni teşvik + CTA",
                "key_elements": "Gentle reminders, added value, persistence without spam"
            },
            "announcement": {
                "purpose": "Bilgi paylaşımı ve heyecan yaratma",
                "structure": "Heyecanlı duyuru + detaylar + impact açıklaması + engagement",
                "key_elements": "Clear information, excitement, community involvement"
            },
            "educational": {
                "purpose": "Değer katma ve expertise gösterme",
                "structure": "Problem tanımı + çözüm açıklaması + pratik ipuçları + resources",
                "key_elements": "Actionable advice, credible information, helpful resources"
            }
        }
        
        tone_descriptions = {
            "professional": "profesyonel, güvenilir ve uzman",
            "friendly": "samimi, dostça ve yaklaşılabilir",
            "exciting": "heyecanlı, enerjik ve motivasyonel",
            "urgent": "acil, eylem odaklı ve motivasyonel",
            "informative": "bilgilendirici, açıklayıcı ve eğitici"
        }
        
        email_info = email_type_specs.get(email_type, email_type_specs["newsletter"])
        tone_desc = tone_descriptions.get(tone, "profesyonel")
        
        return f"""Sen uzman bir email marketing specialist'ısın. {tone_desc} tonunda {email_type} türünde email içerikleri oluşturuyorsun.

Email Türü Özellikleri:
- Amaç: {email_info['purpose']}
- Yapı: {email_info['structure']}
- Kilit Unsurlar: {email_info['key_elements']}

Email Yazım Kuralları:
1. Kişisel ve samimi dil kullan
2. Değer odaklı içerik üret
3. Açık ve net CTA ekle
4. Mobile-friendly formatlamaya dikkat et
5. Spam trigger kelimelerden kaçın
6. Okuyucuya fayda sağla

Teknik Gereksinimler:
- Konu satırı: 30-50 karakter
- Preheader: 90 karakter altı
- İçerik: Tarayarak okunabilir
- CTA: Net ve eylem odaklı
- Kişiselleştirme unsurları

Kaçınılacaklar:
- Aşırı satış odaklı dil
- Spam tetikleyici kelimeler
- Çok uzun paragraflar
- Belirsiz CTA'lar
- Kişiselleştirme eksikliği
- Değer katmayan içerik"""

    def get_email_prompt(self,
                        email_type: str,
                        company_name: str,
                        main_topic: str,
                        target_audience: str,
                        email_goal: str) -> str:
        """Get email-specific content generation prompt"""
        
        email_templates = {
            "newsletter": {
                "opening": "Değerli {audience}, bu haftaki öne çıkan gelişmeler",
                "structure": "Selamlama + Ana içerik + Community haberleri + Next steps",
                "cta_style": "Soft CTA (Daha fazla bilgi, Devamını oku)"
            },
            "promotional": {
                "opening": "Özel fırsat: {topic} hakkında",
                "structure": "Hook + Değer vurgusu + Sosyal kanıt + Urgency + Güçlü CTA",
                "cta_style": "Direct CTA (Satın Al, Şimdi Al, Rezerve Et)"
            },
            "welcome": {
                "opening": "{company_name} ailesine hoş geldiniz!",
                "structure": "Sıcak karşılama + Şirket tanıtımı + Beklentiler + İlk adımlar",
                "cta_style": "Guide CTA (Başla, Keşfet, İlk Adım)"
            },
            "followup": {
                "opening": "{topic} ile ilgili son bir hatırlatma",
                "structure": "Nazik hatırlatma + Ek değer + Yeni motivasyon + Action",
                "cta_style": "Gentle CTA (Gözden Geçir, Dene, Tamamla)"
            },
            "announcement": {
                "opening": "Heyecanlı haberimizi paylaşıyoruz: {topic}",
                "structure": "Duyuru + Detaylar + Impact + Community reaction",
                "cta_style": "Engagement CTA (Öğren, Katıl, Paylaş)"
            },
            "educational": {
                "opening": "{topic} hakkında bilmeniz gerekenler",
                "structure": "Problem + Çözüm + Pratik ipuçları + Kaynak linkler",
                "cta_style": "Learning CTA (Öğren, İndir, Uygula)"
            }
        }
        
        template = email_templates.get(email_type, email_templates["newsletter"])
        
        return f"""Şirket: {company_name}
Ana Konu: {main_topic}
Hedef Kitle: {target_audience}
Email Amacı: {email_goal}

Email Şablonu:
Açılış: {template['opening']}
Yapı: {template['structure']}
CTA Stili: {template['cta_style']}

Bu bilgilere dayanarak, hedef kitle için uygun, engaging ve {email_goal} amacına hizmet eden profesyonel bir email içeriği oluştur.

Email şunları içermeli:
1. Kişisel selamlama
2. Ana mesajın net ifadesi
3. Hedef kitle için değer
4. Açık ve net call-to-action
5. Profesyonel kapanış

Format: Email formatında, doğrudan kullanılabilir şekilde hazırla."""

    def get_subject_line_prompt(self,
                               email_type: str,
                               main_topic: str,
                               company_name: str,
                               include_urgency: bool = False,
                               include_discount: bool = False,
                               count: int = 1) -> str:
        """Get prompt for subject line generation"""
        
        urgency_elements = [
            "Son 24 saat", "Yarın sona eriyor", "Sınırlı süre",
            "Sadece bugün", "Kaçırmayın", "Son şans"
        ] if include_urgency else []
        
        discount_elements = [
            "% indirim", "Özel fiyat", "Ücretsiz",
            "Hediye", "Bonus", "Kampanya"
        ] if include_discount else []
        
        subject_strategies = {
            "newsletter": [
                "Bu hafta {company_name}'dan haberler",
                "{main_topic} hakkında bilmeniz gerekenler",
                "{company_name} Bülteni: {main_topic}"
            ],
            "promotional": [
                "{main_topic} - Özel fırsat!",
                "🎯 {main_topic} kampanyası başladı",
                "{company_name}'dan size özel: {main_topic}"
            ],
            "welcome": [
                "{company_name} ailesine hoş geldiniz!",
                "Hoş geldiniz! İlk adımınız hazır",
                "Merhaba! {company_name} yolculuğunuz başlıyor"
            ],
            "followup": [
                "{main_topic} - Son hatırlatma",
                "Unutmadık: {main_topic}",
                "{main_topic} hâlâ sizinle"
            ],
            "announcement": [
                "Heyecanlı haber: {main_topic}",
                "Duyuruyoruz: {main_topic}",
                "{company_name} yeniliği: {main_topic}"
            ],
            "educational": [
                "{main_topic} rehberi hazır",
                "Nasıl yapılır: {main_topic}",
                "{main_topic} ile ilgili ipuçları"
            ]
        }
        
        strategies = subject_strategies.get(email_type, subject_strategies["newsletter"])
        
        prompt = f"""Email Türü: {email_type}
Ana Konu: {main_topic}
Şirket: {company_name}
Sayı: {count} adet

Konu Satırı Stratejileri:
{chr(10).join(f'- {strategy}' for strategy in strategies)}
"""
        
        if urgency_elements:
            prompt += f"\nAciliyet Unsurları: {', '.join(urgency_elements)}"
        
        if discount_elements:
            prompt += f"\nİndirim/Teklif Unsurları: {', '.join(discount_elements)}"
        
        prompt += f"""

{count} adet etkili konu satırı oluştur. Her konu satırı:

Kriter:
- 30-50 karakter arası
- Merak uyandırıcı
- Açık ve net
- Spam tetikleyici olmayan
- {email_type} türüne uygun
- Hedef kitleye relevant

Format: Her satırda bir konu, tırnak işareti olmadan."""

        return prompt

    def get_series_prompt(self,
                         email_type: str,
                         company_name: str,
                         campaign_theme: str,
                         series_count: int) -> str:
        """Get prompt for email series generation"""
        
        series_structures = {
            3: {
                "Email 1": "Giriş ve farkındalık yaratma",
                "Email 2": "Değer gösterimi ve güven inşası",
                "Email 3": "Son çağrı ve aksiyon alma"
            },
            5: {
                "Email 1": "Problem tanımlama ve ilgi çekme",
                "Email 2": "Çözüm tanıtımı ve değer önerisi",
                "Email 3": "Sosyal kanıt ve başarı hikayeleri",
                "Email 4": "Urgency ve limited time offer",
                "Email 5": "Son şans ve final CTA"
            }
        }
        
        structure = series_structures.get(series_count, series_structures[3])
        
        return f"""Email Serisi Bilgileri:
Şirket: {company_name}
Kampanya Teması: {campaign_theme}
Email Türü: {email_type}
Seri Sayısı: {series_count} email

Seri Yapısı:
{chr(10).join(f'{email}: {purpose}' for email, purpose in structure.items())}

Her email için tutarlı bir hikaye anlatımı ile {series_count} adet bağlantılı email oluştur.

Seri Özellikleri:
1. Progresif değer sunumu
2. Tutarlı marka sesi
3. Birbirini tamamlayan içerikler
4. Giderek artan urgency
5. Her email'de net CTA

Email serisi hazırla. Her email'i "---" ile ayır ve email numarası ile başla."""

    def get_deliverability_prompt(self, email_content: str) -> str:
        """Get prompt for email deliverability optimization"""
        
        return f"""Email İçeriği:
{email_content}

Bu email'in deliverability'sini artırmak için optimize et.

Kontrol Edilecek Alanlar:

📧 Spam Filtreleri:
- Spam trigger kelimeleri
- Excessive capitalization
- Exclamation mark overuse
- Suspicious link patterns

📱 Teknik Optimizasyon:
- HTML/text balance
- Image/text ratio
- Link quantity and quality
- Email length optimization

🎯 Engagement Factors:
- Subject line effectiveness
- Preview text optimization
- Clear call-to-actions
- Mobile compatibility

🔍 Analiz et ve şunları sağla:
1. Spam risk skorunu azaltacak öneriler
2. Engagement artıracak iyileştirmeler
3. Teknik optimizasyon tavsiyeleri
4. Alternative subject line önerileri

Format: Her öneri için açıklama ve öner.
Başlık: Problem → Çözüm şeklinde"""

    def get_a_b_test_prompt(self,
                           email_content: str,
                           test_element: str = "subject") -> str:
        """Get prompt for A/B test variations"""
        
        return f"""Email İçeriği:
{email_content}

Test Elementi: {test_element}

Bu email için A/B test varyasyonları oluştur.

Test Türleri:

📧 Subject Line A/B Test:
- Versiyon A: Merak odaklı
- Versiyon B: Fayda odaklı
- Versiyon C: Urgency odaklı

📝 Content A/B Test:
- Versiyon A: Kısa format
- Versiyon B: Uzun format
- Versiyon C: Liste format

🔘 CTA A/B Test:
- Versiyon A: Direct command
- Versiyon B: Benefit-focused
- Versiyon C: Question format

{test_element} elementi için 3 farklı versiyon oluştur.

Her versiyon için:
1. Temel stratejiyi açıkla
2. Neden etkili olacağını belirt
3. Hedef metric'i tanımla
4. Beklenen sonucu öngör

Format: Versiyon A, B, C şeklinde ayrı bölümler halinde."""

    def get_personalization_prompt(self,
                                  email_template: str,
                                  audience_segments: list) -> str:
        """Get prompt for email personalization"""
        
        segments_text = "\n".join([f"- {segment}" for segment in audience_segments])
        
        return f"""Email Template:
{email_template}

Hedef Kitle Segmentleri:
{segments_text}

Bu email template'ini farklı kitle segmentleri için kişiselleştir.

🎯 Kişiselleştirme Alanları:

📧 Mesaj Tonu:
- Demografik uyum
- İlgi alanı relevansı
- Deneyim seviyesi uyumu

📝 İçerik Vurgusu:
- Segment-specific benefits
- Use case örnekleri
- Pain point addressing

🔘 CTA Optimization:
- Segment motivation
- Action readiness level
- Channel preference

Her segment için:
1. Kişiselleştirilmiş konu satırı
2. Açılış selamlaması
3. Ana mesaj vurgusu
4. CTA metni
5. Kapanış tonu

Format: Her segment için ayrı bölüm."""

    def get_lifecycle_email_prompt(self,
                                  lifecycle_stage: str,
                                  company_name: str,
                                  customer_action: str = "") -> str:
        """Get prompt for lifecycle-based email generation"""
        
        lifecycle_mapping = {
            "welcome": "Yeni müşteri onboarding",
            "activation": "İlk ürün/hizmet kullanımı",
            "engagement": "Aktif kullanım teşviki",
            "retention": "Müşteri tutma ve sadakat",
            "winback": "Kaybolan müşteri geri kazanımı",
            "referral": "Müşteri referansı teşviki",
            "upsell": "Ek ürün/hizmet tanıtımı",
            "renewal": "Yenileme hatırlatması"
        }
        
        stage_description = lifecycle_mapping.get(lifecycle_stage, "Genel müşteri iletişimi")
        
        return f"""Lifecycle Stage: {lifecycle_stage}
Açıklama: {stage_description}
Şirket: {company_name}
Müşteri Aksiyonu: {customer_action}

Bu lifecycle stage için uygun email oluştur.

🔄 Lifecycle Email Özellikleri:

🎯 Stage-Specific Messaging:
- Müşteri journey'deki konum
- Beklenen next action
- Value demonstration method

📧 Content Strategy:
- Relationship building approach
- Information vs. promotion balance
- Trust and credibility factors

💡 Behavioral Triggers:
- Action-based personalization
- Timing optimization
- Frequency considerations

Email İçeriği:
1. Stage-appropriate selamlama
2. Relevant value proposition
3. Clear next steps
4. Relationship building elements
5. Future communication preview

Format: Direkt kullanılabilir email formatında hazırla."""