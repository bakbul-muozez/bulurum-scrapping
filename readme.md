# Bulurum.com Data Scrapping

A versatile tool to scrape data from bulurum.com based on selected districts and categories. This tool provides both a Command-Line Interface (CLI) and a Graphical User Interface (GUI) for flexibility, allowing users to extract structured data efficiently.

## Description

This project offers two versions:

1. **CLI Version:**
   A Python-based Selenium web scraper that allows users to input specific districts and categories through prompts. It automates data extraction from bulurum.com using Selenium and BeautifulSoup.

2. **GUI Version:**
   An interactive GUI version built with Tkinter for non-technical users. It provides dropdown menus for category, city, and district selection, making the scraping process accessible to everyone.

Both versions save the scraped data in a structured CSV format for further analysis or use.

## Getting Started

### Dependencies

* Python 3.8 or higher
* Selenium WebDriver
* Google Chrome (latest version)
* ChromeDriver (compatible with your Chrome version)
* Tkinter (for GUI version)
* OS: Windows 10, macOS, or Linux

### Installing

1. Clone the repository:
    ```bash
    git clone https://github.com/bakbul-muozez/bulurum-scrapping.git
    ```

2. Navigate to the project directory:
    ```bash
    cd bulurum-scrapping
    ```

3. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

4. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Download the ChromeDriver that matches your Chrome version and place it in the project directory.

6. Ensure source files `src/cities_districts.txt` and `src/cleaned_categories.txt` are properly formatted and available.

### Executing the Program

#### CLI Version

1. Run the `interactive_scrapper.py` script:
    ```bash
    python interactive_scrapper.py
    ```

2. Follow the on-screen prompts to select the category, city, and district.

3. The scraped data will be saved in the `output` folder as a CSV file.

#### GUI Version

1. Run the `interactive_scrapper_with_gui.py` script:
    ```bash
    python interactive_scrapper_with_gui.py
    ```

2. Select the category, city, and district from the dropdown menus in the GUI.

3. Click the **"Başlat"** button to begin scraping.

4. The scraped data will be saved in the `output` folder as a CSV file.

## Outputs

The scraped data includes the following fields:

* Category
* City
* District
* Company Name
* Address
* Description
* Phone
* Email
* Website
* Latitude
* Longitude

The data is saved in CSV format for easy analysis.

## Help

Common issues and their solutions:

* **Error: "chromedriver" executable needs to be in PATH.**
    * Ensure ChromeDriver is in the project directory or added to your PATH.

* **Error: "Element not found" or "TimeoutException."**
    * Verify the structure of bulurum.com has not changed.
    * Increase the `timeout` parameter in the script if the page loads slowly.

For additional help with the CLI version:
```bash
python interactive_scrapper.py --help
```

## Authors

* Muhammet Yilmaz  
  [LinkedIn](https://www.linkedin.com/in/muhammet-yilmaz-anka/)  
  [GitHub](https://github.com/bakbul-muozez)

## Version History

* 0.2
    * Added GUI version with Tkinter
    * Improved error handling
    * Optimized scraping logic for speed
    * See [commit change](https://github.com/bakbul-muozez/bulurum-scrapping/commits/main)

* 0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.



