import json
import os
from typing import List
import uuid
from model_architecture.llm_client import LLMClient
from helpers.prompt_loader import PromptLoader
from pipeline.extraction_pipeline import ExtractionPipeline
from langfuse.decorators import observe, langfuse_context

@observe(name="extraction")
def main(description_text, client_type, llm_key, prompt_mode, session_id, pipeline: ExtractionPipeline):

    # Klassifikation durchführen
    classification = pipeline.extract_patterns(
        description=description_text,
        client_type=client_type,
        model_key=llm_key,
        prompt_mode=prompt_mode,
        session_id=session_id
    )

    # Langfuse-Kontext aktualisieren
    langfuse_context.update_current_trace(
        session_id=session_id,
        input={"description_text": description_text},
        output=classification,
        metadata={"client_type": client_type, "model_key": llm_key, "prompt_mode": prompt_mode},
    )
    results = []
    results.append({
        "example": description_text,
        "llm_key": llm_key,
        "prompt_mode": prompt_mode,
        "classification": classification
        })
    for result in results:
        print(f"Example: {result['example']}")
        print(f"Model: {result['llm_key']}")
        print(f"Prompt Mode: {result['prompt_mode']}")
        print(f"Classification: {json.dumps(result['classification'], indent=2) if isinstance(result['classification'], dict) else result['classification']}")
        print()

def process_iterations(patterns, client_types, llms_by_client, prompt_modes, pipeline):
    for pattern in patterns[:5]:
        pattern_name = pattern["name"]
        examples = pattern["examples"]

        # Neue Session pro Pattern
        session_id = f"{pattern_name}_session_{uuid.uuid4()}"

        for client_type in client_types:
            client_llms = llms_by_client.get(client_type, [])

            for llm_key in client_llms:
                for prompt_mode in prompt_modes:
                    for example in examples:
                        main(
                            description_text=example,
                            client_type=client_type,
                            llm_key=llm_key,
                            prompt_mode=prompt_mode,
                            session_id=session_id,
                            pipeline=pipeline
                        )


if __name__ == "__main__":
    # Basisverzeichnisse setzen
    base_dir = os.path.dirname(os.path.abspath(__file__))
    prompts_path = os.path.join(base_dir, '..', 'config', 'prompts_config.yaml')
    models_config_path = os.path.join(base_dir, '..', 'config', 'models_config.yaml')
    json_data_path = os.path.join(base_dir, 'data', 'patterns.json')

    # PromptLoader initialisieren
    prompt_loader = PromptLoader(prompts_path)

    # LLMClient initialisieren
    llm_client = LLMClient(models_config_path, prompts_path)

    # ExtractionPipeline initialisieren
    pipeline = ExtractionPipeline(
        llm_client=llm_client,
        prompt_loader=prompt_loader,
        json_data_path=json_data_path
    )

    # Muster laden
    patterns = pipeline.load_patterns()

    # Client-Typen und Modelle
    client_types = ["openai", "groq"]
    llms_by_client = {
        "openai": ["gpt_4o", "gpt_4o_mini"],
        "groq": ["llama-3.3-70b-versatile"]
        #"groq": ["mixtral-8x7b-32768"]
    }
    prompt_modes = ["zero_shot_2", "few_shot_2", "chain_of_thought_2"]

    # Iteration durchführen
    process_iterations(
        patterns=patterns,
        client_types=client_types,
        llms_by_client=llms_by_client,
        prompt_modes=prompt_modes,
        pipeline=pipeline
    )
