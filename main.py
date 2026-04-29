from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Asset Management API")

# Configuración de CORS para conectar con Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para pruebas
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de datos simple
class Asset(BaseModel):
    id: int
    name: str
    type: str
    status: str

# Base de datos ficticia para rapidez (puedes conectar Supabase luego)
db_assets = [
    {"id": 1, "name": "Dell XPS 15", "type": "Laptop", "status": "Assigned"},
    {"id": 2, "name": "Monitor LG 27'", "type": "Peripheral", "status": "Available"},
]

@app.get("/")
def home():
    return {"message": "API de Gestión de Activos corriendo"}

@app.get("/assets", response_model=List[Asset])
def get_assets():
    return db_assets

@app.post("/assets")
def create_asset(asset: Asset):
    db_assets.append(asset.dict())
    return {"message": "Activo registrado con éxito", "asset": asset}