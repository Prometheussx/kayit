import csv
import time
import pyautogui
import subprocess
import win32gui
import win32con
import pyperclip  # Kopyalama için gerekli kütüphane
import sqlite3
import math
from tqdm import tqdm
import random
import keyboard
from datetime import datetime, timedelta
pyautogui.FAILSAFE = False
# Uygulama çalıştırma ve tam ekran yapma fonksiyonu



#GİRİŞ KISMINI KONTROL ET EKLENTİ OLACKALARI EKLE BİTTİ



def run_application(app_path):
    try:
        # Uygulamayı çalıştır
        process = subprocess.Popen(app_path, shell=True)
        print(f"{app_path} çalıştırılıyor...")

        # Uygulamanın yüklenmesini bekleyin
        time.sleep(2)  # Gerekirse bu süreyi artırabilirsiniz

        # Uygulamanın penceresini al
        hwnd = win32gui.FindWindow(None, "MoreLogin | V2.26.0")  # Uygulamanın penceresini bul

        if hwnd:
            # Pencereyi tam ekran yap
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            print(f"{app_path} uygulaması tam ekrana alındı.")
        else:
            print("Pencere bulunamadı.")

        return process
    except Exception as e:
        print(f"Uygulama çalıştırılırken bir hata oluştu: {e}")
        return None


import sqlite3

def get_phone_number_by_index(index):
    db_name = 'google_accounts.db'
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    try:
        # Belirtilen id değerine göre telefon numarasını seçme
        c.execute('SELECT phone_number FROM accounts WHERE id = ?', (index,))
        phone_number = c.fetchone()  # Tek bir kaydı al
        if phone_number:
            return phone_number[0]  # Telefon numarası değeri
        else:
            print("Belirtilen ID bulunamadı.")
            return None
    except sqlite3.Error as e:
        print(f"Veritabanı hatası: {e}")
        return None
    finally:
        conn.close()



def get_review_by_index(index):
    db_name = 'google_accounts.db'
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    try:
        # Belirtilen id değerine göre yorumu seçme
        c.execute('SELECT yorum FROM accounts WHERE id = ?', (index,))
        review = c.fetchone()  # Tek bir kaydı al
        if review:
            return review[0]  # Yorum değeri
        else:
            print("Belirtilen ID bulunamadı.")
            return None
    except sqlite3.Error as e:
        print(f"Veritabanı hatası: {e}")
        return None
    finally:
        conn.close()

def countdown(seconds):
    for _ in tqdm(range(seconds), desc="Geri sayım", bar_format="{l_bar}{bar} [kalan: {remaining}]", mininterval=1.0):
        time.sleep(1)
    print("Süre doldu!")



def circular_motion(x, y, steps=random.randint(10, 20)):
    """Geniş dairesel hareket"""
    start_x, start_y = pyautogui.position()
    radius = math.hypot(x - start_x, y - start_y) / 2
    angle = 0
    for i in range(steps):
        angle += math.pi / steps + random.uniform(-0.2, 0.2)
        offset_x = int(radius * math.cos(angle))
        offset_y = int(radius * math.sin(angle))
        pyautogui.moveTo(start_x + offset_x, start_y + offset_y)


def zigzag_motion(x, y, steps=random.randint(10, 20)):
    """Geniş zikzak hareket"""
    start_x, start_y = pyautogui.position()
    for i in range(steps):
        offset_x = int((x - start_x) * (i + 1) / steps)
        offset_y = int((y - start_y) * (i + 1) / steps + random.choice([-30, 50]))
        pyautogui.moveTo(start_x + offset_x, start_y + offset_y)


def spiral_motion(x, y, steps=random.randint(10, 20)):
    """Geniş spiral hareket"""
    start_x, start_y = pyautogui.position()
    radius = math.hypot(x - start_x, y - start_y) / 2
    angle = 0
    for i in range(steps):
        angle += math.pi / steps
        offset_radius = radius * (1 - i / steps)
        offset_x = int(offset_radius * math.cos(angle))
        offset_y = int(offset_radius * math.sin(angle))
        pyautogui.moveTo(start_x + offset_x, start_y + offset_y)


