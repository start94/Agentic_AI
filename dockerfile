# Usa un'immagine base di Python. Python 3.10 è una scelta comune e stabile.
FROM python:3.10-slim-buster

# Imposta la directory di lavoro all'interno del container. Tutte le operazioni successive avverranno qui.
WORKDIR /app

# Copia il file requirements.txt nella directory di lavoro del container.
# Questo permette a Docker di mettere in cache questo passo se il file non cambia.
COPY requirements.txt .

# Installa le dipendenze Python specificate nel requirements.txt.
# L'opzione --no-cache-dir riduce la dimensione dell'immagine finale.
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutti gli altri file del progetto nella directory di lavoro del container.
# Questo dovrebbe essere fatto dopo l'installazione delle dipendenze per ottimizzare la cache di Docker.
COPY . .

# Espone la porta se la tua applicazione avesse un server web (non è il tuo caso diretto, ma buona pratica se evolvi).
# EXPOSE 8000 

# Comando per avviare l'applicazione quando il container viene eseguito.
# Utilizziamo 'python -u' per evitare il buffering dell'output, così i log appaiono immediatamente.
CMD ["python", "-u", "main.py"]