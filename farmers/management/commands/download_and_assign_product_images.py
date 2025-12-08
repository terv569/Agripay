from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils.text import slugify
from farmers.models import Product
import requests
import os

class Command(BaseCommand):
    help = 'Download product images (picsum seed by product name) and assign to products'

    def add_arguments(self, parser):
        parser.add_argument('--overwrite', action='store_true', help='Overwrite existing images')
        parser.add_argument('--width', type=int, default=800, help='Image width')
        parser.add_argument('--height', type=int, default=600, help='Image height')

    def handle(self, *args, **options):
        overwrite = options['overwrite']
        width = options['width']
        height = options['height']

        products = Product.objects.all()
        if not products.exists():
            self.stdout.write(self.style.WARNING('No products found.'))
            return

        media_dir = os.path.join('media', 'product_images')
        os.makedirs(media_dir, exist_ok=True)

        for p in products:
            seed = slugify(p.name) or 'product'
            filename = f"product_{seed}.jpg"
            filepath = os.path.join(media_dir, filename)

            if p.image and not overwrite:
                self.stdout.write(f"Skipping {p.name} (already has image). Use --overwrite to replace.")
                continue

            url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
            try:
                r = requests.get(url, timeout=15)
                r.raise_for_status()
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to download image for {p.name}: {e}"))
                continue

            # Save to product.image via Django File API
            try:
                content = ContentFile(r.content)
                p.image.save(filename, content, save=True)
                self.stdout.write(self.style.SUCCESS(f"Assigned image to product '{p.name}' -> {p.image.name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to save image for {p.name}: {e}"))

        self.stdout.write(self.style.SUCCESS('Product image assignment complete.'))
