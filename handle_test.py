#!/usr/bin/env python
from opencv_header import *

def onChange(pos):
    pass

if __name__ == "__main__":
    global path
    path = './'
    # path = '/home/robit/VS_workspace/capstone/'
    # path = './'
    # capture = cv2.VideoCapture(-1)
    # capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    src = cv2.imread(path + "handle_before.jpg", cv2.IMREAD_COLOR)
    src = cv2.resize(src, dsize=(640, 480), interpolation=cv2.INTER_AREA)

    cv2.namedWindow("img_binary")

    cv2.createTrackbar("g_scale", "img_binary", 0, 255, onChange)

    cv2.setTrackbarPos("g_scale", "img_binary", 27)

    while cv2.waitKey(33) != ord('q'):
        # ret, frame = capture.read()
        # cv2.imshow("VideoFrame", frame)
        height, width, channel = src.shape

        g_scale = cv2.getTrackbarPos("g_scale", "img_binary")


        img_binary = Grayscale(src, g_scale)
        cv2.imshow('img_binary', img_binary)


        if cv2.waitKey(33) == ord('r'):
            cv2.setTrackbarPos("g_scale", "img_contourBox", 27)

    capture.release()
    cv2.destroyAllWindows()
