import os
from dotenv import load_dotenv # Lädt Umgebungsvariablen aus einer .env-Datei
import instructor
import yaml 
from model_architecture.control_flow_patterns import ControlFlowClassification
from groq import Groq # Groq-API für LLM-Interaktion
from langfuse.openai import OpenAI # OpenAI-Client für Sprachmodellaufrufe
from langfuse.decorators import observe, langfuse_context # Observability und Logging


class LLMClient:
    """
    Verwaltet die Interaktion mit Large Language Models (LLMs), indem Modellkonfigurationen
    geladen und API-Anfragen an OpenAI oder Groq gesendet werden.
    """

    def __init__(self, config_path, prompts_path):

        """
        Initialisiert den LLM-Client:
        - Lädt Umgebungsvariablen für API-Keys
        - Liest Modell- und Prompt-Konfigurationen aus JSON/YAML-Dateien
        - Initialisiert OpenAI- und Groq-Clients

        :param config_path: Pfad zur Modellkonfigurationsdatei (JSON)
        :param prompts_path: Pfad zur Promptkonfigurationsdatei (YAML)
        """

        # Lade Umgebungsvariablen, um API-Schlüssel bereitzustellen
        load_dotenv()

        # Lese API-Schlüssel für OpenAI und Groq aus den Umgebungsvariablen
        self.api_key_openai = os.getenv("OPENAI_API_KEY")
        self.api_key_groq = os.getenv("GROQ_API_KEY")

        # Falls kein API-Schlüssel gefunden wird, Fehler auslösen
        if not self.api_key_openai and not self.api_key_groq:
            raise ValueError("API Key not found in environment variables.")

        # Falls keine Pfade übergeben wurden, Standardpfade setzen
        base_dir = os.path.dirname(os.path.abspath(__file__))
        if config_path is None:
            config_path = os.path.join(base_dir, '..', '..', 'config', 'models_config.json')
        if prompts_path is None:
            prompts_path = os.path.join(base_dir, '..', '..', 'config', 'prompts_config.yaml')

        # Konfigurationsdateien für Modelle und Prompts einlesen
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file) # Lade die Modellkonfigurationen

        with open(prompts_path, 'r') as file:
            self.prompts_config = yaml.safe_load(file) # Lade die Promptkonfigurationen

        # Initialisiere OpenAI- und Groq-Clients über die Instructor-Bibliothek
        self.openai_client = instructor.from_openai(OpenAI())
        self.groq_client = instructor.from_groq(Groq())

    @observe(as_type="generation")    
    def classify_description(self, system_prompt: str, full_prompt: str, client_type: str, model_key: str, session_id: str, prompt_mode: str) -> ControlFlowClassification:
        """
        Führt eine Klassifikation von Kontrollflussmustern basierend auf einem gegebenen Prompt durch.

        :param system_prompt: Systeminstruktion für das LLM (z. B. Rolle des Modells)
        :param full_prompt: Vollständige Nutzereingabe zur Klassifikation
        :param client_type: Auswahl des Clients ("openai" oder "groq")
        :param model_key: Schlüssel für das zu verwendende Modell in der Konfiguration
        :param session_id: Eindeutige Sitzungs-ID für Observability-Tracking
        :param prompt_mode: Art des Prompting (z. B. "Zero-Shot", "Few-Shot")
        :return: Ein `ControlFlowClassification`-Objekt mit den identifizierten Kontrollflussmustern
        """
    
        # Lade die Modellkonfiguration anhand des übergebenen model_key
        model_config = self.config["models"].get(model_key)
        if not model_config:
            raise ValueError(f"Model configuration for '{model_key}' not found.")
        
        # Definiere verfügbare Clients für LLM-Abfragen
        clients = {
            "openai": self.openai_client,
            "groq": self.groq_client
        }
        
        # Erstelle die Nachrichtenstruktur für das LLM:
        # - Die erste Nachricht beschreibt die Systemrolle (z. B. "Du bist ein Geschäftsprozess-Analyst") und Kontext.
        # - Die zweite Nachricht enthält die verschiedenen Prompting-Techniken und die Prozessbeschreibung.
        messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt},
        ]

        # Passenden Client auswählen
        client = clients.get(client_type)
        if not client:
            raise ValueError(f"Unsupported client type: '{client_type}'.")

         # Anfrage an das Sprachmodell senden und eine strukturierte Klassifikation zurückerhalten
        response = client.chat.completions.create(
            model=model_config["name"], # Modellname aus der Konfiguration
            response_model=ControlFlowClassification, # Definiertes Antwortschema für das LLM
            temperature=model_config["temperature"], # Kontrolliert die Zufälligkeit der Antwort
            max_tokens=model_config["max_tokens"], # Maximale Länge der Antwort
            max_retries=3, # Falls ein Fehler auftritt, maximal 3 erneute Versuche
            messages=messages # Übergabe der System- und Nutzereingaben
        )

        # Aktualisierung der Observability-Daten mit den verwendeten Parametern
        langfuse_context.update_current_observation(
            session_id=session_id,
            input=messages,
            usage={
                "prompt_tokens": int,
                "completion_tokens": int,
                "total_tokens": int,
            },
            model=model_config["name"],
            metadata={"response_format": ControlFlowClassification.model_json_schema(),
                      "client_type": client_type},
            output=response

        )

        return response # Gibt die klassifizierten Kontrollflussmuster zurück
