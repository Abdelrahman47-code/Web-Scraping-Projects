
import tkinter as tk
from tkinter import ttk
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
        self.counter = 1  # Initialize the counter

    def scrape_jobs(self):
        # open csv file and write header
        with open(self.file_name.upper(), 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Num', 'JobTitle', 'Company', 'Location', 'Time'])

            # scrape jobs from each page
            for i in range(self.num_pages + 1):
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
                    writer.writerow([self.counter, job_title, company, location, time_posted])
                    self.counter += 1  # Increment the counter

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


def scrape_jobs_gui():
    job_title = job_title_entry.get()
    num_pages = int(num_pages_entry.get())

    job_scraper = JobScraper(job_title, num_pages)
    job_scraper.scrape_jobs()

    df = job_scraper.read_jobs()
    if df is not None:
        # Clear previous data
        tree.delete(*tree.get_children())

        # Insert data rows
        for index, row in df.iterrows():
            tree.insert('', 'end', values=row.tolist())

        # Show scraping completion message
        completion_text.set(f'Scraping for "{job_title}" jobs is complete. {job_scraper.counter} records have been inserted to "{job_scraper.file_name}".')


# Create the main window
window = tk.Tk()
window.title('Job Scraper')
window.configure(bg='black')

# Create a style for the Treeview
style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial', 14, 'bold'), foreground='red')
style.configure("Treeview", font=('Arial', 12))

# Create a label for the title
title_label = tk.Label(window, text='Scrapping WUZZUF Jobs in Egypt', font=('Arial', 20, 'bold'), fg='white', bg='black')
title_label.pack(pady=10)

# Create a label and entry for job title input
job_title_label = tk.Label(window, text='Job Title', font=('Arial', 16, 'bold'), fg='white', bg='black')
job_title_label.pack()

job_title_entry = tk.Entry(window, justify='center', font=('Arial', 14))
job_title_entry.pack(pady=5)
num_pages_label = tk.Label(window, text='No.of of Pages', font=('Arial', 16, 'bold'), fg='white', bg='black')
num_pages_label.pack()

num_pages_entry = tk.Entry(window, justify='center', font=('Arial', 14))
num_pages_entry.pack(pady=5)
button = tk.Button(window, text='Scrape Jobs', command=scrape_jobs_gui, font=('Arial', 14), bg='white', fg='red')
button.pack(pady=10)

# Create a Treeview widget to display the results in columns
tree = ttk.Treeview(window, columns=['ID', 'Job Title', 'Company', 'Location', 'Time'], show='headings', height=20)
tree.pack()


# Set column headings
for col in ['ID', 'Job Title', 'Company', 'Location', 'Time']:
    tree.heading(col, text=col, anchor='center')
    if col == 'ID':
        tree.column(col, width=50, anchor='center')
    elif col in ['JobTitle', 'Location']:
        tree.column(col, width=400, anchor='center')
    else:
        tree.column(col, width=250, anchor='center')

# Create a label for the completion message
completion_text = tk.StringVar()
completion_label = tk.Label(window, textvariable=completion_text, font=('Arial', 14, 'bold'), fg='white', bg='black')
completion_label.pack(pady=10)

# Create a label for the watermark
watermark_label = tk.Label(window, text='Created by: Abdelrahman Eldaba', font=('Arial', 12), fg='white', bg='black')
watermark_label.place(relx=0.5, rely=0.95, anchor='center')

# Start the GUI event loop
window.mainloop()

# Alhumdallah
