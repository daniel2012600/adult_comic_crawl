import scrapy
import time
from ..items import AdultComicCrawlItem
import hashlib
import json
from PIL import Image
import re
class A18comicSpider(scrapy.Spider):
    name = '18comic'
    allowed_domains = ['18comic.org']
    items = AdultComicCrawlItem()
    time_params = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    start_urls = ["https://18comic.org/albums/hanman?o=mv"]
    def parse(self, response):
        # 第一層 熱門漫畫頁，獲取(作品名稱、作者、作品封面到第一張table)，擷取作品連結，做另一個def去解析
        self.logger.info(response.url)
        for i,j in  enumerate(response.xpath("//div[@class='thumb-overlay-albums']/a/@href")):
            comic_link = response.xpath("//div[@class='thumb-overlay-albums']/a/@href")[i].extract() #作品連結
            comic_id = comic_link.split('/')[2] #作品ID
            # mac 擷取到的封面 https://cdn-msp.18comic.vip/media/albums/blank.jpg  需要找其他方式（拼接或找其他element) 
            # "https://cdn-msp.18comic.vip/media/albums/256394_3x4.jpg?v=1655698199"
            raw_comic_cover = response.xpath("//div[@class='thumb-overlay-albums']/a/img/@src")[i].extract() #封面 (WIN可直接獲取)
            # {comic_id}_3x4.jpg?_v={self.time_trans(self.time_params)}
            if re.match('.*/blank.jpg',raw_comic_cover):
                comic_cover = f"{raw_comic_cover.split('blank.jpg')[0]}{comic_id}_3x4.jpg?_v={self.time_trans(self.time_params)}"  #封面 mac
            else:
                comic_cover = raw_comic_cover

            comic_title = response.xpath("//span[@class='video-title title-truncate m-t-5']/text()")[i].extract() #作品名稱
            comic_author = response.xpath(f"(//div[@class='p-b-15 p-l-5 p-r-5']/div[contains(.,'作者')])[{i+1}]/a/text()").extract() #作者
            m = hashlib.md5()
            m.update(comic_title.encode("utf-8"))
            uuid_id = m.hexdigest()
            self.items['comic_title'] = uuid_id
            # self.items['comic_author'] = json.dumps(comic_author, ensure_ascii=False)
            self.items['image_urls'] = comic_cover
            
            yield self.items
        # 第二層 某本漫畫頁 獲取( 章節數ID(有幾話)
            comic_url = "https://18comic.org" + comic_link
            
            yield scrapy.Request(comic_url, callback = self.get_chapter_url, dont_filter=True, meta = self.items)


    def get_chapter_url(self, response):
        
        # (//div[@class='col-lg-7']/div)[3]/div/ul/a/@href
        # title = response.xpath("//div[@class='panel-heading']/div/h1/text()").extract()
        chapter_list = response.xpath("(//div[@class='col-lg-7']/div)[3]/div/ul/a/@href").extract()

        # if len(chapter_list) == 0  點擊開始閱讀 直接獲取內容
        
        # for i,j in enumerate(chapter_list):
        #     print(i+1,j)
        # 獲取章節網址、ＩＤ
        for i in range(3):
            chapter_url =  "https://18comic.org" + chapter_list[i]
            response.meta['chapter_id']  = i + 1


            yield scrapy.Request(chapter_url, callback = self.get_content, dont_filter=True, meta = response.meta )


    def get_content(self, response):
        # uuid(title)、chapter_id 章節數、page_id 獲取頁數  ．．．meta?
        photo_id = response.xpath("//div[@class='center scramble-page']/@id").extract()
        print('*******')
        print(response.meta)
        
        # https://cdn-msp.18comic.org/media/photos/180459/00001.jpg?v=1655736355
        # 拼接圖片網址
        # for i in photo_id:
        #     jpg_url = f"https://cdn-msp.18comic.org/media/photos/{comic_id}/{i}?={time_trans(time_params)}"
        #     print(jpg_url)
            


# 第一層 熱門漫畫頁  獲取(作品名稱、作者、作品圖片)

# response

# 第二層 某本漫畫頁 獲取( 章節數ID(有幾話)



# 第三層 章節內頁 獲取(漫畫圖片)


# 拼接一次就新增一個DEF



    # 轉換日期格式至UNIX
    def time_trans(self, qurey_date):
        struct_time = time.strptime(qurey_date, "%Y-%m-%d %H:%M:%S") # 轉成時間元組
        time_stamp = int(time.mktime(struct_time)) # 轉成時間戳
        return time_stamp