import speech_recognition as sr
import pyttsx3
import face_recog

spchAuthFxCnt = 0

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

        if audioText == "1356":
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