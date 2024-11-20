from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from fastapi_sqlalchemy import DBSessionMiddleware
from pydantic import BaseModel
from views.jwt.jwt_login_logout import create_access_token, verify_password

# Pydantic Models
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# SQLAlchemy Models
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)  # Store hashed passwords

# Database URL
DATABASE_URL = "sqlite:///./test.db"

# Set up SQLAlchemy engine and sessionmaker
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to create tables on startup
def create_tables():
    print("Creating tables...")  # Debugging: Check if this function is called
    Base.metadata.create_all(bind=engine)  # This ensures that all tables, including 'users', are created
    print("Tables created successfully!")  # Debugging: Ensure table creation is successful

# Initialize FastAPI app
app = FastAPI()

# Add DBSessionMiddleware to inject database session
app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)

# Ensure tables are created on startup
@app.on_event("startup")
async def startup():
    create_tables()  # Ensure tables are created at startup
    print("Tables created on startup.")  # Debugging: Verify this step is reached

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create the router for auth routes
router = APIRouter()

# Login route to authenticate and generate JWT token
@router.post("/login", response_model=TokenResponse)
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    # Debugging: Check if the user exists
    user = db.query(User).filter(User.username == login_request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Debugging: Verify password
    if not verify_password(login_request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Create JWT token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Logout route (usually handled client-side, this just invalidates the token server-side)
@router.post("/logout")
async def logout():
    # For logout, you usually remove the token client-side (clear cookies, local storage, etc.)
    return {"message": "Successfully logged out"}

# Add the router to the app
app.include_router(router, prefix="/auth")
