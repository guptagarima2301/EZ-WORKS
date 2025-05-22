import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from fastapi import Header, HTTPException, status, Depends

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")

def create_token(data: dict, expires: int = 60):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=expires)
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def verify_token(token: str):
    try:
        token = token.strip()
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None
    
async def get_token_data(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return payload
