from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

@app.get("/")
def health():
    return {"status": "Backend is running"}

@app.post("/login")
def login(data: LoginRequest):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM users WHERE username=%s AND password=%s",
        (data.username, data.password)
    )

    user = cur.fetchone()

    if not user:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (data.username, data.password)
        )
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "User created and logged in"}

    cur.close()
    conn.close()
    return {"message": "Login successful"}
