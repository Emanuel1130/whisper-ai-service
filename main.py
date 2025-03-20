import uvicorn
import os
from api import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Avvio del servizio Whisper AI sulla porta {port}...")
    print("Accedi all'interfaccia tramite: http://localhost:8000")
    print("Per terminare, premi CTRL+C")
    uvicorn.run(app, host="0.0.0.0", port=port) 