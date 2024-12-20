import segno
from PIL import Image
import os

dosya = input("Dosya Adı Girini: ")

output_directory = "qrkayit"
os.makedirs(output_directory, exist_ok=True)

with open(dosya+'.txt', 'r') as dosya:
    linkler = dosya.read().split(',')

for x, link in enumerate(linkler):
    print(link.strip())
    # QR kodu oluştur
    qrcode = segno.make(link.strip())

    # QR kodunu SVG formatında bir dosyaya kaydet
    qrcode.save("temp_qrcode.png",light="red",dark="white",scale=5, border=1)

    # SVG dosyasını bir PIL resmine dönüştür
    img = Image.open("temp_qrcode.png").convert("RGBA")

    # Beyaz pikselleri şeffaflaştır
    datas = img.getdata()
    new_data = []

    for item in datas:
        # Renk değerlerini al
        r, g, b, a = item

        # Beyaz pikselleri şeffaflaştır (r=255, g=255, b=255)
        if r == 255 and g == 0 and b == 0:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append((r, g, b, a))

    # Yeni veriyi resme uygula
    img.putdata(new_data)

    # Şeffaf arka planlı resmi kaydet
    output_path = os.path.join(output_directory, f"{x}_transparent_qrcode.png")
    img.save(output_path, format="PNG")

os.remove("temp_qrcode.png")
