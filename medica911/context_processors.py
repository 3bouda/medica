import os

def google_config(request):
    client_id = os.getenv('GOOGLE_CLIENT_ID', '')
    return {
        'GOOGLE_CLIENT_ID': client_id
    }
