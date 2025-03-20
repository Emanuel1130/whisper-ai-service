# Whisper AI Microservizio

Un microservizio basato su FastAPI che utilizza Whisper AI per trascrivere file audio.

## Struttura del Progetto

- `api.py`: Gestisce le rotte HTTP, la sicurezza e la configurazione CORS
- `whisper_service.py`: Contiene la logica di trascrizione audio

## Requisiti

- Python 3.8+
- FastAPI
- Whisper
- Uvicorn

## Installazione

1. Clona questo repository
2. Crea un ambiente virtuale:
   ```bash
   python -m venv venv
   ```
3. Attiva l'ambiente virtuale:
   - Windows: `venv\Scripts\activate` (CMD) o `source venv/Scripts/activate` (Git Bash)
   - Linux/Mac: `source venv/bin/activate`
4. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

## Utilizzo

### Avvio del servizio

```bash
python api.py
```

Il servizio sarà disponibile all'indirizzo `http://localhost:8000`.

### Endpoint disponibili

#### POST /transcribe/

Questo endpoint accetta un file audio e lo trascrive in testo.

**Parametri**:
- `audio_file`: Il file audio da trascrivere (obbligatorio)
- `language`: La lingua dell'audio (opzionale). Se non specificata, Whisper tenterà di rilevarla automaticamente.

**Esempio di utilizzo con curl**:

```bash
curl -X POST "http://localhost:8000/transcribe/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "audio_file=@percorso/al/tuo/file_audio.mp3" \
  -F "language=it"
```

**Esempio di risposta**:

```json
{
  "transcription": "Testo trascritto dal file audio."
}
```

## Configurazione CORS

Il servizio è configurato per accettare richieste solo dai seguenti domini:
- `https://www.wraiter.it`
- `http://localhost:4200`

## Test Locale

Per testare il servizio localmente, puoi:

1. Usare l'interfaccia Swagger UI: http://localhost:8000/docs
2. Aprire il file `test_client.html` in un browser
3. Usare strumenti come curl o Postman

## Accessibilità da Internet

Per rendere il servizio accessibile da una web app online, è possibile utilizzare:

1. **Ngrok**: 
   ```bash
   ngrok http 8000
   ```

2. **Cloudflare Tunnel**:
   ```bash
   cloudflared tunnel --url http://localhost:8000
   ```

3. **Port Forwarding sul Router**

## Modelli Disponibili

Il servizio può utilizzare diversi modelli di Whisper:
- `tiny`: ~39M parametri (molto veloce, meno accurato)
- `base`: ~74M parametri (buon compromesso)
- `small`: ~244M parametri
- `medium`: ~769M parametri
- `large`: ~1.5B parametri (molto accurato, più lento)

Per cambiare il modello, modifica il valore di `MODEL_SIZE` in `api.py`. 