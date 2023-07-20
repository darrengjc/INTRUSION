<<<<<<< Updated upstream
from flask import Flask
=======
# from flask import Flask, render_template
# import face_recog
# from PIL import Image

# app = Flask(__name__)
# app.debug = False

# @app.route('/')
# def index():
#     return render_template('intruder.html', intruder_img=None, stringMsg="Check for Intrusions")

# @app.route('/flag')
# def flag():
#     if face_recog.intruderFlag:
#         print("Intruder Alert")
#         intruder_img = face_recog.intruders[0]
#         im = Image.open(intruder_img)
#         im.show()
#         stringMsg = "INTRUDER DETECTED! Time of Intrusion: {}".format(face_recog.intruderFlag_DT)
#         return render_template('intruder.html', stringMsg=stringMsg)
#     else:
#         return render_template('intruder.html', stringMsg="Intruder Found")

# if __name__ == '__main__':
#     app.run()

from flask import Flask, render_template, redirect
>>>>>>> Stashed changes
import face_recog
from PIL import Image
import face_recog

app = Flask(__name__)
app.debug = False

@app.route('/')
<<<<<<< Updated upstream

def index():
   if face_recog.intruderFlag:
      print("Intruder Alert")
      intruder_img = face_recog.intruders[0]
      im = Image.open(intruder_img)
      im.show()
      stringMsg = "INTRUDER DETECTED! Time of Intrusion:{}".format(face_recog.intruderFlag_DT)
   return stringMsg

=======
def index():
    if face_recog.intruderFlag:
        return redirect('/flag')  # Redirect to /flag route if intruderFlag is True
    else:
        return render_template('intruder.html', stringMsg="No Intruders")

@app.route('/flag')
def flag():
    if face_recog.intruderFlag:
        print("Intruder Alert")
        #intruder_img = face_recog.intruders[0]
        stringMsg = "INTRUDER DETECTED! Time of Intrusion: {}".format(face_recog.intruderFlag_DT)
        return render_template('intruder.html',intruder=True, stringMsg=stringMsg)
    else:
        return render_template('intruder.html', stringMsg="False Detection")
    
@app.route('/displayImg')
def displayImg():
    intruder_img = face_recog.intruders[0]
    im = Image.open(intruder_img)
    im.show()

if __name__ == '__main__':
    app.run()
>>>>>>> Stashed changes
