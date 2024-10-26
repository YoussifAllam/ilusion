# Generated by Django 5.0.2 on 2024-08-19 13:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffe_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Qr_Code_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_image', models.ImageField(blank=True, null=True, upload_to='Qr_images', verbose_name='Qr Image')),
                ('user_fk', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='User_Qr_Code_Set', to='coffe_app.user_model', verbose_name='User Qr Code')),
            ],
        ),
    ]