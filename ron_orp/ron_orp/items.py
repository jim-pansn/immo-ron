# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImmoPost(scrapy.Item):
    id = scrapy.Field()
    heading = scrapy.Field()
    city = scrapy.Field()
    created = scrapy.Field()
    text = scrapy.Field()
    published = scrapy.Field()
    address = scrapy.Field()
    limited = scrapy.Field()
    zip_code = scrapy.Field()
    price = scrapy.Field()
    rooms = scrapy.Field()
    area = scrapy.Field()
    type = scrapy.Field()
    view_count_unique = scrapy.Field()
    url = scrapy.Field()
    pass
