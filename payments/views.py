from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Payment
import json
import requests
import base64
from datetime import datetime

def get_access_token():
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(url, auth=(settings.DARAJA_CONSUMER_KEY, settings.DARAJA_CONSUMER_SECRET))
    response_data = response.json()
    if 'access_token' not in response_data:
        raise Exception(f"Failed to get access token: {response_data}")
    return response_data.get('access_token')

@login_required
def initiate_payment(request):
    from django.contrib import messages
    if request.method == 'POST':
        amount = request.POST.get('amount')
        phone_number = request.POST.get('phone_number')
        if not amount or not phone_number:
            messages.error(request, 'Amount and phone number are required')
            return redirect('marketplace:cart')

        payment = Payment.objects.create(
            user=request.user,
            amount=amount,
            phone_number=phone_number
        )

        try:
            access_token = get_access_token()
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = base64.b64encode((settings.DARAJA_SHORTCODE + settings.DARAJA_PASSKEY + timestamp).encode()).decode()
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            payload = {
                'BusinessShortCode': settings.DARAJA_SHORTCODE,
                'Password': password,
                'Timestamp': timestamp,
                'TransactionType': 'CustomerPayBillOnline',
                'Amount': int(float(amount)),
                'PartyA': phone_number,
                'PartyB': settings.DARAJA_SHORTCODE,
                'PhoneNumber': phone_number,
                'CallBackURL': 'https://mydomain.com/payments/callback/',
                'AccountReference': f'AgriPay{payment.id}',
                'TransactionDesc': 'AgriPay Purchase'
            }
            
            response = requests.post('https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', json=payload, headers=headers)
            result = response.json()
            
            print(f"M-Pesa Response: {result}")  # Debug

            if result.get('ResponseCode') == '0':
                payment.transaction_id = result.get('CheckoutRequestID')
                payment.save()
                messages.success(request, 'Payment initiated! Check your phone for M-Pesa prompt.')
                return redirect('marketplace:cart')
            else:
                payment.status = 'failed'
                payment.save()
                error_msg = result.get('errorMessage') or result.get('ResponseDescription') or 'Unknown error'
                messages.error(request, f"Payment failed: {error_msg}")
                print(f"Payment Error: {result}")  # Debug
                return redirect('marketplace:cart')
        except Exception as e:
            payment.status = 'failed'
            payment.save()
            messages.error(request, f'Error: {str(e)}')
            print(f"Exception: {str(e)}")  # Debug
            return redirect('marketplace:cart')

    return redirect('marketplace:cart')

@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        stk_callback = data.get('Body', {}).get('stkCallback', {})

        checkout_request_id = stk_callback.get('CheckoutRequestID')
        result_code = stk_callback.get('ResultCode')
        result_desc = stk_callback.get('ResultDesc')

        try:
            payment = Payment.objects.get(transaction_id=checkout_request_id)
            if result_code == 0:
                payment.status = 'completed'
            else:
                payment.status = 'failed'
            payment.save()
        except Payment.DoesNotExist:
            pass  # Handle as needed

        return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})

    return JsonResponse({'error': 'Invalid request'}, status=400)
