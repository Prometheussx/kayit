

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
(1, 'Carlos.Mendoza.za800', 'estetik310_ist', '4247038825', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-fwj5g6x4iyn8-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', "Had a GREAT hair transplant experience at the clinic. 0 Pain, friendly staff, and a Comfortable experience threw out my whole procedure.\nDr. B work is the BEST. Couldn't ask for more. Results speak themself. Thanks everyone!"),
(2, 'Emma.Bergstrom.om899', 'estetik984_ist', '8603181195', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-ifuu7vayudt4o9ba-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', 'My experience was outstanding. Having videos and testimonials provided to me prior to the surgery helped and was shocked how it all went according to plan. I was treated like royalty from the minute I arrived till the time I left the hospital. The surgery was painless and Dr B is awesome. Having a real Dr. providing the surgery was comforting. A strong shout out to his staff as well. They could not have been nicer. I would strongly recommend this hospital and look forward to my recovery.'),
(3, 'Anna.Schafer.er983', 'estetik931_ist', '8187918105', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-zwj06nph-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', 'I flew from Berlin to Istanbul specifically for my breast lifting procedure. The clinic took care of everything, including transportation and accommodation. The surgery was a smooth process, and I was surprised at how little discomfort I felt afterward. In just 10 days, I was back to my regular activities, and within a month, I could hit the gym again. I truly felt like I was in the hands of experts. Thank you, Estetik International, for bringing my confidence back!'),
]

# Verileri tabloya ekleyin
for id, email, password, phone_number, proxy, country, region, city, yorum in data:
    cursor.execute(f"INSERT INTO {table_name} (id, email, password, phone_number, proxy, country, region, city, yorum) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", (id, email, password, phone_number, proxy, country, region, city, yorum))

# Veritabanını kaydedin ve bağlantıyı kapatın
conn.commit()
conn.close()

print("Veriler başarıyla eklendi.")
"""


"""
accounts Tablosundaki Veriler:
(1, 'Carlos.Mendoza.za800', 'estetik310_ist', '4247038825', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-fwj5g6x4iyn8-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', "Had a GREAT hair transplant experience at the clinic. 0 Pain, friendly staff, and a Comfortable experience threw out my whole procedure.\nDr. B work is the BEST. Couldn't ask for more. Results speak themself. Thanks everyone!\n\n")
(2, 'Emma.Bergstrom.om899', 'estetik984_ist', '8603181195', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-ifuu7vayudt4o9ba-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', 'My experience was outstanding. Having videos and testimonials provided to me prior to the surgery helped and was shocked how it all went according to plan. I was treated like royalty from the minute I arrived till the time I left the hospital. The surgery was painless and Dr B is awesome. Having a real Dr. providing the surgery was comforting. A strong shout out to his staff as well. They could not have been nicer. I would strongly recommend this hospital and look forward to my recovery.')
(3, 'Anna.Schafer.er983', 'estetik931_ist', '8187918105', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-zwj06nph-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', 'I flew from Berlin to Istanbul specifically for my breast lifting procedure. The clinic took care of everything, including transportation and accommodation. The surgery was a smooth process, and I was surprised at how little discomfort I felt afterward. In just 10 days, I was back to my regular activities, and within a month, I could hit the gym again. I truly felt like I was in the hands of experts. Thank you, Estetik International, for bringing my confidence back!')
(4, 'Sophia.Rossi.si286', 'estetik814_ist', '5123751873', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-i9vimavk7x780k-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', 'After years of hesitation, I finally do a breast lift at Estetik International. From the first consultation to the post-surgery care, everything was much easy. The team made me feel comfortable and listened all my questions. The results were more my expectations – natural, firm, and beautiful lifting! just two weeks, I was back work feeling most confident than ever. The clinic’s hospitality and attention to detail were wow. I very recommend it to anyone thinking this life-changing procedure.')
(5, 'Chloe.Dubois.ois901', 'estetik354_ist', '9852531200', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-3posgw0x-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', "Estetik International total body shaping procedure has transformed my life. After losing kg, I need contouring to feel confident. The clinic's advanced techniques incredible, and the staff with me like family. Swelling go quickly, and I to return to work in 14 days. I can now wear clothes I want, and it’s thanks to this amazing team.")
(6, 'Sofia.Kovacic.c409', 'estetik641_ist', '6624005510', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-mpyhkmjd-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', 'I’m beyond thrilled with my total body shaping results at Estetik International! The surgeons were artists, sculpting my body to perfection. I felt no pressure during consultations and had all my questions answered in detail. The recovery was much faster than I imagined – I was back to light yoga in three weeks. Istanbul was beautiful, and the clinic made sure I had a luxurious and comfortable stay.')
(7, 'Hugo.Silva.a288', 'estetik449_ist', '7732092464', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-wdsyt3qhiazk4ve-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', 'My liposuction experience at Estetik International wonderful. The team tell me every step of the process and made me feel safe and comfortable. Recovery was so quick. I back to my daily routine in a week! The results are perfect; I feel sculpted and beautiful. Plus, Istanbul is a fantastic city to recover!')
(8, 'Jamal.Abdullah.h699', 'estetik196_ist', '6502090590', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-vie2i1dadr-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', "I traveled to Istanbul for liposuction at Estetik International, the best decision of my life. The level of care I get so good. I don't believe how fast I healed. I was back work in 10 days. The clinic feels like a luxury retreat, and the staff is great. The results speak themselves;I never felt this confident ago!")
(9, 'Ryan.Smith.th512', 'estetik287_ist', '2242219574', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-0zvy9hgg3an1xdy5fh-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', 'Estetik International is hands down the best clinic for rhinoplasty. My nose now looks natural and perfectly suits my face. The recovery was easier than I anticipated, and I was back to my normal life in just two weeks. The clinic’s facilities were top-notch, and the team was incredibly supportive. I recommend them to anyone considering rhinoplasty.')
(10, 'Leila.Haddad.dad303', 'estetik488_ist', '2817304570', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-bksdkq9v3qoshj-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', 'Traveling to Estetik International for rhinoplasty was the best decision ever. The team’s professionalism and care were unmatched. I loved how natural my nose looks now. Recovery was smooth – I returned to my daily activities in just 10 days. Istanbul is a beautiful city, and the clinic ensured my trip was stress-free and comfortable. Highly recommended!')
(11, 'Mohammed.Khan.han389', 'estetik362_ist', '4026090915', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-yscupeodqo8fw-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', 'I do a Sapphire Hair Transplant at Estetik International, and the result incredible. The procedure no pain, and staff tell every step. I return my office job in five days! My hair is now growing beautifully, and I’m so so happy for the amazing care I get.')
(12, 'Liam.Connor.r803', 'estetik637_ist', '2057536251', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-fhwmhhqiwinil7mj3mq-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', 'Estetik International’s Sapphire Hair Transplant exceeded all my expectations. The staff was professional and kind, and the clinic felt like a luxury spa. I healed so fast that I resumed light activities in just a few days. My hairline looks completely natural, and I couldn’t have asked for better results.')
(13, 'Fatima.Farsi.i918', 'estetik797_ist', '4172982269', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-rg1lq8foekbmursjrxv-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', 'I was looking for a clinic that could provide privacy and excellent care for my intimate concerns, and Estetik International delivered. The procedure was discreet, and the results are truly life-changing. Within days, I felt more comfortable and confident in my body. The clinic ensured I was well taken care of, making the entire experience feel luxurious.')
(14, 'Olga.Ivanova.va755', 'estetik949_ist', '3072005082', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-jtcdrrnunl03a1ddj-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', 'I fly Istanbul for vaginal tightening at Estetik International, and I couldn’t be happier with the results. The staff very understanding and make me comfy during all process. The healing time was minimal. I am back my active lifestyle in a week. It was a changing experience, and I very very recommend this clinic to all need this procedure.')
(15, 'Aisha.Abdi.di436', 'estetik522_ist', '8583089125', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-wlv4qnuy46kxvwriix-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', 'After having two kids, I decided to treat myself to a mommy makeover at Estetik International. The results are stunning – I have my pre-baby body back! The team was so supportive, addressing all my concerns before and after surgery. Within three weeks, I was back to chasing after my kids, feeling more confident and happy. This clinic truly works miracles!')
(16, 'Nia.Dlamini.i757', 'estetik858_ist', '5204098875', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-u6b3axurxnkb-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', 'The mommy makeover procedure at Estetik International was an incredible experience. I had a tummy tuck, breast lift, and liposuction all in one go, and the recovery was faster than I imagined. The clinic provided top-notch care, ensuring I was comfortable at every step. In just four weeks, I felt like a new woman – more energetic and confident than ever. Highly recommend this to all moms!')
(17, 'Katarina.Novak.vak240', 'estetik314_ist', '5125930819', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-0ucuup876s1gjf-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', 'I want Estetik International for a mommy makeover because their outstanding reputation, and they no disappoint. The surgeons skilled, and the staff so kind. I couldn’t believe how fast I recover, I was back at work in less a month, feeling better than ever. Istanbul perfect place for recovery holiday. Thank you for helping me!')
(18, 'Anastasia.Petrova.a218', 'estetik235_ist', '5863514278', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-u4gdmhbye0a-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', 'I heard about the Spider Web Aesthetic technique and traveled to Estetik International specifically for this procedure. I wanted a natural lift without invasive surgery, and the results are stunning! My face looks rejuvenated, and I feel years younger. The procedure was quick, and I was back to my routine the next day. The care and attention I received were incredible – this clinic truly sets the standard for excellence!')
(19, 'Aya.Tanaka.a400', 'estetik195_ist', '8652362905', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-5irc4xiyrwku-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', 'The Spider Web Aesthetic at Estetik International is a game-changer. The non-invasive nature of the procedure and the expertise of the team gave me immediate confidence. My skin feels firmer and smoother, and I’m thrilled with the natural look. The recovery was so fast – I went sightseeing in Istanbul the very next day. I highly recommend this technique for anyone looking for a subtle but effective lift.')
(20, 'Zara.Hussain.n304', 'estetik650_ist', '9093542365', 'gate.nodemaven.com:8080:erdemtahasokullu_gmail_com-country-ca-region-quebec-city-lasalle-sid-erkvaqgzny-filter-medium:76wnsorw9g', 'deneme', 'deneme', 'deneme', 'I have eyelid surgery at Estetik International to remove droopy lids effect my see and confidence. The surgeons is incredibly skilled, and the results are life-changing. my eyes look youthful, and refreshing. Recovery so smooth; I was back activities a week. The team’s professionalism and care do this experience perfect!')

"""