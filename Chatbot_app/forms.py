from django import forms
from .models import UserProfile, ChatSession, ChatMessage, BotConfig, Feedback
from django.contrib.auth.forms import UserCreationForm

from core.models import*
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords don't match")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']

class ChatSessionForm(forms.ModelForm):
    class Meta:
        model = ChatSession
        fields = ['session_id', 'is_active']

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['session', 'sender', 'message_type', 'message']

class BotConfigForm(forms.ModelForm):
    class Meta:
        model = BotConfig
        fields = ['name', 'description', 'is_active', 'welcome_message']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['chat_session', 'rating', 'comments']