thonimport requests
from bs4 import BeautifulSoup
import json
import time

class AmazonScraper:
    def __init__(self, keyword, pages):
        self.base_url = 'https://www.amazon.com/s?k='
        self.keyword = keyword
        self.pages = pages

    def get_page_content(self, page):
        url = f"{self.base_url}{self.keyword}&page={page}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to retrieve page {page}. Status code: {response.status_code}")

    def parse_product(self, product):
        title = product.find('span', {'class': 'a-text-normal'}).get_text()
        price = product.find('span', {'class': 'a-price-whole'})
        price = price.get_text() if price else 'N/A'
        asin = product.get('data-asin')
        url = 'https://www.amazon.com' + product.find('a', {'class': 'a-link-normal'})['href']
        
        return {
            'url': url,
            'title': title,
            'price': {'currency': '$', 'amount': price},
            'asin': asin
        }

    def scrape(self):
        products = []
        for page in range(1, self.pages + 1):
            print(f"Scraping page {page}...")
            content = self.get_page_content(page)
            soup = BeautifulSoup(content, 'html.parser')
            product_list = soup.find_all('div', {'data-asin': True})
            for product in product_list:
                product_data = self.parse_product(product)
                products.append(product_data)
            time.sleep(2)  # Be polite to the server and avoid blocking
        return products

def save_to_file(products, filename='data/outputs.json'):
    with open(filename, 'w') as file:
        json.dump(products, file, indent=4)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    keyword = "laptop"
    pages = 3
    scraper = AmazonScraper(keyword, pages)
    product_data = scraper.scrape()
    save_to_file(product_data)