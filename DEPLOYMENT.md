# SPECTRA Deployment Guide

Follow these steps to deploy the **SPECTRA** Deepfake Detection Platform:
- **Backend (FastAPI + PyTorch)**: [Render](https://render.com)
- **Frontend (React + Vite)**: [Vercel](https://vercel.com)

---

## 1. Deploying the Backend on Render

### Method A: Connect via GitHub (Recommended)
1. Push your repository to **GitHub**.
2. Log in to [Render Dashboard](https://dashboard.render.com).
3. Click **New +** → **Web Service**.
4. Connect your GitHub repository.
5. Configure the service settings:
   - **Name**: `spectra-forensic-api` (or your preferred name)
   - **Root Directory**: `backend`
   - **Environment**: `Python`
   - **Region**: Choose the closest region (e.g., Singapore, Oregon, Frankfurt)
   - **Branch**: `main` (or your default branch)
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free` or `Starter`
6. Add Environment Variables under **Advanced**:
   - `PYTHON_VERSION`: `3.11.9`
7. Click **Create Web Service**.
8. Once deployed, copy your backend URL (e.g., `https://spectra-forensic-api.onrender.com`).

---

## 2. Deploying the Frontend on Vercel

1. Log in to [Vercel Dashboard](https://vercel.com/dashboard).
2. Click **Add New...** → **Project**.
3. Import your GitHub repository.
4. Configure Project Settings:
   - **Project Name**: `spectra-app`
   - **Framework Preset**: `Vite`
   - **Root Directory**: Click **Edit** and select `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`
5. Expand the **Environment Variables** section and add:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://your-backend-app.onrender.com` *(Paste your Render backend URL from Step 1, without a trailing slash)*
6. Click **Deploy**.
7. Vercel will build and assign you a live HTTPS URL (e.g., `https://spectra-app.vercel.app`).

---

## 3. Verifying the Deployment
1. Open your Vercel frontend URL.
2. Navigate to **Analyze** (`/analyze`).
3. Upload any image or video to run real-time deepfake classification.
4. Check **History** (`/history`) and **About** (`/about`) to ensure all client-side routes and API connections are working properly.
