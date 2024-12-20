import selenium
from selenium import webdriver
import time
import csv
from selenium.webdriver.common.by import By
# WebDriver'ı başlat
driver = webdriver.Chrome()

# Hedef URL'yi belirt
url = "https://mytaget.com/kaydol"
driver.get(url)

# Kullanıcı bilgilerini CSV dosyasından oku ve bir listeye sakla
kullanici_listesi = []
with open("bilgidosya.csv", "r", newline="", encoding="utf-8") as dosya:
    csv_okuyucu = csv.DictReader(dosya)
    for satir in csv_okuyucu:
        kullanici_listesi.append(satir)

    # Her bir kullanıcı bilgisi için kayıt işlemini gerçekleştir
    for kullanici in kullanici_listesi:
        isim = kullanici["isim"] + " " + kullanici["soyisim"]
        email = kullanici["Mail"]
        num = kullanici["num"]
        sifre = kullanici["isim"] + kullanici["index"]
        kod = kullanici["kod"]

        # Web sayfasındaki giriş alanlarına bilgileri gir
        isim_gir = driver.find_element("id","name").send_keys(isim)
        mail_gir = driver.find_element("id","email").send_keys(email)
        num_gir = driver.find_element("id","phone").send_keys(num)
        sifre_gir = driver.find_element("id","password").send_keys(sifre)
        tekrar_sifre_gir = driver.find_element("id","password_confirmation").send_keys(sifre)
        time.sleep(1)
        # Kayıt butonuna tıkla
        kayit = driver.find_element(By.XPATH,"/html/body/main/form/div[1]/div/span")
        kayit.click()
        time.sleep(1)
        #Bilgi girme Atlama
        kayit = driver.find_element(By.XPATH,"/html/body/main/form/div[2]/div/div[2]/span[2]")
        kayit.click()
        #paltform seçimi
        kayit = driver.find_element(By.XPATH,"/html/body/main/form/div[3]/div/div[1]/div[2]/select")
        kayit.click()
        time.sleep(1)
        #paltform seçimi
        kayit = driver.find_element(By.XPATH,"/html/body/main/form/div[3]/div/div[1]/div[2]/select/option[15]")
        kayit.click()
        time.sleep(1)
        platformmail= driver.find_element("id","accountInput").send_keys(email)
        time.sleep(1)
        kayit = driver.find_element(By.XPATH,"/html/body/main/form/div[3]/div/div[2]/span[2]")
        kayit.click()
        time.sleep(1)
        
        #GENEL BİLGİ GİRİŞİ
        firmaadı= driver.find_element("name","company_name").send_keys("Bilkom Bilişim Hizmetleri")
        time.sleep(1)
        
        company_website = driver.find_element("name","company_website").send_keys("www.bilkom.com.tr")
        time.sleep(1)
        
        company_email = driver.find_element("name","company_email").send_keys(email)
        time.sleep(1)
        
        company_phone = driver.find_element("name","company_phone").send_keys(num)
        time.sleep(1)

        sehirsec = driver.find_element(By.XPATH,"/html/body/main/form/div[4]/div/div[1]/div[7]/select")
        sehirsec.click()
        time.sleep(1)
        sehirsec = driver.find_element(By.XPATH,"/html/body/main/form/div[4]/div/div[1]/div[7]/select/option[35]")
        sehirsec.click()
        time.sleep(1)

        ilcesec = driver.find_element(By.XPATH,"/html/body/main/form/div[4]/div/div[1]/div[8]/select")
        ilcesec.click()
        time.sleep(1)
        ilcesec = driver.find_element(By.XPATH,"/html/body/main/form/div[4]/div/div[1]/div[8]/select/option[17]")
        ilcesec.click()
        time.sleep(1)

        firmagec = driver.find_element(By.XPATH,"/html/body/main/form/div[4]/div/div[2]/span[2]")
        firmagec.click()
        time.sleep(1)

    #RENK SEÇİMİ
        renksec = driver.find_element(By.XPATH,"/html/body/main/form/div[5]/div/div[1]/div[2]/div[10]/div/input")
        renksec.click()
        time.sleep(1)
        renksec = driver.find_element(By.XPATH,"/html/body/main/form/div[5]/div/div[2]/span[2]")
        renksec.click()
        time.sleep(1)

        kodgir = driver.find_element(By.XPATH,"/html/body/main/form/div[6]/div/div[1]/div[2]/input").send_keys(kod)
        time.sleep(1)
    #Bitir
        kodgir = driver.find_element(By.XPATH,"/html/body/main/form/div[6]/div/div[3]/button")
        kodgir.click()
        time.sleep(3)

    # Kayıt işleminden sonra tekrar kayıt sayfasına dön
        kayıt = driver.find_element(By.XPATH,"/html/body/main/div/a")
        kayıt.click()
        
