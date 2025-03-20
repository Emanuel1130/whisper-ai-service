# Whisper AI con Cloudflare Tunnel

Questa guida spiega come avviare il servizio Whisper AI e renderlo accessibile da Internet utilizzando Cloudflare Tunnel.

## Prerequisiti

1. Assicurati di aver installato `cloudflared` 
2. Assicurati che il tunnel "Wraiter_Whisper" sia stato configurato su Cloudflare
3. Verifica che la configurazione DNS per `transcription.wraiter.it` sia attiva

## Opzioni disponibili

### 1. Avvio integrato (servizio e tunnel insieme)

Utilizza lo script `avvia_servizio_con_tunnel.bat` per avviare sia il servizio Whisper AI che il tunnel Cloudflare in un'unica finestra:

- Questo script avvia prima il servizio e poi il tunnel
- Chiudendo la finestra, entrambi i servizi vengono terminati
- Ideale per l'uso quotidiano

```
avvia_servizio_con_tunnel.bat
```

### 2. Avvio in finestre separate

Utilizza lo script `avvia_servizio_e_tunnel_parallelo.bat` per avviare il servizio e il tunnel in finestre separate:

- Vengono aperte due finestre separate (servizio locale e tunnel)
- Puoi chiudere le finestre individualmente
- Il servizio locale funzionerà anche se il tunnel viene chiuso
- Utile per debug o test

```
avvia_servizio_e_tunnel_parallelo.bat
```

### 3. Avvio manuale

Puoi anche avviare manualmente i due componenti:

1. Avvia il servizio Whisper AI:
```
dist\whisper-ai-servce.exe
```

2. In una finestra separata, avvia il tunnel Cloudflare:
```
cloudflared tunnel run Wraiter_Whisper
```

## Accesso al servizio

- **Accesso locale**: http://localhost:8000
- **Accesso remoto**: https://transcription.wraiter.it

## Risoluzione problemi

### Il tunnel non si connette

1. Verifica che il servizio Whisper AI sia in esecuzione sulla porta 8000
2. Controlla che `cloudflared` sia installato correttamente
3. Verifica che il tunnel sia configurato su Cloudflare
4. Prova a riavviare `cloudflared` manualmente

### Errori "Too Many Redirects"

Assicurati che l'impostazione SSL/TLS nella dashboard di Cloudflare sia impostata su "Full (Strict)".

### Errori CORS

Verifica che nel file `api.py` del servizio sia presente `"https://transcription.wraiter.it"` nell'elenco degli `allow_origins`. 