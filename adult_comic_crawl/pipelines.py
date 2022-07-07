# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from adult_comic_crawl.models import db_connect, create_news_table, Comic_Data_18, Comic_Content_18
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import logging
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
from . import settings
from adult_comic_crawl.items import AdultComicCrawlItem, ComicContetITem

class image_save(ImagesPipeline):
    # """保存文章到数据库"""
    
    def get_media_requests(self, item):
        
        try:
            print('*********')
            print(item)
            # if isinstance(item, AdultComicCrawlItem):
            #     yield Request(item['comic_cover_urls'], meta= meta_item )
            # elif isinstance(item, ComicContetITem):
            #     yield Request(item['jpg_urls'], meta= meta_item )
        except Exception as error:
            logging.error(error)  

    def file_path(self, request, response=None, info=None):
        meta_item  = request.meta.item

        try:

            if 'comic_cover_urls' in meta_item :
                path = f"covers/{meta_item['category']}/{meta_item['comic_title']}.jpg"
            elif 'jpg_urls' in meta_item :
                path = f"contents/{meta_item['category']}/{meta_item['comic_title']}/chapter_{meta_item['chapter_id']}/{meta_item['photo_id']}"
        
            return path

        except Exception as error:
            logging.error(error)

@contextmanager
def session_scope(Session):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

class AdultComicCrawlPipeline:
    # """保存文章到数据库"""
    def __init__(self):

        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        pass

    def process_item(self, item, spider):
        try:
            if isinstance(item, AdultComicCrawlItem):
                
                image_pipline = image_save(store_uri = settings.IMAGES_STORE )
                image_pipline.get_media_requests(item, info = None)

                data = Comic_Data_18(
                                comic_title = item['comic_title'],
                                comic_author = item['comic_author'],
                                comic_cover = f"{settings.IMAGES_STORE}/covers/{item['category']}/{item['comic_title']}.jpg"
                )
                with session_scope(self.Session) as session:
                    session.add(data)
                
            elif isinstance(item, ComicContetITem):
                pass

                # data = Comic_Content_18(
                #                 comic_title = item['comic_title'],
                #                 chapter_id = item['chapter_id'],
                #                 jpg_urls = f"{settings.IMAGES_STORE}/contents/{item['category']}/{item['comic_title']}/chapter_{item['chapter_id']}/{item['photo_id']}"
                # )
                # with session_scope(self.Session) as session:
                #     session.add(data)
                
        except Exception as error:
            self.connect.rollback()  #發生錯誤，則退回上一次資料庫狀態
            logging.error(error)
            
    def close_spider(self, spider):
        pass

