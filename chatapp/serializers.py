from rest_framework import serializers
from .models import *

#User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'gender', 'dob', 'contact_no']
        extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     return user
class ChatSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.name', read_only=True)
    recipient_name = serializers.CharField(source='recipient.name', read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'sender', 'sender_name', 'recipient', 'recipient_name', 'message', 'created_at']
