# Generated by Django 5.0.2 on 2024-06-19 20:13

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart_items',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
