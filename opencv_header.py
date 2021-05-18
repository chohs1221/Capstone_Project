import cv2
import numpy as np
import math

# Blurring (src, kernel size) >> blured img
def Blurring(img, kernel_size):
    img_blur = cv2.blur(img, (kernel_size, kernel_size), anchor=(-1, -1), borderType=cv2.BORDER_DEFAULT)
    return img_blur

# Grayscale (src, threshold) >> grayscaled img
def Grayscale(img, thresh):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, binary = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
    binary = cv2.bitwise_not(binary)
    return binary

# Contour (src, height, width, channel) >> contour img
def draw_Contours(img, height, width, channel):
    contours, _ = cv2.findContours(
        img, 
        mode=cv2.RETR_LIST, 
        method=cv2.CHAIN_APPROX_SIMPLE
    )
    temp_result = np.zeros((height, width, channel), dtype=np.uint8)
    cv2.drawContours(temp_result, contours=contours, contourIdx=-1, color=(255, 255, 255))
    return contours, temp_result

# Mask (src, low, high) >> masked img
def mask(bgr, low, high):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    low_color = np.array([low[0], low[1], low[2]])
    high_color = np.array([high[0], high[1], high[2]])
    img_mask = cv2.inRange(hsv, low_color, high_color)
    return cv2.bitwise_and(bgr, bgr, mask = img_mask)

# ContourBox (contour, min_width, min ratio, src) >> contour box img
def draw_ContourBox(contours, min_width, min_ratio, src):
    angle = 0
    cart_size = 0
    for contour in contours:
        rect = cv2.minAreaRect(contour)
        if max(rect[1][0], rect[1][1]) > min_width and max(rect[1][0]/rect[1][1], rect[1][1]/rect[1][0]) > min_ratio:
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(src, [box], -1, (0, 255, 0), 2)
            for i in range(4):
                cv2.putText(src, "("+str(box[i][1])+", "+str(box[i][0])+")", (box[i][0], box[i][1]), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)
            #print("==========================================================")
            box_ = sorted(box, key = lambda x: x[0])
            dx = box_[2][0]-box_[0][0]
            dy = box_[0][1]-box_[2][1]
            angle = math.atan2(dy,dx) * 180 / math.pi
            cart_handle = max(rect[1][0], rect[1][1])
            if cart_handle < 400:
                cart_size = 100
            elif 400 <= cart_handle < 450:
                cart_size = 101
            elif 450 <= cart_handle:
                cart_size = 102
            #print("(x, y) = ({0})\n(width, height) = {1}\n(angle) = {2}".format(rect[0], rect[1], angle))
            #print(box)
            print(cart_handle)

    return src, angle, cart_size

if __name__ == "__main__":
    img = cv2.imread('5.jpg')
    height, width, channel = img.shape
    cv2.imshow('original', img)

    img_blur = Blurring(img, 15)
    cv2.imshow('img_blur', img_blur)
    img_binary = Grayscale(img_blur, 170)
    cv2.imshow('img_binary', img_binary)
    contours, img_contour = draw_Contours(img_binary, height, width, channel)
    cv2.imshow('contours', img_contour)
    img_contourBox = draw_ContourBox(img_contour, contours, 300, 3, height, width, channel)
    cv2.imshow('img_contourBox', img_contourBox)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
