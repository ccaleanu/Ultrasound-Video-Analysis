import matplotlib.pyplot as plt
import cv2
import os
import re

#script_dir = os.path.dirname(__file__)

file = './Samples/UMF/a'
# Configure VideoCapture class instance for using file input.
capture = cv2.VideoCapture(file+'.avi')
property_id = int(cv2.CAP_PROP_FRAME_COUNT)
length = int(cv2.VideoCapture.get(capture, property_id))
# Initialize plot.
fig, ax = plt.subplots()
ax.set_title('Intensity in video')
ax.set_xlabel('Frames')
ax.set_ylabel('Level')
ax.set_xlim(0, length)
ax.set_ylim(0, 255)
plt.ion()
plt.show()
plt.autoscale(enable=True, axis='y')
#Read the ROI
# Open the file for reading.
with open(file+'.txt', 'r') as infile:
    data = infile.read()  # Read the contents of the file into memory.
# Return a list of the lines, breaking at line boundaries.
rlines = data.splitlines()
r = [x.split() for x in rlines];
# Grab, process, and display video frames. Update plot line object(s).
y = []
idxROI = 0;
idxFrame = 1;

while True:
    (grabbed, frame) = capture.read()
    if frame is None:
        break

    idxRow = idxROI + 1;
    if idxRow == len(r):
        idxRow = len(r)-1;

    if idxFrame >= int(r[idxRow][0]):
        if idxROI<len(r)-1:
            idxROI=idxROI+1;

    x0 = int(r[idxROI][3])
    y0 = int(r[idxROI][2])
    x1 = int(r[idxROI][5])
    y1 = int(r[idxROI][4])

    cv2_im = cv2.rectangle(frame, (y1 + y0, x1 + x0), (y0, x0), (0, 255, 0), 2)
    cv2.putText(frame, str(length), (10, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.putText(frame, str(idxFrame), (60, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.putText(frame, str(idxROI), (100, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.imshow('RGB', frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imCrop = gray[int(r[idxROI][3]):int(r[idxROI][3])+int(r[idxROI][5]), int(r[idxROI][2]):int(r[idxROI][2])+int(r[idxROI][4])]
    cv2.imshow('ROI', imCrop)
    y = y + [gray.mean()]
    idxFrame=idxFrame+1;
    plt.plot(y, 'b')
    plt.show()
    fig.canvas.draw()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
capture.release()
cv2.destroyAllWindows()