import cv2
import os
import random

def faceRegis():

    global pathCheck
    global img_name
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("Face ID Registration")

    img_counter = random.randint(0,999)

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("Face Registration", frame)

        k = cv2.waitKey(1)
        if k%256 == 32:
            # SPACE pressed
            img_name = "../INTRUSION/INTRUSION/Images/face_id_{}.png".format(img_counter)
            pathCheck = os.path.exists(img_name)

            if not pathCheck:
                cv2.imwrite(img_name, frame)
                print("{} registered".format(img_name))
                break 

            elif pathCheck:
                print("filename exists")
                break
             
    cam.release()

    cv2.destroyAllWindows()