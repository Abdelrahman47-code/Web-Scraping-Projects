from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


class CuisinesScraper:
    def __init__(self):
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        
    def get_cuisine_links(self, url):
        """Scrape the wikipedia page and retrieve links to each cuisine's page"""
        self.browser.get(url)
        items = self.browser.find_elements(By.CLASS_NAME ,"div-col")

        links = []

        for item in items:
            # retrieve keywords for each cuisine
            keywords = [x.text.split("\n") for x in (item.find_elements(By.TAG_NAME, "ul"))]
            for i in range(len(keywords)):
                for word in keywords[i]:
                    # replace spaces with underscores to create wikipedia page url
                    word = word.replace(" ","_")
                    link = f"https://en.wikipedia.org/wiki/{word}"
                    print(link)
                    links.append(link)

        return links
    
    def write_links_to_csv(self, links, filename):
        """Write the cuisine links to a csv file"""
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('Links\n')
            for link in links:
                file.write(f"{link}\n")

    def close_browser(self):
        """Close the web browser"""
        self.browser.quit()
        
        
if __name__ == '__main__':
    scraper = CuisinesScraper()
    
    # retrieve links to each cuisine's wikipedia page
    links = scraper.get_cuisine_links("https://en.wikipedia.org/wiki/List_of_cuisines")
    print(f"Retrieved {len(links)} links to cuisine pages.")
    
    # write links to csv file
    scraper.write_links_to_csv(links, 'links.csv')
            
    scraper.close_browser()
