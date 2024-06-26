from django.urls import path
from .views import (MessageListCreate,
                    UserMessageList,
                    MessageAuthor,
                    MessageRetrieveUpdateDestroy,
                    UserChatList
                    )

urlpatterns = [
    path('user/<str:username>/chats/', UserChatList.as_view(), name='user_chat_list'),
    path('user/<str:username>/chat/<int:chat_id>/messages/', UserMessageList.as_view(), name='user_message_list'),
    path('message/<int:id>/', MessageAuthor.as_view(), name='message_author'),
    path('message/', MessageListCreate.as_view(), name='message_list_create'),
    path('message/<int:pk>/edit/', MessageRetrieveUpdateDestroy.as_view(), name='message_RUD'),
]
