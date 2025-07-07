import os 
import datetime 
import json 
from crewai import Agent, Task, Crew, Process 
from langchain_openai import ChatOpenAI 
from dotenv import load_dotenv 
import speech_recognition as sr 
import datetime


"""
Configurazione iniziale per la modalità vocale.
Questo blocco try-except è fondamentale per gestire l'importazione opzionale del modulo `speech_recognition`.
Se il modulo è installato e disponibile nel sistema, 'VOICE_ENABLED' viene impostato su 'True',
permettendo all'applicazione di accettare input vocali.
Nel caso in cui 'speech_recognition' non sia installato (viene sollevato un ImportError),
VOICE_ENABLED rimane False, e l'applicazione funzionerà solo con input testuale.
Questa strategia rende il codice più robusto, evitando errori e crash se una dipendenza opzionale manca,
e fornisce un feedback chiaro all'utente sulla funzionalità disponibile.
"""
try:
    import speech_recognition as sr
    VOICE_ENABLED = True
except ImportError:
    VOICE_ENABLED = False

"""
Caricamento delle API key di OpenAI dal file .env.
La funzione load_dotenv() cerca un file chiamato '.env' nella stessa directory
e carica tutte le coppie chiave-valore presenti come variabili d'ambiente COME VISTO NELLE LEZIONI.
"""
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Devi impostare OPENAI_API_KEY nel file .env")

"""
Inizializzazione del modello LLM (Large Language Model) di OpenAI.
Viene configurata un'istanza di ChatOpenAI per interagire con i modelli di OpenAI.
- modelgpt-4o: Specifica l'uso del modello 'gpt-4o', noto per le sue capacità avanzate
  nel comprendere e generare linguaggio naturale, rendendolo ideale per compiti complessi.
- `temperature=0.3`: Questo parametro controlla la "creatività" o "casualità" delle risposte del modello.
  Un valore basso (come 0.3) rende le risposte più coerenti, prevedibili e focalizzate,
  il che è cruciale per un assistente finanziario dove la precisione e l'affidabilità sono prioritarie
  rispetto alla generazione di testo fantasioso o ambiguo.
- `openai_api_key=OPENAI_API_KEY`: Passa la chiave API caricata in precedenza per autenticare le richieste.
"""
openai_llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.3,
    openai_api_key=OPENAI_API_KEY
)


# transazioni simulate per testare l'assistente finanziario.
transazioni_reali = [
    {"data": "2025-06-24", "tipo": "Uscita", "categoria": "Cibo", "importo": 25},
    {"data": "2025-06-26", "tipo": "Uscita", "categoria": "Svago", "importo": 40},
    {"data": "2025-06-30", "tipo": "Uscita", "categoria": "Cibo", "importo": 30},
    {"data": "2025-07-01", "tipo": "Entrata", "categoria": "Stipendio", "importo": 1200},
    {"data": "2025-07-01", "tipo": "Uscita", "categoria": "Spesa", "importo": 15},
    {"data": "2025-07-02", "tipo": "Uscita", "categoria": "Trasporti", "importo": 10},
    {"data": "2025-07-03", "tipo": "Uscita", "categoria": "Bar", "importo": 5},
    {"data": "2025-07-03", "tipo": "Uscita", "categoria": "Ristorante", "importo": 20}
]


"""
Definizione degli Agenti  di CrewAI.
Ho scelto CrewAI per la sua capacità di orchestrare agenti AI.
Questa libreria permette di definire "agenti" con ruoli, obiettivi e background specifici,
che collaborano tra loro per risolvere problemi complessi, simulando un vero e proprio "equipaggio".
Ogni agente è equipaggiato con un modello LLM (`openai_llm`) per eseguire i propri compiti.
"""
nlp_agent = Agent(
    role="Analista NLP", # Ruolo: Specializzato nella comprensione del linguaggio.
    goal="Capire l'intento dell'utente e il periodo", # Obiettivo: Decifrare la richiesta dell'utente.
    backstory="Esperto linguista che interpreta richieste finanziarie", # Contesto che definisce la sua specializzazione.
    allow_delegation=True, # Può delegare sub-compiti ad altri, se necessario (se la pipeline fosse più complessa).
    verbose=True, # Abilita output dettagliati per seguire il suo processo decisionale.
    llm=openai_llm # Collega l'agente al modello LLM di OpenAI.
)

