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




## 📽️ Image and Videos


![17](https://github.com/user-attachments/assets/19e2e026-8474-4613-b897-921339cffb1d)
![18](https://github.com/user-attachments/assets/9f9370ee-fc56-4f0d-ad53-e89f65100246)
![19](https://github.com/user-attachments/assets/2a07d24f-b717-4502-9869-671b827bdf62)
![20](https://github.com/user-attachments/assets/bf2aa78c-e966-406a-88b4-17e266b69805)
![21](https://github.com/user-attachments/assets/4e0364f2-9b2a-4d50-a444-970e24d2e9ff)
![22](https://github.com/user-attachments/assets/2cd13a40-de1f-4ad9-8b17-0f90b7b91f79)
![23](https://github.com/user-attachments/assets/6ef9f247-e65c-4679-b307-d3fb5f0c819a)
![24](https://github.com/user-attachments/assets/c1db98a8-bb2b-4361-a3a7-4e267079deb9)
![25](https://github.com/user-attachments/assets/284db6d9-cee2-4843-908f-9a016ff8d8e1)
---

https://github.com/user-attachments/assets/27f789fe-5483-4d54-bd5c-049c24b042e4



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



