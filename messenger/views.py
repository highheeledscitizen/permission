from django.shortcuts import render, redirect, get_object_or_404
from .models import Chat, Message
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.views.generic import TemplateView,ListView
from .mixin import (ChatMemberRequiredMixin,
                    SuperuserRequiredMixin,
                    AddChatPermissionMixin,
                    MessageDeleteMixin,
                    MessageEditMixin,
                    DeleteEditeRequiredMixin)

User = get_user_model()


class Home(TemplateView):
    template_name = 'home.html'


class ChatList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'messenger.can_view_chat_list'

    model = Chat
    template_name = 'chat_list.html'
    context_object_name = 'chat_list'


class ChatView(LoginRequiredMixin, PermissionRequiredMixin, ChatMemberRequiredMixin, View):
    permission_required = 'messenger.can_view_chat_list'

    def get(self, request, chat_id):
        messages = Message.objects.filter(chat_id=chat_id)
        users = self.chat.members.all()
        return render(request, 'chat_view.html', {'messages': messages,
                                                                      'users': users,
                                                                      'current_user': request.user,
                                                                      'chat': self.chat})

    def post(self, request, chat_id):
        text = request.POST.get('text')
        new_message = Message(text=text,
                              author=request.user,
                              chat_id=self.chat)
        new_message.save()

        return redirect('chat_view', chat_id)


class ChatCreate(LoginRequiredMixin, SuperuserRequiredMixin, AddChatPermissionMixin, View):
    def get(self, request):
        users = User.objects.all()
        return render(request, "chat_create.html", {'members': users})

    def post(self, request):
        chat_name = request.POST.get('chat_name')
        users_select = request.POST.getlist('users_select')
        selected_users = User.objects.filter(id__in=users_select)

        self.add_chat_permission(selected_users)

        new_chat = Chat.objects.create(chat_name=chat_name)
        new_chat.members.set(selected_users)
        new_chat.save()

        return redirect('chat_list')


class MessageDelete(LoginRequiredMixin, MessageDeleteMixin, View):
    def get(self, request, message_id):
        return self.delete_message(request, message_id)


class MessageEdit(LoginRequiredMixin, MessageEditMixin, DeleteEditeRequiredMixin, View):
    def get(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        if self.can_edit_or_delete_message(request, message):
            return render(request, "edit_message.html", {'message': message})
        else:
            return redirect('access_required')

    def post(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)

        self.edit_message(request, message)
        chat_id = str(message.chat_id.id)
        return redirect('/chat/' + chat_id)


def access_required_page(request):
    return render(request, "system/access_required.html")
