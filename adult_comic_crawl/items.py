# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AdultComicCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field()
    comic_cover_urls = scrapy.Field()
    comic_title = scrapy.Field()
    comic_author = scrapy.Field()
    comic_cover = scrapy.Field()
    cover_path =  scrapy.Field()

class ComicContetITem(scrapy.Item):
    category = scrapy.Field()
    comic_title = scrapy.Field()
    chapter_id = scrapy.Field()
    jpg_urls = scrapy.Field()
    photo_id = scrapy.Field()
    content_path =  scrapy.Field()