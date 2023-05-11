from flask import Flask
import face_recog
from PIL import Image

app = Flask(__name__)
app.debug = False

@app.route('/')

def index():
   if face_recog.intruderFlag:
      print("Intruder Alert")
      intruder_img = face_recog.intruders[0]
      im = Image.open(intruder_img)
      im.show()
      stringMsg = "INTRUDER DETECTED! Time of Intrusion:{}".format(face_recog.intruderFlag_DT)
   return stringMsg
