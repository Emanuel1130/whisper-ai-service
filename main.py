import uvicorn
from api import app

if __name__ == "__main__":
    print("Avvio del servizio Whisper AI...")
    print("Accedi all'interfaccia tramite: http://localhost:8000")
    print("Per terminare, premi CTRL+C")
    uvicorn.run(app, host="0.0.0.0", port=8000) 