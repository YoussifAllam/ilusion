# Generated by Django 5.0.2 on 2024-06-18 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_remove_products_uploadd_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product_rating',
            options={'ordering': ['-uploaded_at'], 'verbose_name': 'Products Ratings', 'verbose_name_plural': 'Products Ratings'},
        ),
    ]
