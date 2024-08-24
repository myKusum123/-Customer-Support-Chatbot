from django.contrib import admin
from .models import*

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(ChatSession)
admin.site.register(ChatMessage)
admin.site.register(BotConfig)
admin.site.register(Feedback)
