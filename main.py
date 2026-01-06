from fastapi import FastAPI
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os, json

# 🔑 Load Firebase key from Render ENV
firebase_key = os.getenv("FIREBASE_KEY")

if not firebase_key:
    raise Exception("FIREBASE_KEY not found")

cred = credentials.Certificate(json.loads(firebase_key))
firebase_admin.initialize_app(cred)

db = firestore.client()

app = FastAPI()

class Contact(BaseModel):
    name: str
    email: str
    message: str

@app.post("/contact")
def save_contact(data: Contact):
    db.collection("contacts").add({
        "name": data.name,
        "email": data.email,
        "message": data.message,
        "created_at": datetime.utcnow()
    })
    return {"status": "success"}
