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
    direccion = scrapy.Field()
    barrio = scrapy.Field()
    alquiler = scrapy.Field()
    moneda = scrapy.Field()
    expensas = scrapy.Field()
    ambientes = scrapy.Field()
    dormitorios = scrapy.Field()
