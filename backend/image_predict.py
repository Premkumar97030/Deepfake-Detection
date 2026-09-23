from io import BytesIO
import torch
from PIL import Image
from torchvision import transforms
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path

try:
    from backend import config
    from backend.models.resnet import ImageClassifier
except ImportError:
    import config
    from models.resnet import ImageClassifier


router = APIRouter(
    prefix="/image",
    tags=["Image Detection"]
)

transform = transforms.Compose([
    transforms.Resize((config.IMAGE_SIZE, config.IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


def load_model():
    model = ImageClassifier()
    weights_path = config.NEW_MODEL_PATH if Path(config.NEW_MODEL_PATH).exists() else config.MODEL_PATH
    if not Path(weights_path).exists():
        raise FileNotFoundError(f"Model weights file not found: {weights_path}")
    
    checkpoint = torch.load(weights_path, map_location=config.DEVICE)
    if isinstance(checkpoint, dict) and "state_dict" in checkpoint:
        checkpoint = checkpoint["state_dict"]

    cleaned_state_dict = {
        key.removeprefix("module."): value for key, value in checkpoint.items()
    }
    model.load_state_dict(cleaned_state_dict)
    model = model.to(config.DEVICE)
    model.eval()
    return model


_model = None


def get_model():
    global _model
    if _model is None:
        _model = load_model()
    return _model


@router.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    if not file.content_type:
        raise HTTPException(status_code=400, detail="Invalid file type.")

    allowed_types = ["image/jpeg", "image/png", "image/webp", "image/bmp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, PNG, WEBP and BMP images are supported."
        )

    image_data = await file.read()
    try:
        image = Image.open(BytesIO(image_data)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Unable to read image.")

    image_tensor = transform(image).unsqueeze(0).to(config.DEVICE)
    model = get_model()

    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.softmax(outputs, dim=1)[0]

    predicted_index = torch.argmax(probabilities).item()
    predicted_class = config.CLASS_NAMES[predicted_index]
    confidence = probabilities[predicted_index].item() * 100

    class_probabilities = {
        class_name: round(probabilities[i].item() * 100, 2)
        for i, class_name in enumerate(config.CLASS_NAMES)
    }

    return {
        "filename": file.filename,
        "prediction": predicted_class,
        "confidence": round(confidence, 2),
        "probabilities": class_probabilities
    }
