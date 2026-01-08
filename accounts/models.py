from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.crypto import get_random_string
import hashlib
from datetime import timedelta

TOKEN_LENGTH = 64  # Length of the random token string
TOKEN_EXPIRY_HOURS = 24  # Token validity duration in hours
EMAIL_VERIFICATION_RESEND_LIMIT_MINUTES = 5  # Minimum minutes between resending verification emails

class EmailVerificationToken(models.Model):
    """
    Secure token for email verification during signup.
    Uses cryptographically secure random strings hashed with SHA-256.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_tokens')
    token_hash = models.CharField(max_length=TOKEN_LENGTH, unique=True, db_index=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['token_hash', 'used_at']),
        ]
    
    @staticmethod
    def generate_token():
        """Generate a cryptographically secure random token"""
        return get_random_string(length=TOKEN_LENGTH)
    
    @staticmethod
    def hash_token(token):
        """Hash token using SHA-256"""
        return hashlib.sha256(token.encode()).hexdigest()
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            # Set token expiry time
            self.expires_at = timezone.now() + timedelta(hours=TOKEN_EXPIRY_HOURS)
        super().save(*args, **kwargs)
    
    def is_valid(self):
        """Check if token is still valid (not used and not expired)"""
        return not self.used_at and timezone.now() < self.expires_at
    
    #TODO: We should delete used tokens at some point. Either a periodic task or upon usage.
    def mark_used(self):
        """Mark token as used"""
        self.used_at = timezone.now()
        self.save()
    
    def __str__(self):
        return f"Verification token for {self.user.username}"


class UserProfile(models.Model):
    """Extended user profile for email verification and onboarding tracking"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    verification_emails_sent = models.IntegerField(default=0)
    last_verification_email_sent = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def can_resend_verification(self):
        """
        Rate limiting for resending verification email every X minutes
        """
        if not self.last_verification_email_sent:
            return True
        time_since_last = timezone.now() - self.last_verification_email_sent
        return time_since_last > timedelta(minutes=EMAIL_VERIFICATION_RESEND_LIMIT_MINUTES)
    
    def record_verification_sent(self):
        """Record that a verification email was sent"""
        self.verification_emails_sent += 1
        self.last_verification_email_sent = timezone.now()
        self.save()
    
    def verify_email(self):
        """Mark email as verified"""
        self.email_verified = True
        self.email_verified_at = timezone.now()
        self.save()
    
    def __str__(self):
        return f"Profile for {self.user.username}"

