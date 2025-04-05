import os.path
import subprocess
from datetime import datetime, timedelta
import tkinter as tk
import util
import cv2
from PIL import Image, ImageTk
from tkinter import Canvas
import pyttsx3
import time
import threading
import face_recognition
from deepface import DeepFace
import tf_keras
from openpyxl import Workbook, load_workbook
from pathlib import Path
from io import StringIO




class App:

    def show_splash_screen(self):
        splash = tk.Toplevel()
        splash.geometry("1050x600+500+300")
        splash.overrideredirect(True)  # Remove window decorations

        # Load and display splash image
        splash_image_path = os.path.join(os.path.dirname(__file__), "splashImage", "splashimg.jpg")
        if os.path.exists(splash_image_path):
            img = Image.open(splash_image_path)
            img = img.resize((1050, 600))
            photo = ImageTk.PhotoImage(img)

            label = tk.Label(splash, image=photo)
            label.image = photo  # Keep a reference
            label.pack()

        # Close splash after 0.1 seconds
        splash.after(100, splash.destroy)
        return splash




    def __init__(self): #constructor  initializing our app
        self.main_window = tk.Tk() # creating our main window
        self.main_window.withdraw()  # Hide main window initially

        # Show splash screen
        splash = self.show_splash_screen()
        self.main_window.update()  # Force update to show splash

        self.main_window.geometry("1250x520+350+100") # size of the window AND X Y POSITION  was 1200
        self.main_window.configure(bg="#1f1f1f") # bg color
        self.emotion_buffer = []  # Stores recent emotions
        self.buffer_size = 5      # Number of frames to average
        self.setup_logging()  # Initialize Excel logging
        self.log_lock = threading.Lock()


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

        # old log
        #self.log_path = './log.txt' # file format

        # Adding Hover Effects
        self.login_button_main_window.bind("<Enter>", lambda e: self.on_enter(e, "darkgreen"))
        self.login_button_main_window.bind("<Leave>", lambda e: self.on_leave(e, "green"))

        self.register_new_user_button_main_window.bind("<Enter>", lambda e: self.on_enter(e, "lightgray"))
        self.register_new_user_button_main_window.bind("<Leave>", lambda e: self.on_leave(e, "white"))

        # Close splash when done
        splash.destroy()
        self.main_window.deiconify()



    def _init_logging_system(self):
        """Initialize the logging system with proper error handling"""
        self.log_dir = Path("./attendance_logs")
        self.log_dir.mkdir(exist_ok=True)
        self.excel_path = self.log_dir / f"attendance_{datetime.now().strftime('%Y%m%d')}.xlsx"

        if not self.excel_path.exists():
            try:
                self.workbook = Workbook()
                self.sheet = self.workbook.active
                self.sheet.append(["Name", "Emotion", "Time In", "Time Out", "Duration"])
                self._safe_excel_save()
            except Exception as e:
                print(f"Failed to create new log file: {e}")
                self._setup_emergency_logging()

    def _safe_excel_save(self):
        """Save Excel file with proper error handling"""
        for attempt in range(3):
            try:
                temp_path = self.excel_path.with_suffix('.tmp')
                self.workbook.save(temp_path)
                if self.excel_path.exists():
                    self.excel_path.unlink()
                temp_path.rename(self.excel_path)
                return True
            except Exception as e:
                print(f"Save attempt {attempt + 1} failed: {e}")
                time.sleep(0.5)
        return False

    def _setup_emergency_logging(self):
        """Fallback when primary logging fails"""
        self.excel_path = self.log_dir / "emergency_attendance.xlsx"
        try:
            self.workbook = Workbook()
            self.sheet = self.workbook.active
            self.sheet.append(["Name", "Emotion", "Time In", "Time Out", "Duration"])
            self._safe_excel_save()
        except Exception as e:
            print(f"Critical logging failure: {e}")



    def on_enter(self, event, color):
        event.widget.config(bg=color)

    def on_leave(self, event, color):
        event.widget.config(bg=color)

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def detect_age_emotion(self, frame):
        try:
            # Analyze frame with DeepFace (ensure all required actions are included)
            result = DeepFace.analyze(
                frame,
                actions=['age', 'emotion'],
                enforce_detection=False,
                silent=True  # Suppresses console output
            )

            # Safely extract age and emotion with fallbacks
            age = result[0].get('age', 'Unknown')
            emotion = result[0].get('dominant_emotion', 'neutral').lower()

            # Update emotion buffer
            if not hasattr(self, 'emotion_buffer'):
                self.emotion_buffer = []
                self.buffer_size = 5

            self.emotion_buffer.append(emotion)
            if len(self.emotion_buffer) > self.buffer_size:
                self.emotion_buffer.pop(0)

            # Get most frequent emotion
            from collections import Counter
            if self.emotion_buffer:
                final_emotion = Counter(self.emotion_buffer).most_common(1)[0][0]
            else:
                final_emotion = 'neutral'

            return age, final_emotion

        except Exception as e:
            print(f"Error in emotion detection: {str(e)}")
            return "Unknown", "neutral"  # Fallback values


    # new
    def cleanup(self):
        """Proper cleanup on application exit"""
        if hasattr(self, 'workbook'):
            try:
                self.workbook.close()
            except:
                pass



    def process_webcam(self):
        ret, frame = self.cap.read()

        if ret:
            if not hasattr(self, 'frame_counter'):
                self.frame_counter = 0

            # Initialize variables to store detection results
            if not hasattr(self, 'last_age'):
                self.last_age = "Unknown"
            if not hasattr(self, 'last_emotion'):
                self.last_emotion = "Unknown"
            if not hasattr(self, 'last_face_locations'):
                self.last_face_locations = []

            # Process every 4rd frame
            if self.frame_counter % 4 == 0:
                # Resize frame for faster processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Detect age and emotion on the smaller frame
                self.last_age, self.last_emotion = self.detect_age_emotion(small_frame)

                # Convert the smaller frame to RGB for face detection
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                # Detect faces in the smaller frame
                face_locations = face_recognition.face_locations(rgb_small_frame)

                # Scale back face locations to match the original frame size
                self.last_face_locations = [(top * 4, right * 4, bottom * 4, left * 4) for (top, right, bottom, left) in
                                            face_locations]

            # Draw face rectangles and labels using the last detection results
            for (top, right, bottom, left) in self.last_face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            cv2.putText(frame, f"Age: {self.last_age}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1)
            cv2.putText(frame, f"Emotion: {self.last_emotion}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1)

            # Increment frame counter
            self.frame_counter += 1

            # Update the most recent capture array
            self.most_recent_capture_arr = frame

            # Convert the frame to a format suitable for Tkinter
            img_ = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.most_recent_capture_pil = Image.fromarray(img_)
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
            self._label.imgtk = imgtk
            self._label.configure(image=imgtk)

        # Repeat every 20 milliseconds
        self._label.after(20, self.process_webcam)

    # this function is going to take a frame from the webcam and we convert this frame into the format we need in order tto put it into the label and repeat every 20milliseconds



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

    def calculate_duration(self, time_in_str, time_out_str):

        time_in = datetime.strptime(time_in_str, "%H:%M:%S").time()
        time_out = datetime.strptime(time_out_str, "%H:%M:%S").time()
        today = datetime.now().date()

        time_in_dt = datetime.combine(today, time_in)
        time_out_dt = datetime.combine(today, time_out)

        if time_out < time_in:  # Overnight case
            time_out_dt += timedelta(days=1)

        return time_out_dt - time_in_dt



    def setup_logging(self):
        """Initialize Excel logging with proper file handling"""
        from pathlib import Path
        self.log_dir = Path("./attendance_logs")
        self.log_dir.mkdir(exist_ok=True)

        # Create daily log file path
        self.excel_path = self.log_dir / f"attendance_{datetime.now().strftime('%Y%m%d')}.xlsx"

        try:
            if self.excel_path.exists():
                try:
                    # Open with read-only first to check integrity
                    with open(self.excel_path, 'rb') as f:
                        load_workbook(f)
                    self.workbook = load_workbook(self.excel_path)
                except:
                    # Create backup of corrupt file
                    corrupt_path = self.log_dir / f"corrupt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                    self.excel_path.rename(corrupt_path)
                    self._create_new_workbook()
            else:
                self._create_new_workbook()

        except Exception as e:
            print(f"Excel initialization error: {e}")
            self._create_emergency_log()


    def _create_new_workbook(self):
        """Create fresh workbook with proper headers"""
        self.workbook = Workbook()
        self.sheet = self.workbook.active
        self.sheet.append(["Name", "Emotion", "Time In", "Time Out", "Duration"])
        self._safe_save()


    def _safe_save(self):
        """Save workbook with proper file handling"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Create temporary file
                temp_path = self.excel_path.with_suffix('.tmp')
                self.workbook.save(temp_path)

                # Replace original file atomically
                if self.excel_path.exists():
                    self.excel_path.unlink()
                temp_path.rename(self.excel_path)
                break
            except Exception as e:
                print(f"Save attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    self._create_emergency_log()
                time.sleep(0.5)

    def _log_attendance(self, name, emotion):
        """Thread-safe attendance logging with retry logic"""
        for attempt in range(3):
            try:
                now = datetime.now()
                time_str = now.strftime("%H:%M:%S")

                # Load fresh workbook instance
                self.workbook = load_workbook(self.excel_path)
                self.sheet = self.workbook.active

                # Check for existing entry
                record_updated = False
                for idx, row in enumerate(self.sheet.iter_rows(min_row=2, values_only=True), start=2):
                    if row and row[0] == name and row[3] is None:
                        try:
                            # Calculate duration
                            time_in = datetime.strptime(row[2], "%H:%M:%S").time()
                            time_in_dt = datetime.combine(now.date(), time_in)
                            if now.time() < time_in:
                                time_in_dt -= timedelta(days=1)

                            duration = now - time_in_dt
                            hours, rem = divmod(int(duration.total_seconds()), 3600)
                            minutes, seconds = divmod(rem, 60)
                            duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

                            # Update record
                            self.sheet.cell(row=idx, column=4, value=time_str)
                            self.sheet.cell(row=idx, column=5, value=duration_str)
                            record_updated = True
                            break
                        except ValueError as e:
                            print(f"Time parsing error: {e}")
                            continue

                # Add new record if needed
                if not record_updated:
                    self.sheet.append([name, emotion, time_str, None, None])

                # Save changes
                if not self._safe_excel_save():
                    raise IOError("Failed to save Excel file")

                return  # Success

            except Exception as e:
                print(f"Logging attempt {attempt + 1} failed: {e}")
                if attempt == 2:  # Final attempt failed
                    self._log_to_text_backup(name, emotion, time_str)
                time.sleep(0.5)





    def login(self):
        threading.Thread(target=self._login_thread, daemon=True).start()

    def _login_thread(self):
        temp_img_path = Path("./temp/temp_capture.jpg")
        temp_img_path.parent.mkdir(exist_ok=True)

        try:
            # 1. Verify image capture
            if self.most_recent_capture_arr is None:
                raise ValueError("No image captured")

            # 2. Save temporary image
            if not cv2.imwrite(str(temp_img_path), self.most_recent_capture_arr):
                raise IOError("Failed to save temporary image")

            # 3. Face recognition
            try:
                output = subprocess.check_output(
                    ['face_recognition', str(self.db_dir), str(temp_img_path)],
                    stderr=subprocess.PIPE
                ).decode('utf-8')
                name = output.split(',')[1].strip()
            except subprocess.CalledProcessError as e:
                raise ValueError(f"Face recognition failed: {e.stderr.decode('utf-8')}")

            # 4. Emotion detection
            age, emotion = self.detect_age_emotion(self.most_recent_capture_arr)
            emotion = emotion.lower()

            # 5. Handle different cases
            if name == 'unknown_person':
                self.main_window.after(0, lambda: util.msg_box(
                    'Access Denied',
                    'Unknown user. Please register.',
                    icon_path="icons/x-button.png"
                ))
            elif name == 'no_persons_found':
                self.main_window.after(0, lambda: util.msg_box(
                    'Access Denied',
                    'No face detected. Please try again.',
                    icon_path="icons/x-button.png"
                ))
            else:
                # Successful login
                welcome_msg = {
                    'happy': f"Welcome, {name}! You look happy today!",
                    'sad': f"Welcome, {name}. We hope your day gets better.",
                    'angry': f"Welcome, {name}. We appreciate your patience.",
                }.get(emotion, f"Welcome, {name}!")

                self.main_window.after(0, lambda: util.msg_box(
                    'Welcome',
                    welcome_msg,
                    icon_path="icons/shield.png"
                ))
                self.speak(welcome_msg)

                # Log to Excel
                self._log_attendance(name, emotion)

        except Exception as e:
            error_msg = str(e) if str(e) else "Unknown error occurred"
            print(f"Login error: {error_msg}")
            self.main_window.after(0, lambda: util.msg_box(
                'Login Failed',
                'Could not complete login process',
                icon_path="icons/x-button.png"
            ))

        finally:
            # Clean up temporary files
            if temp_img_path.exists():
                try:
                    temp_img_path.unlink()
                except Exception as e:
                    print(f"Failed to delete temp image: {e}")


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

    def accept_register_new_user(self):
        # Disable the button to prevent multiple clicks
        self.accept_button_register_new_user_window.config(state=tk.DISABLED)

        name = self.entry_text_register_new_user.get(1.0, "end-1c")  # Get the username

        # Save the captured image
        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)

        # Log the registration
        self.log_attendance(name, "registration")  # Added this line

        # Close the registration window
        if hasattr(self, 'register_new_user_window') and self.register_new_user_window.winfo_exists():
            self.register_new_user_window.destroy()

        # Show non-blocking success message
        self.main_window.after(0, lambda: util.msg_box('Success', 'User was registered successfully!'))




if __name__ == "__main__":
    app = App()
    try:
        app.start()
    finally:
        app.cleanup()