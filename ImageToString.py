# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 17:09:23 2020

@author: gmot8
"""
from datetime import datetime
from PIL import Image
import sys
import re
import pyocr
import pyocr.builders

import argparse
import cv2
class Image_to_string:
    def image_to_string(self,image):
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            print("No OCR tool found")
            sys.exit(1)
        # The tools are returned in the recommended order of usage
        tool = tools[0]
        txt = tool.image_to_string(
            self.cv2pil(image),#opencv型のimageからpil型に変換
            lang="jpn",
            builder=pyocr.builders.TextBuilder(tesseract_layout=6)
        )
        return txt
    def cv2pil(self,image):#
        ''' imageをOpenCV型 -> PIL型にするためのもの'''
        new_image = image.copy()
        if new_image.ndim == 2:  # モノクロ
            pass
        elif new_image.shape[2] == 3:  # カラー
            new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
        elif new_image.shape[2] == 4:  # 透過
            new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
        new_image = Image.fromarray(new_image)
        return new_image

    
    def images2strings(self,images):
        lst =[]
        for image in images:
            txt = self.image_to_string(image)
            if txt:
                lst.append(txt)
        return lst

    def strigs2dict(self,string_list):
        dict={
            "shop":"FamilyMart",
            "adress":"",
            "date":datetime.now(),
            "item":{
            },
            "total_price":0,
        }
        dict["shop"]=string_list[0]
        dict["adress"]=string_list[1]
        
        for string in string_list:
            if  "\\" in string:
                if '計' in string: 
                    dict["total_price"]=string.split('\\')[-1]
                    break
                name=string.split('\\')[-2]
                dict['item'][name]=string.split('\\')[-1]
            if '月' in string:
                dict["date"]=string
        return dict

if __name__ == "__main__":
    pass
    from CutReceipt import CutReceipt
    import matplotlib.pyplot as plt
    cr=CutReceipt('IMG_2BCE1EB797B2-1.JPG')
    images=cr.cut_image()
    i2s=Image_to_string()
    lst=i2s.images2strings(images)
    for string in lst:
        print(string)
    print(i2s.strigs2dict(lst))