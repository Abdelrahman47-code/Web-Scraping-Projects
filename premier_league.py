import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

# Define the URL of the Premier League table on the BBC Sport website
url = "https://www.bbc.com/sport/football/premier-league/table"

# Use the requests library to fetch the HTML content of the page
page = requests.get(url)

# Check if the response from the server is successful (status code 200)
print(page)  ##<200>

# Use BeautifulSoup to parse the HTML content of the page
soup = BeautifulSoup(page.content, 'html.parser')

# Find the table header and table content using the `find()` and `find_all()` methods of BeautifulSoup
table_header = soup.find('thead').find_all('th')
table_content = soup.find('tbody').find_all('tr')

# Create a new CSV file named `table.csv` using the `open()` function
# Set the `newline=''` parameter to ensure that there are no extra blank lines between rows
with open('premier-league.csv', 'w', newline='') as f:
    writer = csv.writer(f)  # Create a new CSV writer object

    # Extract the header row from the table header using a list comprehension
    elements = [i.text.strip() for i in table_header]

    # Write the header row to the CSV file using the `writerow()` method of the CSV writer object
    writer.writerow(elements[:-1])  # Remove the last column, which is not needed

    # Loop over each row of table content
    for row in table_content:
        body = []  # Create an empty list to store the data for each row

        # Extract the data for each cell of the row using a list comprehension
        details = row.find_all('td')[:-1]  # Remove the last column, which is not needed
        for item in details:
            body.append(item.text)

        # Write the row of data to the CSV file using the `writerow()` method of the CSV writer object
        writer.writerow(body)

df = pd.read_csv('premier-league.csv')
print(df)
