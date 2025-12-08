import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings

def download_bytes(url):
    try:
        # Use urllib to avoid extra dependency
        from urllib.request import urlopen
        with urlopen(url) as r:
            return r.read()
    except Exception as e:
        return None


class Command(BaseCommand):
    help = 'Download and assign sample images to farmer profiles (farmer1, farmer2)'

    def handle(self, *args, **options):
        from django.contrib.auth import get_user_model
        from farmers.models import FarmerProfile

        User = get_user_model()

        mapping = {
            # use a simple stable placeholder for farmer1
            'farmer1': 'https://picsum.photos/seed/farmer1/960/640',
            'farmer2': 'https://images.unsplash.com/photo-1501004318641-b39e6451bec6?q=80&w=960&auto=format&fit=crop&ixlib=rb-4.0.3&s=8f1f9b6b6a0e6a3f6d7d8c5f1b2a4b3c',
        }

        for username, url in mapping.items():
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'User {username} not found, skipping'))
                continue

            fp, created = FarmerProfile.objects.get_or_create(user=user)
            if fp.image:
                self.stdout.write(self.style.NOTICE(f'FarmerProfile for {username} already has an image, skipping'))
                continue

            data = download_bytes(url)
            if not data:
                self.stdout.write(self.style.ERROR(f'Failed to download image for {username} from {url}'))
                continue

            filename = f'{username}.jpg'
            fp.image.save(filename, ContentFile(data), save=True)
            self.stdout.write(self.style.SUCCESS(f'Assigned image for {username} -> {fp.image.url}'))

        self.stdout.write(self.style.SUCCESS('Done assigning images.'))