def shake_motion(x, y, steps=random.randint(10, 20)):
    """Daha geniş sarsıntılı hareket"""
    start_x, start_y = pyautogui.position()
    for i in range(steps):
        offset_x = int((x - start_x) * (i + 1) / steps) + random.randint(-20, 40)
        offset_y = int((y - start_y) * (i + 1) / steps) + random.randint(-20, 40)
        pyautogui.moveTo(start_x + offset_x, start_y + offset_y)


def wavy_motion(x, y, steps=random.randint(10, 20)):
    """Geniş dalgalı hareket"""
    start_x, start_y = pyautogui.position()
    frequency = 3
    for i in range(steps):
        offset_x = int((x - start_x) * (i + 1) / steps)
        offset_y = int((y - start_y) * (i + 1) / steps + math.sin(i * frequency) * 30)
        pyautogui.moveTo(start_x + offset_x, start_y + offset_y)


def jitter_motion(x, y, steps=random.randint(10, 20)):
    """Daha büyük rastgele sapmalı hareket"""
    start_x, start_y = pyautogui.position()
    for i in range(steps):
        offset_x = int((x - start_x) * (i + 1) / steps) + random.randint(-10, 30)
        offset_y = int((y - start_y) * (i + 1) / steps) + random.randint(-10, 30)
        pyautogui.moveTo(start_x + offset_x, start_y + offset_y)


def sin_wave_motion(x, y, steps=random.randint(10, 20)):
    """Daha geniş sinüs dalgası hareketi"""
    start_x, start_y = pyautogui.position()
    amplitude = 20
    frequency = math.pi / 5
    for i in range(steps):
        offset_x = int((x - start_x) * (i + 1) / steps)
        offset_y = int((y - start_y) * (i + 1) / steps + amplitude * math.sin(i * frequency))
        pyautogui.moveTo(start_x + offset_x, start_y + offset_y)


def curve_motion(x, y, steps=random.randint(10, 20)):
    """Daha belirgin kavisli hareket"""
    start_x, start_y = pyautogui.position()
    control_x = (start_x + x) / 2 + random.randint(-80, 100)
    control_y = (start_y + y) / 2 + random.randint(-80, 100)
    for i in range(steps):
        t = i / steps
        offset_x = int((1 - t)**2 * start_x + 2 * (1 - t) * t * control_x + t**2 * x)
        offset_y = int((1 - t)**2 * start_y + 2 * (1 - t) * t * control_y + t**2 * y)
        pyautogui.moveTo(offset_x, offset_y)


def random_walk_motion(x, y, steps=random.randint(10, 20)):
    """Daha geniş rastgele adımlarla hareket"""
    current_x, current_y = pyautogui.position()
    for _ in range(steps):
        current_x += random.randint(-20, 40)
        current_y += random.randint(-20, 40)
        pyautogui.moveTo(current_x, current_y)


def bounce_motion(x, y, steps=random.randint(10, 20)):
    """Daha yüksek zıplama benzeri hareket"""
    start_x, start_y = pyautogui.position()
    for i in range(steps):
        offset_x = int((x - start_x) * (i + 1) / steps)
        offset_y = int((y - start_y) * (i + 1) / steps + abs(math.sin(i)) * 40)
        pyautogui.moveTo(start_x + offset_x, start_y + offset_y)


def smooth_human_like_move(x, y, steps=random.randint(2, 8)):
    start_x, start_y = pyautogui.position()  # Mevcut fare konumu
    delta_x = (x - start_x) / steps


    for i in range(steps):
        # Ara hedef konum hesaplama
        move_x = start_x + delta_x * i + random.uniform(-2, 2)  # Sağ-sol sapmaları

        pyautogui.moveTo(move_x, y)


