# Generated by Django 5.0.2 on 2024-06-09 13:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_products_sku_alter_productimages_productimage_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='Category_image',
        ),
        migrations.AlterField(
            model_name='products',
            name='SKU',
            field=models.CharField(blank=True, default='N/A', max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='Home_OurProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('Category_image', models.ImageField(blank=True, null=True, upload_to='category_images/', verbose_name='Category image')),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category', unique=True, verbose_name='Category')),
            ],
        ),
    ]