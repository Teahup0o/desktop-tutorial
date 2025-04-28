from fastapi import FastAPI
from dotenv import load_dotenv
import asyncpg
import os

# Charger les variables du .env
load_dotenv()

# Créer l'app FastAPI
app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT"))
    )

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

@app.get("/")
async def read_root():
    return {"message": "Hello, database is connected!"}
