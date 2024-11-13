# # # from fastapi import FastAPI, Depends, HTTPException, status
# # # from sqlalchemy.orm import Session
# # # from auth import create_token, verify_token
# # # from database import SessionLocal, engine
# # # from models import User
# # # from pydantic import BaseModel

# # # app = FastAPI()

# # # class UserRegister(BaseModel):
# # #     email: str
# # #     password: str
# # #     role: str

# # # @app.post("/users/register")
# # # def register_user(user: UserRegister, db: Session = Depends(SessionLocal)):
# # #     db_user = User(email=user.email, password=user.password, role=user.role)
# # #     db.add(db_user)
# # #     db.commit()
# # #     return {"msg": "User registered successfully"}

# # # class UserLogin(BaseModel):
# # #     email: str
# # #     password: str

# # # @app.post("/users/login")
# # # def login_user(user: UserLogin, db: Session = Depends(SessionLocal)):
# # #     db_user = db.query(User).filter(User.email == user.email).first()
# # #     if not db_user or db_user.password != user.password:
# # #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
# # #     token = create_token(db_user.id)
# # #     return {"token": token}














# # from fastapi import FastAPI, Depends, HTTPException, status
# # from sqlalchemy.orm import Session
# # from auth import create_token, verify_token
# # from database import SessionLocal, engine
# # from models import User, PZTTile
# # from pydantic import BaseModel

# # app = FastAPI()


# # class UserRegister(BaseModel):
# #     email: str
# #     password: str
# #     role: str  # "admin" or "planner"

# # class UserLogin(BaseModel):
# #     email: str
# #     password: str


# # @app.post("/users/register")
# # def register_user(user: UserRegister, db: Session = Depends(SessionLocal)):
# #     db_user = User(email=user.email, password=user.password, role=user.role)
# #     db.add(db_user)
# #     db.commit()
# #     return {"msg": "User registered successfully"}



# # @app.post("/users/login")
# # def login_user(user: UserLogin, db: Session = Depends(SessionLocal)):
# #     db_user = db.query(User).filter(User.email == user.email).first()
# #     if not db_user or db_user.password != user.password:
# #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
# #     token = create_token(db_user.id)
# #     return {"token": token}



# # @app.get("/pzt/tiles")
# # def get_tiles(db: Session = Depends(SessionLocal)):
# #     return db.query(PZTTile).all()



# # class AreaCalculationRequest(BaseModel):
# #     length: float
# #     width: float
# #     foot_traffic: int  # Average footsteps per day

# # @app.post("/pzt/calculate-tiles")
# # def calculate_tiles(area: AreaCalculationRequest, db: Session = Depends(SessionLocal)):
# #     total_area = area.length * area.width
# #     tiles = db.query(PZTTile).all()

# #     results = []
# #     for tile in tiles:
# #         num_tiles = total_area / tile.size
# #         daily_energy = num_tiles * tile.power_capacity * area.foot_traffic
# #         monthly_energy = daily_energy * 30
# #         results.append({
# #             "tile_id": tile.id,
# #             "num_tiles": num_tiles,
# #             "daily_energy": daily_energy,
# #             "monthly_energy": monthly_energy
# #         })
# #     return results
























# # main.py

# from fastapi import FastAPI, Depends, HTTPException, status
# from pydantic import BaseModel
# from typing import Any, List
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from datetime import datetime, timedelta

# app = FastAPI()

# # Security and token setup
# SECRET_KEY = "your_secret_key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # Mock database for simplicity
# fake_users_db = {}

# # Models
# class User(BaseModel):
#     username: str
#     email: str
#     password: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class Tile(BaseModel):
#     tile_id: int
#     size_sqm: float
#     power_generation_per_footstep: float
#     cost: float

# # Helper functions
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)

# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# # Routes
# @app.post("/users/register", response_model=Token)
# async def register_user(user: User):
#     # Store user in fake database with hashed password
#     user_data = user.dict()
#     user_data["password"] = get_password_hash(user.password)
#     fake_users_db[user.email] = user_data
#     access_token = create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# @app.post("/users/login", response_model=Token)
# async def login(user: User):
#     user_db = fake_users_db.get(user.email)
#     if not user_db or not verify_password(user.password, user_db["password"]):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#         )
#     access_token = create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# @app.get("/pzt/tiles", response_model=List[Tile])
# async def get_pzt_tiles():
#     # Example tile data
#     tile_data = [
#         {"tile_id": 1, "size_sqm": 0.5, "power_generation_per_footstep": 1.2, "cost": 100},
#         {"tile_id": 2, "size_sqm": 1.0, "power_generation_per_footstep": 2.5, "cost": 200}
#     ]
#     return tile_data

# @app.post("/pzt/calculate-tiles")
# async def calculate_tiles(length: float, width: float, foot_traffic: int):
#     area = length * width
#     tile_size = 0.5  # For example, each tile is 0.5 sqm
#     num_tiles = area / tile_size
#     power_per_footstep = 1.2
#     estimated_energy = power_per_footstep * foot_traffic * num_tiles
#     return {"area": area, "num_tiles": int(num_tiles), "estimated_energy": estimated_energy}

































from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

app = FastAPI()

# Security and token setup
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Mock database for simplicity
fake_users_db = {}

# Models
class UserRegister(BaseModel):
    email: str
    password: str
    role: Optional[str] = "user"  # Default role is "user" if not specified

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Tile(BaseModel):
    tile_id: int
    size_sqm: float
    power_generation_per_footstep: float
    cost: float

class AreaCalculationRequest(BaseModel):
    length: float
    width: float
    foot_traffic: int

# Helper functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Routes
@app.post("/users/register", response_model=Token)
async def register_user(user: UserRegister):
    # Store user in fake database with hashed password
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_data = user.dict()
    user_data["password"] = get_password_hash(user.password)
    fake_users_db[user.email] = user_data
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/login", response_model=Token)
async def login(user: UserLogin):
    user_db = fake_users_db.get(user.email)
    if not user_db or not verify_password(user.password, user_db["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/pzt/tiles", response_model=List[Tile])
async def get_pzt_tiles():
    # Example tile data
    tile_data = [
        {"tile_id": 1, "size_sqm": 0.5, "power_generation_per_footstep": 1.2, "cost": 100},
        {"tile_id": 2, "size_sqm": 1.0, "power_generation_per_footstep": 2.5, "cost": 200}
    ]
    return tile_data

@app.post("/pzt/calculate-tiles")
async def calculate_tiles(request: AreaCalculationRequest):
    area = request.length * request.width
    tile_size = 0.5  # Assuming each tile is 0.5 sqm
    num_tiles = area / tile_size
    power_per_footstep = 1.2  # Example power per footstep in watts
    estimated_energy = power_per_footstep * request.foot_traffic * num_tiles
    return {"area": area, "num_tiles": int(num_tiles), "estimated_energy": estimated_energy}
