# Generated by Django 3.2.9 on 2023-11-20 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20231120_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='auth_token',
            field=models.TextField(null=True),
        ),
    ]
