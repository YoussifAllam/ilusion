import uuid
from django.core.management.base import BaseCommand
from apps.products.models import ProductSize

class Command(BaseCommand):
    help = 'Assign unique UUIDs to ProductSize instances'

    def handle(self, *args, **kwargs):
        productsizes = ProductSize.objects.all()
        for ps in productsizes:
            ps.product_size_uuid = uuid.uuid4()
            ps.save()
            self.stdout.write(self.style.SUCCESS(f'Updated ProductSize id={ps.id} with UUID={ps.product_size_uuid}'))
        self.stdout.write(self.style.SUCCESS('Successfully assigned unique UUIDs to all ProductSize instances.'))
