"""
YOLOv5 Web Application Backend with FastAPI
Real-time object detection with WebSocket support
Utilise les fichiers YOLOv5 locaux directement
"""

import asyncio
import base64
import io
import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import cv2
import numpy as np
import torch
import uvicorn
from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image

# YOLOv5 imports - Load from local directory
import sys

# Add parent yolov5 directory to path
YOLOV5_ROOT = Path(__file__).resolve().parents[2]
if str(YOLOV5_ROOT) not in sys.path:
    sys.path.insert(0, str(YOLOV5_ROOT))

# Import YOLOv5 modules
try:
    from models.common import DetectMultiBackend
    from utils.general import non_max_suppression, scale_boxes, check_img_size
    from utils.torch_utils import select_device
    from utils.augmentations import letterbox
    YOLOV5_AVAILABLE = True
    print("✅ Modules YOLOv5 importés avec succès")
except Exception as e:
    print(f"❌ Erreur d'import YOLOv5: {e}")
    YOLOV5_AVAILABLE = False

# Initialize FastAPI app
app = FastAPI(
    title="ZKA Detection API",
    description="API de détection d'objets en temps réel avec IA",
    version="1.0.0"
)

# Mount static files
STATIC_DIR = Path(__file__).parent.parent / "static"
if not STATIC_DIR.exists():
    STATIC_DIR.mkdir(parents=True, exist_ok=True)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Traduction des classes COCO en français
CLASS_NAMES_FR = {
    'person': 'personne',
    'bicycle': 'vélo',
    'car': 'voiture',
    'motorcycle': 'moto',
    'airplane': 'avion',
    'bus': 'bus',
    'train': 'train',
    'truck': 'camion',
    'boat': 'bateau',
    'traffic light': 'feu de circulation',
    'fire hydrant': 'borne d\'incendie',
    'stop sign': 'panneau stop',
    'parking meter': 'parcomètre',
    'bench': 'banc',
    'bird': 'oiseau',
    'cat': 'chat',
    'dog': 'chien',
    'horse': 'cheval',
    'sheep': 'mouton',
    'cow': 'vache',
    'elephant': 'éléphant',
    'bear': 'ours',
    'zebra': 'zèbre',
    'giraffe': 'girafe',
    'backpack': 'sac à dos',
    'umbrella': 'parapluie',
    'handbag': 'sac à main',
    'tie': 'cravate',
    'suitcase': 'valise',
    'frisbee': 'frisbee',
    'skis': 'skis',
    'snowboard': 'snowboard',
    'sports ball': 'ballon',
    'kite': 'cerf-volant',
    'baseball bat': 'batte de baseball',
    'baseball glove': 'gant de baseball',
    'skateboard': 'skateboard',
    'surfboard': 'planche de surf',
    'tennis racket': 'raquette de tennis',
    'bottle': 'bouteille',
    'wine glass': 'verre à vin',
    'cup': 'tasse',
    'fork': 'fourchette',
    'knife': 'couteau',
    'spoon': 'cuillère',
    'bowl': 'bol',
    'banana': 'banane',
    'apple': 'pomme',
    'sandwich': 'sandwich',
    'orange': 'orange',
    'broccoli': 'brocoli',
    'carrot': 'carotte',
    'hot dog': 'hot-dog',
    'pizza': 'pizza',
    'donut': 'donut',
    'cake': 'gâteau',
    'chair': 'chaise',
    'couch': 'canapé',
    'potted plant': 'plante en pot',
    'bed': 'lit',
    'dining table': 'table à manger',
    'toilet': 'toilettes',
    'tv': 'télévision',
    'laptop': 'ordinateur portable',
    'mouse': 'souris',
    'remote': 'télécommande',
    'keyboard': 'clavier',
    'cell phone': 'téléphone portable',
    'microwave': 'micro-ondes',
    'oven': 'four',
    'toaster': 'grille-pain',
    'sink': 'évier',
    'refrigerator': 'réfrigérateur',
    'book': 'livre',
    'clock': 'horloge',
    'vase': 'vase',
    'scissors': 'ciseaux',
    'teddy bear': 'ours en peluche',
    'hair drier': 'sèche-cheveux',
    'toothbrush': 'brosse à dents'
}

# Mount static files for JS/CSS
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Global variables
models_cache = {}
device = None  # Will be set when first model is loaded
detection_history = []
statistics = {
    "total_detections": 0,
    "total_images_processed": 0,
    "objects_detected": {},
    "avg_confidence": 0,
    "processing_times": []
}

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()


