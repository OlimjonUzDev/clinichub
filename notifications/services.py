import requests
import os


def send_sms(phone_number, message_text):
    url = f"https://{os.getenv('INFOBIP_BASE_URL')}/sms/2/text/advanced"
    
    headers = {
        'Authorization': f"App {os.getenv('INFOBIP_API_KEY')}",
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    
    data = {
        "messages": [
            {
                "destinations": [{"to": phone_number}],
                "from": "InfoSMS",
                "text": message_text
            }
        ]
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()