import whisper
import tempfile
import os

class WhisperService:
    def __init__(self, model_size="base"):
        """
        Inizializza il servizio Whisper con il modello specificato.
        
        Args:
            model_size: Dimensione del modello Whisper ('tiny', 'base', 'small', 'medium', 'large')
        """
        self.model = whisper.load_model(model_size)
    
    async def transcribe(self, audio_content, filename, language=None):
        """
        Trascrive un file audio.
        
        Args:
            audio_content: Contenuto binario del file audio
            filename: Nome originale del file per ottenere l'estensione
            language: Lingua opzionale per la trascrizione
            
        Returns:
            Testo trascritto
        """
        temp_audio_path = None
        try:
            # Salvo temporaneamente il file audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_audio:
                temp_audio.write(audio_content)
                temp_audio_path = temp_audio.name
            
            # Opzioni di trascrizione
            options = {}
            if language:
                options["language"] = language
            
            # Trascrizione dell'audio
            result = self.model.transcribe(temp_audio_path, **options)
            
            return result["text"]
            
        finally:
            # Garantisco che il file venga eliminato in ogni caso
            if temp_audio_path and os.path.exists(temp_audio_path):
                try:
                    os.unlink(temp_audio_path)
                except:
                    pass 