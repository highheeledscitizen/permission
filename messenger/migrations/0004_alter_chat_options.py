# Generated by Django 5.0.6 on 2024-05-29 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0003_alter_chat_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chat',
            options={'permissions': [('can_view_chat_list', 'Can view chat list')]},
        ),
    ]
