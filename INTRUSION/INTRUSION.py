import customtkinter
import face_recog
import face_register
import speech_recog
import json

# set main theme
customtkinter.set_appearance_mode("dark")  
customtkinter.set_default_color_theme("dark-blue")  

# define main windows
mainWindow = customtkinter.CTk()
mainWindow.geometry("400x400")
mainWindow.title("INTRUSION")

btnClicked = False

# set button and entry callbacks
# face recognition button callback: Run when face ID button is clicked.
def frcButton_callback():
    global btnClicked
    btnClicked = not btnClicked

    regisButton.pack_forget()

    if btnClicked:
        print(btnClicked)
        print("FRC ACCESSED")

    # call facial recognition function from facial recognition module
    face_recog.faceRecog()

    if face_recog.detection:
        spchButton.configure(state="enabled") 
        print("AuthSuccess")
        print(face_recog.name)
        frcButton.configure(state="disabled")
        response_entry.insert("0.0","AuthSuccess. Proceed to SPEECH ID.\n\n\n\n")

    if face_recog.AuthFail:
        frcButton.configure(state="enabled")
        response_entry.insert("0.0","AuthFail. Please try again.\n\n\n\n")

        # if authorization fail flag counts more than twice, trigger app lock
        if face_recog.AuthFailCount > 2:
            print("SecurityRiskDetected")
            response_entry.insert("0.0","Security Risk Detected. App locked.\n\n\n\n")
            intro_label.configure(text="INTRUDER DETECTED")
            spchButton.pack_forget()
            frcButton.pack_forget()

# speech button callback: Run when speech button is clicked.
def spchButton_callback():
    print("SPCH ACCESSED")

    # call speech code verification function from speech recognition module
    speech_recog.codeVerify()

    if speech_recog.spchAuthSx:
        print("Success Code")
        spchButton.pack_forget()
        frcButton.pack_forget()
        intro_label.pack_forget()
        customtkinter.set_appearance_mode("light")
        mainWindow.geometry("300x200")
        response_entry.configure(text_color="blue", border_color="blue")
        response_entry.insert("0.0","ENTRY GRANTED\n\n\n\n")

    # speech recognition fail flag check and count check till app lock
    if speech_recog.spchAuthFx:
        print("Failed Code")
        response_entry.insert("0.0","AuthFail. Please speak again.\n\n\n\n")

        if speech_recog.spchAuthFxCnt > 2:
            print("SecurityRiskDetected")
            response_entry.insert("0.0","Security Risk Detected. App locked.\n\n\n\n")
            intro_label.configure(text="INTRUDER DETECTED")
            spchButton.pack_forget()
            frcButton.pack_forget()

# login button callback: Run when login button is clicked.
def login_callback():
    print("password entered", pass_entry.get())

    uf = open("../INTRUSION/INTRUSION/userList.json")

    # load passes from json
    userData = json.load(uf)
    userPasses = userData.values()
    entered_pass = pass_entry.get()

    # check if pass is valid
    if entered_pass in userPasses:
        pass_entry.pack_forget()
        pass_button.pack_forget()
        intro_label.configure(text="Welcome Back")
        frcButton.configure(state="enabled", hover=True)
        regisButton.configure(state="enabled", hover=True)
        response_entry.insert("0.0","Please proceed to Facial Recognition.\n\n\n\n")
    else: response_entry.insert("0.0","Wrong Password Entered\n\n\n\n")

