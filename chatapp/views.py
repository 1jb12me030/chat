from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as django_logout
from .serializers import *
#User = get_user_model()
from .models import *

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = User.objects.get(id=token.user_id)
        data = {
            'token': token.key,
            'user_id': user.id,
            'email': user.email,
            'name': user.name
        }
        return Response(data)

class UserLogoutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        django_logout(request)
        return Response({'message': 'Logout successful'})


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        sender_id = self.request.query_params.get('sender_id')
        recipient_id = self.request.query_params.get('recipient_id')
        return Chat.objects.filter(
            models.Q(sender_id=sender_id, recipient_id=recipient_id) |
            models.Q(sender_id=recipient_id, recipient_id=sender_id)
        ).order_by('created_at')
        
from rest_framework.exceptions import ValidationError   

     
class ChatCreateView(generics.CreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def perform_create(self, serializer):
        try:
            token = Token.objects.get(key=self.request.auth)
        except Token.DoesNotExist:
            raise ValidationError("Invalid token.")

        serializer.save(sender=token.user, is_sender=True)

    # def perform_create(self, serializer):
    #     user = Token.objects.get(key=self.request.auth).user
    #     serializer.save(sender=user, is_sender=True)