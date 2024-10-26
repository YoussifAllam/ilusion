# Generated by Django 5.0.2 on 2024-07-11 11:45

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0021_alter_productsize_product_size_uuid'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('total_price', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
                ('product_size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productsize')),
            ],
        ),
    ]