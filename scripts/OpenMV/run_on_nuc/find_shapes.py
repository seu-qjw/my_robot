import cv2
import matplotlib.pyplot as plt
from helper import *


def ShapeDetection(img, imgContour, list1, list2, list3):
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    maxArea = -1
    loc = -1
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if (maxArea < area):
            maxArea = area
            loc = i

    if (loc > -1):
        obj = contours[loc]
        perimeter = cv2.arcLength(obj, True)
        approx = cv2.approxPolyDP(obj, 0.02*perimeter, True)
        CornerNum = len(approx)
        x, y, w, h = cv2.boundingRect(approx)
        objType = get_shape_name(CornerNum, w, h)

        ans1, ans2, ans3 = show_temperature_distribution(
            imgContour, x, y, w, h)
        list1.append(ans1)
        list2.append(ans2)
        list3.append(ans3)

        cv2.rectangle(imgContour, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cv2.putText(imgContour, objType, (x+(w//2), y+(h//2)),
                    cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 0), 1)
        print(CornerNum, area)
    else:
        list1.append(0)
        list2.append(0)
        list3.append(0)


def process_img(srcPath, dstPath, fileName, list1, list2, list3):
    imgGray = cv2.imread(srcPath+fileName+'.pgm', 0)
    imgContour = imgGray.copy()
    ret, imgBinary = cv2.threshold(
        imgGray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)

    conv_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    imgDilate = cv2.dilate(imgBinary, conv_kernel)
    imgErod = cv2.erode(imgDilate, conv_kernel)

    imgCanny = cv2.Canny(imgErod, 60, 60)
    ShapeDetection(imgCanny, imgContour, list1, list2, list3)

    cv2.imwrite(midPath+fileName+'_Gray.jpg', imgGray)
    cv2.imwrite(midPath+fileName+'_Binary.jpg', imgBinary)
    cv2.imwrite(midPath+fileName+'_Dilate.jpg', imgDilate)
    cv2.imwrite(midPath+fileName+'_Erod.jpg', imgErod)
    cv2.imwrite(midPath+fileName+'_Canny.jpg', imgCanny)
    cv2.imwrite(dstPath+fileName+'_Contour.jpg', imgContour)


collectList1 = []
collectList2 = []
collectList3 = []
path = '/home/yr/热成像数据_存档/2022_11_28_1100_tqyb17'
srcPath = path+'/raw/'
midPath = path+'/middleFile/'
dstPath = path+'/result/'
listName = './img_lists/vent.txt'

fp = open(listName, 'r')
filenames = [each.rstrip('\r\n') for each in fp.readlines()]
for fileName in filenames:
    process_img(srcPath, dstPath, fileName,
                collectList1, collectList2, collectList3)

fig = plt.figure(figsize=(4, 4), dpi=300)
x_lable = [int(each)/1000 for each in filenames]
plt.plot(x_lable, collectList1, marker='o', label="up")
plt.plot(x_lable, collectList2, marker='D', label="target")
plt.plot(x_lable, collectList3, marker='*', label="below")
plt.show()
