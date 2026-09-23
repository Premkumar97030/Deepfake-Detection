# SPECTRA — Deepfake & Synthetic Media Forensic Detection

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PyTorch](https://img.shields.io/badge/Model-PyTorch%20%7C%20ResNet50-EE4C2C.svg?logo=pytorch&logoColor=white)](https://pytorch.org)
[![React](https://img.shields.io/badge/Frontend-React%2019%20%7C%20Vite-61DAFB.svg?logo=react&logoColor=black)](https://react.dev)
[![Vercel](https://img.shields.io/badge/Deploy-Vercel-000000.svg?logo=vercel&logoColor=white)](https://vercel.com)
[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7.svg?logo=render&logoColor=white)](https://render.com)

**SPECTRA** is a state-of-the-art synthetic media verification platform designed to detect deepfakes, AI-generated images (Midjourney, DALL-E, Stable Diffusion), and CGI renders across all major digital image and video formats.

---

## 🌟 Key Features

- 🔬 **Multi-Class Classification**: Accurately classifies media into **Authentic Real**, **AI Generated**, or **CGI Render** with confidence scoring and probability distributions.
- 🎬 **Video Temporal Analysis**: Uniform 16-keyframe extraction and aggregation to detect subtle temporal facial manipulations and video artifact anomalies.
- 📦 **Universal Format Ingestion**: Supports all standard image formats (`.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tiff`, `.avif`, `.heic`, etc.) and video containers (`.mp4`, `.webm`, `.mov`, `.avi`, `.mkv`, `.flv`, `.wmv`, etc.).
- 📊 **Screen-Fitting Forensic Report**: Clean, non-distorting analysis cards with side-by-side media inspect viewports, class probability bars, and inference speed metrics.
- 🕒 **Persistent Session Audit Trail**: History dashboard with persistent visual thumbnail snapshots, query filtering, and detailed inspection modals.
- 🚀 **Cloud Deployment Ready**: Pre-configured for deployment with **Render** (Backend API) and **Vercel** (Frontend SPA).

---

## 📁 Project Architecture

```text
Deepfake-Detection/
├── backend/                       # Python FastAPI Backend
│   ├── models/                    # Neural Network Architectures (ResNet-50, LSTM)
│   ├── weights/                   # Trained PyTorch Model Checkpoints (.pth via Git LFS)
│   ├── main.py                    # REST API Endpoints & Lifespan Service
│   ├── prediction_service.py      # Batch Inference & Frame Sampling Engine
│   ├── config.py                  # Environment & Path Configurations
│   ├── requirements.txt           # Python Dependencies (CPU PyTorch + OpenCV Headless)
│   ├── render.yaml                # Render Blueprint Configuration
│   └── Procfile                   # Cloud Process Definition
│
├── frontend/                      # React + Vite Web Application
│   ├── src/
│   │   ├── components/            # Hologram Scanner, Navbar, Footer, UploadBox
│   │   ├── pages/                 # Home, Analyze, Result, History, About
│   │   ├── utils/                 # Local History Storage & Thumbnail Generator
│   │   └── index.css              # Cyber-Forensic Design System
│   ├── vercel.json                # Vercel SPA Routing Configuration
│   └── package.json               # Frontend Scripts & Dependencies
│
├── DEPLOYMENT.md                  # Comprehensive Vercel & Render Deployment Guide
├── package.json                   # Root Dev Runner (Starts Backend & Frontend)
└── README.md                      # Project Overview & Documentation
```

---

## 🚀 Quickstart Guide

### Prerequisites
- **Node.js** (v18+)
- **Python** (v3.10 or v3.11)

---

### Option A: Run Full-Stack with One Command (Root)

1. Clone the repository:
   ```bash
   git clone https://github.com/Premkumar97030/Deepfake-Detection.git
   cd Deepfake-Detection
   ```
2. Install frontend dependencies:
   ```bash
   cd frontend && npm install && cd ..
   ```
3. Start both backend and frontend concurrently:
   ```bash
   npm run dev
   ```
   - **Frontend**: `http://localhost:5173`
   - **Backend API**: `http://127.0.0.1:8000`
   - **Swagger Docs**: `http://127.0.0.1:8000/docs`

---

### Option B: Run Services Separately

#### 1. Start the Backend API
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

#### 2. Start the Frontend Application
```bash
cd frontend
npm install
npm run dev
```

---

## 🌐 Cloud Deployment

Detailed step-by-step instructions are available in [DEPLOYMENT.md](DEPLOYMENT.md).

- **Backend (Render)**:
  - Build Command: `pip install --upgrade pip && pip install -r requirements.txt`
  - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
  - Python Version: `3.11.9`
- **Frontend (Vercel)**:
  - Framework: `Vite`
  - Root Directory: `frontend`
  - Build Command: `npm run build`
  - Environment Variable: `VITE_API_URL=https://<your-render-backend>.onrender.com`

---

## 📡 REST API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/health` | `GET` | Service liveness probe & model load status |
| `/api/analyze` | `POST` | Upload and verify image or video media (`multipart/form-data`) |
| `/image/predict` | `POST` | Direct image tensor inference router |
| `/docs` | `GET` | Interactive Swagger API documentation |

---

## 📄 License
This project is licensed under the MIT License.
