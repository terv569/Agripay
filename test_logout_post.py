import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agripay.settings')
django.setup()
from django.test import Client

c = Client()
# login as buyer1
logged_in = c.login(username='buyer1', password='password123')
print('login success:', logged_in)
# perform logout via POST
resp = c.post('/accounts/logout/')
print('logout status code:', resp.status_code)
print('logout redirected to:', resp.headers.get('Location'))
# Check session for _auth_user_id
print('_auth_user_id in session after logout:', c.session.get('_auth_user_id'))
