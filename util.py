import os
import pickle
import tkinter as tk
from tkinter import messagebox
import face_recognition
import pyttsx3
import threading
from PIL import Image, ImageTk


def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
                        window,
                        text=text,
                        activebackground="black",
                        activeforeground="white",
                        fg=fg,
                        bg=color,
                        command=command,
                        height=2,
                        width=20,
                        font=('Roboto', 20)
                    )

    return button


def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label


def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("Roboto", 21), justify="left")
    return label


def get_entry_text(window):
    inputtxt = tk.Text(window,
                       height=1,
                       width=15, font=("Roboto", 32))


    return inputtxt


#def msg_box(title, description):
 #   messagebox.showinfo(title, description)

# Initialize text-to-speech engine
engine = pyttsx3.init()


def speak(text):
    """ Function to make the AI voice speak """
    engine.say(text)
    engine.runAndWait()


def msg_box(title, message, icon_path=None, speak_text=True, auto_close_time=7000):

    msg_font = ("Roboto", 14)
    btn_font = ("Montserrat", 12)
    """ Show a centered message box with an optional icon in title & below text """

    # Start speaking in a separate thread to prevent UI freezing
    if speak_text:
        threading.Thread(target=speak, args=(message,), daemon=True).start()

    # Create a new top-level window
    root = tk.Toplevel()
    root.title(title)

    # Default window size
    window_width = 430
    window_height = 230

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate x and y coordinates to center the window
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # If an icon is provided, load and set it
    if icon_path:
        try:
            img = Image.open(icon_path)
            img = img.resize((74, 74))  # Resize for better display
            img = ImageTk.PhotoImage(img)

            # Keep a reference to prevent garbage collection
            root.img_ref = img

            # Set icon in the title bar
            root.iconphoto(False, img)

        except Exception as e:
            print(f"Error loading icon: {e}")

    # Create a frame for layout
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True, fill="both")

    # Message label with wrapping
    label = tk.Label(frame, text=message, wraplength=250, justify="center", font = msg_font)
    label.pack(pady=10)

    # If an icon is provided, display it **below the text**
    if icon_path:
        img_label = tk.Label(frame, image=root.img_ref)
        img_label.pack(pady=5)

    # OK button
    button = tk.Button(frame, text="OK", command=root.destroy, font = btn_font)
    button.pack(pady=5)

    # Auto-close after specified time (default: 5000ms = 5s)
    root.after(auto_close_time, root.destroy)

    # Bring window to front
    root.lift()
    root.attributes('-topmost', True)

    root.mainloop()  # Run event loop



def recognize(img, db_path):
    # it is assumed there will be at most 1 match in the db

    embeddings_unknown = face_recognition.face_encodings(img)
    if len(embeddings_unknown) == 0:
        return 'no_persons_found'
    else:
        embeddings_unknown = embeddings_unknown[0]

    db_dir = sorted(os.listdir(db_path))

    match = False
    j = 0
    while not match and j < len(db_dir):
        path_ = os.path.join(db_path, db_dir[j])

        file = open(path_, 'rb')
        embeddings = pickle.load(file)

        match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]
        j += 1

    if match:
        return db_dir[j - 1][:-7]
    else:
        return 'unknown_person'




