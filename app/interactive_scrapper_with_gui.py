import pandas as pd
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage

# WebDriver settings for Selenium
driver_path = r"path\to\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run the browser in the background
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Using the Service class to start WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Load city and district information from a file
def load_cities_and_districts(file_path):
    cities_and_districts = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            city, districts = line.strip().split(":")
            district_list = [d.strip() for d in districts.split(",")]
            cities_and_districts[city.strip().lower()] = district_list
    return cities_and_districts

# Path to the city and district file
city_district_file = "src/cities_districts.txt"
CITIES_AND_DISTRICTS = load_cities_and_districts(city_district_file)

# Load categories from a file
CATEGORIES = []
with open("src/cleaned_categories.txt", "r", encoding="utf-8") as file:
    CATEGORIES = file.read().splitlines()

# Tkinter application for the GUI
def start_gui():
    def on_submit():
        selected_category = category_var.get()
        selected_city = city_var.get().lower()
        selected_district = district_var.get()

        if not selected_category or not selected_city or not selected_district:
            messagebox.showerror("Error", "Please make all selections.")
            return

        OUTPUT_FILE = f"output/{selected_city}_{selected_district}_{selected_category}.csv"
        all_places = []
        base_url = f"https://www.bulurum.com/dir/{selected_category}/{selected_district}/"
        page = 1

        while True:
            try:
                url = f"{base_url}?page={page}"
                driver.get(url)

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "FreeListingItemBox"))
                )

                soup = BeautifulSoup(driver.page_source, "html.parser")
                free_listings = soup.find_all("div", {"class": "FreeListingItemBox", "itemscope": ""})

                if not free_listings:
                    break

                for listing in free_listings:
                    try:
                        company_name = listing.find("h2", class_="CompanyName")
                        company_name = company_name.get_text(strip=True) if company_name else "No data"

                        address = listing.find("div", class_="FreeListingAddress")
                        address = address.get_text(strip=True) if address else "No data"

                        description = listing.find("div", class_="CompanyDescr")
                        description = description.get_text(strip=True) if description else "No data"

                        phone = listing.find("div", itemprop="telephone")
                        phone = phone.get_text(strip=True) if phone else "No data"

                        email_meta = listing.find("meta", itemprop="email")
                        email = email_meta["content"] if email_meta else "No data"

                        website_meta = listing.find("meta", itemprop="url")
                        website = website_meta["content"] if website_meta else "No data"

                        latitude_meta = listing.find("meta", itemprop="latitude")
                        latitude = latitude_meta["content"] if latitude_meta else "No data"

                        longitude_meta = listing.find("meta", itemprop="longitude")
                        longitude = longitude_meta["content"] if longitude_meta else "No data"

                        all_places.append({
                            "Category": selected_category,
                            "City": selected_city,
                            "District": selected_district,
                            "Company Name": company_name,
                            "Address": address,
                            "Description": description,
                            "Phone": phone,
                            "Email": email,
                            "Website": website,
                            "Latitude": latitude,
                            "Longitude": longitude
                        })
                    except Exception as e:
                        print(f"Error processing a record: {e}")

                page += 1
                time.sleep(1)

            except Exception as e:
                print(f"Error occurred: {e}, URL: {url}")
                break

        driver.quit()

        bulurum_df = pd.DataFrame(all_places)
        os.makedirs("output", exist_ok=True)

        if not bulurum_df.empty:
            bulurum_df.to_csv(OUTPUT_FILE, index=False)
            messagebox.showinfo("Success", f"Data saved: {OUTPUT_FILE}")
        else:
            messagebox.showerror("Error", "No data retrieved.")

    root = tk.Tk()
    root.title("Bulurum Data Scraper")
    root.geometry("600x400")
    root.center = lambda: root.geometry(f"+{root.winfo_screenwidth() // 2 - 300}+{root.winfo_screenheight() // 2 - 200}")
    root.center()
    root.configure(bg="#F5F5F5")
    root.columnconfigure(0, weight=1)
    root.resizable(False, False)

    # Modern design for ttk
    style = ttk.Style()
    style.theme_use("clam")
    
    style.configure("TLabel", font=("Helvetica", 11), foreground="#333333", background="#F5F5F5", padding=10)
    style.configure("TButton", font=("Helvetica", 10, "bold"), foreground="white", background="#007BFF", padding=10)
    style.map("TButton", background=[("active", "#0056b3")], relief=[("pressed", "sunken")])
    style.configure("TCombobox", font=("Helvetica", 10), padding=10)

    # Logo and title section
    try:
        logo = PhotoImage(file="src/logo.png")
        tk.Label(root, image=logo, bg="#F5F5F5").pack(pady=10)
    except Exception:
        tk.Label(root, text="Bulurum Data Scraper", font=("Helvetica", 16, "bold"), bg="#F5F5F5", fg="#333333").pack(pady=10)
        link = tk.Label(root, text="bakbul-muozez", fg="#007BFF", bg="#F5F5F5", cursor="hand2", font=("Helvetica", 10, "italic"))
        link.pack()
        link.bind("<Button-1>", lambda e: os.system("start https://github.com/bakbul-muozez"))

    # Category selection
    ttk.Label(root, text="Select Category:").pack(anchor="center", padx=20)
    category_var = tk.StringVar()
    category_menu = ttk.Combobox(root, textvariable=category_var, values=CATEGORIES, state="readonly")
    category_menu.pack(fill="x", padx=20)

    # City selection
    ttk.Label(root, text="Select City:").pack(anchor="center", padx=20)
    city_var = tk.StringVar()
    city_menu = ttk.Combobox(root, textvariable=city_var, values=list(CITIES_AND_DISTRICTS.keys()), state="readonly")
    city_menu.pack(fill="x", padx=20)

    # District selection
    ttk.Label(root, text="Select District:").pack(anchor="center", padx=20)
    district_var = tk.StringVar()
    district_menu = ttk.Combobox(root, textvariable=district_var, state="readonly")
    district_menu.pack(fill="x", padx=20)

    def update_district_menu(*args):
        city = city_var.get().lower()
        if city in CITIES_AND_DISTRICTS:
            district_menu["values"] = CITIES_AND_DISTRICTS[city]

    city_var.trace("w", update_district_menu)

    # Submit button
    ttk.Button(root, text="Start", command=on_submit).pack(pady=20)

    root.mainloop()

# Start the GUI
start_gui()
