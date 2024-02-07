#################### Codes of Scraping Images from Different Websites #####################
## Make sure to write the url correctly and the destinations folders to save the images. ##

#################### Import the Libraries ####################

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv
import os
import requests

#################### Download Function ####################

# Function to download an image
def download_image(image_url, destination_folder, image_name):
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            # Create the destination path
            destination_path = os.path.join(destination_folder, image_name)

            # Save the image
            with open(destination_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=128):
                    file.write(chunk)

            print(f"Image downloaded: {image_name}")
        else:
            print(f"Failed to download image from {image_url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading image: {str(e)}")

#################### Download from Getty ####################

# Set up the Selenium WebDriver
driver = webdriver.Chrome()

# Number of pages to scrape
num_pages = 1000
counter = 0
website_name = 'getty'

try:
    # Create a folder to save downloaded images
    download_folder = 'Mosques_Images/Alaqsa_Mosque'
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Create a CSV file to store information
    csv_file_path = f'Mosques_Images/Alaqsa_Mosque_Images_Data_{website_name}.csv'
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['ID', 'Image Name', 'Image URL']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()

        # Iterate over pages
        for page_num in range(1, num_pages + 1):
            # Navigate to the Getty Images page
            driver.get(f"https://www.gettyimages.in/photos/al-aqsa-mosque?assettype=image&sort=mostpopular&phrase=al%20aqsa%20mosque&license=rf%2Crm&page={page_num}")

            # Wait for some time to allow dynamic content to load
            time.sleep(5)

            # Find all image elements on the page
            image_elements = driver.find_elements(By.CLASS_NAME, 'BLA_wBUJrga_SkfJ8won')
            if len(image_elements) == 0:
                print(f'Page {page_num} is the Final Page')
                break

            # Download and save images, and write information to the CSV file
            for i, element in enumerate(image_elements, start=1):
                image_url = element.get_attribute("src")
                image_name = f"image_{i}_page_{page_num}_{website_name}.jpg"
                download_image(image_url, download_folder, image_name)

                # Write information to CSV file
                csv_writer.writerow({'ID': i, 'Image Name': image_name, 'Image URL': image_url})
                counter += 1

            print(f'\n***** Page {page_num} Scrapped Successfully *****\n')

    # Close the browser
    driver.quit()
    print(f'Number of the Scraped Images is {counter}')
    print(f"CSV file '{csv_file_path}' created successfully.")
    
except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the browser
    driver.quit()

#################### Download from iStock ####################

# Set up the Selenium WebDriver
driver = webdriver.Chrome()

# Number of pages to scrape
num_pages = 1000
counter = 0
website_name = 'istock'

try:    
    # Create a folder to save downloaded images
    download_folder = 'Mosques_Images/Prophet_Mosque4'
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Create a CSV file to store information
    csv_file_path = f'Mosques_Images/Prophet_Mosque_Images_Data_{website_name}.csv'
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['ID', 'Image Name', 'Image URL']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()

        # Iterate over pages
        for page_num in range(1, num_pages + 1):
            # Navigate to the Shutterstock page
            driver.get(f"https://www.istockphoto.com/search/2/image-film?phrase=prophet%20mosque&page={page_num}")
            
            # Wait for the page to load
            driver.implicitly_wait(5)

            # Find all image elements on the page
            image_elements = driver.find_elements(By.CLASS_NAME, "yGh0CfFS4AMLWjEE9W7v")

            if len(image_elements) == 0:
                print(f'Page {page_num} is the Final Page')
                break

            # Download and save images, and write information to the CSV file
            for i, element in enumerate(image_elements, start=1):
                image_url = element.get_attribute("src")
                image_name = f"image_{i}_page_{page_num}_{website_name}.jpg"
                download_image(image_url, download_folder, image_name)

                # Write information to CSV file
                csv_writer.writerow({'ID': i, 'Image Name': image_name, 'Image URL': image_url})
                counter += 1
            
            print(f'\n***** Page {page_num} Scrapped Successfully *****\n')

    print(f"Number of Scraped Images: {counter}")
    print(f"CSV file '{csv_filename}' created successfully.")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the browser
    driver.quit()

#################### Download from Shutterstock ####################

# Set up the Selenium WebDriver
driver = webdriver.Chrome()

# Number of pages to scrape
num_pages = 1000
counter = 0
website_name = 'shutterstock'

