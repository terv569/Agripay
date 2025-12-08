import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File


class Command(BaseCommand):
    help = 'Assign images in media/farmer_images/ to FarmerProfile by matching filename to username (e.g. farmer1.jpg -> user farmer1)'

    def add_arguments(self, parser):
        parser.add_argument('--overwrite', action='store_true', help='Overwrite existing FarmerProfile images')

    def handle(self, *args, **options):
        from django.contrib.auth import get_user_model
        from farmers.models import FarmerProfile

        User = get_user_model()
        img_dir = os.path.join(settings.MEDIA_ROOT, 'farmer_images')
        if not os.path.isdir(img_dir):
            self.stdout.write(self.style.ERROR(f'Image dir not found: {img_dir}'))
            return

        files = [f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f))]
        if not files:
            self.stdout.write(self.style.ERROR(f'No files in {img_dir}'))
            return

        assigned = 0
        overwrite = options.get('overwrite')
        for fname in files:
            name, ext = os.path.splitext(fname)
            username = name
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'No user matching filename: {fname}'))
                continue

            fp, _ = FarmerProfile.objects.get_or_create(user=user)
            if fp.image and not overwrite:
                self.stdout.write(self.style.NOTICE(f'Profile for {username} already has image, skipping'))
                continue
            if fp.image and overwrite:
                # remove existing image file if present
                try:
                    fp.image.delete(save=False)
                except Exception:
                    pass

            path = os.path.join(img_dir, fname)
            try:
                with open(path, 'rb') as fh:
                    fp.image.save(fname, File(fh), save=True)
                assigned += 1
                self.stdout.write(self.style.SUCCESS(f'Assigned {fname} to {username}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to assign {fname} to {username}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Done. Images assigned: {assigned}'))
