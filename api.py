from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any
from whisper_service import WhisperService
import uuid
import time

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
    allow_methods=["POST", "GET", "OPTIONS"],   # Aggiunto GET per il polling
    allow_headers=["*"],
)

# Definisco il modello da utilizzare
MODEL_SIZE = "base"  # Modelli disponibili: 'tiny', 'base', 'small', 'medium', 'large'

# Istanza del servizio Whisper
whisper_service = None

# Dizionario per memorizzare i job di trascrizione
# job_id -> {status, result, error, created_at}
transcription_jobs: Dict[str, Dict[str, Any]] = {}

def get_whisper_service():
    """
    # Factory to obtain the instance of the WhisperService.
    # Initializes the service the first time it is requested.
    """
    global whisper_service
    if whisper_service is None:
        whisper_service = WhisperService(model_size=MODEL_SIZE)
    return whisper_service

async def process_transcription(job_id: str, audio_content: bytes, filename: str, language: Optional[str], service: WhisperService):
    """
    Funzione di background per elaborare la trascrizione
    """
    try:
        # Trascrizione dell'audio
        transcription = await service.transcribe(audio_content, filename, language)
        
        # Aggiornamento dello stato del job
        transcription_jobs[job_id]["status"] = "completed"
        transcription_jobs[job_id]["result"] = transcription
    except Exception as e:
        transcription_jobs[job_id]["status"] = "error"
        transcription_jobs[job_id]["error"] = str(e)

@app.post("/transcribe/")
async def transcribe_audio(
    background_tasks: BackgroundTasks,
    audio_file: UploadFile = File(...),
    language: Optional[str] = Form(None),
    service: WhisperService = Depends(get_whisper_service)
):
    """
    Endpoint per inviare un file audio da trascrivere in modo asincrono
    
    Args:
        audio_file: File audio da trascrivere
        language: Lingua opzionale per la trascrizione
        service: Istanza del servizio WhisperService
        
    Returns:
        JSON con l'ID del job di trascrizione
    """
    # Controllo se il file è un file audio
    if not audio_file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Il file caricato non è un file audio")
    
    try:
        # Lettura del contenuto del file
        content = await audio_file.read()
        
        # Creazione di un ID univoco per il job
        job_id = str(uuid.uuid4())
        
        # Registrazione del job nel dizionario
        transcription_jobs[job_id] = {
            "status": "processing",
            "result": None,
            "error": None,
            "created_at": time.time()
        }
        
        # Avvio del processo di trascrizione in background
        background_tasks.add_task(
            process_transcription, 
            job_id, 
            content, 
            audio_file.filename, 
            language, 
            service
        )
        
        # Restituzione dell'ID del job al client
        return {"job_id": job_id, "status": "processing"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore durante l'elaborazione della richiesta: {str(e)}")

@app.get("/transcribe/status/{job_id}")
async def get_transcription_status(job_id: str):
    """
    Endpoint per controllare lo stato di un job di trascrizione
    
    Args:
        job_id: ID del job di trascrizione
        
    Returns:
        JSON con lo stato e il risultato (se disponibile) del job
    """
    # Controllo se il job esiste
    if job_id not in transcription_jobs:
        raise HTTPException(status_code=404, detail="Job di trascrizione non trovato")
    
    job = transcription_jobs[job_id]
    
    # Pulizia dei job vecchi (opzionale, potrebbe essere fatto in un task periodico)
    current_time = time.time()
    expired_jobs = [jid for jid, j in transcription_jobs.items() 
                    if j["status"] in ["completed", "error"] and 
                    current_time - j["created_at"] > 3600]  # 1 ora di retention
    
    for expired_job in expired_jobs:
        if expired_job != job_id:  # Non cancellare il job corrente
            transcription_jobs.pop(expired_job, None)
    
    # Costruzione della risposta
    response = {
        "job_id": job_id,
        "status": job["status"]
    }
    
    if job["status"] == "completed":
        response["transcription"] = job["result"]
    elif job["status"] == "error":
        response["error"] = job["error"]
    
    return response