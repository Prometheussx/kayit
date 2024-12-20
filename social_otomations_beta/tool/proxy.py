import requests
from concurrent.futures import ThreadPoolExecutor
import random

# Proxy listesi
proxies = [
    "http://erdemtahasokullu_gmail_com-country-us-sid-abkp0lrmwhcb8u13-filter-medium:76wnsorw9g@gate.nodemaven.com:8080",
    "http://erdemtahasokullu_gmail_com-country-us-sid-zhwwsdti23xppa-filter-medium:76wnsorw9g@gate.nodemaven.com:8080",
    # Daha fazla proxy burada
]

# Proxy test fonksiyonu
def test_proxy(proxy, test_count=5):
    success_count = 0
    for _ in range(test_count):
        try:
            proxy_dict = {"http": proxy, "https": proxy}
            response = requests.get("https://httpbin.org/ip", proxies=proxy_dict, timeout=5)
            if response.status_code == 200:
                success_count += 1
        except:
            pass
    # Güvenilirlik yüzdesini hesapla
    reliability = (success_count / test_count) * 100
    return proxy, reliability

# Proxy testlerini paralel olarak çalıştır
def check_proxies_with_reliability(proxy_list, test_count=5):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda p: test_proxy(p, test_count), proxy_list))
    return results

# Proxyleri test et
test_count = 5  # Her proxy 5 kez test edilecek
results = check_proxies_with_reliability(proxies, test_count)

# Sonuçları yazdır
for proxy, reliability in results:
    print(f"Proxy: {proxy}")
    print(f"Güvenilirlik: %{reliability:.2f}")
    print("-" * 50)
