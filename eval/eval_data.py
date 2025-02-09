import json
from collections import defaultdict
import os
from matplotlib import pyplot as plt
import numpy as np

# Definiert den Projektstammordner, um relative Pfade zu den Daten zu ermöglichen
project_root = os.path.dirname(os.path.dirname(__file__))  # Wechselt zur Wurzel des Projekts "extractor"

# Definiert die Pfade zu den benötigten JSON-Dateien
pattern_file_path = os.path.join(project_root, "src", "data", "patterns.json")
data_file_path = os.path.join(project_root, "eval", "raw_data", "new_sysPrompt_all_traces.json")


# Laden der JSON-Daten aus den Dateien
with open(pattern_file_path, "r") as f:
    patterns_data = json.load(f)
with open(data_file_path, "r") as f:
    data = json.load(f)

# Erstellen eines Mappings von Muster-Namen zu ihren Beispielbeschreibungen
pattern_examples = {p["name"]: p["examples"] for p in patterns_data["patterns"]}

# Initialisierung von Datenstrukturen für die Evaluierung
evaluation_results = [] # Speichert einzelne Evaluierungsergebnisse
grouped_results = defaultdict(lambda: defaultdict(list))  # Gruppiert Ergebnisse nach LLM und Prompt Mode

# Durchlaufen der JSON-Daten zur Evaluierung
for i, entry in enumerate(data):
    # Extrahieren der relevanten Daten
    input_data = entry.get("input", {}) # Eingabedaten
    output_data = entry.get("output", {}) # Modellantworten
    metadata = entry.get("metadata", {}) # Metadaten zum Modellaufruf

    # Beschreibungstext des Beispiels aus den Eingabedaten
    example = input_data.get("description_text", "Kein Beschreibungstext gefunden")

    # Erkannte Kontrollflussmuster aus der Modellantwort
    patterns = output_data.get("patterns", [])

    # LLM- und Prompting-Informationen aus den Metadaten
    llm_key = metadata.get("model_key", "unknown LLM")
    prompt_mode = metadata.get("prompt_mode", "unknown prompt mode")

    # Sammeln der Reasoning Steps aller erkannten Muster
    full_reasoning_steps = []
    for pattern in patterns:
        reasoning_steps = pattern.get("reasoning_steps", [])
        full_reasoning_steps.append(reasoning_steps)

    # Latenzzeit des Modellaufrufs
    latency = entry.get("latency", None)

    # Identifizieren des korrekten Musters durch Vergleich mit gespeicherten Beispiele
    correct_pattern = None
    for pattern_name, examples in pattern_examples.items():
        if example in examples:
            correct_pattern = pattern_name
            break

    # Evaluierung der Mustererkennung
    recognized_patterns = [(p["pattern"], p["confidence"]) for p in patterns]

    # Berechnung von True Positives (TP) und False Positives (FP)
    true_positive = 1 if correct_pattern in [p[0] for p in recognized_patterns] else 0
    false_positives = len(recognized_patterns) - true_positive

    # Berechnung von Recall und Precision
    recall = 1 if true_positive > 0 else 0
    precision = true_positive / len(recognized_patterns) if recognized_patterns else 0
    
    # Speichern der Evaluierungsergebnisse
    result_entry = {
        "example": example,
        "correct_pattern": correct_pattern,
        "recognized_patterns": recognized_patterns,
        "true_positive": true_positive,
        "false_positives": false_positives,
        "precision": precision,
        "recall": recall,
        "llm_key": llm_key,
        "prompt_mode": prompt_mode,
        "total_recognized_patterns": len(recognized_patterns),
        "latency": latency,
        "reasoning_steps": full_reasoning_steps
    }
    evaluation_results.append(result_entry)

    # Ergebnisse nach LLM und Prompt Mode gruppieren
    grouped_results[llm_key][prompt_mode].append(result_entry)

# Berechnung der durchschnittlichen Evaluierungsmetriken pro LLM und Prompt Mode
llm_mode_metrics = {}
for llm_key, prompt_modes in grouped_results.items():
    llm_mode_metrics[llm_key] = {}
    for prompt_mode, entries in prompt_modes.items():
        total_entries = len(entries)
        avg_precision = sum(e["precision"] for e in entries) / total_entries if total_entries > 0 else 0
        avg_recall = sum(e["recall"] for e in entries) / total_entries if total_entries > 0 else 0
        avg_latency = sum(e["latency"] for e in entries if e["latency"] is not None) / total_entries if total_entries > 0 else 0
        total_recognized_patterns = sum(e["total_recognized_patterns"] for e in entries)

        # Speichern der berechneten Metriken
        llm_mode_metrics[llm_key][prompt_mode] = {
            "average_precision": avg_precision,
            "average_recall": avg_recall,
            "average_latency": avg_latency,
            "total_entries": total_entries,
            "total_recognized_patterns": total_recognized_patterns
        }

# Sortieren der Ergebnisse nach korrektem Muster, LLM und Prompt Mode
sorted_results = sorted(evaluation_results, key=lambda x: (x["correct_pattern"], x["llm_key"], x["prompt_mode"]))

# Speichern der sortierten Evaluationsergebnisse in JSON-Dateien
results_path = os.path.join(project_root, "eval", "results", "sorted_evaluation_new_sysPrompt_all_traces.json")
with open(results_path, 'w') as f:
    json.dump(sorted_results, f, indent=4)

metrics_path = os.path.join(project_root, "eval", "results", "llm_mode_metrics_new_sysPrompt_all_traces.json")
with open(metrics_path, 'w') as f:
    json.dump(llm_mode_metrics, f, indent=4)

# Ausgabe der durchschnittlichen Präzision, Recall und Latenz pro LLM und Prompt Mode
print("Präzision und Recall pro LLM und Prompt Mode:")
for llm, prompt_modes in llm_mode_metrics.items():
    print(f"\nLLM: {llm}")
    for prompt_mode, metrics in prompt_modes.items():
        print(f"  Prompt Mode: {prompt_mode}")
        print(f"    Durchschnittliche Präzision: {metrics['average_precision']:.2%}")
        print(f"    Durchschnittlicher Recall: {metrics['average_recall']:.2%}")
        print(f"    Durchschnittliche Latenz: {metrics['average_latency']}")
        print(f"    Gesamtanzahl: {metrics['total_entries']}")
        print(f"    Gesamt erkannte Muster: {metrics['total_recognized_patterns']}")


# Visualisierung von Präzision und Recall als Balkendiagramm
for llm, prompt_modes in llm_mode_metrics.items():
    modes = list(prompt_modes.keys())
    precisions = [prompt_modes[mode]["average_precision"] for mode in modes]
    recalls = [prompt_modes[mode]["average_recall"] for mode in modes]

    # Erstellen eines Balkendiagramms für Präzision und Recall pro Prompt Mode
    x = np.arange(len(modes))  # Positionen der Balken
    width = 0.35  # Breite der Balken

    plt.figure(figsize=(10, 6))
    plt.bar(x - width/2, precisions, width, label="Präzision", color="blue")
    plt.bar(x + width/2, recalls, width, label="Recall", color="orange")

    plt.title(f"Präzision und Recall pro Prompt Mode für LLM: {llm}")
    plt.xlabel("Prompt Mode")
    plt.ylabel("Wert")
    plt.ylim(0, 1)
    plt.xticks(x, modes, rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()
