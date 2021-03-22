import json
import cv2
import os, glob

jsons_path = r"D:\repos\json_parse\3"
video_path = r"D:\repos\json_parse\3.avi"

jsons_file_list = []
for file in glob.glob(os.path.join(jsons_path, "*.json")):
    jsons_file_list.append(file)

jsons = []
for json_file in jsons_file_list:
    f = open(json_file)
    js = json.load(f)
    jsons.append(js)


# init tracker
def tracking(frame, bbox, tracker, init):
    if init:
        tracker.init(frame, bbox)
        init = False
    if bbox is not None:
        ok, box = tracker.update(frame)

        if ok:
            result = [int(v) for v in box]
            return result

    return bbox


tracker = cv2.TrackerCSRT_create()

cap = cv2.VideoCapture(video_path)

frame_counter = 0
fps = cap.get(cv2.CAP_PROP_FPS)
bbox = None

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    current_ts = frame_counter / 15
    # search for the right json to show
    is_found = False
    for json in jsons:
        # get timestamp
        json_ts = json["asset"]["timestamp"]
        if abs(current_ts - json_ts) < 0.001:
            # get bounding boxes
            cv2.putText(frame, "Got a match", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            regions = json['regions']
            for region in regions:
                points = region['points']
                tl = points[0]
                br = points[2]
                x_min = int(region['boundingBox']['left'])
                y_min = int(region['boundingBox']['top'])
                width = int(region['boundingBox']['width'])
                height = int(region['boundingBox']['height'])
                cv2.rectangle(frame, (x_min + 50, y_min + 50), (x_min + width, y_min + height), (255, 0, 0), 2)
                bbox = (x_min, y_min, width, height)
                is_found = True

    newBB = tracking(frame, bbox, tracker, is_found)
    if newBB is not None:
        x, y, w, h = newBB
        bbox = newBB
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.putText(frame, str(current_ts), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    # Display the resulting frame
    cv2.imshow('frame', frame)
    # if is_found:
    #     cv2.waitKey()
    if cv2.waitKey(15) & 0xFF == ord('q'):
        break
    frame_counter += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
