# -*- coding: utf-8 -*-

from adult_comic_crawl.models import db_connect, create_news_table, Comic_Info_18, Comic_Content_18
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import adult_comic_crawl.settings
import scrapy
import time
from ..items import AdultComicCrawlItem, ComicContetITem
import hashlib
import json
import re
import requests

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
class A18comicSpider(scrapy.Spider):
    name = '18comic'
    download_timeout = 1
    allowed_domains = ['18comic.org']
    comic_data_items = AdultComicCrawlItem()
    comic_content_items = ComicContetITem()
    time_params = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    start_urls = ["https://18comic.org/albums/hanman?o=mv"]

    def parse(self, response):
        # 第一層 熱門漫畫頁，獲取(作品名稱、作者、作品封面到第一張table)，擷取作品連結，做另一個def去解析
        for i,j in  enumerate(response.xpath("//div[@class='thumb-overlay-albums']/a/@href")):
            category = re.split('[/?]', response.url)[-2]
            comic_link = response.xpath("//div[@class='thumb-overlay-albums']/a/@href")[i].extract() #作品連結
            comic_id = comic_link.split('/')[2] #作品ID,漫畫頁跟漫畫內容頁不同！！！
            # mac 擷取到的封面 https://cdn-msp.18comic.vip/media/albums/blank.jpg  需要找其他方式（拼接或找其他element) 
            # "https://cdn-msp.18comic.vip/media/albums/256394_3x4.jpg?v=1655698199"
            raw_comic_cover = response.xpath("//div[@class='thumb-overlay-albums']/a/img/@src")[i].extract() #封面
            # {comic_id}_3x4.jpg?_v={self.time_trans(self.time_params)}
            if re.match('.*/blank.jpg',raw_comic_cover):
                comic_cover_url = f"{raw_comic_cover.split('blank.jpg')[0]}{comic_id}_3x4.jpg?_v={self.time_trans(self.time_params)}" 
            else:
                comic_cover_url = raw_comic_cover

            comic_title = response.xpath("//span[@class='video-title title-truncate m-t-5']/text()")[i].extract() #作品名稱
            comic_author = response.xpath(f"(//div[@class='p-b-15 p-l-5 p-r-5']/div[contains(.,'作者')])[{i+1}]/a/text()").extract() #作者
            m = hashlib.md5()
            m.update(comic_title.encode("utf-8"))
            uuid_id = m.hexdigest()
            # 確認資料庫是否有漫畫相關資訊
            query = self.query_data('Info', uuid_id)
            if query:
                pass
            else:
                self.comic_data_items['category'] = category
                self.comic_data_items['comic_title'] = uuid_id
                self.comic_data_items['comic_author'] = json.dumps(comic_author, ensure_ascii=False)
                self.comic_data_items['comic_cover_urls'] = comic_cover_url
                yield self.comic_data_items
        # 第二層 某本漫畫頁 獲取( 章節數ID(有幾話)
            comic_url = "https://18comic.org" + comic_link
            
            yield scrapy.Request(comic_url, callback = self.get_chapter_url, dont_filter=True, meta = self.comic_data_items)


    def get_chapter_url(self, response):
        chapter_list = response.xpath("(//div[@class='col-lg-7']/div)[3]/div/ul/a/@href").extract()
        
        # 獲取章節網址、ＩＤ
        # for i,j in enumerate(chapter_list):
        #     print(i+1,j)

        meta = {'category':response.meta['category']}
        for i in range(2):
            if len(chapter_list) == 0 : 
                comic_href = response.xpath("((//div[@class='col-lg-7']/div)[2]/a)[1]/@href").extract()
                self.logging.error('檢查')
                self.logging.error('==================')
                self.logging.error(comic_href)
                self.logging.error(comic_href.split('/'))
                self.logging.error('==================')
                meta['comic_id'] = comic_href.split('/')[2]
                meta['comic_title'] = response.meta['comic_title']
                chapter_url = "https://18comic.org" + comic_href
                yield scrapy.Request(chapter_url, callback = self.get_content, dont_filter=True, meta = meta )
                break

            else:
                chapter_url =  "https://18comic.org" + chapter_list[i]
                meta['comic_id'] = chapter_list[i].split('/')[2]
                meta['chapter_id'] = i + 1
                meta['comic_title'] = response.meta['comic_title']
                yield scrapy.Request(chapter_url, callback = self.get_content, dont_filter=True, meta = meta )


    # 第三層 章節內頁 獲取(漫畫圖片)
    def get_content(self, response):
        # uuid(title)、chapter_id 章節數、page_id 獲取頁數 
        
        comic_id = response.meta['comic_id']
        photo_id_list = response.xpath("//div[@class='center scramble-page']/@id").extract()
        comic_title = response.meta['comic_title']

        # print(response.meta['chapter_id'])
        
        # https://cdn-msp.18comic.org/media/photos/180459/00001.jpg?v=1655736355
        # 拼接圖片網址
        for photo_id in photo_id_list:
            jpg_url = f"https://cdn-msp.18comic.org/media/photos/{comic_id}/{photo_id}?={self.time_trans(self.time_params)}"
            self.comic_content_items['category'] = response.meta['category']
            self.comic_content_items['comic_title'] = comic_title
            self.comic_content_items['chapter_id'] = response.meta['chapter_id']
            self.comic_content_items['comic_content'] = jpg_url
            self.comic_content_items['photo_id'] = photo_id
            yield self.comic_content_items

    # 轉換日期格式至UNIX
    def time_trans(self, qurey_date):
        struct_time = time.strptime(qurey_date, "%Y-%m-%d %H:%M:%S") # 轉成時間元組
        time_stamp = int(time.mktime(struct_time)) # 轉成時間戳
        return time_stamp

    def query_data(self, item, title):
        try:
            with session_scope(Session) as session:
                if item == 'Info':
                    query = session.query(Comic_Info_18).filter(Comic_Info_18.comic_title==title).all()
                elif item == 'Content':
                    query = session.query( func.max(Comic_Content_18.chapter_id) ).filter(Comic_Content_18.comic_title==title).group_by(Comic_Content_18.comic_title).one()[0]

                return query
        except Exception as error:
            print(error)