def load_model(model_name: str = "yolov5s"):
    """Load YOLOv5 model from local files"""
    global device
    
    if not YOLOV5_AVAILABLE:
        raise Exception("YOLOv5 non disponible - vérifiez l'installation")
    
    # Initialize device on first load
    if device is None:
        device = select_device('')
        print(f"📊 Device sélectionné: {device}")
    
    if model_name not in models_cache:
        try:
            print(f"🔄 Chargement du modèle {model_name}...")
            
            # Path to model weights
            model_path = YOLOV5_ROOT / f"{model_name}.pt"
            
            if not model_path.exists():
                print(f"⚠️  {model_path} non trouvé, utilisation de yolov5s.pt")
                model_path = YOLOV5_ROOT / "yolov5s.pt"
            
            if not model_path.exists():
                raise FileNotFoundError(f"Modèle non trouvé: {model_path}. Téléchargez-le depuis https://github.com/ultralytics/yolov5/releases")
            
            # Load model using DetectMultiBackend
            model = DetectMultiBackend(str(model_path), device=device, dnn=False, fp16=False)
            model.eval()
            
            models_cache[model_name] = model
            print(f"✅ Modèle {model_name} chargé avec succès!")
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement du modèle {model_name}: {e}")
            import traceback
            traceback.print_exc()
            
            # Fallback to yolov5s
            if model_name != "yolov5s":
                return load_model("yolov5s")
            raise
    
    return models_cache[model_name]


