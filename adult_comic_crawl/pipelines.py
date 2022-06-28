# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from adult_comic_crawl.models import db_connect, create_news_table, Comic_Data_18
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import base64
import logging
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request

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

    """保存文章到数据库"""
    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        pass

    def process_item(self, item, spider):
        try:
            img = item['comic_cover']
            print(222222)
            print(img)
            print(222222)
            # img = base64.b64encode(img.read())
            # data = Comic_Data_18(
            #                     comic_cover = img
            # )
            # with session_scope(self.Session) as session:
            #     session.add(data)
                
        except Exception as error:
            self.connect.rollback()  #發生錯誤，則退回上一次資料庫狀態
            logging.error(error)
            
    def close_spider(self, spider):
        pass



class ImgDownloadPipeline(ImagesPipeline):
    # """保存文章到数据库"""
    # def __init__(self):
    #     engine = db_connect()
    #     create_news_table(engine)
    #     self.Session = sessionmaker(bind=engine)

    def get_media_requests(self, item, info):
        print(1111111)
        yield Request(item['comic_cover'])

    def item_completed(self, results, item, info):
        print(results)
        image_paths = [x['path'] for ok, x in results if ok]
        
        if not image_paths:
            raise DropItem("Item contains no images")
        item['comic_cover'] = image_paths
        return item
