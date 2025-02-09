import json
from collections import defaultdict

"""
Dieses Skript berechnet die durchschnittlichen Precision-, Recall- und Latenzwerte für 
verschiedene LLMs und Prompting-Techniken, gruppiert nach den erkannten Kontrollflussmustern.

### Gruppierung und Verarbeitung:
1. **Eingabeformat (JSON)**: Die Datei enthält eine Liste von Evaluierungsergebnissen, wobei 
   jedes Element folgende Felder enthält:
   - `correct_pattern`: Das richtige Kontrollflussmuster für die gegebene Prozessbeschreibung.
   - `llm_key`: Das verwendete Sprachmodell (z. B. "gpt_4o").
   - `prompt_mode`: Der angewendete Prompting-Modus (z. B. "few_shot").
   - `precision`, `recall`, `latency`: Die Metriken für das jeweilige Modell und die Anfrage.
2. **Gruppierung der Werte**:
   - Die Ergebnisse werden nach `correct_pattern` (richtiges Muster) gruppiert.
   - Innerhalb jedes Musters wird nach `(llm_key, prompt_mode)` weiter unterteilt.
   - Die Precision-, Recall- und Latenzwerte werden für jede Gruppe aufaddiert.
3. **Berechnung der Durchschnittswerte**:
   - Die aufsummierten Werte werden durch die Anzahl der Einträge geteilt, um Mittelwerte zu erhalten.
4. **Speicherung der aggregierten Daten**:
   - Die berechneten Durchschnittswerte werden in einer neuen JSON-Datei gespeichert.

"""

def calculate_averages(file_path, output_path):
    """
    Berechnet die durchschnittlichen Precision-, Recall- und Latenzwerte für jede Kombination aus 
    Kontrollflussmuster, LLM und Prompting-Technik.

    :param file_path: Pfad zur Eingabedatei mit den Evaluierungsergebnissen.
    :param output_path: Pfad zur Datei, in der die aggregierten Ergebnisse gespeichert werden.
    :return: Der Pfad der gespeicherten Datei mit den Durchschnittswerten.
    """
        
    # Datenstruktur zum Speichern der aggregierten Werte
    results = defaultdict(lambda: defaultdict(lambda: {"precision_sum": 0, "recall_sum": 0, "latency_sum": 0, "count": 0}))

    # JSON-Daten laden
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Verarbeitung der Einträge aus der JSON-Datei
    for entry in data:
        correct_pattern = entry.get("correct_pattern")
        llm_key = entry.get("llm_key")
        prompt_mode = entry.get("prompt_mode")
        precision = entry.get("precision", 0)
        recall = entry.get("recall", 0)
        latency = entry.get("latency", 0)

        # Gruppenschlüssel für Aggregation
        key = (llm_key, prompt_mode)

        # Werte aufsummieren
        results[correct_pattern][key]["precision_sum"] += precision
        results[correct_pattern][key]["recall_sum"] += recall
        results[correct_pattern][key]["latency_sum"] += latency
        results[correct_pattern][key]["count"] += 1

    # Berechnung der Durchschnittswerte
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

    # Ergebnis als JSON speichern
    with open(output_path, 'w') as outfile:
        json.dump(averages, outfile, indent=4)

    return output_path

def main():
    """
    Führt die Berechnung der Durchschnittswerte aus und speichert die Ergebnisse.
    """
        
    # Definierte Dateipfade für Eingabe und Ausgabe
    input_file_path = "eval/results/sorted_evaluation_new_sysPrompt_all_traces.json"  # Originale Eingabedatei
    output_file_path = "eval/eval_grouped_by_pattern_new_sysPrompt_all_traces.json"  # Datei für aggregierte Ergebnisse

    # Durchschnittswerte berechnen und speichern
    output_path = calculate_averages(input_file_path, output_file_path)
    print(f"Die aggregierten Ergebnisse wurden in der Datei '{output_path}' gespeichert.")

# Falls das Skript direkt ausgeführt wird, starte die `main()`-Funktion
if __name__ == "__main__":
    main()
