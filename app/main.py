from fastapi import FastAPI
from app.routes import ops, client

app = FastAPI()

app.include_router(ops.router)
app.include_router(client.router)
