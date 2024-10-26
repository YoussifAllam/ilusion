from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class DrinkMenu(models.Model):
    pdf = models.FileField(
        upload_to='pdfs/',
        help_text='if the menu is in pdf format, upload it here',
        verbose_name='Menu as PDF',
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to='Menu_images/',
        help_text='if the menu is in image format, upload it here',
        verbose_name='Menu as image',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Drink Menus'
        verbose_name_plural = 'Drink Menus'

    def __str__(self):
        return f'{self.id}'


class FoodMenu(models.Model):
    pdf = models.FileField(
        upload_to='pdfs/',
        help_text='if the menu is in pdf format, upload it here',
        verbose_name='Menu as PDF',
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to='Menu_images/',
        help_text='if the menu is in image format, upload it here',
        verbose_name='Menu as image',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Food Menus'
        verbose_name_plural = 'Food Menus'


class DailyPromo(models.Model):
    pdf = models.FileField(
        upload_to='pdfs/',
        help_text='if the WeeklyEvents is in pdf format, upload it here',
        verbose_name='Daily Promo as pdf',
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to='Menu_images/',
        help_text='if the daily promo is in image format, upload it here',
        verbose_name='Daily Promo as image',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Daily Promo'
        verbose_name_plural = 'Daily Promo'


class WeeklyEvents(models.Model):
    pdf = models.FileField(
        upload_to='pdfs/',
        help_text='if the Weekly Event is in pdf format, upload it here',
        verbose_name='Weekly Event as pdf',
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to='Menu_images/',
        help_text='if the Weekly Event is in image format, upload it here',
        verbose_name='Weekly Event as image',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Weekly Events'
        verbose_name_plural = 'Weekly Events'


class ClubMembers(models.Model):
    pdf = models.FileField(
        upload_to='pdfs/',
        help_text='if the file is in pdf format, upload it here',
        verbose_name='File as pdf',
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to='Menu_images/',
        help_text='if the file is in image format, upload it here',
        verbose_name='File as image',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Club Members'
        verbose_name_plural = 'Club Members'


class LoyaltyProgram(models.Model):
    pdf = models.FileField(
        upload_to='pdfs/',
        help_text='if the file is in pdf format, upload it here',
        verbose_name='File as pdf',
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to='Menu_images/',
        help_text='if the file is in image format, upload it here',
        verbose_name='File as image',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Loyalty Program'
        verbose_name_plural = 'Loyalty Program'


class Complains(models.Model):
    cutomer_name = models.CharField(
        max_length=100,
        verbose_name='Customer Name',
        null=True,
        blank=True
    )
    cutomer_email = models.CharField(
        max_length=100,
        verbose_name='Customer email',
        null=True,
        blank=True
    )
    cutomer_complain = models.TextField(
        verbose_name='Customer complain'
    )

    def save(self, *args, **kwargs):
        if self.cutomer_name is None:
            self.cutomer_name = 'Anonymous'
        if self.cutomer_email is None:
            self.cutomer_email = 'Anonymous'
        super().save(*args, **kwargs)


class Rates(models.Model):
    cutomer_name = models.CharField(
        max_length=100,
        verbose_name='Customer Name',
        null=True,
        blank=True
    )
    cutomer_rate = models.TextField(
        verbose_name='Customer rate'
    )
    cutomer_email = models.CharField(
        max_length=100,
        verbose_name='Customer email',
        null=True,
        blank=True
    )
    stars = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)],
        verbose_name='Rate stars',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Rates'
        verbose_name_plural = 'Rates'

    def save(self, *args, **kwargs):
        if self.cutomer_name is None:
            self.cutomer_name = 'Anonymous'
        if self.cutomer_email is None:
            self.cutomer_email = 'Anonymous'
        if self.stars is None:
            self.stars = 5
        super().save(*args, **kwargs)
