from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl
import time

# WhatsApp Web'i açmak için tarayıcı başlatın
driver = webdriver.Chrome()
driver.get('https://web.whatsapp.com')

# QR kodu taranana kadar bekle
print("WhatsApp Web'e giriş yapmak için QR kodunu tarayın. Oturum açıldıktan sonra işlem başlayacak.")

# Mesaj kutularını bulmak için bir bekleyici tanımlayın
wait = WebDriverWait(driver, 95)  # 60 saniyeye kadar QR kodunu tarayana kadar bekleyin

# Daha önce eklenen numaraları takip etmek için bir küme oluşturun
added_numbers = set()

try:
    # QR kodu tarandıktan sonra otomatik işlem yapacak alan
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'x1iyjqo2')))  # Mesaj kutularını bulana kadar bekle

    # Excel dosyasını oluşturun veya var olan dosyayı açın
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Katılımcı Bilgileri"

    # Başlık satırını ekleyin
    ws.append(["Numara", "Email", "İsim", "Soyisim", "Katılım Durumu (Evet/Hayır)", "Ödeme Alındı mı?"])

    # Sonsuz döngü içinde ekrandaki numaraları sürekli olarak kontrol edin
    while True:
        
        try:
            # Mesaj kutularını bulun
            chats = driver.find_elements(By.CLASS_NAME, 'x1iyjqo2')

            for chat in chats:
                title = chat.get_attribute('title')
                if title and '+90' in title and title not in added_numbers:
                    # Varsayılan diğer bilgiler
                    email = ""
                    isim = ""
                    soyisim = ""
                    katilim_durumu = "Hayır"  # Varsayılan olarak 'Hayır'
                    odeme_alindi = "Alınmadı"  # Varsayılan olarak 'Alınmadı'
                    
                    ws.append([title, email, isim, soyisim, katilim_durumu, odeme_alindi])
                    added_numbers.add(title)  # Eklenen numarayı kümeye ekleyin
                wb.save('katilimci_bilgileri.xlsx')
        except EC.StaleElementReferenceException:
            pass
        
        # 2 saniye bekle ve tekrar numaraları kontrol et
        time.sleep(2)

finally:
    # Tarayıcıyı kapatın
    driver.quit()
