# 🌱 EcoScout

**Smart Vehicle Littering & Smoke Emission Detection System**  
*For Urban & Hilly Terrains*

![EcoScout Banner](https://img.shields.io/badge/EcoScout-Smart_surveillance-00ff41?style=for-the-badge&logo=leaf)

## 📖 Overview

**EcoScout** is an advanced AI-powered surveillance system designed to monitor, detect, and report environmental violations by vehicles. Utilizing state-of-the-art Computer Vision and Deep Learning technologies, EcoScout identifies acts of **littering** from moving vehicles and detects excessive **smoke emissions** that contribute to air pollution.

Built for deployment on highways, motorways, and urban areas, the system automatically captures evidence, reads license plates (ANPR), and maintains a comprehensive history of violations to support environmental enforcement.

---

## ✨ Key Features

### 🔍 AI-Powered Detection
- **Littering Detection**: Detects objects being thrown from vehicles in real-time or from recorded footage.
- **Smoke Emission Detection**: Identifies vehicles emitting excessive black smoke.
- **License Plate Recognition (ANPR)**: Automatically extracts and logs vehicle license plate numbers for identification.

### 💻 Modern User Interface
- **Dual Theme Support**:
  - 🟢 **Hacker Mode (Dark)**: A high-contrast, cyberpunk-inspired green/black aesthetic.
  - 🔵 **Eco Mode (Light)**: A clean, professional white/blue/green interface for daytime visibility.
- **Interactive Dashboard**: Real-time stats, system status, and quick access to features.
- **Media Upload**: Support for processing both images and video files.

### 📊 Data & Reporting
- **Violation History**: specific logs of all detected incidents with date, time, and type.
- **Evidence Management**: detailed view of detection frames and confidence scores.
- **Downloadable Reports**: Export violation data for official use.

---

## 🛠️ Tech Stack

### Frontend
![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB) ![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat&logo=vite&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
- **Framework**: React.js (Vite)
- **Styling**: Custom CSS with CSS Variables for dynamic theming (Glassmorphism & Neomorphism)
- **Icons**: Lucide React

### Backend & AI
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![YOLOv8](https://img.shields.io/badge/YOLOv8-00FFFF?style=flat&logo=yolo&logoColor=black) ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white) ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat&logo=pytorch&logoColor=white)
- **Core Logic**: Python
- **Object Detection**: YOLOv8 (Custom trained models for Litter & Smoke)
- **Image Processing**: OpenCV
- **Framework**: PyTorch

---

## 🚀 Installation & Setup

### Prerequisites
- Node.js & npm
- Python 3.8+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ecoscout.git
cd ecoscout
```

### 2. Backend Setup
Navigate to the backend directory and install dependencies.
```bash
cd backend
pip install -r requirements.txt
# Run the backend server
python main.py
```

### 3. Frontend Setup
Navigate to the frontend directory and start the React application.
```bash
cd ../frontend
npm install
npm run dev
```

The application should now be running at `http://localhost:5173` (or the port specified by Vite).

---

## 🖼️ Usage Guide

1.  **Dashboard**: Upon login, view the system overview and features.
2.  **Upload Media**: Drag and drop images or videos of traffic.
3.  **Processing**: The system processes the media using YOLOv8 to identify violations.
4.  **Results**: View annotated images with bounding boxes around litter, smoke, and license plates.
5.  **History**: Access past records, filter by violation type (Littering/Smoke), and export data.
6.  **Settings**: Toggle between "Hacker" (Dark) and "Eco" (Light) themes via the sidebar.

---

## 🤝 Contribution

Contributions are welcome! Please fork the repository and create a pull request for any feature enhancements or bug fixes.

---

## 📜 Disclaimer

This project is an **academic prototype** developed for research and educational purposes. It is designed to demonstrate the potential of AI in environmental monitoring and is not a fully certified commercial surveillance product.

---

*EcoScout © 2025 - Protecting Our Environment Through Technology*
