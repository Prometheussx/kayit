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
