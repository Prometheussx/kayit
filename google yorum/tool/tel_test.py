import time
import requests
from oto_tel import TextVerifiedAPI

# Gerekli API bilgileri
API_KEY = "ilGoSbd6APTxoT5iC5v53vmXQuDovUDGtQCNHSRXqgV5Q1aCAdUDdY7aFXduAWa"
EMAIL = "erdemtahasokullu@gmail.com"

# Initialize the API
text_verified = TextVerifiedAPI(API_KEY, EMAIL)

if __name__ == "__main__":
    try:
        text_verified.generate_bearer_token()
        account_details = text_verified.get_account_details()
        print(f"Account Details: {account_details}")

        verification = text_verified.create_verification()
        print(f"Verification Created: {verification}")

        href = verification.get('href')
        if href:
            verification_details = text_verified.get_verification_details(href)
            phone_number = verification_details.get("number")
            print(f"Phone Number: {phone_number}")

            text_verified.poll_for_verification(href)
            time.sleep(1)
            sms_details = text_verified.get_sms_details(phone_number=phone_number)

            for sms in sms_details:
                print(f"From: {sms['from']}, To: {sms['to']}, Content: {sms['smsContent']}")

    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")


    # Step 8: Optional - Cancel or Reactivate Verification
    verification_id = "your_verification_id_here"
    cancel_result = text_verified.cancel_verification(verification_id)
    print(f"Verification Canceled: {cancel_result}")

    reactivate_result = text_verified.reactivate_verification(verification_id)
    print(f"Verification Reactivated: {reactivate_result}")
