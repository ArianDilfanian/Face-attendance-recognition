# FaceRec: Emotion-Aware Face Recognition Attendance System


FaceRec is a GUI-based face recognition system with real-time age and emotion detection. It enables secure login and user registration using facial features, while also logging attendance data into Excel files, including emotional context. The system integrates several advanced libraries like face_recognition, DeepFace, OpenCV, pyttsx3, and Tkinter to deliver an intuitive and intelligent interface.


---

## 🚩 Features
---

### ✅ Face Recognition
- Matches faces against a registered local database using `face_recognition`.

### 😀 Emotion & Age Detection
- Detects **dominant emotion** (happy, sad, angry, etc.) and **age** in real-time using `DeepFace`.

### 🗣️ Voice Feedback (TTS)
- Emotion-based greetings using `pyttsx3`.

### 🗓️ Attendance Logging
- Logs user:
  - Name
  - Emotion
  - Time In / Time Out
  - Duration of presence  
- Uses Excel via `openpyxl` and includes:
  - Backup of corrupt logs
  - Emergency fallbacks
  - Atomic file saving for data integrity

### 👤 User Registration
- Register new users via webcam and save their face image locally for future recognition.

### 🎥 Live Camera Interface
- Real-time webcam feed with:
  - Bounding boxes for faces
  - Emotion & age display overlays

### 🖥️ GUI Interface
- Dark-mode UI built with `Tkinter`
- Splash screen with load status
- Hover effect on buttons

---

## 🧰 Built With
---

- **Python 3.x**
- [`face_recognition`](https://github.com/ageitgey/face_recognition)
- [`DeepFace`](https://github.com/serengil/deepface)
- `OpenCV`
- `Tkinter`
- `pyttsx3`
- `openpyxl`
- `Pillow`

---

🛡️ License
This project is open-source and available under the MIT License.

---

👨‍💻 Author
Arian Dilfanian
Feel free to connect and collaborate!

## 📦 Installation
---

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/FaceRec.git
cd FaceRec



