# Generated by Django 5.1.5 on 2025-02-18 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0002_alter_login_role_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login_role',
            name='name',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Manager', 'Manager'), ('Masoom', 'Masoom'), ('Road Safety', 'Road Safety'), ('Health', 'Health'), ('Sports', 'Sports'), ('Accessibility', 'Accessibility'), ('Learning(YI Talks)', 'Learning(YI Talks)'), ('Climate action', 'Climate action'), ('Climate action', 'Climate action'), ('Innovation', 'Innovation'), ('Entrepreneurship', 'Entrepreneurship'), ('Branding & PR', 'Branding & PR'), ('Women Engagement (YIWE)', 'Women Engagement (YIWE)'), ('Culture Connect', 'Culture Connect'), ('Yi Angel', 'Yi Angel'), ('Special Interest Group (S.I.G)', 'Special Interest Group (S.I.G)')], max_length=200, primary_key=True, serialize=False),
        ),
    ]
