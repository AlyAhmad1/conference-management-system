# Generated by Django 3.2 on 2021-05-06 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('afterlogin', '0005_remove_conferencedata_your_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authordata',
            name='paper_name',
        ),
        migrations.RemoveField(
            model_name='authordata',
            name='topics',
        ),
    ]