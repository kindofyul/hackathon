# Generated by Django 4.2.1 on 2023-08-12 05:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0015_posting_writer'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='posting',
            name='remaining_count',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
