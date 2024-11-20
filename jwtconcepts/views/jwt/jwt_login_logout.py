import os
import jwt
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from dotenv import load_dotenv
from jose import JWTError, ExpiredSignatureError
from fastapi_sqlalchemy import DBSessionMiddleware

# Load environment variables
load_dotenv()

# Environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Token expiration time

# Check if necessary env variables are set
if not SECRET_KEY or not ALGORITHM:
    raise ValueError("SECRET_KEY and ALGORITHM must be set in environment variables.")

# Initialize bcrypt password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Password hashing and verification
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT creation and verification
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# SQLAlchemy models
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)  # Store hashed passwords

# Database connection setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
def create_tables():
    print("Creating tables...")  # Debugging line
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")  # Debugging line

# FastAPI app
app = FastAPI()

# Middleware
app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)

# Ensure tables are created
@app.on_event("startup")
async def startup():
    create_tables()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for request and response
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class CreateUserRequest(BaseModel):
    username: str
    password: str

# Router
router = APIRouter()

# Register user
@router.post("/register")
async def register_user(request: CreateUserRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = hash_password(request.password)
    print(f"Hashed password (register): {hashed_password}")  # Debugging line
    new_user = User(username=request.username, password_hash=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Confirm that the hash is stored correctly
    print(f"User created: {new_user.username}, Hash: {new_user.password_hash}")
    
    return {"message": "User created successfully!", "username": new_user.username}

# Login route
@router.post("/login", response_model=TokenResponse)
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_request.username).first()
    print(f"User found: {user}")  # Debugging line
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Debugging: Verify password
    print(f"Password entered: {login_request.password}")  # Check the entered password
    print(f"Password hash stored in DB: {user.password_hash}")  # Check the stored hash
    
    if not verify_password(login_request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    print(f"Generated access token: {access_token}")  # Debugging line
    return {"access_token": access_token, "token_type": "bearer"}

# Add the router to the app
app.include_router(router, prefix="/auth")
