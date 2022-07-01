# -*- coding: utf-8 -*-
# import os
# from unicodedata import name
# import requests
# import time # 引入time
# import requests
# from lxml import etree
# import re
# from fake_useragent import UserAgent
# from PIL import Image
# import pymysql
import hashlib
import json
import re
# comic_id = 14617
# cover_list = ["https://cdn-msp.18comic.vip/media/albums/blank.jpg","https://cdn-msp.18comic.vip/media/albums/256394_3x4.jpg?v=1655698199"]
# for i in cover_list:
#     if re.match('.*/blank.jpg',i):
#         print(f"{i.split('blank.jpg')[0]}{comic_id}_3x4.jpg?_v=1655698199")
#     else:
#         print(i)
# a = ['full/67966a51a50cb69e48d18a241e9e045aa2ba0590.jpg']
# print(a[0].split('/')[1] )
# class A:
#      def add(self, x):
#          y = x+1
#          print(y)
# class B(A):
#     def add(self, x):
#         super(B, self).add(x)
# b = B()
# b.add(2)  # 3
path = "https://cdn-msp.18comic.vip/media/albums/85250_3x4.jpg?_v=1656502977"
x = re.split('albums/', path)
print(x[1].split('?_')[0])

chapter_list = ['/photo/291396', '/photo/292822', '/photo/293874', '/photo/297097', '/photo/298582', '/photo/299170', '/photo/300011', '/photo/301463', '/photo/303021', '/photo/304464', '/photo/306006', '/photo/308443', '/photo/310021', '/photo/314455', '/photo/315928', '/photo/318149', '/photo/319723', '/photo/321965', '/photo/324046', '/photo/325949', '/photo/330252', '/photo/332046', '/photo/333694', '/photo/335458', '/photo/337194', '/photo/339467', '/photo/341265', '/photo/343519', '/photo/345550', '/photo/346786', '/photo/347940', '/photo/351909', '/photo/351825', '/photo/354391']

for i,j in enumerate(chapter_list):
    print(i+1,j)

    # print(f"{i.split('blank.jpg')[0]}{comic_id}_3x4.jpg?_v=1655698199")

# a = "H的玩具~追求刺激的愛~ / 玩具大師 [Doya/zeplin]エッチなオモチャ〜刺激的な愛を求めて〜 [禁漫天堂]"
# b = ['夏黑', '醃蘿蔔']
# # x = json.dumps(b,ensure_ascii=False)
# p = []
# w = {}
# for i,j in enumerate(b):
#     w[f'author{i+1}'] = j

# x = json.dumps(w,ensure_ascii=False)

# print(x)

# # 轉換日期格式至UNIX
# def time_trans(qurey_date):
#     struct_time = time.strptime(qurey_date, "%Y-%m-%d %H:%M:%S") # 轉成時間元組
#     time_stamp = int(time.mktime(struct_time)) # 轉成時間戳
#     return time_stamp

# time_params = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# ua = UserAgent()
# public_headers={
#    'cookie':'__cfduid=d3af1fe4e02395143768f49120192d89a1612161290; _gid=GA1.2.537470263.1612161292; shunt=1; AVS=pgucjspmo4rgafa4vinl3feug4; ipcountry=TW; ipm5=ad96616d894884f20b4e263448a05911; _ga_YYJWNTTJEN=GS1.1.1612339484.9.1.1612339785.59; _gat_ga0=1; _gat_ga1=1; _ga=GA1.2.2093487367.1612161292; _gat_gtag_UA_99252457_3=1; cover=1; _gali=chk_cover',
#     'User-Agent':ua.random
# }


# url = "https://18comic.org/albums/hanman?o=mv"
# res = requests.get(url, headers = public_headers).text
# res_parse = etree.HTML(res)
# # 熱門漫畫頁

# # for i in res_parse.xpath("//div[@class='thumb-overlay-albums']/a/@href"):
# #     print("https://18comic.org" + i)
# comic_address = res_parse.xpath("//div[@class='thumb-overlay-albums']/a/@href")[0]
# comic_url = "https://18comic.org" +  comic_address
# comic_id = comic_address.split('/')[2]
# comic_res = requests.get(comic_url, headers = public_headers ).text
# comic_res_parse = etree.HTML(comic_res)
# title = comic_res_parse.xpath("(//div[@class='panel-heading'])[2]/text()")
# # 章節（第...話)
# chapter_url =  "https://18comic.org" + comic_res_parse.xpath("(//div[@class='episode'])[3]/ul/a/@href")[0]
# chapter_res = requests.get(chapter_url, headers = public_headers ).text
# chapter_res_parse = etree.HTML(chapter_res)
# photo_id = chapter_res_parse.xpath("//div[@class='center scramble-page']/@id")
# # https://cdn-msp.18comic.org/media/photos/180459/00001.jpg?v=1655736355
# # 拼接圖片網址
# for i in photo_id:
#     jpg_url = f"https://cdn-msp.18comic.org/media/photos/{comic_id}/{i}?={time_trans(time_params)}"
#     jpg = requests.get(jpg_url, headers = public_headers )


#     with open("jpg_folder/" + i , "wb") as file:  # 開啟資料夾及命名圖片檔
#         file.write(jpg.content)  # 寫入圖片的二進位碼




# try:
#     db = pymysql.connect(
#         host=MYSQL_HOST,
#         db=MYSQL_DATABASE,
#         user=MYSQL_USERNAME,
#         passwd=MYSQL_PASSWORD,
#         charset='utf8'
#     )
#     cursor = db.cursor()
#     sql = f'SELECT id FROM new_table ORDER BY id DESC ;'
    
#     #執行語法
#     cursor.execute(sql)
#     #選取第一筆結果
#     data = cursor.fetchone()
#     if data :
#         data = ''.join(data)
#         db.close()

# except Exception as error:
#     print("============")
#     print("資料庫連線異常")
#     print(error)
#     print("============")


# table
# 漫畫資訊： uuid、name、author(非唯一）、publish_date、views

# table2
# 漫畫圖片： uuid、chapter、photo_path(image base64)

# p.s : photo_path，找Ｓ３的ＡＷＳ ＳＤＫ存入