# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelscraperItem(scrapy.Item):
    # name = scrapy.Field()
    hotel_name =scrapy.Field()
    hotel_url = scrapy.Field()
    hotel_address = scrapy.Field()
    hotel_rating = scrapy.Field()
    hotel_review_num = scrapy.Field()
    hotel_price = scrapy.Field()
    hotel_info  = scrapy.Field()
    check_in = scrapy.Field()
    check_out = scrapy.Field()
    rooms = scrapy.Field()
    general = scrapy.Field()
    food_beverage = scrapy.Field()
    business_service = scrapy.Field()
    front_desk_service = scrapy.Field()
    travel = scrapy.Field()
    recreation = scrapy.Field()
    kids = scrapy.Field()

    pass
