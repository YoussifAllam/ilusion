# Generated by Django 5.0.2 on 2024-06-19 19:26

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_alter_productsize_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsize',
            name='product_size_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]