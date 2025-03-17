import os.path
import subprocess
import datetime
import tkinter as tk
import util
import cv2
from PIL import Image, ImageTk
from tkinter import Canvas
import pyttsx3
import time




class App:
    def __init__(self): #constructor  initializing our app
        self.main_window = tk.Tk() # creating our main window
        self.main_window.geometry("1200x520+350+100") # size of the window AND X Y POSITION
        self.main_window.configure(bg="#1f1f1f") # bg color

        # 323232
        self.main_window.title("FaceRec") # title name

        self.canvas = Canvas(self.main_window, width=1100, height=600, bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=2, pady=20)
        self.canvas.configure(bg="#1f1f1f")

        self.engine = pyttsx3.init()  # Initialize text-to-speech engine
        self.set_voice()  # Set female voice and adjust properties

        # Ensure correct image path
        image_path = os.path.join(os.path.dirname(__file__), "logo", "image1.png")

        if not os.path.exists(image_path):
            print("ERROR: Image file not found at", image_path)
        else:
            self.img_file = Image.open(image_path)
            self.img_file = self.img_file.resize((370, 220))
            self.img = ImageTk.PhotoImage(self.img_file)


            # Calculate x position to be at the top-right
            window_width = 1100  # Match window width
            image_width = 370  # Image width after resizing
            x_position = window_width - image_width

            # Place image on canvas at top-right
            self.canvas.create_image(x_position, 0, anchor=tk.NW, image=self.img)

        # Ensure correct image path


        self.login_button_main_window = util.get_button(self.main_window, 'Login', 'green', self.login) # our function from util module window text color/rgb command text color
        self.login_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Register new user', 'white', self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window) # creating label(grid) for our webcam
        self.webcam_label.place(x=10, y=10, width=700, height=500)
        self.webcam_label.configure(bg="#1f1f1f")


        self.add_webcam(self.webcam_label)

        self.db_dir = './db' # we will implement this later
        if not os.path.exists(self.db_dir): # if the directory doesnt exist we will create it using this command
            os.mkdir(self.db_dir)


        self.log_path = './log.txt' # implement later attendense system

        # Adding Hover Effects
        self.login_button_main_window.bind("<Enter>", lambda e: self.on_enter(e, "darkgreen"))
        self.login_button_main_window.bind("<Leave>", lambda e: self.on_leave(e, "green"))

        self.register_new_user_button_main_window.bind("<Enter>", lambda e: self.on_enter(e, "lightgray"))
        self.register_new_user_button_main_window.bind("<Leave>", lambda e: self.on_leave(e, "white"))

    def on_enter(self, event, color):
        event.widget.config(bg=color)

    def on_leave(self, event, color):
        event.widget.config(bg=color)

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam) # this function is going to take a frame from the webcam and we convert this frame into the format we need in order tto put it into the label and repeat every 20milliseconds

    def speak(self, text, pause_before_name=False):
        """Speaks the given text using the text-to-speech engine"""
        if pause_before_name:
            parts = text.split()
            if len(parts) > 1:
                first_part = parts[0]  # "Welcome"
                second_part = " ".join(parts[1:])  # The name

                self.engine.say(first_part)
                self.engine.runAndWait()  # Pause before saying the name
                time.sleep(0.1)  # Small pause
                self.engine.say(second_part)
            else:
                self.engine.say(text)
        else:
            self.engine.say(text)

        self.engine.runAndWait()



    def set_voice(self):
        voices = self.engine.getProperty('voices')

        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.name.lower():  # "Zira" is a common female voice on Windows
                self.engine.setProperty('voice', voice.id)
                break

        self.engine.setProperty('rate', 170)  # Adjust speed
        self.engine.setProperty('volume', 1.0)  # Max volume

    def login(self):
        unknown_img_path = './.tmp.jpg'

        # Ensure the frame is valid before writing
        if self.most_recent_capture_arr is None:
            util.msg_box('Error', 'Failed to capture image.', icon_path="icons/x-button.png")
            return

        # Save the captured frame
        success = cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        if not success:
            util.msg_box('Error', 'Could not save temporary image.', icon_path="icons/x-button.png")
            return

        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        name = output.split(',')[1][:-5]
        print(name)

        if name in ['unknown_person']:
            util.msg_box('Access Denied', 'Unknown user. Please register.', icon_path="icons/x-button.png")

        elif name in ['no_persons_found']:
            util.msg_box('Access Denied', 'No persons found. Try again.', icon_path="icons/x-button.png")

        else:
            util.msg_box('Welcome', f"Welcome, {name}!", icon_path="icons/shield.png")
            with open(self.log_path, 'a') as f:
                f.write(f'{name},{datetime.datetime.now()}\n')

        # Check before deleting the file
        if os.path.exists(unknown_img_path):
            os.remove(unknown_img_path)

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window) # we create a new window secondary window inside the other window
        self.register_new_user_window.geometry("1200x520+370+120")
        self.register_new_user_window.title("FaceRec Register")


        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green',  self.accept_register_new_user) # our function from util module window text color/rgb command text color
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red',  self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)  # creating label(grid) for our webcam
        self.capture_label.place(x=10, y=10, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window) # text input
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window,"Please, \ninput username: ") # text label
        self.text_label_register_new_user.place(x=750, y=70)

        # Adding Hover Effects
        self.accept_button_register_new_user_window.bind("<Enter>", lambda e: self.on_enter(e, "darkgreen"))
        self.accept_button_register_new_user_window.bind("<Leave>", lambda e: self.on_leave(e, "green"))

        self.try_again_button_register_new_user_window.bind("<Enter>", lambda e: self.on_enter(e, "darkred"))
        self.try_again_button_register_new_user_window.bind("<Leave>", lambda e: self.on_leave(e, "red"))



    def try_again_register_new_user(self):
        self.register_new_user_window.destroy() # because we want to exit secondary window

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy() # we are taking one of these frames




    def start(self): # implement first
        self.main_window.mainloop() # in order to run our app and keep it open

    def accept_register_new_user(self): # later
        name = self.entry_text_register_new_user.get(1.0, "end-1c") # search

        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture) # save the image - path and format register_new_user_capture

        util.msg_box('Success', 'User was registered successfully !') # title, description we need to show user a msg

        self.register_new_user_window.destroy()



if __name__ == "__main__":
    app = App() #INSTANCE
    app.start()
