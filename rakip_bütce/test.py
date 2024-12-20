import sqlite3
import pandas as pd
import random
import time
import pyautogui
from playwright.sync_api import sync_playwright
import traceback
import re
import math


def load_safe_websites():
    """Load safe websites from the CSV file into a list."""
    safe_websites_df = pd.read_csv('data/safe_website.csv')
    return safe_websites_df['website'].tolist()
def load_proxies():
    """Load proxy data from CSV file into a list."""
    proxy_data_df = pd.read_csv('data/proxy_data.csv')
    return proxy_data_df.to_dict(orient='records')

def is_safe_website(website, safe_websites):
    """Check if the website is in the list of safe websites."""
    return website in safe_websites
def circular_motion(x, y, steps=random.randint(10, 20)):
    """Geniş dairesel hareket"""
    start_x, start_y = pyautogui.position()
    radius = math.hypot(x - start_x, y - start_y) / 2
    angle = 0
    for i in range(steps):
        angle += math.pi / steps + random.uniform(-0.2, 0.2)
        offset_x = int(radius * math.cos(angle))
        offset_y = int(radius * math.sin(angle))
        pyautogui.moveTo(start_x + offset_x, start_y + offset_y)


def zigzag_motion(x, y, steps=random.randint(10, 20)):
    """Geniş zikzak hareket"""
    start_x, start_y = pyautogui.position()
    for i in range(steps):
        offset_x = int((x - start_x) * (i + 1) / steps)
        offset_y = int((y - start_y) * (i + 1) / steps + random.choice([-30, 50]))
        pyautogui.moveTo(start_x + offset_x, start_y + offset_y)


def spiral_motion(x, y, steps=random.randint(10, 20)):
    """Geniş spiral hareket"""
    start_x, start_y = pyautogui.position()
    radius = math.hypot(x - start_x, y - start_y) / 2
    angle = 0
    for i in range(steps):
        angle += math.pi / steps
        offset_radius = radius * (1 - i / steps)
        offset_x = int(offset_radius * math.cos(angle))
        offset_y = int(offset_radius * math.sin(angle))
        pyautogui.moveTo(start_x + offset_x, start_y + offset_y)


def shake_motion(x, y, steps=random.randint(10, 20)):
    """Daha geniş sarsıntılı hareket"""
    start_x, start_y = pyautogui.position()
    for i in range(steps):
        offset_x = int((x - start_x) * (i + 1) / steps) + random.randint(-20, 40)
        offset_y = int((y - start_y) * (i + 1) / steps) + random.randint(-20, 40)
        pyautogui.moveTo(start_x + offset_x, start_y + offset_y)


def wavy_motion(x, y, steps=random.randint(10, 20)):
    """Geniş dalgalı hareket"""
    start_x, start_y = pyautogui.position()
    frequency = 3
    for i in range(steps):
        offset_x = int((x - start_x) * (i + 1) / steps)
        offset_y = int((y - start_y) * (i + 1) / steps + math.sin(i * frequency) * 30)
        pyautogui.moveTo(start_x + offset_x, start_y + offset_y)


def jitter_motion(x, y, steps=random.randint(10, 20)):
    """Daha büyük rastgele sapmalı hareket"""
    start_x, start_y = pyautogui.position()
    for i in range(steps):
        offset_x = int((x - start_x) * (i + 1) / steps) + random.randint(-10, 30)
        offset_y = int((y - start_y) * (i + 1) / steps) + random.randint(-10, 30)
        pyautogui.moveTo(start_x + offset_x, start_y + offset_y)


def sin_wave_motion(x, y, steps=random.randint(10, 20)):
    """Daha geniş sinüs dalgası hareketi"""
    start_x, start_y = pyautogui.position()
    amplitude = 20
    frequency = math.pi / 5
    for i in range(steps):
        offset_x = int((x - start_x) * (i + 1) / steps)
        offset_y = int((y - start_y) * (i + 1) / steps + amplitude * math.sin(i * frequency))
        pyautogui.moveTo(start_x + offset_x, start_y + offset_y)


def curve_motion(x, y, steps=random.randint(10, 20)):
    """Daha belirgin kavisli hareket"""
    start_x, start_y = pyautogui.position()
    control_x = (start_x + x) / 2 + random.randint(-80, 100)
    control_y = (start_y + y) / 2 + random.randint(-80, 100)
    for i in range(steps):
        t = i / steps
        offset_x = int((1 - t)**2 * start_x + 2 * (1 - t) * t * control_x + t**2 * x)
        offset_y = int((1 - t)**2 * start_y + 2 * (1 - t) * t * control_y + t**2 * y)
        pyautogui.moveTo(offset_x, offset_y)


def random_walk_motion(x, y, steps=random.randint(10, 20)):
    """Daha geniş rastgele adımlarla hareket"""
    current_x, current_y = pyautogui.position()
    for _ in range(steps):
        current_x += random.randint(-20, 40)
        current_y += random.randint(-20, 40)
        pyautogui.moveTo(current_x, current_y)


def bounce_motion(x, y, steps=random.randint(10, 20)):
    """Daha yüksek zıplama benzeri hareket"""
    start_x, start_y = pyautogui.position()
    for i in range(steps):
        offset_x = int((x - start_x) * (i + 1) / steps)
        offset_y = int((y - start_y) * (i + 1) / steps + abs(math.sin(i)) * 40)
        pyautogui.moveTo(start_x + offset_x, start_y + offset_y)


