import os
import yaml

class PromptLoader:
    def __init__(self, config_path):
        if config_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(base_dir, '..', '..', 'config', 'prompts_config.yaml')

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Prompts configuration file not found: {config_path}")

        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
    
    def get_system_message(self) -> str:
        return self.config["prompts"]["system_message"]
    
    def generate_prompt(self, mode: str, description: str, **kwargs) -> str:
        if mode not in self.config["prompts"]["templates"]:
            raise ValueError(f"Unsupported prompt mode: {mode}")
        
        template: str = self.config["prompts"]["templates"][mode]
        return template.format(description=description, **kwargs)