data_agent = Agent(
    role="Motore Dati", # Ruolo: Responsabile dell'elaborazione numerica.
    goal="Elaborare i dati delle transazioni", # Obiettivo: Eseguire calcoli sui dati finanziari.
    backstory="Analista che conosce ogni spesa", # Contesto che ne rafforza la competenza analitica.
    allow_delegation=False, # Non delega: esegue direttamente i calcoli precisi.
    verbose=True, # Abilita output dettagliati.
    llm=openai_llm # Collega l'agente al modello LLM.
)

response_agent = Agent(
    role="Assistente Utente", # Ruolo: Interfaccia finale con l'utente.
    goal="Fornire una risposta chiara e utile in italiano", # Obiettivo: Formulare la risposta.
    backstory="Esperto in comunicazione finanziaria", # Contesto che lo rende bravo a comunicare.
    allow_delegation=False, # Non delega la formulazione della risposta finale.
    verbose=True, # Abilita output dettagliati.
    llm=openai_llm # Collega l'agente al modello LLM.
)

"""
Le emoji come `💼`, `🎤`, `🎯`, `❌` 
sono state aggiunte per rendere l'interfaccia più simpatica e intuitiva. 
Non hanno una funzione logica nel codice, ma migliorano l'esperienza utente,
rendendo i messaggi più facili da comprendere e il programma più coinvolgente. Ad esempio,
`🎤 Parla ora` rende immediatamente chiaro che il sistema è in attesa di input vocale.
"""
# Input dinamico
def get_user_input():
    print("\n💼 Assistente finanziario multimodale")
    print("Scegli la modalità: [text] [voice] [exit]")
    while True: # Il ciclo 'while True' è fondamentale per permettere interazioni continue.
                # L'utente può fare più domande senza riavviare il programma.
        mode = input("👉 Modalità input: ").strip().lower()
        if mode == "text":
            return input("✏️ Inserisci la tua richiesta: ").strip()
        elif mode == "voice" and VOICE_ENABLED:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("🎤 Parla ora ")
                audio = r.listen(source)
            try:
                text = r.recognize_google(audio, language="it-IT")
                print(f"🎯 Richiesta ricevuta: {text}")
                return text
            except Exception as e:
                print("❌ Errore nel riconoscimento vocale:", e)
        elif mode == "voice" and not VOICE_ENABLED:
            print("❌ Modalità vocale non disponibile: modulo non installato.")
        elif mode == "exit": # L'opzione 'exit' permette all'utente di chiudere il programma in modo controllato.
            print("👋 Uscita dalla chat. A presto!")
            exit() # Termina l'esecuzione del programma.
        else:
            print("❌ Modalità non valida.")

