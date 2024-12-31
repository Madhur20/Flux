from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import Optional
from PIL import Image
import pytesseract
import io
from pathlib import Path

# Initialize the FastAPI app
app = FastAPI()

# Directory to save uploaded images
UPLOAD_FOLDER = Path("uploaded_images")
UPLOAD_FOLDER.mkdir(exist_ok=True)

# Request and Response Models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# Health Endpoint
@app.get("/health")
def health():
    return {"status": "healthy"}

# Detect Chat Endpoint (Save Image)
@app.post("/detect_chat")
async def detect_chat(file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

        # Save the image to the UPLOAD_FOLDER
        file_path = UPLOAD_FOLDER / file.filename
        with open(file_path, "wb") as f:
            f.write(await file.read())

        return {"message": "Image successfully uploaded", "file_path": str(file_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Response Endpoint
@app.post("/get_response", response_model=ChatResponse)
def get_response(chat_request: ChatRequest):
    # Placeholder response logic
    response_message = f"Echo: {chat_request.message}"
    return ChatResponse(response=response_message)

# Run the application with: uvicorn script_name:app --reload
def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

run_api()
