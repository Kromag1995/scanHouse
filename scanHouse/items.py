# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PropItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    m2_total = scrapy.Field()
    m2_cub = scrapy.Field()
    direction = scrapy.Field()
    location = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    expens = scrapy.Field()
    rooms = scrapy.Field()
    bedrooms = scrapy.Field()
