from fastapi import FastAPI
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

cred = credentials.Certificate("firebase_key.json")
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
