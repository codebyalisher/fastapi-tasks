from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import FastAPI
from models.user_login_logout import User  # Make sure User is imported
from fastapi_sqlalchemy import DBSessionMiddleware

# Database URL
DATABASE_URL = "sqlite:///./test.db"

# Set up SQLAlchemy engine and sessionmaker
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Function to create tables on startup
def create_tables():
    Base.metadata.create_all(bind=engine)  # This ensures that all tables, including 'users', are created
    print("Tables created successfully!")

# Initialize FastAPI app
app = FastAPI()

# Add DBSessionMiddleware to inject database session
app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)

# Ensure tables are created on startup
@app.on_event("startup")
async def startup():
    create_tables()  # Ensure tables are created at startup
    print("Tables created on startup.")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
