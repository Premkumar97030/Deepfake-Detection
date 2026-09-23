"""HTTP API for the DeepFake Detector frontend."""

from contextlib import asynccontextmanager
from io import BytesIO
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError

try:
    from backend.prediction_service import PredictionService
    from backend.image_predict import router as image_router
except ImportError:
    from prediction_service import PredictionService
    from image_predict import router as image_router

MAX_UPLOAD_BYTES = 500 * 1024 * 1024  # 500 MB max

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif",
    ".gif", ".svg", ".ico", ".heic", ".heif", ".avif", ".jfif",
    ".pjpeg", ".pjp", ".ppm", ".pgm", ".pnm"
}

VIDEO_EXTENSIONS = {
    ".mp4", ".webm", ".mov", ".avi", ".mkv", ".flv", ".wmv",
    ".m4v", ".3gp", ".3g2", ".ts", ".mts", ".m2ts", ".ogv",
    ".mpeg", ".mpg", ".vob", ".f4v", ".asf", ".rm", ".rmvb"
}


_predictor_instance = None


def get_predictor() -> PredictionService:
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = PredictionService()
    return _predictor_instance


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Eagerly load model on server startup
    app.state.predictor = get_predictor()
    yield


app = FastAPI(title="SPECTRA Forensic API", version="1.0.0", lifespan=lifespan)

# Allow CORS for local development and frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include sub-routers
app.include_router(image_router)


async def read_upload(file: UploadFile) -> bytes:
    payload = await file.read()
    if not payload:
        raise HTTPException(status_code=400, detail="Please choose a non-empty file.")
    if len(payload) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Files must be 500 MB or smaller.")
    return payload


@app.get("/")
def root():
    return {
        "service": "SPECTRA Forensic API",
        "status": "online",
        "endpoints": {
            "health": "/health",
            "analyze": "/api/analyze",
            "image_predict": "/image/predict",
            "docs": "/docs"
        }
    }


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "model_loaded": True}


@app.post("/api/analyze")
async def analyze_media(request: Request, file: UploadFile = File(...)) -> dict:
    content_type = (file.content_type or "").lower()
    suffix = Path(file.filename or "").suffix.lower()
    payload = await read_upload(file)
    
    predictor: PredictionService = getattr(request.app.state, "predictor", None) or get_predictor()

    is_image = content_type.startswith("image/") or suffix in IMAGE_EXTENSIONS
    is_video = content_type.startswith("video/") or suffix in VIDEO_EXTENSIONS

    if is_image:
        try:
            image = Image.open(BytesIO(payload)).convert("RGB")
        except (UnidentifiedImageError, OSError) as error:
            raise HTTPException(status_code=400, detail="The image file could not be decoded or is corrupted.") from error
        result = predictor.predict_image(image)
    elif is_video:
        video_suffix = suffix if suffix in VIDEO_EXTENSIONS else ".mp4"
        temporary_path: Path | None = None
        try:
            with NamedTemporaryFile(delete=False, suffix=video_suffix) as temporary_file:
                temporary_file.write(payload)
                temporary_path = Path(temporary_file.name)
            result = predictor.predict_video(temporary_path)
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error
        finally:
            if temporary_path and temporary_path.exists():
                temporary_path.unlink()
    else:
        # Fallback: Try decoding as Image first, then as Video
        try:
            image = Image.open(BytesIO(payload)).convert("RGB")
            result = predictor.predict_image(image)
        except Exception:
            temporary_path = None
            try:
                with NamedTemporaryFile(delete=False, suffix=".mp4") as temporary_file:
                    temporary_file.write(payload)
                    temporary_path = Path(temporary_file.name)
                result = predictor.predict_video(temporary_path)
            except Exception as error:
                raise HTTPException(status_code=400, detail="File format could not be decoded as image or video.") from error
            finally:
                if temporary_path and temporary_path.exists():
                    temporary_path.unlink()

    return {"filename": file.filename, **result}


if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    uvicorn.run("main:app", host=host, port=port, reload=False)