# Ana hareket fonksiyonu
def human_like_click(x, y):
    movements = [
        circular_motion, zigzag_motion, spiral_motion, shake_motion,
        wavy_motion, jitter_motion, sin_wave_motion, curve_motion,
        random_walk_motion, bounce_motion
    ]

    # 3 farklı rastgele hareketi seç ve sırayla uygula
    selected_movements = random.choices(movements, k=5)
    for move in selected_movements:
        # Her hareket için rastgele koordinatlar belirle
        rand_x = random.randint(83, 1254)
        rand_y = random.randint(268, 987)
        print(rand_x,rand_y)
        move(rand_x, rand_y)

    # Son olarak hedef konuma gidip tıklayın
    bounce_motion(x, y)
    rand_x = x + random.randint(-25, 50)
    rand_y = y + random.randint(-10, 10)
    smooth_human_like_move(rand_x, rand_y)
    pyautogui.click()


def get_proxy_groups(csv_file, group_size=10):
    proxies = []
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            proxies.append(row[0])
    for i in range(0, len(proxies), group_size):
        yield proxies[i:i + group_size]


def del_account(panel_num):
    print("İlk Hesap kaldırma")
    pyautogui.click(x=750, y=350)#start
    time.sleep(12)

    pyautogui.hotkey('alt', 'space')
    time.sleep(2)
    pyautogui.press("down", presses=5)
    time.sleep(2)
    pyautogui.press("enter",presses=3)
    time.sleep(3)
    print(f"{panel_num + 1}. Kodlu Tarayıcı Tam Ekran Yapıldı")

    time.sleep(6)
    pyautogui.hotkey("ctrl","t")
    time.sleep(3)
    pyautogui.click(x=600, y=80)
    web = r"chrome://password-manager/passwords"
    pyautogui.write(web)
    pyautogui.press("enter")
    time.sleep(3)
    pyautogui.click(x=700, y=330) #ilk tıklama
    time.sleep(2)
    pyautogui.click(x=900, y=640) #pin click
    time.sleep(1)
    pyautogui.write("1115")

    time.sleep(1)
    pyautogui.click(x=700, y=330)  # ilk tıklama
    pyautogui.click(x=720, y=580) #delet
    time.sleep(2)

    pyautogui.hotkey("alt","f4")
    time.sleep(2)




def save_account(index):
    conn = sqlite3.connect('google_accounts.db')
    email, password, phone_number= get_account_by_index(conn, index)
    conn.close()
    if not email or not password:
        print(f"Account not found for index {index}")
        return


    time.sleep(1)
    #Burada ise A-1 Girmeden Hemen Önce Girip Sıradaki Hesabı Girecek eskisini silip
    #account edit
    pyautogui.moveTo(x=1320, y=338)
    time.sleep(2)
    pyautogui.doubleClick(x=1320, y=338)
    time.sleep(4)
    # Username Clear
    pyautogui.click(x=728, y=415)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")

    # Password Clear
    time.sleep(3)
    pyautogui.click(x=1050, y=415)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")
    time.sleep(1)
    #new_account_data
    pyautogui.click(x=728, y=415)
    pyautogui.write(email)
    time.sleep(2)

    pyautogui.click(x=1050, y=415)
    pyautogui.write(password)

    time.sleep(2)
    pyautogui.click(x=1350, y=855)


# Veritabanından id'ye göre yorum çekme fonksiyonu
def get_review_by_index(index):
    db_name = 'google_accounts.db'
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    try:
        c.execute('SELECT yorum FROM accounts WHERE id = ?', (index,))
        review = c.fetchone()
        if review:
            return review[0]
        else:
            print("Belirtilen ID bulunamadı.")
            return None
    except sqlite3.Error as e:
        print(f"Veritabanı hatası: {e}")
        return None
    finally:
        conn.close()


