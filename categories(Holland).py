import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

# URL to scrape
url = "https://gemeentegidz.nl/listings/"

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object
soup = BeautifulSoup(response.content, "html.parser")

# Find all li elements that contain the names
name_elements = soup.find_all("li")

# Extract the names and create Google Maps links
names_with_links = []
for element in name_elements:
    span_element = element.find("span")
    if span_element is not None:
        name = span_element.text
        encoded_name = urllib.parse.quote(name)
        google_maps_link = f"https://www.google.com/maps/search/{encoded_name}"
        names_with_links.append((name, google_maps_link))

# Extract data from Google Maps for each location
for name, link in names_with_links:
    print("Location:", name)
    print("Google Maps Link:", link)

    # Send a GET request to the Google Maps link
    response = requests.get(link)

    # Create a BeautifulSoup object for the Google Maps page
    maps_soup = BeautifulSoup(response.content, "html.parser")

    # Extract additional data from the Google Maps page
    website_element = maps_soup.find("a", {"data-attribution-url": "website"})
    if website_element is not None:
        website = website_element.get("href")
        print("Website:", website)

    address_element = maps_soup.find("span", {"class": "widget-pane-link"})
    if address_element is not None:
        address = address_element.text
        print("Address:", address)

    # Extract phone, email, altitude, longitude, or other data as needed
    phone_element = maps_soup.find("span", {"data-dtype": "d3ph"})
    if phone_element is not None:
        phone = phone_element.text
        print("Phone:", phone)

    email_element = maps_soup.find("a", {"data-dtype": "d3se"})
    if email_element is not None:
        email = email_element.text
        print("Email:", email)

    altitude_element = maps_soup.find("meta", {"itemprop": "latitude"})
    longitude_element = maps_soup.find("meta", {"itemprop": "longitude"})
    if altitude_element is not None and longitude_element is not None:
        altitude = altitude_element.get("content")
        longitude = longitude_element.get("content")
        print("Altitude:", altitude)
        print("Longitude:", longitude)
        
    time.sleep(3)
