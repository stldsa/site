# Generated by Django 3.2.6 on 2021-08-27 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_homepage_action_network_embed_api_endpoint'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='body',
        ),
        migrations.AddField(
            model_name='homepage',
            name='mission_statement',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='values_statement',
            field=models.TextField(null=True),
        ),
    ]
