import random
from humancursor.system_cursor import SystemCursor

cursor = SystemCursor()  # Initializing SystemCursor object


# Hareketlerin rastgele koordinatlarını belirliyoruz
def generate_random_move():
    # x ve y için rastgele değerler oluşturuyoruz
    x = random.randint(158, 1593)  # x koordinatı 100 ile 1500 arasında
    y = random.randint(117, 1273)  # y koordinatı 100 ile 1500 arasında
    return [x, y]


# Hareketleri başlatan fonksiyon
def human_like_click(x,y):
    print('Initializing System Demo')

    # Her hareket için, 3 rastgele seçim yapıp çalıştıracağız
    for _ in range(1):  # 50 hareket yapacağız
        # 3 farklı rastgele hareket seç
        random_moves = [generate_random_move() for i in range(random.randint(1,5))]

        # Seçilen 3 hareketi sırayla gerçekleştir
        for move in random_moves:
            print(move)
            cursor.move_to(move)

        # Son olarak kullanıcı hareketini gerçekleştir
        # Burada, örneğin hedef olarak [500, 700] konumunu alalım
          # Örnek kullanıcı hareketi
        cursor.move_to([x,y])

    print('System Demo ended')


# Demo'yu başlat
human_like_click(500,500)
