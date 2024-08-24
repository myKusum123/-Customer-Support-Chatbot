from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import*


urlpatterns = [
    # Authentication URLs
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login_view'),
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('chat/<str:session_id>/', chat_view, name='chat_view'),


    # UserProfile URLs
    path('userprofiles/', UserProfileListView.as_view(), name='userprofile_list'),
    path('userprofiles/<int:pk>/', UserProfileDetailView.as_view(), name='userprofile_detail'),
    path('userprofiles/new/', UserProfileCreateView.as_view(), name='userprofile_create'),
    path('userprofiles/edit/<int:pk>/', UserProfileUpdateView.as_view(), name='userprofile_update'),
    path('userprofiles/delete/<int:pk>/', UserProfileDeleteView.as_view(), name='userprofile_delete'),

    # ChatSession URLs
    path('chatsessions/', ChatSessionListView.as_view(), name='chatsession_list'),
    path('chatsessions/<int:pk>/', ChatSessionDetailView.as_view(), name='chatsession_detail'),
    path('chatsessions/new/', ChatSessionCreateView.as_view(), name='chatsession_create'),
    path('chatsessions/edit/<int:pk>/', ChatSessionUpdateView.as_view(), name='chatsession_update'),
    path('chatsessions/delete/<int:pk>/', ChatSessionDeleteView.as_view(), name='chatsession_delete'),

    # ChatMessage URLs
    path('chatmessages/', ChatMessageListView.as_view(), name='chatmessage_list'),
    path('chatmessages/<int:pk>/', ChatMessageDetailView.as_view(), name='chatmessage_detail'),
    path('chatmessages/new/', ChatMessageCreateView.as_view(), name='chatmessage_create'),
    path('chatmessages/edit/<int:pk>/', ChatMessageUpdateView.as_view(), name='chatmessage_update'),
    path('chatmessages/delete/<int:pk>/', ChatMessageDeleteView.as_view(), name='chatmessage_delete'),

    # BotConfig URLs
    path('botconfigs/', BotConfigListView.as_view(), name='botconfig_list'),
    path('botconfigs/<int:pk>/', BotConfigDetailView.as_view(), name='botconfig_detail'),
    path('botconfigs/new/', BotConfigCreateView.as_view(), name='botconfig_create'),
    path('botconfigs/edit/<int:pk>/', BotConfigUpdateView.as_view(), name='botconfig_update'),
    path('botconfigs/delete/<int:pk>/', BotConfigDeleteView.as_view(), name='botconfig_delete'),

    # Feedback URLs
    path('feedbacks/', FeedbackListView.as_view(), name='feedback_list'),
    path('feedbacks/<int:pk>/', FeedbackDetailView.as_view(), name='feedback_detail'),
    path('feedbacks/new/', FeedbackCreateView.as_view(), name='feedback_create'),
    path('feedbacks/edit/<int:pk>/', FeedbackUpdateView.as_view(), name='feedback_update'),
    path('feedbacks/delete/<int:pk>/', FeedbackDeleteView.as_view(), name='feedback_delete'),

    # Base and Index URLs
    path('', index, name='index'),
    path('base/', base, name='base'),
]


