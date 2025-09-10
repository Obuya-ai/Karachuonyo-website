import requests
import base64
import json
from datetime import datetime
import os

class MPesaAPI:
    def __init__(self):
        self.consumer_key = os.getenv('MPESA_CONSUMER_KEY', 'test_key')
        self.consumer_secret = os.getenv('MPESA_CONSUMER_SECRET', 'test_secret')
        self.business_short_code = '174379'  # Test shortcode
        self.passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        self.base_url = 'https://sandbox.safaricom.co.ke'
        self.callback_url = 'https://karachuonyo-backend.onrender.com/api/mpesa/callback'
        self.access_token = None
    
    def get_access_token(self):
        credentials = f"{self.consumer_key}:{self.consumer_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()
        
        headers = {'Authorization': f'Basic {encoded}'}
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            print(f"Access token request status: {response.status_code}")
            print(f"Access token response: {response.text}")
            
            if response.status_code == 200:
                self.access_token = response.json()['access_token']
                return self.access_token
            else:
                print(f"Failed to get access token. Status: {response.status_code}, Response: {response.text}")
                raise Exception(f'Failed to get access token: {response.status_code} - {response.text}')
        except requests.exceptions.RequestException as e:
            print(f"Request exception: {e}")
            raise Exception(f'Network error getting access token: {str(e)}')
    
    def stk_push(self, phone, amount, account_ref, description):
        if not self.access_token:
            self.get_access_token()
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f"{self.business_short_code}{self.passkey}{timestamp}".encode()).decode()
        
        # Format phone number
        if phone.startswith('0'):
            phone = '254' + phone[1:]
        
        payload = {
            'BusinessShortCode': self.business_short_code,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': int(amount),
            'PartyA': phone,
            'PartyB': self.business_short_code,
            'PhoneNumber': phone,
            'CallBackURL': self.callback_url,
            'AccountReference': account_ref,
            'TransactionDesc': description
        }
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
        response = requests.post(url, json=payload, headers=headers)
        
        return response.json()

mpesa = MPesaAPI()