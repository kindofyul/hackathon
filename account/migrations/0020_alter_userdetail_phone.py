# Generated by Django 4.2.4 on 2023-08-04 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_alter_userdetail_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='phone',
            field=models.TextField(),
        ),
    ]