# register button callback: Run when register user button is clicked.
def regisButton_callback():

    # set global so we can access these variables across functions
    global name_set
    global pass_set
    global submit_btn
    global face_regis_btn

    print("user registration mode")

    spchButton.pack_forget()
    frcButton.pack_forget()
    pass_entry.pack_forget()
    pass_button.pack_forget()
    regisButton.pack_forget()

    intro_label.configure(text="USER REGISTRATION")
    
    name_set = customtkinter.CTkEntry(master=main_frame, placeholder_text="Enter Your Name")
    name_set.pack(pady=10, padx=10)

    pass_set = customtkinter.CTkEntry(master=main_frame, placeholder_text="Set Password")
    pass_set.pack(pady=10, padx=10)
    pass_set.configure(show="*")

    face_regis_btn = customtkinter.CTkButton(master=main_frame,command=face_regis_callback)
    face_regis_btn.pack(pady=10, padx=10)
    face_regis_btn.configure(text="Register Face ID")

    submit_btn = customtkinter.CTkButton(master=main_frame,command=submit_regis_callback,state="disabled")
    submit_btn.pack(pady=10, padx=10)
    submit_btn.configure(text="Submit")

    response_entry.insert("0.0","Face Registration:\nPlease look directly at the camera and \npress spacebar once ready.\n\n\n\n")

# face registration button callback: Run when face registration button is clicked.
def face_regis_callback():
    face_register.faceRegis()

    if face_register.pathCheck:
        response_entry.insert("0.0","Filename Exists\n\n\n\n")

    if not face_register.pathCheck:
        response_entry.insert("0.0","Face Registered\n\n\n\n")
        face_regis_btn.configure(state="disabled")
        submit_btn.configure(state="enabled")
        #should append file number to here

# submit button callback: Run when submit registration button is clicked.
def submit_regis_callback():

    # save the user input fields into json file
    with open("../INTRUSION/INTRUSION/userList.json",'r') as f:
        userData = json.loads(f.read())

    userData[name_set.get()] = pass_set.get()

    with open("../INTRUSION/INTRUSION/userList.json", 'w') as f:
        f.write(json.dumps(userData,sort_keys=False, indent=4, separators=(',', ': ')))

    customtkinter.set_appearance_mode("light")

    mainWindow.geometry("400x400")

    response_entry.configure(text_color="blue", border_color="blue")
    response_entry.insert("0.0","USER REGISTERED SUCCESSFULLY\n\n\n\n")

    submit_btn.pack_forget()
    face_regis_btn.pack_forget()
    submit_btn.pack_forget()
    pass_entry.pack_forget()
    name_set.pack_forget()
    pass_set.pack_forget()

    restart_btn = customtkinter.CTkButton(master=main_frame,command=reset_win_callback)
    restart_btn.pack(pady=10, padx=10)
    restart_btn.configure(text="Finish")

# finish button callback: Run when finish registration button is clicked.
def reset_win_callback():
    mainWindow.destroy()

# set the main window frame
main_frame = customtkinter.CTkFrame(master=mainWindow)
main_frame.pack(pady=20, padx=60, fill="both", expand=True)

#set main window label
intro_label = customtkinter.CTkLabel(master=main_frame, justify=customtkinter.LEFT,text="Verify Password")
intro_label.pack(pady=10, padx=10)

# password entry GUI initializer
pass_entry = customtkinter.CTkEntry(master=main_frame, placeholder_text="Password")
pass_entry.pack(pady=10, padx=10)
pass_entry.configure(show="*")

# login button GUI initializer
pass_button = customtkinter.CTkButton(master=main_frame, command=login_callback)
pass_button.pack(pady=10, padx=10)
pass_button.configure(text="Log In")

# facial recognition button GUI initializer
frcButton = customtkinter.CTkButton(master=main_frame, command=frcButton_callback)
frcButton.pack(pady=10, padx=10)
frcButton.configure(state="disabled", text="FACE ID")

# speech recognition button GUI initializer
spchButton = customtkinter.CTkButton(master=main_frame, command=spchButton_callback)
spchButton.pack(pady=10, padx=10)
spchButton.configure(state="disabled", text="SPEECH ID")  

# user registration button GUI initializer
regisButton = customtkinter.CTkButton(master=main_frame, command=regisButton_callback)
regisButton.pack(pady=10, padx=10)
regisButton.configure(state="disabled", text="REGISTER USER")  

# response box GUI initializer
response_entry = customtkinter.CTkTextbox(master=main_frame, width=300, height=70,activate_scrollbars=False)
response_entry.pack(pady=10, padx=10)  

# initialize main
if __name__=='__main__':
    mainWindow.mainloop()