# Yazıyı manipüle eden
def random_delay():
    time.sleep(random.uniform(0.04, 0.7))  # Her harf arasındaki gecikme süresi


def add_random_punctuation_or_space():
    # %15 ihtimalle rastgele boşluk veya noktalama karakteri ekle, ardından geri sil
    if random.random() < 0.15:
        random_char = random.choice([' ', '.', ',', ':', ';'])
        keyboard.write(random_char)
        random_delay()
        keyboard.write('\b')


def temporary_capitalize(char):
    # %10 ihtimalle harfi geçici olarak büyük/küçük yaz, ardından düzelt
    if random.random() < 0.1:
        temp_char = char.upper() if char.islower() else char.lower()
        keyboard.write(temp_char)  # Geçici büyük/küçük harf yaz
        random_delay()
        keyboard.write('\b')  # Geri sil
        keyboard.write(char)  # Doğru haliyle yaz


# Rastgele işlemleri sıralı uygulayan fonksiyon
def write_with_random_operations(text):
    char_count = 0  # Yazılan karakter sayısını takip et
    for char in text:
        # Karakteri normal olarak yaz
        keyboard.write(char)
        random_delay()

        char_count += 1  # Karakter sayısını artır

        # Her 3,7 karakterde bir işlem uygula
        if char_count >= random.randint(3, 7):
            # %15 ihtimalle noktalama veya boşluk ekle
            add_random_punctuation_or_space()

            # %10 ihtimalle geçici büyük/küçük harf dönüşümü uygula
            temporary_capitalize(char)

            char_count = 0  # Karakter sayacını sıfırla



def paste_proxies(proxy_group):
    try:
        proxies_text = "\n".join(proxy_group)
        pyperclip.copy(proxies_text)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        print(f"{len(proxy_group)} adet proxy yapıştırıldı.")
    except Exception as e:
        print(f"Proxy yapıştırılırken bir hata oluştu: {e}")


