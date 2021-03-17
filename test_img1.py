from opencv_header import *

if __name__ == "__main__":
    src = cv2.imread("./images/1.jpg", cv2.IMREAD_COLOR)
    src = cv2.resize(src, dsize=(640, 480), interpolation=cv2.INTER_AREA)
    height, width, channel = src.shape
    cv2.imshow("src", src)

    low = [7, 20, 160]
    high = [30, 140, 250]
    img_masked = mask(src, low, high)
    cv2.imshow("img_masked", img_masked)

    img_blur = Blurring(img_masked, 9)
    cv2.imshow('img_blur', img_blur)

    img_binary = Grayscale(img_blur, 100)
    cv2.imshow('img_binary', img_binary)

    contours, img_contour = draw_Contours(img_binary, height, width, channel)
    cv2.imshow('contours', img_contour)

    img_contourBox, angle, cart_size = draw_ContourBox(contours, 300, 3, src)
    cv2.imshow('img_contourBox', img_contourBox)

    cv2.waitKey()
    cv2.destroyAllWindows()
