# Generated by Django 5.1 on 2024-08-29 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_forgetpassword'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forgetpassword',
            name='email',
        ),
        migrations.AddField(
            model_name='forgetpassword',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
