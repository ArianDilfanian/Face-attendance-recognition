import os
import pickle
import tkinter as tk
from tkinter import messagebox
import face_recognition
from PIL import Image, ImageTk
import threading


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
    return tk.Text(window, height=1, width=15, font=("Roboto", 32))


def msg_box(title, message, icon_path=None, auto_close_time=7000):
    """Show a centered message box with optional icon and auto-close"""
    root = tk.Toplevel()
    root.title(title)

    # Window sizing and positioning
    window_width = 430
    window_height = 230
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.attributes('-topmost', True)

    # Icon handling
    icon_img = None
    if icon_path:
        try:
            icon_img = Image.open(icon_path)
            icon_img = icon_img.resize((74, 74))
            icon_photo = ImageTk.PhotoImage(icon_img)
            root.iconphoto(False, icon_photo)
            root.img_ref = icon_photo  # Keep reference
        except Exception as e:
            print(f"Error loading icon: {e}")

    # Frame container
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True, fill="both")

    # Message label
    msg_label = tk.Label(
        frame,
        text=message,
        wraplength=350,
        justify="center",
        font=("Roboto", 14)
    )
    msg_label.pack(pady=10)

    # Icon display if available
    if icon_img:
        icon_label = tk.Label(frame, image=icon_photo)
        icon_label.pack(pady=5)

    # OK button
    ok_btn = tk.Button(
        frame,
        text="OK",
        command=root.destroy,
        font=("Montserrat", 12)
    )
    ok_btn.pack(pady=5)

    # Auto-close functionality
    root.after(auto_close_time, root.destroy)
    root.grab_set()
    root.wait_window()


def recognize(img, db_path):
    """Improved face recognition with error handling"""
    try:
        embeddings_unknown = face_recognition.face_encodings(img)
        if not embeddings_unknown:
            return 'no_persons_found'

        embeddings_unknown = embeddings_unknown[0]

        for file_name in sorted(os.listdir(db_path)):
            if not file_name.endswith('.pickle'):
                continue

            file_path = os.path.join(db_path, file_name)

            try:
                with open(file_path, 'rb') as f:
                    embeddings = pickle.load(f)

                if face_recognition.compare_faces([embeddings], embeddings_unknown)[0]:
                    return os.path.splitext(file_name)[0]

            except Exception as e:
                print(f"Error processing {file_name}: {e}")
                continue

        return 'unknown_person'

    except Exception as e:
        print(f"Recognition error: {e}")
        return 'error_occurred'


