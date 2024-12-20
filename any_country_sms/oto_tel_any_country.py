import http.client
import json
import time

# API anahtarınızı buraya ekleyin
api_key = "j7YN1GiGDBXLwuOlvZJA7dTzjRn6k1"

def get_phone_number(country_code, service_code):
    conn = http.client.HTTPSConnection("api.smspva.com")

    # API başlıkları (API anahtarı)
    headers = {
        'apikey': api_key
    }

    # API isteği gönderme
    conn.request("GET", f"/activation/number/{country_code}/{service_code}", headers=headers)

    # Yanıtı alma
    res = conn.getresponse()
    data = res.read()

    # JSON yanıtını çözümleme
    response_data = json.loads(data.decode("utf-8"))

    # Yanıt kodunun 200 olduğunu kontrol etme
    if response_data['statusCode'] == 200:
        phone_number = response_data['data']['phoneNumber']
        order_id = response_data['data']['orderId']
        return order_id, phone_number
    else:
        # Hata mesajı döndürme
        return response_data['statusCode'], None

def check_sms(order_id):

    conn = http.client.HTTPSConnection("api.smspva.com")
    headers = {
        'apikey': api_key
    }

    # SMS kontrolü için API isteği gönderme
    conn.request("GET", f"/activation/sms/{order_id}", headers=headers)
    res = conn.getresponse()
    data = res.read()

    # Yanıtı çözümleme
    response_data = json.loads(data.decode("utf-8"))

    if response_data['statusCode'] == 200:
        return response_data['data']['sms']['code']  # SMS kodunu döndürüyoruz
    else:
        return None

# Ülke kodunu (örneğin 'RU' Rusya için) ve hizmet kodunu (örneğin 'opt20') belirleyin
country_code = "IT"
service_code = "opt1"
