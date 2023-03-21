import cv2
import numpy as np

# 이미지를 불러오고 전처리
img = cv2.imread('./picture/question5.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# 윤곽선 찾기
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contour_idx_list = list(range(len(contours)))
sorted_contours = [contours[i] for i in sorted(contour_idx_list, key=lambda x: cv2.boundingRect(contours[x])[0])]

boxes = []
for cnt in sorted_contours:
    area = cv2.contourArea(cnt)
    if 500 > area > 300:
        x,y,w,h = cv2.boundingRect(cnt)
        boxes.append((x,y,w,h))

boxes = sorted(boxes, key=lambda coord: coord[1])
newBoxes = sorted(boxes, key=lambda coord: coord[0])
    
for j in range(5):
    x, y, w, h = boxes[j]
    question_img = img[y:y+h, x:x+w]
    cv2.imwrite("./picture/question{}.jpg".format(j+1), question_img)

results = []
for j in range(len(newBoxes)):
    x,y,w,h = newBoxes[j]
    roi = gray[y:y+h, x:x+w]
    total_pixels = roi.shape[0] * roi.shape[1]
    black_pixels = total_pixels - cv2.countNonZero(roi)
    if black_pixels > total_pixels/2:
        results.append(j+1)

print("results :", results)

// 호고동