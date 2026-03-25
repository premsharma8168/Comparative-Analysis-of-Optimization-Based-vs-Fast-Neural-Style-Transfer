from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import shutil
import os
import uuid
from backend.nst_optimization import optimize_nst
from backend.nst_fast import fast_nst

app = FastAPI(title="NST Benchmark API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
MODELS_DIR = os.path.join(BASE_DIR, "models")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(FRONTEND_DIR, exist_ok=True)

app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")
app.mount("/results", StaticFiles(directory=RESULTS_DIR), name="results")
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

@app.get("/")
def read_root():
    return RedirectResponse(url="/frontend/index.html")

@app.post("/api/optimize")
def api_optimize(content: UploadFile = File(...), style: UploadFile = File(...), steps: int = Form(50)):
    content_id = str(uuid.uuid4())
    style_id = str(uuid.uuid4())
    result_id = str(uuid.uuid4())
    
    content_ext = content.filename.split('.')[-1]
    style_ext = style.filename.split('.')[-1]
    
    content_path = os.path.join(UPLOADS_DIR, f"{content_id}.{content_ext}")
    style_path = os.path.join(UPLOADS_DIR, f"{style_id}.{style_ext}")
    output_path = os.path.join(RESULTS_DIR, f"{result_id}.jpg")
    
    with open(content_path, "wb") as f:
        shutil.copyfileobj(content.file, f)
    with open(style_path, "wb") as f:
        shutil.copyfileobj(style.file, f)
        
    try:
        time_taken = optimize_nst(content_path, style_path, output_path, steps=steps)
        return {"status": "success", "result_url": f"/results/{result_id}.jpg", "time_taken": round(time_taken, 2), "method": "Optimization-Based"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/fast")
def api_fast(content: UploadFile = File(...), model_name: str = Form(...)):
    if not model_name.endswith('.t7'):
        model_name += '.t7'
    model_path = os.path.join(MODELS_DIR, model_name)
    if not os.path.exists(model_path):
        raise HTTPException(status_code=400, detail="Fast NST model not found.")
        
    content_id = str(uuid.uuid4())
    result_id = str(uuid.uuid4())
    content_ext = content.filename.split('.')[-1]
    
    content_path = os.path.join(UPLOADS_DIR, f"{content_id}.{content_ext}")
    output_path = os.path.join(RESULTS_DIR, f"{result_id}.jpg")
    
    with open(content_path, "wb") as f:
        shutil.copyfileobj(content.file, f)
        
    try:
        time_taken = fast_nst(content_path, model_path, output_path)
        return {"status": "success", "result_url": f"/results/{result_id}.jpg", "time_taken": round(time_taken, 2), "method": f"Fast NST ({model_name})"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/models")
async def list_models():
    models = []
    if os.path.exists(MODELS_DIR):
        models = [f for f in os.listdir(MODELS_DIR) if f.endswith('.t7')]
    return {"models": models}
