from datetime import datetime
import cv2
from CutReceipt import CutReceipt

class ConvertReceipt:
    def __init__(self,image_pass):
        self.image=cv2.imread(image_pass)


    def convert(self):
        testdict={
            "shop":"FamilyMart一の橋店",
            "adress":"東京都港区麻布十番1-2-10",
            "date":datetime(2016,9,29,12,45),
            "item":{
                "十六茶":151,
                "ベーコン":198,
                "茶碗蒸し":133,
            },
            "total_price":460,
        }
        return testdict


if __name__=="__main__":
    image=cv2.imread("receipt_image.jpg")
    cr=CutReceipt(image)
    cr.save_cut_image('TestCutImageFolder')

    r=ConvertReceipt("receipt_image.jpg")
    dict=r.convert()
    print(dict["shop"])
