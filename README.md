# Scrapy Desktop.bg Spider

## Overview
This Scrapy spider, named `desktop`, is designed to crawl the website desktop.bg, a Bulgarian online retailer specializing in computer hardware. The spider is built to extract information about desktop computers listed on the website, including their specifications such as processor, GPU, RAM, motherboard, and price.

## Installation
1. Make sure you have Python installed on your system. You can download it from [Python's official website](https://www.python.org/).
2. Install Scrapy using pip:
```
pip install scrapy
```

3. Clone or download the spider code from this repository.

## Usage
1. Navigate to the directory containing the spider code.
2. Run the spider using the following command:

```
scrapy crawl desktop
```

3. The spider will start crawling the website and extracting information from the desktop computer listings.
4. Extracted data will be stored in a SQLite database named `computers_data.db`.
5. Logs will be generated during the crawling process.

## Spider Structure
- **ComputerSpider**: The main spider class responsible for crawling the website.
- **parse**: Method to parse the homepage of desktop.bg and extract the link to the `https://desktop.bg/computers-all` page.
- **parse_computers_page**: Method to parse individual brand pages and extract links to computer pages.
- **parse_product_page**: Method to parse computer pages and extract detailed information about each desktop computer.

## Database Schema
The spider creates a SQLite database named `computers_data.db` with a single table named `products`. The table schema is as follows:
- `url` (TEXT, PRIMARY KEY): The URL of the product page. The `url` is used to assure that each product is stored only once in the DB and there are no duplicates.
- `title` (TEXT): The title/name of the desktop computer. ***_Note: I know that the `title` is not required in the task description, but I decided to crawl it and store it, just to make it easier for the examiner._***
- `price` (TEXT): The price of the desktop computer. ***_Note: I know that the `price` is not required in the task description, but I decided to crawl it and store it, just to make it easier for the examiner._***
- `processor` (TEXT): The processor of the desktop computer.
- `gpu` (TEXT): The GPU (graphics processing unit) of the desktop computer.
- `motherboard` (TEXT): The motherboard of the desktop computer.
- `ram` (TEXT): The RAM (random access memory) of the desktop computer.

_**Note: For this task (first task), I notices it is not specified if/where should store the crawled data, so I decided to use SQLite to store the data for its simplicity and ease of setup, making it convenient for this task.**_

## Example of Crawled Data
Here is an example of the data crawled by the spider:

```
{
'url': 'https://desktop.bg/computers-dell-Vostro_3020_MT-dell_vostro_3020_mt_N2044VDT3020MTEMEA01',
'title': 'Dell Vostro 3020 MT',
'price': '1129',
'processor': 'Intel Core i3-13100 (4-ядрен, 8-нишков, до 4.50GHz, 12MB кеш)',
'gpu': 'Intel UHD Graphics 730 (споделена памет)',
'motherboard': 'Intel B660',
'ram': '8GB (1x 8192MB) - DDR4, 3200MHz'
}
```

## Dependencies
- Scrapy: A powerful web crawling and scraping framework for Python.
- SQLite3: A lightweight database engine used to store extracted data.

## Logging
The spider utilizes Python's built-in logging module to provide information and error logs during the crawling process. Logs are printed to the console and can be redirected to a file for further analysis.
