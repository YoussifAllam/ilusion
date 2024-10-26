# Generated by Django 5.0.2 on 2024-10-26 16:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ClubMembers",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "pdf",
                    models.FileField(
                        blank=True,
                        help_text="if the file is in pdf format, upload it here",
                        null=True,
                        upload_to="pdfs/",
                        verbose_name="File as pdf",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="if the file is in image format, upload it here",
                        null=True,
                        upload_to="Menu_images/",
                        verbose_name="File as image",
                    ),
                ),
            ],
            options={
                "verbose_name": "Club Members",
                "verbose_name_plural": "Club Members",
            },
        ),
        migrations.CreateModel(
            name="Complains",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "cutomer_name",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Customer Name",
                    ),
                ),
                (
                    "cutomer_email",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Customer email",
                    ),
                ),
                (
                    "cutomer_complain",
                    models.TextField(verbose_name="Customer complain"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DailyPromo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "pdf",
                    models.FileField(
                        blank=True,
                        help_text="if the WeeklyEvents is in pdf format, upload it here",
                        null=True,
                        upload_to="pdfs/",
                        verbose_name="Daily Promo as pdf",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="if the daily promo is in image format, upload it here",
                        null=True,
                        upload_to="Menu_images/",
                        verbose_name="Daily Promo as image",
                    ),
                ),
            ],
            options={
                "verbose_name": "Daily Promo",
                "verbose_name_plural": "Daily Promo",
            },
        ),
        migrations.CreateModel(
            name="DrinkMenu",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "pdf",
                    models.FileField(
                        blank=True,
                        help_text="if the menu is in pdf format, upload it here",
                        null=True,
                        upload_to="pdfs/",
                        verbose_name="Menu as PDF",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="if the menu is in image format, upload it here",
                        null=True,
                        upload_to="Menu_images/",
                        verbose_name="Menu as image",
                    ),
                ),
            ],
            options={
                "verbose_name": "Drink Menus",
                "verbose_name_plural": "Drink Menus",
            },
        ),
        migrations.CreateModel(
            name="FoodMenu",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "pdf",
                    models.FileField(
                        blank=True,
                        help_text="if the menu is in pdf format, upload it here",
                        null=True,
                        upload_to="pdfs/",
                        verbose_name="Menu as PDF",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="if the menu is in image format, upload it here",
                        null=True,
                        upload_to="Menu_images/",
                        verbose_name="Menu as image",
                    ),
                ),
            ],
            options={
                "verbose_name": "Food Menus",
                "verbose_name_plural": "Food Menus",
            },
        ),
        migrations.CreateModel(
            name="LoyaltyProgram",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "pdf",
                    models.FileField(
                        blank=True,
                        help_text="if the file is in pdf format, upload it here",
                        null=True,
                        upload_to="pdfs/",
                        verbose_name="File as pdf",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="if the file is in image format, upload it here",
                        null=True,
                        upload_to="Menu_images/",
                        verbose_name="File as image",
                    ),
                ),
            ],
            options={
                "verbose_name": "Loyalty Program",
                "verbose_name_plural": "Loyalty Program",
            },
        ),
        migrations.CreateModel(
            name="Rates",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "cutomer_name",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Customer Name",
                    ),
                ),
                ("cutomer_rate", models.TextField(verbose_name="Customer rate")),
                (
                    "cutomer_email",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Customer email",
                    ),
                ),
                (
                    "stars",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MaxValueValidator(5),
                            django.core.validators.MinValueValidator(1),
                        ],
                        verbose_name="Rate stars",
                    ),
                ),
            ],
            options={
                "verbose_name": "Rates",
                "verbose_name_plural": "Rates",
            },
        ),
        migrations.CreateModel(
            name="WeeklyEvents",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "pdf",
                    models.FileField(
                        blank=True,
                        help_text="if the Weekly Event is in pdf format, upload it here",
                        null=True,
                        upload_to="pdfs/",
                        verbose_name="Weekly Event as pdf",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="if the Weekly Event is in image format, upload it here",
                        null=True,
                        upload_to="Menu_images/",
                        verbose_name="Weekly Event as image",
                    ),
                ),
            ],
            options={
                "verbose_name": "Weekly Events",
                "verbose_name_plural": "Weekly Events",
            },
        ),
    ]
