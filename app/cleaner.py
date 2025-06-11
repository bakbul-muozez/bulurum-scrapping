import pandas as pd

# CSV dosyasını okuma
file_path = "bulurum_selenium_data.csv"  # Dosyanın yolunu buraya yazın
data = pd.read_csv(file_path)

# Eksik verileri "Yok" olarak doldurma
data = data.fillna("Yok")

# Sütun adlarını daha okunaklı hale getirme
data.columns = [
    "Kategori", "Şehir", "İlçe", "Firma Adı", "Adres", 
    "Açıklama", "Telefon", "E-posta", "Web Sitesi", "Enlem", "Boylam"
]

# Verileri okunaklı hale getirme
data["Kategori"] = data["Kategori"].str.title()
data["Şehir"] = data["Şehir"].str.title()
data["İlçe"] = data["İlçe"].str.title()
data["Firma Adı"] = data["Firma Adı"].str.title()
data["Adres"] = data["Adres"].str.title()
data["Açıklama"] = data["Açıklama"].apply(lambda x: x.title() if x != "Yok" else "Yok")
data["E-posta"] = data["E-posta"].apply(lambda x: x.lower() if x != "Yok" else "Yok")
data["Web Sitesi"] = data["Web Sitesi"].apply(lambda x: x.lower() if x != "Yok" else "Yok")

# Kategorilere göre verileri ayırma ve kaydetme
for kategori, group in data.groupby("Kategori"):
    output_file = f"{kategori.lower().replace(' ', '_')}_veri.csv"
    group.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"'{kategori}' kategorisindeki veri '{output_file}' olarak kaydedildi.")
