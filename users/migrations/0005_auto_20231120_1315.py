# Generated by Django 3.2.9 on 2023-11-20 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20231120_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='auth_token',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='refresh_token',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