def smooth_human_like_move(x, y, steps=random.randint(2, 8)):
    start_x, start_y = pyautogui.position()  # Mevcut fare konumu
    delta_x = (x - start_x) / steps


    for i in range(steps):
        # Ara hedef konum hesaplama
        move_x = start_x + delta_x * i + random.uniform(-2, 2)  # Sağ-sol sapmaları

        pyautogui.moveTo(move_x, y)
def human_like_click(x, y):
    movements = [
        circular_motion, zigzag_motion, spiral_motion, shake_motion,
        wavy_motion, jitter_motion, sin_wave_motion, curve_motion,
        random_walk_motion, bounce_motion
    ]

    # 3 farklı rastgele hareketi seç ve sırayla uygula
    selected_movements = random.choices(movements, k=5)
    for move in selected_movements:
        # Her hareket için rastgele koordinatlar belirle
        rand_x = random.randint(83, 1254)
        rand_y = random.randint(268, 987)
        print(rand_x,rand_y)
        move(rand_x, rand_y)

    # Son olarak hedef konuma gidip tıklayın
    bounce_motion(x, y)
    rand_x = x + random.randint(-25, 50)
    rand_y = y + random.randint(-10, 10)
    smooth_human_like_move(rand_x, rand_y)
    pyautogui.click()

def inputs():
    search = input("Aranacak Anahtar Cümleyi Seçin: ")
    tour_count = int(input("Kaç Tur Çalışacağını Seçin: "))
    return search, tour_count


def configure_proxy(proxy):
    """Configure Playwright proxy."""
    return {
        "server": f"http://{proxy['ip']}:{proxy['port']}",
        "username": proxy.get('username'),
        "password": proxy.get('password')
    }

proxy_df = pd.read_csv('data/proxy_data.csv')

# Otomatik doldurulacak veriler
form_data = {
    "name": "John Doe",
    "email": "johndoe@example.com",
    "phone": "+1234567890"
}


def fill_form(page):
    """Sayfa üzerinde formu otomatik olarak doldurur."""
    try:
        # Form elemanlarını doldur
        page.fill('[name="namesurname"], [name="name"], [id="name"], [name="your-name"]', form_data["name"])
    except Exception:
        print("Ad ve soyad alanı bulunamadı veya doldurulamadı.")

    try:
        page.fill('[id="email"], [name="mail"], [name="email"], [name="your-email"]', form_data["email"])
    except Exception:
        print("E-posta alanı bulunamadı veya doldurulamadı.")

    try:
        page.fill('[id="phone"], [name="phone"], [name="phonetext-949"]', form_data["phone"])
    except Exception:
        print("Telefon numarası alanı bulunamadı veya doldurulamadı.")



def main():
    # Load safe websites and proxy data
    safe_websites = load_safe_websites()
    proxies = load_proxies()

    search, tour_count = inputs()

    for index, row in proxy_df.iterrows():
        proxy = row['proxy']
        country = row['country']
        region = row['region']
        city = row['city']
        a, b, c, d = proxy.split(':')[:4]
        a = f"{a}:{b}"

        with sync_playwright() as p:
            try:
                # Start the browser with the proxy settings
                browser = p.chromium.launch(headless=False)
                context = browser.new_context(proxy={"server": f"{a}", "username": f"{c}", "password": f"{d}"})
                page = context.new_page()

                # Perform actions
                page.goto("https://www.google.com")
                time.sleep(2)
                pyautogui.hotkey('alt', 'space')
                time.sleep(1)
                pyautogui.press("down", presses=5, interval=0.8)
                time.sleep(1)
                pyautogui.press("enter", presses=3, interval=0.8)

                human_like_click(x=550, y=450)
                time.sleep(2)
                pyautogui.write(search, interval=0.2)
                pyautogui.press('enter')
                time.sleep(10)

                # Handle search results
                for j in [0, 3]:
                    for i in range(1, 5):
                        try:
                            element = page.locator(f'[data-ta-slot="{j}"][data-ta-slot-pos="{i}"] .v5yQqb a')
                            data_dtld_element = page.locator(f'[data-ta-slot="{j}"][data-ta-slot-pos="{i}"] span[data-dtld]').nth(0)
                            data_dtld = data_dtld_element.get_attribute('data-dtld') if data_dtld_element else None

                            if data_dtld:
                                print(f'{i}. sıradaki linkin data-dtld değeri: {data_dtld}')
                                if is_safe_website(data_dtld, safe_websites):
                                    print(f'{i}. sıradaki link güvenli site: {data_dtld}. Tıklanmayacak.')
                                    continue
                                href = element.get_attribute('href')
                                if href and href.startswith('https'):
                                    print(f'{i}. sıradaki link açılıyor: {href}')
                                    page.evaluate(f"window.open('{href}', '_blank');")
                                    fill_form(page)
                                else:
                                    print(f'{i}. sıradaki geçersiz veya hatalı link: {href}')
                            else:
                                print(f'{i}. sıradaki linkte data-dtld değeri bulunamadı.')

                            time.sleep(20)
                        except Exception as e:
                            print(f"Error in handling search result {i}: {e}")
                            traceback.print_exc()
            except Exception as e:
                print(f"An error occurred while setting up the browser: {e}")
                traceback.print_exc()



            finally:
                browser.close()


if __name__ == "__main__":
    main()