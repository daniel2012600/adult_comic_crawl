# -*- coding: utf-8 -*-

from adult_comic_crawl.models import db_connect, create_news_table, Comic_Info_18, Comic_Content_18
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from contextlib import contextmanager
import adult_comic_crawl.settings

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
engine = db_connect()
create_news_table(engine)
Session = sessionmaker(bind=engine)

def query_data(item,args):
    try:
        with session_scope(Session) as session:
            if item == 'Info':
                query = session.query(Comic_Info_18).filter(Comic_Info_18.comic_title==args).all()
            elif item == 'Content':
                query = session.query( func.max(Comic_Content_18.chapter_id) ).filter(Comic_Content_18.comic_title==args).group_by(Comic_Content_18.comic_title).one()[0]

            return query
    except Exception as error:
        print(error)

print(query_data('Content','158238cd075721499bf77009788a11c5'))

# table
# 漫畫資訊： uuid、name、author(非唯一）、publish_date、views

# table2
# 漫畫圖片： uuid、chapter、photo_path(image base64)

# p.s : photo_path，找Ｓ３的ＡＷＳ ＳＤＫ存入