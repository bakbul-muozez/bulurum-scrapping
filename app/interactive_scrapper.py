import pandas as pd
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# WebDriver settings for Selenium
driver_path = r"path\to\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run the browser in the background
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Use Service class to start WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Load city and district data from file
def load_cities_and_districts(file_path):
    cities_and_districts = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            city, districts = line.strip().split(":")
            district_list = [d.strip() for d in districts.split(",")]
            cities_and_districts[city.strip().lower()] = district_list
    return cities_and_districts

# Load city-district data from file
city_district_file = "src/cities_districts.txt"  # File path
CITIES_AND_DISTRICTS = load_cities_and_districts(city_district_file)

# Load categories from a file
CATEGORIES = []
with open("src/cleaned_categories.txt", "r", encoding="utf-8") as file:
    CATEGORIES = file.read().splitlines()

# Settings for page size
PAGE_SIZE = 30

# Provide step-by-step selection to the user
def select_from_list(items, prompt):
    current_page = 0
    while True:
        start_index = current_page * PAGE_SIZE
        end_index = start_index + PAGE_SIZE
        selected_items = items[start_index:end_index]

        print(f"\n{prompt} (Page {current_page + 1}/{(len(items) - 1) // PAGE_SIZE + 1}):")
        for idx, item in enumerate(selected_items, start=1):
            print(f"{idx}. {item}")
        print("0. Next")
        print("-1. Previous")

        try:
            choice = int(input("Make your selection: "))
            if choice == 0 and end_index < len(items):
                current_page += 1
            elif choice == -1 and current_page > 0:
                current_page -= 1
            elif 1 <= choice <= len(selected_items):
                return selected_items[choice - 1]
        except ValueError:
            print("Please make a valid selection.")

# Step 1: Select category
print("Categories")
selected_category = select_from_list(CATEGORIES, "Select a category")

# Step 2: Select city
print("Cities")
selected_city = select_from_list(list(CITIES_AND_DISTRICTS.keys()), "Select a city")

# Step 3: Select district
print("Districts")
selected_district = select_from_list(CITIES_AND_DISTRICTS[selected_city], "Select a district")

# Output file name
OUTPUT_FILE = f"output/{selected_city}_{selected_district}_{selected_category}.csv"

# Use Selenium and BeautifulSoup to collect data
all_places = []
base_url = f"https://www.bulurum.com/dir/{selected_category}/{selected_district}/"
page = 1

while True:
    try:
        url = f"{base_url}?page={page}"
        driver.get(url)

        # Wait for the page to fully load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "FreeListingItemBox"))
        )

        # Get the page source and process it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        free_listings = soup.find_all("div", {"class": "FreeListingItemBox", "itemscope": ""})

        if not free_listings:
            print(f"Empty data or last page: {url}")
            break

        # Process and add data to the list
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
        time.sleep(1)  # Wait to avoid overloading the server

    except Exception as e:
        print(f"Error occurred: {e}, URL: {url}")
        break

# Close WebDriver
driver.quit()

# Convert data to DataFrame
bulurum_df = pd.DataFrame(all_places)

# Create output directory
os.makedirs("output", exist_ok=True)

# Write to CSV file
if not bulurum_df.empty:
    bulurum_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Data successfully saved to CSV file: {OUTPUT_FILE}")
else:
    print("No data retrieved. Output file not created.")
