# DeepFake Detector Backend API

The backend loads the trained 3-class ResNet50 model once at startup and serves prediction endpoints for both images and videos.

## Features

- **Image Analysis**: Classifies uploaded images into `ai`, `cgi`, or `real` with full probability distribution.
- **Video Analysis**: Samples 16 temporal frames and aggregates AI/CGI predictions with majority vote confidence.
- **Endpoints**:
  - `GET /health` - Health status and model readiness.
  - `POST /api/analyze` - Unified image and video analysis (used by frontend).
  - `POST /image/predict` - Standalone image prediction router.
  - `GET /docs` - Interactive Swagger API documentation.

## Running the Backend

From the project root (`d:\DFP`):

```powershell
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Or from inside the `backend` folder:

```powershell
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## API Documentation

Once started, open `http://127.0.0.1:8000/docs` in your browser.
