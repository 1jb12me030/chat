from django.urls import path
from chatapp.views import UserRegistrationView, UserLoginView, UserLogoutView, UserListView, ChatListView, ChatCreateView



urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('chats/', ChatListView.as_view(), name='chat-list'),
    path('chats/create/', ChatCreateView.as_view(), name='chat-create'),
]
