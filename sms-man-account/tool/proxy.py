import pandas as pd
from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

# Proxy dosyasını oku (data.csv dosyasını id ve proxy sütunları ile okuyoruz)
proxy_df = pd.read_csv('../data/proxy_data.csv')

# Set up Chrome options
opts = Options()

# Add user-agent if needed
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
opts.add_argument(f"user-agent={user_agent}")

# Her proxy için işlemi gerçekleştir
for index, row in proxy_df.iterrows():
    PROXY = row['proxy']  # Proxy sütunundaki proxy'yi alıyoruz

    # Set up Selenium Wire with proxy settings
    seleniumwire_options = {
        'proxy': {
            'http': PROXY,
            'https': PROXY,
            'no_proxy': 'localhost,127.0.0.1'  # Bypass proxy for these addresses
        }
    }

    # Initialize the Chrome driver with Selenium Wire and proxy settings
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts,
                              seleniumwire_options=seleniumwire_options)

    try:
        # Access test sites
        driver.get("https://wrong.host.badssl.com/")
        driver.get('https://www.expressvpn.com/what-is-my-ip')

        # Check the user agent
        user_agent_check = driver.execute_script("return navigator.userAgent;")
        print(f"Proxy: {PROXY} - User Agent: {user_agent_check}")

        # İşlemi tamamlamak için bekle
        time.sleep(10)
    except Exception as e:
        print(f"Error with proxy {PROXY}: {e}")
    time.sleep(2000)    
    finally:
        driver.quit()  # Tarayıcıyı kapat

    # Bir sonraki proxy'ye geçmeden önce kısa bir bekleme süresi koyabilirsiniz

