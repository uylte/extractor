
import os
from dotenv import load_dotenv
import instructor
import yaml
from model_architecture.control_flow_patterns import ControlFlowClassification
from groq import Groq
from langfuse.openai import OpenAI
from langfuse.decorators import observe, langfuse_context


class LLMClient:

    def __init__(self, config_path, prompts_path):

        # Lade Umgebungsvariablen (z. B. für den API-Schlüssel)
        load_dotenv()

        # API-Schlüssel aus der Umgebungsvariable laden
        self.api_key_openai = os.getenv("OPENAI_API_KEY")
        self.api_key_groq = os.getenv("GROQ_API_KEY")
        if not self.api_key_openai and not self.api_key_groq:
            raise ValueError("API Key not found in environment variables.")
        """
        self.openai_client = OpenAI(api_key=self.api_key_openai) if self.api_key_openai else None
        self.groq_client = OpenAI(
            base_url = "https://api.groq.com/openai/v1",
            api_key=self.api_key_groq) if self.api_key_groq else None
        """
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

        #self.client = OpenAI(api_key=self.api_key)
        self.openai_client = instructor.from_openai(OpenAI())
        self.groq_client = instructor.from_groq(Groq())

    @observe(as_type="generation")    
    def classify_description(self, system_prompt: str, full_prompt: str, client_type: str, model_key: str, session_id: str) -> ControlFlowClassification:
    # Modelleinstellungen laden
        model_config = self.config["models"].get(model_key)
        if not model_config:
            raise ValueError(f"Model configuration for '{model_key}' not found.")
        
        # Clients als Dictionary für leichtere Erweiterbarkeit
        clients = {
            "openai": self.openai_client,
            "groq": self.groq_client
        }
        
        messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt},
        ]

        # Passenden Client auswählen
        client = clients.get(client_type)
        if not client:
            raise ValueError(f"Unsupported client type: '{client_type}'.")

        # API-Anfrage ausführen
        response = client.chat.completions.create(
            model=model_config["name"],
            response_model=ControlFlowClassification,
            temperature=model_config["temperature"],
            max_tokens=model_config["max_tokens"],
            max_retries=3,
            messages=messages
        )
        langfuse_context.update_current_observation(
            session_id=session_id,
            input=messages,
            usage={
                "prompt_tokens": int,
                "completion_tokens": int,
                "total_tokens": int,
            },
            model=model_config["name"],
            metadata={"response_format": ControlFlowClassification.model_json_schema(), "client_type": client_type},
            output=response

        )

        return response