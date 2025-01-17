
import os
from dotenv import load_dotenv
import instructor
import yaml
from model_architecture.control_flow_patterns import ControlFlowClassification
from langfuse.openai import OpenAI
from langfuse.decorators import observe


class LLMClient:

    def __init__(self, config_path, prompts_path):

        # Lade Umgebungsvariablen (z. B. für den API-Schlüssel)
        load_dotenv()

        # API-Schlüssel aus der Umgebungsvariable laden
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API Key not found in environment variables.")

        # Setze Standardpfade, falls keine angegeben wurden
        base_dir = os.path.dirname(os.path.abspath(__file__))
        if config_path is None:
            config_path = os.path.join(base_dir, '..', '..', 'config', 'models_config.json')
        if prompts_path is None:
            prompts_path = os.path.join(base_dir, '..', '..', 'config', 'prompts_config.yaml')

        # Modelleinstellungen und Prompts laden
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        with open(prompts_path, 'r') as file:
            self.prompts_config = yaml.safe_load(file)

        self.client = OpenAI(api_key=self.api_key)
        self.client = instructor.from_openai(OpenAI())

    #@observe()    
    def classify_description(self, system_prompt: str, full_prompt: str, model_key: str) -> ControlFlowClassification:

        model_config = self.config["models"].get(model_key)
        if not model_config:
            raise ValueError(f"Model configuration for '{model_key}' not found.")
        
        #system_message = self.prompts_config["prompts"]["system_message"]

        response = self.client.chat.completions.create(
            model=model_config["name"],
            response_model=ControlFlowClassification,
            temperature=model_config["temperature"],
            max_tokens=model_config["max_tokens"],
            max_retries=3,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt},
            ]
        )
            
        return response