# Generated by Django 5.1.5 on 2025-02-07 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_app', '0002_alter_event_data_which_sig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event_data',
            name='associate_partner',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
