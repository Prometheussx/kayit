import sqlite3
import pandas as pd
import time
from playwright.sync_api import sync_playwright
import random

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

# Veritabanından tüm hesap bilgilerini al
def get_all_accounts(conn):
    c = conn.cursor()
    c.execute("SELECT email, password, phone_number, proxy, country, region, city, yorum FROM accounts")
    return c.fetchall()

# Proxy verilerini yükle
def get_proxies_from_db(conn):
    c = conn.cursor()
    c.execute("SELECT proxy, country, region, city FROM accounts")
    return c.fetchall()

# Veritabanını başlat
conn = initialize_db()

# Veritabanından tüm hesap bilgilerini al
accounts_data = get_all_accounts(conn)
proxies_data = get_proxies_from_db(conn)

# Playwright işlemini başlat
with sync_playwright() as p:
    retry = True
    i = 0
    while True:
        for account_data, proxy_data in zip(accounts_data, proxies_data):
            email, password, phone_number, _, country, region, city, yorum = account_data
            PROXY, proxy_country, proxy_region, proxy_city = proxy_data

            a, b, c, d = PROXY.split(':')[:4]
            a = f"{a}:{b}"

            # Proxy ayarlarıyla tarayıcıyı başlat
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(proxy={
                "server": f"{a}",
                "username": f"{c}",
                "password": f"{d}"
            })
            page = context.new_page()

            try:
                # Veritabanından alınan hesap bilgilerini kullanarak giriş yap
                print(f"Logging in with {email}")

                # Google login sayfasına git
                page.goto("https://accounts.google.com/signin/v2/identifier")

                # E-posta adresini gir
                page.fill("input[type='email']", email)
                page.click("//button[span[text()='Sonraki']]")
                time.sleep(150)



                # Şifreyi gir
                page.fill("input[type='password']", password)
                page.click("button[jsname='LgbsSe']")
                time.sleep(5)

                # Hesaba giriş yapıldı mı kontrol et
                if page.locator("h1.vAV9bf:has-text('Hata')").is_visible():
                    print("HESAP GİRİŞİ HATASI ALINDI!!!! YENİ SAYFAYA GEÇİLİYOR")
                    retry = True  # Hata alındı, aynı bilgilerle tekrar denenecek.
                    page.close()
                else:
                    print("Başarıyla giriş yapıldı")
                    retry = False  # Başarılı olursa tekrar denemeyecek.

                    # Diğer işlemleri buradan başlatabilirsiniz
                    # Örneğin, kullanıcı ayarları veya başka bir işlem yapılabilir.

            except Exception as e:
                print(f"Error occurred during login: {e}")
                retry = True  # Eğer başka bir hata alırsa tekrar denemesi için `retry` bayrağını `True` yapıyoruz.
                page.close()
            finally:
                page.close()
                context.close()
                browser.close()

            # Kullanıcı verileri için index'i arttır
            i += 1

# Veritabanı bağlantısını kapat
conn.close()
