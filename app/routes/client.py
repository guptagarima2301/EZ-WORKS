from fastapi import APIRouter, HTTPException
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import UserSignup, UserLogin
from app.utils import hash_password, verify_password
from app.auth import create_token, verify_token
from app.database import db

router = APIRouter()


@router.post("/client/signup")
async def signup(user: UserSignup):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Only allow client or ops roles for security
    if user.role not in ("client", "ops"):
        raise HTTPException(status_code=400, detail="Invalid role")

    encrypted_url = create_token({"email": user.email, "role": user.role}, expires=1440)
    await db.users.insert_one({
        "email": user.email,
        "password": hash_password(user.password),
        "role": user.role,
        "verified": False
    })
    return {"encrypted_url": f"/{user.role}/verify/{encrypted_url}"}

@router.get("/client/verify/{token}")
async def verify_user(token: str):
    data = verify_token(token)
    if not data:
        raise HTTPException(status_code=400, detail="Invalid token")
    await db.users.update_one({"email": data["email"]}, {"$set": {"verified": True}})
    return {"message": "Email verified successfully"}

@router.post("/client/login")
async def login(user: UserLogin):
    found = await db.users.find_one({"email": user.email, "role": "client"})
    if not found or not verify_password(user.password, found["password"]):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    if not found.get("verified"):
        raise HTTPException(status_code=403, detail="Email not verified")
    return {"token": create_token({"email": user.email, "role": "client"})}

@router.get("/client/files")
async def list_files():
    files = await db.files.find().to_list(100)
    return files

@router.get("/download-file/{file_id}")
async def generate_download_link(file_id: str, token_data=Depends(create_token)):
    if token_data["role"] != "client":
        raise HTTPException(status_code=403, detail="Only clients can download")
    secure_url = create_token({"file_id": file_id, "role": "client"}, expires=10)
    return {"download_link": f"/download/{secure_url}"}