def paste_cookie_click(cookie_csv_file):
    cookie = []
    with open(cookie_csv_file, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            cookie.append(row[0])
    try:
        cookie_text = "\n".join(cookie)
        pyperclip.copy(cookie_text)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
    except Exception as e:
        print(f"Cookie yapıştırılırken bir hata oluştu: {e}")


def proxy_return(tour, proxy_groups):
    print("Proxy Return Başlatıldı")
    # Şu anki proxy grubunu al
    current_proxy_group = proxy_groups[tour]
    pyautogui.click(x=350, y=270)
    time.sleep(1)
    pyautogui.click(x=1580, y=210)
    time.sleep(1)
    pyautogui.click(x=800, y=400)
    time.sleep(1)
    pyautogui.click(x=800, y=400)
    time.sleep(1)
    paste_proxies(current_proxy_group)
    time.sleep(3)
    pyautogui.click(x=1020, y=840)
    time.sleep(12)
    pyautogui.click(x=1250, y=830)
    time.sleep(5)


def clear_cache():
    print("Clear Cache Başlatıldı")
    pyautogui.click(x=350, y=270)
    time.sleep(2)
    pyautogui.click(x=1690, y=210)
    time.sleep(2)
    pyautogui.moveTo(x=1580, y=510)
    pyautogui.click(x=1530, y=510)
    time.sleep(2)
    pyautogui.click(x=605, y=240)
    time.sleep(1)
    pyautogui.click(x=575, y=410)
    time.sleep(1)
    pyautogui.click(x=725, y=410)
    time.sleep(1)
    pyautogui.click(x=1065, y=410)
    time.sleep(1)
    pyautogui.click(x=1370, y=950)
    time.sleep(10)


def refresh_fingerprint():
    print("Refresh FingerPrint Başlatıldı")
    x = ["A-1","B-2", "C-3", "D-4", "E-5", "F-6", "G-7", "H-8", "I-9", "J-10"]
    for i in x:
        pyautogui.click(x=1000, y=150)
        pyautogui.write(i)
        pyautogui.press("enter")
        time.sleep(5)
        pyautogui.click(x=825, y=350)
        time.sleep(1)
        pyautogui.click(x=825, y=420)
        time.sleep(3)
        pyautogui.click(x=1400, y=970)
        time.sleep(3)
        pyautogui.click(x=1000, y=150)
        pyautogui.press("backspace", presses=4)
        print(f"{i}. Tarayıcının Finger Printi Yenilendi")
        time.sleep(3)


def cookie_refresh():
    print("Cookie Refresh Başlatıldı")
    cookie_csv_file = r"data\cokkie_data.csv"
    pyautogui.click(x=350, y=270)
    time.sleep(1)
    pyautogui.click(x=1690, y=210)
    time.sleep(1)
    pyautogui.moveTo(x=1580, y=460)
    time.sleep(1)
    pyautogui.click(x=1530, y=460)
    time.sleep(3)
    pyautogui.click(x=930, y=360)  # cokkie chat click
    time.sleep(1)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")
    time.sleep(1)
    paste_cookie_click(cookie_csv_file)
    time.sleep(1)
    pyautogui.click(x=1060, y=625)
    pyautogui.press("backspace")
    pyautogui.press("backspace")
    pyautogui.write("39")
    time.sleep(1)
    pyautogui.click(x=1200, y=625)
    pyautogui.press("backspace")
    pyautogui.press("backspace")
    pyautogui.write("40")
    time.sleep(1)
    pyautogui.click(x=1230, y=830)
    time.sleep(1)
    pyautogui.click(x=1130, y=360)
    print("Cookie Başlatıldı...")
    countdown(720) #12Dk


def get_account_by_index(conn, index):
    c = conn.cursor()
    c.execute("SELECT email, password, phone_number FROM accounts WHERE id=?", (index,))
    result = c.fetchone()
    return result if result else (None, None)


def open_account(index,sirket,country_code):
    conn = sqlite3.connect('google_accounts.db')
    email, password, phone_number = get_account_by_index(conn, index)
    conn.close()
    if not email or not password:
        print(f"Account not found for index {index}")
        return

    time.sleep(5)


    #mail
    pyautogui.click(x=1555, y=150) #Sign in
    time.sleep(4)

    #Mailin İlk 5 Hargi Girdirtilecek Ardından 5.Tıklandırıalcak bu sayede bulunabilecek

    pyautogui.click(x=1050, y=450)  # chatıklama
    time.sleep(1)
    pyautogui.click(x=1050, y=450)  # chatıklama
    time.sleep(3)
    pyautogui.click(x=1250, y=520) #1. hesaba tıklama
    time.sleep(2)
    pyautogui.click(x=1580, y=700)
    time.sleep(4)

    # CAPTCHA EKLENTİ KOY
    time.sleep(3)
    pyautogui.click(x=1020, y=520)
    time.sleep(4)
    pyautogui.click(x=645, y=845)
    time.sleep(8)
    pyautogui.click(x=1580, y=700)
    time.sleep(6)
    pyautogui.click(x=1580, y=700)
    time.sleep(2)



    #password
    pyautogui.click(x=1050, y=500)
    time.sleep(1)

    pyautogui.click(x=1160, y=590)
    time.sleep(1)
    pyautogui.click(x=1580, y=700)
    time.sleep(5)


    #telefon numarası zorunlu girdi alanı
    pyautogui.click(x=1050, y=720)
    time.sleep(2)
    pyautogui.click(x=1160, y=530)
    time.sleep(2)
    phn_number = get_phone_number_by_index(index)
    pyautogui.write(phn_number)
    time.sleep(2)
    pyautogui.click(x=1580, y=670)#tel sorusu nexti

    time.sleep(3)
    pyautogui.click(x=1400, y=740)#password kayıta natnow tuşu
    time.sleep(2)
    print("Hata Tıklama Geldi")
    pyautogui.click(x=1580, y=700)
    time.sleep(6)
    pyautogui.click(x=1400, y=740)
    time.sleep(6)
    pyautogui.click(x=1140, y=840)
    time.sleep(6)
    pyautogui.click(x=390, y=790)





    """1
    #tel no girme
    pyautogui.click(x=1050, y=570)
    pyautogui.write(phone_number)
    time.sleep(1)
    pyautogui.click(x=1220, y=710)

    #Not Now
    human_like_click(x=1400, y=740)
    time.sleep(2)
    #Recovery Information
    human_like_click(x=1140, y=840)
    time.sleep(2)
    #two not now
    human_like_click(x=330, y=775)
    time.sleep(2)

"""



    print(f"Opened account for {email}")
    time.sleep(9)

    #TrustPilot İçin Yeni Sayfanın Açılması
    pyautogui.hotkey('ctrl', 't')  # Yeni sekme açıldı
    time.sleep(3)

    pyautogui.click(x=350, y=80)
    web = f"https://{country_code}.trustpilot.com/users/connect"
    pyautogui.write(web)
    pyautogui.press("enter")
    time.sleep(22)

    #Trustpilot Login
    human_like_click(x=950, y=445) #Google Button
    time.sleep(15)
    human_like_click(x=850, y=575) #Hesabı Seçme
    time.sleep(10)
    human_like_click(x=1100, y=825)
    time.sleep(10)
    pyautogui.click(x=755, y=440)#onaytiki ve onay tuşu
    time.sleep(4)
    human_like_click(x=900, y=600)

#şirket arama

    time.sleep(12)
    human_like_click(x=320, y=155)
    time.sleep(12)
    human_like_click(x=850, y=575) #Arama Çubuğu
    time.sleep(2)
    pyautogui.write(sirket)
    time.sleep(3)
    human_like_click(x=850, y=730) #ŞİRKERE TIKLAMA
    time.sleep(9)
    pyautogui.click(x=1070, y=590) #YILDIZ SEÇİMİ 5
    time.sleep(4)
    pyautogui.moveTo(x=750, y=590)#cchat gitme
    human_like_click(x=750, y=590)
    print(index)
    #YORUM YAZDIRMA
    review_text = get_review_by_index(index)
    print(review_text)
    if review_text:
        write_with_random_operations(review_text)
    time.sleep(2)
    human_like_click(x=1450, y=590)
    time.sleep(2)
    pyautogui.scroll(-800) # Aşağıya doğru 200 piksel kaydır
    time.sleep(2)

    pyautogui.click(x=695, y=740)
    pyautogui.click(x=695, y=740)
    time.sleep(5)
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 10, 20)

    # Rastgele bir tarih seçimi
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

    # Tarihi gün, ay, yıl olarak formatlama
    day = random_date.day
    month = random_date.month
    year = 2024

    for value in [month, day]:
        pyautogui.write(str(value))
        time.sleep(2)

    for digit in str(year):
        pyautogui.write(digit)
        time.sleep(2)

    time.sleep(3)
    #Yorumu Gönderme

    human_like_click(x=950, y=900)
    time.sleep(12)

    #ANA SAYFAYA GELME
    human_like_click(x=320, y=155)
    time.sleep(5)
    #trustpilot LOG OUT

    pyautogui.moveTo(x=1480, y=180)
    time.sleep(2)
    pyautogui.moveTo(x=1450, y=420)
    time.sleep(3)
    pyautogui.click(x=1450, y=420)
    time.sleep(5)
    #GMAİL LOGOUT
    #never sistem
    pyautogui.click(x=800, y=20)
    time.sleep(3)
    pyautogui.click(x=1810, y=450)#never kodus
    time.sleep(2)
    pyautogui.moveTo(x=1875, y=135)
    time.sleep(1)
    pyautogui.click(x=1875, y=135)
    time.sleep(2)
    pyautogui.click(x=1750, y=505)
    time.sleep(12)
    #ACCOUNT REMOVE
    pyautogui.click(x=1200, y=600)
    time.sleep(1)
    pyautogui.click(x=1450, y=450)
    time.sleep(1)
    pyautogui.click(x=1200, y=620)


