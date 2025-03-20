from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
from whisper_service import WhisperService

app = FastAPI(title="Whisper AI Service")

# Configurazione CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200", 
        "http://localhost:8080",
        "http://localhost:8000",
        "https://ematosc.pythonanywhere.com/",
        "https://www.wraiter.it",
        "https://transcription.wraiter.it"
    ],
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],   # Aggiunto OPTIONS per supportare i preflight request
    allow_headers=["*"],
)

# Definisco il modello da utilizzare, leggendo da variabile d'ambiente o utilizzando un valore predefinito
MODEL_SIZE = os.environ.get("MODEL_SIZE", "base")  # Legge da variabile d'ambiente o usa "base" come default
print(f"Usando il modello Whisper: {MODEL_SIZE}")

# Istanza del servizio Whisper
whisper_service = None

def get_whisper_service():
    """
    Factory per ottenere l'istanza del servizio WhisperService.
    Inizializza il servizio la prima volta che viene richiesto.
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
    Endpoint per trascrivere un file audio utilizzando Whisper.
    
    Args:
        audio_file: File audio da trascrivere
        language: Lingua opzionale per la trascrizione
        service: Istanza del servizio WhisperService
        
    Returns:
        Oggetto JSON contenente la trascrizione
    """
    # Controllo se il file è un file audio
    if not audio_file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Il file caricato non è un file audio")
    
    try:
        # Lettura del contenuto del file
        content = await audio_file.read()
        
        # Trascrizione dell'audio
        transcription = await service.transcribe(content, audio_file.filename, language)
        
        return {"transcription": transcription}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore durante la trascrizione: {str(e)}")