import csv
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- CONFIGURATION ---
BMS_URL = "https://in.bookmyshow.com/movies/vijayawada/hari-hara-veera-mallu-part-1-sword-vs-spirit/buytickets/ET00308207/20250724"
CSV_FILE_NAME = 'booking_status_log.csv'

# --- SCRIPT ---
print("Starting the booking status checker...")
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode (no browser window)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(BMS_URL)

try:
    print("Loading page and waiting for main content...")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "synopsis-tab")))
    print("Page loaded successfully.")
    time.sleep(3)

    # --- COUNTING LOGIC ---
    active_shows_list = driver.find_elements(By.CSS_SELECTOR, 'a[class*="__showtime-link"]')
    active_count = len(active_shows_list)
    
    all_shows_list = driver.find_elements(By.CSS_SELECTOR, '.venue-show-listing a')
    total_count = len(all_shows_list)
    
    pending_count = total_count - active_count if total_count > 0 else 0

    # --- SAVE TO CSV ---
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_row = [timestamp, total_count, active_count, pending_count]
    
    file_exists = os.path.isfile(CSV_FILE_NAME)
    with open(CSV_FILE_NAME, mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        if not file_exists:
            writer.writerow(['Timestamp', 'Total Shows', 'Open for Booking', 'Not Yet Open']) # Write header
        writer.writerow(new_row)
    
    print(f"Successfully saved data to {CSV_FILE_NAME}")

except Exception as e:
    print(f"--- An Error Occurred --- \n{e}")

finally:
    print("\nScript finished. Closing browser.")
    driver.quit()
