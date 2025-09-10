import os
from dotenv import load_dotenv
from mpesa import mpesa

# Load environment variables
load_dotenv()

print('=== M-Pesa Configuration Test ===')
print(f'Consumer Key: {os.getenv("MPESA_CONSUMER_KEY", "NOT_SET")[:20]}...')
print(f'Consumer Secret: {os.getenv("MPESA_CONSUMER_SECRET", "NOT_SET")[:20]}...')
print('\n=== Testing M-Pesa Access Token ===')

try:
    token = mpesa.get_access_token()
    if token:
        print(f'✅ Success: {token[:20]}...')
    else:
        print('❌ Failed: No token returned')
except Exception as e:
    print(f'❌ Error: {str(e)}')