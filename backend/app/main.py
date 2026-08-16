from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import shutil
import uuid
import sys

# Ensure project root is in sys.path to load pipeline modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the master pipeline
from stage5_full_pipeline.core.pipeline import analyze_vehicle_damage
from stage5_full_pipeline.core.visualization import draw_visualizations

app = FastAPI(title="AutoInspect AI")

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files to serve the annotated images
STATIC_DIR = os.path.join(current_dir, "../static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

UPLOAD_DIR = os.path.join(current_dir, "../uploads")
RESULTS_DIR = os.path.join(STATIC_DIR, "results")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

@app.post("/api/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    vehicle_make: str = Form(None),
    vehicle_model: str = Form(None),
    vehicle_year: int = Form(None)
):
    try:
        # Save uploaded file
        file_ext = os.path.splitext(file.filename)[1]
        unique_id = str(uuid.uuid4())
        safe_filename = f"{unique_id}{file_ext}"
        upload_path = os.path.join(UPLOAD_DIR, safe_filename)
        
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        vehicle_info = None
        if vehicle_make and vehicle_model:
            vehicle_info = {
                "make": vehicle_make,
                "model": vehicle_model,
                "year": vehicle_year or 2022
            }
            
        # Run AI Pipeline
        result_json = analyze_vehicle_damage(upload_path, save_crops=False, vehicle_info=vehicle_info)
        
        # Generate Visualization
        vis_filename = f"{unique_id}_annotated.jpg"
        vis_path = os.path.join(RESULTS_DIR, vis_filename)
        draw_visualizations(upload_path, result_json, vis_path)
        
        # Inject the visualization URL into the response
        result_json["image_url"] = f"/static/results/{vis_filename}"
        
        return JSONResponse(content=result_json)
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
