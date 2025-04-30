# app.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import asyncpg, os, io, datetime
from dotenv import load_dotenv
from steg_custom import encode_lsb
from PIL import Image

load_dotenv()
app = FastAPI()

# DB 
@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
    )

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

# ROUTES EXISTANTES 
@app.get("/")
async def root():
    return {"message": "Hello from FastAPI + PostgreSQL!"}


# upload photo + steganographie 
@app.post("/upload_profile_photo")
async def upload_profile_photo(
    user_id: int = Form(...),
    file: UploadFile = File(...)
):
    if file.content_type not in ("image/png", "image/jpeg"):
        raise HTTPException(status_code=400, detail="PNG ou JPG uniquement")

    raw = await file.read()
    img = Image.open(io.BytesIO(raw)).convert("RGB")

    secret = f"{user_id}|{datetime.date.today()}"
    try:
        stego = encode_lsb(img, secret.encode())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    buf = io.BytesIO()
    stego.save(buf, format="PNG")
    stego_bytes = buf.getvalue()

    await app.state.db.execute(
        "UPDATE users SET photo=$1 WHERE id=$2;",
        stego_bytes, user_id
    )
    return {"ok": True, "embedded": secret}
