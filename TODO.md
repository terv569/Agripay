# TODO: Add Payment Feature with Daraja API

- [ ] Update requirements.txt to include daraja-python library
- [ ] Create payments app using Django's startapp command
- [ ] Add 'payments' to INSTALLED_APPS in agripay/settings.py
- [ ] Add Daraja API credentials placeholders in agripay/settings.py (consumer key, secret, shortcode, etc.)
- [ ] Create Payment model in payments/models.py
- [ ] Implement payment views in payments/views.py (initiate STK push, handle callback)
- [ ] Create URLs for payments app in payments/urls.py
- [ ] Include payments URLs in agripay/urls.py
- [ ] Update marketplace/cart.html template to add checkout button
- [ ] Run database migrations for new Payment model
- [ ] Test the payment integration in sandbox mode
