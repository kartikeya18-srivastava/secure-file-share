🔐 Secure File Sharing API (FastAPI)
A simple FastAPI-based system for securely uploading and downloading files using Fernet encryption from the cryptography library.

⚙️ Features
Upload and store files in encrypted form (.enc)

Decrypt and download files on request

Uses a symmetric key stored in filekey.key

Saves encrypted files in the uploads/ directory

🚀 How to Run
Install dependencies:

bash
Copy
Edit
pip install fastapi uvicorn cryptography
Run the app:

bash
Copy
Edit
uvicorn main:app --reload
API Endpoints:

POST /upload/ — Upload and encrypt a file

GET /download/{filename} — Decrypt and download the file
