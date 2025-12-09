import requests
import base64
from datetime import datetime

# Your credentials
CONSUMER_KEY = 'yv5rFJCoqXFUX3qsG5hxyjml4Ko39AzLHRhwtzfb5fJrQq4k'
CONSUMER_SECRET = 'V9fJFGcGTbiRnXRCsMoujkbqIQyo9bBPlY0tmTIIUjdi6PxrAFXwr5PozjVTjsF9'
SHORTCODE = '174379'
PASSKEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

print("Testing M-Pesa Integration...")
print("-" * 50)

# Step 1: Get Access Token
print("\n1. Getting Access Token...")
url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")

if response.status_code == 200:
    access_token = response.json().get('access_token')
    print(f"[OK] Access Token: {access_token[:20]}...")
    
    # Step 2: Test STK Push
    print("\n2. Testing STK Push...")
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode((SHORTCODE + PASSKEY + timestamp).encode()).decode()
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'BusinessShortCode': SHORTCODE,
        'Password': password,
        'Timestamp': timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': 1,
        'PartyA': '254708374149',
        'PartyB': SHORTCODE,
        'PhoneNumber': '254708374149',
        'CallBackURL': 'https://mydomain.com/callback',
        'AccountReference': 'Test123',
        'TransactionDesc': 'Test Payment'
    }
    
    stk_response = requests.post(
        'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
        json=payload,
        headers=headers
    )
    
    print(f"Status Code: {stk_response.status_code}")
    print(f"Response: {stk_response.json()}")
    
    result = stk_response.json()
    if result.get('ResponseCode') == '0':
        print("\n[OK] SUCCESS! STK Push initiated")
    else:
        print(f"\n[FAIL] FAILED: {result.get('errorMessage') or result.get('ResponseDescription')}")
else:
    print("[FAIL] Failed to get access token")
