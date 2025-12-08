import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File


class Command(BaseCommand):
    help = 'Assign specific image files to matching usernames (overwrites existing images)'

    def handle(self, *args, **options):
        from django.contrib.auth import get_user_model
        from farmers.models import FarmerProfile

        User = get_user_model()
        img_dir = os.path.join(settings.MEDIA_ROOT, 'farmer_images')
        if not os.path.isdir(img_dir):
            self.stdout.write(self.style.ERROR(f'Image dir not found: {img_dir}'))
            return

        mapping = {
            'farmer1.jpg': 'farmer1',
            'farmer2.jpg': 'farmer2',
        }

        for fname, username in mapping.items():
            path = os.path.join(img_dir, fname)
            if not os.path.exists(path):
                self.stdout.write(self.style.WARNING(f'File not found: {path}'))
                continue

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'User not found: {username}'))
                continue

            fp, _ = FarmerProfile.objects.get_or_create(user=user)
            # delete existing
            try:
                if fp.image:
                    fp.image.delete(save=False)
            except Exception:
                pass

            try:
                with open(path, 'rb') as fh:
                    fp.image.save(fname, File(fh), save=True)
                self.stdout.write(self.style.SUCCESS(f'Assigned {fname} to {username}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to assign {fname} to {username}: {e}'))

        self.stdout.write(self.style.SUCCESS('Done specific assignments.'))
