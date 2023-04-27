from flask import Flask

app = Flask(__name__)

@app.route('/')
def intro_msg():
   return "Everything's Safe!"

def intrusion():
   import face_recog
   import cv2
   if face_recog.intruderFlag:
      print("Intruder Alert")
      cv2.imshow(face_recog.intruders)
      print("Time of Intrusion:{})".format(face_recog.intruderFlag_DT))
      
if __name__ == '__main__':
   app.run()