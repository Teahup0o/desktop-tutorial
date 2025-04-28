from fastapi import FastAPI
from fastapi.responses import JSONResponse
import asyncpg
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Créer l'application FastAPI
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
    return {"message": "Hello from FastAPI + PostgreSQL!"}

@app.get("/users")
async def get_users():
    records = await app.state.db.fetch("SELECT * FROM users;")
    users = [dict(record) for record in records]
    return JSONResponse(content={"users": users})

@app.get("/orders")
async def get_orders():
    records = await app.state.db.fetch("SELECT * FROM orders;")
    orders = [dict(record) for record in records]
    return JSONResponse(content={"orders": orders})

@app.get("/tables")
async def get_tables():
    records = await app.state.db.fetch("SELECT * FROM tables;")
    tables = [dict(record) for record in records]
    return JSONResponse(content={"tables": tables})
