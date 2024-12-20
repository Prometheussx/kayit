

import sqlite3

# Veritabanına bağlan
conn = sqlite3.connect('../google_accounts.db')

# Bir cursor oluştur
cursor = conn.cursor()

# Tüm tabloları listele
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tablolar:")
for table in tables:
    print(table[0])  # Tablo adını yazdır

# Her tablo için verileri görüntüle
for table in tables:
    table_name = table[0]
    print(f"\n{table_name} Tablosundaki Veriler:")

    # Tablo verilerini al
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()

    # Verileri yazdır
    for row in rows:
        print(row)

# Bağlantıyı kapat
conn.close()


"""
import sqlite3

# Veritabanına bağlan
conn = sqlite3.connect('../google_accounts.db')
cursor = conn.cursor()

# Tablo adını belirleyin
table_name = 'accounts'  # Eğer tablo ismini biliyorsanız bunu girin, bilmediğiniz durumda otomatik alınabilir

# Eğer tablo varsa, içindeki tüm verileri sil
cursor.execute(f"DELETE FROM {table_name};")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='accounts';")

data = [
]

# Verileri tabloya ekleyin
for id, email, password, phone_number, proxy, country, region, city, yorum in data:
    cursor.execute(f"INSERT INTO {table_name} (id, email, password, phone_number, proxy, country, region, city, yorum) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", (id, email, password, phone_number, proxy, country, region, city, yorum))

# Veritabanını kaydedin ve bağlantıyı kapatın
conn.commit()
conn.close()

print("Veriler başarıyla eklendi.")
"""