import os
from django.core.management.base import BaseCommand
from django.conf import settings

def download_bytes(url):
    try:
        from urllib.request import urlopen
        with urlopen(url) as r:
            return r.read()
    except Exception:
        return None


class Command(BaseCommand):
    help = 'Download close-up farmer photos from Unsplash Source into media/farmer_images/stock_farmer_{i}.jpg'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=6, help='Number of images to download')

    def handle(self, *args, **options):
        count = options.get('count', 6)
        out_dir = os.path.join(settings.MEDIA_ROOT, 'farmer_images')
        os.makedirs(out_dir, exist_ok=True)

        for i in range(1, count + 1):
            # Use Unsplash Source to fetch a farmer portrait; add sig to vary results
            url = f'https://source.unsplash.com/1200x800/?farmer,portrait&sig={i}'
            data = download_bytes(url)
            if not data:
                self.stdout.write(self.style.ERROR(f'Failed to download image {i} from {url}'))
                continue
            filename = f'stock_farmer_{i}.jpg'
            path = os.path.join(out_dir, filename)
            with open(path, 'wb') as f:
                f.write(data)
            self.stdout.write(self.style.SUCCESS(f'Downloaded {filename}'))

        self.stdout.write(self.style.SUCCESS(f'Download complete: {count} images (in {out_dir})'))
