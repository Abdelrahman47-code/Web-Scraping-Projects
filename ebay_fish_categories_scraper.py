import csv
from bs4 import BeautifulSoup
import requests
from time import sleep

categories = {
    'Food': '20759',
    'Decorations': '66789',
    'Filters': '46310',
    'Other Fish & Aquarium Supplies': '8444',
    'Aquariums & Tanks': '20755',
    'Lighting & Bulbs': '46314',
    'Water Tests & Treatment': '77659',
    'Filter Media & Accessories': '126476',
    'Cleaning & Maintenance': '148983',
    'Pumps (Water)': '77641',
    'Coral & Live Rock': '177797',
    'Live Plants': '66794',
    'Heaters & Chillers': '177799',
    'Pumps (Air)': '100351',
    'Tubing & Valves': '177800',
    'Health Care': '177798',
    'Air Stones': '100355',
    'Gravel & Substrate': '46439',
    'Live Invertebrates': '66788',
    'CO2 Equipment': '100345',
    'Feeders': '63034',
    'Reverse Osmosis & Deionization': '77658',
    'Meters & Controllers': '117435',
    'UV Sterilizers': '117434',
    'Fish Pond Supplies': '134750',
    'Algae Repellent': '262998'
}

length = len(categories)
print(f'Number of The Categoreis is {length}')

csv_file_path = 'ebay_fish_all.csv'

# Open the CSV file in write mode inside the loop
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)

    # Write the header row
    csv_writer.writerow([
        'Title', 'Category', 'Price', 'Seller Info', 'Top Rated Seller', 'Purchase Options',
        'Shipping', 'Source', 'Dynamic Status', 'Item URL', 'Image URL'
    ])
        
    for key, value in categories.items():
        counter = 0

        for i in range(1000):
            try:
                url = f"https://www.ebay.com/sch/{value}/i.html?_nkw=aquarium+%26+fish&norover=1&mkrid=711-34000-13078-0&mkcid=2&mkscid=102&keyword=aquarium+%26+fish&crlp=_2-1300-0-1-1&MT_ID=&geo_id=&rlsatarget=kwd-77309444664613%3Aloc-187&adpos=&device=c&mktype=&loc=187&poi=&abcId=&cmpgn=301063871&sitelnk=&adgroupid=1236950625515563&network=o&matchtype=b&msclkid=1435ad8e5606165bb6efc834f9bb1104&ul_noapp=true&_pgn={i}"
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                }

                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    cards = soup.find_all('li', class_='s-item')

                    if (len(cards)==0 or len(cards)==1):
                        print(f"Page {i} is the final page")
                        break

                    for card in cards[1:]:
                        try:
                            title = card.find('div', class_='s-item__title').text.strip()
                        except AttributeError:
                            title = ''

                        try:
                            price = card.find('span', class_='s-item__price').text.strip()
                        except AttributeError:
                            price = ''

                        try:
                            seller_info = card.find('span', class_='s-item__seller-info-text').text.strip()
                        except AttributeError:
                            seller_info = ''

                        try:
                            top_rated_seller_element = card.find('span', class_='s-item__etrs-text')
                            top_rated_seller = 'Yes' if top_rated_seller_element and top_rated_seller_element.text.strip() == 'Top Rated Seller' else 'No'
                        except AttributeError:
                            top_rated_seller = 'No'

                        try:
                            purchase_options = card.find('span', class_='s-item__purchase-options').text.strip()
                        except AttributeError:
                            purchase_options = ''

                        try:
                            shipping = card.find('span', class_='s-item__shipping').text.strip()
                        except AttributeError:
                            shipping = ''

                        try:
                            source = card.find('span', class_='s-item__itemLocation').text.strip()
                        except AttributeError:
                            source = ''

                        try:
                            dynamic_status = card.find('span', class_='s-item__dynamic').text.strip()
                        except AttributeError:
                            dynamic_status = ''

                        try:
                            item_url = card.find('a').get('href')
                        except AttributeError:
                            item_url = ''

                        try:
                            image_url = card.find('img').get('src')
                        except AttributeError:
                            image_url = ''

                        # Write data to the CSV file
                        csv_writer.writerow([
                            title, key, price, seller_info, top_rated_seller, purchase_options,
                            shipping, source, dynamic_status, item_url, image_url
                        ])

                        counter += 1
                else:
                    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

                print(f"***** Page {i+1} for '{key}' Scraped Successfully *****")

            except requests.exceptions.RequestException as e:
                print(f"Error: {e}. Retrying after 15 seconds...")
                sleep(10)

        print(f"\n ***** '{key}' Scraped Successfully with {counter} Items through {i+1} Pages *****\n")
        sleep(10)

print(f"Scraping complete. Data saved to {csv_file_path}")

# Alhumdallah for Completeing this Project 🤲🙏
