# -*- encoding: utf-8 -*-
"""
Topic: 定义数据库模型实体
Desc : 
"""
import datetime
import adult_comic_crawl.settings as settings
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
#from coolscrapy.settings import DATABASE
#
def db_connect():
    db_url = {
        'database': settings.MYSQL_DATABASE,
        'drivername': 'mysql+pymysql',
        'username': settings.MYSQL_USERNAME,
        'password': settings.MYSQL_PASSWORD,
        'host': settings.MYSQL_HOST,
        'query': {'charset': 'utf8'},  # the key-point setting
    }

    return create_engine(URL(**db_url), encoding="utf8",max_overflow=4)

def create_news_table(engine):
    """"""
    Base.metadata.create_all(engine)

def _get_date():
    return datetime.datetime.now()
Base = declarative_base()

class Comic_Info_18(Base): #这个参数父类名
    __tablename__='18comic_data' #存储岗位基本信息的数据表
    __table_args__ = {'mysql_charset': "utf8"}
    id=Column(Integer,primary_key=True)
    comic_title=Column(String(50))
    comic_author=Column(String(50))
    comic_cover=Column(String(200))

class Comic_Content_18(Base): #这个参数父类名
    __tablename__='18comic_content' #存储岗位基本信息的数据表
    __table_args__ = {'mysql_charset': "utf8"}
    id=Column(Integer,primary_key=True)
    comic_title=Column(String(50))
    chapter_id=Column(String(50))
    comic_content=Column(String(200))
