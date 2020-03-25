#%%
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import copy

class CutReceipt:
    
    def __init__(self,receipt_image_pass):
        self.receipt_image_pass=receipt_image_pass
        self.receipt_image=cv2.imread(self.receipt_image_pass)
        self.contours=self.find_contours()
        self.cutting_lines=self.find_cutting_lines()
        self.height, self.width, self.channels=self.receipt_image.shape[:3]
        return

    def find_cutting_lines(self):
        cutting_lines=[]
        image=self.receipt_image
        # 抽出した領域を繰り返し処理する 
        contours=self.contours
        bound_rects=[cv2.boundingRect(c) for c in contours]
        #bound_rectsは(x,y,w,h)のリスト
        df_bound_rects=pd.DataFrame(bound_rects)
        df_bound_rects.columns = ['x','y','w','h']
        margin=int(df_bound_rects["h"].quantile()/4)
        self.half_letter_size=int(df_bound_rects["h"].quantile()/2)

        cutting_line_candidates=[df_bound_rects["y"][0]]#同じ行中の文字のy座標を入れておくリスト
        for cnt in contours:# 抽出した領域を繰り返し処理する 
            x, y, w, h = cv2.boundingRect(cnt)
            if (h<self.half_letter_size): continue # 小さすぎるの大きすぎるのは飛ばす
            if abs(cutting_line_candidates[-1]-y)<self.half_letter_size:#同じ行だったら
                cutting_line_candidates.append(y)
            else:#同じ行じゃなかったら
                if len(cutting_line_candidates)>4:#列に4文字以上あるなら
                    cutting_lines.append(int(sum(cutting_line_candidates)/len(cutting_line_candidates)))#平均値を追加
                cutting_line_candidates.clear()
                cutting_line_candidates.append(y)
        return cutting_lines
    
    def find_contours(self):
         # 画像の読み込み
        image=self.receipt_image
        # グレイスケールに変換しぼかした上で二値化する 
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
        # 輪郭を抽出 --- (※1)
        contours = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
        return contours

    def draw_cutting_lines(self):   
        image=copy.copy(self.receipt_image)
        for line in self.cutting_lines:
            cv2.line(image,(0,line),(self.width,line),(255,0,0),2)
        plt.imshow(image)
        plt.show()
        return image

    def cut_image(self):
        cut_images=[]
        image=copy.copy(self.receipt_image)
        line_queue=copy.copy(self.cutting_lines)
        line_queue.append(0)
        while len(line_queue)>2:
            upper=line_queue.pop()
            lower=line_queue[-1]
            cut_images.append(image[upper:lower])
        if len(line_queue)==1:
            cut_images.append(image[line_queue.pop():self.height])
        return cut_images

    def save_cut_image(self,folder_pass):
        for i,image in enumerate(self.cut_image()):
            file_pass='./'+folder_pass+'/cutimage'+str(i)+'.png'
            cv2.imwrite(file_pass,image)

    def draw_rect(self):
        image=copy.copy(self.receipt_image)
        for cnt in self.contours:# 抽出した領域を繰り返し処理する 
            x, y, w, h = cv2.boundingRect(cnt) # --- (※5)
            if h < 1: continue # 小さすぎるのは飛ばす
            cv2.rectangle(image, (x, y), (x+w, y+h), (0,0,255), 2)
        plt.imshow(image)
        plt.show()
        return image
  

if __name__ == "__main__":
    cr=CutReceipt('receipt_image.jpg')
    cr.draw_cutting_lines()
    cr.save_cut_image('TestCutImageFolder')
    print(len(cr.cut_image()))
   