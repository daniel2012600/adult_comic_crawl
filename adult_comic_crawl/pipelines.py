# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from adult_comic_crawl.models import db_connect, create_news_table, Comic_Data_18
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

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
        data = Comic_Data_18(comic_title = item['comic_title'],
                                comic_author = item['comic_author'],
                                comic_cover = item['comic_cover']
        )
        with session_scope(self.Session) as session:
            session.add(data)

    def close_spider(self, spider):
        pass
