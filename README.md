# Skin Disease Detection - Android App

**Project:** Skin Disease Detection Android App with AI
**Course:** Mobile Application Development with AI
**Year:** 2025
---

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
**Last Updated:** November 2025
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)

---

## 🎯 Project Overview

This project is an end-to-end mobile application that leverages artificial intelligence and deep learning to automatically detect and classify various skin diseases from images captured by a smartphone camera or selected from the gallery.

### Problem Statement
Skin diseases are common health problems affecting millions of people worldwide. Early detection and accurate diagnosis are crucial for effective treatment. However, there is a shortage of dermatologists, especially in remote and rural areas. Many people lack access to timely skin disease diagnosis, leading to delayed treatment and worsening conditions.

### Solution
This application provides an accessible, instant, and AI-powered preliminary skin disease detection system that:
- **Democratizes healthcare access** - Anyone with a smartphone can get instant preliminary diagnosis
- **Reduces diagnosis time** - From days/weeks to seconds
- **Assists healthcare workers** - Provides a second opinion and helps prioritize cases
- **Maintains privacy** - Images are processed and stored locally (not shared publicly)
- **Educational tool** - Helps users understand different skin conditions

### Key Capabilities
- Real-time skin disease detection using deep learning
- Support for multiple disease categories (Fungal, Viral, Parasitic infections)
- Automatic image storage with descriptive naming
- Complete prediction history with database logging
- User-friendly Android interface with Material Design
- RESTful API for easy integration

---

## ✨ Features

### Mobile Application Features
- 📷 **Camera Integration** - Capture images directly from device camera
- 🖼️ **Gallery Selection** - Choose existing images from phone gallery
- 🤖 **AI-Powered Analysis** - Deep learning model analyzes images instantly
- 📊 **Results Display** - Clear presentation of detected skin disease
- ⚡ **Fast Processing** - Results in seconds
- 🎨 **Modern UI** - Clean, intuitive Material Design interface
- 📱 **Responsive Design** - Works on various Android devices

### Backend Features
- 🧠 **Deep Learning Model** - Keras/TensorFlow CNN for classification
- 💾 **Database Storage** - SQLite database for prediction history
- 📁 **Smart File Naming** - Images saved as `DiseaseName_YYYY-MM-DD_HH-MM-SS.jpg`
- 🔄 **Async Processing** - Quart (async Python) for better performance
- 📡 **RESTful API** - Clean API endpoints for mobile integration
- 📝 **Logging System** - Comprehensive logging for debugging and monitoring
- 🔒 **Error Handling** - Robust error handling and validation

### Disease Categories Supported
The AI model can detect various skin diseases including:
- **Fungal Infections (FU):**
  - Ringworm
  - Athlete's Foot
  - Other fungal conditions
- **Viral Infections (VI):**
  - Shingles
  - Other viral skin conditions
- **Parasitic Infections (PA):**
  - Cutaneous Larva Migrans
  - Other parasitic conditions

---

## 🛠️ Technology Stack

### Frontend (Android App)
- **Language:** Java
- **IDE:** Android Studio
- **UI Framework:** Material Design Components
- **HTTP Client:** Retrofit 2.9.0
- **JSON Parsing:** Gson 2.10.1
- **Image Loading:** Glide (for image handling)
- **Min SDK:** Android 7.0 (API 24)
- **Target SDK:** Android 14 (API 34)

### Backend (Server)
- **Language:** Python 3.11
- **Web Framework:** Quart (Async Flask alternative)
- **ML Framework:** TensorFlow 2.x / Keras
- **Database:** SQLite 3
- **Image Processing:** Pillow (PIL)
- **Configuration:** TOML files
- **Dependencies Management:** pip, requirements.txt

### Machine Learning
- **Model Architecture:** Convolutional Neural Network (CNN)
- **Framework:** Keras with TensorFlow backend
- **Input:** Image files (JPG, PNG)
- **Output:** Disease classification with confidence
- **Model File:** classifier.h5 (HDF5 format)

### Development Tools
- **Version Control:** Git
- **Build System:** Gradle 8.7
- **Package Manager:** pip (Python), Gradle (Android)

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.11** installed
- **Android Studio** installed
- **Android device or emulator**
- **Model file:** `classifier.h5` in `backend/instance/`

### 1. Start the Backend

```bash
cd skin-disease-detection-main
python run_for_phone.py
```

**Expected Output:**
```
Starting Skin Disease Detection Backend
============================================================
🌐 Server will be accessible at:
   - From this computer: http://127.0.0.1:5000/
   - From your phone:    http://YOUR_LOCAL_IP:5000/
============================================================
```

