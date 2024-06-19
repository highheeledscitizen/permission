from django.contrib import admin
from .models import Chat, Message, LogEntry, UserStatus


admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(LogEntry)
admin.site.register(UserStatus)
