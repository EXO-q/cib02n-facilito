import os
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import jwt

PWD_CTX = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET = os.getenv("JWT_SECRET", "changeme")
JWT_ALGO = "HS256"
JWT_EXP_HOURS = 6

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "facilito_login.db"

app = FastAPI(title="ms-login", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_tables():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password_hash TEXT,
            created_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()


class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@app.on_event("startup")
def startup_event():
    ensure_tables()


@app.get("/")
def health():
    return {"servicio": "ms-login", "estado": "activo"}


@app.post("/signup")
def signup(payload: SignupRequest):
    conn = get_db()
    cur = conn.cursor()

    # Verificar existencia
    cur.execute("SELECT id FROM users WHERE email = ? OR username = ?", (payload.email, payload.username))
    if cur.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Usuario o email ya registrado")

    uid = str(uuid4())
    pwd_hash = PWD_CTX.hash(payload.password)
    created = datetime.utcnow().isoformat()
    cur.execute("INSERT INTO users (id, username, email, password_hash, created_at) VALUES (?,?,?,?,?)",
                (uid, payload.username, payload.email, pwd_hash, created))
    conn.commit()
    conn.close()

    return {"id": uid, "username": payload.username, "email": payload.email}


@app.post("/login")
def login(payload: LoginRequest):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (payload.email,))
    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    stored_hash = row["password_hash"]
    if not PWD_CTX.verify(payload.password, stored_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    user_id = row["id"]
    now = datetime.utcnow()
    exp = now + timedelta(hours=JWT_EXP_HOURS)
    token = jwt.encode({"sub": user_id, "email": row["email"], "exp": int(exp.timestamp())}, JWT_SECRET, algorithm=JWT_ALGO)

    return {"access_token": token, "token_type": "bearer", "expires_at": exp.isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="127.0.0.1", port=8004, reload=True)
