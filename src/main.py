import os
from typing import List
import uuid
from model_architecture.llm_client import LLMClient
from helpers.prompt_loader import PromptLoader
from pipeline.extraction_pipeline import ExtractionPipeline
from langfuse.decorators import observe, langfuse_context

@observe
def main():

    # Basisverzeichnisse setzen
    base_dir = os.path.dirname(os.path.abspath(__file__))
    prompts_path = os.path.join(base_dir, '..', 'config', 'prompts_config.yaml')
    models_config_path = os.path.join(base_dir, '..', 'config', 'models_config.yaml')
    json_data_path = os.path.join(base_dir, 'data', 'patterns.json')

    llms = ["gpt_4o", "gpt_4o_mini"]
    prompt_modes = ["zero_shot", "few_shot", "chain_of_thought"]

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

    patterns = pipeline.load_patterns()

    results = []

    for pattern in patterns[:2]:
        pattern_name = pattern["name"]
        examples = pattern["examples"]

        session_id = f"{pattern_name}_session_{uuid.uuid4()}"

        langfuse_context.update_current_trace(
            session_id=session_id
            )

        # Über Prompt-Modi iterieren
        for prompt_mode in prompt_modes:

            # Über LLMs iterieren
            for llm_key in llms:
                for example in examples:

                    # Klassifikation durchführen
                    classification = pipeline.extract_patterns(
                    description=example,
                    model_key=llm_key,
                    prompt_mode=prompt_mode
                    )
                    results.append({
                    "pattern_name": pattern_name,
                    "example": example,
                    "llm_key": llm_key,
                    "prompt_mode": prompt_mode,
                    "classification": classification
                    })

                    print(f"Pattern: {pattern_name}")
                    print(f"Example: {example}")
                    print(f"Model: {llm_key}")
                    print(f"Prompt Mode: {prompt_mode}")
                    print(f"Classification: {classification.model_dump_json(indent=2)}")


"""
    # Ergebnisse ausgeben
    for result in results:
        print(f"Pattern: {result['pattern_name']}")
        print(f"Example: {result['example']}")
        print(f"Model: {result['llm_key']}")
        print(f"Prompt Mode: {result['prompt_mode']}")
        print(f"Classification: {result['classification'].model_dump_json(indent=2)}")
        print()
"""


if __name__ == "__main__":
    main()