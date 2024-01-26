import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse, parse_qs

countries = {'eg': 'Egypt', 'ae': 'UAE', 'bh': 'Bahrain', 'qa': 'Qatar', 'sa': 'Saudi Arabia'}
total = 0

# Open a CSV file for writing
with open('scraped_properties.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Create a CSV writer object
    csv_writer = csv.writer(csvfile)

    # Write the header row to the CSV file
    csv_writer.writerow(['Title', 'Type', 'Price', 'Location', 'Country', 'Bedrooms', 'Bathrooms', 'Area', 'URL', 'Phone', 'WhatsApp Number', 'WhatsApp URL'])

    for k, v in countries.items():
        print(20 * '*', 'Properties in', v, 20 * '*')
        counter = 0
        for i in range(1, 1000):
            try:
                url = f"https://www.propertyfinder.{k}/en/buy/properties-for-sale.html?page={i}"
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Find all property cards
                    property_cards = soup.find_all('li', {'role': 'listitem'})
                    print(f'Number of the scraped properties in page {i} is {len(property_cards)}')

                    for card in property_cards:
                        # Extract information from each property card
                        title = card.select_one('.styles-module_content__title__eOEkd').text.strip()
                        property_type = card.select_one('.styles-module_content__property-type__QuVl4 span').text.strip()
                        price = card.select_one('.styles-module_content__price__SgQ5p').text.strip()
                        location = card.select_one('.styles-module_content__location__bNgNM').text.strip()
                        bedrooms = card.select_one('[data-testid="property-card-spec-bedroom"]').text.strip()
                        bathrooms = card.select_one('[data-testid="property-card-spec-bathroom"]').text.strip()
                        area = card.select_one('[data-testid="property-card-spec-area"]').text.strip()
                        urls = card.find_all('a')

                        # Extract WhatsApp number from the URL
                        whatsapp_url = urls[3].get('href')
                        whatsapp_number = whatsapp_url.split("&")[0].split("=")[1]
                        
                        # Print or process the extracted information
                        print(f"Title: {title}")
                        print(f"Type: {property_type}")
                        print(f"Price: {price}")
                        print(f"Location: {location}")
                        print(f"Bedrooms: {bedrooms}")
                        print(f"Bathrooms: {bathrooms}")
                        print(f"Area: {area}")
                        print(f"URL: {urls[0].get('href')}")
                        print(f"Phone: {urls[2].get('href').split(':')[1]}")
                        print(f"WhatsApp Number: {whatsapp_number}")
                        print(f"WhatsApp URL: {whatsapp_url}")
                        print("\n---\n")

                        # Write the extracted information to the CSV file
                        csv_writer.writerow([title, property_type, price, location, v, bedrooms, bathrooms, area, urls[0].get('href'), urls[2].get('href').split(':')[1], whatsapp_number, whatsapp_url])
                        counter += 1
                        total += 1

                else:
                    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

            except Exception as e:
                print(f'The final page is {i - 1}')
                break

        print(f'Number of Scrapped Properties in {v}:', counter)
        print(60 * '*')

print(f'The Total Scrapped Properties:', total)

# Alhumdallah for completing this!
