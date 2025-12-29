from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os

app = FastAPI()

# -----------------------------
# CORS Configuration
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Request Schema
# -----------------------------
class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

# -----------------------------
# Database Connection
# -----------------------------
def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def health():
    return {"status": "Backend is running"}

# -----------------------------
# Login / Signup Endpoint
# -----------------------------
@app.post("/login")
def login(data: LoginRequest):

    # Defensive validation (extra safety)
    if not data.username.strip() or not data.password.strip():
        raise HTTPException(
            status_code=400,
            detail="Username and password must not be empty"
        )

    conn = get_db()
    cur = conn.cursor()

    # Check if user exists
    cur.execute(
        "SELECT id FROM users WHERE username=%s AND password=%s",
        (data.username, data.password)
    )
    user = cur.fetchone()

    # Create user if not exists
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
