from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import*
from django.urls import reverse_lazy
from .utils import extract_entities, generate_response_based_on_entities, analyze_sentiment
from .models import *
# Create your views here.
from django.contrib.auth import authenticate,logout, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import LoginForm
from django.views.generic.edit import CreateView
from .forms import SignupForm
from django.contrib.auth import get_user_model

class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login_view')

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return super().form_valid(form)

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, password=password)

        if user is not None:
            auth_login(self.request, user)

            # Retrieve or create the token for the user
            token, created = Token.objects.get_or_create(user=user)

            # Store token in context to display
            context = self.get_context_data()
            context['token'] = token.key

            try:
                customer = Customer.objects.get(user=user)
                if customer.company:
                    return redirect('home')  # Redirect to home if company exists
                else:
                    return redirect('company_create')  # Redirect to company creation if no company exists
            except Customer.DoesNotExist:
                return redirect('company_create')  # Redirect if no customer exists
        else:
            messages.error(self.request, "Invalid email or password.")
            return self.form_invalid(form)

class LogoutView(RedirectView):
    url = reverse_lazy('login_view')

    def get(self, request, *args, **kwargs):
        user = request.user

        # Delete the user's token to invalidate their session
        Token.objects.filter(user=user).delete()

        logout(request)
        return super().get(request, *args, **kwargs)

class UserProfileListView(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'userprofile_list.html'
    context_object_name = 'profiles'
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'userprofile_detail.html'
    context_object_name = 'profile'


class UserProfileCreateView(LoginRequiredMixin, CreateView):
    model = UserProfile
    template_name = 'userprofile_form.html'
    fields = ['bio', 'avatar']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('userprofile_list')
    
class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'userprofile_form.html'
    fields = ['bio', 'avatar']
    
    def get_success_url(self):
        return reverse_lazy('userprofile_detail', kwargs={'pk': self.object.pk})
    

class UserProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = UserProfile
    template_name = 'userprofile_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('userprofile_list')
    

class ChatSessionListView(LoginRequiredMixin, ListView):
    model = ChatSession
    template_name = 'chatsession_list.html'
    context_object_name = 'sessions'
    
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)
    
class ChatSessionDetailView(LoginRequiredMixin, DetailView):
    model = ChatSession
    template_name = 'chatsession_detail.html'
    context_object_name = 'session'


class ChatSessionCreateView(LoginRequiredMixin, CreateView):
    model = ChatSession
    template_name = 'chatsession_form.html'
    fields = ['session_id', 'is_active']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('chatsession_list')
    
class ChatSessionUpdateView(LoginRequiredMixin, UpdateView):
    model = ChatSession
    template_name = 'chatsession_form.html'
    fields = ['end_time', 'is_active', 'user_feedback']
    
    def get_success_url(self):
        return reverse_lazy('chatsession_detail', kwargs={'pk': self.object.pk})
    
class ChatSessionDeleteView(LoginRequiredMixin, DeleteView):
    model = ChatSession
    template_name = 'chatsession_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('chatsession_list')
    
class ChatMessageListView(LoginRequiredMixin, ListView):
    model = ChatMessage
    template_name = 'chatmessage_list.html'
    context_object_name = 'messages'
    
    def get_queryset(self):
        return ChatMessage.objects.filter(session__user=self.request.user)
    
class ChatMessageDetailView(LoginRequiredMixin, DetailView):
    model = ChatMessage
    template_name = 'chatmessage_detail.html'
    context_object_name = 'message'

class ChatMessageCreateView(LoginRequiredMixin, CreateView):
    model = ChatMessage
    template_name = 'chatmessage_form.html'
    fields = ['session', 'sender', 'message_type', 'message']
    
    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            form.instance.sender = 'Anonymous'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('chatmessage_list')
    
class ChatMessageUpdateView(LoginRequiredMixin, UpdateView):
    model = ChatMessage
    template_name = 'chatmessage_form.html'
    fields = ['message', 'is_read']
    
    def get_success_url(self):
        return reverse_lazy('chatmessage_detail', kwargs={'pk': self.object.pk})

class ChatMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = ChatMessage
    template_name = 'chatmessage_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('chatmessage_list')
    
class BotConfigListView(LoginRequiredMixin, ListView):
    model = BotConfig
    template_name = 'botconfig_list.html'
    context_object_name = 'bots'
    
class BotConfigDetailView(LoginRequiredMixin, DetailView):
    model = BotConfig
    template_name = 'botconfig_detail.html'
    context_object_name = 'bot'

class BotConfigCreateView(LoginRequiredMixin, CreateView):
    model = BotConfig
    template_name = 'botconfig_form.html'
    fields = ['name', 'description', 'is_active', 'welcome_message']
    
    def get_success_url(self):
        return reverse_lazy('botconfig_list')
    
class BotConfigUpdateView(LoginRequiredMixin, UpdateView):
    model = BotConfig
    template_name = 'botconfig_form.html'
    fields = ['description', 'is_active', 'welcome_message']
    
    def get_success_url(self):
        return reverse_lazy('botconfig_detail', kwargs={'pk': self.object.pk})
    

class BotConfigDeleteView(LoginRequiredMixin, DeleteView):
    model = BotConfig
    template_name = 'botconfig_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('botconfig_list')
    

class FeedbackListView(LoginRequiredMixin, ListView):
    model = Feedback
    template_name = 'feedback_list.html'
    context_object_name = 'feedbacks'
    
    def get_queryset(self):
        return Feedback.objects.filter(chat_session__user=self.request.user)
    

class FeedbackDetailView(LoginRequiredMixin, DetailView):
    model = Feedback
    template_name = 'feedback_detail.html'
    context_object_name = 'feedback'


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    template_name = 'feedback_form.html'
    fields = ['chat_session', 'rating', 'comments']
    
    def form_valid(self, form):
        chat_session = form.instance.chat_session
        if chat_session.user != self.request.user:
            form.add_error(None, "You cannot submit feedback for this session.")
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('feedback_list')
    
class FeedbackUpdateView(LoginRequiredMixin, UpdateView):
    model = Feedback
    template_name = 'feedback_form.html'
    fields = ['rating', 'comments']
    
    def get_success_url(self):
        return reverse_lazy('feedback_detail', kwargs={'pk': self.object.pk})
    

class FeedbackDeleteView(LoginRequiredMixin, DeleteView):
    model = Feedback
    template_name = 'feedback_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('feedback_list')
    
def base(request):
    return render(request, 'base.html') 

def index(request):
    return render(request, 'index.html')   



