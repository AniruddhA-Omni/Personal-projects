import cv2
img1 = cv2.imread('assets/2.jpg', 1)
img2 = cv2.imread('assets/pokemon1.jpg',1)

tag=img1[200:400,550:750]
img2[300:500,250:450] = tag
cv2.imshow("IMG",img2)
cv2.waitKey(0)
cv2.destroyAllWindows()