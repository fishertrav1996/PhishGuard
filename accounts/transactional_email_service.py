"""
Production-quality transactional account email service for PhishGuard.

Supports both SMTP (Gmail for testing) and AWS SES (for production).
Follows industry best practices for transactional emails.
"""

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import logging

# Email header for high priority emails
HIGH_PRIORITY_HEADER = '1'  
MAILER_SERVICE_HEADER = 'PhishGuard Transactional Email Service'

# Initialize logger
logger = logging.getLogger(__name__)


class TransactionalEmailService:
    """
    Abstraction layer for sending transactional account emails only.
    
    DO NOT use this for phishing simulation emails - those are sent 
    via the campaigns app using direct SMTP to maintain separation.
    """
    
    @staticmethod
    def get_from_email():
        """Get the FROM email address for transactional emails"""
        return settings.DEFAULT_FROM_EMAIL
    
    @staticmethod
    def send_verification_email(user, verification_url):
        """
        Send email verification link to user.
        
        Args:
            user: Django User object
            verification_url: Complete verification URL with token
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Render HTML email from template
            html_content = render_to_string('accounts/emails/verify_email.html', {
                'user': user,
                'verification_url': verification_url,
                'site_name': 'PhishGuard',
                'support_email': TransactionalEmailService.get_from_email(),
            })
            
            # Generate plain text version (fallback)
            text_content = strip_tags(html_content)
            
            # Create email with both HTML and plain text versions
            email = EmailMultiAlternatives(
                subject='Verify Your PhishGuard Email Address',
                body=text_content,
                from_email=TransactionalEmailService.get_from_email(),
                to=[user.email],
                headers={
                    'X-Priority': HIGH_PRIORITY_HEADER,  # High priority for verification emails
                    'X-Mailer': MAILER_SERVICE_HEADER,
                }
            )
            email.attach_alternative(html_content, "text/html")
            
            # Send email
            email.send(fail_silently=False)
            
            logger.info(f"Verification email sent successfully to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send verification email to {user.email}: {str(e)}")
            return False
    
    @staticmethod
    def send_welcome_email(user):
        """
        Send welcome email after user verifies their email.
        
        Args:
            user: Django User object
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Render HTML email from template
            html_content = render_to_string('accounts/emails/welcome_email.html', {
                'user': user,
                'site_name': 'PhishGuard',
                'support_email': TransactionalEmailService.get_from_email(),
                'login_url': settings.BASE_URL + '/accounts/login',
            })
            
            # Generate plain text version
            text_content = strip_tags(html_content)
            
            # Create email
            email = EmailMultiAlternatives(
                subject='Welcome to PhishGuard! 🎉',
                body=text_content,
                from_email=TransactionalEmailService.get_from_email(),
                to=[user.email],
            )
            email.attach_alternative(html_content, "text/html")
            
            # Send email
            email.send(fail_silently=False)
            
            logger.info(f"Welcome email sent successfully to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send welcome email to {user.email}: {str(e)}")
            return False
    
    @staticmethod
    def send_password_reset_email(user, reset_url):
        """
        Send password reset link to user.
        
        Args:
            user: Django User object
            reset_url: Complete password reset URL with token
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            html_content = render_to_string('accounts/emails/password_reset.html', {
                'user': user,
                'reset_url': reset_url,
                'site_name': 'PhishGuard',
                'support_email': settings.DEFAULT_FROM_EMAIL,
            })
            
            text_content = strip_tags(html_content)
            
            email = EmailMultiAlternatives(
                subject='Reset Your PhishGuard Password',
                body=text_content,
                from_email=TransactionalEmailService.get_from_email(),
                to=[user.email],
                headers={
                    'X-Priority': HIGH_PRIORITY_HEADER
                }
            )
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)
            
            logger.info(f"Password reset email sent successfully to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send password reset email to {user.email}: {str(e)}")
            return False
