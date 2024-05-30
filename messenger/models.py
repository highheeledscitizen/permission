from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Chat(models.Model):

    chat_name = models.CharField(max_length=50, blank=False)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.chat_name

    class Meta:
        permissions = [
            ('can_view_chat_list', 'Can view chat list')
        ]


class Message(models.Model):
    text = models.TextField(max_length=500, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default="deleted user")
    published_time = models.DateField(auto_now_add=True)
    chat_id = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)

    def can_edit_or_delete_message(self, user):
        if self.author:
            return self.author == user and (timezone.now().date() - self.published_time).days < 1
        return True


