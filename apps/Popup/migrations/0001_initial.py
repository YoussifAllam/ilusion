# Generated by Django 5.0.2 on 2024-06-14 09:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Popup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Popup Message')),
                ('discount', models.IntegerField(help_text='discount Percentage value should be between 0 and 100', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='discount Percentage value')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
            ],
        ),
    ]