from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Lip Reader")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def root():
    return {"status": "Lip Reader Backend läuft"}

@app.get("/training-sentences")
def get_sentences():
    return [
        "Hallo",
        "Bitte Wasser",
        "Bitte Hilfe",
        "Ich habe Schmerzen",
        "Mir ist kalt",
        "Danke",
        "Ja",
        "Nein"
    ]

@app.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())
    return {"message": "Video gespeichert", "filename": file.filename}

@app.post("/predict")
async def predict():
    return {"predicted_text": "Demo: Bitte Wasser"}
