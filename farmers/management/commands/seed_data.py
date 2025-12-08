from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Seed sample users, farmer profiles and products'

    def handle(self, *args, **options):
        User = get_user_model()
        from farmers.models import FarmerProfile, Product

        sample = [
            {
                'username': 'farmer1',
                'email': 'farmer1@example.com',
                'password': 'password123',
                'farm_name': 'Green Acres',
                'products': [
                    {'name': 'Maize', 'description': 'Sweet yellow maize', 'price': '50.00', 'quantity': 100},
                    {'name': 'Beans', 'description': 'Red kidney beans', 'price': '120.00', 'quantity': 50},
                ],
            },
            {
                'username': 'farmer2',
                'email': 'farmer2@example.com',
                'password': 'password123',
                'farm_name': 'Sunny Fields',
                'products': [
                    {'name': 'Tomatoes', 'description': 'Ripe tomatoes', 'price': '80.00', 'quantity': 200},
                    {'name': 'Onions', 'description': 'Red onions', 'price': '60.00', 'quantity': 150},
                ],
            },
            {
                'username': 'buyer1',
                'email': 'buyer1@example.com',
                'password': 'password123',
                'farm_name': None,
                'products': [],
            },
        ]

        for entry in sample:
            user, created = User.objects.get_or_create(username=entry['username'], defaults={'email': entry.get('email', '')})
            if created:
                user.set_password(entry['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user {user.username}"))
            else:
                self.stdout.write(self.style.WARNING(f"User {user.username} already exists"))

            if entry.get('farm_name'):
                fp, fp_created = FarmerProfile.objects.get_or_create(user=user, defaults={'farm_name': entry['farm_name']})
                if not fp_created and fp.farm_name != entry['farm_name']:
                    fp.farm_name = entry['farm_name']
                    fp.save()
                    self.stdout.write(self.style.SUCCESS(f"Updated farm name for {user.username}"))

                for p in entry.get('products', []):
                    product, p_created = Product.objects.get_or_create(farmer=fp, name=p['name'], defaults={
                        'description': p.get('description', ''),
                        'price': p.get('price', '0.00'),
                        'quantity': p.get('quantity', 0),
                    })
                    if p_created:
                        self.stdout.write(self.style.SUCCESS(f"  Added product {product.name} for {user.username}"))
                    else:
                        # update existing
                        product.description = p.get('description', product.description)
                        product.price = p.get('price', product.price)
                        product.quantity = p.get('quantity', product.quantity)
                        product.save()
                        self.stdout.write(self.style.NOTICE(f"  Updated product {product.name} for {user.username}"))

        self.stdout.write(self.style.SUCCESS('Seeding complete.'))
