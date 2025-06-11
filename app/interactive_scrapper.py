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
driver_path = r"C:\Users\muozez\Desktop\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run the browser in the background
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-webgl")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--disable-extensions")
options.add_argument("--disable-dev-shm-usage")

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

# Target category
TARGET_CATEGORY = "guzellik-salonu"

# Create output directory
os.makedirs("output", exist_ok=True)

# Use Selenium and BeautifulSoup to collect data
def scrape_city_district_data(city, district, category):
    all_places = []
    base_url = f"https://www.bulurum.com/dir/{category}/{district}/"
    page = 1

    while True:
        try:
            url = f"{base_url}?page={page}"
            driver.get(url)

            # Wait for the page to fully load
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "FreeListingItemBox"))
                )
            except Exception as e:
                print(f"Timeout or no data found for {city}-{district}, Page {page}: {e}")
                break

            # Get the page source and process it with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")
            free_listings = soup.find_all("div", {"class": "FreeListingItemBox", "itemscope": ""})

            if not free_listings:
                print(f"No more data found for {city}-{district}, Page {page}. Ending.")
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
                        "Category": category,
                        "City": city,
                        "District": district,
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

    return all_places

# Main loop to iterate through cities and districts
try:
    for city, districts in CITIES_AND_DISTRICTS.items():
        city_data = []
        for district in districts:
            print(f"Scraping data for {city} - {district}")
            district_data = scrape_city_district_data(city, district, TARGET_CATEGORY)
            city_data.extend(district_data)

        # Convert data to DataFrame
        city_df = pd.DataFrame(city_data)

        # Save to CSV if data is available
        if not city_df.empty:
            output_file = f"output/{city}_beauty_salons.csv"
            city_df.to_csv(output_file, index=False)
            print(f"Data successfully saved to: {output_file}")
        else:
            print(f"No data found for {city}. Skipping.")

except KeyboardInterrupt:
    print("Process interrupted. Saving progress...")
finally:
    driver.quit()

print("Data scraping completed.")
