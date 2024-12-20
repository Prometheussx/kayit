import keyboard
import time
time.sleep(5)
# Arapça metin

text = """My breast augmentation at Estetik International was an exceptional experience and a great value for the level of service provided. From the first consultation, I felt welcomed and valued. The clinic is beautifully designed, and the food and room services were outstanding, making my stay comfortable and stress-free. The entire process, from consultation to recovery, was handled professionally, and I couldn’t be happier with the results. If you want a comprehensive and quality experience, Estetik International is the place to go."""
def slow_type(text, delay=0.2):
    for char in text:
        keyboard.write(char)  # Her bir karakteri yazdır
        time.sleep(delay)  # Belirtilen süre kadar bekle

# Türkçe karakterleri yavaşça yazdırmak için
slow_type(text)  # 0.5 saniye gecikmeyle yazdırır


