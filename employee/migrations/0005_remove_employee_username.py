# Generated by Django 2.0.7 on 2019-04-21 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_auto_20190422_0102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='username',
        ),
    ]
