from passlib.context import CryptContext
from fastapi import HTTPException, UploadFile

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(raw, hashed):
    return pwd_context.verify(raw, hashed)

def is_allowed_file(file: UploadFile, role: str):
    if role == "ops":
        return file.content_type in ["application/vnd.openxmlformats-officedocument.presentationml.presentation",
                                     "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]
    return False
