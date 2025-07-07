# Agentic_AI
# Assistente Finanziario Multimodale

Questo progetto implementa un assistente finanziario multimodale (testo e voce) che utilizza CrewAI per orchestrare l'interazione tra diversi agenti intelligenti. L'assistente è in grado di interpretare le richieste dell'utente, elaborare dati transazionali e fornire risposte chiare.

## Caratteristiche

* **Multimodalità:** Input tramite testo o voce.
* **Architettura ad Agenti:** Utilizza CrewAI con agenti specializzati (Analista NLP, Motore Dati, Assistente Utente).
* **Elaborazione del Linguaggio Naturale (NLP):** Comprende l'intento e il contesto temporale delle richieste.
* **Analisi Dati Finanziari:** Calcola spese totali basandosi su transazioni simulate.
* **Risposte Chiare:** Genera risposte user-friendly in italiano.

## Installazione

1.  **Clona il repository:**
    ```bash
    git clone [https://github.com/tuo-utente/assistente-finanziario-multimodale.git](https://github.com/tuo-utente/assistente-finanziario-multimodale.git)
    cd assistente-finanziario-multimodale
    ```
    Sostituisci `tuo-utente` con il tuo username GitHub.

2.  **Crea un ambiente virtuale (consigliato):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Su Linux/macOS
    # venv\Scripts\activate   # Su Windows
    ```

3.  **Installa le dipendenze:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura la chiave API di OpenAI:**
    Crea un file `.env` nella directory principale del progetto e aggiungi la tua chiave API di OpenAI:
    ```
    OPENAI_API_KEY="la_tua_chiave_api_di_openai_qui"
    ```

## Utilizzo

Per avviare l'assistente, esegui il file `main.py`:
```bash
python main.py
