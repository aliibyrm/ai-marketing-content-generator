class SocialMediaPrompts:
    """Social media content generation prompts"""
    
    def get_system_prompt(self, platform: str, tone: str = "professional") -> str:
        """Get system prompt for social media content generation"""
        
        platform_specs = {
            "instagram": {
                "style": "görsel odaklı, yaratıcı ve engaging",
                "features": "hikaye anlatımı, hashtag'ler, emoji'ler",
                "best_practices": "9:16 görsel formatı için optimize, carousel postlar için uygun"
            },
            "twitter": {
                "style": "kısa, akılda kalıcı ve conversation starter",
                "features": "thread potansiyeli, retweet değeri, trending konular",
                "best_practices": "280 karakter limiti, hashtag'ler dikkatli kullanım"
            },
            "linkedin": {
                "style": "profesyonel, değer odaklı ve network building",
                "features": "industry insights, thought leadership, professional growth",
                "best_practices": "uzun-form content, meaningful connections"
            },
            "facebook": {
                "style": "community odaklı, paylaşılabilir ve tartışma açıcı",
                "features": "group sharing, family-friendly, local community",
                "best_practices": "engaging questions, shareable content"
            }
        }
        
        tone_descriptions = {
            "professional": "profesyonel, güvenilir ve uzman",
            "casual": "samimi, dostça ve yaklaşılabilir", 
            "exciting": "heyecanlı, enerjik ve motivasyonel",
            "informative": "bilgilendirici, açıklayıcı ve eğitici",
            "persuasive": "ikna edici, satış odaklı ve aksiyon odaklı"
        }
        
        platform_info = platform_specs.get(platform, platform_specs["instagram"])
        tone_desc = tone_descriptions.get(tone, "profesyonel")
        
        return f"""Sen uzman bir sosyal medya content creator'ısın. {platform.title()} platformu için {tone_desc} tonunda içerik oluşturuyorsun.

Platform Özellikleri:
- Stil: {platform_info['style']}
- Özellikler: {platform_info['features']}
- En İyi Uygulamalar: {platform_info['best_practices']}

İçerik Kuralları:
1. Hedef kitleye uygun dil kullan
2. Platform sınırlarını göz önünde bulundur
3. Engagement arttıracak unsurlar ekle
4. Brand voice'i koruy
5. Actionable content üret
6. Türkçe dilbilgisi kurallarına uy

Kaçınılacaklar:
- Spam benzeri içerik
- Alakasız hashtag'ler
- Aşırı tanıtım yapma
- Yanlış bilgi verme
- Hedef kitle dışı dil kullanma"""

    def get_platform_prompt(self, 
                           platform: str,
                           post_type: str,
                           topic: str,
                           target_audience: str) -> str:
        """Get platform-specific content generation prompt"""
        
        post_type_templates = {
            "promotional": {
                "structure": "dikkat çekici başlık + değer propositionu + özellikler + CTA",
                "focus": "ürün/hizmetin faydalarını vurgula, satış odaklı"
            },
            "educational": {
                "structure": "problem tanımı + çözüm açıklaması + adım adım rehber + kaynak",
                "focus": "bilgi verme, öğretme, değer katma"
            },
            "entertaining": {
                "structure": "hook + eğlenceli içerik + community engagement + hashtag'ler",
                "focus": "eğlence, viral potansiyel, paylaşılabilirlik"
            },
            "inspirational": {
                "structure": "ilham verici açılış + kişisel hikaye/örnek + motivasyon + call to action",
                "focus": "motivasyon, ilham verme, pozitif enerji"
            },
            "behind_scenes": {
                "structure": "merak uyandırıcı giriş + süreç açıklaması + personal touch + community",
                "focus": "şeffaflık, insan tarafı, güven inşası"
            },
            "user_generated": {
                "structure": "kullanıcı teşekkürü + içerik paylaşımı + community celebration + hashtag",
                "focus": "sosyal kanıt, community building, appreciation"
            },
            "announcement": {
                "structure": "heyecan verici duyuru + detaylar + faydalar + next steps",
                "focus": "bilgi verme, heyecan yaratma, aksiyon alma"
            },
            "question": {
                "structure": "engaging soru + context + seçenekler/görüşler + community invite",
                "focus": "engagement, tartışma başlatma, community input"
            }
        }
        
        platform_guidelines = {
            "instagram": "Görsel odaklı düşün, hikaye anlat, 5-30 hashtag kullan, emoji ekle",
            "twitter": "280 karakter limiti, thread potansiyeli, trending hashtag'ler",
            "linkedin": "Profesyonel ton, industry insights, network değeri, uzun-form OK",
            "facebook": "Community odaklı, paylaşılabilir, family-friendly, tartışma açıcı"
        }
        
        template_info = post_type_templates.get(post_type, post_type_templates["promotional"])
        
        return f"""Konu: {topic}
Hedef Kitle: {target_audience}
Platform: {platform.title()}
Post Türü: {post_type}

İçerik Yapısı:
{template_info['structure']}

Odak Noktası:
{template_info['focus']}

Platform Özel Rehber:
{platform_guidelines.get(platform, '')}

Bu bilgilere dayanarak, hedef kitle için uygun, engaging ve platform özelliklerine uygun bir post oluştur."""

    def get_series_prompt(self, 
                         platform: str, 
                         theme: str, 
                         post_count: int) -> str:
        """Get prompt for generating content series"""
        
        return f"""Theme: {theme}
Platform: {platform.title()}
Post Sayısı: {post_count}

{post_count} adet birbiriyle bağlantılı, tutarlı bir content series oluştur. Her post:

Seri Özellikleri:
1. Ana tema: {theme}
2. Her post bağımsız değer sağlamalı
3. Seri olarak takip edildiğinde daha büyük resmi vermeli
4. Consistent tone ve brand voice
5. Cross-reference ve continuity

Seri Formatı:
- Her post'u "---" ile ayır
- Numaralama ekle (1/5, 2/5, etc.)
- Her post'ta seri referansı yap
- Son post'ta seri özeti

Post İçerikleri:
{self._get_series_structure(post_count)}

Her post platform özelliklerine uygun olsun ve engaging elements içersin."""

    def get_hashtag_prompt(self, 
                          topic: str, 
                          platform: str, 
                          count: int,
                          mix_popular_niche: bool) -> str:
        """Get prompt for hashtag generation"""
        
        hashtag_strategy = "popular ve niche hashtag'lerin karışımı" if mix_popular_niche else "sadece relevant hashtag'ler"
        
        return f"""Konu: {topic}
Platform: {platform.title()}
Hashtag Sayısı: {count}
Strateji: {hashtag_strategy}

{count} adet etkili hashtag oluştur:

Hashtag Kategorileri:
1. Ana konu hashtag'leri (3-5 adet)
2. Niche/spesifik hashtag'ler (2-4 adet)
3. Popular/trending hashtag'ler (2-3 adet)
4. Community hashtag'leri (1-2 adet)
5. Call-to-action hashtag'leri (1-2 adet)

Hashtag Kuralları:
- Türkçe ve İngilizce karışım OK
- Platform trend'lerine uygun
- Spam hashtag'lerden kaçın
- Brand için relevant olsun
- Searchable ve discoverable

Format: Her hashtag yeni satırda, # ile başlayarak"""

    def get_caption_optimization_prompt(self, existing_caption: str) -> str:
        """Get prompt for optimizing existing captions"""
        
        return f"""Mevcut Caption:
{existing_caption}

Bu caption'ı daha etkili hale getir:

Optimizasyon Alanları:
1. Hook - İlk cümle daha çekici
2. Structure - Daha iyi organize
3. Engagement - Daha fazla interaction 
4. Clarity - Daha net mesaj
5. CTA - Daha güçlü call-to-action

Koruyacakların:
- Ana mesaj ve tone
- Marka sesi
- Hedef kitle uyumu

Geliştireceklerin:
- Readability
- Engagement potential
- Visual appeal (line breaks, emojis)
- Action-oriented language

Optimized versiyonu ver, ardından ne değiştirdiğini açıkla."""

    def get_trend_adaptation_prompt(self, topic: str, trend: str) -> str:
        """Get prompt for adapting content to current trends"""
        
        return f"""Ana Konu: {topic}
Güncel Trend: {trend}

Bu trend'i ana konuna uyarlayarak viral potansiyeli yüksek content oluştur:

Trend Uyarlama Stratejisi:
1. Trend'in ne olduğunu açıkla
2. Ana konunla bağlantıyı kur
3. Authentic bir yaklaşım geliştir
4. Meme/viral element ekle
5. Timely ve relevant olsun

Kaçınılacaklar:
- Zoraki trend kullanımı
- Brand voice'ten uzaklaşma
- Late trend adoption
- Controversy için controversy

Trend Format Önerileri:
- Challenge participation
- Meme adaptation  
- Hashtag hijacking (positive)
- Current events tie-in
- Cultural moment leveraging

Creative ve authentic bir yaklaşımla trend'i konu ile birleştir."""

    def _get_series_structure(self, post_count: int) -> str:
        """Get structure suggestions for content series"""
        
        if post_count == 3:
            return """
            Post 1: Problem/Durum Tanımı + Hook
            Post 2: Çözüm/Yaklaşım + Deep Dive
            Post 3: Sonuç/Takeaway + CTA
            """
        elif post_count == 5:
            return """
            Post 1: Introduction + Problem Statement
            Post 2: Background + Context
            Post 3: Solution/Method + Examples
            Post 4: Implementation + Tips
            Post 5: Results + Next Steps
            """
        elif post_count == 7:
            return """
            Post 1: Hook + Series Preview
            Post 2: Problem Definition
            Post 3: Current State Analysis
            Post 4: Solution Framework
            Post 5: Implementation Strategy
            Post 6: Case Study/Examples
            Post 7: Conclusion + Action Items
            """
        else:
            return f"""
            {post_count} post için uygun bir yapı geliştir:
            - Giriş ve dikkat çekme
            - Konu geliştirme ve derinleştirme
            - Pratik örnekler ve uygulamalar
            - Sonuç ve harekete geçirme
            """

    def get_engagement_boost_prompt(self, content: str) -> str:
        """Get prompt for boosting engagement of existing content"""
        
        return f"""Mevcut İçerik:
{content}

Bu içeriği daha engaging hale getir:

Engagement Teknikleri:
1. Soru ekle (audience participation)
2. Poll/survey elements
3. "Double tap if..." statements
4. Story invitation ("Share yours in comments")
5. Challenge/dare elements
6. Relatable scenarios
7. Emoji reactions encouragement
8. Tag a friend requests

Psikolojik Triggerlar:
- Curiosity gap
- Social proof desire  
- FOMO (Fear of Missing Out)
- Belonging need
- Achievement recognition
- Controversy (constructive)

Format İyileştirmeleri:
- Better line breaks
- Strategic emoji placement
- Scannable structure
- Multiple engagement points

Engagement-optimized versiyonu oluştur ve hangi teknikleri kullandığını açıkla."""