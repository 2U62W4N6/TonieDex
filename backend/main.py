from crawler.tonie_crawler import TonieCrawler
from service.tonie_service import TonieServcie

import os

if __name__ == "__main__":
    key, database = os.environ.get("CRAWLER_URL"), os.environ.get("DB_URL")
    if key and database:
        crawler = TonieCrawler(key)
        service = TonieServcie(database)
        tonies = list(crawler.crawl_tonies())
        service.insert_tonies(tonies)
