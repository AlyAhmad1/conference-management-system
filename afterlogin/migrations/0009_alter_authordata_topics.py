# Generated by Django 3.2 on 2021-05-06 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afterlogin', '0008_authordata_topics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authordata',
            name='topics',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]