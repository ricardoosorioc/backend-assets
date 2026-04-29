import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# CONFIGURACIÓN BASE DE DATOS
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "3b89f7a9d8e6c5")

if not URL or not KEY:
    print("ERROR: No se encontraron las credenciales de Supabase en las variables de entorno")

supabase: Client = create_client(URL, KEY)

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# MODELOS
class Asset(BaseModel):
    name: str
    type: str
    status: str

# SEGURIDAD
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#  AUTENTICACIÓN 
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    
    if form_data.username == "admin" and form_data.password == "admin123":
        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Usuario o clave incorrecta")

# CRUD 
@app.get("/assets")
def read_assets():
    response = supabase.table("assets").select("*").execute()
    return response.data

@app.post("/assets")
def create_asset(asset: Asset, token: str = Depends(oauth2_scheme)):
    response = supabase.table("assets").insert(asset.dict()).execute()
    return response.data

@app.delete("/assets/{asset_id}")
def delete_asset(asset_id: int, token: str = Depends(oauth2_scheme)):
    supabase.table("assets").delete().eq("id", asset_id).execute()
    return {"message": "Eliminado"}