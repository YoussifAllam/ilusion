# Generated by Django 5.0.2 on 2024-06-17 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_products_uploadd_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='uploadd_at',
        ),
    ]