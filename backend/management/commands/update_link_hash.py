from django.core.management.base import BaseCommand
from hashlib import sha256
from backend.models import Products

class Command(BaseCommand):
    help = "Update link_hash for existing products"

    def handle(self, *args, **kwargs):
        products = Products.objects.filter(link_hash__isnull=True)
        count = products.count()

        self.stdout.write(f"Found {count} products to update...")

        for product in products:
            product.link_hash = sha256(product.link.encode('utf-8')).hexdigest()
            product.save()

        self.stdout.write("Update completed!")

