import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agripay.settings')
django.setup()
from django.test import Client

c = Client()
# login as buyer1
logged_in = c.login(username='buyer1', password='password123')
print('login success:', logged_in)
# confirm user state via a protected view or context
resp = c.get('/')
print('home status code after login:', resp.status_code)
# perform logout
resp2 = c.get('/accounts/logout/')
print('logout status code:', resp2.status_code)
# After logout, access home again
resp3 = c.get('/')
print('home status code after logout:', resp3.status_code)
# Check session for _auth_user_id
print('_auth_user_id in session after logout:', c.session.get('_auth_user_id'))
# Print redirect location if any
print('logout redirect location header:', resp2.headers.get('Location'))
