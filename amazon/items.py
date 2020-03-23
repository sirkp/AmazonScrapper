# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    base_price = scrapy.Field()
    final_price = scrapy.Field()
    discount = scrapy.Field()
    brand = scrapy.Field()
    product_name = scrapy.Field()
    rating = scrapy.Field()
    fit = scrapy.Field()
    colour = scrapy.Field()
    product_details = scrapy.Field()

