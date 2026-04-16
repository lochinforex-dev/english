from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Brauzerdan so'rov yuborish uchun ruxsat
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Ma'lumotlarni saqlash (Oddiy baza)
class Result(BaseModel):
    name: str
    surname: str
    score: int

db = {"users": [], "total_visits": 5742}

@app.get("/api/stats")
async def get_stats():
    # Top 10 ni saralab berish
    top_10 = sorted(db["users"], key=lambda x: x['score'], reverse=True)[:10]
    return {"total": db["total_visits"], "leaderboard": top_10}

@app.post("/api/save")
async def save_result(data: Result):
    db["users"].append(data.dict())
    db["total_visits"] += 1
    return {"status": "saved"}
