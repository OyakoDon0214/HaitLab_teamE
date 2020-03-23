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

def Image_to_string():
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
# The tools are returned in the recommended order of usage
    tool = tools[0]
    txt = tool.image_to_string(
        Image.open('./image/img.jpg'),
        lang="jpn",
        builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    )
    return txt   

txt = Image_to_string()
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