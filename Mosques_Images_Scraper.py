import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from urllib.parse import urlparse, urljoin
import requests

counter = 0

try:
    # Set up ChromeDriver
    chrome_driver_path = "chromedriver.exe"
    chrome_service = ChromeService(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=chrome_service)

    # Folder to save images
    folder_path = 'Mosques_Images/Prophet_Mosque'
    os.makedirs(folder_path, exist_ok=True)

    # CSV file setup
    csv_filename = "Prophet_Mosque_Images_Data.csv"
    csv_fields = ["ID", "Image Name", "Image URL"]

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_fields)
        writer.writeheader()

        # Iterate over pages
        for i in range(1, 1000):
            url = f"https://www.istockphoto.com/search/2/image-film?phrase=prophet%20mohammed%20mosque&page={i}"
            driver.get(url)

            # Wait for the page to load
            driver.implicitly_wait(10)

            # Find all image elements on the page using Selenium
            image_elements = driver.find_elements(By.CLASS_NAME, 'yGh0CfFS4AMLWjEE9W7v')

            if len(image_elements) == 0:
                print(f"Page {i - 1} is the Final Page.")
                break

            for img in image_elements:
                # Get the image URL
                img_url = img.get_attribute('src')

                # Create a full URL if it's a relative path
                if not urlparse(img_url).netloc:
                    img_url = urljoin(url, img_url)

                # Get the image filename from the URL
                img_filename = os.path.join(folder_path, os.path.basename(urlparse(img_url).path)).replace('\\', '/')

                # Download the image
                img_data = requests.get(img_url).content
                with open(img_filename, 'wb') as img_file:
                    img_file.write(img_data)

                # Write data to CSV
                writer.writerow({"ID": counter + 1, "Image Name": os.path.basename(img_filename), "Image URL": img_url})
                
                counter += 1
                print(f"{counter}) Downloaded: {img_filename}")
                
            print(f'\n***** Page {i} Scraped Successfully *****\n')

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the browser
    driver.quit()

print(f"Number of Scraped Images: {counter}")
print(f"CSV file '{csv_filename}' created successfully.")

# Alhumdallah for Completing this Project 🤲🙏
