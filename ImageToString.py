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
class ImageToString:
    def image_to_string(self,image):
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            print("No OCR tool found")
            sys.exit(1)
    # The tools are returned in the recommended order of usage
        tool = tools[0]
        txt = tool.image_to_string(
            self.cv2pil(image),#opencv型のimageからpilのimage型に変換
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



image=cv2.imread("trimmed_image.png")
txt = ImageToString().image_to_string(image)
print(txt)
'''
# txt is a Python string
parser = argparse.ArgumentParser(description='tesseract ocr test')
parser.add_argument('image', help='./image/img.jpg')

args = parser.parse_args()

res = tool.image_to_string(Image.open('./image/img.jpg'),
                           lang="jpn",
                           builder=pyocr.builders.WordBoxBuilder(tesseract_layout=6))

# draw result 
out = cv2.imread('./image/img.jpg')
for d in res:
    print( d.content)
    print( d.position)
    cv2.rectangle(out, d.position[0], d.position[1], (0, 0, 255), 2)

cv2.imshow('image',out)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''