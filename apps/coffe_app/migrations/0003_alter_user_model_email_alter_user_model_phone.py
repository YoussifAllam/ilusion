# Generated by Django 5.0.2 on 2024-08-19 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffe_app', '0002_user_qr_code_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_model',
            name='email',
            field=models.EmailField(max_length=100, unique=True, verbose_name='User Email'),
        ),
        migrations.AlterField(
            model_name='user_model',
            name='phone',
            field=models.CharField(max_length=100, unique=True, verbose_name='User Phone Number'),
        ),
    ]