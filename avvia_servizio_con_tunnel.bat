@echo off
echo ==================================
echo = Avvio Whisper AI con Tunnel    =
echo ==================================
echo.
echo AVVISO: Al primo avvio, il programma scarichera' automaticamente il modello Whisper.
echo Questo processo potrebbe richiedere alcuni minuti.
echo.
echo Per interrompere il servizio e il tunnel, premere CTRL+C o chiudere questa finestra.
echo.
echo Servizio disponibile su: https://transcription.wraiter.it
echo.

REM Crea una variabile per salvare la directory corrente
set "CURRENT_DIR=%cd%"

REM Avvia il servizio Whisper AI in un nuovo processo
start "Whisper AI Service" cmd /c "cd /d "%~dp0dist" && echo Avvio del servizio Whisper AI... && whisper-ai-servce.exe"

REM Attendi che il servizio sia inizializzato (5 secondi)
timeout /t 5 /nobreak

REM Avvia il tunnel Cloudflare
echo Avvio del tunnel Cloudflare...
cloudflared tunnel run Wraiter_Whisper

REM Se il tunnel si chiude (per errore o manualmente), termina anche il processo Whisper AI
taskkill /FI "WINDOWTITLE eq Whisper AI Service*" /F

REM Torna alla directory originale
cd /d "%CURRENT_DIR%"

echo.
echo Il servizio e il tunnel sono stati terminati.
echo.
pause 