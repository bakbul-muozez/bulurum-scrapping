import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Kategoriler ve şehir-ilçe bilgileri
CATEGORIES = [
    "guzellik-salonlari-ve-merkezleri",
    "plastik-cerrahi",
    "bayan-kuaforleri",
    "erkek-kuaforleri",
    "dovme-piercing-ve-ekipmanlari"
]

CITIES_AND_DISTRICTS = {
    "bursa": ["nilufer", "osmangazi", "yildirim"],
    "istanbul": [
        "kadikoy", "besiktas", "uskudar", "sariyer", "fatih", "sisli", "beyoglu",
        "ataşehir", "kartal", "pendik", "maltepe", "bahcelievler", "bagcilar"
    ]
}

# Çıktı dosyasının adı
OUTPUT_FILE = "output/bulurum_combined_data.csv"

# Verileri toplamak için liste
all_places = []

# Tüm şehir ve kategorilerde veri çekme
for city, districts in CITIES_AND_DISTRICTS.items():
    for district in districts:
        for category in CATEGORIES:
            base_url = f"https://www.bulurum.com/dir/{category}/{district}/"
            page = 1
            
            print(f"Şehir: {city}, İlçe: {district}, Kategori: {category} -> Veri çekiliyor...")
            
            while True:
                response = requests.get(f"{base_url}?page={page}", verify=False)  # SSL doğrulamasını atladık
                if response.status_code != 200:
                    print(f"Sayfa yüklenemedi: {base_url}?page={page}")
                    break

                soup = BeautifulSoup(response.text, "html.parser")
                free_listings = soup.find_all("div", {"data-type": "FreeListing"})

                if not free_listings:
                    print(f"Tüm veriler toplandı: {base_url}")
                    break

                for listing in free_listings:
                    spans = [span.get_text(strip=True) for span in listing.find_all("span")]
                    divs = [div.get_text(strip=True) for div in listing.find_all("div")]

                    all_places.append({
                        "Şehir": city,
                        "İlçe": district,
                        "Kategori": category,
                        "Spans": " | ".join(spans),
                        "Divs": " | ".join(divs),
                    })

                page += 1

# Verileri DataFrame'e dönüştür
bulurum_df = pd.DataFrame(all_places)

# Çıktı klasörü oluştur
os.makedirs("output", exist_ok=True)

# CSV dosyasına yaz
bulurum_df.to_csv(OUTPUT_FILE, index=False)
print(f"Veriler başarıyla CSV dosyasına kaydedildi: {OUTPUT_FILE}")
