"""
import json
import os
from typing import Dict, List

def load_json(file_name: str) -> List[Dict]:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(current_dir, f"{file_name}")

    with open(input_path, 'r') as file:
        return json.load(file)
    
def process_and_save_data(input_file: str):
    #Lädt die JSON-Daten, verarbeitet sie und speichert sie in einer neuen Datei.
    try:
        data = load_json(input_file)
        result = {}

        for session in data:
            session_id = session['sessionId']
            latency = session.get('latency', None)
            usage = session.get('usage', {})
            input_cost = session.get('inputCost', None)
            output_cost = session.get('outputCost', None)
            total_cost = session.get('totalCost', None)

            for trace in session['output']:
                

                example = trace['example']
                if example not in result:
                    result[example] = []

                result[example].append({
                    "session_id": session_id,
                    "llm_key": trace['llm_key'],
                    "prompt_mode": trace['prompt_mode'],
                    "classification": trace['classification']['patterns'],
                    "latency": latency,
                    "usage": {
                        "promptTokens": usage.get('promptTokens', 0),
                        "completionTokens": usage.get('completionTokens', 0),
                        "totalTokens": usage.get('totalTokens', 0)
                    },
                    "costs": {
                        "input_cost": input_cost,
                        "output_cost": output_cost,
                        "total_cost": total_cost
                    }
                })
        
        # Ausgabe-Dateiname generieren
        input_file_name = os.path.basename(input_file).replace('.json', '')
        output_file = f"processed_{input_file_name}.json"

        # Ergebnis in eine Datei speichern
        with open(output_file, 'w') as file:
            json.dump(result, file, indent=4)

        print(f"Die verarbeiteten Daten wurden in {output_file} gespeichert.")

    except FileNotFoundError:
        print(f"Die Datei {input_file} wurde nicht gefunden.")
    except json.JSONDecodeError as e:
        print(f"Fehler beim Laden der JSON-Daten: {e}")
        """

"""
def transform_data():
    # Pfad des aktuellen Skripts
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Input- und Output-Pfade relativ zum Skript
    input_path = os.path.join(current_dir, "raw_eval_data.json")
    output_path = os.path.join(current_dir, "Structured_Traces_Form.json")

    # Dateien laden und speichern
    with open(input_path, "r") as file:
        data = json.load(file)
        
    structured_data = {}
    index = 0

    for record in data:
        if "output" in record:
            for output_entry in record["output"]:
                # Extrahiere und transformiere die Daten
                structured_data[index] = {
                    "example": output_entry.get("example", ""),
                    "llm_key": output_entry.get("llm_key", ""),
                    "prompt_mode": output_entry.get("prompt_mode", ""),
                    "classification": {
                        "patterns": {
                            i: pattern
                            for i, pattern in enumerate(output_entry.get("classification", {}).get("patterns", []))
                        }
                    }
                }
                index += 1
    
    with open(output_path, "w") as outfile:
        json.dump(structured_data, outfile, indent=4)

transform_data()
"""

"""
if __name__ == "__main__":
    # Pfad zur JSON-Datei
    json_file_path = "traces_sequence_session.json"  

    # JSON laden, verarbeiten und speichern
    process_and_save_data(json_file_path)
"""
import json
from collections import defaultdict
import os
from typing import Dict, List

def load_json(file_name: str) -> List[Dict]:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(current_dir, f"{file_name}")

    with open(input_path, 'r') as file:
        return json.load(file)

def group_traces_by_session(data):
    """Gruppiert die Traces nach sessionId und extrahiert relevante Informationen."""
    grouped_data = defaultdict(list)

    for trace in data:
        session_id = trace.get("sessionId", "unknown_session")
        grouped_data[session_id].append({
            "session_id": session_id,
            "input": trace.get("input", {}),
            "output": trace.get("output", {}),
            "metadata": trace.get("metadata", {}),
            "latency": trace.get("latency", 0),
            "inputTokens": trace.get("inputTokens", 0),
            "outputTokens": trace.get("outputTokens", 0),
            "totalTokens": trace.get("totalTokens", 0),
        })

    return grouped_data

def save_grouped_data(grouped_data, output_file):
    
    """Speichert die gruppierten Daten in einer JSON-Datei."""
    with open(output_file, 'w') as file:
        json.dump(grouped_data, file, indent=4)

    print(f"Die gruppierten Daten wurden in {output_file} gespeichert.")

def process_file(input_file, output_file):
    """Lädt die JSON-Daten, gruppiert sie nach sessionId und speichert sie."""
    try:
        data = load_json(input_file)
        grouped_data = group_traces_by_session(data)
        save_grouped_data(grouped_data, output_file)
    except FileNotFoundError:
        print(f"Die Datei {input_file} wurde nicht gefunden.")
    except json.JSONDecodeError as e:
        print(f"Fehler beim Dekodieren der JSON-Daten: {e}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(current_dir, f"traces_sequence_session.json")  # JSON-Datei mit den Traces
    output_file_path = os.path.join(current_dir, f"grouped_traces_by_session.json")  # Gruppierte Ausgabedatei

    input_path = os.path.join(current_dir, f"{input_file_path}")

    process_file(input_file_path, output_file_path)