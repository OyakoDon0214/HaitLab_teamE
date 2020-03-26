# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 17:09:23 2020

@author: gmot8
"""

from PIL import Image
import sys

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

from CutReceipt import CutReceipt
import matplotlib.pyplot as plt
cr=CutReceipt('receipt_image.jpg')
images=cr.cut_image()

import os

# ファイル数を調べたいフォルダのパス
path = "./TestCutImageFolder" 

# フォルダ内の全ファイル名をリスト化
files = os.listdir(path)

lst =[]
for i in range(0,len(images)):
    path = "./TestCutImageFolder/" + files[i]
    image=cv2.imread(path)
    txt = Image_to_string().image_to_string(image)
    lst.append(txt)
print(lst)