# Generated by Django 5.0.2 on 2024-08-19 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffe_app', '0007_remove_user_model_monthly_bills_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bills_model',
            name='serial_number',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Bill Serial number'),
        ),
    ]