def open_panel(total_comments,sirket,country_code):
    proxy_path = r"data\\rewiev_proxy.csv"
    proxy_groups = list(get_proxy_groups(proxy_path))  # Proxy gruplarını oluştur

    num_panels = math.ceil(total_comments / 10)
    for panel_num in range(total_comments):
        if panel_num >= 10:
            panel_num = panel_num-10

        time.sleep(2)
        pyautogui.click(x=1000, y=150)
        time.sleep(1) #65 ve 1 di
        pyautogui.write(f"{chr(68 + panel_num)}-{panel_num + 4}")
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(1)
        account_index = panel_num + 1

        del_account(panel_num)
        time.sleep(5)

        save_account(account_index)
        time.sleep(3)


        pyautogui.click(x=750, y=350)

        time.sleep(12)
        pyautogui.hotkey('alt', 'space')
        time.sleep(1)
        pyautogui.press("down", presses=5)
        time.sleep(2)
        pyautogui.press("enter",presses=3)
        time.sleep(2)
        print(f"{panel_num + 1}. Kodlu Tarayıcı Tam Ekran Yapıldı")
        time.sleep(10)


        # Her panelde yalnızca bir hesap açılacak
        open_account(account_index,sirket,country_code)

        # Yorum atma işlemleri burada olacak
        time.sleep(6)
        print("ALT F4 DEVREYE GİRDİ")
        print(panel_num)
        print(num_panels)

        pyautogui.hotkey('alt', 'f4')
        time.sleep(2)
        pyautogui.click(x=1000, y=150)
        pyautogui.press("backspace", presses=4)
        time.sleep(2)

        #5-10-15-20 DK ARA İLE ARALIK FONKSİYONU Belki Sayaç Eklenir
        # Bekleme sürelerini dakika cinsinden tanımlayın

        # Rastgele bir bekleme süresi seçin
        selected_wait_time = random.randint(37, 62)
        dakika = selected_wait_time*60
        # Dakikayı saniyeye çevirin ve bekleyin
        print(f"{selected_wait_time} dakika bekleniyor...")
        countdown(dakika)  # Dakikaları saniyeye çeviriyoruz

        print("Bekleme süresi tamamlandı.")


        # Proxy işlemi ve cache temizleme
        if panel_num % 10 == 9:  # Her 10 panelde bir proxy değiştir
            if panel_num // 10 < len(proxy_groups):  # Proxy grubu mevcut mu kontrol et
                print(proxy_groups)
                print(panel_num)
                panel_num = panel_num+1
                proxy_return(panel_num // 10, proxy_groups)
                clear_cache()
                refresh_fingerprint()
                cookie_refresh()
            else:
                print("Proxy grubu mevcut değil.")



def main():
    app_path = r"C:\\Users\\erdem\\MoreLoginPlus\\2.26.0.0\\MoreLogin.exe"
    proxy_path = r"data\\rewiev_proxy.csv"
    sirket = input("Hangi Şirkete atmak istiyosunuz? ")
    total_comments = int(input("Kaç yorum atmak istiyorsunuz? "))
    country_code = input("Hangi Ülke Kodu ca,uk,us: ")
    run_application(app_path)
    time.sleep(5)
    # Proxy gruplarını listeye dönüştür
    #proxy_groups = list(get_proxy_groups(proxy_path))  # Generator'ı listeye çevir

    # İlk proxy grubunu kullan
    #proxy_return(0, proxy_groups)

    #clear_cache()
    #refresh_fingerprint()
    #cookie_refresh()

    open_panel(total_comments,sirket,country_code)



#trustpilot çıkma mail çıkma mail silme yapılacak kapanacak

if __name__ == "__main__":
    main()