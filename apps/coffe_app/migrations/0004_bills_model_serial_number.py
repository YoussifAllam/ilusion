# Generated by Django 5.0.2 on 2024-08-19 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffe_app', '0003_alter_user_model_email_alter_user_model_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='bills_model',
            name='serial_number',
            field=models.CharField(default=1, max_length=100, unique=True, verbose_name='Bill Serial'),
            preserve_default=False,
        ),
    ]
