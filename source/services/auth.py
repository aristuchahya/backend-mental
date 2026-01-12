from sqlalchemy.orm import Session
from source.models.models import Admin
from passlib.context import CryptContext
from jose import jwt
import datetime

SECRET_KEY = "rahasia_21"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_user(db: Session, username: str, role: str, password: str):
    hashed_password = pwd_context.hash(password)
    user = Admin(username=username, role=role, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(Admin).filter(Admin.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.param_functions import Depends
from fastapi.security.api_key import APIKeyHeader

authorize = APIKeyHeader(name="Authorization", auto_error=False)

def get_current_user(token = Depends(authorize)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if token is None:
            raise credentials_exception
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userdata: str = payload.get("sub")
        if userdata is None:
            raise credentials_exception
        print(userdata)
        return userdata
    except:
        raise credentials_exception