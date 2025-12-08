import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File


class Command(BaseCommand):
    help = 'Assign downloaded stock images (media/farmer_images/stock_farmer_*.jpg) to FarmerProfile objects missing an image.'

    def handle(self, *args, **options):
        from farmers.models import FarmerProfile

        out_dir = os.path.join(settings.MEDIA_ROOT, 'farmer_images')
        if not os.path.isdir(out_dir):
            self.stdout.write(self.style.ERROR(f'No directory: {out_dir}'))
            return

        # collect stock images
        files = sorted([f for f in os.listdir(out_dir) if f.startswith('stock_farmer_')])
        if not files:
            self.stdout.write(self.style.ERROR('No stock images found (stock_farmer_*.jpg)'))
            return

        profiles = FarmerProfile.objects.filter(image__isnull=True)
        if not profiles.exists():
            self.stdout.write(self.style.NOTICE('No FarmerProfile without image found.'))
            return

        idx = 0
        for fp in profiles:
            src = os.path.join(out_dir, files[idx % len(files)])
            with open(src, 'rb') as fh:
                fp.image.save(os.path.basename(src), File(fh), save=True)
            self.stdout.write(self.style.SUCCESS(f'Assigned {os.path.basename(src)} to {fp.user.username}'))
            idx += 1

        self.stdout.write(self.style.SUCCESS('Stock image assignment complete.'))
