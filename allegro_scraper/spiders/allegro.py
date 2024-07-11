# spiders/allegro.py

import scrapy
from scrapy import Request
from bs4 import BeautifulSoup

class AllegroSpider(scrapy.Spider):
    name = 'allegro'
    allowed_domains = ['allegro.pl']
    start_urls = ['https://allegro.pl/']

    def parse(self, response):
        # Extract product links from search results
        product_links = response.css('a.product-link::attr(href)').getall()
        for link in product_links:
            yield Request(url=link, callback=self.parse_product)

        # Follow pagination links
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield Request(url=next_page, callback=self.parse)

    def parse_product(self, response):
        # Extract product data
        soup = BeautifulSoup(response.body, 'lxml')
        product_data = {
            'title': soup.find('h1', class_='product-title').text.strip(),
            'price': soup.find('span', class_='price').text.strip(),
            'description': soup.find('div', class_='description').text.strip(),
            # Add more fields as needed
        }
        yield product_data
