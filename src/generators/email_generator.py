from generators.base_generator import BaseGenerator
from utils.api_handler import PromptOptimizer
from prompts.email_prompts import EmailPrompts

class EmailGenerator(BaseGenerator):
    """Generate email marketing content for various purposes"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        super().__init__(api_key, model)
        self.prompts = EmailPrompts()
    
    def generate_content(self, **kwargs) -> dict:
        """
        Generate content based on parameters (abstract method implementation)
        
        Returns:
            Dict containing generated content and metadata
        """
        # Default to generate_email if no specific method is called
        return self.generate_email(**kwargs)
    
    def generate_email(self,
                      email_type: str,
                      company_name: str,
                      main_topic: str,
                      target_audience: str = "Mevcut Müşteriler",
                      email_goal: str = "Satış Artışı",
                      tone: str = "professional",
                      include_personalization: bool = True,
                      include_social_proof: bool = False,
                      include_urgency: bool = False,
                      include_discount: bool = False,
                      cta_text: str = "Hemen İncele",
                      cta_url: str = "",
                      sender_name: str = "",
                      preheader_text: str = "",
                      email_length: str = "Orta",
                      custom_instructions: str = "",
                      creativity_level: float = 0.6) -> dict:
        """
        Generate a complete email marketing content
        
        Args:
            email_type: Type of email (newsletter, promotional, welcome, etc.)
            company_name: Company or brand name
            main_topic: Main topic or campaign
            target_audience: Target audience description
            email_goal: Goal of the email
            tone: Email tone
            include_personalization: Include personalization elements
            include_social_proof: Include social proof
            include_urgency: Include urgency elements
            include_discount: Include discount/offer
            cta_text: Call-to-action text
            cta_url: CTA URL
            sender_name: Sender name
            preheader_text: Preheader text
            email_length: Email length preference
            custom_instructions: Additional instructions
            creativity_level: AI creativity level (0-1)
        
        Returns:
            Dict with generated email content and metadata
        """
        
        # Generate subject line first
        subject_result = self.generate_subject_line(
            email_type=email_type,
            main_topic=main_topic,
            company_name=company_name,
            tone=tone,
            include_urgency=include_urgency,
            include_discount=include_discount
        )
        
        if not subject_result['success']:
            return subject_result
        
        # Get email-specific prompt
        base_prompt = self.prompts.get_email_prompt(
            email_type=email_type,
            company_name=company_name,
            main_topic=main_topic,
            target_audience=target_audience,
            email_goal=email_goal
        )
        
        # Add optional elements
        optional_elements = []
        if include_personalization:
            optional_elements.append("kişiselleştirme unsurları")
        if include_social_proof:
            optional_elements.append("sosyal kanıt örnekleri")
        if include_urgency:
            optional_elements.append("aciliyet unsurları")
        if include_discount:
            optional_elements.append("indirim/teklif detayları")
        
        if optional_elements:
            base_prompt += f"\n\nDahil edilecek unsurlar: {', '.join(optional_elements)}"
        
        # Add CTA information
        base_prompt += f"\n\nCall-to-Action: '{cta_text}'"
        if cta_url:
            base_prompt += f" (Link: {cta_url})"
        
        # Add length preference
        length_mapping = {
            "Kısa": "50-100 kelime arasında kısa ve öz",
            "Orta": "100-200 kelime arasında dengeli",
            "Uzun": "200+ kelime detaylı açıklamalar ile"
        }
        base_prompt += f"\n\nEmail uzunluğu: {length_mapping.get(email_length, 'Orta')}"
        
        # Add custom instructions
        if custom_instructions:
            base_prompt += f"\n\nEk talimatlar: {custom_instructions}"
        
        # Get system prompt
        system_prompt = self.prompts.get_system_prompt(email_type, tone)
        
        # Optimize prompt
        optimized_prompt = PromptOptimizer.optimize_prompt(
            base_prompt=base_prompt,
            content_type="email",
            platform="email",
            tone=tone,
            target_audience=target_audience
        )
        
        # Generate email content
        content_result = self.api_handler.generate_content(
            prompt=optimized_prompt,
            system_prompt=system_prompt,
            max_tokens=self._get_max_tokens_for_length(email_length),
            temperature=creativity_level
        )
        
        if content_result['success']:
            # Process and structure the email
            processed_email = self._process_email_content(
                subject=subject_result['subject'],
                content=content_result['content'],
                preheader=preheader_text,
                cta_text=cta_text,
                sender_name=sender_name or company_name
            )
            
            # Combine results
            result = {
                'success': True,
                'email_data': processed_email,
                'model': self.model,
                'tokens_used': content_result['tokens_used'] + subject_result.get('tokens_used', 0),
                'generation_time': content_result['generation_time'] + subject_result.get('generation_time', 0),
                'cost_estimate': content_result['cost_estimate'] + subject_result.get('cost_estimate', 0)
            }
            
            return result
        else:
            return content_result
    
    def generate_subject_line(self,
                            email_type: str,
                            main_topic: str,
                            company_name: str,
                            tone: str = "professional",
                            include_urgency: bool = False,
                            include_discount: bool = False,
                            count: int = 1) -> dict:
        """
        Generate email subject lines
        
        Args:
            email_type: Type of email
            main_topic: Main topic
            company_name: Company name
            tone: Tone of voice
            include_urgency: Include urgency elements
            include_discount: Include discount elements
            count: Number of subject lines to generate
        
        Returns:
            Dict with generated subject lines
        """
        
        subject_prompt = self.prompts.get_subject_line_prompt(
            email_type=email_type,
            main_topic=main_topic,
            company_name=company_name,
            include_urgency=include_urgency,
            include_discount=include_discount,
            count=count
        )
        
        system_prompt = f"Sen uzman bir email marketing specialist'ısın. {tone} tonunda etkili konu satırları oluşturuyorsun."
        
        result = self.api_handler.generate_content(
            prompt=subject_prompt,
            system_prompt=system_prompt,
            max_tokens=200,
            temperature=0.8
        )
        
        if result['success']:
            if count == 1:
                # Single subject line
                subject = result['content'].strip().split('\n')[0]
                subject = subject.replace('"', '').replace("'", "").strip()
                result['subject'] = subject
            else:
                # Multiple subject lines
                subjects = [line.strip().replace('"', '').replace("'", "") 
                          for line in result['content'].strip().split('\n') 
                          if line.strip()]
                result['subjects'] = subjects[:count]
        
        return result
    
    def generate_email_series(self,
                            email_type: str,
                            company_name: str,
                            campaign_theme: str,
                            series_count: int = 3,
                            **kwargs) -> dict:
        """
        Generate a series of related emails
        
        Args:
            email_type: Base email type
            company_name: Company name
            campaign_theme: Overall campaign theme
            series_count: Number of emails in series
            **kwargs: Additional parameters
        
        Returns:
            Dict with generated email series
        """
        
        series_prompt = self.prompts.get_series_prompt(
            email_type=email_type,
            company_name=company_name,
            campaign_theme=campaign_theme,
            series_count=series_count
        )
        
        system_prompt = self.prompts.get_system_prompt(
            email_type, 
            kwargs.get('tone', 'professional')
        )
        
        result = self.api_handler.generate_content(
            prompt=series_prompt,
            system_prompt=system_prompt,
            max_tokens=self._get_max_tokens_for_length("Uzun") * series_count,
            temperature=kwargs.get('creativity_level', 0.6)
        )
        
        if result['success']:
            # Split content into individual emails
            emails = self._split_email_series(result['content'], series_count)
            result['email_series'] = emails
            result['series_count'] = len(emails)
        
        return result
    
    def optimize_email_deliverability(self, email_content: str) -> dict:
        """
        Optimize email for better deliverability
        
        Args:
            email_content: Email content to optimize
        
        Returns:
            Dict with optimization suggestions and improved content
        """
        
        deliverability_prompt = self.prompts.get_deliverability_prompt(email_content)
        
        result = self.api_handler.generate_content(
            prompt=deliverability_prompt,
            max_tokens=800,
            temperature=0.3
        )
        
        if result['success']:
            # Parse optimization results
            result['suggestions'] = self._parse_deliverability_suggestions(result['content'])
        
        return result
    
    def _get_max_tokens_for_length(self, length: str) -> int:
        """Get appropriate max tokens for email length"""
        token_mapping = {
            "Kısa": 300,
            "Orta": 600,
            "Uzun": 1000
        }
        return token_mapping.get(length, 600)
    
    def _process_email_content(self, 
                             subject: str, 
                             content: str, 
                             preheader: str = "",
                             cta_text: str = "",
                             sender_name: str = "") -> dict:
        """Process and structure email content"""
        
        # Clean content
        content = content.strip()
        
        # Ensure proper formatting
        if not content.startswith(('Merhaba', 'Sayın', 'Sevgili')):
            if sender_name:
                content = f"Merhaba,\n\n{content}"
            else:
                content = f"Sayın Müşterimiz,\n\n{content}"
        
        # Ensure closing
        if not any(content.endswith(ending) for ending in ['saygılarımızla,', 'sevgilerle,', 'iyi günler,']):
            content += f"\n\nSaygılarımızla,\n{sender_name or 'Ekibimiz'}"
        
        # Add CTA if not present
        if cta_text and cta_text.lower() not in content.lower():
            content += f"\n\n[{cta_text}]"
        
        return {
            'subject': subject,
            'preheader': preheader,
            'content': content,
            'sender': sender_name,
            'cta_text': cta_text
        }
    
    def _split_email_series(self, content: str, expected_count: int) -> list:
        """Split series content into individual emails"""
        
        # Try different splitting patterns
        separators = [
            '\n\n---\n\n',
            '\n\nEmail',
            '\n\n**Email',
            '\n\n1.',
            '\n\n2.',
            '\n\n3.'
        ]
        
        emails = []
        for separator in separators:
            if separator in content:
                emails = [email.strip() for email in content.split(separator) if email.strip()]
                break
        
        # Fallback: split by paragraph breaks
        if not emails:
            emails = [email.strip() for email in content.split('\n\n') if len(email.strip()) > 50]
        
        # Ensure we have the expected number
        if len(emails) < expected_count:
            emails.extend(['[Ek email içeriği gerekli]'] * (expected_count - len(emails)))
        elif len(emails) > expected_count:
            emails = emails[:expected_count]
        
        # Structure each email
        structured_emails = []
        for i, email in enumerate(emails, 1):
            structured_emails.append({
                'sequence': i,
                'subject': f'[Email {i}] Subject needed',
                'content': email
            })
        
        return structured_emails
    
    def _parse_deliverability_suggestions(self, content: str) -> list:
        """Parse deliverability optimization suggestions"""
        
        suggestions = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                suggestion = line.lstrip('-•*').strip()
                if suggestion:
                    suggestions.append(suggestion)
        
        return suggestions
    
    def generate_preheader(self, subject: str, main_message: str) -> str:
        """Generate preheader text that complements the subject line"""
        
        preheader_prompt = f"""
        Konu satırı: {subject}
        Ana mesaj: {main_message}
        
        Bu konu satırını destekleyen, merak uyandırıcı ve 90 karakter altında bir preheader text oluştur.
        Preheader konu satırını tekrarlamamalı, ek bilgi ve context sağlamalı.
        """
        
        result = self.api_handler.generate_content(
            prompt=preheader_prompt,
            max_tokens=100,
            temperature=0.7
        )
        
        if result['success']:
            preheader = result['content'].strip().replace('"', '')
            return preheader[:90]  # Ensure character limit
        
        return ""