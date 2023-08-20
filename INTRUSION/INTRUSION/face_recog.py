import face_recognition
import cv2
import os
import json
from pathlib import Path
from datetime import datetime
from sklearn.metrics.pairwise import euclidean_distances

AuthFailCount = 0
intruderFlag = False

def faceRecog():
    now = datetime.now()
    date_time = now.strftime("%m%d%Y_%H%M%S")
    directory = '../INTRUSION/INTRUSION/INTRUSION/Images/'

    global detection
    global name
    global AuthFail
    global AuthFailCount
    global intruders
    global intruderFlag_DT
    global face_dist_flag
    global intruderFlag
    
    AuthFail = False
    detection = False
    intruders = []
    flag_dt_format = now.strftime("%m/%d/%Y, %H:%M:%S")

    video_capture = cv2.VideoCapture(0)
    
    face_encs = []
    face_names = []

    # sorting paths by creation date
    sortedPath = sorted(Path(directory).iterdir(),key=os.path.getctime)
    print(sortedPath)

    # load the sorted paths for encoding list
    for sortedFiles in sortedPath: 
        faceImg = face_recognition.load_image_file(sortedFiles)
        faceEnc = face_recognition.face_encodings(faceImg)[0]
        face_encs.append(faceEnc)
    print(face_encs)

    with open("../INTRUSION/INTRUSION/INTRUSION/userList.json",'r') as f:
        userData = json.loads(f.read())
        for i in userData:
            face_names.append(i)
        print(face_names)

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Find all the faces and face encodings in the frame of video
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Calculate the center of the detected face
            face_center = (top + bottom) // 2, (left + right) // 2

            # Calculate the distance of the face from the camera position (you can use any appropriate distance metric)
            face_dist = euclidean_distances([face_center], [(frame.shape[0] // 2, frame.shape[1] // 2)])[0][0]

            if face_dist > 0 and face_dist < 70:
                face_dist_flag = True
                name = "Too Far"
                print(face_dist)
                
            if face_dist > 70:
                face_dist_flag = False
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(face_encs, face_encoding)

                # If a match was found in face_encs, just use the first one.
                if True in matches:
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}
                    for i in matchedIdxs:
                        # Check the names at respective indexes we stored in matchedIdxs
                        name = face_names[i]
                        print(name)
                        # Increase count for the name we got
                        counts[name] = counts.get(name, 0) + 1
                        print(counts)
                    # Set name which has the highest count
                    name = max(counts, key=counts.get)
                    detection = True
                    print(name, matches)
                    break

                if False in matches:
                    name = "Unknown"
                    AuthFail = True
                    detection = False
                    break

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Face Recognition', frame)

        # On detect, break
        if cv2.waitKey(1) & detection:
        #if detection:
            break

        if AuthFail:
            print("AuthFail. Unauthorized User.")
            AuthFailCount += 1
            print("Number of tries: ", AuthFailCount)
            if AuthFailCount >2:
                intruderFlag = True
                intruderFlag_DT = flag_dt_format
                print("Capturing Intruder Image")
                newIntruder = "../INTRUSION/INTRUSION/INTRUSION/IntruderImgs/intruder_flag_{}.png".format(date_time)
                intruders.append(newIntruder)
                cv2.imwrite(newIntruder, frame)
                print("{} captured".format(intruders))
                return intruderFlag
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

    print("Person detected is: ", name)
