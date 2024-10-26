from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Popup(models.Model):
    content = models.TextField(verbose_name='Popup Message')
    discount = models.IntegerField(
        verbose_name='discount Percentage value',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='discount Percentage value should be between 0 and 100'
    )
    is_active = models.BooleanField(verbose_name='is active', default=True)

    def delete(self, *args, **kwargs):
        raise ValidationError("Deletion of this object is not allowed.")

    @staticmethod
    def can_create_popup():
        return not Popup.objects.exists()

    def save(self, *args, **kwargs):
        if not self.pk and not Popup.can_create_popup():
            raise ValidationError("Cannot create more than one Popup instance.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.content
