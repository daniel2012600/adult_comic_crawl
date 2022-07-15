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


# table
# 漫畫資訊： uuid、name、author(非唯一）、publish_date、views

# table2
# 漫畫圖片： uuid、chapter、photo_path(image base64)

# p.s : photo_path，找Ｓ３的ＡＷＳ ＳＤＫ存入


# "章節 1： https://18comic.org/photo/282293"
# "章節 2： https://18comic.org/photo/315540"
# "章節 3： https://18comic.org/photo/282303"
# "章節 4： https://18comic.org/photo/282304"
# "章節 5： https://18comic.org/photo/282305"
# "章節 6： https://18comic.org/photo/282306"
# "章節 7： https://18comic.org/photo/282307"
# "章節 8： https://18comic.org/photo/283741"
# "章節 9： https://18comic.org/photo/285858"


chapter_list  = ["/photo/282293",
            "/photo/315540",
            "/photo/282303",
            "/photo/282304",
            "/photo/282305",
            "/photo/282306",
            "/photo/282307",
            "/photo/283741",
            "/photo/285858"]

query_chapter = query_data('Content', '9f330a32d0b9039ee344531127bfed7c')
if query_chapter:
    del chapter_list[0:int(query_chapter)]
    for i,j in enumerate(chapter_list):
        print(f'章節 {i+1+int(query_chapter)}： https://18comic.org{j}')
else:
    for i,j in enumerate(chapter_list):
        print(f'章節 {i+1}： https://18comic.org{j}')