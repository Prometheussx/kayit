import requests
import time


class SMSManAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.sms-man.com/control/"

    def get_balance(self):
        response = requests.get(f"{self.base_url}get-balance?token={self.api_key}")
        return response.json()

    def get_limits(self, country_id=None, application_id=None):
        params = {"token": self.api_key}
        if country_id:
            params['country_id'] = country_id
        if application_id:
            params['application_id'] = application_id

        response = requests.get(f"{self.base_url}limits", params=params)
        return response.json()

    def request_phone_number(self, country_id=None, application_id=None, ref=None):
        params = {"token": self.api_key}
        if country_id:
            params['country_id'] = country_id
        if application_id:
            params['application_id'] = application_id
        if ref:
            params['ref'] = ref  # Ref ID ekleniyor

        response = requests.get(f"{self.base_url}get-number", params=params)
        return response.json()

    def get_sms(self, request_id):
        response = requests.get(f"{self.base_url}get-sms?token={self.api_key}&request_id={request_id}")
        return response.json()

    def change_request_status(self, request_id, status):
        params = {
            "token": self.api_key,
            "request_id": request_id,
            "status": status
        }
        response = requests.post(f"{self.base_url}set-status", data=params)
        return response.json()


def get_random_phone_number():
    api_key = "MDyufAcST2t90Fq9rdNvc0RMCh9z-Xjb"  # Your API key
    sms_man = SMSManAPI(api_key)
    ref_id = "https://sms-man.com/?ref=--6WzJpWBx9Y"  # Reference ID (optional)
    number_response = sms_man.request_phone_number(country_id=12, application_id=122, ref=ref_id)
    if 'number' in number_response:
        request_id = number_response['request_id']
        number = number_response['number']
        print(f"Received phone number: {number}")
        print(f"Request_id: {request_id}")
        return number, request_id
    else:
        print("Failed to get a phone number")
        return None, None


def get_sms_for_request(request_id, timeout=300):
    api_key = "MDyufAcST2t90Fq9rdNvc0RMCh9z-Xjb"
    sms_man = SMSManAPI(api_key)
    start_time = time.time()
    while time.time() - start_time < timeout:
        sms_response = sms_man.get_sms(request_id)
        print(f"SMS Response: {sms_response}")  # Yanıtı yazdır
        if 'sms' in sms_response and sms_response['sms']:
            print(f"REQUEST ID: {request_id}")
            print(f"Received SMS: {sms_response['sms']}")
            return sms_response['sms']
        if 'error_code' in sms_response:
            print("No SMS received yet, retrying...")
        time.sleep(2)
    print("SMS alma süresi doldu.")
    return None

# Kullanım Örneği
if __name__ == "__main__":
    # Rastgele bir telefon numarası al
    phone_number, request_id = get_random_phone_number()

    # Eğer telefon numarası başarılı bir şekilde alındıysa, SMS almayı dene
    if phone_number and request_id:
        print(f"Test için alınan numara: {phone_number}, Request ID: {request_id}")

        # SMS alma fonksiyonunu test et
        received_sms = get_sms_for_request(request_id, timeout=300)  # 300 saniye (5 dakika) timeout
        if received_sms:
            print(f"Başarıyla SMS alındı: {received_sms}")
        else:
            print("SMS alma işlemi başarısız oldu.")
    else:
        print("Telefon numarası alınamadı, işlem durduruldu.")