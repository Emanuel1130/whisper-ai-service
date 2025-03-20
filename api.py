from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from whisper_service import WhisperService

app = FastAPI(title="Whisper AI Service")

# Configurazione CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200", 
        "http://localhost:8080",
        "http://localhost:8000",
        "https://ematosc.pythonanywhere.com/"
    ],
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],   # Aggiunto OPTIONS per supportare i preflight request
    allow_headers=["*"],
)

# Definisco il modello da utilizzare
MODEL_SIZE = "base"  # Modelli disponibili: 'tiny', 'base', 'small', 'medium', 'large'

# Istanza del servizio Whisper
whisper_service = None

def get_whisper_service():
    """
    # Factory to obtain the instance of the WhisperService.
    # Initializes the service the first time it is requested.
    """
    global whisper_service
    if whisper_service is None:
        whisper_service = WhisperService(model_size=MODEL_SIZE)
    return whisper_service

@app.post("/transcribe/")
async def transcribe_audio(
    audio_file: UploadFile = File(...),
    language: Optional[str] = Form(None),
    service: WhisperService = Depends(get_whisper_service)
):
    """
    Endpoint to transcribe an audio file using Whisper.
    
    Args:
        audio_file: Audio file to be transcribed
        language: Optional language for the transcription
        service: Instance of the WhisperService
        
    Returns:
        JSON object containing the transcription
    """
    # Controllo se il file è un file audio
    if not audio_file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="The uploaded file is not an audio file")
    
    try:
        # Lettura del contenuto del file
        content = await audio_file.read()
        
        # Trascrizione dell'audio
        transcription = await service.transcribe(content, audio_file.filename, language)
        
        return {"transcription": transcription}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during transcription: {str(e)}")