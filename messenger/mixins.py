from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from .models import Chat, Message, LogEntry
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class ChatMemberRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        chat_id = kwargs.get('chat_id')
        chat = get_object_or_404(Chat, id=chat_id)
        self.chat = chat
        if request.user in chat.members.all() or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('access_required')


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class AddChatPermissionMixin:
    def add_chat_permission(self,selected_user):
        content_type = ContentType.objects.get_for_model(Chat)
        permission = Permission.objects.get(
            codename="can_view_chat_list",
            content_type=content_type,
        )

        for user in selected_user:
            user.user_permissions.add(permission)


class DeleteEditeRequiredMixin:
    def can_edit_or_delete_message(self, request, message):
        if message.author:
            return message.author == request.user and (timezone.now().date() - message.published_time).days < 1
        return True


class MessageDeleteMixin(DeleteEditeRequiredMixin):
    def delete_message(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        chat_id = str(message.chat_id.id)
        if self.can_edit_or_delete_message(request, message):
            message.delete()
        return redirect('/chat/' + chat_id)


class MessageEditMixin(DeleteEditeRequiredMixin):
    def edit_message(self, request, message):
        if self.can_edit_or_delete_message(request, message):
            message.text = request.POST.get('text')
            message.save()
        else:
            return redirect('access_required')

class LogOnCreateMixin:
    def log_on_create(self, message):
            LogEntry.objects.create(
                action='Created message:' + message.id,
                author=message.author
            )

class LogOnUpdateMixin:
    def log_on_update(self, message):
        LogEntry.objects.create(
            action='Created message:' + message.id,
            author=message.author
        )


class LogOnDeleteMixin:
    def log_on_delete(self, message):
        LogEntry.objects.create(
            action='Created message:' + message.id,
            author=message.author
        )


class LogOnViewMixin:
    def log_on_view(self, message):
        LogEntry.objects.create(
            action='Created message:' + message.id,
            author=message.author
        )

