#%%
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
# 画像の読み込み
im = cv2.imread('IMG_2BCE1EB797B2-1.JPG')
image=cv2.imread('IMG_2BCE1EB797B2-1.JPG')
# グレイスケールに変換しぼかした上で二値化する 
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

# 輪郭を抽出 --- (※1)
contours = cv2.findContours(
    thresh,      
    cv2.RETR_EXTERNAL, 
    cv2.CHAIN_APPROX_SIMPLE)[0]
x=[cv2.boundingRect(c)[0] for c in contours]
y=[cv2.boundingRect(c)[1] for c in contours]
w=[cv2.boundingRect(c)[2] for c in contours]
h=[cv2.boundingRect(c)[3] for c in contours]
"""for cnt in contours:# 抽出した領域を繰り返し処理する 
    x, y, w, h = cv2.boundingRect(cnt) # --- (※5)
    if h < 10: continue # 小さすぎるのは飛ばす
    cv2.rectangle(im, (x, y), (x+w, y+h), (0,0,255), 2)
#plt.plot(y)"""
plt.scatter(x,y)

plt.show()
cv2.imwrite('numbers100-cnt2.png',im)

#%%
trimmed_image=image[765:810,]
cv2.imwrite("trimmed_image.png", trimmed_image)

# %%
print(trimmed_image.shape)

# %%
im.shape


# %%
