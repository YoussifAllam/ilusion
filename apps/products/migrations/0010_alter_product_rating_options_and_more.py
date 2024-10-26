# Generated by Django 5.0.2 on 2024-06-09 14:06

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_product_rating'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product_rating',
            options={'verbose_name': 'Ratings', 'verbose_name_plural': 'Ratings'},
        ),
        migrations.AddField(
            model_name='product_rating',
            name='rate_content',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product_rating',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
