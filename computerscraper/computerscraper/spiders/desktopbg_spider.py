import scrapy
import sqlite3
import logging
import json
from jsonschema import validate, ValidationError
import os


class ComputerSpider(scrapy.Spider):
    name = "desktop"
    allowed_domains = ["desktop.bg"]
    start_urls = ["https://desktop.bg/"]

    def __init__(self):
        self.conn = sqlite3.connect('computers_data.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products
                         (url TEXT PRIMARY KEY, title TEXT, price TEXT, processor TEXT, gpu TEXT, motherboard TEXT, ram TEXT)''')
        self.conn.commit()

        schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema.json')
        with open(schema_path) as f:
            self.schema = json.load(f)

    def closed(self):
        self.conn.close()

    def parse(self, response):
        try:
            computers_page_link = response.css('div[data-menu="menu-Computer"] ul.brands li:nth-child(1) a::attr(href)').get()
            if computers_page_link:
                full_computers_page_url = 'https://desktop.bg' + computers_page_link
                yield response.follow(full_computers_page_url, callback=self.parse_computers_page)
            else:
                logging.error("Computers page link not found on the homepage.")
        except Exception as e:
            logging.error("Error parsing homepage: %s", str(e))

    def parse_computers_page(self, response):
        try:
            product_page_urls = response.css('article[itemtype="http://schema.org/product"] > a::attr(href)').getall()
            for product_page_url in product_page_urls:
                yield response.follow(product_page_url, callback=self.parse_product_page)
        except Exception as e:
            logging.error("Error parsing computers page: %s", str(e))

    def parse_product_page(self, response):
        try:
            product_url = response.url
            product_title = response.css('h1[itemprop="name"]::text').get()
            product_price = response.css('span.price span[itemprop="price"]::text').get()
            product_processor = response.xpath('//th[contains(text(), "Процесор")]/following-sibling::td//text()').get()
            product_gpu = response.xpath('//th[contains(text(), "Видеокарта")]/following-sibling::td//text()').get()
            product_motherboard = response.css('#characteristics > table > tbody > tr:nth-child(6) > td::text').get()
            ram_options = response.xpath('//tr[@id="DesktopRam"]/td//div[@class="default-option options"]/label/span/text()').getall()
            
            # At some of the computer pages, there are options, for example 3 motherboard or processor options
            # So this way only the default option is crawled, if there are multiple options
            if len(product_motherboard) < 2:
                product_motherboard = response.css('#Motherboard > td > div.default-option.options > label > span:nth-child(1)::text').get()

            if len(product_processor) < 2:
                product_processor = response.css('#DesktopCpu > td > div.default-option.options > label > span:nth-child(1)::text').get()

            if len(product_gpu) < 2:
                product_gpu = response.css('#DesktopVideoCard > td > div.default-option.options > label > span:nth-child(1)::text').get()

            if len(ram_options) < 2:
                ram_options = response.css('#characteristics > table > tbody > tr:nth-child(9) > td::text').get()

            product_ram = ''.join(ram_options).strip() if ram_options else None

            product_data = {
                'url': product_url,
                'title': product_title.strip() if product_title else None,
                'price': product_price.strip() if product_price else None,
                'processor': product_processor.strip() if product_processor else None,
                'gpu': product_gpu.strip() if product_gpu else None,
                'motherboard': product_motherboard.strip() if product_motherboard else None,
                'ram': product_ram if ram_options else None
            }

            try:
                validate(instance=product_data, schema=self.schema)
            except ValidationError as e:
                logging.error("Validation error: %s", str(e))
                return

            self.cursor.execute("SELECT * FROM products WHERE url=?", (product_url,))
            existing_product = self.cursor.fetchone()

            if not existing_product:
                try:
                    self.cursor.execute("INSERT INTO products (url, title, price, processor, gpu, motherboard, ram) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                        (product_url,
                                         product_title.strip() if product_title else None,
                                         product_price.strip() if product_price else None,
                                         product_processor.strip() if product_processor else None,
                                         product_gpu.strip() if product_gpu else None,
                                         product_motherboard.strip() if product_motherboard else None,
                                         product_ram if ram_options else None))
                    self.conn.commit()
                    logging.info("Data inserted into SQLite successfully.")
                except sqlite3.Error as e:
                    logging.error("Error inserting data into SQLite: %s", str(e))
        except Exception as e:
            logging.error("Error parsing product page: %s", str(e))

        yield product_data
