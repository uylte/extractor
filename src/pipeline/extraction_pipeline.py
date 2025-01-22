import json
import os
from helpers.prompt_loader import PromptLoader
from model_architecture.llm_client import LLMClient
from langfuse.decorators import observe, langfuse_context

class ExtractionPipeline:
    def __init__(self, llm_client: LLMClient, prompt_loader: PromptLoader, json_data_path):

        self.prompt_loader = prompt_loader
        self.llm_client = llm_client
        self.json_data_path = json_data_path
        
        if not os.path.exists(self.json_data_path):
            raise FileNotFoundError(f"JSON data file not found: {self.json_data_path}")
    
    def load_patterns(self):
        with open(self.json_data_path, 'r') as file:
            data = json.load(file)

        if "patterns" not in data:
            raise KeyError("Key 'patterns' not found in JSON data.")
        return data["patterns"]

    @observe()
    def extract_patterns(self, description: str, client_type: str, model_key: str, prompt_mode: str, session_id: str):
        """
        Extrahiert Kontrollflussmuster aus einer Prozessbeschreibung.
        :param description: Die Prozessbeschreibung.
        :param model_key: Schlüssel des zu verwendenden Modells (z. B. "gpt_4o").
        :param prompt_mode: Der Modus des Prompts (z. B. "zero_shot", "few_shot").
        :return: Klassifizierte Kontrollflussmuster.
        """
        
        # Generiere den Prompt basierend auf der Beschreibung und dem Modus
        system_prompt = self.prompt_loader.get_system_message()
        prompt = self.prompt_loader.generate_prompt(mode=prompt_mode, description=description)
        return self.llm_client.classify_description(system_prompt=system_prompt, full_prompt=prompt, client_type=client_type, model_key=model_key, session_id=session_id)