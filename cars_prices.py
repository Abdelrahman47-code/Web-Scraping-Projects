import requests
from bs4 import BeautifulSoup
import csv

class CarScraper:
    def __init__(self):
        self.cars = []

    def scrape(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        containers = soup.find_all('tr')
        
        if len(containers) == 0:
            return False
        
        for x in containers:
            i = x.text.strip().split()
            name = ''.join(i[0:3])
            system = ''.join(i[3:7])
            motor = ''.join(i[7:9])
            price = ''.join(i[9:])
            self.cars.append({'اسم السيارة': name, 'الخصائص': system, 'سعة الموتور': motor, 'السعر': price})
        
        return True

    def save_to_csv(self, filename):
        with open(filename, 'w', encoding='utf8') as f:
            writer = csv.DictWriter(f, self.cars[0].keys())
            writer.writeheader()
            writer.writerows(self.cars)
            print('File Created')

if __name__ == '__main__':
    url = 'https://eg.hatla2ee.com/ar/car/all-prices'
    car_scraper = CarScraper()

    for u in range(15):
        url = f'https://eg.hatla2ee.com/ar/car/all-prices/page/{u}'
        success = car_scraper.scrape(url)
        
        if not success:
            break
        
        print(f"Page {u} scraped")
    
    car_scraper.save_to_csv('cars_prices.csv')
