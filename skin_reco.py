import numpy as np
import cv2

def filter_skin(area, lower_range, upper_range):
    skinkernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    hsv = cv2.cvtColor(area, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_range, upper_range)
    mask = cv2.erode(mask, skinkernel, iterations = 1)
    mask = cv2.dilate(mask, skinkernel, iterations = 1)
    mask = cv2.GaussianBlur(mask, (15,15), 1)
    result = cv2.bitwise_and(hsv, hsv, mask = mask)
    result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    return result

def main():
    # load haar file for face detection
    face_cascade = cv2.CascadeClassifier('haar/haarcascade_frontalface_default.xml')

    # start camera
    cap = cv2.VideoCapture(0)

    while(1):
        # read frame from camera
        ret, frame = cap.read()

        # draw region of interest
        cv2.rectangle(frame, (100,100), (300,300), (0,0,255), 1)
        area = frame[100:300, 100:300]

        # detect faces
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi = frame[y:y+h, x:x+w]

            # get hsv color of the face
            h,w,c = roi.shape
            color = roi[int(h/2), int(w/2)]
            bgr = np.uint8([[color]])
            hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

            # define skin color range based on face color
            lower_range = np.array(hsv-[10,100,100])
            upper_range = np.array(hsv+[10,255,255])

            # filter region of interest with skin color range
            result = filter_skin(area, lower_range, upper_range)
            cv2.imshow('skin filter', result)

        cv2.imshow('camera', frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
