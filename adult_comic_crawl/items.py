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
    image_urls=scrapy.Field()
    comic_title = scrapy.Field()
    comic_author = scrapy.Field()
    comic_cover = scrapy.Field()



    pass
