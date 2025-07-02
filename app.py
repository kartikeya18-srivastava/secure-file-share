import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from cryptography.fernet import Fernet

app = FastAPI()
UPLOAD_FOLDER = "uploads"
KEY_FILE = "filekey.key"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Generate/load encryption key
if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as keyfile:
        keyfile.write(key)
else:
    with open(KEY_FILE, "rb") as keyfile:
        key = keyfile.read()
fernet = Fernet(key)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    enc_location = os.path.join(UPLOAD_FOLDER, file.filename + ".enc")
    # Encrypt and save uploaded file
    content = await file.read()
    enc_content = fernet.encrypt(content)
    with open(enc_location, "wb") as enc_file:
        enc_file.write(enc_content)
    return {"filename": file.filename, "message": "File uploaded and encrypted."}

@app.get("/download/{filename}")
def download_file(filename: str):
    enc_location = os.path.join(UPLOAD_FOLDER, filename + ".enc")
    if not os.path.exists(enc_location):
        raise HTTPException(status_code=404, detail="File not found.")
    # Decrypt file temporarily for downloading
    with open(enc_location, "rb") as enc_file:
        enc_content = enc_file.read()
        dec_content = fernet.decrypt(enc_content)
    dec_location = os.path.join(UPLOAD_FOLDER, filename)
    with open(dec_location, "wb") as dec_file:
        dec_file.write(dec_content)
    response = FileResponse(dec_location, filename=filename)
    # Clean up decrypted file after response (optional: implement background task for deletion)
    return response