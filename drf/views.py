from django.http import Http404
from rest_framework import generics
from messenger.models import Message, Chat
from .serializers import MessageSerializer, ChatSerializer, MessageWithUserSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()


class MessageListCreate(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MessageRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class UserChatList(generics.ListAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        return Chat.objects.filter(members=user)


class UserMessageList(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)

        return Message.objects.filter(author=user, chat_id=chat_id)


class MessageAuthor(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageWithUserSerializer
    lookup_field = 'id'
