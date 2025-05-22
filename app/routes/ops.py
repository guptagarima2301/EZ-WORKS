from fastapi import APIRouter, Depends, UploadFile, HTTPException
from app.models import UserLogin
from app.auth import create_token, get_token_data
from app.utils import verify_password, is_allowed_file
from app.database import db
from fastapi import File

router = APIRouter()

@router.post("/ops/login")
async def ops_login(user: UserLogin):
    found = await db.users.find_one({"email": user.email, "role": "ops"})
    if not found or not verify_password(user.password, found["password"]):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return {"token": create_token({"email": user.email, "role": "ops"})}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), token_data: dict = Depends(get_token_data)):
    if not is_allowed_file(file, token_data['role']):
        raise HTTPException(status_code=403, detail="Invalid file type")
    content = await file.read()
    await db.files.insert_one({
        "filename": file.filename,
        "content": content,
        "uploaded_by": token_data["email"]
    })
    return {"message": "File uploaded successfully"}