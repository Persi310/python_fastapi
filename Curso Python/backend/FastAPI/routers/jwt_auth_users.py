from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "10930381a35b6300317908675fdd2ccfa1ab363c96d8c6a03b8d138638b10c85"

app = APIRouter(prefix="/jwt_auth", responses={404: {"message": "No encontrado"}}, tags=["jwt_auth"])

#fakehashedsecret

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword")


class Token(BaseModel):
    access_token: str 
    token_type: str
    
class TokenData(BaseModel):
    username: str | None = None 

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool 
    
class UserDB(User):
    password: str
    
users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "disable": False,
        "password": "$argon2id$v=19$m=65536,t=3,p=4$BDhr3jMaWatMDjUbDlhn0g$XAXZIBYaI1Lbvo2F4On5wHvHjWwhirfMssCrlwEY+0s"
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "disable": False,
        "password": "$argon2id$v=19$m=65536,t=3,p=4$BDhr3jMaWatMDjUbDlhn0g$XAXZIBYaI1Lbvo2F4On5wHvHjWwhirfMssCrlwEY+0s"
    },
    "persi": {
        "username": "persi",
        "full_name": "Persi Casado",
        "email": "persi@example.com",
        "disable": False,
        "password": "$argon2id$v=19$m=65536,t=3,p=4$BDhr3jMaWatMDjUbDlhn0g$XAXZIBYaI1Lbvo2F4On5wHvHjWwhirfMssCrlwEY+0s"
    },
}

    
def search_user_db( username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user( username: str):
    if username in users_db:
        return User(**users_db[username])
    
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)


def authenticate_user( username: str, password: str):
    user = search_user_db(username)
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
    
        if username is None:
            raise exception
    
    except InvalidTokenError:
        raise exception
    
    return search_user(username)
    

async def current_user(user: User = Depends(auth_user)):
    if user.disable: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo")
        
    return user 

@app.post("/login")
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user_db = authenticate_user(form.username, form.password)
    
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El usuario o contraseña son incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_db.username}, expires_delta=access_token_expires
    )
        
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user