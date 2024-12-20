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
import pandas as pd
import keyboard
from datetime import datetime, timedelta

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


df = pd.read_csv("data/rewiev_text_data.csv")

def get_review_by_index(index):
    # Belirtilen indeksteki yorumu seçme
    try:
        review = df.loc[df['Unnamed: 0'] == index, 'yorum'].values[0]
        return review
    except IndexError:
        print("Belirtilen index bulunamadı.")
        return None

def countdown(seconds):
    for _ in tqdm(range(seconds), desc="Geri sayım", bar_format="{l_bar}{bar} [kalan: {remaining}]", mininterval=1.0):
        time.sleep(1)
    print("Süre doldu!")


def human_like_click(x, y):
    # Dairesel hareketle hedefe gitmeden önce bir süre bekleyin


    # Mevcut fare konumunu alın
    start_x, start_y = pyautogui.position()
    distance = math.hypot(x - start_x, y - start_y)  # Hedefe olan uzaklık

    # Hedefe doğru bir daire çizme işleEstetmi
    steps = random.randint(5, 10)  # Hareketk Internat sayısı
    radius = distance / 3  # Dairenin yarıçapı
    angle = 0  # Başlangıç açısı

    for i in range(steps):
        # Açıya göre yeni pozisyon hesapla
        angle += math.pi / steps  # Açıyı artırarak daireyi tamamla
        offset_x = int(radius * math.cos(angle))
        offset_y = int(radius * math.sin(angle))

        # Yeni ara konuma git
        pyautogui.moveTo(start_x + offset_x, start_y + offset_y)
        time.sleep(random.uniform(0.01, 0.03))  # Hareketler arası kısa bekleme süresi

    # Hedef konuma hızlıca gidin ve tıklayın
    pyautogui.moveTo(x, y, duration=random.uniform(0.1, 0.2))
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
    time.sleep(4)

    pyautogui.hotkey('alt', 'space')
    pyautogui.press("down", presses=5)
    pyautogui.press("enter")
    time.sleep(1)
    print(f"{panel_num + 1}. Kodlu Tarayıcı Tam Ekran Yapıldı")

    time.sleep(6)
    pyautogui.hotkey("ctrl","t")
    time.sleep(3)
    human_like_click(x=350, y=80)
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
    # Şu anki proxy grubunu al
    current_proxy_group = proxy_groups[tour]
    human_like_click(x=350, y=270)
    time.sleep(1)
    human_like_click(x=1580, y=210)
    time.sleep(1)
    human_like_click(x=800, y=400)
    time.sleep(1)
    human_like_click(x=800, y=400)
    time.sleep(1)
    paste_proxies(current_proxy_group)
    time.sleep(3)
    human_like_click(x=1020, y=840)
    time.sleep(12)
    human_like_click(x=1250, y=830)

    # Proxy'leri yapıştır
    paste_proxies(current_proxy_group)
    time.sleep(6)


def clear_cache():
    human_like_click(x=350, y=270)
    time.sleep(1)
    human_like_click(x=1690, y=210)
    time.sleep(1)
    pyautogui.moveTo(x=1580, y=510)
    human_like_click(x=1530, y=510)
    time.sleep(2)
    human_like_click(x=605, y=240)
    human_like_click(x=575, y=410)
    human_like_click(x=725, y=410)
    human_like_click(x=1065, y=410)
    human_like_click(x=1370, y=950)
    time.sleep(10)


def refresh_fingerprint():
    x = ["A-1", "B-2", "C-3", "D-4", "E-5", "F-6", "G-7", "H-8", "I-9", "J-10"]
    for i in x:
        human_like_click(x=1000, y=150)
        pyautogui.write(i)
        pyautogui.press("enter")
        time.sleep(5)
        human_like_click(x=825, y=350)
        time.sleep(1)
        human_like_click(x=825, y=420)
        time.sleep(3)
        human_like_click(x=1400, y=970)
        time.sleep(3)
        human_like_click(x=1000, y=150)
        pyautogui.press("backspace", presses=4)
        print(f"{i}. Tarayıcının Finger Printi Yenilendi")
        time.sleep(3)


