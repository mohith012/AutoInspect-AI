from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import shutil
import uuid
import sys
import urllib.request
import urllib.parse
import json
import math
from fastapi import Query

# Ensure project root is in sys.path to load pipeline modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the master pipeline
from stages.full_pipeline.core.pipeline import analyze_vehicle_damage
from stages.full_pipeline.core.visualization import draw_visualizations

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
        
    except ValueError as ve:
        return JSONResponse(status_code=400, content={"error": str(ve)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

@app.get("/api/nearby-shops")
async def get_nearby_shops(
    lat: float = Query(...),
    lon: float = Query(...),
    radius: int = Query(5000)
):
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json][timeout:25];
    (
      node["shop"="car_repair"](around:{radius},{lat},{lon});
      way["shop"="car_repair"](around:{radius},{lat},{lon});
      node["shop"="tyres"](around:{radius},{lat},{lon});
      way["shop"="tyres"](around:{radius},{lat},{lon});
    );
    out center;
    """
    try:
        import ssl
        ssl_context = ssl._create_unverified_context()
        req = urllib.request.Request(
            overpass_url, 
            data=overpass_query.encode('utf-8'),
            headers={'User-Agent': 'AutoInspect AI / 1.0'}
        )
        with urllib.request.urlopen(req, context=ssl_context) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        shops = []
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            name = tags.get("name", "Unknown Repair Shop")
            shop_lat = element.get("lat") or element.get("center", {}).get("lat")
            shop_lon = element.get("lon") or element.get("center", {}).get("lon")
            
            if not shop_lat or not shop_lon: continue
            
            dist_km = haversine(lat, lon, shop_lat, shop_lon)
            
            addr = []
            if tags.get("addr:street"): addr.append(tags.get("addr:street"))
            if tags.get("addr:city"): addr.append(tags.get("addr:city"))
            address = ", ".join(addr) if addr else "Address not provided"
            
            phone = tags.get("phone") or tags.get("contact:phone")
            
            category = "Auto Repair"
            if tags.get("shop") == "tyres": category = "Tyre Shop"
            
            shops.append({
                "id": element["id"],
                "name": name,
                "lat": shop_lat,
                "lon": shop_lon,
                "distance": round(dist_km, 2),
                "address": address,
                "phone": phone,
                "category": category,
                "rating": None,
                "reviews": None,
                "open_status": tags.get("opening_hours")
            })
            
        shops.sort(key=lambda x: x["distance"])
        return JSONResponse(content={"shops": shops})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e) or repr(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
