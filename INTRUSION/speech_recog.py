import speech_recognition as sr
import pyttsx3
import face_recog
from datetime import datetime
import pandas as pd
import random
from pushbullet import Pushbullet

spchAuthFxCnt = 0

# speech code OTP
def renewCode(token):
    pb = Pushbullet(token)

    # date delta
    with open("../INTRUSION/INTRUSION/dateChecker.txt", 'r') as file:
        last_date = datetime.strptime(file.read(), "%d-%m-%y")
        now_date = datetime.now()
        d1 = pd.to_datetime(now_date).date()
        d2 = pd.to_datetime(last_date).date()
        print(d1)
        print(d2)
        deltaDate = d1-d2
        d3 = deltaDate.days
        print(d3)

        #renew the speech OTP code every day or every time and send to user via bullet notification.
        #this code is designed to be an adjustable-time OTP renewal
        if d3 == 0:
            #instantiate speech code file on the spot and destroy after
            with open("../INTRUSION/INTRUSION/speechCode.txt", 'w') as file:
                speechCode = random.randint(1000,3000)
                file.write(str(speechCode))

            pb.push_note("Your Speech Code OTP Is:", str(speechCode))
            with open("../INTRUSION/INTRUSION/dateChecker.txt", 'w') as file:
                file.write(datetime.now().strftime("%d-%m-%y"))



# convert text to speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# transcribes and verifies spoken code
def codeVerify():

    global spchSuccess
    global spchAuthSx
    global spchAuthFx
    global spchAuthFxCnt

    spchSuccess = False
    spchAuthSx = False
    spchAuthFx = False
    
    while(1):
        recog = sr.Recognizer()
        micIn = sr.Microphone()

        with micIn as source:
            recog.adjust_for_ambient_noise(source,duration=0.2)
            audioInput = recog.listen(source)

            print("Verifying")

            audioText = recog.recognize_google(audioInput, language='en-US')

        print("Code Received: ", audioText)

        with open("../INTRUSION/INTRUSION/speechCode.txt", 'r') as file:
            speechCode = file.read()

        if audioText == speechCode:
            spchSuccess = True
            print(spchSuccess)
        else: 
            spchSuccess = False 
            print(spchSuccess)

        if spchSuccess == True:
            SpeakText(audioText)
            SpeakText("Verified Code, Entry Granted")
            SpeakText(face_recog.name)
            spchAuthSx = True
            break

        if spchSuccess == False:
            SpeakText(audioText)
            SpeakText("Wrong Code, Access Denied")
            spchAuthFx = True

        if spchAuthFx:
            spchAuthFxCnt += 1
            print("Number of tries: ", spchAuthFxCnt)
            break