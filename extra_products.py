import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep

categories = ['electronics/c/1', 'mobiles-tablets/c/2', 'computer/c/3', 'white-goods/c/4',
              'small-appliances/c/5', 'accessories/c/6', 'electronic-games/c/13', 'extra-smart/c/66', 'home-automation/c/105']

urls = [
        'https://www.extra.com/en-sa/electronics/c/1',
        'https://www.extra.com/en-sa/mobiles-tablets/c/2',
        'https://www.extra.com/en-sa/computer/c/3',
        'https://www.extra.com/en-sa/white-goods/c/4',
        'https://www.extra.com/en-sa/small-appliances/c/5',
        'https://www.extra.com/en-sa/accessories/c/6',
        'https://www.extra.com/en-sa/electronic-games/c/13',
        'https://www.extra.com/en-sa/extra-smart/c/66',
        'https://www.extra.com/en-sa/home-automation/c/105'
       ]

output_folder = 'extra_items'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

total = 0

# Open CSV file for writing
with open(os.path.join('extra_items.csv'), mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Product Name', 'Brand Name', 'Category', 'Post Price', 'Pre Price', 'Discount',
                  'Basseta Payment', 'Rating', 'Item URL', 'Stats', 'Image URLs']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write header
    writer.writeheader()
    
    for category in categories:
        category_counter = 0
        
        # Loop through pages for the current category
        for i in range(1000):
            counter = 0
            
            url = f'https://www.extra.com/en-sa/{category}/facet/?q=:relevance&text=&pageSize=24&pg={i}&sort=relevance'
            
            chrome_options = Options()
            chrome_options.add_argument('--headless')

            chromedriver_path = 'chromedriver.exe'
            driver = webdriver.Chrome(service=ChromeService(chromedriver_path), options=chrome_options)

            try:
                driver.get(url)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                product_cards = soup.find_all('section', class_='main-section')
                if len(product_cards) == 0:
                    print(f'---------- Page {i+1} is the Final One for "{category.split("/")[0]}" Items ----------')
                    break

                for card in product_cards:
                    try:
                        product_name = card.select_one('.product-name-data').text.strip()
                    except AttributeError:
                        product_name = ''

                    try:
                        brand_name = card.select_one('.brand-name').text.strip()
                    except AttributeError:
                        brand_name = ''

                    try:
                        post_price = card.select_one('.price-side').text.strip()
                    except AttributeError:
                        post_price = ''

                    try:
                        pre_price = card.select_one('.secondary-price').text.strip()
                    except AttributeError:
                        pre_price = ''

                    try:
                        discount = card.select_one('.discount-side').text.strip()
                    except AttributeError:
                        discount = ''

                    try:
                        basseta_price = card.select_one('.tasheel-with-emi-wrapper').text.strip()
                    except AttributeError:
                        basseta_price = ''

                    try:
                        rating = card.select_one('.product-rating-review').text.strip()
                    except AttributeError:
                        rating = ''

                    try:
                        item_url_text = card.select_one('a').get('href')
                        item_url = 'https://www.extra.com' + item_url_text
                    except AttributeError:
                        item_url = ''

                    # Extracting stats
                    try:
                        stats_container = card.select_one('.product-stats')
                        stats = ' || '.join([stat.text.strip() for stat in stats_container.find_all('li')])
                    except AttributeError:
                        stats = ''

                    # Extracting images
                    try:
                        image_container = card.select_one('.image-container')
                        image_urls = []
                        img_tag = image_container.select_one('img')
                        if img_tag:
                            image_urls.append(img_tag['src'])
                        source_tags = image_container.select('source')
                        for source in source_tags:
                            image_urls.append(source['srcset'])
                        image_urls = ' || '.join(image_urls)
                    except AttributeError:
                        image_urls = ''

                    # Write data to CSV file
                    writer.writerow({
                        'Product Name': f"{brand_name} {product_name}",
                        'Brand Name': brand_name,
                        'Category': category.split('/')[0].title(),
                        'Post Price': post_price,
                        'Pre Price': pre_price,
                        'Discount': discount,
                        'Basseta Payment': basseta_price,
                        'Rating': rating,
                        'Item URL': item_url,
                        'Stats': stats,
                        'Image URLs': image_urls
                    })

                    counter += 1

                category_counter += counter
                total += category_counter
                print(f'----- Page {i+1} Scraped Successfully for "{category.split("/")[0]}" with {counter} Items -----')

            except Exception as e:
                print(f'Error during web scraping for "{category.split("/")[0]}": {e}')
                print(f'---------- Page {i+1} is the Final One for "{category.split("/")[0]}" Items ----------')
                break

            finally:
                driver.quit()

    print(f'\n***** Total Number of the Scraped Items for "{category.split("/")[0]}" is {category_counter} *****\n')
    sleep(10)

print(f'\nTotal Number of the Scraped Items for all categories is {total}')

# Alhumdallah for Completeing this Project 🤲🙏
