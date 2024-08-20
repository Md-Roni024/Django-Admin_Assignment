import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging

load_dotenv()
BOT_NAME = "hotel_scrapper"

SPIDER_MODULES = ["hotel_scrapper.spiders"]
NEWSPIDER_MODULE = "hotel_scrapper.spiders"
ROBOTSTXT_OBEY = False


PASSWORD = quote_plus(os.getenv('PASSWORD')) or 'p@stgress'
HOST = os.getenv('HOST') or 'localhost'
DATABASE = os.getenv('SCRAPY_DATABASE') or 'scrapy_database'
USERNAME = os.getenv('DB_USER') or 'postgres'
PORT = os.getenv('PORT') or '5433'
DATABASE_URL = f'postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'


FEEDS = {
    'output.json': {
        'format': 'json',
        'overwrite': True
    }
}

LOG_LEVEL = 'WARNING'  


ITEM_PIPELINES = {
    'hotel_scrapper.pipelines.ImageDownloadPipeline': 100,
    'hotel_scrapper.pipelines.HotelPipeline': 200,
}


REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

