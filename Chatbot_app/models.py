from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.email

class ChatSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_sessions', null=True, blank=True)
    session_id = models.CharField(max_length=255, unique=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    user_feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Session {self.session_id} for {self.user.email if self.user else 'Anonymous'}"

class ChatMessage(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('link', 'Link'),
    ]

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=50)  # 'User' or 'Bot'
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, default='text')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Track if the message was read

    def __str__(self):
        return f"{self.sender}: {self.message[:50]}... ({self.timestamp})"

class BotConfig(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    welcome_message = models.TextField(default="Hello! How can I assist you today?")

    def __str__(self):
        return self.name

class Feedback(models.Model):
    chat_session = models.OneToOneField(ChatSession, on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Rating from 1 to 5
    comments = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for Session {self.chat_session.session_id}"
