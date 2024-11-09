from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel, validator

app = FastAPI()
router = APIRouter(prefix="/profiles")

profiles_db = {}

class User(BaseModel):
  email: str
  first_name: str
  last_name: str

  @validator('email')
  def validate_email(cls, value):
    if "@" not in value:
      raise ValueError("Неверный формат эмейла")
    return value

@router.post("/", response_model=User, status_code=201)
async def create_profile(user: User):
  if user.email in profiles_db:
    raise HTTPException(status_code=400, detail="Профиль уже существует")
  profiles_db[user.email] = user
  return user

@router.get("/{email}", response_model=User)
async def get_profile(email: str):
  if email not in profiles_db:
    raise HTTPException(status_code=404, detail="Профиль не найден")
  return profiles_db[email]

@router.get("/", response_model=list[User])
async def get_all_profiles():
  return list(profiles_db.values()) 

@app.get("/")
async def root():
  return {"message": "Добро пожаловать! Введите почту человека через /profiles/ для поиска профиля в базе"}

app.include_router(router)

