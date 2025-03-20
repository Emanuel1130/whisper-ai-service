@echo off
echo ==================================
echo = Whisper AI e Cloudflare Tunnel =
echo ==================================
echo.
echo AVVISO: Al primo avvio, il programma scarichera' automaticamente il modello Whisper.
echo Questo processo potrebbe richiedere alcuni minuti.
echo.
echo Saranno aperte DUE finestre:
echo  - Servizio Whisper AI (locale su http://localhost:8000)
echo  - Tunnel Cloudflare (pubblico su https://transcription.wraiter.it)
echo.
echo Puoi chiudere individualmente le finestre quando hai finito.
echo.
echo Avvio dei servizi in 3 secondi...
timeout /t 3 /nobreak > nul

REM Avvia il servizio Whisper AI in un nuovo processo
start "Whisper AI Service" cmd /c "cd /d "%~dp0dist" && echo Avvio del servizio Whisper AI... && whisper-ai-servce.exe && pause"

REM Avvia il tunnel Cloudflare in un altro processo
start "Cloudflare Tunnel" cmd /c "echo Avvio del tunnel Cloudflare... && cloudflared tunnel run Wraiter_Whisper && pause"

echo.
echo I servizi sono stati avviati in finestre separate.
echo Puoi chiudere questa finestra.
echo.
pause 