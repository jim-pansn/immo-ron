from scrapy.crawler import CrawlerProcess

from ron_orp.spiders.immo_spider import ImmoSpider
from scrapy.utils.project import get_project_settings


if __name__ == '__main__':

    process = CrawlerProcess(settings=get_project_settings())

    process.crawl(ImmoSpider)
    process.start() # the script will block here until the crawling is finished