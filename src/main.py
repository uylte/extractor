import json
import os
from typing import List
import uuid
from model_architecture.llm_client import LLMClient # LLM-Client für die Kommunikation mit Sprachmodellen
from helpers.prompt_loader import PromptLoader # Lädt und verwaltet Prompts für das LLM
from pipeline.extraction_pipeline import ExtractionPipeline # Pipeline zur Musterextraktion
from langfuse.decorators import observe, langfuse_context # Tools zur Protokollierung und Analyse

@observe(name="extraction")
def main(description_text, client_type, llm_key, prompt_mode, session_id, pipeline: ExtractionPipeline):
    """
    Führt die Extraktion von Kontrollflussmustern aus einer Geschäftsprozessbeschreibung durch.

    :param description_text: Die zu analysierende Prozessbeschreibung.
    :param client_type: Typ des LLM-Clients (z. B. "openai" oder "groq").
    :param llm_key: Identifikator des verwendeten Sprachmodells (z. B. "gpt_4o").
    :param prompt_mode: Verwendeter Prompting-Modus (z. B. "zero_shot", "few_shot").
    :param session_id: Eindeutige Sitzungs-ID zur Nachverfolgung.
    :param pipeline: Instanz der ExtractionPipeline zur Verarbeitung der Eingabe.
    """

    # Durchführung der Musterklassifikation durch das LLM
    classification = pipeline.extract_patterns(
        description=description_text,
        client_type=client_type,
        model_key=llm_key,
        prompt_mode=prompt_mode,
        session_id=session_id
    )

    # Aktualisierung des Langfuse-Kontexts zur Analyse der Verarbeitung
    langfuse_context.update_current_trace(
        session_id=session_id,
        input={"description_text": description_text},
        output=classification,
        metadata={"client_type": client_type, "model_key": llm_key, "prompt_mode": prompt_mode},
    )

    # Ergebnisse speichern und ausgeben
    results = []
    results.append({
        "example": description_text,
        "llm_key": llm_key,
        "prompt_mode": prompt_mode,
        "classification": classification
        })
    
    # Ausgabe der Klassifikationsergebnisse im JSON-Format
    for result in results:
        print(f"Example: {result['example']}")
        print(f"Model: {result['llm_key']}")
        print(f"Prompt Mode: {result['prompt_mode']}")
        print(f"Classification: {json.dumps(result['classification'], indent=2) if isinstance(result['classification'], dict) else result['classification']}")
        print()

def process_iterations(patterns, client_types, llms_by_client, prompt_modes, pipeline):
    """
    Führt die Extraktion iterativ für verschiedene Prozessmuster, Modelle und Prompting-Methoden durch.

    :param patterns: Liste der zu analysierenden Kontrollflussmuster.
    :param client_types: Liste der verwendeten LLM-Anbieter (z. B. "openai", "groq").
    :param llms_by_client: Dictionary mit den zugehörigen Modellnamen pro Client.
    :param prompt_modes: Liste der zu testenden Prompting-Modi.
    :param pipeline: Instanz der ExtractionPipeline zur Steuerung der Verarbeitung.
    """
        
    # Verarbeitung einer Teilmenge der Muster (hier nur 7 Muster)    
    for pattern in patterns[7]:
        pattern_name = pattern["name"]
        examples = pattern["examples"]

        # Generierung einer eindeutigen Sitzungs-ID für das aktuelle Muster
        session_id = f"{pattern_name}_session_{uuid.uuid4()}"

        # Iteration über alle LLM-Clients und deren Modelle
        for client_type in client_types:
            client_llms = llms_by_client.get(client_type, [])

            for llm_key in client_llms:
                for prompt_mode in prompt_modes:
                    for example in examples:
                        # Hauptfunktion zur Extraktion aufrufen
                        main(
                            description_text=example,
                            client_type=client_type,
                            llm_key=llm_key,
                            prompt_mode=prompt_mode,
                            session_id=session_id,
                            pipeline=pipeline
                        )


if __name__ == "__main__":
    """
    Initialisiert alle benötigten Komponenten und führt die Verarbeitung durch.
    """

    # Basisverzeichnis ermitteln
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Dateipfade für Konfigurationsdateien setzen
    prompts_path = os.path.join(base_dir, '..', 'config', 'prompts_config.yaml')
    models_config_path = os.path.join(base_dir, '..', 'config', 'models_config.yaml')
    json_data_path = os.path.join(base_dir, 'data', 'patterns.json')

    # Initialisierung des PromptLoaders zur Verwaltung der Eingabeaufforderungen
    prompt_loader = PromptLoader(prompts_path)

    # Initialisierung des LLMClients zur Kommunikation mit den Sprachmodellen
    llm_client = LLMClient(models_config_path, prompts_path)

    # Erstellung der Extraktionspipeline mit den geladenen Komponenten
    pipeline = ExtractionPipeline(
        llm_client=llm_client,
        prompt_loader=prompt_loader,
        json_data_path=json_data_path
    )

    # Laden der Prozessmuster mit Beispielen aus der JSON-Datei
    patterns = pipeline.load_patterns()

    # Definierte LLM-Clients und zugehörige Modelle
    client_types = ["openai", "groq"]
    llms_by_client = {
        "openai": ["gpt_4o", "gpt_4o_mini"],
        "groq": ["llama-3.3-70b-versatile"]
        
    }
    # Verwendete Prompting-Modi
    prompt_modes = ["zero_shot", "few_shot", "zero_shot_cot", "few_shot_cot"]

    # Start der iterativen Verarbeitung mit den geladenen Mustern
    process_iterations(
        patterns=patterns,
        client_types=client_types,
        llms_by_client=llms_by_client,
        prompt_modes=prompt_modes,
        pipeline=pipeline
    )
