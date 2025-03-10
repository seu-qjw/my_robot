# 对图像进行水平方向的切片

import cv2
from helper import *


if __name__ == '__main__':
    read_path = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/'
    num_list = [421802, 444743]

    for num in num_list:
        image = cv2.imread(read_path+str(num)+".bmp")

        windowSize = (10, 120)
        for (x, y, window) in sliding_window(image, int(windowSize[0]/2), windowSize):
            if window.shape[0] != windowSize[1] or window.shape[1] != windowSize[0]:
                continue
            clone = image.copy()
            cv2.rectangle(
                clone, (x, y), (x + windowSize[0], y + windowSize[1]), (0, 255, 0), 2)
            cv2.imshow("Window", clone)
            cv2.waitKey(100)
