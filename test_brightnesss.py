import cv2
import random
import numpy as np
img = cv2.imread(r'D:\AI\Process_ScrewPartE_T9\yolov5\data\images\train\Cam_crop-16-05-2022_11-25-52.jpg')
bright =  np.ones(img.shape, dtype = 'uint8') * 40
brightinncress = cv2.add(img, bright)
filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
brightinncress = cv2.GaussianBlur(brightinncress, (3, 3), 0)
brightinncress = cv2.filter2D(brightinncress, -1, filter)
brightinncress = cv2.blur(brightinncress, (3, 3))

cv2.imwrite(r'D:\test.jpg', brightinncress)