**Keep this terminal open!**

### 2. Configure Your Device

**For Android Emulator (Recommended for Testing):**
- Already configured! Uses `http://10.0.2.2:5000/`
- Just run the app

**For Physical Device:**
1. Find your computer's IP address:
   - Windows: `ipconfig`
   - Linux/Mac: `ifconfig` or `ip addr`
   
   Look for your local network IP (typically starts with 192.168.x.x)

2. Update the default URL in `app/src/main/java/com/ahaanmehta/skin_disease/RetrofitClient.java`:
   ```java
   return "http://YOUR_SERVER_IP:5000/";
   ```

3. **Important:** Ensure phone and computer are on the **SAME WiFi network**

### 3. Run the Android App

1. Open Android Studio
2. **Build → Clean Project**
3. **Build → Rebuild Project**
4. Click **Run (▶️)**
5. Select your device/emulator

### 4. Test the App

1. Click "Gallery" and select a skin image
2. Click "Analyze Image"
3. View the diagnosis result!

---

## 🛠️ Setup Instructions

### Backend Setup

1. **Install Python Dependencies:**
   ```bash
   cd skin-disease-detection-main
   pip install -r requirements.txt
   ```

2. **Ensure Model File Exists:**
   - Model location: `skin-disease-detection-main/backend/instance/classifier.h5`
   - If missing, you'll see an error when starting the backend

3. **Initialize Database (if needed):**
   ```bash
   python -m backend.database.genesis
   ```

4. **Configure Firewall (for Physical Device):**
   - Windows: Allow Python through Windows Firewall
   - Linux/Mac: Adjust firewall settings to allow port 5000

### Android App Setup

1. **Open Project in Android Studio:**
   - Open the `Skin_Disease` folder
   - Wait for Gradle sync to complete

2. **Update Configuration:**
   - Edit: `app/src/main/java/com/ahaanmehta/skin_disease/RetrofitClient.java`
   - Replace `YOUR_SERVER_IP` with your actual server IP address
   - OR use the in-app Settings to configure the backend URL dynamically

3. **Update Network Security Config (Optional):**
   - Edit: `app/src/main/res/xml/network_security_config.xml`
   - Add your local network IP addresses for development

4. **Build and Run:**
   - Clean and rebuild the project
   - Run on emulator or physical device

---

## 📁 Project Structure

```
Skin_Disease/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/ahaanmehta/skin_disease/
│   │   │   │   ├── MainActivity.java
│   │   │   │   ├── HomeActivity.java
│   │   │   │   ├── SplashActivity.java
│   │   │   │   ├── AboutActivity.java
│   │   │   │   ├── SettingsActivity.java
│   │   │   │   ├── RetrofitClient.java
│   │   │   │   ├── ApiService.java
│   │   │   │   └── PredictionResponse.java
│   │   │   ├── res/
│   │   │   │   ├── layout/
│   │   │   │   ├── drawable/
│   │   │   │   ├── values/
│   │   │   │   └── xml/
│   │   │   └── AndroidManifest.xml
│   │   └── test/
│   └── build.gradle.kts
├── skin-disease-detection-main/
│   ├── backend/
│   │   ├── app.py
│   │   ├── blueprints/
│   │   ├── classification/
│   │   ├── database/
│   │   └── instance/
│   │       └── classifier.h5
│   ├── requirements.txt
│   └── run_for_phone.py
├── build.gradle.kts
├── settings.gradle.kts
├── .gitignore
└── README.md
```

---

## 🔧 Configuration

### Backend URL Configuration

The app uses a configurable backend URL system:

1. **Default URL** (in code):
   - Location: `RetrofitClient.java`
   - Default: `http://YOUR_SERVER_IP:5000/`

2. **Runtime Configuration** (Settings screen):
   - Open Settings in the app
   - Enter your backend server address
   - The app saves this and uses it for all future requests

---

## 📱 Usage

1. **Launch the app** - Opens with splash screen
2. **Home screen** - Choose "Start Detection"
3. **Main screen** - Select image source:
   - Camera: Take a new photo
   - Gallery: Choose existing image
4. **Analyze** - Click "Analyze Image" button
5. **Results** - View detected disease information

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is for educational purposes.

---

## ⚠️ Disclaimer

This application is intended for educational and research purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider with any questions regarding a medical condition.

---

## 📞 Support

For issues or questions, please open an issue on GitHub.
