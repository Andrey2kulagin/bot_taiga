# Generated by Django 3.2.9 on 2023-12-10 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_alter_botuser_tg_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BotUser',
        ),
    ]