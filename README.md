# EZ Backend (FastAPI)

This is a document management backend using FastAPI and MongoDB Atlas.

## Features

- Client & Ops login
- JWT-based Auth
- File upload & download with validation
- Role-based access

## Getting Started

### Setup

1. Create a `.env` file:
    MONGODB URI: "your-own-key"

2. Install dependencies:

```bash
pip install -r requirements.txt

run server:
uvicorn app.main:app --reload


