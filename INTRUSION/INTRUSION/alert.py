from flask import Flask, render_template, redirect
import face_recog
from PIL import Image
import face_recog

app = Flask(__name__)
app.debug = False

@app.route('/')
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
        return redirect('/')
    
@app.route('/displayImg')
def displayImg():
    intruder_img = face_recog.intruders[0]
    im = Image.open(intruder_img)
    im.show()
    return redirect('/flag')

if __name__ == '__main__':
    app.run()
