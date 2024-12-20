"""
Country
id

Kazakhstan
2

China
3

USA
5

Malaysia
6

Indonesia
7

Philippines
8

Myanmar
9

Vietnam
10

Romania
11

Poland
12

Canada
13

India
14

Zambia
15

Pakistan
16

Bangladesh
17

Mexico
18

Cambodia
19

Nicaragua
20

Kenya
96

Kyrgyzstan
97

Israel
98

Hong Kong
99

United Kingdom/England
100

Madagascar
101

Congo
102

Nigeria
103

Macao
104

Egypt
105

Ireland
106

Laos
107

Haiti
108

Côte d'Ivoire
109

Gambia
110

Serbia
111

Yemen
112

South Africa
113

Colombia
114

Estonia
115

Azerbaijan
116

Morocco
117

Ghana
118

Argentina
119

Uzbekistan
120

Cameroon
121

Chad
122

Germany
123

Lithuania
124

Croatia
125

Sweden
126

Iraq
127

Netherlands
128

Latvia
129

Austria
130

Belarus
131

Thailand
132

Saudi Arabia
133

Taiwan, Province of China
134

Spain
135

Algeria
137

Slovenia
138

Senegal
139

Turkey
140

Czechia
141

Sri Lanka
142

Peru
143

New Zealand
144

Guinea
145

Mali
146

Venezuela
147

Ethiopia
148

Mongolia
149

Brazil
150

Afghanistan
151

Uganda
152

Angola
153

Cyprus
154

France
155

Papua New Guinea
156

Mozambique
157

Nepal
158

Belgium
159

Bulgaria
160

Hungary
161

Moldova
162

Italy
163

Paraguay
164

Honduras
165

Tunisia
166

Somalia
167

Timor-Leste
168

Bolivia
169

Costa Rica
170

Guatemala
171

United Arab Emirates
172

Zimbabwe
173

Puerto Rico
174

Sudan
175

Togo
176

DR Congo
177

Albania
178

American Samoa
179

Antigua and Barbuda
182

Armenia
183

Australia
185

Bahamas
186

Bahrain
187

Barbados
188

Belize
189

Benin
190

Bhutan
192

Bosnia and Herzegovina
193

Botswana
194

Burkina Faso
196

Burundi
197

Cabo Verde
198

Central African Republic
200

Chile
201

Comoros
203

Denmark
206

Dominican Republic
209

Ecuador
210

El Salvador
211

Equatorial Guinea
212

Faroe Islands
214

Finland
216

French Guiana
217

Gabon
219

Georgia
220

Greece
222

Grenada
224

Guadeloupe
225

Guinea-Bissau
227

Guyana
228

Iceland
229

Jamaica
230

Japan
231

Jordan
232

Kuwait
234

Lebanon
235

Lesotho
236

Liberia
237

Luxembourg
239

Malawi
240

Maldives
241

Martinique
244

Mauritania
245

Mauritius
246

Namibia
251

New Caledonia
254

Niger
255

Norway
259

Oman
260

Portugal
263

Qatar
264

Rwanda
265

Singapore
270

Slovakia
271

Solomon Islands
272

Suriname
274

Switzerland
276

Tajikistan
277

Trinidad and Tobago
280

Turkmenistan
281

Turks and Caicos Islands
282

Uruguay
284

Korea (Korean Democratic People's Republic)
295

Korea, Republic of
296

Libya
297

North Macedonia
298

Palestine
300

Saint Kitts and Nevis
305

Saint Lucia
306

Saint Vincent and the Grenadines
309

Tanzania
313

Swaziland
315

Panama
316

Sierra Leone
317

Réunion
319

Republic of South Sudan
320

Republic of Kosovo
321


"""


import sqlite3
import pandas as pd
import random
import time
from tool.oto_tel import SMSManAPI
import traceback
import re
from playwright.sync_api import sync_playwright

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
def get_random_phone_number():
    api_key = "MDyufAcST2t90Fq9rdNvc0RMCh9z-Xjb"  # API anahtarınız
    sms_man = SMSManAPI(api_key)
    ref_id = "https://sms-man.com/?ref=--6WzJpWBx9Y"  # Referans ID'si (isteğe bağlı)
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


