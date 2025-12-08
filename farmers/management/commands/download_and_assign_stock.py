import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File

def download_bytes(url):
    try:
        from urllib.request import urlopen
        with urlopen(url) as r:
            return r.read()
    except Exception:
        return None


class Command(BaseCommand):
    help = 'Download stock farmer close-ups from picsum.photos and assign to all FarmerProfile images (overwrite)'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=6, help='Number of stock images to download')

    def handle(self, *args, **options):
        count = options.get('count', 6)
        out_dir = os.path.join(settings.MEDIA_ROOT, 'farmer_images')
        os.makedirs(out_dir, exist_ok=True)

        # Download images
        downloaded = []
        for i in range(1, count + 1):
            url = f'https://picsum.photos/seed/farmerstock{i}/1200/800'
            data = download_bytes(url)
            if not data:
                self.stdout.write(self.style.ERROR(f'Failed to download image {i} from {url}'))
                continue
            filename = f'stock_farmer_{i}.jpg'
            path = os.path.join(out_dir, filename)
            with open(path, 'wb') as f:
                f.write(data)
            downloaded.append(path)
            self.stdout.write(self.style.SUCCESS(f'Downloaded {filename}'))

        if not downloaded:
            self.stdout.write(self.style.ERROR('No images downloaded; aborting assignment'))
            return

        # Assign to all FarmerProfile objects (overwrite existing images)
        from farmers.models import FarmerProfile
        profiles = list(FarmerProfile.objects.select_related('user').all())
        if not profiles:
            self.stdout.write(self.style.WARNING('No FarmerProfile objects found.'))
            return

        idx = 0
        for fp in profiles:
            try:
                # remove existing image
                if fp.image:
                    try:
                        fp.image.delete(save=False)
                    except Exception:
                        pass
                src = downloaded[idx % len(downloaded)]
                with open(src, 'rb') as fh:
                    fp.image.save(os.path.basename(src), File(fh), save=True)
                self.stdout.write(self.style.SUCCESS(f'Assigned {os.path.basename(src)} to {fp.user.username}'))
                idx += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to assign image to {fp.user.username}: {e}'))

        self.stdout.write(self.style.SUCCESS('Stock download and assignment complete.'))
