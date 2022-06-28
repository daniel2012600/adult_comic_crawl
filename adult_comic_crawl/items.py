# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AdultComicCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    comic_title = scrapy.Field()
    comic_author = scrapy.Field()
    comic_cover = scrapy.Field()



    pass
