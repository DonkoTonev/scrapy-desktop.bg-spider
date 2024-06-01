import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "desktop"
    allowed_domains = ["desktop.bg"]
    start_urls = ["https://desktop.bg/"]

    def parse(self, response):
        computers_all = response.css('div[data-menu="menu-Computer"] ul.brands li:nth-child(1) a::attr(href)').get()
        computers_all_whole_link = 'https://desktop.bg' + computers_all

        yield response.follow(computers_all_whole_link, callback=self.parse_computers_page)


    def parse_computers_page(self, response):
        product_titles = response.css('h2[itemprop="name"]::text').getall()
        product_prices = response.css('span.price span[itemprop="price"]::text').getall()
        product_urls = response.css('article[itemtype="http://schema.org/product"] > a::attr(href)').getall()
        
        for title, price, url in zip(product_titles, product_prices, product_urls):
            yield {
                'title': title.strip(),
                'price': price.strip(),
                'url': response.urljoin(url)
            }
    
    def parse_product_page(self, response):
        
        processor = response.xpath('//th[contains(text(), "Процесор")]/following-sibling::td//text()').get()
        gpu = response.xpath('//th[contains(text(), "Видеокарта")]/following-sibling::td//text()').get()
        motherboard = response.xpath('//th[contains(text(), "Дънна платка")]/following-sibling::td//text()').get()
        ram_option = response.xpath('//tr[@id="DesktopRam"]/td//div[@class="default-option options"]/label/span/text()').getall()
        ram = ''.join(ram_option).strip() if ram_option else None
        
        yield {
            'processor': processor.strip() if processor else None,
            'gpu': gpu.strip() if gpu else None,
            'motherboard': motherboard.strip() if motherboard else None,
            'ram': ram if ram_option else None,
        }