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
        # print("Product Titles:", product_titles)
        
        product_prices = response.css('span.price span[itemprop="price"]::text').getall()
        # print("Product Prices:", product_prices)
        
        product_urls = response.css('article[itemtype="http://schema.org/product"] > a::attr(href)').getall()
        # print("Product URLs:", product_urls)
        
        for title, price, url in zip(product_titles, product_prices, product_urls):
            yield {
                'title': title.strip(),
                'price': price.strip(),
                'url': response.urljoin(url)
            }