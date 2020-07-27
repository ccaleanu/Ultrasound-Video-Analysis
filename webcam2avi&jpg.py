import cv2
import time

capture = cv2.VideoCapture(1)
time.sleep(2)
size = (int(capture.get(3)),int(capture.get(4)))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video = cv2.VideoWriter('output.avi',fourcc,30,size)
print(capture.isOpened())
num=0

while True:
    ret, img = capture.read()
    video.write(img)
    cv2.imshow('video',img)
    cv2.imwrite("image" + str(num) + ".jpg",img)
    num = num + 1
    key= cv2.waitKey(1)
    if  key == ord('q'):
        num=0
        break

video.release()
capture.release()
cv2.destroyAllWindows() 
