# -*- coding: utf-8 -*-
class A:
     def add(self, x):
         y = x+1
         print(y)
class B(A):
    def add(self, x):
        super().add(x)
b = B()
b.add(2)  # 3


# table
# 漫畫資訊： uuid、name、author(非唯一）、publish_date、views

# table2
# 漫畫圖片： uuid、chapter、photo_path(image base64)

# p.s : photo_path，找Ｓ３的ＡＷＳ ＳＤＫ存入