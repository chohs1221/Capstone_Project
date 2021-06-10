import cv2
import numpy as np
import math

if __name__ == "__main__":
    with open("foo111.txt", "w") as f:
        f.write("Life is too short, you need python")
    src = cv2.imread("/home/robit/VS_workspace/capstone/images/1.jpg", cv2.IMREAD_COLOR)
    src = cv2.resize(src, dsize=(640, 480), interpolation=cv2.INTER_AREA)
    height, width, channel = src.shape
    cv2.imshow("src", src)
    with open("foo2.txt", "w") as f:
        f.write(str(height))

    cv2.waitKey()
    cv2.destroyAllWindows()