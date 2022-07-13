# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from adult_comic_crawl.models import db_connect, create_news_table, Comic_Info_18, Comic_Content_18
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import logging
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
from . import settings
from adult_comic_crawl.items import AdultComicCrawlItem, ComicContetITem



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
class AdultComicPipeline(ImagesPipeline):
    # """保存文章到数据库"""
    
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    def get_media_requests(self, item, info ):

        try:
            if isinstance(item, AdultComicCrawlItem):

                data = Comic_Info_18(
                                comic_title = item['comic_title'],
                                comic_author = item['comic_author'],
                                comic_cover = f"{settings.IMAGES_STORE}/covers/{item['category']}/{item['comic_title']}.jpg"
                )
                with session_scope(self.Session) as session:
                    session.add(data)

                yield Request(item['comic_cover_urls'], meta= item )
            elif isinstance(item, ComicContetITem):
 
                data = Comic_Content_18(
                                comic_title = item['comic_title'],
                                chapter_id = item['chapter_id'],
                                comic_content = f"{settings.IMAGES_STORE}/contents/{item['category']}/{item['comic_title']}/chapter_{item['chapter_id']}/{item['photo_id']}"
                )
                with session_scope(self.Session) as session:
                    session.add(data)

                yield Request(item['jpg_urls'], meta= item )
        except Exception as error:
            self.connect.rollback()  #發生錯誤，則退回上一次資料庫狀態
            logging.error(error)  

    def file_path(self, request, response=None, info=None):
        meta_item  = request.meta
        try:

            if 'comic_cover_urls' in meta_item :
                path = f"covers/{meta_item['category']}/{meta_item['comic_title']}.jpg"
            elif 'jpg_urls' in meta_item :
                path = f"contents/{meta_item['category']}/{meta_item['comic_title']}/chapter_{meta_item['chapter_id']}/{meta_item['photo_id']}"

            return path

        except Exception as error:
            logging.error(error)
