from django.shortcuts import render, redirect, get_object_or_404
from .models import Chat, Message
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

User = get_user_model()


def is_superuser(user):
    return user.is_superuser


def home(request):
    return render(request, 'home.html')


@login_required()
@permission_required('messenger.can_view_chat_list')
def chat_list(request):
    chat = Chat.objects.all()
    return render(request, 'chat_list.html', {'chat_list': chat})


@login_required()
@permission_required('messenger.can_view_chat_list')
def chat_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user not in chat.members.all():
        return redirect(access_required_page)

    if request.method == 'POST':
        text = request.POST.get('text')
        new_message = Message(text=text,
                              author=request.user,
                              chat_id=chat)
        new_message.save()

        return redirect('chat_view', chat_id)
    messages = Message.objects.filter(chat_id=chat_id)
    users = chat.members.all()
    return render(request, 'chat_view.html', {'messages': messages,
                                                                  'users': users,
                                                                  'current_user': request.user,
                                                                  'chat': chat})


@user_passes_test(is_superuser)
def chat_create(request):
    if request.method == 'POST':
        chat_name = request.POST.get('chat_name')
        users_select = request.POST.getlist('users_select')

        selected_users = User.objects.filter(id__in=users_select)

        content_type = ContentType.objects.get_for_model(Chat)
        permission = Permission.objects.get(
            codename="can_view_chat_list",
            content_type=content_type,
        )
        for user in selected_users:
            user.user_permissions.add(permission)

        new_chat = Chat.objects.create(chat_name=chat_name)
        new_chat.members.set(selected_users)
        new_chat.save()
        return redirect('chat_list')

    users = User.objects.all()
    return render(request, "chat_create.html", {'members': users})


@login_required()
def message_delete(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.can_edit_or_delete_message(request.user):
        chat_id = str(message.chat_id.id)
        message.delete()
        return redirect('/chat/' + chat_id)
    else:
        return redirect('/chat/' + str(message.chat_id.id))


@login_required()
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.can_edit_or_delete_message(request.user):
        if request.method == 'POST':
            chat_id = str(message.chat_id.id)
            message.text = request.POST.get('text')
            message.save()
            return redirect('/chat/' + chat_id)
        return render(request, "edit_message.html", {'message': message})
    else:
        return redirect('/chat/' + str(message.chat_id.id))


def access_required_page(request):
    return render(request, "system/access_required.html")
