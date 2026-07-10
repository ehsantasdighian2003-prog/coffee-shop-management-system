from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import psycopg2

# ==========================================
# APP
# ==========================================

app = FastAPI(
    title="Coffee Shop API ☕",
    version="1.0.0"
)

# ==========================================
# SECURITY
# ==========================================

security = HTTPBearer()

SECRET_KEY = "test123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

# ==========================================
# DATABASE
# ==========================================

def get_connection():
    return psycopg2.connect(
        dbname="coffe_shop",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )

# ==========================================
# MODELS
# ==========================================

class User(BaseModel):
    username: str
    password: str

# ==========================================
# JWT
# ==========================================

def create_access_token(data: dict):

    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload["exp"] = expire

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

# ==========================================
# AUTH
# ==========================================

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    print("TOKEN RECEIVED:", repr(token))
    print("TOKEN LENGTH:", len(token))

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("PAYLOAD:", payload)

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return user_id

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=401, detail=f"JWT Error: {str(e)}")
# ==========================================
# REGISTER
# ==========================================

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: User):

    conn = get_connection()
    cur = conn.cursor()

    try:

        # بررسی وجود کاربر
        cur.execute(
            """
            SELECT id
            FROM users
            WHERE username = %s
            """,
            (user.username,)
        )

        if cur.fetchone():
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )

        # هش کردن رمز عبور
        hashed_password = pwd_context.hash(user.password)

        # ثبت کاربر
        cur.execute(
            """
            INSERT INTO users (username, password)
            VALUES (%s, %s)
            RETURNING id
            """,
            (
                user.username,
                hashed_password
            )
        )

        user_id = cur.fetchone()[0]

        conn.commit()

        return {
            "message": "User registered successfully",
            "user_id": user_id
        }

    finally:
        cur.close()
        conn.close()


# ==========================================
# LOGIN
# ==========================================

@app.post("/login")
def login(user: User):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT id, password
            FROM users
            WHERE username = %s
            """,
            (user.username,)
        )

        db_user = cur.fetchone()

        if db_user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        user_id = db_user[0]
        hashed_password = db_user[1]

        # بررسی رمز عبور
        if not pwd_context.verify(
            user.password,
            hashed_password
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        access_token = create_access_token(
            {
                "user_id": user_id
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    finally:
        cur.close()
        conn.close()
# ==========================================
# PROTECTED ROUTE
# ==========================================

@app.get("/me")
def me(user_id: int = Depends(get_current_user)):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT id, username
            FROM users
            WHERE id = %s
            """,
            (user_id,)
        )

        user = cur.fetchone()

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return {
            "message": "You are authenticated",
            "user": {
                "id": user[0],
                "username": user[1]
            }
        }

    finally:
        cur.close()
        conn.close()


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Coffee Shop API is running 🚀"
    }
