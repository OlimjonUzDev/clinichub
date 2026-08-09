import requests
import os

def send_sms(phone_number, message_text):
    """Berilgan telefon raqamiga Infobip SMS API orqali matnli xabar yuboradi.

    Funksiya `INFOBIP_BASE_URL` va `INFOBIP_API_KEY` muhit o'zgaruvchilari
    yordamida Infobip'ning "/sms/2/text/advanced" endpointiga POST so'rov
    yuboradi (side effect: tashqi SMS xizmatiga tarmoq chaqiruvi, 10 soniya
    timeout bilan).

    Parametrlar:
        phone_number: Xabar yuboriladigan qabul qiluvchi telefon raqami
            (masalan, "998901234567" formatida).
        message_text: Yuboriladigan SMS matni.

    Qaytaradi:
        So'rov muvaffaqiyatli bo'lsa, Infobip javobining JSON (dict) ko'rinishi.
        Tarmoq/HTTP xatosi yuz bersa, `{'error': <xato matni>}` ko'rinishidagi
        dict qaytariladi (istisno tashqariga chiqarilmaydi).

    Xatolar:
        `requests.exceptions.RequestException` ichkarida ushlanadi va
        xato matni natija sifatida qaytariladi, funksiya buzilmaydi.
    """

    url = f"https://{os.getenv('INFOBIP_BASE_URL')}/sms/2/text/advanced"
    headers = {
        'Authorization': f"App {os.getenv('INFOBIP_API_KEY')}",
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    data = {
        "messages": [
            {"destinations": [{"to": phone_number}], "from": "InfoSMS", "text": message_text}
        ]
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}