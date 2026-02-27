import bcrypt
#import jwt
from datetime import datetime, timedelta
from fastapi import Request, Depends
from sqlalchemy.orm import Session
from Application.Database.session import get_read_db
from Application.Database.models.user import User

SECRET_KEY = "super-secret-key-change-this-later" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(password: str) -> str:
    pwd_bytes = password[:72].encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password[:72].encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    #return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return "fake-token-for-demo" 

def get_current_user_from_cookie(request: Request, db: Session = Depends(get_read_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    #try:
    #    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #    username: str = payload.get("sub")
    #    if username is None:
    #        return None
    #except jwt.PyJWTError:
    #    return None
    username = "demo_user" 
    user = db.query(User).filter(User.username == username).first()
    return user