import keyboard
import time
time.sleep(5)
# Arapça metin

text = """
I had a teeth whitening procedure at Estetik International and the results were great. My teeth look brighter and whiter than ever. The procedure was quick and comfortable, I did not feel any discomfort. The clinic was very clean and modern and the staff was very professional. I felt very comfortable thanks to their friendly approach and detailed information. I would recommend Estetik International to anyone considering teeth whitening!

"""
def slow_type(text, delay=0.3):
    for char in text:
        keyboard.write(char)  # Her bir karakteri yazdır
        time.sleep(delay)  # Belirtilen süre kadar bekle

# Türkçe karakterleri yavaşça yazdırmak için
slow_type(text)  # 0.5 saniye gecikmeyle yazdırır


