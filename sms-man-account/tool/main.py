import sqlite3
import pandas as pd
from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import random
import pyautogui
import time
from selenium.common.exceptions import NoSuchElementException
from oto_tel import SMSManAPI

# SQLite bağlantısı kur
conn = sqlite3.connect('../google_accounts.db')
c = conn.cursor()
# Eğer tablo yoksa oluştur
c.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        password TEXT,
        proxy TEXT,
        country TEXT,
        region TEXT,
        city TEXT
    )
''')

conn.commit()


# This function generates a random first name and last name
def generate_random_name():
    first_names = ["Andrew", "James", "Joshua", "David", "Matthew", "Joseph", "Jonathan", "Samuel", "Alexander", "Luke"]
    last_names = ["Brown", "Morris", "Lee", "Hall", "Johnson", "Smith", "Wilson"]
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return first_name, last_name


# Function to get a random phone number
def get_random_phone_number():
    api_key = "MDyufAcST2t90Fq9rdNvc0RMCh9z-Xjb"  # Your API keSy
    sms_man = SMSManAPI(api_key)
    ref_id = "https://sms-man.com/?ref=--6WzJpWBx9Y"  # Reference ID (optional)
    number_response = sms_man.request_phone_number(country_id=155, application_id=122, ref=ref_id)
    if 'number' in number_response:
        request_id = number_response['request_id']
        number = number_response['number']
        print(f"Received phone number: {number}")
        print(f"Request_id: {request_id}")
        return number, request_id
    else:
        print("Failed to get a phone number")
        return None, None


# Function to fetch SMS for a given request
def get_sms_for_request(request_id, timeout=300):
    api_key = "MDyufAcST2t90Fq9rdNvc0RMCh9z-Xjb"
    sms_man = SMSManAPI(api_key)
    start_time = time.time()
    while time.time() - start_time < timeout:
        sms_response = sms_man.get_sms(request_id)
        print(f"SMS Response: {sms_response}")  # Print the response
        if 'sms_code' in sms_response and sms_response['sms_code']:
            print(f"REQUEST ID: {request_id}")
            print(f"Received SMS: {sms_response['sms_code']}")
            return sms_response['sms_code']
        if 'error_code' in sms_response:
            print("No SMS received yet, retrying...")
        time.sleep(2)
    print("Timeout while waiting for SMS.")
    return None


# Generates a random password
def generate_random_password():
    random_number = random.randint(100, 999)
    psw = f"estetik{random_number}_ist"
    return psw


from selenium.common.exceptions import NoSuchElementException

def check_and_retry_phone_number(driver):
    try:
        # Hata mesajını kontrol et
        error_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Bu telefon numarası çok fazla kez kullanıldı')]")
        if error_element:
            print("Hata: Telefon numarası çok fazla kez kullanıldı. Yeni telefon numarası alınıyor...")
            # Yeni bir telefon numarası al
            new_phone_number, new_request_id = get_random_phone_number()
            if new_phone_number:
                driver.find_element(By.ID, "phoneNumberId").clear()
                time.sleep(6)
                driver.find_element(By.ID, "phoneNumberId").send_keys(new_phone_number)
                time.sleep(3)
                driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div/div/div/button").click()
                time.sleep(5)

                # Yeni SMS kodunu al ve doğrula
                new_sms_code = get_sms_for_request(new_request_id)
                if new_sms_code:
                    driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[2]/div/div[1]/div/div[1]/input").send_keys(new_sms_code)
                    time.sleep(5)
                    driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button").click()
                    time.sleep(5)
                    print("Yeni telefon numarası ve SMS doğrulandı.")
                else:
                    print("Yeni SMS alınamadı.")
    except NoSuchElementException:
        print("Telefon numarası hatası yok.")





# Load proxy data
proxy_df = pd.read_csv('../data/proxy_data.csv')

for index, row in proxy_df.iterrows():
    PROXY = row['proxy']  # Get the proxy from the 'proxy' column
    country = row['country']
    region = row['region']
    city = row['city']

    # Initialize ChromeDriver with proxy settings
    chrome_options = Options()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--no-sandbox")

    seleniumwire_options = {
        'proxy': {
            'http': PROXY,
            'https': PROXY,
            'no_proxy': 'localhost,127.0.0.1'
        }
    }

    # Start WebDriver (with proxy)
    driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=chrome_options,
                              seleniumwire_options=seleniumwire_options)

    try:
        # Open the Google account creation page
        driver.get("https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp")

        # Fill in the user information
        first_name, last_name = generate_random_name()
        username = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 1000)}"
        password = generate_random_password()

        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "firstName"))).send_keys(first_name)
            driver.find_element(By.ID, "lastName").send_keys(last_name)
            driver.find_element(By.XPATH, "//*[@id='collectNameNext']/div/button").click()
            time.sleep(9)

            # Fill in the birthdate and gender
            driver.find_element(By.ID, "month").click()
            driver.find_element(By.XPATH,
                                "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[1]/div[2]/div/div/div[2]/select/option[2]").click()

            rand_day = random.randint(1, 30)
            rand_year = random.randint(1990, 2002)

            driver.find_element(By.ID, "day").send_keys(rand_day)
            driver.find_element(By.ID, "year").send_keys(rand_year)

            driver.find_element(By.ID, "gender").click()
            driver.find_element(By.XPATH,
                                "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[2]/div[1]/div/div[2]/select/option[4]").click()

            driver.find_element(By.XPATH, "//*[@id='birthdaygenderNext']/div/button").click()
            time.sleep(10)

            # Select or enter a Gmail username
            rand_gmail = random.randint(1, 3)
            gmail = f"{first_name}.{last_name}.{last_name[-rand_gmail:]}{random.randint(0, 99)}"
            try:
                driver.find_element(By.XPATH,
                                    "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[1]/div[1]/div/span/div[3]/div/div[1]/div").click()
                driver.find_element(By.XPATH,
                                    "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[2]/div[1]/div/div[1]/div/div[1]/input").send_keys(gmail)
                driver.find_element(By.XPATH,
                                    "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button").click()
                time.sleep(10)
            except NoSuchElementException:
                try:
                    driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div/div[1]/div/div[1]/div/div[1]/input").send_keys(gmail)
                    driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button").click()
                    time.sleep(6)
                except NoSuchElementException:
                    print("No element found.")

            # Fill in the password and confirm password
            driver.find_element(By.NAME, "Passwd").send_keys(password)
            driver.find_element(By.NAME, "PasswdAgain").send_keys(password)
            time.sleep(5)

            driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div/div/div/button").click()
            time.sleep(9)

            #BURAYA HATA MESAJI ALINDIĞIDNA TLEEFON ÇEKEMEMSİ İÇİN BİR SİSTME EKLENMELİ BOŞA TEL EÇKİP SMS APİ YORUYUO TIKIYOR



            # Phone number and SMS verification
            phone_number, request_id = get_random_phone_number()
            if phone_number:
                driver.find_element(By.ID, "phoneNumberId").send_keys(phone_number)
                time.sleep(12)
                driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div/div/div/button").click()
                time.sleep(5)

                # Hata mesajını kontrol et ve yeniden dene
                check_and_retry_phone_number(driver)

                sms_code = get_sms_for_request(request_id)
                print(sms_code)
                if sms_code:
                    driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[2]/div/div[1]/div/div[1]/input").send_keys(sms_code)
                    time.sleep(5)

                    driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button").click()
                    time.sleep(5)

                    driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div/div[1]/div/div/button").click()
                    time.sleep(7)
                    driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div/div/div/button").click()
                    time.sleep(7)
                    driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button").click()
                    time.sleep(1)
                    # Ekleme: Hesap bilgilerini SQLite veritabanına kaydet
                    c.execute("INSERT INTO accounts (email, password, proxy, country, region, city) VALUES (?, ?, ?, ?, ?, ?)",
                              (gmail, password, PROXY, country, region, city))
                    conn.commit()
                    print(f"{username} adlı kullanıcı SQLite veritabanına eklendi.")
                    time.sleep(40)
        except Exception as e:
            print(f"Hata: {e}")

    finally:
        driver.quit()

# Bağlantıyı kapat
conn.close()
