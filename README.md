
Developed as part of Mobile Application Development with AI coursework.

---

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review configuration guides

---

## 🎉 Acknowledgments

- TensorFlow/Keras team for the ML framework
- Android development community
- Open-source contributors
- Dataset providers

---

**Made with ❤️ for better healthcare accessibility**

---

## Quick Start Commands

```bash
# Backend
cd skin-disease-detection-main
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run_for_phone.py

# Android (in Android Studio)
# File → Open → Select project folder
# Run → Run 'app'
```

Now you're ready to detect skin diseases! 🚀
# Skin Disease Detection - Android App with AI Backend

An end-to-end mobile application that uses artificial intelligence and deep learning to detect and classify skin diseases from smartphone images.

[![Android](https://img.shields.io/badge/Platform-Android-green.svg)](https://developer.android.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://www.tensorflow.org/)

---

## 📋 Table of Contents
- [Overview](#-overview)
- [How It Works](#-how-it-works)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Local Setup Guide](#-local-setup-guide)
- [Running the Application](#-running-the-application)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

### Problem Statement
Skin diseases affect millions of people worldwide. Early detection and accurate diagnosis are crucial for effective treatment, but there's a shortage of dermatologists, especially in remote areas. Manual diagnosis is time-consuming, subjective, and often inaccessible to those who need it most.

### Our Solution
This application provides an accessible, instant, AI-powered skin disease detection system that:
- **Democratizes Healthcare** - Anyone with a smartphone can get instant preliminary diagnosis
- **Reduces Diagnosis Time** - From days/weeks to seconds
- **Assists Healthcare Workers** - Provides a second opinion and helps prioritize cases
- **Maintains Privacy** - Images are processed locally, not shared publicly
- **Educational Tool** - Helps users understand different skin conditions

### Disease Categories Detected
The AI model can detect various skin diseases including:
- **Fungal Infections (FU):** Ringworm, Athlete's Foot, Candidiasis
- **Viral Infections (VI):** Shingles, Herpes, Warts
- **Parasitic Infections (PA):** Cutaneous Larva Migrans, Scabies

---

## 🔬 How It Works

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   ANDROID APPLICATION                        │
│                                                              │
│  ┌──────────┐  ┌─────────────┐  ┌──────────────────┐      │
│  │  Camera  │  │   Gallery   │  │  Results Display │      │
│  │ Capture  │  │  Selection  │  │      Screen      │      │
│  └─────┬────┘  └──────┬──────┘  └────────▲─────────┘      │
│        │              │                   │                 │
│        └──────────────┴───────────────────┘                 │
│                       │                                     │
│              ┌────────▼────────────┐                        │
│              │   MainActivity      │                        │
│              │  (Image Handler)    │                        │
│              └────────┬────────────┘                        │
│                       │                                     │
│              ┌────────▼────────────┐                        │
│              │  RetrofitClient     │                        │
│              │  (HTTP Client)      │                        │
│              └────────┬────────────┘                        │
│                       │                                     │
└───────────────────────┼─────────────────────────────────────┘
                        │
                        │ HTTP POST (Image)
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                   PYTHON BACKEND                             │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │       Quart Web Server (Async Python)                │  │
│  │              Port: 5000                              │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                     │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │     API Endpoint: /api/v1/predictions/              │  │
│  │     (Receives Image, Returns Prediction)            │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                     │
│         ┌─────────────┼─────────────┐                      │
│         │             │             │                      │
│  ┌──────▼──────┐ ┌───▼─────┐ ┌────▼────────┐            │
│  │ Image Save  │ │   CNN   │ │  Database   │            │
│  │  & Rename   │ │  Model  │ │   Logging   │            │
│  └──────┬──────┘ └───┬─────┘ └────┬────────┘            │
│         │            │             │                      │
│  ┌──────▼────────────▼─────────────▼────────┐            │
│  │   Classification Result                   │            │
│  │   DiseaseName_YYYY-MM-DD_HH-MM-SS.jpg    │            │
│  └───────────────────┬───────────────────────┘            │
│                      │                                     │
└──────────────────────┼─────────────────────────────────────┘
                       │
                       ▼
              ┌────────────────┐
              │ JSON Response  │
              │   to Mobile    │
              └────────────────┘
```

### Workflow Explanation

#### 1. **Image Capture/Selection**
   - User opens the Android app
   - Chooses to either take a photo with the camera or select from gallery
   - Image is loaded into memory

#### 2. **Image Upload**
   - App uses Retrofit (HTTP client) to send the image to the backend
   - Image is sent as multipart/form-data to `http://YOUR_SERVER:5000/api/v1/predictions/`
   - Request includes the image file

#### 3. **Backend Processing**
   - **Step 1:** Quart server receives the image
   - **Step 2:** Image is temporarily saved with a timestamp
   - **Step 3:** Image is preprocessed:
     - Resized to model's expected input size
     - Normalized pixel values
     - Converted to array format
   - **Step 4:** Deep learning model (CNN) analyzes the image
   - **Step 5:** Model outputs prediction (disease category)
   - **Step 6:** Image is renamed to descriptive format: `DiseaseName_YYYY-MM-DD_HH-MM-SS.jpg`
   - **Step 7:** Prediction is logged to SQLite database

#### 4. **Response & Display**
   - Backend sends JSON response: `{"prediction": "Fungal Infection"}`
   - Android app receives and parses the response
   - Results are displayed in a beautiful Material Design card
   - User sees the detected disease type

#### 5. **Storage & History**
   - Image stored locally on server: `backend/image_bucket/DiseaseName_2025-11-07_14-30-45.jpg`
   - Database record created with:
     - Timestamp
     - Prediction result
     - Image filename
     - Processing time

---

## ✨ Features

### Mobile App Features
- 📷 **Camera Integration** - Capture images directly
- 🖼️ **Gallery Selection** - Choose existing images
- 🤖 **AI Analysis** - Instant disease detection
- 📊 **Results Display** - Clear, easy-to-understand results
- ⚙️ **Settings** - Configure backend server URL
- 🔄 **Dynamic URL Configuration** - Change server address without recompiling
- 🎨 **Modern UI** - Material Design 3 components
- 🌙 **Dark Mode Support** - Automatic theme switching

### Backend Features
- 🧠 **Deep Learning** - TensorFlow/Keras CNN model
- 💾 **Database Logging** - SQLite for prediction history
- 📁 **Smart Naming** - Auto-rename images with results
- 🔄 **Async Processing** - Fast, non-blocking operations
- 📡 **RESTful API** - Clean, standardized endpoints
- 📝 **Comprehensive Logging** - Debug and monitor everything
- 🔒 **Error Handling** - Robust validation and error responses

---

## 🛠️ Technology Stack

### Frontend (Android)
- **Language:** Java
- **IDE:** Android Studio Koala | 2024.1.1
- **Build System:** Gradle 8.7
- **Min SDK:** Android 11 (API 30)
- **Target SDK:** Android 14 (API 35)

**Key Libraries:**
- Retrofit 2.9.0 - HTTP networking
- OkHttp 4.11.0 - HTTP client
- Gson 2.10.1 - JSON parsing
- Material Design 3 - UI components

### Backend (Python)
- **Language:** Python 3.11
- **Framework:** Quart (async Flask)
- **ML Framework:** TensorFlow 2.x / Keras
- **Database:** SQLite 3
- **Image Processing:** Pillow (PIL)

**Key Libraries:**
```
quart==0.19.4
tensorflow==2.x
pillow==10.0.0
numpy==1.24.3
```

### Machine Learning
- **Architecture:** Convolutional Neural Network (CNN)
- **Training:** Google Colab / Jupyter Notebook
- **Input Size:** 224x224x3 (RGB images)
- **Output:** Multi-class classification
- **Model Format:** HDF5 (.h5 file)

---

## 📁 Project Structure

```
Skin_Disease/
├── app/                                          # Android Application
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/ahaanmehta/skin_disease/
│   │   │   │   ├── MainActivity.java            # Image upload & analysis
│   │   │   │   ├── HomeActivity.java            # Landing page
│   │   │   │   ├── SplashActivity.java          # Startup screen
│   │   │   │   ├── AboutActivity.java           # About page
│   │   │   │   ├── SettingsActivity.java        # Backend URL config
│   │   │   │   ├── RetrofitClient.java          # HTTP client setup
│   │   │   │   ├── ApiService.java              # API endpoints
│   │   │   │   └── PredictionResponse.java      # Response model
│   │   │   ├── res/
│   │   │   │   ├── layout/                      # XML layouts
│   │   │   │   ├── drawable/                    # Icons & graphics
│   │   │   │   ├── values/                      # Strings, colors, themes
│   │   │   │   └── xml/                         # Network & file configs
│   │   │   └── AndroidManifest.xml              # App configuration
│   │   └── test/                                # Unit tests
│   └── build.gradle.kts                         # App dependencies
├── skin-disease-detection-main/                 # Python Backend
│   ├── backend/
│   │   ├── app.py                               # Main application
│   │   ├── blueprints/
│   │   │   └── model_blueprint.py               # API routes
│   │   ├── classification/
│   │   │   ├── predictions.py                   # ML prediction logic
│   │   │   ├── categories.json                  # Disease categories
│   │   │   └── final_file_tech_proj.ipynb       # Model training notebook
│   │   ├── database/
│   │   │   ├── genesis.py                       # Database setup
│   │   │   └── population.py                    # Data operations
│   │   ├── config/
│   │   │   ├── app_config.toml                  # App settings
│   │   │   └── server_config.toml               # Server settings
│   │   ├── instance/
│   │   │   ├── classifier.h5                    # ⚠️ ML model (required!)
│   │   │   └── app.db                           # SQLite database
│   │   └── image_bucket/                        # Uploaded images
│   ├── requirements.txt                         # Python dependencies
│   └── run_for_phone.py                         # Server startup script
├── .gitignore                                   # Git exclusions
├── CONFIG_SETUP.md                              # Configuration guide
├── GITHUB_READY_CHECKLIST.md                    # Deployment checklist
└── README.md                                    # This file
```

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

### For Android App Development
- ✅ **Android Studio** (latest version)
  - Download: https://developer.android.com/studio
- ✅ **Java Development Kit (JDK) 11** or higher
- ✅ **Android SDK** (automatically installed with Android Studio)
- ✅ **Android Device or Emulator**
  - Physical device: Android 11 (API 30) or higher
  - Emulator: Use Android Studio AVD Manager

### For Backend Development
- ✅ **Python 3.11** or higher
  - Download: https://www.python.org/downloads/
  - ⚠️ During installation, check "Add Python to PATH"
- ✅ **pip** (Python package manager - comes with Python)
- ✅ **Git** (for cloning the repository)
  - Download: https://git-scm.com/downloads

### Network Requirements
- ✅ **Same WiFi Network** - Phone and computer must be on the same network
- ✅ **Firewall Configuration** - Allow Python through Windows Firewall

---

## 🚀 Local Setup Guide

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/de-code-bot/skin-disease-detection.git

# Navigate to the project directory
cd skin-disease-detection
```

### Step 2: Set Up Python Backend

#### 2.1 Install Python Dependencies

```bash
# Navigate to the backend directory
cd skin-disease-detection-main

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

#### 2.2 Set Up the ML Model

**⚠️ IMPORTANT:** You need the trained model file!

The model file `classifier.h5` should be placed in:
```
skin-disease-detection-main/backend/instance/classifier.h5
```

**Options to get the model:**
1. **Train your own model** using the Jupyter notebook:
   - Open `backend/classification/final_file_tech_proj.ipynb`
   - Run all cells in Google Colab or Jupyter
   - Save the trained model as `classifier.h5`

2. **Use a pre-trained model** (if available)
   - Download from project resources
   - Place in `backend/instance/` folder

#### 2.3 Initialize the Database

```bash
# From the skin-disease-detection-main directory
python -m backend.database.genesis
```

You should see: `Database initialized successfully!`

#### 2.4 Configure Firewall (Windows)

Run Command Prompt as Administrator:

```cmd
netsh advfirewall firewall add rule name="Python Server" dir=in action=allow program="C:\Path\To\Python\python.exe" enable=yes
```

Or use the provided batch file:
```cmd
# Run as Administrator
add_firewall_rule.bat
```

### Step 3: Set Up Android App

#### 3.1 Open in Android Studio

1. Launch **Android Studio**
2. Click **Open** (or File → Open)
3. Navigate to the cloned repository folder
4. Select the main `Skin_Disease` folder
5. Click **OK**
6. Wait for Gradle sync to complete (this may take a few minutes)

#### 3.2 Configure Backend URL

You have two options:

**Option A: Use In-App Settings (Recommended)**
- Just run the app and configure the URL in Settings
- No code changes needed!

**Option B: Edit Source Code**

Open `app/src/main/java/com/ahaanmehta/skin_disease/RetrofitClient.java`

Find this line (around line 67):
```java
return "http://YOUR_SERVER_IP:5000/";
```

Replace with:
- **For Emulator:** `http://10.0.2.2:5000/`
- **For Physical Device:** `http://YOUR_COMPUTER_IP:5000/`

**How to find your computer's IP:**
```cmd
# On Windows
ipconfig

# Look for "IPv4 Address" under your WiFi adapter
# Example: 192.168.1.15
```

#### 3.3 Update Network Security Config (Optional)

If using a physical device, edit:
`app/src/main/res/xml/network_security_config.xml`

Add your computer's IP:
```xml
<domain includeSubdomains="true">192.168.1.15</domain>
```

---

## 🎮 Running the Application

### Start the Backend Server

```bash
# Navigate to backend directory
cd skin-disease-detection-main

# Activate virtual environment (if not already active)
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Start the server
python run_for_phone.py
```

**Expected Output:**
```
Starting Skin Disease Detection Backend
============================================================
🌐 Server will be accessible at:
   - From this computer: http://127.0.0.1:5000/
   - From your phone:    http://192.168.1.15:5000/
============================================================
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://192.168.1.15:5000
```

**✅ Backend is now running! Keep this terminal open.**

### Run the Android App

#### Using Android Emulator:

1. Open Android Studio
2. Click **Run** (▶️ button) or press `Shift + F10`
3. Select an emulator device
4. Wait for the app to install and launch
5. The emulator will automatically use `http://10.0.2.2:5000/`

#### Using Physical Device:

1. Enable **Developer Options** on your phone:
   - Go to Settings → About Phone
   - Tap "Build Number" 7 times
   
2. Enable **USB Debugging**:
   - Settings → Developer Options → USB Debugging

3. Connect phone via USB cable

4. In Android Studio:
   - Click **Run** (▶️)
   - Select your device
   - Wait for installation

5. Configure Backend URL:
   - Open app → Settings
   - Click "Change Backend URL"
   - Enter your computer's IP: `http://192.168.1.15:5000`
   - Click "Test Connection"
   - Should show "✓ Connection successful!"

### Test the Application

1. **Launch the app** - Opens with splash screen
2. **Home screen** - Click "Start Detection"
3. **Main screen** - Select image source:
   - Click "📷 Camera" to take a new photo
   - Click "🖼️ Gallery" to choose existing image
4. **Select/capture** an image of a skin condition
5. **Click "Analyze Image"** button
6. **Wait for results** (usually 1-3 seconds)
7. **View diagnosis** - Results appear in a card showing the detected disease type

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### 1. **Backend: "Model file not found"**
```
Error: Could not find classifier.h5
```
**Solution:**
- Ensure `classifier.h5` exists in `backend/instance/`
- Train the model using the Jupyter notebook
- Check file permissions

#### 2. **Android: "Connection failed"**
```
Error: Failed to connect to /192.168.1.15:5000
```
**Solutions:**
- ✅ Verify backend is running (`python run_for_phone.py`)
- ✅ Check devices are on same WiFi network
- ✅ Verify firewall allows Python
- ✅ Ping the server from your phone's browser: `http://192.168.1.15:5000/`
- ✅ Check the IP address is correct

#### 3. **Android: "Unable to resolve host"**
```
Error: Unable to resolve host "YOUR_SERVER_IP"
```
**Solution:**
- You forgot to replace `YOUR_SERVER_IP` with actual IP
- Edit `RetrofitClient.java` or use in-app Settings

#### 4. **Gradle Sync Failed**
```
Error: Could not resolve dependencies
```
**Solution:**
```bash
# In Android Studio terminal:
./gradlew clean
./gradlew build --refresh-dependencies
```

#### 5. **Python: "Module not found"**
```
ModuleNotFoundError: No module named 'quart'
```
**Solution:**
```bash
# Activate virtual environment first!
venv\Scripts\activate
pip install -r requirements.txt
```

#### 6. **Emulator: Very Slow**
**Solution:**
- Use x86_64 system image (not ARM)
- Enable hardware acceleration (HAXM/WHPX)
- Allocate more RAM to emulator
- Or use a physical device

#### 7. **Port 5000 Already in Use**
```
Error: Address already in use
```
**Solution:**
```cmd
# Find what's using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Or change port in server_config.toml
```

### Still Having Issues?

1. **Check Logs:**
   - Android: Android Studio → Logcat
   - Backend: Terminal output

2. **Test Backend Directly:**
   ```bash
   # Open browser or use curl
   curl http://localhost:5000/
   ```

3. **Verify Network:**
   ```cmd
   # From phone, open browser and visit:
   http://YOUR_COMPUTER_IP:5000/
   # You should see a webpage
   ```

---

## 📚 Additional Resources

### Learning Materials
- [Android Development Guide](https://developer.android.com/guide)
- [Retrofit Documentation](https://square.github.io/retrofit/)
- [Quart Framework](https://quart.palletsprojects.com/)
- [TensorFlow/Keras](https://www.tensorflow.org/guide/keras)

### Dataset Information
The model was trained on a skin disease dataset containing:
- Multiple disease categories
- Thousands of labeled images
- Various skin types and conditions

Training notebook: `backend/classification/final_file_tech_proj.ipynb`

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Areas for Improvement
- Add more disease categories
- Improve model accuracy
- Add multi-language support
- Implement user authentication
- Create prediction history in app
- Add confidence scores to results

---

## ⚠️ Disclaimer

**IMPORTANT:** This application is intended for **educational and research purposes only**. It is NOT a substitute for professional medical advice, diagnosis, or treatment.

- ❌ Do NOT use for actual medical diagnosis
- ❌ Do NOT delay seeking professional medical care
- ✅ Always consult a qualified dermatologist
- ✅ Use as a learning tool only

---

## 📄 License

This project is for educational purposes. Feel free to use, modify, and distribute for learning and non-commercial purposes.

---

## 👥 Team
