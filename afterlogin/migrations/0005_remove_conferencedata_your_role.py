# Generated by Django 3.2 on 2021-05-06 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('afterlogin', '0004_reviews_suggest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conferencedata',
            name='Your_role',
        ),
    ]
