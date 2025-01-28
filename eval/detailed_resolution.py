import json
from collections import defaultdict

def calculate_averages(file_path, output_path):
    # Datenstruktur zum Speichern der aggregierten Werte
    results = defaultdict(lambda: defaultdict(lambda: {"precision_sum": 0, "recall_sum": 0, "latency_sum": 0, "count": 0}))

    # JSON-Daten laden
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Daten verarbeiten
    for entry in data:
        correct_pattern = entry.get("correct_pattern")
        llm_key = entry.get("llm_key")
        prompt_mode = entry.get("prompt_mode")
        precision = entry.get("precision", 0)
        recall = entry.get("recall", 0)
        latency = entry.get("latency", 0)

        # Aggregierte Werte berechnen
        key = (llm_key, prompt_mode)
        results[correct_pattern][key]["precision_sum"] += precision
        results[correct_pattern][key]["recall_sum"] += recall
        results[correct_pattern][key]["latency_sum"] += latency
        results[correct_pattern][key]["count"] += 1

    # Durchschnittswerte berechnen
    averages = defaultdict(dict)
    for correct_pattern, key_data in results.items():
        for (llm_key, prompt_mode), metrics in key_data.items():
            count = metrics["count"]
            averages[correct_pattern][f"{llm_key} | {prompt_mode}"] = {
                "average_precision": round(metrics["precision_sum"] / count, 4),
                "average_recall": round(metrics["recall_sum"] / count, 4),
                "average_latency": round(metrics["latency_sum"] / count, 5),
                "count": count,
            }

    # Ergebnis speichern
    with open(output_path, 'w') as outfile:
        json.dump(averages, outfile, indent=4)

    return output_path

def main():
    # Eingabe- und Ausgabepfade
    input_file_path = "eval/sorted_evaluation_results_new_prompts.json"  # Originale Eingabedatei
    output_file_path = "eval/eval_grouped_by_pattern_new_prompts.json"  # Datei für aggregierte Ergebnisse

    # Durchschnittswerte berechnen und speichern
    output_path = calculate_averages(input_file_path, output_file_path)
    print(f"Die aggregierten Ergebnisse wurden in der Datei '{output_path}' gespeichert.")

if __name__ == "__main__":
    main()
