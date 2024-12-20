import sqlite3
import pandas as pd
import random
import time
from oto_tel_any_country import get_phone_number,check_sms
from playwright.sync_api import sync_playwright
import traceback
import re


# HER HESABI OLANA KADAR HER PROXYDE DENİYECEK

# g-code ayıkla
i = 0

# SQLite bağlantısını kur ve tabloyu oluştur
def initialize_db(db_name='google_accounts.db'):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            password TEXT,
            phone_number TEXT,
            proxy TEXT,
            country TEXT,
            region TEXT,
            city TEXT,
            yorum TEXT
        )
    ''')
    conn.commit()
    return conn

def get_phone_number_by_email(conn, email):
    c = conn.cursor()
    c.execute("SELECT phone_number FROM accounts WHERE email = ?", (email,))
    result = c.fetchone()
    return result[0] if result else None

# Hesap bilgilerini veritabanına kaydet
def save_account(conn, email, password, phone_number, proxy, country, region, city, yorum):
    try:
        c = conn.cursor()
        c.execute(
            "INSERT INTO accounts (email, password, phone_number, proxy, country, region, city, yorum) VALUES (?, ?, ?, ?, ?, ?, ?,?)",
            (email, password, phone_number, proxy, country, region, city, yorum)
        )
        conn.commit()
        print(f"Account created: {email}:{password}")
    except Exception as e:
        print(f"Error saving account data: {e}")
        traceback.print_exc()


# Rastgele bir ad ve soyad oluşturur
def generate_random_name_from_excel(excel_path,i):

    try:
        # Excel dosyasını oku
        df = pd.read_excel(excel_path)
        # Sadece dolu olan satırları filtrele
        df = df[['İsim', 'Soyisim', 'Yorum']]
        # Verileri döngüyle sırayla çekmek için indeks oluştur
        first_name = df.loc[i,'İsim']
        last_name = df.loc[i,'Soyisim']
        gmail_first_name = '.'.join(df.loc[i,'İsim'].split())
        gmail_last_name = '.'.join(df.loc[i,'Soyisim'].split())
        yorum = df.loc[i,'Yorum']

        print(f"{i}. değer defteki {first_name}{last_name}{gmail_first_name}{gmail_last_name}{yorum}")
        yield first_name, last_name,gmail_first_name,gmail_last_name,yorum  # Her isim soyisim çifti döndürülecek
    except Exception as e:
        print(f"Error reading Excel data: {e}")
        return None


# Rastgele bir telefon numarası almak için fonksiyon
def get_random_phone_number(country_code,service_code):
    order_id, phone_number = get_phone_number(country_code, service_code)
    print(f"Verification Created: {phone_number}")
    return phone_number, order_id



def extract_numbers(code):
    # 'G-' ifadesinden sonra gelen sayıları eşleştirir
    match = re.search(r"G-(\d+)", code)
    if match:
        return match.group(1)
    return None


# Verilen bir istek için SMS almak için fonksiyon
def get_sms_for_request(order_id):

    if order_id:
        sms_details = check_sms(order_id)
        print(sms_details)
        sms_code = sms_details['data']['sms']['code']
        # Sonucu yazdırma
        print(f"SMS Kodu: {sms_code}")
        return sms_code


# Rastgele bir şifre oluşturur
def generate_random_password():
    random_number = random.randint(100, 999)
    psw = f"estetik{random_number}_ist"
    return psw


# Yeni telefon numarasını al ve SMS kodunu doğrula
def check_and_retry_phone_number(page):
    try:
        while True:
            error_element = page.locator("//div[contains(text(), 'Bu telefon numarası çok fazla kez kullanıldı')]")
            error_element_two = page.locator(
                "//div[contains(text(), 'Bu telefon numarası doğrulama için kullanılamaz')]")
            print("one", error_element.count())
            print("two:", error_element_two.count())
            if any(element.count() > 0 for element in [error_element, error_element_two]):
                # Kod buraya gelecek
                print("Hata: Telefon numarası çok fazla kez kullanıldı. Yeni telefon numarası alınıyor...")
                new_phone_number, order_id = get_random_phone_number()
                if new_phone_number:
                    page.fill("#phoneNumberId", "")  # Telefon numarası alanını temizle
                    time.sleep(6)
                    page.fill("#phoneNumberId", new_phone_number)
                    time.sleep(3)
                    page.click('button[jsname="LgbsSe"]')
                    time.sleep(5)

                    g_element = page.locator("span:has-text('G-')")
                    if g_element.count() > 0:
                        new_sms_code = get_sms_for_request(order_id)
                        if new_sms_code:
                            new_clear_sms = extract_numbers(new_sms_code)
                            page.fill("input[name='code']", new_clear_sms)  # Güncellenen alan
                            time.sleep(5)
                            page.click('button[jsname="LgbsSe"]')
                            time.sleep(5)
                            son_number = new_phone_number
                            page.click('button[jsname="LgbsSe"]')
                            time.sleep(5)
                            page.click('button[jsname="LgbsSe"]')
                            time.sleep(5)
                            try:
                                page.click('//button//span[text()="Kabul ediyorum"]')
                            except:
                                print("Kabul Ediyorum Yok Beklemede Devam edicek")
                            time.sleep(20)
                            # Hesap bilgilerini kaydet
                            save_account(conn, gmail, password, son_number, PROXY, country, region, city, yorum)

                            break
                    else:
                        print("G- değeri hala görünmüyor, devam ediliyor...")
            else:
                print("Error element not found, exiting loop.")

    except Exception as e:
        print(f"Error checking phone number: {e}")


# Proxy verilerini yükle
proxy_df = pd.read_csv('data/proxy_data.csv')
flag_lock_sms = True
# Veritabanını başlat
# Veritabanını başlat
conn = initialize_db()

with sync_playwright() as p:
    # Jeneratör burada tanımlanmalı
    retry = True

    while True:
        for index, row in proxy_df.iterrows():
            excel_path = 'data/users_data.xlsx'
            name_generator = generate_random_name_from_excel(excel_path, i)
            first_name, last_name, gmail_first_name, gmail_last_name, yorum = next(name_generator)
            print(f"{i}. değer DÖNGÜDEKİ {first_name}{last_name}{gmail_first_name}{gmail_last_name}{yorum}")

            PROXY = row['proxy']  # 'proxy' sütunundan proxy al
            country = row['country']
            region = row['region']
            city = row['city']

            a, b, c, d = PROXY.split(':')[:4]
            a = f"{a}:{b}"
              # Başlangıçta `retry` bayrağını `False` yapıyoruz, hata durumunda tekrar `True` yapılacak.

            # Proxy ayarlarıyla tarayıcıyı başlat
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(proxy={
                "server": f"{a}",
                "username": f"{c}",
                "password": f"{d}"
            })
            page = context.new_page()

            try:
                # Google hesap oluşturma sayfasını aç
                page.goto(
                    "https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp")

                # Kullanıcı bilgilerini doldur
                 # Her seferinde yeni bir isim almak için burada kullanıyoruz
                username = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 1000)}"
                password = generate_random_password()

                page.fill("#firstName", first_name)
                page.fill("#lastName", last_name)
                page.click("#collectNameNext > div > button")
                time.sleep(9)

                # Doğum tarihi ve cinsiyeti doldur
                page.select_option("#month", value="1")  # Ocak ayı için '1' varsayıldı
                rand_day = random.randint(1, 30)
                rand_year = random.randint(1990, 2002)
                page.fill("#day", str(rand_day))
                page.fill("#year", str(rand_year))

                page.select_option("#gender", value="3")  # '3' istenen cinsiyet değeri varsayıldı
                page.click("#birthdaygenderNext > div > button")
                time.sleep(10)

                # Gmail kullanıcı adını seç veya gir

                rand_gmail = random.randint(1, 3)
                gmail = f"{gmail_first_name}.{gmail_last_name}.{last_name[-rand_gmail:]}{random.randint(0, 999)}"

                # Öğenin varlığını kontrol et
                if page.locator('//div[@aria-labelledby="selectionc4"]').is_visible():
                    page.click('//div[@aria-labelledby="selectionc4"]')
                    page.fill('xpath=//input[@type="text"]', gmail)
                    time.sleep(2)
                    page.click('button[jsname="LgbsSe"]')
                    time.sleep(10)
                else:
                    page.fill('xpath=//input[@type="text"]', gmail)
                    time.sleep(2)
                    page.click('button[jsname="LgbsSe"]')
                    time.sleep(10)

                # Şifreyi ve şifreyi onayla
                page.fill("input[name='Passwd']", password)
                page.fill("input[name='PasswdAgain']", password)
                time.sleep(2)
                page.click('button[jsname="LgbsSe"]')
                time.sleep(9)

                # Hata kontrolü
                if page.locator("h1.vAV9bf:has-text('Hata')").is_visible():
                    print("HESAP AÇILAMAM HATASI ALINDI!!!! YENİ SAYFAYA GEÇİLİYOR")
                    retry = True  # Hata alındı, aynı bilgilerle tekrar denenecek.
                    flag_data = False
                    page.close()
                else:
                    # Başarılı olursa diğer işlemleri burada yapabilirsiniz.
                    retry = False  # Hesap başarıyla açıldığından dolayı döngü tekrar etmeyecek.
                    # Veritabanı kaydetme işlemi gibi diğer işlemler burada yapılabilir.
                    error_element = page.locator(
                        "//div[contains(text(), 'Bu telefon numarası çok fazla kez kullanıldı')]")

                    error_element_two = page.locator(
                        "//div[contains(text(), 'Bu telefon numarası doğrulama için kullanılamaz')]")

                    phone_number, href = get_random_phone_number()

                    if phone_number:
                        page.fill("#phoneNumberId", phone_number)
                        time.sleep(3)
                        page.click('button[jsname="LgbsSe"]')
                        time.sleep(8)

                        if any(element.count() > 0 for element in [error_element, error_element_two]):
                            # Telefon numarasının yeniden doğrulanması gerekiyorsa
                            check_and_retry_phone_number(page)
                            flag_lock_sms = False
                        if flag_lock_sms:
                            # SMS kodunu al ve doldur
                            sms_code = get_sms_for_request(href)
                            clear_sms_one = extract_numbers(sms_code)
                            if sms_code:
                                page.fill("input[name='code']", clear_sms_one)  # SMS kodunu doldur
                                time.sleep(3)
                                page.click('button[jsname="LgbsSe"]')
                                time.sleep(5)
                                son_number_one = phone_number
                                page.click('button[jsname="LgbsSe"]')
                                time.sleep(5)
                                page.click('button[jsname="LgbsSe"]')
                                time.sleep(5)
                                page.click('//button//span[text()="Kabul ediyorum"]')
                                time.sleep(4)
                                try:
                                    page.click('//button//span[text()="Onayla"]')
                                except:
                                    print("Onay Yok Devam")
                                time.sleep(5)
                                # Hesap bilgilerini kaydet
                                save_account(conn, gmail, password, son_number_one, PROXY, country, region, city, yorum)
                                print("Kullanıcı başarıyla oluşturuldu.")
                                time.sleep(6)

                                # YENİ SEKME MAİL GİRİŞ
                                page2 = context.new_page()
                                page2.goto("https://mail.google.com/mail/u/0/#inbox", timeout=300000)
                                time.sleep(5)
                                url = f"https://accounts.google.com/AccountChooser?Email={gmail}@gmail.com&continue=https://myaccount.google.com/signinoptions/recoveryoptions?opendialog%3Dcollectphone%26skipverify%3Dtrue%26roc%3Dfalse%26continue%3Dhttps://myaccount.google.com%26hl%3Dtr%26utm_source%3Dogep_bn_a3_w%26utm_medium%3Dam_ep%26utm_campaign%3Dbento_mvp"
                                page3 = context.new_page()
                                page3.goto(url)
                                time.sleep(5)
                                phone_number = get_phone_number_by_email(conn, gmail)

                                # Telefon numarası alanını doldurun
                                if phone_number:
                                    try:
                                        page3.fill("input[placeholder='Enter number']", phone_number)  # İngilizce
                                    except:
                                        page3.fill("input[placeholder='Numarayı girin']", phone_number)  # Türkçe
                                    time.sleep(2)

                                    # "Save" veya "Kaydet" butonuna tıklayın
                                    # Try clicking the button with the aria-label in English first, then fall back to Turkish if it fails.
                                    try:
                                        page3.click("button[aria-label='Save your recovery phone']")  # English version
                                    except:
                                        page3.click(
                                            "button[aria-label='Kurtarma telefon numaranızı kaydedin']")  # Turkish version

                                        print(retry)
                                    time.sleep(5)
                                    i = i+1
                                    print(f"{i}. Değere Gelindi")
                                    retry = False



            except Exception as e:
                print(f"Error occurred during account creation: {e}")
                retry = True  # Eğer başka bir hata alırsa tekrar denemesi için `retry` bayrağını `True` yapıyoruz.
                flag_data = False
            finally:
                print("Sondaki:",retry)
                page.close()
                context.close()
                browser.close()


# Veritabanı bağlantısını kapat
conn.close()