# Verilen bir istek için SMS almak için fonksiyon
def get_sms_for_request(request_id, timeout=300):
    api_key = "MDyufAcST2t90Fq9rdNvc0RMCh9z-Xjb"
    sms_man = SMSManAPI(api_key)
    start_time = time.time()
    while time.time() - start_time < timeout:
        sms_response = sms_man.get_sms(request_id)
        print(f"SMS Response: {sms_response}")  # Cevabı yazdır
        if 'sms_code' in sms_response and sms_response['sms_code']:
            print(f"REQUEST ID: {request_id}")
            print(f"Received SMS: {sms_response['sms_code']}")
            return sms_response['sms_code']
        if 'error_code' in sms_response:
            print("No SMS received yet, retrying...")
        time.sleep(2)
    print("Timeout while waiting for SMS.")
    return None


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
            print(error_element.count())
            print("two:", error_element_two.count())
            if any(element.count() > 0 for element in [error_element, error_element_two]):
                print("Hata: Telefon numarası çok fazla kez kullanıldı. Yeni telefon numarası alınıyor...")
                new_phone_number, new_request_id = get_random_phone_number()
                if new_phone_number:
                    page.fill("#phoneNumberId", "")  # Telefon numarası alanını temizle
                    time.sleep(6)
                    page.fill("#phoneNumberId", new_phone_number)
                    time.sleep(3)
                    page.click('button[jsname="LgbsSe"]')
                    time.sleep(5)

                    g_element = page.locator("span:has-text('G-')")
                    if g_element.count() > 0:
                        new_sms_code = get_sms_for_request(new_request_id)
                        if new_sms_code:
                            page.fill("input[name='code']", new_sms_code)  # Güncellenen alan
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
                break
    except Exception as e:
        print(f"Error checking phone number: {e}")


# Proxy verilerini yükle
proxy_df = pd.read_csv('data/proxy_data.csv')
flag_lock_sms = True

# Veritabanını başlat
conn = initialize_db()

with sync_playwright() as p:
    retry = True
    while True:
        for index, row in proxy_df.iterrows():
            PROXY = row['proxy']  # 'proxy' sütunundan proxy al
            country = row['country']
            region = row['region']
            city = row['city']

            a, b, c, d = PROXY.split(':')[:4]
            a = f"{a}:{b}"
            flag_one = True

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
                page.goto("https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp")
                excel_path = 'data/users_data.xlsx'
                # Kullanıcı bilgilerini doldur
                name_generator = generate_random_name_from_excel(excel_path, i)
                first_name, last_name, gmail_first_name, gmail_last_name, yorum = next(name_generator)
                print(f"{i}. değer DÖNGÜDEKİ {first_name}{last_name}{gmail_first_name}{gmail_last_name}{yorum}")
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
                if page.locator('//div[@aria-labelledby="selectionc2"]').is_visible():
                    # Eğer öğe varsa, bu işlemleri yap
                    page.click('//div[@aria-labelledby="selectionc2"]')
                    page.click('button[jsname="LgbsSe"]')
                    time.sleep(10)

                else:
                    print("GİRDİ ALANI BULAMADI!!!")

                # Öğenin varlığını kontrol et
                if page.locator('//div[@aria-labelledby="selectionc7"]').is_visible():
                    # Eğer öğe varsa, bu işlemleri yap
                    page.click('//div[@aria-labelledby="selectionc7"]')
                    page.fill('xpath=//input[@type="text"]', gmail)
                    time.sleep(2)
                    page.click('button[jsname="LgbsSe"]')
                    time.sleep(10)

                # Öğenin varlığını kontrol et
                else:
                    # Eğer öğe yoksa, doğrudan inputa yaz ve butona tıkla
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

                    phone_number, request_id = get_random_phone_number()

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
                            sms_code = get_sms_for_request(request_id)
                            if sms_code:
                                page.fill("input[name='code']", sms_code)  # SMS kodunu doldur
                                time.sleep(5)
                                page.click('button[jsname="LgbsSe"]')
                                time.sleep(5)
                                son_number_one = phone_number
                                page.click('button[jsname="LgbsSe"]')
                                time.sleep(5)
                                page.click('button[jsname="LgbsSe"]')
                                time.sleep(5)
                                page.click('//button//span[text()="Kabul ediyorum"]')
                                time.sleep(10)
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
                                page2.goto("https://mail.google.com/mail/u/0/#inbox", timeout=400000)
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
                                    i = i + 1
                                    print(f"{i}. Değere Gelindi")
                                    retry = False



            except Exception as e:
                print(f"Error occurred during account creation: {e}")
                retry = True  # Eğer başka bir hata alırsa tekrar denemesi için `retry` bayrağını `True` yapıyoruz.
                flag_data = False
            finally:
                print("Sondaki:", retry)
                page.close()
                context.close()
                browser.close()

# Veritabanı bağlantısını kapat
conn.close()
