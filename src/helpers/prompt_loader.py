import os
import yaml

class PromptLoader:
    """
    Eine Klasse zum Laden und Verwalten von Prompt-Konfigurationen aus einer YAML-Datei.
    """

    def __init__(self, config_path):
        """
        Initialisiert den PromptLoader und lädt die Konfigurationsdatei.

        :param config_path: Der Pfad zur YAML-Konfigurationsdatei mit den Prompts.
                           Falls `None`, wird ein Standardpfad verwendet.
        :raises FileNotFoundError: Falls die Datei nicht existiert.
        """

        # Falls kein Pfad angegeben ist, verwende den Standardpfad in `config/prompts_config.yaml`
        if config_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(base_dir, '..', '..', 'config', 'prompts_config.yaml')

        # Überprüfen, ob die Konfigurationsdatei existiert, ansonsten Fehler auslösen
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Prompts configuration file not found: {config_path}")

        # YAML-Datei öffnen und die Konfiguration laden
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
    
    def get_system_message(self) -> str:
        """
        Gibt die vordefinierte Systemnachricht zurück.

        :return: Die Systemnachricht aus der Konfiguration.
        :raises KeyError: Falls die entsprechende Konfiguration nicht existiert.
        """
        return self.config["prompts"]["system_message_2"]
    
    
    def generate_prompt(self, mode: str, description: str, **kwargs) -> str:
        """
        Erstellt einen formatierten Prompt basierend auf einem vorgegebenen Template.

        :param mode: Der Name des Prompt-Modus (z. B. "Zero-Shot", "Few-Shot").
        :param description: Die Beschreibung des zu klassifizierenden Prozesses.
        :param kwargs: Zusätzliche Schlüssel-Werte-Paare zur Platzhalterersetzung.
        :return: Der generierte Prompt als String.
        :raises ValueError: Falls der angegebene Prompt-Modus nicht existiert.
        """

        # Prüfen, ob der angegebene Modus in der Konfigurationsdatei existiert
        if mode not in self.config["prompts"]["templates"]:
            raise ValueError(f"Unsupported prompt mode: {mode}")
        
        # Prompt-Template abrufen
        template: str = self.config["prompts"]["templates"][mode]

        # Platzhalter im Template mit den übergebenen Werten ersetzen
        return template.format(description=description, **kwargs)