"""
Funzione run_assistant(): Il cuore operativo e orchestrale dell'assistente.

Questa funzione è responsabile dell'intero flusso di lavoro:
 Ottiene l'input dall'utente (testuale o vocale) tramite `get_user_input()`.
Prepara il contesto temporale (`oggi`) per le successive elaborazioni.
Definisce la sequenza di compiti (Tasks) che gli agenti di CrewAI dovranno eseguire in modo collaborativo.
Avvia l'equipaggio (Crew) di agenti per processare la richiesta.
Gestisce la visualizzazione del risultato finale o di eventuali errori.

Ogni volta che 'run_assistant()' viene chiamata (grazie al ciclo 'while True' nel blocco principale),
si avvia un nuovo ciclo completo di interazione e elaborazione.
"""
def run_assistant():
    """
    Ottiene l'input dell'utente.
    Questa è la prima fase, dove il programma attende la richiesta dell'utente.
    La funzione `get_user_input()` gestisce l'interfaccia multimodale (testo/voce).
    """
    user_input = get_user_input()
    
    """
    Gestione di un input vuoto.
    Se `get_user_input()` restituisce un valore vuoto (ad esempio, l'utente non ha digitato nulla
    o il riconoscimento vocale non ha prodotto testo), il programma stampa un messaggio di errore
    e la funzione `run_assistant()` termina qui. Questo impedisce di avviare l'intera pipeline
    di CrewAI su una richiesta non valida o inesistente.
    """
    if not user_input:
        print("❌ Nessuna richiesta valida ricevuta.")
        return

    """
    Acquisizione della data corrente.
    `datetime.date.today()` recupera la data attuale del sistema.
    `.strftime("%Y-%m-%d")` la formatta come una stringa 'Anno-Mese-Giorno' (es. "2025-07-03").
    Questa data è fondamentale per dare un contesto temporale agli agenti,
    permettendo loro di interpretare correttamente richieste relative a periodi come "questa settimana",
    "ieri", "mese scorso", ecc., basandosi su un punto di riferimento reale.
    Rende l'assistente dinamico e non legato a date fisse.
    """
    oggi = datetime.date.today().strftime("%Y-%m-%d")

    """
    Definizione del Compito (Task) per l'Analista NLP (`nlp_agent`).
    Questo task è il primo anello della catena di elaborazione.
    - `description`: Istruisce l'NLP Agent su cosa deve fare: estrarre l'intento dell'utente
      (es. "spesa_totale") e il periodo di riferimento (es. "questa settimana") dalla richiesta originale.
      Specifica anche il formato JSON desiderato per l'output, guidando l'LLM.
    - `expected_output`: Indica il formato preciso in cui ci si aspetta la risposta del task.
    - `agent`: Assegna questo compito specifico all'`nlp_agent`, che è specializzato in questo tipo di analisi.
    """
    nlp_task = Task(
        description=f"Estrai intento e periodo da: '{user_input}'. Output JSON tipo: {{'intent': 'spesa_totale', 'periodo': 'questa settimana'}}",
        expected_output="JSON con 'intent' e 'periodo'",
        agent=nlp_agent
    )

    """
    Definizione del Compito (Task) per il Motore Dati (`data_agent`).
    Questo task prende in carico l'output strutturato dal `nlp_task` (l'intento e il periodo).
    description`: Fornisce al `data_agent` tutte le informazioni necessarie:
     La data odierna (`oggi`) per il contesto temporale.
    Una chiara definizione di "questa settimana" (da lunedì a oggi).
    L'indicazione di utilizzare i "Dati NLP" (l'output del task precedente).
     Il set di `transazioni_reali` su cui operare.
       La logica specifica per calcolare la spesa totale, filtrando per 'Uscita' e il periodo.
      È cruciale che questo task sia molto preciso per ottenere il calcolo corretto.
     `expected_output`: Richiede un numero float, essenziale per la successiva fase di generazione della risposta.
    -`agent`: Assegna questo compito al `data_agent`, l'esperto nell'elaborazione numerica.
    """
    data_task = Task(
        description=(
            f"Oggi è: {oggi}. Interpreta 'questa settimana' come l'intervallo da lunedì a oggi della settimana corrente.\n"
            f"Dati NLP: {{output NLP}}\n" # Questo placeholder verrà sostituito dal risultato del nlp_task.
            f"Transazioni disponibili:\n{json.dumps(transazioni_reali, indent=2)}\n"
            f"Se l'intento è 'spesa_totale', somma gli 'importo' delle transazioni con 'tipo': 'Uscita' nel periodo indicato.\n"
            f"Restituisci un numero float come 123.45"
        ),
        expected_output="Numero float tipo: 123.45",
        agent=data_agent
    )

    """
    Definizione del Compito (Task) per l'Assistente Utente (`response_agent`).
    Questo è il task finale della pipeline, focalizzato sulla presentazione del risultato.
    - `description`: Istruisce il `response_agent` a formulare una frase finale in italiano,
      usando l'intento originale e il valore numerico calcolato dal `data_agent`.
      L'esempio mostra il formato desiderato per la risposta all'utente.
    - `expected_output`: Una frase chiara e completa.
    - `agent`: Assegna il compito al `response_agent`, specializzato nella comunicazione.
    """
    response_task = Task(
        description="Genera una frase finale in italiano basata su intento e valore. Es: 'Hai speso 100 euro questa settimana.'",
        expected_output="Frase utente finale",
        agent=response_agent
    )

    """
    Creazione dell'Equipaggio (Crew) di Agenti.
    Un "Crew" è l'orchestratore di CrewAI. Raggruppa gli agenti e i loro compiti
    per lavorare insieme verso un obiettivo comune.
    - agents: Una lista di tutti gli agenti che parteciperanno al processo.
    - tasks: Una lista dei compiti da eseguire. L'ordine in cui sono definiti qui è cruciale
      quando il 'process' è 'sequential', poiché determina l'ordine di esecuzione.
    - process=Process.sequential`: Questo parametro indica che i compiti verranno eseguiti uno dopo l'altro.
      L'output di un task diventa automaticamente l'input per il task successivo, creando un flusso di lavoro lineare.
    - verbose=True: Abilita una modalità di output dettagliata durante l'esecuzione del crew.
      Questo è estremamente utile per il debug e per capire esattamente cosa sta facendo ogni agente
      e come i dati fluiscono tra i task.
    """
    crew = Crew(
        agents=[nlp_agent, data_agent, response_agent],
        tasks=[nlp_task, data_task, response_task],
        process=Process.sequential,
        verbose=True
    )

    print("\n🚀 Avvio del processo multi-agente...\n")
    """
    Avvio dell'esecuzione dell'equipaggio.
    Il metodo crew.kickoff() lancia l'intero processo di CrewAI.
    Gli agenti iniziano a collaborare, passando i risultati dei loro task come input
    per i compiti successivi, fino al completamento.
    Il blocco try-except è implementato per catturare qualsiasi eccezione o errore
    che possa verificarsi durante l'esecuzione del processo degli agenti,
    fornendo un feedback chiaro all'utente invece di un crash inaspettato.
    """
    try:
        result = crew.kickoff()
        print("\n✅ Risposta finale:")
        print(result) # Stampa il risultato finale generato dal response_agent.
    except Exception as e:
        print(f"\n❌ Errore durante l'esecuzione del processo: {e}")

"""
Ciclo continuo nel blocco principale del programma.
`if __name__ == "__main__": assicura che il codice all'interno di questo blocco
venga eseguito solo quando lo script viene avviato direttamente (non quando viene importato come modulo).
Il ciclo `while True` ha lo scopo cruciale di mantenere l'assistente in esecuzione continua.
Dopo che run_assistant() ha completato un'interazione, il ciclo si ripete,
chiedendo all'utente un nuovo input. Questo permette un'interazione fluida e multipla
senza dover riavviare il programma ogni volta, fino a quando l'utente non sceglie esplicitamente di "exit".
per quewsto progetto mi sarebbe piaciuto un file readme con spiegazione completa in modo da rendere il codice pulito.
"""
if __name__ == "__main__":
    while True:
        run_assistant()
        
        
"""         
Questo codice è stato sviluppato da Raffaele Diomaiuto, studente in AI DEVELOPMENT.
Il progetto è un assistente finanziario multimodale che utilizza CrewAI per orchestrare interazioni tra diversi agenti intelligenti."""