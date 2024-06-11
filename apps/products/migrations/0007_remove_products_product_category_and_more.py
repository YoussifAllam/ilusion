# Generated by Django 5.0.2 on 2024-06-09 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_home_ourproducts_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='Product_category',
        ),
        migrations.AddField(
            model_name='products',
            name='Product_category',
            field=models.ManyToManyField(to='products.category', verbose_name='Product Category'),
        ),
    ]
