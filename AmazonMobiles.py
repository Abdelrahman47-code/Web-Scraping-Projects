import requests
from bs4 import BeautifulSoup

class AmazonMobilesScraper:
    def __init__(self, output_file, number_of_pages):
        self.output_file = output_file
        self.pages = number_of_pages
        self.header = 'Details, Price\n'

    def scrape(self):
        # Open the output file in write mode and write the header
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(self.header)
            
            # Iterate over the desired range of pages
            for u in range(self.pages):
                # Construct the URL for each page
                url = f'https://www.amazon.eg/s?rh=n%3A21832883031&fs=true&language=en&ref=lp_21832883031_sar&page={u}'
                # Send a GET request to the URL with appropriate headers
                page = requests.get(url, headers={'Accept-Language': 'en-US'})
                # Parse the HTML content of the page
                soup = BeautifulSoup(page.content, 'html.parser')
                # Find all the containers that hold the desired data
                containers = soup.find_all('div', {'class': 'a-section a-spacing-base'})
                # Check if there are no containers found, indicating the last page
                if len(containers) == 0:
                    print("This is the last page.")
                    break

                # Iterate over each container
                for i in range(len(containers)):
                    # Extract the description from the container
                    description = containers[i].find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'}).text.strip().replace(',', '')
                    # Extract the price from the container
                    c_price = containers[i].find('span', {'class': 'a-price-whole'})
                    if c_price is not None:
                        price = c_price.text.strip()[:-1].replace(',', '.')
                    else:
                        price = ''
                    # Write the description and price to the output file
                    f.write(description + ',' + price + '\n')
                print(f"Page {u} scraped")

        print('File created')

if __name__ == '__main__':
    scraper = AmazonMobilesScraper('AmazonMobiles.csv', 3)
    scraper.scrape()
