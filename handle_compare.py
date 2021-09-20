import cv2
import numpy as np

path = './'
# path = '/home/robit/VS_workspace/capstone/'
a = cv2.imread(path + 'handle_after_binary.jpg')
dst = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
ret, dst = cv2.threshold(dst, 100, 255, cv2.THRESH_BINARY)
cv2.imshow("dst", dst)
x, y = dst.shape[0], dst.shape[1]
q = 0
for i in dst:
    q += np.count_nonzero(i)
print(q)
print(x, y, x*y)
print(1 - q/(x*y))
cv2.waitKey()
cv2.destroyAllWindows()