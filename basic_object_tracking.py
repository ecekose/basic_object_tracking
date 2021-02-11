# importing required packages
import cv2
import time

# defining video path 
video_path = r'C:...' 
# open video 
camera = cv2.VideoCapture(video_path)

# getting frame per second
fps= int(camera.get(cv2.CAP_PROP_FPS))

print("Fps:", fps)

# in case of video path does not open, any device, which your computer already has, will open 
if not camera.isOpened():
    print("video path can't be found, webcam is opening...")
    camera = cv2.VideoCapture(0)

# adjusting color range for HSV color space to recognize red dot or region
colorRanges = [
    ((161, 155, 84), (179, 255, 255), "red dot")]

# while loop
while True:
    # reading frames
    (retval, frame) = camera.read()
    # converting BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # thresholding
    for (lower, upper, colorName) in colorRanges:
        # morphological operations
        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.erode(mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=1)
        # finding contours
        cnts= cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        if cnts is None:
            continue
        else:
            # if function finds at least one contour
            if len(cnts) > 0:
                # labelling red object which has the biggest area
                c = max(cnts, key=cv2.contourArea)
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.putText(frame, colorName, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
            else: 
                continue

    # remove comment row in below to see video as usual 
    #time.sleep(1/fps)
    
    # displaying frames
    cv2.imshow("Object Tracking", frame)
    
    # press 'q' button to close the window
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()
