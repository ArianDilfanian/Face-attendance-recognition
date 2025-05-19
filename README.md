# FaceRec: Emotion-Aware Face Recognition Attendance System


FaceRec is a GUI-based face recognition system with real-time age and emotion detection. It enables secure login and user registration using facial features, while also logging attendance data into Excel files, including emotional context. The system integrates several advanced libraries like face_recognition, DeepFace, OpenCV, pyttsx3, and Tkinter to deliver an intuitive and intelligent interface.

🧠 Features
✅ Face Recognition
Authenticates users by matching their faces against a registered face database using the face_recognition library.

Supports automatic capture and recognition from webcam feed.

😀 Emotion & Age Detection
Uses DeepFace to analyze live video frames and detect:

Dominant emotion (happy, sad, angry, neutral, etc.)

Estimated age

Smooths predictions using a buffer to improve reliability.

🗣️ Text-to-Speech (TTS)
Greets users audibly using pyttsx3 with emotion-aware personalized messages.

💾 Robust Attendance Logging
Logs user name, detected emotion, time in, time out, and duration in an Excel file (.xlsx) using openpyxl.

Handles corrupt or missing log files gracefully by creating backups or emergency files.

Atomic file saves ensure no data loss.

👤 User Registration
Allows new users to register via webcam by capturing their face and entering a username.

Saves facial data in a local image-based database for future recognition.

🪟 Modern GUI with Tkinter
Clean, dark-themed GUI for login and registration.

Splash screen with load progress.

Hover effects on buttons for better UX.

🎥 Real-Time Webcam Processing
Displays live webcam feed with:

Detected face bounding boxes

Age and emotion overlays

🧩 Error Handling & Logging
Logs all debug and runtime information to app_debug.log.

Fallback mechanisms for:

Face recognition failure

Excel logging issues

Emotion detection errors

🏗️ Built With
Python 3.x

face_recognition

DeepFace

OpenCV

Tkinter

pyttsx3

OpenPyXL

🚀 Getting Started
📦 Requirements
Install required packages via pip:

bash
Copy
Edit
pip install -r requirements.txt
Example dependencies:

text
Copy
Edit
face_recognition
deepface
opencv-python
pyttsx3
Pillow
openpyxl
⚠️ Note: dlib (used by face_recognition) can be tricky to install on some systems. Refer to platform-specific build instructions if needed.

🔧 How to Use
📥 Run the App
bash
Copy
Edit
python main.py
👥 Register a New User
Click on "Register new user"

Enter your name and press "Accept"

Your face will be saved and used for future recognition.

🔐 Login with Face
Click "Login"

FaceRec will:

Recognize your face

Analyze your emotion

Greet you with a personalized message

Log your attendance

📁 Project Structure
bash
Copy
Edit
.
├── db/                    # Registered user face images
├── logo/                  # App logo for UI
├── splashImage/           # Splash screen graphic
├── temp/                  # Temporary image capture
├── attendance_logs/       # Attendance logs (Excel)
├── util.py                # Utility functions (not shown here)
├── main.py                # Main application script
├── icons/                 # Icon assets for messages
├── app_debug.log          # Runtime logs
🛡️ License
This project is open-source and available under the MIT License.

👨‍💻 Author
Arian Dilfanian
Feel free to connect and collaborate!

