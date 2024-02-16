import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

total_counter = 0

# Function to create a session with retry mechanism
def create_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.mount('http://', HTTPAdapter(max_retries=retries))
    return session

# Open a CSV file in write mode
with open('hatla2ee_scraped_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Define fieldnames for the CSV file
    fieldnames = ['Name', 'Price', 'Color', 'Mileage', 'Make', 'Model', 'City', 'Date Displayed', 'Automatic Transmission', 'Air Conditioner', 'Power Steering', 'Remote Control', 'Item URL']
    
    # Initialize a CSV writer object
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write the header row
    writer.writeheader()
    
    session = create_session()

    for i in range(1, 1000):
        url = f"https://eg.hatla2ee.com/en/car/page/{i}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        try:
            # Send a GET request to the URL using the session
            response = session.get(url)

            # Parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")

            # Find all car cards
            car_cards = soup.find_all("div", class_="newCarListUnit_contain")
            if len(car_cards) == 0:
                break

            counter = 0

            # Iterate over each car card
            for card in car_cards:
                car_name = car_price = car_color = mileage = make = model = city = date_displayed = is_automatic = has_air_conditioner = has_power_steering = has_remote_control = item_url = None

                try:
                    car_name = card.find("div", class_="newCarListUnit_header").text.strip()
                except:
                    pass

                try:
                    car_price = card.find("div", class_="main_price").text.strip()
                    if car_price == "-":
                        car_price = None
                except:
                    pass

                try:
                    meta_tags = card.find_all("span", class_="newCarListUnit_metaTag")
                    car_color = meta_tags[0].text.strip()
                    mileage = meta_tags[-1].text.strip()
                    if mileage == "- Km":
                        mileage = None
                except:
                    pass

                try:
                    meta_links = card.find("div", class_="newCarListUnit_metaTags").find_all("span", class_="newCarListUnit_metaLink")
                    make = meta_links[0].text.strip()
                    model = meta_links[1].text.strip()
                    city = meta_links[-1].text.strip()
                except:
                    pass

                try:
                    date_displayed = card.find("div", class_="otherData_Date").find("span").text.strip()
                except:
                    pass
                
                try:
                    icons_element = card.find("div", class_="otherData_carType")

                    # Check for the existence of each icon and update variables accordingly
                    is_automatic = 'No'
                    has_air_conditioner = 'No'
                    has_power_steering = 'No'
                    has_remote_control = 'No'

                    if icons_element.find('i', {'title': 'Automatic'}):
                        is_automatic = 'Yes'

                    if icons_element.find('i', {'title': 'Air Conditioner'}):
                        has_air_conditioner = 'Yes'

                    if icons_element.find('i', {'title': 'Power Steering'}):
                        has_power_steering = 'Yes'

                    if icons_element.find('i', {'title': 'Remote Control'}):
                        has_remote_control = 'Yes'
                except:
                    pass
                
                try:
                    item_url = card.find("div", class_="newMainImg").find('a').get('href')
                except:
                    pass
                
                # Write the row to the CSV file
                writer.writerow({'Name': car_name, 'Price': car_price, 'Color': car_color, 'Mileage': mileage, 'Make': make, 'Model': model, 'City': city, 'Date Displayed': date_displayed, 'Automatic Transmission': is_automatic, 'Air Conditioner': has_air_conditioner, 'Power Steering': has_power_steering, 'Remote Control': has_remote_control, 'Item URL': f"https://eg.hatla2ee.com{item_url}"})
                counter += 1

            print(f"***** Page {i} Scrapped Successfully with {counter} Items*****")
            total_counter += counter
            sleep(5)
        except Exception as e:
            print(f"Error occurred while scraping page {i}: {e}")
            sleep(30)

print(f"\n***** Total Number of the Scrapped Items is {total_counter} *****\n")

# Alhumdallah for Completeing this Project 🤲🙏