def process_image(image: Image.Image, model_name: str = "yolov5s", conf_threshold: float = 0.25):
    """Process image and return detections"""
    start_time = time.time()
    
    try:
        # Load model
        model = load_model(model_name)
        
        # Prepare image
        img = np.array(image)
        
        # Handle different image formats
        if img.ndim == 2:  # Grayscale
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        elif img.shape[2] == 4:  # RGBA
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        # Resize and letterbox
        img_size = 640
        h0, w0 = img_bgr.shape[:2]
        r = img_size / max(h0, w0)
        if r != 1:
            img_bgr = cv2.resize(img_bgr, (int(w0 * r), int(h0 * r)), interpolation=cv2.INTER_LINEAR)
        
        # Letterbox
        img_letter, ratio, (dw, dh) = letterbox(img_bgr, img_size, auto=False, scaleup=True)
        
        # Convert to tensor
        img_tensor = torch.from_numpy(img_letter).to(device)
        img_tensor = img_tensor.permute(2, 0, 1).float() / 255.0
        if img_tensor.ndimension() == 3:
            img_tensor = img_tensor.unsqueeze(0)
        
        # Inference
        with torch.no_grad():
            pred = model(img_tensor)
        
        # NMS avec seuil IoU plus élevé pour éviter doublons
        pred = non_max_suppression(pred, conf_threshold, 0.50, classes=None, agnostic=False, max_det=300)
        
        # Process detections
        detections = []
        img_display = img.copy()  # RGB image for display
        
        if pred[0] is not None and len(pred[0]) > 0:
            # Scale boxes back to original image
            pred[0][:, :4] = scale_boxes(img_tensor.shape[2:], pred[0][:, :4], img_display.shape).round()
            
            for *xyxy, conf, cls in pred[0]:
                x1, y1, x2, y2 = [int(x.item()) for x in xyxy]
                confidence = float(conf.item())
                class_id = int(cls.item())
                class_name_en = model.names[class_id]
                class_name = CLASS_NAMES_FR.get(class_name_en, class_name_en)
                
                detections.append({
                    "bbox": [x1, y1, x2, y2],
                    "confidence": confidence,
                    "class": class_name,
                    "class_id": class_id
                })
                
                # Draw on image (RGB)
                cv2.rectangle(img_display, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{class_name} {confidence:.2f}"
                (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                cv2.rectangle(img_display, (x1, y1 - label_h - 10), (x1 + label_w, y1), (0, 255, 0), -1)
                cv2.putText(img_display, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        # Convert back to PIL
        img_pil = Image.fromarray(img_display)
        
        processing_time = time.time() - start_time
        
        print(f"✅ Détection terminée: {len(detections)} objets trouvés en {processing_time:.3f}s")
        
        # Update statistics
        update_statistics(detections, processing_time)
        
        return {
            "detections": detections,
            "image": img_pil,
            "processing_time": processing_time,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Erreur lors du traitement de l'image: {e}")
        import traceback
        traceback.print_exc()
        # Return original image if error
        return {
            "detections": [],
            "image": image,
            "processing_time": time.time() - start_time,
            "timestamp": datetime.now().isoformat()
        }


def update_statistics(detections: List[dict], processing_time: float):
    """Update global statistics"""
    statistics["total_images_processed"] += 1
    statistics["total_detections"] += len(detections)
    statistics["processing_times"].append(processing_time)
    
    # Keep only last 100 processing times
    if len(statistics["processing_times"]) > 100:
        statistics["processing_times"] = statistics["processing_times"][-100:]
    
    # Update object counts
    for det in detections:
        class_name = det["class"]
        statistics["objects_detected"][class_name] = statistics["objects_detected"].get(class_name, 0) + 1
    
    # Update average confidence
    if detections:
        avg_conf = sum(d["confidence"] for d in detections) / len(detections)
        statistics["avg_confidence"] = avg_conf


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML page"""
    html_path = STATIC_DIR / "index.html"
    if html_path.exists():
        return FileResponse(html_path)
    return JSONResponse({"message": "YOLOv5 Detection API", "version": "1.0.0"})


@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "message": "ZKA Detection API",
        "version": "1.0.0",
        "yolov5_available": YOLOV5_AVAILABLE,
        "endpoints": {
            "detect": "/detect",
            "detect_batch": "/detect/batch",
            "statistics": "/statistics",
            "history": "/history",
            "models": "/models",
            "websocket": "/ws"
        }
    }


@app.post("/detect")
async def detect_image(
    file: UploadFile = File(...),
    model: str = "yolov5s",
    confidence: float = 0.35
):
    """Detect objects in uploaded image"""
    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # Process image
        result = process_image(image, model, confidence)
        
        # Convert image to base64
        buffered = io.BytesIO()
        result["image"].save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Add to history
        history_entry = {
            "timestamp": result["timestamp"],
            "filename": file.filename,
            "detections": result["detections"],
            "processing_time": result["processing_time"]
        }
        detection_history.append(history_entry)
        if len(detection_history) > 100:
            detection_history.pop(0)
        
        return JSONResponse({
            "success": True,
            "detections": result["detections"],
            "image": img_str,
            "processing_time": result["processing_time"],
            "timestamp": result["timestamp"]
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)


@app.post("/detect/batch")
async def detect_batch(files: List[UploadFile] = File(...), model: str = "yolov5s", confidence: float = 0.35):
    """Detect objects in multiple images"""
    results = []
    
    for file in files:
        try:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents)).convert("RGB")
            result = process_image(image, model, confidence)
            
            buffered = io.BytesIO()
            result["image"].save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            results.append({
                "filename": file.filename,
                "detections": result["detections"],
                "image": img_str,
                "processing_time": result["processing_time"]
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return JSONResponse({"success": True, "results": results})


@app.get("/statistics")
async def get_statistics():
    """Get detection statistics"""
    avg_processing_time = sum(statistics["processing_times"]) / len(statistics["processing_times"]) if statistics["processing_times"] else 0
    
    return JSONResponse({
        "total_detections": statistics["total_detections"],
        "total_images_processed": statistics["total_images_processed"],
        "objects_detected": statistics["objects_detected"],
        "avg_confidence": statistics["avg_confidence"],
        "avg_processing_time": avg_processing_time,
        "fps": 1 / avg_processing_time if avg_processing_time > 0 else 0
    })


@app.get("/history")
async def get_history(limit: int = 50):
    """Get detection history"""
    return JSONResponse({
        "history": detection_history[-limit:]
    })


@app.delete("/history")
async def clear_history():
    """Clear detection history"""
    detection_history.clear()
    return JSONResponse({"success": True, "message": "History cleared"})


@app.get("/models")
async def list_models():
    """List available models"""
    models = ["yolov5n", "yolov5s", "yolov5m", "yolov5l", "yolov5x"]
    return JSONResponse({"models": models})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time detection"""
    await manager.connect(websocket)
    
    try:
        while True:
            # Receive frame from client
            data = await websocket.receive_text()
            frame_data = json.loads(data)
            
            # Decode base64 image
            img_data = base64.b64decode(frame_data["frame"].split(",")[1])
            image = Image.open(io.BytesIO(img_data)).convert("RGB")
            
            # Process image
            model_name = frame_data.get("model", "yolov5s")
            confidence = frame_data.get("confidence", 0.25)
            result = process_image(image, model_name, confidence)
            
            # Convert result image to base64
            buffered = io.BytesIO()
            result["image"].save(buffered, format="JPEG", quality=85)
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # Send result back
            await websocket.send_json({
                "detections": result["detections"],
                "image": f"data:image/jpeg;base64,{img_str}",
                "processing_time": result["processing_time"],
                "timestamp": result["timestamp"]
            })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        import traceback
        traceback.print_exc()
        manager.disconnect(websocket)


if __name__ == "__main__":
    print("🚀 Démarrage du serveur ZKA...")
    
    if not YOLOV5_AVAILABLE:
        print("❌ YOLOv5 non disponible. Vérifiez l'installation.")
        sys.exit(1)
    
    # Précharger le modèle yolov5s au démarrage
    print("\n📦 Préchargement du modèle IA...")
    try:
        load_model("yolov5s")
        print("✅ Modèle chargé avec succès!\n")
    except Exception as e:
        print(f"❌ Erreur lors du préchargement: {e}")
        print("⚠️  Le serveur démarre quand même, le modèle se chargera à la première utilisation\n")
    
    print(f"🔗 Documentation API: http://localhost:8001/docs")
    print(f"🌐 Application ZKA: http://localhost:8001")
    print("\n💡 Appuyez sur Ctrl+C pour arrêter le serveur\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
