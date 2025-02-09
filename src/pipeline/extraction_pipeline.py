import json
import os
from helpers.prompt_loader import PromptLoader # Lädt die Prompts für das LLM
from model_architecture.llm_client import LLMClient # Verwaltet die Kommunikation mit dem LLM
from langfuse.decorators import observe, langfuse_context # Dekoratoren zur Überwachung und Protokollierung

class ExtractionPipeline:

    """
    Diese Klasse steuert den Workflow zur Extraktion von Kontrollflussmustern 
    aus Prozessbeschreibungen unter Verwendung eines LLMs.
    """

    def __init__(self, llm_client: LLMClient, prompt_loader: PromptLoader, json_data_path):
        """
        Initialisiert die Extraktionspipeline.

        :param llm_client: Instanz des LLMClients zur Kommunikation mit dem Sprachmodell.
        :param prompt_loader: Instanz des PromptLoaders zur Verwaltung der Prompts.
        :param json_data_path: Pfad zur JSON-Datei mit den Kontrollflussmustern.
        """


        self.prompt_loader = prompt_loader # Lädt die passenden Prompts für die Extraktion
        self.llm_client = llm_client # Schnittstelle zur Kommunikation mit dem LLM
        self.json_data_path = json_data_path # Speicherort der JSON-Daten

        
        if not os.path.exists(self.json_data_path):
            raise FileNotFoundError(f"JSON data file not found: {self.json_data_path}")
    
    def load_patterns(self):
        """
        Lädt Kontrollflussmuster aus der JSON-Datei.

        :return: Liste von Mustern aus der JSON-Datei.
        :raises KeyError: Falls der Schlüssel 'patterns' in der Datei fehlt.
        """

        # Öffnen und Laden der JSON-Datei
        with open(self.json_data_path, 'r') as file:
            data = json.load(file)

        # Sicherstellen, dass der Schlüssel 'patterns' existiert
        if "patterns" not in data:
            raise KeyError("Key 'patterns' not found in JSON data.")
        return data["patterns"]

    @observe()
    def extract_patterns(self, description: str, client_type: str, model_key: str, prompt_mode: str, session_id: str):
        """
        Extrahiert Kontrollflussmuster aus einer gegebenen Prozessbeschreibung mithilfe eines LLMs.

        :param description: Die textuelle Beschreibung des Geschäftsprozesses.
        :param client_type: Der LLM-Client-Typ (z. B. "openai" oder "groq").
        :param model_key: Schlüssel des zu verwendenden Modells (z. B. "gpt_4o").
        :param prompt_mode: Der Modus des Prompts (z. B. "zero_shot", "few_shot").
        :param session_id: ID der aktuellen Sitzung zur Nachverfolgung.
        :return: Klassifizierte Kontrollflussmuster.
        """
        
        # System-Prompt aus der Konfigurationsdatei laden
        system_prompt = self.prompt_loader.get_system_message()

        # Generiere den vollständigen Prompt basierend auf dem gewählten Prompt-Modus
        prompt = self.prompt_loader.generate_prompt(mode=prompt_mode, description=description)

        # Klassifizierung der Kontrollflussmuster mithilfe des LLMs
        return self.llm_client.classify_description(system_prompt=system_prompt, full_prompt=prompt, client_type=client_type, model_key=model_key, session_id=session_id, prompt_mode=prompt_mode)