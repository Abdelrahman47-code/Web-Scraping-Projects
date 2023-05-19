import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time


class JobScraper:
    def __init__(self, job_title, num_pages):
        self.job_title = job_title
        self.num_pages = num_pages
        self.file_name = f'{job_title} Jobs.csv'
        self.base_url = 'https://wuzzuf.net'
        
    def scrape_jobs(self):
        # open csv file and write header
        with open(self.file_name.upper(), 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['JobTitle', 'Company', 'Location', 'Time'])

            # scrape jobs from each page
            for i in range(1, self.num_pages + 1):
                url = f'https://wuzzuf.net/search/jobs/?a=hpb%7Cspbg&q={self.job_title}&start={i}'
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')
                jobs = soup.find_all('div', class_="css-1gatmva e1v1l3u10")

                if len(jobs) == 0:
                    break
                
                for job in jobs:
                    # get job information
                    job_title = job.find('h2', class_="css-m604qf").text.strip().replace(', ', '-')
                    company = job.find('a', class_="css-17s97q8").text.strip().split()[0]
                    location = job.find('span', class_="css-5wys0k").text.strip().replace(', ', '-')
                    time_posted = job.find('span', class_="css-1ve4b75 eoyjyou0").text.strip()

                    # write job information to csv file
                    writer.writerow([job_title, company, location, time_posted])

                # add a delay between requests to prevent getting blocked
                time.sleep(2)

        print(f'Scraping for "{self.job_title}" jobs is complete. Data has been written to "{self.file_name}".')

    def read_jobs(self):
        try:
            df = pd.read_csv(self.file_name, error_bad_lines=False)
            return df
        except FileNotFoundError:
            print(f'Error: The file "{self.file_name}" does not exist.')
            return None


# example usage
job_scraper = JobScraper('digital marketing', 100)
job_scraper.scrape_jobs()

df = job_scraper.read_jobs()
if df is not None:
    print(df.head())