try:
    # Create a folder to save downloaded images
    download_folder = 'Mosques_Images/Scared_Mosque'
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Create a CSV file to store information
    csv_file_path = f'Mosques_Images/Scared_Mosque_Images_Data_{website_name}.csv'
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['ID', 'Image Name', 'Image URL']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()

        # Iterate over pages
        for page_num in range(1, num_pages + 1):
            # Navigate to the Shutterstock page
            driver.get(f"https://www.shutterstock.com/search/mecca?page={page_num}")

            # Wait for some time to allow dynamic content to load
            time.sleep(5)

            # Find all image elements on the page
            image_elements = driver.find_elements(By.CLASS_NAME, "mui-1l7n00y-thumbnail")

            if len(image_elements) == 0:
                print(f'Page {page_num} is the Final Page')
                break

            # Download and save images, and write information to the CSV file
            for i, element in enumerate(image_elements, start=1):
                image_url = element.get_attribute("src")
                image_name = f"image_{i}_page_{page_num}_{website_name}.jpg"
                download_image(image_url, download_folder, image_name)

                # Write information to CSV file
                csv_writer.writerow({'ID': i, 'Image Name': image_name, 'Image URL': image_url})
                counter += 1
                print(f'\n***** Page {page_num} Scrapped Successfully *****\n')

    print(f'Number of the Scraped Images is {counter}')
    print(f"CSV file '{csv_file_path}' created successfully.")
    
except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the browser
    driver.quit()

#################### Download from Dreamstime ####################

# Set up the Selenium WebDriver
driver = webdriver.Chrome()

# Number of pages to scrape
num_pages = 1000
counter = 0
website_name = 'dreamstime'

try:
    # Create a folder to save downloaded images
    download_folder = 'Mosques_Images/Alazhar_Mosque'
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Create a CSV file to store information
    csv_file_path = f'Mosques_Images/Alazhar_Mosque_Images_Data_{website_name}.csv'
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['ID', 'Image Name', 'Image URL']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()

        # Iterate over pages
        for page_num in range(1, num_pages + 1):
            # Navigate to the Dreamstime page
            driver.get(f"https://www.dreamstime.com/photos-images/al-azhar-mosque.html?pg={page_num}")

            # Wait for some time to allow dynamic content to load
            time.sleep(5)

            # Get the page source and parse it with BeautifulSoup
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all image elements on the page
            image_elements = soup.find_all('img', class_='item__thumb')

            if len(image_elements) == 0:
                print(f'Page {page_num} is the Final Page')
                break

            # Download and save images, and write information to the CSV file
            for i, img in enumerate(image_elements, start=1):
                image_url = img['src']
                image_name = f"image_{i}_page_{page_num}_{website_name}.jpg"
                download_image(image_url, download_folder, image_name)

                # Write information to CSV file
                csv_writer.writerow({'ID': i, 'Image Name': image_name, 'Image URL': image_url})
                counter += 1
            print(f'\n***** Page {page_num} Scrapped Successfully *****\n')

    print(f'Number of the Scraped Images is {counter}')
    print(f"CSV file '{csv_file_path}' created successfully.")
    
except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the browser
    driver.quit()

#################### Renaming the Images ####################

import os

# Specify the folder containing the images
folder_path = 'Mosques_Images/Alazhar_Mosque'

# Get a list of all files in the folder
files = os.listdir(folder_path)

# Filter out non-image files
allowed_extensions = ['.jpg', '.jpeg', '.png']
image_files = [file for file in files if any(file.lower().endswith(ext) for ext in allowed_extensions)]


# Number of the images
num_images = len(image_files)
print(f'\n***** Number of the Images in the Folder is: {num_images} *****\n')

# Sort the image files alphabetically
image_files.sort()

# Find the number of digits needed for padding
num_digits = len(str(num_images))

# Rename the image files with sequential numbers
for i, old_name in enumerate(image_files, start=1):
    # Extract the file extension
    _, extension = os.path.splitext(old_name)

    # Check if the new name already exists
    if os.path.exists(os.path.join(folder_path, new_name)):
        # If the new name exists, append a unique identifier
        new_name = f"{i:0{num_digits}d}_conflict{extension}"

    # Create the full paths for the old and new names
    old_path = os.path.join(folder_path, old_name)
    new_path = os.path.join(folder_path, new_name)

    # Rename the file
    os.rename(old_path, new_path)

# Rename the image files with sequential numbers again to make them from 1 to the number of the last image
for i, old_name in enumerate(image_files, start=1):
    # Extract the file extension
    _, extension = os.path.splitext(old_name)

    new_name = f"{i}{extension}"
    
    # Create the full paths for the old and new names
    old_path = os.path.join(folder_path, old_name)
    new_path = os.path.join(folder_path, new_name)

    # Rename the file
    os.rename(old_path, new_path)

    print(f"Renamed: {old_name} to {new_name}")
    
print(f"\n***** All Images Renamed Successfully in '{folder_path}' Folder *****\n")
