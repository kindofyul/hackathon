# Generated by Django 4.2.4 on 2023-08-04 04:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_userdetail_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetail',
            name='user',
        ),
    ]
