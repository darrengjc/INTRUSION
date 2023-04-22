import face_recognition
import cv2
import numpy as np
import os
import json

AuthFailCount = 0

def faceRecog():
    directory = '../INTRUSION/Images/'
    # Get a reference to webcam #0 (the default one)

    global detection
    global name
    global AuthFail
    global AuthFailCount

    AuthFail = False
    detection = False

    video_capture = cv2.VideoCapture(0)

    # Load a sample picture and learn how to recognize it.
    for filename in os.listdir(directory):
        face_enc_cnt = 0
        f = os.path.join(directory,filename)
        face_recognition.load_image_file(f)

    with open("userList.json",'r') as f:
        userData = json.loads(f.read())

    darren_faceImg = face_recognition.load_image_file("../INTRUSION/Images/darren.jpg")
    darren_face_Enc = face_recognition.face_encodings(darren_faceImg)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        darren_face_Enc
    ]
    known_face_names = [
        "Darren Goh"
    ]

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        
        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                detection = True
                
            if False in matches:
                name = "Unknown"
                AuthFail = True

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
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

    print("Person detected is: ", name)
    
