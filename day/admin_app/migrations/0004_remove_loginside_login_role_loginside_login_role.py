# Generated by Django 5.1.5 on 2025-02-06 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0003_login_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loginside',
            name='login_role',
        ),
        migrations.AddField(
            model_name='loginside',
            name='login_role',
            field=models.ManyToManyField(to='admin_app.login_role'),
        ),
    ]
