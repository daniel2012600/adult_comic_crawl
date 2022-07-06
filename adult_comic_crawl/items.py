# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AdultComicCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 分類的標題
    category=scrapy.Field()
    # 存放圖片地址
    comic_cover_urls = scrapy.Field()
    comic_title = scrapy.Field()
    comic_author = scrapy.Field()
    comic_cover = scrapy.Field()
    chapter_id = scrapy.Field()
    comic_id = scrapy.Field()
    chapter_id = scrapy.Field()
    jpg_url = scrapy.Field()
    pass

class ComicContetITem(scrapy.Item):
    comic_title = scrapy.Field()
    chapter_id = scrapy.Field()
    jpg_url = scrapy.Field()