def cookie_refresh():
    cookie_csv_file = r"data\cokkie_data.csv"
    human_like_click(x=350, y=270)
    time.sleep(1)
    human_like_click(x=1690, y=210)
    time.sleep(1)
    pyautogui.moveTo(x=1580, y=460)
    time.sleep(1)
    human_like_click(x=1530, y=460)
    time.sleep(3)
    human_like_click(x=930, y=360)  # cokkie chat click
    time.sleep(1)
    paste_cookie_click(cookie_csv_file)
    time.sleep(1)
    human_like_click(x=1060, y=625)
    pyautogui.press("backspace")
    pyautogui.press("backspace")
    pyautogui.write("39")
    time.sleep(1)
    human_like_click(x=1200, y=625)
    pyautogui.press("backspace")
    pyautogui.press("backspace")
    pyautogui.write("40")
    time.sleep(1)
    human_like_click(x=1230, y=830)
    time.sleep(1)
    human_like_click(x=1130, y=360)
    print("Cookie Başlatıldı...")
    countdown(720) #12Dk


def get_account_by_index(conn, index):
    c = conn.cursor()
    c.execute("SELECT email, password, phone_number FROM accounts WHERE id=?", (index,))
    result = c.fetchone()
    return result if result else (None, None)


def open_account(index,sirket):
    conn = sqlite3.connect('google_accounts.db')
    email, password, phone_number = get_account_by_index(conn, index)
    conn.close()
    if not email or not password:
        print(f"Account not found for index {index}")
        return

    time.sleep(3)


    #mail
    pyautogui.click(x=1450, y=150) #Sign in
    time.sleep(2)

    #Mailin İlk 5 Hargi Girdirtilecek Ardından 5.Tıklandırıalcak bu sayede bulunabilecek

    pyautogui.click(x=1050, y=450)  # chatıklama
    time.sleep(1)
    pyautogui.click(x=1050, y=300)
    time.sleep(1)
    pyautogui.click(x=1050, y=450)
    time.sleep(1)
    pyautogui.click(x=1050, y=300)
    time.sleep(1)
    pyautogui.click(x=1050, y=450)
    time.sleep(2)
    pyautogui.click(x=1250, y=790) #5.tıklama
    time.sleep(2)
    pyautogui.click(x=1580, y=700)
    time.sleep(4)

    # CAPTCHA EKLENTİ KOY
    time.sleep(3)
    human_like_click(x=1020, y=520)
    time.sleep(4)
    human_like_click(x=645, y=845)
    time.sleep(8)
    human_like_click(x=1580, y=700)
    time.sleep(6)
    human_like_click(x=1580, y=700)
    time.sleep(2)



    #password
    pyautogui.click(x=1050, y=500)
    time.sleep(1)

    pyautogui.click(x=1160, y=590)

    time.sleep(1)
    pyautogui.click(x=1580, y=700)

    time.sleep(5)



    """
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
    time.sleep(1)

    #TrustPilot İçin Yeni Sayfanın Açılması
    pyautogui.hotkey('ctrl', 't')  # Yeni sekme açıldı
    time.sleep(3)

    human_like_click(x=350, y=80)
    web = r"https://www.trustpilot.com/users/connect?redirect=%2f&source_cta=header"
    pyautogui.write(web)
    pyautogui.press("enter")
    time.sleep(10)

    #Trustpilot Login
    human_like_click(x=950, y=445) #Google Button
    time.sleep(9)
    human_like_click(x=850, y=575) #Hesabı Seçme
    time.sleep(8)
    pyautogui.click(x=850, y=575)
    #onaytiki ve onay tuşu
    time.sleep(9)
    human_like_click(x=320, y=155)
    time.sleep(4)
    human_like_click(x=850, y=575) #Arama Çubuğu
    time.sleep(2)
    pyautogui.write(sirket)
    time.sleep(3)
    human_like_click(x=850, y=730) #ŞİRKERE TIKLAMA
    time.sleep(3)
    human_like_click(x=1070, y=590) #YILDIZ SEÇİMİ 5
    time.sleep(2)
    pyautogui.moveTo(x=750, y=590)#cchat gitme
    human_like_click(x=750, y=590)
    print(index)
    #YORUM YAZDIRMA
    review_text = get_review_by_index(index)
    for char in review_text:
        keyboard.write(char)  # Her bir karakteri yazdır
        time.sleep(0.2)

    time.sleep(2)
    pyautogui.scroll(-800)  # Aşağıya doğru 200 piksel kaydır
    time.sleep(2)

    pyautogui.doubleClick(x=950, y=740)


    #Tarih Yazdırma

    # Başlangıç ve bitiş tarihleri
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 10, 20)

    # Rastgele bir tarih seçimi
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

    # Tarihi gün, ay, yıl olarak formatlama
    day = random_date.day
    month = random_date.month
    year = random_date.year

    for value in [month, day, year]:
        pyautogui.write(str(value))
        time.sleep(0.5)# Gün/Ay/Yıl şeklinde

    time.sleep(2)
    #Yorumu Gönderme
    #human_like_click(x=950, y=900)
    time.sleep(5)
    #ANA SAYFAYA GELME
    pyautogui.click(x=320, y=155)
    time.sleep(3)
    #trustpilot LOG OUT

    pyautogui.moveTo(x=1480, y=180)
    time.sleep(1)
    pyautogui.moveTo(x=1450, y=420)
    time.sleep(1)
    pyautogui.click(x=1450, y=420)
    time.sleep(3)
    #GMAİL LOGOUT
    pyautogui.click(x=800, y=20)
    time.sleep(1)
    pyautogui.moveTo(x=1875, y=135)
    time.sleep(1)
    pyautogui.click(x=1875, y=135)
    time.sleep(1)
    pyautogui.click(x=1750, y=505)
    time.sleep(12)
    #ACCOUNT REMOVE
    pyautogui.click(x=1200, y=600)
    time.sleep(1)
    pyautogui.click(x=1450, y=450)
    time.sleep(1)
    pyautogui.click(x=1200, y=620)


def open_panel(total_comments,sirket):
    proxy_path = r"data\\rewiev_proxy.csv"
    proxy_groups = list(get_proxy_groups(proxy_path))  # Proxy gruplarını oluştur

    num_panels = math.ceil(total_comments / 10)
    for panel_num in range(total_comments):
        if panel_num >= 10:
            panel_num = panel_num-10

        time.sleep(2)
        human_like_click(x=1000, y=150)
        time.sleep(1)
        pyautogui.write(f"{chr(65 + panel_num)}-{panel_num + 1}")
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(1)
        account_index = panel_num + 1



        del_account(panel_num)
        time.sleep(5)

        save_account(account_index)
        time.sleep(3)


        human_like_click(x=750, y=350)

        time.sleep(8)
        pyautogui.hotkey('alt', 'space')
        pyautogui.press("down", presses=5)
        pyautogui.press("enter",presses=3)
        time.sleep(2)
        print(f"{panel_num + 1}. Kodlu Tarayıcı Tam Ekran Yapıldı")
        time.sleep(10)


        # Her panelde yalnızca bir hesap açılacak
        open_account(account_index,sirket)

        # Yorum atma işlemleri burada olacak
        time.sleep(6)
        print("ALT F4 DEVREYE GİRDİ")
        print(panel_num)
        print(num_panels)

        pyautogui.hotkey('alt', 'f4')
        time.sleep(2)
        human_like_click(x=1000, y=150)
        pyautogui.press("backspace", presses=4)
        time.sleep(2)

        #5-10-15-20 DK ARA İLE ARALIK FONKSİYONU Belki Sayaç Eklenir
        # Bekleme sürelerini dakika cinsinden tanımlayın
        wait_times = [5, 10, 15, 20]

        # Rastgele bir bekleme süresi seçin
        selected_wait_time = random.choice(wait_times)

        # Dakikayı saniyeye çevirin ve bekleyin
        print(f"{selected_wait_time} dakika bekleniyor...")
        time.sleep(selected_wait_time * 60)  # Dakikaları saniyeye çeviriyoruz

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
    sirket = input("Hangi Şirkete atmak istiyorsunuz? ")
    total_comments = int(input("Kaç yorum atmak istiyorsunuz? "))
    run_application(app_path)
    time.sleep(5)
    # Proxy gruplarını listeye dönüştür
    #proxy_groups = list(get_proxy_groups(proxy_path))  # Generator'ı listeye çevir

    # İlk proxy grubunu kullan
    #proxy_return(0, proxy_groups)

    #clear_cache()
    #refresh_fingerprint()
    #cookie_refresh()

    open_panel(total_comments,sirket)



#trustpilot çıkma mail çıkma mail silme yapılacak kapanacak

if __name__ == "__main__":
    main()
