from rest_framework import serializers
from messenger.models import Message, Chat
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'author', 'published_time', 'chat_id']


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'chat_name', 'members']


class MessageWithUserSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Message
        fields = ['id', 'text', 'author', 'published_time', 'chat_id']
