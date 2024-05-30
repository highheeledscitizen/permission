"""hw7 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from messenger import views


urlpatterns = [
    path('', views.home, name='home'),
    path('chat_list/', views.chat_list, name='chat_list'),
    path('chat/<int:chat_id>/', views.chat_view, name='chat_view'),
    path('chat_create/', views.chat_create, name='chat_create'),
    path('access_required/', views.access_required_page, name='access_required'),
    path('chat/delete-message/<int:message_id>/', views.message_delete, name='message_delete'),
    path('chat/edit-message/<int:message_id>/', views.edit_message, name='edit_message'),

]
