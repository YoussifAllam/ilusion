
from django.forms import ModelForm
from .models import ProductImages, Products
from django.forms import inlineformset_factory

class ProductImagesForm(ModelForm):
    class Meta:
        model = ProductImages
        fields = ['ProductImage']

ProductImagesFormSet = inlineformset_factory(Products, ProductImages, form=ProductImagesForm, extra=3)